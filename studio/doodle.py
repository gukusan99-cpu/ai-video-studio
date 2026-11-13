"""Bộ hình "doodle" (phong cách vẽ tay hài hước, ghép ảnh thật, nhiều hiệu ứng) – dùng cho format "fun".

- Nhân vật "hình nhộng": thân trụ, đầu to, mắt lờ đờ tỉnh bơ; nét vẽ tay rung nhẹ (SVG turbulence).
- Đất nước thành nhân vật: hình bản đồ có mắt, lông mày, miệng.
- Nền ảnh thật (Wikimedia Commons, giấy phép tự do) + sương/cỏ tiền cảnh che chi tiết hiện đại.
- Hiệu ứng: chữ BÙM/TÙNG, đường tốc độ, chớp sáng, emoji meme, mũi tên chú thích.
"""
from __future__ import annotations

import base64
import io
import math
import random
from pathlib import Path

from studio import svgart as A
from studio import svgextra as X

INK = "#1C1612"
ROOT = Path(__file__).resolve().parent.parent

WOBBLE = ('<filter id="wob" x="-10%" y="-10%" width="120%" height="120%">'
          '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/>'
          '<feDisplacementMap in="SourceGraphic" scale="4"/></filter>')


def _wob(inner: str) -> str:
    return f'<defs>{WOBBLE}</defs><g filter="url(#wob)">{inner}</g>'


# ------------------------------------------------------------------ ảnh thật
def photo(file: str, crop: list | None = None, x: float = 0, y: float = 0, w: float | None = None, h: float | None = None,
          tint: str = "", tint_op: float = 0.0, blur: float = 0) -> str:
    """Ảnh nền thật. crop = [x0,y0,x1,y1] theo tỉ lệ 0–1 của ảnh gốc. Tự phủ kín khung (cover)."""
    from PIL import Image, ImageFilter
    w, h = w or A.W, h or A.H
    im = Image.open(ROOT / file).convert("RGB")
    if crop:
        W0, H0 = im.size
        im = im.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
    l, t = (im.width - int(w)) // 2, (im.height - int(h)) // 2
    im = im.crop((l, t, l + int(w), t + int(h)))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86)
    b64 = base64.b64encode(buf.getvalue()).decode()
    out = f'<image href="data:image/jpeg;base64,{b64}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
    if tint:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{tint}" opacity="{tint_op}"/>'
    return out


def fg_grass(y: float = 980, color: str = "#2E4A2C", seed: int = 1, h: float = 140) -> str:
    """Cỏ + bụi cây tiền cảnh (che đường/xe hiện đại trong ảnh thật)."""
    rnd = random.Random(seed)
    W, H = A.W, A.H
    out = f'<path d="M0 {y} ' + " ".join(f"Q{i*120+60} {y - rnd.uniform(20, h*0.5):.0f} {i*120+120} {y - rnd.uniform(0, 30):.0f}" for i in range(17)) + f' L{W} {H} L0 {H} Z" fill="{color}"/>'
    for i in range(90):
        gx = rnd.uniform(0, W)
        out += f'<path d="M{gx:.0f} {H} q{rnd.uniform(-14, 14):.0f} -{h*0.6:.0f} {rnd.uniform(-30, 30):.0f} -{rnd.uniform(h*0.6, h*1.2):.0f}" stroke="#203A22" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return out


def mist_band(y: float, h: float = 260, op: float = 0.75) -> str:
    return (f'<defs><linearGradient id="mb{int(y)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF1EE" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#EEF1EE" stop-opacity="{op}"/><stop offset="1" stop-color="#EEF1EE" stop-opacity="{op*0.9}"/></linearGradient></defs>'
            f'<rect x="0" y="{y}" width="{A.W}" height="{h}" fill="url(#mb{int(y)})"/>')


