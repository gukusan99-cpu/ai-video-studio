"""Thư viện vẽ vector (SVG) cho kênh "Tí Xuyên Sử".

Mọi nhân vật / đạo cụ / bối cảnh được vẽ bằng code => miễn phí, tự động,
và nhân vật luôn giống hệt nhau giữa các tập (character consistency 100%).

Toạ độ chuẩn: khung dọc 1080 x 1920 (YouTube Shorts).
"""
from __future__ import annotations

import base64
import math
import random
from pathlib import Path

W, H = 1080, 1920
ROOT = Path(__file__).resolve().parent.parent
FONT_FILE = ROOT / "assets" / "fonts" / "BeVietnamPro-ExtraBold.ttf"

INK = "#2B1B12"  # màu viền hoạt hình
SKIN = "#F2C29B"
SHIRT = "#2F4D8F"
SCARF = "#D62F3A"
GOLD = "#F4C430"


# ---------------------------------------------------------------- tiện ích
def _font_face() -> str:
    if not FONT_FILE.exists():
        return ""
    b64 = base64.b64encode(FONT_FILE.read_bytes()).decode()
    return (
        "<style>@font-face{font-family:'BVP';"
        f"src:url(data:font/ttf;base64,{b64}) format('truetype');}}"
        "text{font-family:'BVP',sans-serif;}</style>"
    )


def svg_doc(body: str, defs: str = "", w: int | None = None, h: int | None = None) -> str:
    w, h = w or W, h or H
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {W} {H}">{_font_face()}<defs>{DEFS}{defs}</defs>{body}</svg>'
    )


DEFS = """
<linearGradient id="g_day" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FC0EE"/><stop offset="1" stop-color="#F6EBD3"/></linearGradient>
<linearGradient id="g_dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5F7FBF"/><stop offset=".55" stop-color="#F6A871"/><stop offset="1" stop-color="#FCE4C2"/></linearGradient>
<linearGradient id="g_night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1533"/><stop offset="1" stop-color="#34497A"/></linearGradient>
<linearGradient id="g_mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FA5B3"/><stop offset="1" stop-color="#E3E9EA"/></linearGradient>
<linearGradient id="g_storm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3B4256"/><stop offset="1" stop-color="#A07A62"/></linearGradient>
<linearGradient id="g_water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4C8DB0"/><stop offset="1" stop-color="#1F4C6B"/></linearGradient>
<linearGradient id="g_water_t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4C8DB0" stop-opacity=".88"/><stop offset="1" stop-color="#1F4C6B" stop-opacity=".95"/></linearGradient>
<linearGradient id="g_mud" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A6A4A"/><stop offset="1" stop-color="#5A412C"/></linearGradient>
<radialGradient id="g_glow"><stop offset="0" stop-color="#FFE27A" stop-opacity=".95"/><stop offset="1" stop-color="#FFE27A" stop-opacity="0"/></radialGradient>
<radialGradient id="g_spot" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#FFF6DA" stop-opacity=".8"/><stop offset="1" stop-color="#FFF6DA" stop-opacity="0"/></radialGradient>
"""


def _pt(x, y):
    return f"{x:.1f} {y:.1f}"


# ---------------------------------------------------------------- nhân vật Tí
POSES = {
    #        (vai_trai, khuyu_trai), (vai_phai, khuyu_phai)  độ, tính từ hướng thẳng xuống
    "stand": ((14, 8), (14, 8)),
    "wave": ((14, 8), (122, 40)),
    "point": ((14, 8), (92, -4)),
    "cheer": ((125, 35), (125, 35)),
    "think": ((14, 8), (35, 130)),
    "hold": ((40, 75), (40, 75)),
    "shock": ((120, 40), (120, 40)),
    "run": ((-35, 60), (50, 70)),
}


def _arm(side: int, shoulder: float, elbow: float) -> str:
    sx, sy = side * 78, -300
    a = math.radians(shoulder)
    ex, ey = sx + side * 78 * math.sin(a), sy + 78 * math.cos(a)
    b = math.radians(shoulder + elbow)
    hx, hy = ex + side * 70 * math.sin(b), ey + 70 * math.cos(b)
    return (
        f'<path d="M{_pt(sx,sy)} L{_pt(ex,ey)}" stroke="{INK}" stroke-width="48" stroke-linecap="round"/>'
        f'<path d="M{_pt(ex,ey)} L{_pt(hx,hy)}" stroke="{INK}" stroke-width="38" stroke-linecap="round"/>'
        f'<path d="M{_pt(ex,ey)} L{_pt(hx,hy)}" stroke="{SKIN}" stroke-width="28" stroke-linecap="round"/>'
        f'<path d="M{_pt(sx,sy)} L{_pt(ex,ey)}" stroke="{SHIRT}" stroke-width="38" stroke-linecap="round"/>'
        f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="21" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>'
    ), (hx, hy)


