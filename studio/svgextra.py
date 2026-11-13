"""Bộ đồ hoạ cho video NGANG 16:9 dạng "tóm tắt lịch sử" (bản đồ, chân dung, quân đội, thành, dòng thời gian...).

Phong cách riêng của Tí Xuyên Sử: vector phẳng, viền nâu đậm, màu phe:
  Đại Việt = vàng nghệ  #E9A92B   ·  Nhà Minh = đỏ son  #C4453C   ·  nước khác = be xám
Toạ độ: 1920 x 1080.
"""
from __future__ import annotations

import json
import math
import random
import subprocess
from pathlib import Path

from studio import svgart as A

GEO = Path(__file__).resolve().parent / "geo"
INK = "#2B1B12"
DV = "#E9A92B"      # Đại Việt
DV_D = "#B97E12"
MINH = "#C4453C"    # nhà Minh
MINH_D = "#8E2A24"
SEA = "#7EC4DE"
LAND = "#EADFC8"
TAG = "#3D4657"

# ------------------------------------------------------------------ bản đồ
VIEWS = {
    # bắc Đại Việt + nam Trung Hoa: lon/lat khung nhìn
    "north": {"lon": (100.6, 110.4), "lat": (17.0, 25.0)},
    # chiến trường Lạng Sơn – Bắc Giang – Thăng Long
    "front": {"lon": (104.95, 107.75), "lat": (20.45, 22.45)},
    "asia": {"lon": (97.0, 121.0), "lat": (6.0, 36.0)},
}

PLACES = {
    "Đông Quan": (21.03, 105.85), "Lam Sơn": (19.98, 105.43), "Lạng Sơn": (21.85, 106.76),
    "Chi Lăng": (21.66, 106.60), "Mã Yên": (21.62, 106.57), "Cần Trạm": (21.47, 106.36),
    "Phố Cát": (21.40, 106.30), "Xương Giang": (21.29, 106.21), "Ải Pha Lũy": (22.02, 106.70),
    "Lê Hoa": (22.50, 103.97), "Tốt Động": (20.87, 105.66), "Quảng Tây": (23.3, 107.9),
    "Vân Nam": (24.2, 102.8), "Thanh Hoá": (19.81, 105.78),
}

RIVER_HONG = [(22.50, 103.97), (22.0, 104.6), (21.70, 104.90), (21.32, 105.42), (21.03, 105.86), (20.6, 106.25), (20.25, 106.60)]


def _proj(view: str):
    v = VIEWS[view]
    w, h = A.W, A.H
    lon0, lon1 = v["lon"]
    lat0, lat1 = v["lat"]
    my = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
    sx = w / math.radians(lon1 - lon0)
    sy = h / (my(lat1) - my(lat0))
    s = min(sx, sy) * 1.0
    cx, cy = math.radians((lon0 + lon1) / 2), (my(lat0) + my(lat1)) / 2
    tx, ty = w / 2 - s * cx, h / 2 + s * cy
    return s, tx, ty


def ll(view: str, lat: float, lon: float) -> tuple[float, float]:
    s, tx, ty = _proj(view)
    return s * math.radians(lon) + tx, -s * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) + ty


def _mapgen(cfg: dict, key: str) -> dict:
    cache = GEO / f"cache_{key}.json"
    if not cache.exists():
        out = subprocess.check_output(["node", str(GEO / "mapgen.js"), json.dumps(cfg)], cwd=str(GEO))
        cache.write_text(out.decode())
    return json.loads(cache.read_text())


def _paths(view: str) -> dict:
    s, tx, ty = _proj(view)
    return _mapgen({"s": s, "tx": tx, "ty": ty, "w": A.W, "h": A.H}, f"{view}_{A.W}x{A.H}_v2")


# Hai quần đảo của Việt Nam (toạ độ trung tâm để đặt nhãn)
ISLANDS = {"QĐ. Hoàng Sa": (16.5, 112.0), "QĐ. Trường Sa": (10.0, 114.2)}
ISLAND_DOTS = {
    "QĐ. Hoàng Sa": [(16.83, 112.33), (16.53, 111.61), (15.78, 111.20), (16.67, 112.73), (16.45, 111.70), (16.25, 112.05), (16.95, 112.25)],
    "QĐ. Trường Sa": [(8.64, 111.92), (11.43, 114.33), (10.18, 114.36), (9.88, 114.33), (10.38, 114.36), (7.89, 112.91),
                      (10.37, 114.48), (11.05, 114.28), (9.12, 113.80), (8.85, 112.6), (10.7, 115.8), (9.6, 115.5)],
}


def _place(p, view):
    if isinstance(p, str):
        return ll(view, *PLACES[p])
    return ll(view, p[0], p[1])


def map_base(view: str = "north", vn: str = DV, cn: str = "#D8CDB6", la: str = "#E3D9C3", river: bool = True,
             cn_label: str = "", vn_label: str = "", la_label: str = "") -> str:
    """Nền bản đồ: biển + các nước. vn/cn/la = màu tô lãnh thổ."""
    P = _paths(view)
    col = {"156": cn, "418": la, "764": "#E3D9C3", "116": "#E3D9C3", "104": "#E3D9C3", "158": "#E3D9C3"}
    out = f'<rect width="{A.W}" height="{A.H}" fill="{SEA}"/>'
    # sóng biển nhẹ
    rnd = random.Random(2)
    for _ in range(26):
        x, y = rnd.randint(0, A.W), rnd.randint(0, A.H)
        out += f'<path d="M{x} {y} q14 -8 28 0 t28 0" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/>'
    for cid, d in P["countries"].items():
        out += f'<path d="{d}" fill="{col.get(cid, LAND)}" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
    # Việt Nam: 34 tỉnh thành (ranh giới mảnh) + đường bao quốc gia
    for pr in P["provinces"]:
        out += f'<path d="{pr["d"]}" fill="{vn}" stroke="#FFF7E2" stroke-width="1.6" stroke-opacity=".75" stroke-linejoin="round"/>'
    if P["vn"]:
        out += f'<path d="{P["vn"]}" fill="none" stroke="#fff" stroke-width="3.5" stroke-linejoin="round"/>'
    # quần đảo Hoàng Sa, Trường Sa: luôn ghi nhãn khi nằm trong khung
    for name, (la_, lo_) in ISLANDS.items():
        x, y = ll(view, la_, lo_)
        if -20 < x < A.W + 20 and -20 < y < A.H - 60:
            for (a, b) in ISLAND_DOTS[name]:
                dx, dy = ll(view, a, b)
                out += f'<circle cx="{dx:.0f}" cy="{dy:.0f}" r="5" fill="{vn}" stroke="#fff" stroke-width="2"/>'
            if view == "asia":
                lx, ly = (x + 200, y - 50) if "Hoàng" in name else (x + 250, y - 70)
            else:
                lx, ly = x + (150 if "Trường" in name else 0), (y - 30 if y < A.H - 330 else y - 230)
            out += map_tag(name + " (Việt Nam)", lx, ly, 24, fill="#2B1B12")
    if river:
        pts = [ll(view, *p) for p in RIVER_HONG]
        out += f'<path d="{_smooth(pts)}" fill="none" stroke="#5FA9CC" stroke-width="7" stroke-linecap="round" opacity=".9"/>'
    for txt, p in ((cn_label, {"north": (23.9, 106.2), "asia": (31.5, 113.0)}.get(view, (22.33, 107.55))), (vn_label, (21.55, 104.55) if view == "north" else (20.75, 105.4)),
                   (la_label, (20.2, 102.4))):
        if txt:
            x, y = ll(view, *p)
            out += f'<text x="{x:.0f}" y="{y:.0f}" font-size="46" text-anchor="middle" fill="{INK}" opacity=".55" letter-spacing="6">{txt}</text>'
    return out


def _smooth(pts) -> str:
    if len(pts) < 3:
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        xc, yc = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        d += f" Q{pts[i][0]:.1f} {pts[i][1]:.1f} {xc:.1f} {yc:.1f}"
    d += f" L{pts[-1][0]:.1f} {pts[-1][1]:.1f}"
    return d


def map_tag(text: str, x: float, y: float, size: int = 30, fill: str = TAG, color: str = "#fff") -> str:
    w = len(text) * size * 0.58 + 36
    return (f'<g transform="translate({x - w/2:.0f} {y - size*0.9:.0f})"><rect width="{w:.0f}" height="{size*1.55:.0f}" rx="{size*.5:.0f}" fill="{fill}" opacity=".92"/>'
            f'<text x="{w/2:.0f}" y="{size*1.1:.0f}" font-size="{size}" text-anchor="middle" fill="{color}">{text}</text></g>')


def map_label(place, view: str = "north", text: str = "", kind: str = "city", dx: float = 0, dy: float = -46,
              size: int = 30, color: str = INK) -> str:
    x, y = _place(place, view)
    name = text or (place if isinstance(place, str) else "")
    if kind == "fort":
        icon = (f'<g transform="translate({x:.0f} {y:.0f})"><rect x="-22" y="-18" width="44" height="30" fill="#9C8466" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M-22 -18 v-10 h10 v10 M-5 -18 v-10 h10 v10 M12 -18 v-10 h10 v10" fill="#9C8466" stroke="{INK}" stroke-width="4"/>'
                f'<rect x="-7" y="-4" width="14" height="16" fill="{INK}"/></g>')
    elif kind == "battle":
        icon = (f'<g transform="translate({x:.0f} {y:.0f})" stroke="{INK}" stroke-width="6" stroke-linecap="round">'
                '<circle r="26" fill="#fff" stroke-width="4"/><path d="M-13 -13 L13 13 M13 -13 L-13 13" stroke="#C4453C"/></g>')
    elif kind == "star":
        icon = f'<g transform="translate({x:.0f} {y:.0f})"><circle r="24" fill="{DV}" stroke="{INK}" stroke-width="4"/><path d="M0 -14 L4 -4 L14 -4 L6 3 L9 13 L0 7 L-9 13 L-6 3 L-14 -4 L-4 -4Z" fill="#fff"/></g>'
    else:
        icon = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="#fff" stroke="{INK}" stroke-width="5"/>'
    return icon + (map_tag(name, x + dx, y + dy, size) if name else "")