# ------------------------------------------------------------------ nhân vật hình nhộng
OUTFITS = {
    #            áo,        viền/đai,  mũ
    "dv_soldier": ("#C98B2E", "#7A4E1A", "non"),
    "peasant": ("#7A5A3A", "#4A3424", "non"),
    "minh_soldier": ("#C4453C", "#7A1E18", "minh_helmet"),
    "lieuthang": ("#B5302A", "#F1C232", "general"),
    "tranluu": ("#6E7A4A", "#3A4024", "dv_helmet"),
    "leloi": ("#E9A92B", "#9A6A12", "khan"),
    "scholar": ("#3F6A8A", "#22384A", "scholar"),
}

FACES = ("deadpan", "smug", "angry", "shock", "panic", "cry", "wink", "happy", "cool")


def _face(expr: str, skin: str = "#F0C9A0") -> str:
    I = INK
    lid = '<path d="M-26 -8 h18 M8 -8 h18" stroke="#1C1612" stroke-width="4" stroke-linecap="round"/>'  # mí trên lờ đờ
    eye = lambda cx, r=5: f'<circle cx="{cx}" cy="-2" r="{r}" fill="{I}"/>'
    out = ""
    if expr == "deadpan":
        out = lid + eye(-17, 4) + eye(17, 4) + f'<path d="M-10 26 h20" stroke="{I}" stroke-width="4" stroke-linecap="round"/>'
    elif expr == "smug":
        out = (lid + '<path d="M-26 -14 L-8 -10 M8 -10 L26 -14" stroke="#1C1612" stroke-width="4"/>' + eye(-15, 4) + eye(19, 4)
               + f'<path d="M-12 24 q14 10 26 -4" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    elif expr == "angry":
        out = (f'<path d="M-30 -20 L-6 -8 M6 -8 L30 -20" stroke="{I}" stroke-width="6" stroke-linecap="round"/>' + eye(-16) + eye(16)
               + f'<path d="M-14 30 q14 -14 28 0z" fill="#5A1A1E" stroke="{I}" stroke-width="3"/>')
    elif expr == "shock":
        out = ('<circle cx="-17" cy="-4" r="11" fill="#fff" stroke="#1C1612" stroke-width="3"/><circle cx="17" cy="-4" r="11" fill="#fff" stroke="#1C1612" stroke-width="3"/>'
               + eye(-17, 4) + eye(17, 4) + f'<ellipse cx="0" cy="30" rx="10" ry="14" fill="#5A1A1E" stroke="{I}" stroke-width="3"/>')
    elif expr == "panic":
        out = ('<circle cx="-17" cy="-4" r="10" fill="#fff" stroke="#1C1612" stroke-width="3"/><circle cx="17" cy="-4" r="10" fill="#fff" stroke="#1C1612" stroke-width="3"/>'
               + eye(-19, 3) + eye(15, 3) + f'<path d="M-14 30 q7 -8 14 0 t14 0" stroke="{I}" stroke-width="4" fill="none"/>'
               + '<path d="M34 -30 q8 12 0 18 q-8 -6 0 -18z" fill="#7FD0F2" stroke="#2B6F8F" stroke-width="2"/>')
    elif expr == "cry":
        out = (lid + eye(-17, 3) + eye(17, 3) + f'<path d="M-12 32 q12 -12 24 0" stroke="{I}" stroke-width="4" fill="none"/>'
               + '<path d="M-20 4 q-4 20 0 34 M20 4 q4 20 0 34" stroke="#7FD0F2" stroke-width="6" fill="none" stroke-linecap="round"/>')
    elif expr == "wink":
        out = (eye(-17) + '<path d="M8 -2 q9 -7 18 0" stroke="#1C1612" stroke-width="4" fill="none"/>'
               + f'<path d="M-12 24 q14 12 26 -2" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    elif expr == "happy":
        out = ('<path d="M-26 -2 q9 -9 18 0 M8 -2 q9 -9 18 0" stroke="#1C1612" stroke-width="4" fill="none"/>'
               + f'<path d="M-16 20 q16 20 32 0z" fill="#5A1A1E" stroke="{I}" stroke-width="3"/>')
    elif expr == "cool":  # kính râm "ngầu"
        out = (f'<path d="M-34 -12 h68 v6 q-2 16 -16 16 h-6 q-10 0 -12 -12 h-4 q-2 12 -12 12 h-6 q-14 0 -16 -16 z" fill="{I}"/>'
               '<path d="M-26 -8 l8 -4 M10 -8 l8 -4" stroke="#fff" stroke-width="3" opacity=".8"/>'
               + f'<path d="M-12 26 q14 8 26 -2" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    return out


def _hat(kind: str, rim: str) -> str:
    I = INK
    return {
        "non": f'<path d="M-66 -40 L0 -104 L66 -40 Z" fill="#E6C98A" stroke="{I}" stroke-width="4" stroke-linejoin="round"/><path d="M-34 -58 L0 -92 M34 -58 L0 -92" stroke="#B89A5A" stroke-width="3"/>',
        "minh_helmet": f'<path d="M-46 -30 C-50 -100 50 -100 46 -30 Z" fill="#8F99A0" stroke="{I}" stroke-width="4"/><path d="M-52 -30 h104" stroke="{I}" stroke-width="6"/><path d="M0 -96 v-18" stroke="{I}" stroke-width="4"/><path d="M-10 -114 q10 -26 20 0z" fill="#D2352C" stroke="{I}" stroke-width="3"/>',
        "general": f'<path d="M-50 -28 C-54 -110 54 -110 50 -28 Z" fill="#A8B0B5" stroke="{I}" stroke-width="4"/><path d="M-58 -28 h116" stroke="{rim}" stroke-width="8"/><path d="M0 -104 v-16" stroke="{I}" stroke-width="4"/><path d="M-22 -118 q22 -50 44 0z" fill="#D2352C" stroke="{I}" stroke-width="3"/>',
        "dv_helmet": f'<path d="M-46 -30 C-48 -96 48 -96 46 -30 Z" fill="#7C8A6A" stroke="{I}" stroke-width="4"/><path d="M0 -92 l-8 -20 h16z" fill="#D62F3A"/>',
        "khan": f'<path d="M-44 -34 C-48 -92 48 -92 44 -34 Z" fill="#1E1A17" stroke="{I}" stroke-width="4"/><path d="M-44 -44 h88" stroke="{rim}" stroke-width="7"/>',
        "scholar": f'<path d="M-40 -34 L-36 -92 L36 -92 L40 -34 Z" fill="#1E1A17" stroke="{I}" stroke-width="4"/><path d="M-56 -60 h112" stroke="#1E1A17" stroke-width="9" stroke-linecap="round"/>',
    }[kind]


def dude(x: float, y: float, s: float = 1.0, outfit: str = "dv_soldier", expr: str = "deadpan", flip: bool = False,
         item: str = "", beard: str = "", wobble: bool = True, lean: float = 0, label: str = "") -> str:
    """Nhân vật hình nhộng. item: '' | spear | sword | flag | bow | scroll. beard: '' | long | mustache."""
    shirt, rim, hat = OUTFITS[outfit]
    I = INK
    sx = -s if flip else s
    items = {
        "spear": f'<path d="M46 30 L62 -230" stroke="#5A3A22" stroke-width="7"/><path d="M62 -230 l-8 -26 l18 4z" fill="#C9D0D4" stroke="{I}" stroke-width="2"/>',
        "sword": f'<path d="M40 -10 L86 -96" stroke="#C9D0D4" stroke-width="8" stroke-linecap="round"/><path d="M34 -2 L52 -20" stroke="{I}" stroke-width="8"/>',
        "flag": f'<path d="M46 40 L46 -230" stroke="#5A3A22" stroke-width="7"/><path d="M46 -230 q60 -14 110 8 q-50 20 -110 44z" fill="{rim if outfit.startswith("minh") or outfit == "lieuthang" else "#E9A92B"}" stroke="{I}" stroke-width="3"/>',
        "bow": f'<path d="M46 -110 Q96 -40 46 30" stroke="#6B4226" stroke-width="7" fill="none"/><path d="M46 -110 L46 30" stroke="#ddd" stroke-width="2"/>',
        "scroll": f'<rect x="30" y="-40" width="70" height="50" rx="6" fill="#F3E3BC" stroke="{I}" stroke-width="3"/>',
    }.get(item, "")
    beard_svg = {
        "long": f'<path d="M-24 34 Q0 110 24 34 Q0 50 -24 34Z" fill="#2A2420" stroke="{I}" stroke-width="2"/>',
        "mustache": f'<path d="M-26 18 Q-10 8 0 16 Q10 8 26 18 Q12 26 0 22 Q-12 26 -26 18Z" fill="#2A2420"/>',
    }.get(beard, "")
    # thân trụ cao (y từ -96 tới 40), đầu tâm (0,-150), mũ dời theo đầu
    body = (f'<ellipse cx="0" cy="44" rx="58" ry="10" fill="#000" opacity=".22"/>'
            f'<path d="M-44 -96 C-52 -96 -56 -84 -56 -70 L-50 34 Q0 50 50 34 L56 -70 C56 -84 52 -96 44 -96 Z" fill="{shirt}" stroke="{I}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M-54 -20 Q0 -8 54 -20" stroke="{rim}" stroke-width="8" fill="none"/>'
            f'<path d="M0 -94 V30" stroke="{rim}" stroke-width="3" opacity=".7"/>'
            f'<path d="M-30 -96 L0 -60 L30 -96" fill="none" stroke="#F4EEDD" stroke-width="6"/>' + items
            + f'<ellipse cx="0" cy="-150" rx="44" ry="48" fill="#F0C9A0" stroke="{I}" stroke-width="5"/>'
            f'<g transform="translate(0 -150) scale(.92)">{_face(expr)}{beard_svg}</g>'
            f'<g transform="translate(0 {-152 if hat in ("minh_helmet", "general", "dv_helmet", "khan", "scholar") else -146})">{_hat(hat, rim)}</g>')
    inner = f'<g transform="translate({x:.0f} {y:.0f}) rotate({lean}) scale({sx:.3f} {s:.3f})">{body}</g>'
    lab = ""
    if label:
        lab = X.map_tag(label, x, y + 60 * s + 34, 28, fill="#FFF7E2", color=INK).replace('opacity=".92"', 'stroke="#1C1612" stroke-width="3"')
    return (_wob(inner) if wobble else inner) + lab


def mob(x: float, y: float, n: int = 6, outfit: str = "minh_soldier", expr: str = "deadpan", s: float = 0.6,
        gap: float = 70, rows: int = 1, flip: bool = False, item: str = "spear", seed: int = 1, exprs: list | None = None) -> str:
    """Đám đông nhân vật hình nhộng (hàng sau nhỏ hơn)."""
    rnd = random.Random(seed)
    out = ""
    for r in range(rows - 1, -1, -1):
        k = 1 - r * 0.12
        for i in range(n):
            px = x + (i - (n - 1) / 2) * gap * k + (r % 2) * gap * 0.5 + rnd.uniform(-8, 8)
            py = y - r * 50 + rnd.uniform(-6, 6)
            e = rnd.choice(exprs) if exprs else expr
            out += dude(px, py, s * k, outfit, e, flip, item, wobble=False, lean=rnd.uniform(-5, 5))
    return _wob(out)


def _cast_keys():
    from studio.cast import CAST as _C
    return _C


def doodle_horse(x: float, y: float, s: float = 1.0, flip: bool = False, rider: str = "", expr: str = "smug") -> str:
    """Ngựa vẽ tay + người cưỡi (outfit)."""
    sx = -s if flip else s
    h = (f'<g transform="translate({x:.0f} {y:.0f}) scale({sx:.2f} {s:.2f})">'
         f'<ellipse cx="0" cy="44" rx="120" ry="14" fill="#000" opacity=".2"/>'
         f'<path d="M-80 -20 l-12 64 M-46 -14 l-4 58 M50 -14 l4 58 M82 -20 l10 64" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
         f'<path d="M-80 -20 l-12 64 M-46 -14 l-4 58 M50 -14 l4 58 M82 -20 l10 64" stroke="#8A5A3A" stroke-width="9" stroke-linecap="round"/>'
         f'<ellipse cx="0" cy="-40" rx="110" ry="50" fill="#8A5A3A" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M80 -60 C100 -110 120 -140 138 -148 L184 -122 C186 -110 178 -102 166 -102 L140 -110 C130 -86 120 -66 104 -36 Z" fill="#8A5A3A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
         f'<circle cx="160" cy="-128" r="5" fill="{INK}"/><path d="M130 -150 l-6 -24 l18 12z" fill="#8A5A3A" stroke="{INK}" stroke-width="3"/>'
         f'<path d="M-104 -60 C-150 -50 -150 0 -132 20" fill="none" stroke="#3A2418" stroke-width="16" stroke-linecap="round"/>'
         f'<path d="M-50 -88 Q0 -100 50 -88 L44 -40 Q0 -30 -44 -40Z" fill="#8E2A1E" stroke="{INK}" stroke-width="4"/>'
         f'<path d="M-44 -40 Q0 -30 44 -40" stroke="#E0B43A" stroke-width="5" fill="none"/>'
         f'<path d="M150 -118 L108 -78 L90 -82" stroke="#3A2418" stroke-width="4" fill="none"/>'
         f'<path d="M86 -96 Q120 -150 140 -150" stroke="#3A2418" stroke-width="10" fill="none" stroke-linecap="round"/></g>')
    if rider in _cast_keys():
        from studio.cast import peg as _peg
        r = _peg(rider, x + (-10 if flip else 10) * s, y - 62 * s, s * 0.78, expr, flip, "sword" if rider not in ("minh_soldier", "dv_soldier") else "spear")
    else:
        r = dude(x + (-6 if flip else 6) * s, y - 70 * s, s * 0.8, rider, expr, flip, "sword" if rider else "", wobble=False) if rider else ""
    return _wob(h + r)


# ------------------------------------------------------------------ đất nước có cảm xúc
def nation(which: str = "CN", view: str = "asia", expr: str = "smug", color: str = "", eyes_at: list | None = None,
           size: float = 1.0, label: str = "", shape: bool = True) -> str:
    """Vẽ lãnh thổ như một nhân vật: hình đất nước + mắt/mày/miệng đặt tại eyes_at [lat, lon]."""
    P = X._paths(view)
    I = INK
    if which == "VN":
        shape_svg = "".join(f'<path d="{pr["d"]}" fill="{color or X.DV}" stroke="{color or X.DV}" stroke-width="1"/>' for pr in P["provinces"]) \
            + f'<path d="{P["vn"]}" fill="none" stroke="{I}" stroke-width="5" stroke-linejoin="round"/>'
    else:
        d = P["countries"].get({"CN": "156", "LA": "418"}[which], "")
        shape_svg = f'<path d="{d}" fill="{color or X.MINH}" stroke="{I}" stroke-width="5" stroke-linejoin="round"/>'
    ex, ey = X.ll(view, *(eyes_at or [21, 105]))
    face = f'<g transform="translate({ex:.0f} {ey:.0f}) scale({2.2*size:.2f})">'
    face += ('<ellipse cx="-22" cy="0" rx="16" ry="20" fill="#fff" stroke="#1C1612" stroke-width="3"/>'
             '<ellipse cx="22" cy="0" rx="16" ry="20" fill="#fff" stroke="#1C1612" stroke-width="3"/>')
    pupils = {"smug": (4, 4), "angry": (0, 2), "shock": (0, 0), "cry": (0, 4), "deadpan": (0, 6), "cool": (0, 0), "happy": (0, 0), "panic": (-4, 0)}.get(expr, (0, 0))
    if expr != "cool":
        face += f'<circle cx="{-22+pupils[0]}" cy="{pupils[1]}" r="7" fill="{I}"/><circle cx="{22+pupils[0]}" cy="{pupils[1]}" r="7" fill="{I}"/>'
    brows = {"smug": "M-40 -24 L-6 -18 M6 -18 L40 -24", "angry": "M-40 -32 L-6 -16 M6 -16 L40 -32",
             "cry": "M-40 -18 L-8 -30 M8 -30 L40 -18", "shock": "M-38 -34 Q-22 -44 -6 -34 M6 -34 Q22 -44 38 -34",
             "deadpan": "M-40 -16 h32 M8 -16 h32", "panic": "M-40 -18 L-8 -30 M8 -30 L40 -18"}.get(expr, "")
    if brows:
        face += f'<path d="{brows}" stroke="{I}" stroke-width="6" stroke-linecap="round" fill="none"/>'
    if expr == "deadpan":
        face += '<path d="M-38 -8 h32 M6 -8 h32" stroke="#1C1612" stroke-width="5"/>'
    if expr == "cool":
        face += f'<path d="M-46 -14 h92 v8 q-2 20 -20 20 h-8 q-12 0 -16 -14 h-4 q-4 14 -16 14 h-8 q-18 0 -20 -20 z" fill="{I}"/>'
    mouth = {"smug": "M-14 34 q18 12 30 -6", "angry": "M-16 40 q16 -16 32 0", "cry": "M-14 42 q14 -14 28 0",
             "deadpan": "M-12 36 h24", "happy": "M-18 30 q18 22 36 0", "cool": "M-14 34 q18 10 30 -4"}.get(expr, "")
    if expr in ("shock", "panic"):
        face += f'<ellipse cx="0" cy="40" rx="11" ry="15" fill="#5A1A1E" stroke="{I}" stroke-width="3"/>'
    elif mouth:
        face += f'<path d="{mouth}" stroke="{I}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    if expr == "cry":
        face += '<path d="M-24 20 q-6 26 0 44 M24 20 q6 26 0 44" stroke="#7FD0F2" stroke-width="7" fill="none" stroke-linecap="round"/>'
    face += "</g>"
    lab = X.map_tag(label, ex, ey + 150 * size, 34, fill=I) if label else ""
    return (shape_svg if shape else "") + face + lab


# ------------------------------------------------------------------ hiệu ứng
def boom(text: str, x: float, y: float, size: int = 150, fill: str = "#F4C430", rot: float = -8, burst: bool = True) -> str:
    """Chữ hiệu ứng kiểu truyện tranh: BÙM!, TÙNG TÙNG!, VÈO… (nền nổ răng cưa)."""
    out = f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot})">'
    if burst:
        n, w, h = 16, len(text) * size * 0.42 + 80, size * 1.2
        pts = []
        for i in range(n * 2):
            a = math.pi * i / n
            r = 1.0 if i % 2 == 0 else 0.72
            pts.append((math.cos(a) * w * r, math.sin(a) * h * r))
        out += f'<path d="M' + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts) + f' Z" fill="#FFFFFF" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
    out += (f'<text x="0" y="{size*0.36:.0f}" font-size="{size}" text-anchor="middle" fill="{fill}" stroke="{INK}" stroke-width="{size*0.1:.0f}" '
            f'paint-order="stroke" stroke-linejoin="round">{text}</text></g>')
    return out