def _face(expr: str, look: int) -> str:
    ex = look * 8
    big = 1.18 if expr in ("surprised", "shock") else 1.0
    eyes = ""
    for s in (-1, 1):
        cx, cy = s * 50, -432
        eyes += (
            f'<ellipse cx="{cx}" cy="{cy}" rx="{30*big:.0f}" ry="{37*big:.0f}" fill="#fff" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{cx+ex}" cy="{cy+4}" r="{21*big:.0f}" fill="#4A2C17"/>'
            f'<circle cx="{cx+ex}" cy="{cy+4}" r="{11*big:.0f}" fill="#120A05"/>'
            f'<circle cx="{cx+ex-7}" cy="{cy-7}" r="7" fill="#fff"/>'
        )
    brow_tilt = {"worried": 10, "surprised": -6, "shock": -8, "determined": -12}.get(expr, 0)
    brows = "".join(
        f'<path d="M{_pt(s*25, -474)} '
        f'L{_pt(s*72, -474 + brow_tilt)}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
        for s in (-1, 1)
    )
    if expr in ("surprised", "shock"):
        mouth = f'<ellipse cx="0" cy="-362" rx="18" ry="25" fill="#7A2430" stroke="{INK}" stroke-width="5"/>'
    elif expr in ("excited", "cheer"):
        mouth = (
            f'<path d="M-40 -380 Q0 -305 40 -380 Z" fill="#7A2430" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            '<path d="M-20 -352 Q0 -335 20 -352 Q0 -345 -20 -352Z" fill="#E8707A"/>'
        )
    elif expr == "worried":
        mouth = f'<path d="M-24 -362 Q0 -378 24 -362" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    else:
        mouth = f'<path d="M-34 -378 Q0 -342 34 -378" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    blush = "".join(
        f'<ellipse cx="{s*88}" cy="-388" rx="22" ry="12" fill="#F28B8B" opacity=".55"/>' for s in (-1, 1)
    )
    return eyes + brows + mouth + blush


def ti(x: float, y: float, s: float = 1.0, pose: str = "stand", expr: str = "happy",
       flip: bool = False, glow: bool = False, look: int = 0, gecko: bool = True) -> str:
    """Nhân vật Tí: cậu bé 9 tuổi, tóc bát úp, áo bà ba chàm, khăn đỏ, đồng hồ thời gian vàng.
    (x, y) = điểm giữa bàn chân."""
    (ls, le), (rs, re_) = POSES.get(pose, POSES["stand"])
    larm, _ = _arm(-1, ls, le)
    rarm, _ = _arm(1, rs, re_)
    tr = f"translate({x:.1f} {y:.1f}) scale({-s if flip else s:.3f} {s:.3f})"
    glow_svg = '<circle cx="40" cy="-228" r="95" fill="url(#g_glow)"/>' if glow else ""
    body = f"""
<g transform="{tr}">
  <ellipse cx="0" cy="4" rx="120" ry="18" fill="#000" opacity=".18"/>
  <rect x="-58" y="-118" width="36" height="112" rx="16" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
  <rect x="22" y="-118" width="36" height="112" rx="16" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
  <ellipse cx="-42" cy="-6" rx="34" ry="15" fill="#6B4226" stroke="{INK}" stroke-width="5"/>
  <ellipse cx="42" cy="-6" rx="34" ry="15" fill="#6B4226" stroke="{INK}" stroke-width="5"/>
  <path d="M-80 -175 L80 -175 L74 -100 L6 -100 L0 -125 L-6 -100 L-74 -100 Z" fill="#1F2A44" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  {larm}
  <rect x="-88" y="-335" width="176" height="180" rx="56" fill="{SHIRT}" stroke="{INK}" stroke-width="5"/>
  <circle cx="0" cy="-285" r="6" fill="#E8E1CF"/><circle cx="0" cy="-245" r="6" fill="#E8E1CF"/><circle cx="0" cy="-205" r="6" fill="#E8E1CF"/>
  {glow_svg}
  <path d="M40 -330 L40 -250" stroke="#A87B00" stroke-width="4"/>
  <circle cx="40" cy="-228" r="24" fill="{GOLD}" stroke="#8A6400" stroke-width="5"/>
  <path d="M40 -228 L40 -243 M40 -228 L51 -222" stroke="#5A3E00" stroke-width="4" stroke-linecap="round"/>
  <path d="M-74 -330 L74 -330 L0 -262 Z" fill="{SCARF}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  <circle cx="0" cy="-318" r="13" fill="#B21E2A" stroke="{INK}" stroke-width="4"/>
  {rarm}
  <circle cx="-133" cy="-440" r="26" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
  <circle cx="133" cy="-440" r="26" fill="{SKIN}" stroke="{INK}" stroke-width="5"/>
  <circle cx="0" cy="-445" r="138" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>
  <path d="M-144 -470 C-160 -625 160 -625 144 -470 L124 -492 L98 -474 L70 -502 L40 -480 L10 -506 L-22 -482 L-52 -504 L-82 -478 L-112 -498 Z" fill="#1B1B1F" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  <path d="M6 -584 C-14 -632 40 -642 30 -606" fill="none" stroke="#1B1B1F" stroke-width="12" stroke-linecap="round"/>
  {_face(expr, look)}
  {_gecko() if gecko else ""}
</g>"""
    return body