def map_arrow(pts: list, view: str = "north", color: str = MINH, width: float = 26, dashed: bool = False,
              label: str = "", label_at: float = 0.5, label_dy: float = -50) -> str:
    """Mũi tên hành quân đi qua các điểm (tên địa danh hoặc [lat, lon])."""
    P = [_place(p, view) for p in pts]
    d = _smooth(P)
    (x1, y1), (x2, y2) = P[-2], P[-1]
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    head = (f'<g transform="translate({x2:.1f} {y2:.1f}) rotate({ang:.1f})">'
            f'<path d="M{-width*1.2:.0f} {-width*1.25:.0f} L{width*0.9:.0f} 0 L{-width*1.2:.0f} {width*1.25:.0f} Z" fill="{color}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>')
    dash = f' stroke-dasharray="{width*1.4:.0f} {width*.9:.0f}"' if dashed else ""
    out = (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{width+10}" stroke-linecap="round" opacity=".85"{dash}/>'
           f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dash}/>' + head)
    if label:
        i = min(int(label_at * (len(P) - 1)), len(P) - 2)
        lx, ly = (P[i][0] + P[i + 1][0]) / 2, (P[i][1] + P[i + 1][1]) / 2
        out += map_tag(label, lx, ly + label_dy, 30, fill=color)
    return out


# ------------------------------------------------------------------ chân dung
PORTRAITS = {
    # mũ/đầu, màu áo, râu
    "leloi": {"hat": "khan", "robe": "#E9A92B", "beard": "long", "skin": "#E8B98E"},
    "nguyentrai": {"hat": "scholar", "robe": "#3F6A8A", "beard": "long", "skin": "#EDC39B"},
    "tranluu": {"hat": "dv_helmet", "robe": "#8C5A32", "beard": "short", "skin": "#E2AE82"},
    "lieuthang": {"hat": "minh_helmet", "robe": "#C4453C", "beard": "mustache", "skin": "#EAC29C"},
    "mocthanh": {"hat": "minh_helmet", "robe": "#9E3B5A", "beard": "short", "skin": "#EAC29C"},
    "vuongthong": {"hat": "minh_helmet", "robe": "#7D3A2E", "beard": "mustache", "skin": "#E8BF98"},
    "luongminh": {"hat": "minh_helmet", "robe": "#A2463C", "beard": "none", "skin": "#EAC29C"},
    "minh_official": {"hat": "official", "robe": "#5B3F7A", "beard": "long", "skin": "#EAC29C"},
    "lykhanh": {"hat": "official", "robe": "#4E5B7A", "beard": "short", "skin": "#EAC29C"},
    "hoangphuc": {"hat": "official", "robe": "#5B3F7A", "beard": "long", "skin": "#EAC29C"},
    "thoitu": {"hat": "minh_helmet", "robe": "#7A3E5A", "beard": "short", "skin": "#E8BF98"},
    "minh_soldier": {"hat": "minh_helmet", "robe": "#C4453C", "beard": "none", "skin": "#EAC29C"},
    "dv_soldier": {"hat": "dv_helmet", "robe": "#B97E12", "beard": "none", "skin": "#E2AE82"},
}


EXPRS = ("neutral", "smug", "angry", "scared", "shock", "sweat", "cry", "wink", "happy", "sad", "dizzy", "determined")


def _face_expr(expr: str) -> tuple[str, str]:
    """Trả về (mắt+mày, miệng) theo biểu cảm. Toạ độ mặt chân dung (tâm 0,-6; rx52 ry60)."""
    I = INK
    eye = lambda cx, r=6: f'<circle cx="{cx}" cy="-1" r="{r}" fill="{I}"/><circle cx="{cx-2}" cy="-3" r="{max(1.5, r/3):.1f}" fill="#fff"/>'
    big = lambda cx: (f'<ellipse cx="{cx}" cy="-2" rx="11" ry="13" fill="#fff" stroke="{I}" stroke-width="3"/>'
                      f'<circle cx="{cx}" cy="0" r="5" fill="{I}"/>')
    brows = {
        "neutral": "M-32 -16 L-12 -16 M12 -16 L32 -16",
        "smug": "M-32 -20 L-12 -14 M12 -14 L32 -20",
        "angry": "M-34 -24 L-10 -12 M10 -12 L34 -24",
        "determined": "M-34 -22 L-10 -14 M10 -14 L34 -22",
        "scared": "M-32 -12 L-12 -24 M12 -24 L32 -12",
        "sweat": "M-32 -12 L-12 -22 M12 -22 L32 -12",
        "sad": "M-32 -10 L-12 -22 M12 -22 L32 -10",
        "cry": "M-32 -10 L-12 -22 M12 -22 L32 -10",
        "shock": "M-32 -30 Q-22 -38 -12 -30 M12 -30 Q22 -38 32 -30",
        "happy": "M-32 -20 Q-22 -26 -12 -20 M12 -20 Q22 -26 32 -20",
        "wink": "M-32 -20 Q-22 -26 -12 -20 M12 -18 L32 -18",
        "dizzy": "M-32 -18 L-12 -18 M12 -18 L32 -18",
    }[expr]
    out = f'<path d="{brows}" stroke="{I}" stroke-width="7" stroke-linecap="round" fill="none"/>'
    if expr in ("shock", "scared", "sweat"):
        out += big(-21) + big(21)
    elif expr in ("smug",):
        out += f'<path d="M-30 0 Q-21 -6 -12 0 M12 0 Q21 -6 30 0" stroke="{I}" stroke-width="5" fill="none" stroke-linecap="round"/>' + eye(-21, 4).replace('cy="-1"', 'cy="2"') + eye(21, 4).replace('cy="-1"', 'cy="2"')
    elif expr in ("happy",):
        out += f'<path d="M-30 2 Q-21 -8 -12 2 M12 2 Q21 -8 30 2" stroke="{I}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    elif expr == "wink":
        out += eye(-21) + f'<path d="M12 0 Q21 -6 30 0" stroke="{I}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    elif expr == "dizzy":
        out += ''.join(f'<path d="M{c-7} -8 L{c+7} 6 M{c+7} -8 L{c-7} 6" stroke="{I}" stroke-width="4" stroke-linecap="round"/>' for c in (-21, 21))
    elif expr in ("sad", "cry"):
        out += eye(-21, 5) + eye(21, 5)
    else:
        out += eye(-21) + eye(21)
    mouth = {
        "neutral": f'<path d="M-12 36 Q0 40 12 36" fill="none" stroke="{I}" stroke-width="4" stroke-linecap="round"/>',
        "smug": f'<path d="M-14 34 Q4 44 18 30" fill="none" stroke="{I}" stroke-width="5" stroke-linecap="round"/>',
        "angry": f'<path d="M-18 40 Q0 26 18 40 Z" fill="#6E1E24" stroke="{I}" stroke-width="4"/><path d="M-12 36 h24" stroke="#fff" stroke-width="3"/>',
        "determined": f'<path d="M-14 38 L14 38" stroke="{I}" stroke-width="5" stroke-linecap="round"/>',
        "scared": f'<path d="M-14 40 q7 -8 14 0 t14 0" fill="none" stroke="{I}" stroke-width="4" stroke-linecap="round"/>',
        "sweat": f'<path d="M-14 40 q7 -8 14 0 t14 0" fill="none" stroke="{I}" stroke-width="4" stroke-linecap="round"/>',
        "shock": f'<ellipse cx="0" cy="40" rx="11" ry="15" fill="#6E1E24" stroke="{I}" stroke-width="4"/>',
        "happy": f'<path d="M-18 32 Q0 54 18 32 Z" fill="#6E1E24" stroke="{I}" stroke-width="4"/>',
        "wink": f'<path d="M-16 32 Q2 48 18 30" fill="none" stroke="{I}" stroke-width="5" stroke-linecap="round"/>',
        "sad": f'<path d="M-12 42 Q0 34 12 42" fill="none" stroke="{I}" stroke-width="4" stroke-linecap="round"/>',
        "cry": f'<path d="M-16 44 Q0 30 16 44 Z" fill="#6E1E24" stroke="{I}" stroke-width="4"/>',
        "dizzy": f'<path d="M-14 38 q5 -6 10 0 t10 0 t10 0" fill="none" stroke="{I}" stroke-width="4" stroke-linecap="round"/>',
    }[expr]
    return out, mouth


def _face_fx(expr: str) -> str:
    """Hiệu ứng truyện tranh trên mặt (vẽ ngoài khung tròn): mồ hôi, nước mắt, gân tức, sao choáng."""
    if expr in ("sweat", "scared"):
        return ('<path d="M58 -54 q12 18 0 26 q-12 -8 0 -26z" fill="#7FD0F2" stroke="#2B6F8F" stroke-width="3"/>'
                '<path d="M74 -20 q9 14 0 20 q-9 -6 0 -20z" fill="#7FD0F2" stroke="#2B6F8F" stroke-width="3"/>')
    if expr == "cry":
        return ('<path d="M-24 8 q-6 30 -2 56" stroke="#7FD0F2" stroke-width="7" fill="none" stroke-linecap="round"/>'
                '<path d="M24 8 q6 30 2 56" stroke="#7FD0F2" stroke-width="7" fill="none" stroke-linecap="round"/>')
    if expr == "angry":
        return ('<g transform="translate(66 -72)" stroke="#D2352C" stroke-width="7" stroke-linecap="round" fill="none">'
                '<path d="M-14 -4 q6 -2 6 -10 M4 -14 q2 6 10 6 M14 4 q-6 2 -6 10 M-4 14 q-2 -6 -10 -6"/></g>')
    if expr == "dizzy":
        return ''.join(f'<path transform="translate({x} {y}) scale(.9)" d="M0 -12 L3 -3 L12 -3 L5 3 L8 12 L0 6 L-8 12 L-5 3 L-12 -3 L-3 -3Z" fill="#F4C430" stroke="{INK}" stroke-width="2"/>'
                       for x, y in ((-60, -96), (0, -116), (60, -96)))
    if expr == "shock":
        return f'<path d="M-92 -70 l-22 -16 M-96 -40 l-26 -4 M92 -70 l22 -16 M96 -40 l26 -4" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    return ""


