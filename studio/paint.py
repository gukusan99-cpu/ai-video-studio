"""Nền "tranh sơn dầu" tự vẽ – không dùng ảnh chụp, không cần GPU/API.

Bước 1  dựng phong cảnh thô bằng thủ tục (bầu trời, núi đá vôi, thung lũng, sông, ruộng, thành luỹ, rừng...).
Bước 2  "vẽ lại" bằng hàng chục nghìn nét cọ (thuật toán Hertzmann: cọ to → cọ nhỏ, nét chạy theo hướng
        vuông góc gradient), màu lấy từ ảnh thô.
Bước 3  vân vải canvas + nổi sơn (impasto) + nét mực phác nhẹ (giống nền kênh vẽ tay) + tối góc.

Dùng trong episode JSON:  {"fn": "oil_bg", "args": {"kind": "karst_valley", "time": "dusk", "seed": 3}}
Kết quả được cache ở assets/paint/<kind>-<time>-<seed>.jpg (lần sau dùng lại ngay).

    python -m studio.paint karst_valley dusk 3      # vẽ thử 1 nền
    python -m studio.paint --sheet                  # vẽ bảng mẫu tất cả các nền
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "assets" / "paint"
W, H = 1920, 1080

KINDS = ("karst_valley", "gorge", "rice_field", "river", "citadel", "forest_camp", "sea", "mountain_pass")
TIMES = ("day", "dusk", "dawn", "night", "storm")

PAL = {  # trời trên, trời chân, mặt trời, ánh, ánh sáng chung (nhân), sương
    "day":   ((92, 148, 196), (214, 222, 214), (255, 246, 214), 0.25, 1.00, (200, 212, 214)),
    "dusk":  ((70, 62, 112), (246, 160, 86), (255, 214, 140), 0.65, 0.88, (226, 160, 120)),
    "dawn":  ((120, 150, 190), (248, 206, 168), (255, 236, 200), 0.45, 0.95, (230, 210, 196)),
    "night": ((14, 22, 46), (52, 66, 98), (230, 232, 210), 0.20, 0.45, (60, 74, 104)),
    "storm": ((70, 78, 84), (150, 156, 150), (210, 210, 200), 0.05, 0.70, (150, 156, 152)),
}


# ------------------------------------------------------------------ tiện ích nhiễu
def _noise1d(n: int, rnd: np.random.Generator, octaves: int = 5, base: int = 6) -> np.ndarray:
    out = np.zeros(n)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        k = base * 2 ** o
        pts = rnd.uniform(-1, 1, k + 2)
        out += amp * np.interp(np.linspace(0, k, n), np.arange(k + 2), pts)
        tot += amp
        amp *= 0.5
    return out / tot


def _noise2d(h: int, w: int, rnd: np.random.Generator, scale: int = 8, octaves: int = 4) -> np.ndarray:
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        sh, sw = max(2, scale * 2 ** o * h // w), scale * 2 ** o
        g = rnd.uniform(-1, 1, (sh, sw)).astype(np.float32)
        out += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    return out / tot


def _mix(a, b, t):
    return np.asarray(a, np.float32) * (1 - t) + np.asarray(b, np.float32) * t


def _fill(img: np.ndarray, mask: np.ndarray, color, tex: np.ndarray | None = None, tex_amp: float = 18):
    c = np.asarray(color, np.float32)[None, None, :]
    m = mask[..., None].astype(np.float32)
    col = np.broadcast_to(c, img.shape).copy()
    if tex is not None:
        col += tex[..., None] * tex_amp
    img[:] = img * (1 - m) + col * m


def _ridge_mask(ys: np.ndarray) -> np.ndarray:
    """ys[x] = đỉnh dãy núi tại cột x → mask (H,W) của vùng dưới đường đó."""
    yy = np.arange(H)[:, None]
    return (yy >= ys[None, :]).astype(np.float32)


def _soft(mask: np.ndarray, k: int = 3) -> np.ndarray:
    return cv2.GaussianBlur(mask, (0, 0), k)


# ------------------------------------------------------------------ các thành phần cảnh
def _sky(time: str, rnd, sun_x: float = 0.7, sun_y: float = 0.32, horizon: float = 0.62) -> np.ndarray:
    top, bot, sun, glow, _, _ = PAL[time]
    t = np.clip(np.linspace(0, 1, H) / horizon, 0, 1) ** 1.25
    img = _mix(top, bot, t[:, None, None]) * np.ones((1, W, 1), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx / W - sun_x) ** 2 * 3.2 + (yy / H - sun_y) ** 2)
    g = np.exp(-d * 5.5)[..., None] * glow
    img = img * (1 - g) + np.asarray(sun, np.float32) * g
    if time != "storm":
        disk = _soft((d < 0.035).astype(np.float32), 2)[..., None]
        img = img * (1 - disk) + np.asarray(sun, np.float32) * disk
    # mây: nhiễu dải ngang
    n = _noise2d(H, W, rnd, 5, 5)
    band = np.exp(-((yy / H - rnd.uniform(0.12, 0.3)) / 0.16) ** 2)
    cl = np.clip((n * 1.6 + 0.15) * band, 0, 1) ** 1.4
    if time == "storm":
        cl = np.clip(n * 1.2 + 0.55, 0, 1) * (1 - t[:, None] * 0.4)
    ccol = _mix(bot, (255, 255, 255), 0.45) if time not in ("night", "storm") else _mix(top, bot, 0.5)
    shade = _mix(ccol, top, 0.35)
    cl3 = cl[..., None] * 0.85
    lit = np.clip(np.roll(n, 14, axis=0) - n, -1, 1)[..., None]
    img = img * (1 - cl3) + (ccol * (0.75 + 0.25 * lit) + shade * (0.25 - 0.25 * lit)) * cl3
    if time == "night":  # sao
        st = rnd.random((H, W)) > 0.9993
        img[st & (yy < H * 0.5)] = (240, 240, 220)
    return img


def _range(img, rnd, base: float, amp: float, color, haze: float, time: str, karst: bool = False,
           n_towers: int = 9, tex_scale: int = 10, x_from: float = 0, x_to: float = 1):
    """Một dãy núi. karst=True: những khối đá vôi tháp tròn (đặc trưng Lạng Sơn/Ninh Bình)."""
    xs = np.linspace(0, 1, W)
    if karst:
        ys = np.full(W, base * H + amp * H * 0.25)
        for _ in range(n_towers):
            cx = rnd.uniform(x_from, x_to)
            wdt = rnd.uniform(0.03, 0.08)
            hgt = rnd.uniform(0.55, 1.0) * amp * H
            prof = np.exp(-np.abs((xs - cx) / wdt) ** rnd.uniform(2.2, 3.4))
            ys = np.minimum(ys, base * H + amp * H * 0.25 - hgt * prof)
        ys += _noise1d(W, rnd, 6, 30) * amp * H * 0.05
    else:
        ys = base * H - (_noise1d(W, rnd, 6, 3) * 0.5 + 0.5) * amp * H
    m = _ridge_mask(ys)
    sky_col = PAL[time][5]
    col = _mix(color, sky_col, haze) * PAL[time][4]
    tex = _noise2d(H, W, rnd, tex_scale, 4)
    # sáng một sườn (ánh từ phải)
    side = np.clip(np.gradient(ys)[None, :] * 0.06, -1, 1)
    _fill(img, _soft(m, 1.5), col, tex + side * 0.0, 22 * (1 - haze))
    # khối: sườn phải (hướng nắng) sáng, sườn trái tối; vệt đá dọc
    bm = cv2.GaussianBlur(m, (0, 0), 18)
    lit = np.clip(cv2.Sobel(bm, cv2.CV_32F, 1, 0, ksize=5) * -6, -1, 1)
    streak = cv2.resize(rnd.uniform(-1, 1, (H // 40, W // 3)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    k3 = (lit[..., None] * 34 * (1 - haze) + streak[..., None] * 14 * (1 - haze)) * m[..., None]
    img[:] = img + k3 * np.array([1.0, 0.95, 0.85], np.float32)
    # vệt cây cối lấm tấm trên sườn núi
    if haze < 0.5:
        speck = (_noise2d(H, W, rnd, 60, 2) > 0.25).astype(np.float32) * m
        _fill(img, _soft(speck, 1.2) * 0.5, _mix(col, (20, 40, 20), 0.35))
    # mép đỉnh sáng
    top_line = _soft(np.clip(m - np.roll(m, 6, axis=0), 0, 1), 2) * (1 - haze) * 0.5
    _fill(img, top_line, _mix(col, PAL[time][2], 0.5))
    return ys


def _ground(img, rnd, y0: float, color, time: str, tex_scale=14):
    m = np.zeros((H, W), np.float32)
    m[int(y0 * H):] = 1
    m = _soft(m, 3)
    tex = _noise2d(H, W, rnd, tex_scale, 5)
    col = np.asarray(color, np.float32) * PAL[time][4]
    _fill(img, m, col, tex, 26)
    # gần thì đậm hơn
    yy = np.arange(H)[:, None, None] / H
    dark = np.clip((yy - y0) / (1 - y0 + 1e-6), 0, 1) * 0.25 * m[..., None]
    img[:] = img * (1 - dark)


def _river(img, rnd, y_top: float, time: str, width0=0.05, width1=0.6, cx0=0.55, cx1=0.4):
    sky_col = _mix(PAL[time][1], PAL[time][0], 0.3)
    yy = np.arange(H)
    mask = np.zeros((H, W), np.float32)
    wig = _noise1d(H, rnd, 4, 3)
    for y in range(int(y_top * H), H):
        t = (y - y_top * H) / (H - y_top * H)
        c = (cx0 * (1 - t) + cx1 * t + wig[y] * 0.05 + math.sin(t * 4.2) * 0.12 * t) * W
        w = (width0 * (1 - t) + width1 * t) * W / 2
        mask[y, max(0, int(c - w)):min(W, int(c + w))] = 1
    mask = _soft(mask, 3)
    rw = cv2.resize(rnd.uniform(-1, 1, (H // 7, W // 90)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    ripple = np.sin(rw * 5 + np.arange(H)[:, None] * 0.12)
    _fill(img, mask, _mix(sky_col, (40, 70, 90), 0.35) * PAL[time][4], ripple.astype(np.float32), 16)
    sun_ref = np.exp(-((np.arange(W)[None, :] / W - 0.68) / 0.03) ** 2) * mask * (ripple > 0.4) * PAL[time][3]
    _fill(img, sun_ref.astype(np.float32) * 0.8, PAL[time][2])
    return mask


def _rice(img, rnd, y0: float, time: str):
    """Ruộng bậc phẳng: dải xanh/vàng nối tiếp có bờ, thu nhỏ dần về xa."""
    import PIL.Image as Im
    import PIL.ImageDraw as D
    lay = Im.new("RGBA", (W, H), (0, 0, 0, 0))
    d = D.Draw(lay)
    y = y0 * H
    k = 0
    greens = [(118, 156, 64), (150, 170, 70), (196, 180, 82), (92, 140, 70)]
    while y < H:
        hgt = 10 + (y - y0 * H) * 0.22
        c = greens[k % len(greens)]
        c = tuple(int(v * PAL[time][4]) for v in c)
        off = rnd.uniform(-30, 30)
        d.polygon([(-50, y), (W + 50, y + off * 0.3), (W + 50, y + hgt + off * 0.3), (-50, y + hgt)], fill=c + (255,))
        d.line([(-50, y), (W + 50, y + off * 0.3)], fill=(90, 72, 44, 255), width=max(2, int(hgt * 0.08)))
        y += hgt
        k += 1
    a = np.asarray(lay, np.float32)
    m = a[..., 3] / 255
    tex = _noise2d(H, W, rnd, 50, 3)[..., None] * 18
    img[:] = img * (1 - m[..., None]) + (a[..., :3] + tex) * m[..., None]


def _trees(img, rnd, n: int, y_from: float, y_to: float, size: float, time: str, x_from=0.0, x_to=1.0,
           palm: bool = False, dark: float = 0.0):
    import PIL.Image as Im
    import PIL.ImageDraw as D
    lay = Im.new("RGBA", (W, H), (0, 0, 0, 0))
    d = D.Draw(lay)
    L = PAL[time][4] * (1 - dark)
    pts = sorted([(rnd.uniform(x_from, x_to) * W, rnd.uniform(y_from, y_to) * H) for _ in range(n)], key=lambda p: p[1])
    for x, y in pts:
        s = size * (0.6 + 0.8 * (y / H)) * rnd.uniform(0.7, 1.3)
        g = rnd.uniform(0.75, 1.1)
        base = (int(46 * g * L), int(82 * g * L), int(40 * g * L))
        lite = (int(96 * g * L), int(140 * g * L), int(58 * g * L))
        d.line([(x, y), (x + rnd.uniform(-6, 6), y - s * 1.1)], fill=(int(70 * L), int(50 * L), int(34 * L), 255), width=max(3, int(s * 0.09)))
        if palm:
            for a in range(7):
                ang = math.pi * (1.05 + a * 0.15)
                ex, ey = x + math.cos(ang) * s * 0.9, y - s * 1.1 + math.sin(ang) * s * 0.35 + s * 0.2
                d.line([(x, y - s * 1.1), ((x + ex) / 2, (y - s * 1.25 + ey) / 2), (ex, ey)], fill=base + (255,), width=max(4, int(s * 0.12)), joint="curve")
            continue
        form = rnd.integers(0, 3)
        if form == 1:  # bụi tre
            for k in range(7):
                bx = x + (k - 3) * s * 0.07
                top = y - s * rnd.uniform(1.3, 1.8)
                d.line([(bx, y), (bx + (k - 3) * s * 0.12, top)], fill=(int(96 * L), int(130 * L), int(60 * L), 255), width=max(3, int(s * 0.05)))
                for j in range(5):
                    ly = y - (y - top) * (0.4 + j * 0.13)
                    lx = bx + (k - 3) * s * 0.12 * (0.4 + j * 0.13)
                    d.polygon([(lx, ly), (lx + s * 0.28 * (1 if j % 2 else -1), ly + s * 0.05), (lx, ly + s * 0.06)], fill=base + (255,))
            continue
        if form == 2:  # cây tùng/thông dáng đứng
            for j in range(4):
                w_ = s * (0.55 - j * 0.11)
                ty = y - s * (0.5 + j * 0.32)
                d.polygon([(x - w_, ty + s * 0.2), (x, ty - s * 0.32), (x + w_, ty + s * 0.2)], fill=(base if j % 2 else lite) + (255,))
            continue
        for _ in range(9):
            cx, cy = x + rnd.uniform(-0.5, 0.5) * s, y - s * 1.1 + rnd.uniform(-0.45, 0.25) * s
            r = s * rnd.uniform(0.28, 0.45)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=base + (255,))
        for _ in range(5):
            cx, cy = x + rnd.uniform(-0.3, 0.45) * s, y - s * 1.25 + rnd.uniform(-0.35, 0.05) * s
            r = s * rnd.uniform(0.14, 0.25)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=lite + (255,))
    a = np.asarray(lay, np.float32)
    m = a[..., 3:] / 255
    img[:] = img * (1 - m) + a[..., :3] * m


def _citadel(img, rnd, y_base: float, time: str, x0=0.18, x1=0.86):
    """Tường thành gạch đá + cổng có lầu mái cong (thành cổ thế kỷ 15, phong cách chung)."""
    import PIL.Image as Im
    import PIL.ImageDraw as D
    L = PAL[time][4]
    c = lambda r, g, b: (int(r * L), int(g * L), int(b * L), 255)
    lay = Im.new("RGBA", (W, H), (0, 0, 0, 0))
    d = D.Draw(lay)
    yb = y_base * H
    top = yb - 190
    d.polygon([(x0 * W, yb), (x0 * W + 30, top), (x1 * W - 30, top), (x1 * W, yb)], fill=c(150, 132, 110))
    for xx in range(int(x0 * W + 30), int(x1 * W - 30), 46):  # răng cưa
        d.rectangle([xx, top - 26, xx + 26, top], fill=c(150, 132, 110))
    for yy in range(int(top + 22), int(yb), 26):  # mạch gạch
        d.line([(x0 * W + 10, yy), (x1 * W - 10, yy)], fill=c(118, 102, 84), width=2)
    gx = (x0 + x1) / 2 * W
    d.rectangle([gx - 70, yb - 150, gx + 70, yb], fill=c(52, 40, 32))
    d.pieslice([gx - 70, yb - 220, gx + 70, yb - 80], 180, 360, fill=c(52, 40, 32))
    # lầu
    lt = top - 150
    d.rectangle([gx - 150, top - 90, gx + 150, top - 26], fill=c(160, 60, 44))
    for k in range(-2, 3):
        d.rectangle([gx + k * 56 - 8, top - 90, gx + k * 56 + 8, top - 26], fill=c(92, 40, 30))
    d.polygon([(gx - 240, top - 80), (gx - 200, top - 120), (gx - 120, lt + 20), (gx + 120, lt + 20), (gx + 200, top - 120),
               (gx + 240, top - 80), (gx + 150, top - 100), (gx - 150, top - 100)], fill=c(58, 52, 50))
    d.polygon([(gx - 120, lt + 20), (gx - 60, lt - 10), (gx + 60, lt - 10), (gx + 120, lt + 20)], fill=c(70, 62, 58))
    # cờ
    for fx in (x0 * W + 90, x1 * W - 90):
        d.line([(fx, top - 26), (fx, top - 160)], fill=c(70, 50, 34), width=6)
        d.polygon([(fx, top - 160), (fx + 70, top - 146), (fx, top - 124)], fill=c(196, 56, 40))
    a = np.asarray(lay, np.float32)
    m = a[..., 3:] / 255
    tex = _noise2d(H, W, rnd, 30, 3)[..., None] * 16
    img[:] = img * (1 - m) + (a[..., :3] + tex) * m


def _camp(img, rnd, y: float, time: str, n=5):
    import PIL.Image as Im
    import PIL.ImageDraw as D
    L = PAL[time][4]
    lay = Im.new("RGBA", (W, H), (0, 0, 0, 0))
    d = D.Draw(lay)
    for i in range(n):
        x = (0.12 + i * 0.76 / max(1, n - 1)) * W + rnd.uniform(-40, 40)
        yy = y * H + rnd.uniform(-20, 30)
        s = rnd.uniform(90, 130)
        d.polygon([(x - s, yy), (x, yy - s * 0.9), (x + s, yy)], fill=(int(196 * L), int(170 * L), int(120 * L), 255))
        d.polygon([(x - s * 0.2, yy), (x, yy - s * 0.5), (x + s * 0.2, yy)], fill=(int(70 * L), int(50 * L), int(36 * L), 255))
        d.line([(x, yy - s * 0.9), (x, yy - s * 1.3)], fill=(int(70 * L), int(50 * L), int(34 * L), 255), width=4)
        d.polygon([(x, yy - s * 1.3), (x + 40, yy - s * 1.22), (x, yy - s * 1.12)], fill=(int(220 * L), int(170 * L), int(40 * L), 255))
    a = np.asarray(lay, np.float32)
    m = a[..., 3:] / 255
    img[:] = img * (1 - m) + a[..., :3] * m


def _mist(img, rnd, y: float, h: float, op: float, time: str):
    yy = np.arange(H)[:, None] / H
    n = _noise2d(H, W, rnd, 6, 3)
    m = np.exp(-((yy - y) / h) ** 2) * np.clip(0.7 + n * 0.8, 0, 1) * op
    _fill(img, m.astype(np.float32), PAL[time][5])


def _sea(img, rnd, y0: float, time: str):
    m = np.zeros((H, W), np.float32)
    m[int(y0 * H):] = 1
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wave = cv2.resize(rnd.uniform(-1, 1, (H // 7, W // 90)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    wave = np.sin(wave * 5 + yy * 0.08)
    base = _mix(PAL[time][1], (36, 84, 112), 0.6) * PAL[time][4]
    _fill(img, m, base, wave, 20)
    ref = np.exp(-((xx / W - 0.68) / 0.05) ** 2) * m * (wave > 0.5) * PAL[time][3]
    _fill(img, ref.astype(np.float32) * 0.9, PAL[time][2])



def _foreground(img, rnd, time: str, y0: float = 0.9, corners: bool = True, rocks: int = 3):
    """Tiền cảnh: cỏ lau, đá, bụi tối ở hai góc – tạo khung tranh có chiều sâu."""
    import PIL.Image as Im
    import PIL.ImageDraw as D
    L = PAL[time][4]
    c = lambda r, g, b, a=255: (int(r * L), int(g * L), int(b * L), a)
    lay = Im.new("RGBA", (W, H), (0, 0, 0, 0))
    d = D.Draw(lay)
    for _ in range(rocks):
        x, y = rnd.uniform(0.05, 0.95) * W, rnd.uniform(y0, 1.0) * H
        r = rnd.uniform(40, 90)
        d.ellipse([x - r * 1.4, y - r, x + r * 1.4, y + r * 0.5], fill=c(108, 104, 96))
        d.ellipse([x - r * 0.9, y - r * 0.9, x + r * 0.5, y - r * 0.2], fill=c(150, 146, 134))
    for _ in range(700):
        x = rnd.uniform(-0.02, 1.02) * W
        y = H * (y0 + rnd.uniform(0, 1 - y0) ** 0.7 * (1 - y0) / max(1e-6, (1 - y0)) * (1 - y0) * 0 + rnd.uniform(0, 1.05 - y0))
        hgt = rnd.uniform(30, 90) * (0.6 + (y / H - y0) * 3)
        lean = rnd.uniform(-0.5, 0.5)
        g = rnd.uniform(0.7, 1.2)
        d.line([(x, y), (x + lean * hgt * 0.5, y - hgt * 0.6), (x + lean * hgt, y - hgt)],
               fill=c(60 * g, 96 * g, 44 * g), width=int(rnd.uniform(3, 6)), joint="curve")
    if corners:
        for side in (0, 1):
            for _ in range(12):
                x = (rnd.uniform(-0.05, 0.08) if side == 0 else rnd.uniform(0.92, 1.05)) * W
                y = rnd.uniform(0.74, 1.05) * H
                r = rnd.uniform(45, 95)
                g = rnd.uniform(0.85, 1.25)
                d.ellipse([x - r, y - r, x + r, y + r], fill=c(46 * g, 76 * g, 40 * g))
                d.ellipse([x - r * 0.5, y - r * 0.9, x + r * 0.3, y - r * 0.2], fill=c(80 * g, 116 * g, 56 * g))
    a = np.asarray(lay, np.float32)
    m = a[..., 3:] / 255
    img[:] = img * (1 - m) + a[..., :3] * m

# ------------------------------------------------------------------ dựng cảnh
def compose(kind: str, time: str = "day", seed: int = 1) -> np.ndarray:
    rnd = np.random.default_rng(seed * 101 + KINDS.index(kind))
    sun = {"dusk": (0.72, 0.5), "dawn": (0.25, 0.48), "night": (0.8, 0.18)}.get(time, (0.7, 0.25))
    img = _sky(time, rnd, *sun)
    if kind == "karst_valley":
        _range(img, rnd, 0.50, 0.30, (90, 110, 120), 0.65, time, karst=True, n_towers=14)
        _mist(img, rnd, 0.56, 0.05, 0.6, time)
        _range(img, rnd, 0.62, 0.42, (70, 96, 70), 0.30, time, karst=True, n_towers=10)
        _ground(img, rnd, 0.70, (104, 132, 64), time)
        _rice(img, rnd, 0.74, time)
        _trees(img, rnd, 14, 0.72, 0.80, 70, time)
        _foreground(img, rnd, time, 0.9)
    elif kind == "gorge":  # ải hẹp giữa hai vách núi (kiểu Chi Lăng)
        _range(img, rnd, 0.52, 0.25, (100, 116, 124), 0.6, time, karst=True, n_towers=8, x_from=0.3, x_to=0.7)
        _mist(img, rnd, 0.55, 0.06, 0.7, time)
        _ground(img, rnd, 0.62, (128, 120, 76), time)
        for side in (0, 1):
            xs = np.linspace(0, 1, W)
            edge = 0.30 + _noise1d(H, rnd, 5, 4) * 0.05
            m = np.zeros((H, W), np.float32)
            for y in range(H):
                e = edge[y] - 0.12 * (1 - y / H) * 0
                if side == 0:
                    m[y, :int((e + 0.08 * (y / H)) * W)] = 1
                else:
                    m[y, int((1 - e - 0.08 * (y / H)) * W):] = 1
            tex = _noise2d(H, W, rnd, 14, 5)
            _fill(img, _soft(m, 2), np.asarray((74, 84, 70)) * PAL[time][4], tex, 30)
        _trees(img, rnd, 18, 0.15, 0.95, 80, time, 0.0, 0.25)
        _trees(img, rnd, 18, 0.15, 0.95, 80, time, 0.75, 1.0)
        # con đường đất giữa ải
        path = np.zeros((H, W), np.float32)
        for y in range(int(0.62 * H), H):
            t = (y - 0.62 * H) / (0.38 * H)
            c = 0.5 + math.sin(t * 3) * 0.04
            w = 0.02 + 0.16 * t
            path[y, int((c - w) * W):int((c + w) * W)] = 1
        _fill(img, _soft(path, 4), np.asarray((166, 136, 94)) * PAL[time][4], _noise2d(H, W, rnd, 30, 3), 18)
    elif kind == "rice_field":
        _range(img, rnd, 0.55, 0.18, (100, 120, 130), 0.6, time)
        _range(img, rnd, 0.60, 0.14, (80, 110, 80), 0.35, time)
        _ground(img, rnd, 0.60, (120, 150, 70), time)
        _rice(img, rnd, 0.62, time)
        _trees(img, rnd, 10, 0.60, 0.64, 46, time, palm=False)
        _trees(img, rnd, 3, 0.62, 0.66, 80, time, 0.75, 0.95, palm=True)
        _foreground(img, rnd, time, 0.92, corners=False, rocks=0)
    elif kind == "river":
        _range(img, rnd, 0.52, 0.28, (96, 112, 124), 0.55, time, karst=True, n_towers=12)
        _range(img, rnd, 0.58, 0.20, (70, 100, 74), 0.3, time)
        _ground(img, rnd, 0.58, (96, 128, 66), time)
        _river(img, rnd, 0.58, time)
        _trees(img, rnd, 16, 0.6, 0.9, 70, time, 0.0, 0.25)
        _trees(img, rnd, 16, 0.6, 0.9, 70, time, 0.75, 1.0)
        _mist(img, rnd, 0.58, 0.04, 0.5, time)
        _foreground(img, rnd, time, 0.93, corners=False, rocks=2)
    elif kind == "citadel":
        _range(img, rnd, 0.55, 0.16, (100, 116, 128), 0.6, time)
        _ground(img, rnd, 0.62, (126, 128, 80), time)
        _citadel(img, rnd, 0.70, time)
        _trees(img, rnd, 10, 0.66, 0.74, 60, time, 0.0, 0.16)
        _trees(img, rnd, 10, 0.66, 0.74, 60, time, 0.86, 1.0)
        _foreground(img, rnd, time, 0.9, corners=False, rocks=2)
    elif kind == "forest_camp":
        _range(img, rnd, 0.52, 0.22, (90, 110, 110), 0.55, time, karst=True)
        _ground(img, rnd, 0.62, (100, 122, 64), time)
        _trees(img, rnd, 30, 0.58, 0.66, 70, time)
        _camp(img, rnd, 0.76, time)
        _trees(img, rnd, 8, 0.86, 1.02, 160, time, 0.0, 0.18, dark=0.25)
        _trees(img, rnd, 8, 0.86, 1.02, 160, time, 0.84, 1.0, dark=0.25)
    elif kind == "sea":
        _range(img, rnd, 0.56, 0.08, (90, 110, 120), 0.7, time, karst=True, n_towers=6, x_from=0.0, x_to=0.35)
        _sea(img, rnd, 0.56, time)
    elif kind == "mountain_pass":
        _range(img, rnd, 0.45, 0.25, (110, 124, 140), 0.7, time)
        _range(img, rnd, 0.58, 0.30, (84, 104, 90), 0.45, time)
        _range(img, rnd, 0.74, 0.30, (70, 90, 60), 0.15, time)
        _ground(img, rnd, 0.80, (110, 118, 70), time)
        _trees(img, rnd, 14, 0.74, 0.86, 60, time)
        _foreground(img, rnd, time, 0.9, rocks=4)
    else:
        raise ValueError(f"kind phải thuộc {KINDS}")
    return np.clip(img, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ nét cọ sơn dầu
def paint_strokes(src: np.ndarray, seed: int = 1, radii=(40, 22, 12, 6), thresh: float = 12.0) -> np.ndarray:
    """Vẽ lại ảnh bằng nét cọ (Hertzmann 1998, rút gọn): cọ to phủ nền, cọ nhỏ chỉ ở nơi còn sai lệch."""
    rnd = np.random.default_rng(seed)
    canvas = np.full_like(src, 0)
    canvas[:] = cv2.GaussianBlur(src, (0, 0), 30)
    srcf = src.astype(np.float32)
    first = True
    for R in radii:
        ref = cv2.GaussianBlur(srcf, (0, 0), max(1.0, R * 0.5))
        gray = cv2.cvtColor(ref.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        gx, gy = cv2.GaussianBlur(gx, (0, 0), R), cv2.GaussianBlur(gy, (0, 0), R)
        mag = np.hypot(gx, gy)
        diff = np.linalg.norm(canvas.astype(np.float32) - ref, axis=2)
        step = max(2, int(R * 0.8))
        hh, ww = H // step, W // step
        blk = cv2.resize(diff[:hh * step, :ww * step], (ww, hh), interpolation=cv2.INTER_AREA)
        cy, cx = np.nonzero(blk > (0 if first else thresh))
        order = rnd.permutation(len(cy))
        jit = rnd.uniform(0, step, (len(cy), 2))
        L = R * 4.2
        for i in order:
            x = int(cx[i] * step + jit[i, 0])
            y = int(cy[i] * step + jit[i, 1])
            if x >= W or y >= H:
                continue
            col = ref[y, x] * rnd.uniform(0.94, 1.06) + rnd.normal(0, 3, 3)
            pts = [(x, y)]
            hz = rnd.uniform(-0.12, 0.12)
            px, py = float(x), float(y)
            dx0, dy0 = 0.0, 0.0
            for _ in range(3):  # nét cong nhẹ theo trường hướng
                ix, iy = min(W - 1, max(0, int(px))), min(H - 1, max(0, int(py)))
                m_ = mag[iy, ix]
                wgt = min(1.0, m_ / 12.0)  # vùng phẳng (trời, nước): nét gần như ngang
                ex, ey = -gy[iy, ix] / (m_ + 1e-6), gx[iy, ix] / (m_ + 1e-6)
                if ex < 0:
                    ex, ey = -ex, -ey
                dx, dy = ex * wgt + (1 - wgt), ey * wgt + (1 - wgt) * hz
                n = math.hypot(dx, dy) + 1e-6
                dx, dy = dx / n, dy / n
                if dx * dx0 + dy * dy0 < 0:
                    dx, dy = -dx, -dy
                px, py = px + dx * L / 4, py + dy * L / 4
                dx0, dy0 = dx, dy
                pts.append((int(px), int(py)))
            c = tuple(float(v) for v in np.clip(col, 0, 255))
            cv2.polylines(canvas, [np.array(pts, np.int32)], False, c, thickness=max(2, R), lineType=cv2.LINE_AA)
        first = False
    return canvas


def _canvas_texture(rnd) -> np.ndarray:
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    weave = (np.sin(xx * 1.9) * np.sin(yy * 1.9)) * 0.5 + rnd.normal(0, 0.6, (H, W)).astype(np.float32)
    weave = cv2.GaussianBlur(weave, (0, 0), 0.7)
    return weave


def finish(painted: np.ndarray, src: np.ndarray, seed: int = 1, ink: float = 0.5, impasto: float = 1.0) -> np.ndarray:
    rnd = np.random.default_rng(seed + 7)
    p = painted.astype(np.float32)
    # nổi sơn: ánh sáng chiếu từ trên-trái lên "độ cao" = độ sáng chi tiết nhỏ của nét cọ
    g = cv2.cvtColor(painted, cv2.COLOR_RGB2GRAY).astype(np.float32)
    hp = g - cv2.GaussianBlur(g, (0, 0), 3)
    relief = cv2.filter2D(hp, -1, np.array([[1, 0, 0], [0, 0, 0], [0, 0, -1]], np.float32))
    p += relief[..., None] * 0.55 * impasto
    # vân vải
    p += _canvas_texture(rnd)[..., None] * 6
    # nét mực phác nhẹ theo đường viền lớn của cảnh
    if ink > 0:
        e = cv2.Canny(cv2.GaussianBlur(src, (0, 0), 2.2), 30, 70)
        e = cv2.dilate(e, np.ones((2, 2), np.uint8))
        noise = _noise2d(H, W, rnd, 30, 2)
        e = (e.astype(np.float32) / 255) * np.clip(0.6 + noise, 0, 1)
        e = cv2.GaussianBlur(e, (0, 0), 0.8)
        p = p * (1 - e[..., None] * ink) + np.array([40, 28, 22], np.float32) * e[..., None] * ink
    # tối góc + ấm nhẹ như sơn dầu
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.28 * (((xx / W - 0.5) * 1.3) ** 2 + ((yy / H - 0.5) * 1.6) ** 2)
    p = p * v[..., None]
    p = p * np.array([1.03, 1.0, 0.95], np.float32)
    return np.clip(p, 0, 255).astype(np.uint8)


def oil(kind: str, time: str = "day", seed: int = 1, ink: float = 0.5, force: bool = False) -> Path:
    """Tạo (hoặc lấy từ cache) nền sơn dầu, trả về đường dẫn JPG 1920x1080."""
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"{kind}-{time}-{seed}{'' if ink == 0.5 else f'-i{int(ink*100)}'}.jpg"
    if out.exists() and not force:
        return out
    src = compose(kind, time, seed)
    painted = paint_strokes(src, seed)
    fin = finish(painted, src, seed, ink)
    cv2.imwrite(str(out), cv2.cvtColor(fin, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    return out


def sheet(out: Path, combos=None):
    combos = combos or [("karst_valley", "day"), ("gorge", "dusk"), ("rice_field", "dawn"), ("river", "day"),
                        ("citadel", "dusk"), ("forest_camp", "night"), ("sea", "dusk"), ("mountain_pass", "storm")]
    tiles = []
    for k, t in combos:
        p = oil(k, t, 1)
        im = cv2.resize(cv2.imread(str(p)), (640, 360), interpolation=cv2.INTER_AREA)
        cv2.putText(im, f"{k} / {t}", (14, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4, cv2.LINE_AA)
        cv2.putText(im, f"{k} / {t}", (14, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        tiles.append(im)
    while len(tiles) % 3:
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
    cv2.imwrite(str(out), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 90])
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--sheet":
        print(sheet(ROOT / "channel" / "oil_backgrounds.jpg"))
    else:
        k = a[0] if a else "karst_valley"
        t = a[1] if len(a) > 1 else "day"
        s = int(a[2]) if len(a) > 2 else 1
        print(oil(k, t, s, force=True))