def _gecko() -> str:
    """Mít — chú thạch sùng nhỏ luôn ngồi trên vai Tí."""
    return f"""
<g transform="translate(96 -350) rotate(-8)">
  <path d="M-30 6 C-60 10 -70 40 -48 52" fill="none" stroke="#3E9A45" stroke-width="10" stroke-linecap="round"/>
  <ellipse cx="0" cy="0" rx="36" ry="17" fill="#62C462" stroke="{INK}" stroke-width="4"/>
  <circle cx="34" cy="-10" r="19" fill="#62C462" stroke="{INK}" stroke-width="4"/>
  <circle cx="40" cy="-15" r="7" fill="#fff"/><circle cx="42" cy="-15" r="3.5" fill="#000"/>
  <path d="M-14 14 l-6 14 M14 14 l6 14" stroke="#3E9A45" stroke-width="7" stroke-linecap="round"/>
</g>"""


# ---------------------------------------------------------------- bối cảnh
def sky(kind: str = "day") -> str:
    out = f'<rect width="{W}" height="{H}" fill="url(#g_{kind})"/>'
    if kind == "night":
        rnd = random.Random(3)
        out += "".join(
            f'<circle cx="{rnd.randint(0,W)}" cy="{rnd.randint(0,900)}" r="{rnd.choice([2,2,3,4])}" fill="#fff" opacity="{rnd.uniform(.4,.9):.2f}"/>'
            for _ in range(70)
        )
        out += '<circle cx="820" cy="260" r="70" fill="#F4F0DA"/><circle cx="850" cy="240" r="62" fill="#152150" opacity=".25"/>'
    elif kind in ("day", "dawn"):
        cy = 330 if kind == "day" else 820
        out += f'<circle cx="790" cy="{cy}" r="95" fill="#FFF2B8" opacity=".9"/>'
        out += _clouds()
    return out


def _clouds() -> str:
    out = ""
    for cx, cy, s in ((200, 230, 1.0), (640, 150, .7), (930, 470, .8)):
        out += (
            f'<g transform="translate({cx} {cy}) scale({s})" fill="#fff" opacity=".85">'
            '<ellipse cx="0" cy="0" rx="120" ry="42"/><ellipse cx="-55" cy="-22" rx="60" ry="45"/>'
            '<ellipse cx="45" cy="-35" rx="70" ry="55"/></g>'
        )
    return out


def karst(base: float, color: str = "#5E8A6E", seed: int = 1, n: int = 6, hmin=260, hmax=560) -> str:
    """Dãy núi đá vôi kiểu vịnh Hạ Long / Quảng Yên."""
    rnd = random.Random(seed)
    out = ""
    x = -80
    while x < W + 80:
        w = rnd.randint(150, 260)
        h = rnd.randint(hmin, hmax)
        top = base - h
        out += (
            f'<path d="M{x} {base} C{x+10} {top+h*.35} {x+w*.15} {top} {x+w*.5} {top} '
            f'C{x+w*.85} {top} {x+w-10} {top+h*.4} {x+w} {base} Z" fill="{color}"/>'
        )
        x += int(w * rnd.uniform(.55, .85))
    return out