def portrait(x: float, y: float, r: float = 90, who: str = "leloi", name: str = "", ring: str = "",
             mark: str = "", name_size: int = 28, expr: str = "neutral") -> str:
    """Chân dung tròn (medallion) có BIỂU CẢM.
    expr: neutral | smug | angry | determined | scared | sweat | shock | happy | wink | sad | cry | dizzy
    mark: '' | 'x' (tử trận) | 'target' | 'captured' | 'flee'."""
    p = PORTRAITS[who]
    ring = ring or (DV if p["hat"] in ("khan", "scholar", "dv_helmet") else MINH)
    s = r / 100
    skin, robe = p["skin"], p["robe"]
    hat = {
        "khan": f'<path d="M-52 -40 C-56 -95 56 -95 52 -40 Z" fill="#1E1A17" stroke="{INK}" stroke-width="4"/><path d="M-50 -48 L50 -48" stroke="{DV}" stroke-width="7"/>',
        "scholar": f'<path d="M-50 -38 L-44 -92 L44 -92 L50 -38 Z" fill="#1E1A17" stroke="{INK}" stroke-width="4"/><path d="M-62 -60 L62 -60" stroke="#1E1A17" stroke-width="9" stroke-linecap="round"/>',
        "dv_helmet": f'<path d="M-56 -36 C-58 -100 58 -100 56 -36 Z" fill="#7C8A6A" stroke="{INK}" stroke-width="4"/><path d="M0 -98 l-8 -22 h16 z" fill="{SCARF_RED}"/>',
        "minh_helmet": f'<path d="M-58 -34 C-60 -104 60 -104 58 -34 L66 -30 L-66 -30 Z" fill="#9AA3A8" stroke="{INK}" stroke-width="4"/><path d="M-40 -70 Q0 -96 40 -70" stroke="#C9D0D4" stroke-width="6" fill="none" opacity=".7"/><path d="M0 -104 l0 -18" stroke="{INK}" stroke-width="5"/><path d="M-12 -122 q12 -30 24 0 z" fill="#D2352C" stroke="{INK}" stroke-width="3"/>',
        "official": f'<path d="M-48 -40 L-44 -96 L44 -96 L48 -40 Z" fill="#1E1A17" stroke="{INK}" stroke-width="4"/><ellipse cx="-72" cy="-70" rx="26" ry="10" fill="#1E1A17"/><ellipse cx="72" cy="-70" rx="26" ry="10" fill="#1E1A17"/>',
    }[p["hat"]]
    beard = {
        "long": f'<path d="M-28 22 Q0 110 28 22 Q0 40 -28 22Z" fill="#2A2420" stroke="{INK}" stroke-width="3"/>',
        "short": f'<path d="M-30 20 Q0 62 30 20 Q0 34 -30 20Z" fill="#2A2420"/>',
        "mustache": f'<path d="M-34 14 Q-14 2 0 12 Q14 2 34 14 Q16 20 0 18 Q-16 20 -34 14Z" fill="#2A2420"/><path d="M-8 52 Q0 66 8 52Z" fill="#2A2420"/>',
        "none": "",
    }[p["beard"]]
    eyes, mouth = _face_expr(expr if expr in EXPRS else "neutral")
    blush = ('<ellipse cx="-34" cy="18" rx="10" ry="6" fill="#E77" opacity=".45"/><ellipse cx="34" cy="18" rx="10" ry="6" fill="#E77" opacity=".45"/>'
             if expr in ("happy", "wink", "smug", "cry", "sweat") else "")
    face = (f'<path d="M-100 100 C-90 40 90 40 100 100 Z" fill="{robe}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-100 100 C-90 50 -20 46 0 60 L0 100 Z" fill="#000" opacity=".12"/>'
            f'<path d="M-24 52 L0 86 L24 52" fill="none" stroke="#F4EEDD" stroke-width="8"/>'
            f'<ellipse cx="0" cy="-6" rx="52" ry="60" fill="{skin}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M20 -60 C56 -40 58 30 18 52 C40 20 42 -24 20 -60Z" fill="#7A4A2A" opacity=".16"/>'
            f'<ellipse cx="-22" cy="-30" rx="16" ry="9" fill="#fff" opacity=".18"/>'
            + eyes + f'<path d="M0 4 L-5 22 L5 22" fill="none" stroke="{INK}" stroke-width="3"/>' + blush
            + beard + mouth + hat)
    marks = ""
    if mark == "x":
        marks = '<path d="M-70 -70 L70 70 M70 -70 L-70 70" stroke="#B3221B" stroke-width="16" stroke-linecap="round" opacity=".9"/>'
    elif mark == "target":
        marks = '<circle r="112" fill="none" stroke="#B3221B" stroke-width="8" stroke-dasharray="20 12"/><path d="M0 -128 V-96 M0 96 V128 M-128 0 H-96 M96 0 H128" stroke="#B3221B" stroke-width="8"/>'
    elif mark == "captured":
        marks = f'<g transform="translate(0 70)"><rect x="-58" y="-14" width="116" height="28" rx="14" fill="#6D6D6D" stroke="{INK}" stroke-width="4"/><circle cx="-30" r="9" fill="none" stroke="#ddd" stroke-width="4"/><circle cx="0" r="9" fill="none" stroke="#ddd" stroke-width="4"/><circle cx="30" r="9" fill="none" stroke="#ddd" stroke-width="4"/></g>'
    elif mark == "flee":
        marks = '<path d="M80 -40 h40 M86 0 h52 M80 40 h40" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".9"/>'
    nm = ""
    if name:
        nm = map_tag(name, x, y + r + 44 * (name_size / 28), name_size, fill="#fff", color=INK).replace('opacity=".92"', 'stroke="#2B1B12" stroke-width="3"')
    cid = f"cp_{who}_{int(x)}_{int(y)}"
    return (f'<defs><clipPath id="{cid}"><circle r="100"/></clipPath>'
            f'<radialGradient id="bg_{cid}" cx=".35" cy=".3"><stop offset="0" stop-color="#FFFBF0"/><stop offset="1" stop-color="#E9DDC4"/></radialGradient></defs>'
            f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.3f})">'
            f'<circle r="112" fill="#000" opacity=".18" transform="translate(6 8)"/>'
            f'<circle r="108" fill="{ring}" stroke="{INK}" stroke-width="6"/>'
            f'<circle r="100" fill="url(#bg_{cid})"/>'
            f'<g clip-path="url(#{cid})">{face}</g>{_face_fx(expr)}{marks}</g>{nm}')


def bubble(x: float, y: float, text: str, tx: float = 0, ty: float = 80, kind: str = "speech", size: int = 34,
           fill: str = "#FFFFFF") -> str:
    """Bong bóng thoại truyện tranh. (x,y)=tâm bóng; (tx,ty)=đầu đuôi trỏ tới người nói (toạ độ tuyệt đối).
    kind: speech | shout (răng cưa) | think (mây)."""
    lines = text.split("|")
    w = max(len(l) for l in lines) * size * 0.56 + 60
    h = len(lines) * size * 1.25 + 34
    out = ""
    if kind == "think":
        for i, (dx, dy, r) in enumerate(((0.35, 0.55, 14), (0.65, 0.8, 9))):
            px, py = x + (tx - x) * dx, y + (ty - y) * dy
            out += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="4"/>'
        rnd = random.Random(len(text))
        blobs = "".join(f'<ellipse cx="{x + (i/5-0.5)*w*0.9:.0f}" cy="{y + rnd.uniform(-h*.25, h*.25):.0f}" rx="{w*0.24:.0f}" ry="{h*0.5:.0f}" fill="{fill}" stroke="{INK}" stroke-width="4"/>' for i in range(6))
        out += blobs + f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w*.5:.0f}" ry="{h*.44:.0f}" fill="{fill}"/>'
    elif kind == "shout":
        n = 18
        pts = []
        for i in range(n * 2):
            a = math.pi * i / n
            rr = 1.0 if i % 2 == 0 else 0.82
            pts.append((x + math.cos(a) * w * 0.62 * rr, y + math.sin(a) * h * 0.78 * rr))
        out += f'<path d="M{tx:.0f} {ty:.0f} L{x-24:.0f} {y+h*.3:.0f} L{x+24:.0f} {y+h*.3:.0f} Z" fill="{fill}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        out += f'<path d="M' + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts) + f' Z" fill="{fill}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    else:
        out += f'<path d="M{tx:.0f} {ty:.0f} L{x-22:.0f} {y+h*.3:.0f} L{x+26:.0f} {y+h*.3:.0f} Z" fill="{fill}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        out += f'<rect x="{x-w/2:.0f}" y="{y-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{h*.45:.0f}" fill="{fill}" stroke="{INK}" stroke-width="5"/>'
        out += f'<path d="M{x-22:.0f} {y+h*.3:.0f} L{x+26:.0f} {y+h*.3:.0f}" stroke="{fill}" stroke-width="8"/>'
    for i, l in enumerate(lines):
        yy = y - (len(lines) - 1) * size * 0.62 + i * size * 1.25 + size * 0.36
        out += f'<text x="{x:.0f}" y="{yy:.0f}" font-size="{size}" text-anchor="middle" fill="{INK}">{l}</text>'
    return out


def emote(x: float, y: float, kind: str = "!", s: float = 1.0) -> str:
    """Dấu cảm xúc nổi: ! | ? | !! | sweat | anger | stars | lines (hoảng loạn) | heart."""
    g = f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
    if kind in ("!", "!!", "?"):
        txt = {"!": "!", "!!": "!!", "?": "?"}[kind]
        col = "#D2352C" if kind != "?" else "#2F4D8F"
        return g + f'<text x="0" y="0" font-size="90" text-anchor="middle" fill="{col}" stroke="#FFF7E2" stroke-width="10" paint-order="stroke">{txt}</text></g>'
    if kind == "sweat":
        return g + '<path d="M0 -40 q20 30 0 44 q-20 -14 0 -44z" fill="#7FD0F2" stroke="#2B6F8F" stroke-width="4"/></g>'
    if kind == "anger":
        return g + '<g stroke="#D2352C" stroke-width="9" stroke-linecap="round" fill="none"><path d="M-20 -6 q8 -2 8 -14 M6 -20 q2 8 14 8 M20 6 q-8 2 -8 14 M-6 20 q-2 -8 -14 -8"/></g></g>'
    if kind == "stars":
        return g + "".join(f'<path transform="translate({dx} {dy})" d="M0 -14 L4 -4 L14 -4 L6 3 L9 14 L0 7 L-9 14 L-6 3 L-14 -4 L-4 -4Z" fill="#F4C430" stroke="{INK}" stroke-width="2.5"/>' for dx, dy in ((-34, 0), (0, -18), (34, 0))) + "</g>"
    if kind == "lines":
        return g + f'<path d="M-50 -30 l-26 -14 M-54 0 l-30 0 M-50 30 l-26 14 M50 -30 l26 -14 M54 0 l30 0 M50 30 l26 14" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>'
    if kind == "heart":
        return g + '<path d="M0 20 C-40 -10 -24 -44 0 -24 C24 -44 40 -10 0 20Z" fill="#E2504F" stroke="#2B1B12" stroke-width="4"/></g>'
    return ""