def speed_lines(cx: float = 960, cy: float = 540, n: int = 60, inner: float = 360, color: str = "#FFFFFF", op: float = 0.85, seed: int = 2) -> str:
    rnd = random.Random(seed)
    out = f'<g opacity="{op}">'
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.03, 0.03)
        r0 = inner + rnd.uniform(0, 160)
        r1 = 1400
        w = rnd.uniform(4, 16)
        x0, y0 = cx + math.cos(a) * r0, cy + math.sin(a) * r0
        x1, y1 = cx + math.cos(a + 0.012) * r1, cy + math.sin(a + 0.012) * r1
        x2, y2 = cx + math.cos(a - 0.012) * r1, cy + math.sin(a - 0.012) * r1
        out += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f} Z" fill="{color}"/>'
    return out + "</g>"


def flash(color: str = "#FFFFFF", op: float = 0.95) -> str:
    return f'<rect width="{A.W}" height="{A.H}" fill="{color}" opacity="{op}"/>'


def emoji(ch: str, x: float, y: float, size: int = 120, rot: float = 0) -> str:
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" transform="rotate({rot} {x} {y})" '
            f'style="font-family:\'Noto Color Emoji\',sans-serif">{ch}</text>')


def callout(text: str, x: float, y: float, tx: float, ty: float, size: int = 34, color: str = "#FFFFFF") -> str:
    """Chú thích kiểu "mũi tên vẽ tay" chỉ vào chi tiết."""
    mx, my = (x + tx) / 2 + 40, (y + ty) / 2 - 40
    ang = math.degrees(math.atan2(ty - my, tx - mx))
    return (f'<path d="M{x} {y+10} Q{mx:.0f} {my:.0f} {tx} {ty}" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x} {y+10} Q{mx:.0f} {my:.0f} {tx} {ty}" stroke="{color}" stroke-width="6" fill="none" stroke-linecap="round"/>'
            f'<g transform="translate({tx} {ty}) rotate({ang:.0f})"><path d="M0 0 l-30 -16 l6 16 l-6 16 z" fill="{color}" stroke="{INK}" stroke-width="4"/></g>'
            f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{color}" stroke="{INK}" stroke-width="8" paint-order="stroke">{text}</text>')


def caption_box(text: str, x: float = 40, y: float = 40, size: int = 34) -> str:
    """Hộp chú thích nhỏ góc màn hình (kiểu 'note' cà khịa)."""
    w = len(text) * size * 0.56 + 40
    return (f'<g transform="translate({x} {y}) rotate(-2)"><rect width="{w:.0f}" height="{size*1.7:.0f}" fill="#FFF36B" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{w/2:.0f}" y="{size*1.18:.0f}" font-size="{size}" text-anchor="middle" fill="{INK}">{text}</text></g>')


def sign(text: str, x: float, y: float, s: float = 1.0) -> str:
    """Biển gỗ chỉ đường."""
    w = len(text) * 30 + 60
    inner = (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"><rect x="-8" y="-150" width="16" height="150" fill="#6B4226" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M{-w/2:.0f} -210 h{w-30:.0f} l30 30 l-30 30 h-{w-30:.0f} z" fill="#B5793F" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<text x="0" y="-168" font-size="40" text-anchor="middle" fill="#FFF7E2" stroke="{INK}" stroke-width="6" paint-order="stroke">{text}</text></g>')
    return _wob(inner)


# ------------------------------------------------------------------ dàn nhân vật búp bê trụ + nền sơn dầu tự vẽ
from studio.cast import CAST, chauchau, closeup, crowd, fallen_flag, fallen_helmet, medallion, peg  # noqa: E402,F401


def oil_bg(kind: str = "karst_valley", time: str = "day", seed: int = 1, ink: float = 0.35, tint: str = "", tint_op: float = 0.0,
           crop: list | None = None, blur: float = 0) -> str:
    """Nền tranh sơn dầu tự vẽ (studio/paint.py) – thay cho ảnh chụp; không cần ghi nguồn ảnh."""
    from studio import paint
    p = paint.oil(kind, time, seed, ink)
    return photo(str(p.relative_to(ROOT)), crop=crop, tint=tint, tint_op=tint_op, blur=blur)