def mist(y: float, opacity: float = .55) -> str:
    return (
        f'<g fill="#fff" opacity="{opacity}">'
        f'<ellipse cx="200" cy="{y}" rx="420" ry="55"/><ellipse cx="820" cy="{y+40}" rx="460" ry="60"/>'
        f'<ellipse cx="520" cy="{y-30}" rx="380" ry="40"/></g>'
    )


def river(top: float, fill: str = "url(#g_water)") -> str:
    out = f'<rect x="0" y="{top}" width="{W}" height="{H-top}" fill="{fill}"/>'
    rnd = random.Random(int(top))
    for i in range(14):
        y = top + 40 + i * ((H - top) / 14)
        x = rnd.randint(-100, W - 200)
        L = rnd.randint(120, 300)
        out += f'<path d="M{x} {y:.0f} q{L/4:.0f} -14 {L/2:.0f} 0 t{L/2:.0f} 0" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="6" stroke-linecap="round"/>'
    return out


def bank(y: float, color: str = "#6F9A4B", side: str = "both") -> str:
    out = ""
    if side in ("left", "both"):
        out += f'<path d="M0 {y} C200 {y-40} 330 {y+30} 420 {y+120} L420 {H} L0 {H} Z" fill="{color}"/>'
    if side in ("right", "both"):
        out += f'<path d="M{W} {y} C{W-200} {y-40} {W-330} {y+30} {W-420} {y+120} L{W-420} {H} L{W} {H} Z" fill="{color}"/>'
    if side == "full":
        out += f'<path d="M0 {y} C300 {y-50} 700 {y+40} {W} {y-20} L{W} {H} L0 {H} Z" fill="{color}"/>'
    return out


def reeds(x: float, y: float, n: int = 9, h: float = 220, seed: int = 0) -> str:
    rnd = random.Random(seed)
    out = ""
    for i in range(n):
        xx = x + i * 18 + rnd.randint(-6, 6)
        hh = h * rnd.uniform(.7, 1.1)
        bend = rnd.randint(-40, 40)
        out += f'<path d="M{xx} {y} Q{xx+bend/2} {y-hh/2} {xx+bend} {y-hh}" fill="none" stroke="#4E7A35" stroke-width="9" stroke-linecap="round"/>'
        if i % 3 == 0:
            out += f'<ellipse cx="{xx+bend}" cy="{y-hh}" rx="9" ry="26" fill="#8A5A2B" transform="rotate({bend/3} {xx+bend} {y-hh})"/>'
    return out


def warship(x: float, y: float, s: float = 1.0, tilt: float = 0, broken: bool = False, flip: bool = False) -> str:
    """Chiến thuyền lớn quân Nguyên (không vẽ biểu tượng thật, chỉ cờ sẫm màu)."""
    sx = -s if flip else s
    sail = (
        '<path d="M-10 -330 L150 -330 L140 -120 L-10 -120 Z" fill="#D9C9A3" stroke="#2B1B12" stroke-width="5"/>'
        '<path d="M-10 -280 L148 -280 M-10 -230 L145 -230 M-10 -175 L142 -175" stroke="#9C8A63" stroke-width="5"/>'
        if not broken else
        '<path d="M-10 -300 L120 -260 L90 -150 L-10 -170 Z" fill="#C9B88F" stroke="#2B1B12" stroke-width="5" opacity=".9"/>'
    )
    mast_h = -360 if not broken else -250
    return f"""
<g transform="translate({x:.0f} {y:.0f}) rotate({tilt}) scale({sx:.3f} {s:.3f})">
  <path d="M-230 -60 L230 -60 L190 10 C100 40 -100 40 -190 10 Z" fill="#4A2E1F" stroke="#2B1B12" stroke-width="6" stroke-linejoin="round"/>
  <path d="M-200 -10 L200 -10" stroke="#2E1C12" stroke-width="10"/>
  <rect x="-170" y="-120" width="110" height="60" fill="#6B4430" stroke="#2B1B12" stroke-width="5"/>
  <path d="M-180 -120 L-50 -120 L-60 -140 L-170 -140 Z" fill="#3A2418" stroke="#2B1B12" stroke-width="5"/>
  <line x1="-10" y1="-60" x2="-10" y2="{mast_h}" stroke="#3A2418" stroke-width="12"/>
  {sail}
  <path d="M-10 {mast_h} L-75 {mast_h+18} L-10 {mast_h+36} Z" fill="#1E2433"/>
  {''.join(f'<circle cx="{c}" cy="-35" r="9" fill="#2E1C12"/>' for c in range(-150, 180, 55))}
</g>"""