SCARF_RED = "#D62F3A"


# ------------------------------------------------------------------ quân đội
def _footman(color: str, dark: str, hat: str) -> str:
    h = (f'<path d="M-15 -52 L0 -66 L15 -52 Z" fill="#E6C98A" stroke="{INK}" stroke-width="2.5"/>' if hat == "non"
         else f'<path d="M-11 -50 C-12 -70 12 -70 11 -50 Z" fill="#9AA3A8" stroke="{INK}" stroke-width="2.5"/><path d="M0 -68 l0 -8" stroke="#D2352C" stroke-width="4"/>')
    return (f'<path d="M-12 -38 L12 -38 L15 0 L-15 0 Z" fill="{color}" stroke="{INK}" stroke-width="2.5"/>'
            f'<line x1="16" y1="4" x2="16" y2="-76" stroke="#5A3A22" stroke-width="3"/><path d="M16 -76 l-4 -10 l8 0z" fill="#B9C1C6"/>'
            f'<circle cx="0" cy="-46" r="10" fill="#EBC097" stroke="{INK}" stroke-width="2.5"/>' + h)


def _horseman(color: str, hat: str) -> str:
    return (f'<path d="M-34 -24 C-30 -40 26 -40 30 -24 L30 -12 C10 -6 -10 -6 -34 -12 Z" fill="#7A5236" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M26 -30 L44 -54 L54 -50 L40 -22 Z" fill="#7A5236" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M-28 -12 l-4 22 M-14 -10 l0 22 M12 -10 l0 22 M24 -12 l4 22" stroke="#5A3A22" stroke-width="5" stroke-linecap="round"/>'
            f'<g transform="translate(0 -26) scale(.85)">{_footman(color, color, hat)}</g>')


def army(x: float, y: float, cols: int = 6, rows: int = 3, color: str = MINH, s: float = 1.0, kind: str = "foot",
         hat: str = "", flip: bool = False, gap: float = 42, flag: bool = True, seed: int = 1) -> str:
    """Khối quân (lính bộ / kỵ binh) theo màu phe. (x,y) = góc trái-dưới hàng trước."""
    hat = hat or ("non" if color == DV else "helmet")
    rnd = random.Random(seed)
    unit = _horseman(color, hat) if kind == "horse" else _footman(color, color, hat)
    g = gap * (1.5 if kind == "horse" else 1)
    out = f'<g transform="translate({x:.0f} {y:.0f}) scale({-s if flip else s:.3f} {s:.3f})">'
    for r in range(rows - 1, -1, -1):
        for c in range(cols):
            ox = c * g + r * g * 0.45 + rnd.uniform(-4, 4)
            oy = -r * 26 + rnd.uniform(-3, 3)
            out += f'<g transform="translate({ox:.0f} {oy:.0f})">{unit}</g>'
    if flag:
        fx = (cols - 1) * g + 30
        out += (f'<line x1="{fx}" y1="0" x2="{fx}" y2="-150" stroke="#5A3A22" stroke-width="6"/>'
                f'<path d="M{fx} -150 L{fx+70} -132 L{fx} -112 Z" fill="{color}" stroke="{INK}" stroke-width="3"/>')
    return out + "</g>"


# ------------------------------------------------------------------ công trình & đạo cụ
def fortress(x: float, y: float, s: float = 1.0, flag: str = DV, label: str = "") -> str:
    out = f"""<g transform="translate({x:.0f} {y:.0f}) scale({s:.3f})">
  <rect x="-260" y="-150" width="520" height="150" fill="#A68D6B" stroke="{INK}" stroke-width="6"/>
  {''.join(f'<rect x="{-260+i*52}" y="-180" width="30" height="34" fill="#A68D6B" stroke="{INK}" stroke-width="5"/>' for i in range(10))}
  <path d="M-60 0 L-60 -90 Q0 -140 60 -90 L60 0 Z" fill="#3A2A1E" stroke="{INK}" stroke-width="6"/>
  <path d="M-150 -180 L-150 -260 L-90 -300 L-30 -260 L-30 -180 Z" fill="#B85C3E" stroke="{INK}" stroke-width="6"/>
  <path d="M30 -180 L30 -260 L90 -300 L150 -260 L150 -180 Z" fill="#B85C3E" stroke="{INK}" stroke-width="6"/>
  <line x1="0" y1="-180" x2="0" y2="-330" stroke="#5A3A22" stroke-width="8"/>
  <path d="M0 -330 L90 -305 L0 -280 Z" fill="{flag}" stroke="{INK}" stroke-width="4"/>
  {''.join(f'<path d="M{-240+i*60} -40 h30 M{-230+i*60} -95 h30" stroke="#7F6A4E" stroke-width="5"/>' for i in range(8))}
</g>"""
    if label:
        out += map_tag(label, x, y + 60 * s + 30, 34)
    return out


def camp(x: float, y: float, n: int = 7, s: float = 1.0, color: str = MINH, seed: int = 3) -> str:
    rnd = random.Random(seed)
    out = ""
    for i in range(n):
        tx = x + (i % 4) * 150 * s + (i // 4) * 70 * s + rnd.randint(-15, 15)
        ty = y + (i // 4) * 60 * s
        out += (f'<g transform="translate({tx:.0f} {ty:.0f}) scale({s:.2f})"><path d="M-70 0 L0 -90 L70 0 Z" fill="#E7DCC4" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M-18 0 L0 -50 L18 0 Z" fill="{INK}"/><line x1="0" y1="-90" x2="0" y2="-130" stroke="#5A3A22" stroke-width="4"/>'
                f'<path d="M0 -130 l36 10 l-36 10z" fill="{color}"/></g>')
    return out


def gorge(floor: float = 760, marsh: bool = True) -> str:
    """Ải hiểm: vách núi đá dựng đứng 2 bên, lòng thung lũng hẹp, đầm lầy."""
    W, H = A.W, A.H
    out = f'<rect width="{W}" height="{H}" fill="url(#g_mist)"/>'
    out += A.karst(floor - 80, "#93A79A", 21, hmin=260, hmax=480)
    out += f'<path d="M0 {floor} L{W} {floor} L{W} {H} L0 {H} Z" fill="#8FA36A"/>'
    out += f'<path d="M{W*0.36} {floor} C{W*0.42} {floor+120} {W*0.30} {H-200} {W*0.25} {H} L{W*0.75} {H} C{W*0.70} {H-200} {W*0.58} {floor+120} {W*0.64} {floor} Z" fill="#A7905F"/>'
    if marsh:
        for i, (cx, cy, rx) in enumerate(((W*0.48, floor+170, 120), (W*0.55, floor+250, 160), (W*0.44, floor+300, 110))):
            out += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx}" ry="{rx*.22:.0f}" fill="#6E7C55" opacity=".85"/>'
    for side in (-1, 1):  # vách núi
        x0 = 0 if side < 0 else W
        out += (f'<path d="M{x0} 0 L{x0} {H} L{W/2 + side*W*0.18:.0f} {H} C{W/2 + side*W*0.12:.0f} {floor+40} {W/2 + side*W*0.16:.0f} {floor-260} '
                f'{W/2 + side*W*0.24:.0f} {floor-420} C{W/2 + side*W*0.28:.0f} {floor-600} {W/2 + side*W*0.36:.0f} 80 {x0 - side*240} 0 Z" '
                f'fill="#566E5C" stroke="{INK}" stroke-width="6"/>')
        out += (f'<path d="M{W/2 + side*W*0.2:.0f} {floor-150} q{side*60} -60 {side*130} -40 M{W/2 + side*W*0.26:.0f} {floor-430} q{side*50} -40 {side*120} -20" '
                f'stroke="#435747" stroke-width="10" fill="none" stroke-linecap="round"/>')
    return out


def scroll_doc(x: float, y: float, w: float = 640, h: float = 560, title: str = "", lines: list | None = None,
               seal: bool = True, size: int = 34) -> str:
    lines = lines or []
    txt = "".join(f'<text x="{x}" y="{y - h/2 + 150 + i*size*1.5:.0f}" font-size="{size}" text-anchor="middle" fill="#4A3424">{l}</text>' for i, l in enumerate(lines))
    return (f'<rect x="{x-w/2:.0f}" y="{y-h/2:.0f}" width="{w}" height="{h}" fill="#F3E3BC" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x-w/2-30:.0f}" y="{y-h/2-24:.0f}" width="{w+60}" height="36" rx="18" fill="#7A4E2C" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x-w/2-30:.0f}" y="{y+h/2-12:.0f}" width="{w+60}" height="36" rx="18" fill="#7A4E2C" stroke="{INK}" stroke-width="5"/>'
            f'<text x="{x}" y="{y - h/2 + 80:.0f}" font-size="{size+12}" text-anchor="middle" fill="#8E2A24">{title}</text>' + txt
            + (f'<rect x="{x + w/2 - 120:.0f}" y="{y + h/2 - 130:.0f}" width="80" height="80" fill="#C4453C" stroke="#8E2A24" stroke-width="5" transform="rotate(-6 {x + w/2 - 80:.0f} {y + h/2 - 90:.0f})"/>' if seal else ""))


def boat_supply(x: float, y: float, s: float = 1.0) -> str:
    """Thuyền chở lương (bao gạo)."""
    sacks = "".join(f'<ellipse cx="{-70+i*50}" cy="-58" rx="26" ry="20" fill="#E6D3A3" stroke="{INK}" stroke-width="4"/>' for i in range(4))
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">{sacks}'
            f'<path d="M-150 -40 L150 -40 C130 4 -130 4 -150 -40 Z" fill="#B5793F" stroke="{INK}" stroke-width="5"/></g>')


def horse(x: float, y: float, s: float = 1.0, flip: bool = False, color: str = "#8A5A3A") -> str:
    sx = -s if flip else s
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({sx:.2f} {s:.2f})">'
            f'<path d="M-62 -60 l-10 60 M-38 -58 l-2 58 M44 -58 l2 58 M66 -60 l8 60" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M-62 -60 l-10 60 M-38 -58 l-2 58 M44 -58 l2 58 M66 -60 l8 60" stroke="{color}" stroke-width="9" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="-92" rx="92" ry="44" fill="{color}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M62 -110 C80 -150 96 -176 108 -184 L150 -160 C152 -150 146 -142 136 -142 L112 -150 C104 -130 96 -112 84 -84 Z" fill="{color}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M100 -186 l-4 -22 l16 14 z" fill="{color}" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="128" cy="-166" r="4" fill="{INK}"/>'
            f'<path d="M66 -120 C78 -150 92 -176 104 -186" fill="none" stroke="#3A2418" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M-90 -100 C-130 -90 -132 -40 -118 -10" fill="none" stroke="#3A2418" stroke-width="14" stroke-linecap="round"/></g>')