def dvboat(x: float, y: float, s: float = 1.0, flip: bool = False, rowers: int = 2) -> str:
    """Thuyền nhỏ quân Đại Việt, cờ đỏ."""
    sx = -s if flip else s
    crew = ""
    for i in range(rowers):
        cx = -60 + i * 70
        crew += (
            f'<rect x="{cx-14}" y="-80" width="28" height="44" rx="10" fill="#8C5A32" stroke="#2B1B12" stroke-width="4"/>'
            f'<circle cx="{cx}" cy="-92" r="15" fill="{SKIN}" stroke="#2B1B12" stroke-width="4"/>'
            f'<path d="M{cx-32} -98 L{cx} -128 L{cx+32} -98 Z" fill="#E6C98A" stroke="#2B1B12" stroke-width="4" stroke-linejoin="round"/>'
            f'<line x1="{cx+10}" y1="-60" x2="{cx+60}" y2="20" stroke="#6B4226" stroke-width="7" stroke-linecap="round"/>'
        )
    return f"""
<g transform="translate({x:.0f} {y:.0f}) scale({sx:.3f} {s:.3f})">
  {crew}
  <path d="M-140 -40 L140 -40 C120 0 -120 0 -140 -40 Z" fill="#B5793F" stroke="#2B1B12" stroke-width="5" stroke-linejoin="round"/>
  <line x1="100" y1="-40" x2="100" y2="-190" stroke="#5A3A22" stroke-width="8"/>
  <path d="M100 -190 L175 -170 L100 -145 Z" fill="{SCARF}" stroke="#2B1B12" stroke-width="4"/>
</g>"""


def soldier(x: float, y: float, s: float = 1.0, arm_up: bool = False, flag: bool = False, flip: bool = False) -> str:
    sx = -s if flip else s
    arm = (
        '<path d="M18 -120 L45 -190" stroke="#2B1B12" stroke-width="18" stroke-linecap="round"/>'
        '<path d="M18 -120 L45 -190" stroke="#F0BE94" stroke-width="10" stroke-linecap="round"/>'
        if arm_up else
        '<path d="M18 -120 L40 -70" stroke="#2B1B12" stroke-width="18" stroke-linecap="round"/>'
        '<path d="M18 -120 L40 -70" stroke="#F0BE94" stroke-width="10" stroke-linecap="round"/>'
    )
    pole_top = -300 if flag else -260
    flag_svg = f'<path d="M48 {pole_top} L130 {pole_top+22} L48 {pole_top+48} Z" fill="{SCARF}" stroke="#2B1B12" stroke-width="4"/>' if flag else '<path d="M48 -260 l-10 -30 l20 0 z" fill="#9AA3A8" stroke="#2B1B12" stroke-width="3"/>'
    return f"""
<g transform="translate({x:.0f} {y:.0f}) scale({sx:.3f} {s:.3f})">
  <rect x="-24" y="-50" width="18" height="50" fill="#5A3A22"/><rect x="6" y="-50" width="18" height="50" fill="#5A3A22"/>
  <path d="M-36 -140 L36 -140 L44 -45 L-44 -45 Z" fill="#7A4E2A" stroke="#2B1B12" stroke-width="5" stroke-linejoin="round"/>
  <line x1="48" y1="-40" x2="48" y2="{pole_top}" stroke="#5A3A22" stroke-width="7"/>
  {flag_svg}
  {arm}
  <circle cx="0" cy="-165" r="27" fill="#F0BE94" stroke="#2B1B12" stroke-width="5"/>
  <path d="M-62 -170 L0 -226 L62 -170 Z" fill="#E6C98A" stroke="#2B1B12" stroke-width="5" stroke-linejoin="round"/>
</g>"""


def stake(x: float, y: float, h: float = 260, lean: float = 0, w: float = 30) -> str:
    """Cọc gỗ đầu nhọn. (x,y) = chân cọc."""
    return f"""
<g transform="translate({x:.0f} {y:.0f}) rotate({lean})">
  <path d="M{-w/2} 0 L{-w/2} {-h+40} L0 {-h} L{w/2} {-h+40} L{w/2} 0 Z" fill="#7B4F2C" stroke="#2B1B12" stroke-width="5" stroke-linejoin="round"/>
  <path d="M-3 -20 L-3 {-h+60}" stroke="#5A3A22" stroke-width="4"/>
</g>"""


def stake_field(y: float, n: int = 11, h: float = 250, seed: int = 5, x0=40, x1=W - 40) -> str:
    rnd = random.Random(seed)
    out = ""
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(n - 1, 1) + rnd.randint(-20, 20)
        out += stake(x, y + rnd.randint(-15, 25), h * rnd.uniform(.8, 1.1), rnd.randint(-14, 14))
    return out


def splash(x: float, y: float, s: float = 1.0) -> str:
    out = f'<g transform="translate({x} {y}) scale({s})" fill="#fff" stroke="#BFE3F2" stroke-width="4">'
    for dx, dy, r in ((-60, -20, 26), (-20, -70, 34), (30, -40, 30), (70, -90, 20), (-90, -80, 16), (100, -30, 18)):
        out += f'<circle cx="{dx}" cy="{dy}" r="{r}"/>'
    return out + "</g>"


def badge(text: str, x: float, y: float, size: int = 54, fill: str = "#FFF4D6", color: str = "#2B1B12") -> str:
    width = len(text) * size * 0.62 + 70
    return (
        f'<g transform="translate({x - width/2:.0f} {y})">'
        f'<rect width="{width:.0f}" height="{size*1.7:.0f}" rx="{size*.85:.0f}" fill="{fill}" stroke="{INK}" stroke-width="6"/>'
        f'<text x="{width/2:.0f}" y="{size*1.2:.0f}" font-size="{size}" text-anchor="middle" fill="{color}">{text}</text></g>'
    )


def museum_room(case_y: float = 1180) -> str:
    dy = case_y - 1180
    return f"""
<rect width="{W}" height="{H}" fill="#EFE5D3"/>
<rect y="{1250+dy}" width="{W}" height="{H-1250-dy}" fill="#B98B5E"/>
<path d="M0 {1250+dy} L{W} {1250+dy}" stroke="#8A6440" stroke-width="10"/>
<rect x="80" y="260" width="300" height="230" fill="#D6C5A5" stroke="#8A6440" stroke-width="12"/>
<path d="M100 470 L180 360 L240 420 L290 340 L360 470 Z" fill="#7FA38A"/>
<path d="M240 0 L120 1250 L960 1250 L840 0 Z" fill="url(#g_spot)" opacity=".7"/>
<g transform="translate(0 {dy})"><rect x="330" y="560" width="420" height="690" fill="#CFE6F0" fill-opacity=".35" stroke="#7F98A6" stroke-width="10"/>
<rect x="300" y="1180" width="480" height="90" fill="#6B4A30" stroke="{INK}" stroke-width="6"/>
{stake(540, 1180, 560, 4, 52)}
<rect x="420" y="1295" width="240" height="70" rx="10" fill="#2B1B12"/>
<text x="540" y="1342" font-size="34" text-anchor="middle" fill="#F4C430">CỌC BẠCH ĐẰNG</text></g>"""


def portal(cx: float, cy: float, r: float = 260) -> str:
    out = f'<circle cx="{cx}" cy="{cy}" r="{r*1.25}" fill="url(#g_glow)" opacity=".8"/>'
    for i in range(5):
        rr = r * (1 - i * .17)
        out += f'<circle cx="{cx}" cy="{cy}" r="{rr:.0f}" fill="none" stroke="#FFE27A" stroke-width="{10-i}" stroke-dasharray="{40+i*12} {24+i*6}" opacity="{.9-i*.12:.2f}"/>'
    return out


def water_layer(top: float) -> str:
    """Lớp nước bán trong suốt (dùng cho hiệu ứng thuỷ triều lên/xuống)."""
    return river(top, "url(#g_water_t)")