def ribbon_title(kicker: str, title: str, x: float, y: float, size: int = 96, sub: str = "", gap: float = 1.08, kicker_dy: float = 0) -> str:
    """Khối tiêu đề riêng của kênh: nhãn đỏ nhỏ + tiêu đề lớn có viền + gạch chân vàng."""
    kw = len(kicker) * 30 * .62 + 60
    out = (f'<g transform="translate({x:.0f} {y:.0f})">'
           f'<rect x="0" y="{-60 + kicker_dy}" width="{kw:.0f}" height="50" rx="8" fill="{MINH}" stroke="{INK}" stroke-width="4"/>'
           f'<text x="{kw/2:.0f}" y="{-24 + kicker_dy}" font-size="30" text-anchor="middle" fill="#fff" letter-spacing="3">{kicker}</text>')
    for i, line in enumerate(title.split("|")):
        out += (f'<text x="0" y="{size*0.95 + i*size*gap:.0f}" font-size="{size}" fill="#FFF7E2" stroke="{INK}" stroke-width="14" paint-order="stroke" stroke-linejoin="round">{line}</text>')
    n = len(title.split("|"))
    out += f'<rect x="4" y="{size*0.95 + (n-1)*size*gap + 26:.0f}" width="{min(900, len(title.split("|")[-1])*size*.6):.0f}" height="14" rx="7" fill="{DV}"/>'
    if sub:
        out += f'<text x="0" y="{size*0.95 + (n-1)*size*gap + 100:.0f}" font-size="40" fill="#FFF7E2" stroke="{INK}" stroke-width="8" paint-order="stroke">{sub}</text>'
    return out + "</g>"


def panel(x: float, y: float, w: float, h: float, fill: str = "#FFF7E2", header: str = "", header_fill: str = MINH, size: int = 40) -> str:
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
    if header:
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="{size*1.9:.0f}" rx="26" fill="{header_fill}" stroke="{INK}" stroke-width="6"/>'
                f'<text x="{x + w/2}" y="{y + size*1.3:.0f}" font-size="{size}" text-anchor="middle" fill="#fff">{header}</text>')
    return out


def text(t: str, x: float, y: float, size: int = 44, color: str = INK, anchor: str = "middle", stroke: str = "") -> str:
    st = f' stroke="{stroke}" stroke-width="{size*0.16:.0f}" paint-order="stroke" stroke-linejoin="round"' if stroke else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}"{st}>{t}</text>'


def number_badge(n: str, x: float, y: float, r: float = 46, fill: str = DV) -> str:
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
            f'<text x="{x}" y="{y + r*0.38:.0f}" font-size="{r*1.1:.0f}" text-anchor="middle" fill="{INK}">{n}</text>')


def chains(x: float, y: float, s: float = 1.0) -> str:
    out = f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="#5E6670" stroke-width="12">'
    for i in range(6):
        out += f'<ellipse cx="{i*46}" cy="0" rx="30" ry="18" transform="rotate({20 if i%2 else -20} {i*46} 0)"/>'
    return out + "</g>"


def white_flag(x: float, y: float, s: float = 1.0) -> str:
    return (f'<g transform="translate({x} {y}) scale({s})"><line x1="0" y1="0" x2="0" y2="-200" stroke="#5A3A22" stroke-width="8"/>'
            f'<path d="M0 -200 Q60 -220 110 -195 Q60 -170 0 -150 Z" fill="#fff" stroke="{INK}" stroke-width="4"/></g>')


def dim(opacity: float = 0.35) -> str:
    return f'<rect width="{A.W}" height="{A.H}" fill="#101420" opacity="{opacity}"/>'


def vignette_circle(x: float, y: float, r: float = 220, ring: str = DV) -> str:
    """Vòng tròn khung (dùng kèm lớp minh hoạ đặt bên trong)."""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{ring}" stroke-width="14"/><circle cx="{x}" cy="{y}" r="{r+9}" fill="none" stroke="{INK}" stroke-width="5"/>'


# ------------------------------------------------------------------ dòng thời gian (tự thêm bởi make.py)
def timeline_bar(start: float, end: float, title: str, ticks: list | None = None) -> str:
    W, H = A.W, A.H
    y = H - 92
    x0, x1 = 120, W - 120
    out = (f'<rect x="0" y="{y-34}" width="{W}" height="{H-y+34}" fill="#FFF7E2" opacity=".93"/>'
           f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="16" rx="8" fill="{MINH}" stroke="{INK}" stroke-width="3"/>'
           f'<text x="{x0-14}" y="{y+16}" font-size="28" text-anchor="end" fill="{INK}">{start:g}</text>'
           f'<text x="{x1+14}" y="{y+16}" font-size="28" fill="{INK}">{end:g}</text>'
           f'<text x="{W/2}" y="{H-22}" font-size="32" text-anchor="middle" fill="{INK}" letter-spacing="2">{title}</text>')
    for t in ticks or []:
        tx = x0 + (x1 - x0) * (t - start) / (end - start)
        out += f'<rect x="{tx-2:.0f}" y="{y-6}" width="4" height="28" fill="{INK}"/>'
    return out


def timeline_marker(start: float, end: float, at: float, label: str) -> str:
    W, H = A.W, A.H
    y = H - 92
    x0, x1 = 120, W - 120
    x = x0 + (x1 - x0) * (min(max(at, start), end) - start) / (end - start)
    return (f'<path d="M{x:.0f} {y+22} l-16 26 h32 z" fill="{DV}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x-4:.0f}" y="{y-8}" width="8" height="32" fill="{INK}"/>'
            + map_tag(label, x, y - 30, 26, fill=INK))


def gorge_icon_text(t1: str, t2: str, x: float, y: float, size: int = 46) -> str:
    """Hai dòng chữ giữa thẻ (dùng cho infographic)."""
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{INK}">{t1}</text>'
            f'<text x="{x}" y="{y + size*1.35:.0f}" font-size="{size}" text-anchor="middle" fill="{MINH_D}">{t2}</text>')


def map_locator(view: str = "north", x: float = 24, y: float = 24, w: float = 230, h: float = 330, vn: str = DV) -> str:
    """Bản đồ định vị nhỏ: toàn Việt Nam + quần đảo Hoàng Sa, Trường Sa + khung vùng đang xem."""
    lon0, lon1, lat0, lat1 = 101.6, 117.8, 7.2, 23.8
    my = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
    sc = min(w / math.radians(lon1 - lon0), (h - 34) / (my(lat1) - my(lat0)))
    cx, cy = math.radians((lon0 + lon1) / 2), (my(lat0) + my(lat1)) / 2
    tx, ty = w / 2 - sc * cx, (h - 34) / 2 + 34 + sc * cy
    P = _mapgen({"s": sc, "tx": tx, "ty": ty, "w": int(w), "h": int(h), "pad": 0}, f"locator_{int(w)}x{int(h)}")
    pj = lambda la, lo: (sc * math.radians(lo) + tx, -sc * my(la) + ty)
    out = (f'<g transform="translate({x:.0f} {y:.0f})"><rect width="{w}" height="{h}" rx="16" fill="{SEA}" stroke="{INK}" stroke-width="4"/>'
           f'<clipPath id="lc_{int(x)}_{int(y)}"><rect width="{w}" height="{h}" rx="16"/></clipPath><g clip-path="url(#lc_{int(x)}_{int(y)})">')
    for cid, d in P["countries"].items():
        out += f'<path d="{d}" fill="#E3D9C3" stroke="#fff" stroke-width="1"/>'
    out += f'<path d="{P["vn"]}" fill="{vn}" stroke="#fff" stroke-width="1.2"/>'
    for name, dots in ISLAND_DOTS.items():
        for a, b in dots:
            px, py = pj(a, b)
            out += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{vn}" stroke="{INK}" stroke-width="1.2"/>'
    hx, hy = pj(*ISLANDS["QĐ. Hoàng Sa"])
    sx_, sy_ = pj(*ISLANDS["QĐ. Trường Sa"])
    lab = 'font-size="21" font-weight="700" text-anchor="middle" fill="#2B1B12" stroke="#FFF7E2" stroke-width="4" paint-order="stroke"'
    out += (f'<text x="{min(hx, w-86):.0f}" y="{hy-16:.0f}" {lab}>QĐ. HOÀNG SA</text>'
            f'<text x="{min(sx_-6, w-92):.0f}" y="{sy_+44:.0f}" {lab}>QĐ. TRƯỜNG SA</text>')
    v = VIEWS[view]
    (ax, ay), (bx, by) = pj(v["lat"][1], v["lon"][0]), pj(v["lat"][0], v["lon"][1])
    out += f'<rect x="{ax:.0f}" y="{ay:.0f}" width="{bx-ax:.0f}" height="{by-ay:.0f}" fill="none" stroke="{MINH}" stroke-width="3" stroke-dasharray="6 4"/>'
    out += (f'</g><rect width="{w}" height="30" rx="14" fill="{INK}"/>'
            f'<text x="{w/2:.0f}" y="21" font-size="17" text-anchor="middle" fill="#fff" letter-spacing="1">VỊ TRÍ TRÊN BẢN ĐỒ</text></g>')
    return out


# ================================================================== BỘ HÌNH TRẬN ĐÁNH v2 (chi tiết hơn)
def _shield(color: str, kind: str) -> str:
    if kind == "dv":  # khiên mây tròn
        return (f'<circle cx="-14" cy="-30" r="15" fill="#C9A15A" stroke="{INK}" stroke-width="2.5"/>'
                f'<circle cx="-14" cy="-30" r="9" fill="none" stroke="#8A6A32" stroke-width="2"/><circle cx="-14" cy="-30" r="3" fill="{color}"/>')
    return (f'<rect x="-28" y="-50" width="24" height="38" rx="5" fill="{color}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M-16 -46 v30" stroke="#F1D36B" stroke-width="2.5"/>')


def _soldier2(color: str, side: str, pose: str = "spear", mood: str = "calm") -> str:
    """Lính chi tiết: side 'dv' (nón, áo vàng nâu, khiên mây) / 'minh' (mũ sắt, giáp đỏ, khiên chữ nhật)."""
    dark = DV_D if side == "dv" else MINH_D
    head = (f'<path d="M-17 -60 L0 -76 L17 -60 Z" fill="#E6C98A" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>' if side == "dv"
            else f'<path d="M-12 -58 C-13 -78 13 -78 12 -58 Z" fill="#8F99A0" stroke="{INK}" stroke-width="2.5"/><path d="M-14 -58 h28" stroke="{INK}" stroke-width="3"/><path d="M0 -76 v-9" stroke="#D2352C" stroke-width="5" stroke-linecap="round"/>')
    weapon = {
        "spear": f'<line x1="18" y1="6" x2="34" y2="-84" stroke="#5A3A22" stroke-width="3.5"/><path d="M34 -84 l-3 -13 l8 2z" fill="#C9D0D4" stroke="{INK}" stroke-width="1.5"/>',
        "charge": f'<line x1="-6" y1="-30" x2="58" y2="-44" stroke="#5A3A22" stroke-width="3.5"/><path d="M58 -44 l12 -4 l-10 9z" fill="#C9D0D4" stroke="{INK}" stroke-width="1.5"/>',
        "bow": f'<path d="M22 -70 Q44 -36 22 -2" fill="none" stroke="#6B4226" stroke-width="3.5"/><line x1="22" y1="-70" x2="22" y2="-2" stroke="#ddd" stroke-width="1.2"/><line x1="4" y1="-36" x2="30" y2="-36" stroke="#5A3A22" stroke-width="2"/>',
        "sword": f'<line x1="14" y1="-40" x2="34" y2="-78" stroke="#C9D0D4" stroke-width="4" stroke-linecap="round"/><line x1="10" y1="-36" x2="20" y2="-44" stroke="{INK}" stroke-width="4"/>',
    }[pose]
    arm_end = {"spear": (18, -36), "charge": (14, -36), "bow": (20, -36), "sword": (14, -40)}[pose]
    return (f'<ellipse cx="0" cy="2" rx="20" ry="5" fill="#000" opacity=".18"/>'
            f'<path d="M-9 -16 L-12 2 M9 -16 L12 2" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M-9 -16 L-12 2 M9 -16 L12 2" stroke="#4A3424" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M-14 -46 L14 -46 L17 -14 L-17 -14 Z" fill="{color}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<path d="M-15 -30 h30" stroke="{dark}" stroke-width="3"/><path d="M0 -46 v32" stroke="{dark}" stroke-width="2"/>'
            + weapon
            + f'<path d="M10 -42 L{arm_end[0]} {arm_end[1]}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M10 -42 L{arm_end[0]} {arm_end[1]}" stroke="#EBC097" stroke-width="4" stroke-linecap="round"/>'
            + f'<circle cx="0" cy="-52" r="10" fill="#EBC097" stroke="{INK}" stroke-width="2.5"/>' + _mini_face(mood) + head
            + (_shield(color, side) if pose in ("spear", "charge", "sword") else ""))


def _mini_face(mood: str) -> str:
    """Nét mặt tí hon cho lính (đầu r=10, tâm 0,-52)."""
    if mood == "charge":   # hét xung trận
        return (f'<path d="M-6 -57 l4 2 M6 -57 l-4 2" stroke="{INK}" stroke-width="2"/><circle cx="-3.5" cy="-53" r="1.4" fill="{INK}"/><circle cx="3.5" cy="-53" r="1.4" fill="{INK}"/>'
                f'<ellipse cx="0" cy="-47.5" rx="3" ry="2.6" fill="#6E1E24"/>')
    if mood == "panic":    # hoảng
        return (f'<circle cx="-3.5" cy="-53" r="2.6" fill="#fff" stroke="{INK}" stroke-width="1"/><circle cx="3.5" cy="-53" r="2.6" fill="#fff" stroke="{INK}" stroke-width="1"/>'
                f'<circle cx="-3.5" cy="-53" r="1" fill="{INK}"/><circle cx="3.5" cy="-53" r="1" fill="{INK}"/><ellipse cx="0" cy="-47" rx="2.2" ry="3" fill="#6E1E24"/>'
                f'<path d="M10 -62 q4 6 0 9 q-4 -3 0 -9z" fill="#7FD0F2" stroke="#2B6F8F" stroke-width="1"/>')
    if mood == "smug":
        return f'<path d="M-6 -53 h4 M2 -53 h4" stroke="{INK}" stroke-width="1.8"/><path d="M-3 -48 q4 2 6 -1" stroke="{INK}" stroke-width="1.6" fill="none"/>'
    return f'<circle cx="-3.5" cy="-53" r="1.4" fill="{INK}"/><circle cx="3.5" cy="-53" r="1.4" fill="{INK}"/>'


def _rider2(color: str, side: str, mood: str = "calm") -> str:
    return (f'<g transform="scale(.42)">{horse(0, 0, 1.0, color="#7A5236" if side == "minh" else "#9A6B44")}</g>'
            f'<g transform="translate(6 -52) scale(.9)">{_soldier2(color, side, "charge" if side == "minh" else "sword", mood)}</g>'
            f'<path d="M-34 -48 q14 8 34 0" fill="{MINH_D if side == "minh" else DV_D}" opacity=".9"/>')


def troops(x: float, y: float, cols: int = 6, rows: int = 3, side: str = "minh", pose: str = "spear", s: float = 1.0,
           gap: float = 40, flip: bool = False, seed: int = 1, flags: int = 1, cavalry: bool = False, mood: str = "calm") -> str:
    """Khối quân v2 – có chiều sâu (hàng sau nhỏ & nhạt hơn), cờ phe. (x,y) = giữa-dưới hàng đầu."""
    color = DV if side == "dv" else MINH
    rnd = random.Random(seed)
    unit_w = gap * (1.7 if cavalry else 1)
    out = f'<g transform="translate({x:.0f} {y:.0f}) scale({-s if flip else s:.3f} {s:.3f})">'
    for r in range(rows - 1, -1, -1):
        k = 1 - r * 0.09
        shade = r * 0.12
        out += f'<g transform="translate(0 {-r*30*k:.0f}) scale({k:.3f})" opacity="{1 - shade*0.6:.2f}">'
        for c in range(cols):
            ox = (c - (cols - 1) / 2) * unit_w + (r % 2) * unit_w * 0.5 + rnd.uniform(-5, 5)
            p = pose if pose != "mix" else rnd.choice(["spear", "spear", "bow", "sword"])
            unit = _rider2(color, side, mood) if cavalry else _soldier2(color, side, p, mood)
            out += f'<g transform="translate({ox:.0f} {rnd.uniform(-3, 3):.0f})">{unit}</g>'
        out += "</g>"
    for i in range(flags):
        fx = ((i + 0.5) / flags - 0.5) * cols * unit_w
        top = -rows * 30 - 150
        flag_col = color
        out += (f'<line x1="{fx:.0f}" y1="{-rows*20:.0f}" x2="{fx:.0f}" y2="{top}" stroke="#5A3A22" stroke-width="5"/>'
                f'<path d="M{fx:.0f} {top} q40 -10 78 6 q-34 14 -78 30 z" fill="{flag_col}" stroke="{INK}" stroke-width="3"/>'
                f'<path d="M{fx+8:.0f} {top+8} q26 -4 50 4" stroke="{DV_D if side == "dv" else "#F1D36B"}" stroke-width="3" fill="none"/>')
    return out + "</g>"


def arrow_volley(x0: float, y0: float, x1: float, y1: float, n: int = 14, seed: int = 4, color: str = INK) -> str:
    """Mưa tên bay theo đường vòng cung từ (x0,y0) tới (x1,y1)."""
    rnd = random.Random(seed)
    out = ""
    for _ in range(n):
        t = rnd.uniform(0.25, 0.95)
        dx, dy = rnd.uniform(-90, 90), rnd.uniform(-40, 40)
        cx, cy = (x0 + x1) / 2, min(y0, y1) - 200
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1 + dx
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1 + dy
        tx_ = 2 * (1 - t) * (cx - x0) + 2 * t * (x1 - cx)
        ty_ = 2 * (1 - t) * (cy - y0) + 2 * t * (y1 - cy)
        ang = math.degrees(math.atan2(ty_, tx_))
        out += (f'<g transform="translate({px:.0f} {py:.0f}) rotate({ang:.0f})"><line x1="-26" y1="0" x2="20" y2="0" stroke="{color}" stroke-width="3"/>'
                f'<path d="M20 0 l-8 -4 l0 8z" fill="{color}"/><path d="M-26 0 l-7 -5 M-26 0 l-7 5" stroke="#B84A3A" stroke-width="2.5"/></g>')
    return out


def dust(x: float, y: float, w: float = 300, n: int = 9, seed: int = 2, opacity: float = 0.7) -> str:
    rnd = random.Random(seed)
    out = f'<g opacity="{opacity}">'
    for _ in range(n):
        out += f'<circle cx="{x + rnd.uniform(-w/2, w/2):.0f}" cy="{y - rnd.uniform(0, 60):.0f}" r="{rnd.uniform(26, 60):.0f}" fill="#D9C7A4"/>'
    return out + "</g>"


def rocks(x: float, y: float, n: int = 5, s: float = 1.0, seed: int = 3) -> str:
    rnd = random.Random(seed)
    out = ""
    for _ in range(n):
        rx, ry = x + rnd.uniform(-90, 90) * s, y + rnd.uniform(-60, 60) * s
        r = rnd.uniform(16, 34) * s
        out += (f'<path d="M{rx-r:.0f} {ry:.0f} L{rx-r*.4:.0f} {ry-r:.0f} L{rx+r*.6:.0f} {ry-r*.8:.0f} L{rx+r:.0f} {ry+r*.2:.0f} L{rx+r*.2:.0f} {ry+r:.0f} Z" '
                f'fill="#8C8577" stroke="{INK}" stroke-width="3"/>'
                f'<path d="M{rx+r*1.1:.0f} {ry-r*1.4:.0f} l18 -22 M{rx+r*1.4:.0f} {ry-r*0.6:.0f} l22 -14" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".7"/>')
    return out


def tree(x: float, y: float, s: float = 1.0, color: str = "#3F6B4A") -> str:
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"><rect x="-6" y="-40" width="12" height="40" fill="#5A3A22"/>'
            f'<circle cx="0" cy="-70" r="38" fill="{color}" stroke="{INK}" stroke-width="3"/><circle cx="-26" cy="-50" r="26" fill="{color}" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="26" cy="-50" r="26" fill="{color}" stroke="{INK}" stroke-width="3"/><circle cx="-10" cy="-80" r="12" fill="#fff" opacity=".12"/></g>')


def gorge2(floor: float = 600, marsh: bool = True, seed: int = 5, mood: str = "day") -> str:
    """Ải Chi Lăng bản chi tiết: trời, dãy núi xa, vách đá 2 bên có cây & bóng đổ, lòng thung lũng, đầm lầy, cỏ."""
    W, H = A.W, A.H
    rnd = random.Random(seed)
    sky = {"day": "g_day", "storm": "g_storm", "dawn": "g_dawn"}[mood]
    out = (f'<defs><linearGradient id="cliffL" x1="0" x2="1"><stop offset="0" stop-color="#3E5446"/><stop offset="1" stop-color="#5F7A62"/></linearGradient>'
           f'<linearGradient id="cliffR" x1="1" x2="0"><stop offset="0" stop-color="#3E5446"/><stop offset="1" stop-color="#5F7A62"/></linearGradient>'
           f'<linearGradient id="vfloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9A06A"/><stop offset="1" stop-color="#7E8A4E"/></linearGradient></defs>'
           f'<rect width="{W}" height="{H}" fill="url(#{sky})"/>')
    out += A.karst(floor - 140, "#A9B8B0", seed + 1, hmin=180, hmax=320)
    out += A.karst(floor - 60, "#8DA294", seed + 2, hmin=140, hmax=260)
    out += A.mist(floor - 90, 0.45)
    out += f'<rect x="0" y="{floor}" width="{W}" height="{H-floor}" fill="url(#vfloor)"/>'
    out += f'<path d="M{W*0.30} {floor} C{W*0.36} {floor+140} {W*0.24} {H-180} {W*0.18} {H} L{W*0.82} {H} C{W*0.76} {H-180} {W*0.64} {floor+140} {W*0.70} {floor} Z" fill="#B49A63" opacity=".7"/>'
    if marsh:
        for cx, cy, rx in ((W*0.47, floor+120, 150), (W*0.56, floor+200, 190), (W*0.42, floor+260, 130), (W*0.6, floor+300, 120)):
            out += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx}" ry="{rx*.2:.0f}" fill="#62704A"/>'
                    f'<ellipse cx="{cx-rx*.2:.0f}" cy="{cy-4:.0f}" rx="{rx*.5:.0f}" ry="{rx*.06:.0f}" fill="#9FB3A0" opacity=".6"/>')
    for side in (-1, 1):
        x0 = 0 if side < 0 else W
        grad = "cliffL" if side < 0 else "cliffR"
        edge = [(W/2 + side*W*0.27, H), (W/2 + side*W*0.24, floor + 60), (W/2 + side*W*0.26, floor - 160),
                (W/2 + side*W*0.30, floor - 320), (W/2 + side*W*0.34, floor - 460), (W/2 + side*W*0.39, 60), (x0 - side*150, 0)]
        d = f"M{x0} 0 L{x0} {H} " + " ".join(f"L{px:.0f} {py:.0f}" for px, py in edge) + " Z"
        out += f'<path d="{d}" fill="url(#{grad})" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        for i in range(7):  # gờ đá
            yy = floor - 420 + i * 90 + rnd.randint(-20, 20)
            xx = W/2 + side*(W*0.30 + rnd.randint(0, 120))
            out += f'<path d="M{xx:.0f} {yy} q{side*50} -30 {side*120} -10" stroke="#34473A" stroke-width="9" fill="none" stroke-linecap="round"/>'
        for i in range(6):  # cây trên vách
            tx_ = W/2 + side*(W*0.32 + rnd.randint(0, 200))
            ty_ = floor - 450 + rnd.randint(0, 420)
            out += tree(tx_, ty_, rnd.uniform(0.5, 0.8), rnd.choice(["#3F6B4A", "#4C7A50", "#36603F"]))
    for i in range(40):  # cỏ tiền cảnh
        gx = rnd.uniform(0, W)
        if W*0.22 < gx < W*0.78:
            continue
        out += f'<path d="M{gx:.0f} {H} q{rnd.uniform(-10,10):.0f} -40 {rnd.uniform(-24,24):.0f} -{rnd.uniform(50,110):.0f}" stroke="#2F4A34" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return out


def legend(x: float, y: float, items: list, size: int = 30) -> str:
    """Chú thích màu phe: items = [[màu, nhãn], ...]."""
    w = max(len(t) for _, t in items) * size * 0.58 + 90
    h = len(items) * size * 1.5 + 24
    out = f'<g transform="translate({x:.0f} {y:.0f})"><rect width="{w:.0f}" height="{h:.0f}" rx="16" fill="#FFF7E2" stroke="{INK}" stroke-width="4" opacity=".95"/>'
    for i, (c, t) in enumerate(items):
        yy = 22 + i * size * 1.5
        out += (f'<rect x="18" y="{yy:.0f}" width="{size}" height="{size}" rx="6" fill="{c}" stroke="{INK}" stroke-width="3"/>'
                f'<text x="{30+size}" y="{yy+size*0.85:.0f}" font-size="{size}" fill="{INK}">{t}</text>')
    return out + "</g>"


def siege_ring(place, view: str = "north", r: float = 70, n: int = 14, color: str = DV) -> str:
    x, y = _place(place, view)
    out = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#FFF7E2" fill-opacity=".35" stroke="{INK}" stroke-width="6" stroke-dasharray="14 10"/>'
    for i in range(n):
        a = 2 * math.pi * i / n
        out += f'<path d="M{x + r*math.cos(a):.0f} {y + r*math.sin(a) - 14:.0f} l-12 18 h24 z" fill="{color}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    return out


# ================================================================== CẢNH ĐỜI SỐNG (đô hộ): dân, quan thu thuế, lao dịch, đốt sách
def peasant(x: float, y: float, s: float = 1.0, pose: str = "stand", expr: str = "sad", flip: bool = False,
            shirt: str = "#7A5A3A", hat: bool = True) -> str:
    """Người dân Đại Việt (nón lá, áo nâu). pose: stand | carry (gánh bao trên lưng) | haul (kéo dây) | bow | kneel | reach.
    expr: sad | cry | sweat | scared | tired."""
    sx = -s if flip else s
    I = INK
    body_tilt = {"carry": 18, "haul": -24, "bow": 38, "kneel": 10, "reach": -8}.get(pose, 0)
    legs = (f'<path d="M-10 -40 L-16 0 M10 -40 L16 0" stroke="{I}" stroke-width="11" stroke-linecap="round"/>'
            f'<path d="M-10 -40 L-16 0 M10 -40 L16 0" stroke="#D9A57A" stroke-width="6" stroke-linecap="round"/>'
            if pose != "kneel" else
            f'<path d="M-12 -30 L-30 -4 L4 -4 M12 -30 L24 0" stroke="{I}" stroke-width="11" stroke-linecap="round" fill="none"/>'
            f'<path d="M-12 -30 L-30 -4 L4 -4 M12 -30 L24 0" stroke="#D9A57A" stroke-width="6" stroke-linecap="round" fill="none"/>')
    pants = f'<path d="M-18 -66 L18 -66 L16 -36 L-16 -36 Z" fill="#3E3A36" stroke="{I}" stroke-width="3"/>'
    arms = {
        "carry": f'<path d="M14 -100 L30 -128" stroke="{I}" stroke-width="10" stroke-linecap="round"/>',
        "haul": f'<path d="M14 -100 L58 -112 M-10 -100 L40 -118" stroke="{I}" stroke-width="10" stroke-linecap="round"/>',
        "bow": f'<path d="M12 -100 L26 -70 M-12 -100 L4 -72" stroke="{I}" stroke-width="10" stroke-linecap="round"/>',
        "reach": f'<path d="M14 -104 L62 -116" stroke="{I}" stroke-width="10" stroke-linecap="round"/>',
        "kneel": f'<path d="M12 -98 L28 -128 M-12 -98 L-24 -128" stroke="{I}" stroke-width="10" stroke-linecap="round"/>',
    }.get(pose, f'<path d="M14 -100 L22 -66 M-14 -100 L-22 -66" stroke="{I}" stroke-width="10" stroke-linecap="round"/>')
    eyes = {"cry": '<path d="M-9 -146 q4 -4 8 0 M3 -146 q4 -4 8 0" stroke="#2B1B12" stroke-width="2.5" fill="none"/>',
            "scared": '<circle cx="-5" cy="-146" r="4" fill="#fff" stroke="#2B1B12" stroke-width="1.5"/><circle cx="7" cy="-146" r="4" fill="#fff" stroke="#2B1B12" stroke-width="1.5"/><circle cx="-5" cy="-146" r="1.6" fill="#2B1B12"/><circle cx="7" cy="-146" r="1.6" fill="#2B1B12"/>',
            "tired": '<path d="M-9 -146 h8 M3 -146 h8" stroke="#2B1B12" stroke-width="2.5"/>'}.get(expr, '<circle cx="-5" cy="-146" r="2" fill="#2B1B12"/><circle cx="7" cy="-146" r="2" fill="#2B1B12"/>')
    brows = '<path d="M-10 -154 L-1 -151 M3 -151 L12 -154" stroke="#2B1B12" stroke-width="2.5"/>' if expr != "sad" else '<path d="M-10 -151 L-1 -155 M3 -155 L12 -151" stroke="#2B1B12" stroke-width="2.5"/>'
    mouth = {"cry": '<path d="M-4 -134 q5 -7 10 0z" fill="#6E1E24"/>', "scared": '<ellipse cx="1" cy="-134" rx="3" ry="4" fill="#6E1E24"/>',
             "tired": '<path d="M-4 -134 q5 3 10 0" stroke="#2B1B12" stroke-width="2.5" fill="none"/><path d="M-3 -131 v5" stroke="#7FD0F2" stroke-width="2"/>'}.get(
        expr, '<path d="M-4 -133 q5 -4 10 0" stroke="#2B1B12" stroke-width="2.5" fill="none"/>')
    fx = ""
    if expr == "cry":
        fx = '<path d="M-7 -142 q-2 10 0 18 M9 -142 q2 10 0 18" stroke="#7FD0F2" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    if expr in ("sweat", "tired"):
        fx = '<path d="M20 -160 q7 10 0 15 q-7 -5 0 -15z" fill="#7FD0F2" stroke="#2B6F8F" stroke-width="1.5"/><path d="M-22 -150 q6 9 0 13 q-6 -4 0 -13z" fill="#7FD0F2" stroke="#2B6F8F" stroke-width="1.5"/>'
    head = (f'<circle cx="2" cy="-144" r="17" fill="#E2AE82" stroke="{I}" stroke-width="3"/>' + brows + eyes + mouth + fx
            + (f'<path d="M-26 -152 L2 -182 L30 -152 Z" fill="#E6C98A" stroke="{I}" stroke-width="3" stroke-linejoin="round"/><path d="M-14 -160 L2 -176 M18 -160 L2 -176" stroke="#C9A96A" stroke-width="2"/>' if hat else
               f'<path d="M-15 -152 q17 -18 34 0" fill="#1E1A17"/>'))
    torso = f'<path d="M-18 -120 L20 -120 L22 -64 L-20 -64 Z" fill="{shirt}" stroke="{I}" stroke-width="3" stroke-linejoin="round"/><path d="M-19 -92 h40" stroke="#5A3F28" stroke-width="2"/>'
    load = ""
    if pose == "carry":
        load = f'<ellipse cx="-14" cy="-128" rx="30" ry="24" fill="#E6D3A3" stroke="{I}" stroke-width="3"/><path d="M-30 -140 q16 8 32 0" stroke="#B39B66" stroke-width="2" fill="none"/>'
    upper = f'<g transform="rotate({body_tilt} 0 -66)">{torso}{load}{arms}{head}</g>'
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({sx:.2f} {s:.2f})">'
            f'<ellipse cx="0" cy="2" rx="30" ry="6" fill="#000" opacity=".2"/>{legs}{pants}{upper}</g>')


def official_fig(x: float, y: float, s: float = 1.0, expr: str = "smug", flip: bool = False, item: str = "ledger") -> str:
    """Quan thu thuế nhà Minh (mũ cánh chuồn, áo đỏ tía) – dáng đứng, cầm sổ hoặc roi."""
    sx = -s if flip else s
    I = INK
    face = {"smug": '<path d="M-10 -150 h7 M4 -150 h7" stroke="#2B1B12" stroke-width="3"/><path d="M-6 -134 q8 5 14 -3" stroke="#2B1B12" stroke-width="3" fill="none"/>',
            "angry": '<path d="M-11 -156 L-2 -151 M4 -151 L13 -156" stroke="#2B1B12" stroke-width="3"/><circle cx="-6" cy="-147" r="2.2" fill="#2B1B12"/><circle cx="8" cy="-147" r="2.2" fill="#2B1B12"/><path d="M-6 -132 q7 -6 14 0z" fill="#6E1E24"/>'
            }.get(expr, '<circle cx="-6" cy="-148" r="2.2" fill="#2B1B12"/><circle cx="8" cy="-148" r="2.2" fill="#2B1B12"/>')
    hold = (f'<rect x="20" y="-116" width="34" height="44" rx="3" fill="#F3E3BC" stroke="{I}" stroke-width="3" transform="rotate(-12 37 -94)"/><path d="M26 -104 h22 M26 -96 h20 M26 -88 h22" stroke="#8A6A32" stroke-width="2"/>'
            if item == "ledger" else f'<path d="M22 -96 Q70 -150 92 -110" stroke="#5A3A22" stroke-width="5" fill="none"/>')
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({sx:.2f} {s:.2f})">'
            f'<ellipse cx="0" cy="2" rx="40" ry="7" fill="#000" opacity=".2"/>'
            f'<path d="M-30 -122 L30 -122 L42 0 L-42 0 Z" fill="#7A3E5A" stroke="{I}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M-36 -40 h72" stroke="#F1D36B" stroke-width="4"/><rect x="-14" y="-108" width="28" height="22" fill="#F1D36B" stroke="{I}" stroke-width="2"/>'
            f'<path d="M-30 -110 L-46 -70 M30 -110 L20 -92" stroke="{I}" stroke-width="12" stroke-linecap="round"/>{hold}'
            f'<path d="M-20 -126 q22 44 44 0" fill="#2A2420"/>'
            f'<circle cx="2" cy="-146" r="20" fill="#EAC29C" stroke="{I}" stroke-width="3"/>{face}'
            f'<path d="M-14 -138 q16 10 32 0 q-4 12 -16 12 q-12 0 -16 -12z" fill="#2A2420"/>'
            f'<path d="M-18 -158 L-16 -178 L20 -178 L22 -158 Z" fill="#1E1A17" stroke="{I}" stroke-width="3"/>'
            f'<ellipse cx="-34" cy="-170" rx="16" ry="6" fill="#1E1A17"/><ellipse cx="38" cy="-170" rx="16" ry="6" fill="#1E1A17"/></g>')


def sacks(x: float, y: float, n: int = 6, s: float = 1.0, label: str = "", seed: int = 2) -> str:
    rnd = random.Random(seed)
    out = f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
    k = 0
    for row in range(3):
        for c in range(max(1, n // 2 - row)):
            if k >= n:
                break
            cx = (c - (n // 2 - row - 1) / 2) * 64 + rnd.uniform(-4, 4)
            cy = -row * 46
            out += (f'<ellipse cx="{cx:.0f}" cy="{cy - 26}" rx="34" ry="28" fill="#E6D3A3" stroke="{INK}" stroke-width="3"/>'
                    f'<path d="M{cx-12:.0f} {cy-52} q12 -10 24 0" stroke="#B39B66" stroke-width="3" fill="none"/>')
            k += 1
    if label:
        out += f'<text x="0" y="-150" font-size="30" text-anchor="middle" fill="{INK}" stroke="#FFF7E2" stroke-width="6" paint-order="stroke">{label}</text>'
    return out + "</g>"


def hut(x: float, y: float, s: float = 1.0) -> str:
    """Nhà tranh vách đất."""
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
            f'<rect x="-110" y="-120" width="220" height="120" fill="#C9A77A" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-140 -110 L0 -220 L140 -110 Z" fill="#B58B4A" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            + "".join(f'<path d="M{-120+i*30} -118 L{-100+i*24} -200" stroke="#8E6A33" stroke-width="3"/>' for i in range(9))
            + f'<rect x="-30" y="-80" width="60" height="80" fill="#5A3F28" stroke="{INK}" stroke-width="3"/></g>')


def stone_block(x: float, y: float, s: float = 1.0) -> str:
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
            f'<path d="M-90 0 L-80 -110 L70 -118 L96 -6 Z" fill="#9A958A" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M-60 -70 l40 6 M10 -90 l36 10 M-30 -30 l50 -4" stroke="#7D786E" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M-130 30 h260" stroke="#6B4226" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="-110" cy="30" r="14" fill="#6B4226" stroke="{INK}" stroke-width="3"/><circle cx="0" cy="30" r="14" fill="#6B4226" stroke="{INK}" stroke-width="3"/><circle cx="110" cy="30" r="14" fill="#6B4226" stroke="{INK}" stroke-width="3"/></g>')


def rope(x1: float, y1: float, x2: float, y2: float) -> str:
    d = f"M{x1} {y1} Q{(x1+x2)/2} {max(y1, y2)+24} {x2} {y2}"
    return (f'<path d="{d}" stroke="#2B1B12" stroke-width="13" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#C9A96A" stroke-width="8" fill="none" stroke-dasharray="12 5" stroke-linecap="round"/>')


def mine(x: float, y: float, s: float = 1.0) -> str:
    """Cửa hầm mỏ trong vách đá."""
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
            f'<path d="M-260 0 C-240 -260 -60 -360 80 -330 C220 -300 280 -140 300 0 Z" fill="#6E6A60" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-70 0 C-70 -150 70 -150 70 0 Z" fill="#1E1A17" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-78 0 V-130 M78 0 V-130 M-90 -126 H90" stroke="#6B4226" stroke-width="16"/>'
            f'<circle cx="-30" cy="-60" r="10" fill="#F4C430" opacity=".8"/><circle cx="20" cy="-40" r="8" fill="#F4C430" opacity=".6"/></g>')


def fire(x: float, y: float, s: float = 1.0) -> str:
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
            f'<ellipse cx="0" cy="0" rx="110" ry="24" fill="#3A2A1E"/>'
            f'<path d="M-90 -4 C-100 -80 -40 -90 -50 -160 C-10 -120 10 -150 0 -210 C50 -150 40 -110 60 -140 C90 -90 100 -40 90 -4 Z" fill="#F07A2A" stroke="#8E2A24" stroke-width="5"/>'
            f'<path d="M-50 -4 C-60 -60 -20 -60 -20 -110 C10 -80 20 -100 20 -130 C50 -90 60 -50 50 -4 Z" fill="#F4C430"/>'
            + "".join(f'<circle cx="{dx}" cy="{dy}" r="{r}" fill="#9AA0A6" opacity=".5"/>' for dx, dy, r in ((-30, -250, 30), (20, -300, 40), (-10, -360, 50)))
            + "</g>")


def books(x: float, y: float, n: int = 6, s: float = 1.0, seed: int = 4) -> str:
    rnd = random.Random(seed)
    out = f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
    for i in range(n):
        bx, by = rnd.uniform(-90, 90), -i * 18 + rnd.uniform(-4, 4)
        col = rnd.choice(["#8E2A24", "#2F4D8F", "#6B4226", "#3F6B4A"])
        out += (f'<g transform="translate({bx:.0f} {by:.0f}) rotate({rnd.uniform(-25, 25):.0f})"><rect x="-44" y="-16" width="88" height="20" rx="3" fill="{col}" stroke="{INK}" stroke-width="3"/>'
                f'<rect x="-40" y="-13" width="80" height="4" fill="#F3E3BC"/></g>')
    return out + "</g>"


def crate(x: float, y: float, s: float = 1.0, label: str = "") -> str:
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"><rect x="-70" y="-90" width="140" height="90" fill="#9C7A4E" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-70 -45 h140 M-70 -90 L70 0 M70 -90 L-70 0" stroke="#6B4F2E" stroke-width="5"/>'
            + books(0, -96, 3, 0.8, 9)
            + (f'<text x="0" y="-36" font-size="26" text-anchor="middle" fill="#FFF7E2" stroke="{INK}" stroke-width="5" paint-order="stroke">{label}</text>' if label else "") + "</g>")
