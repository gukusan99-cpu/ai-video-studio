"""Dàn nhân vật "búp bê trụ" cho format fun (tham khảo cách vẽ của các kênh lịch sử hoạt hình – tự thiết kế,
không sao chép nhân vật của ai).

- Thân: khối trụ không tay, áo vẽ thẳng lên thân (cổ giao lĩnh, đai, nút, giáp vảy, bổ tử...), đổ bóng hình trụ.
- Mặt 2 cấp:  "hero"  – nhân vật chính: tròng mắt, mí, lông mày rậm, mũi, tai, râu có sợi, nghiến răng...
              "extra" – lính/dân: mắt chấm lờ đờ, miệng nét – hài kiểu tỉnh bơ.
- Gốc toạ độ (x, y) = điểm chân chạm đất. s=1 → cao ~290px (vừa khung 1920x1080 cùng lúc 3–6 người).

Dùng trong episode JSON:
    {"fn": "peg", "args": {"who": "leloi", "x": 600, "y": 900, "s": 1.2, "expr": "determined", "item": "sword"}}
    {"fn": "crowd", "args": {"who": "minh_soldier", "x": 1300, "y": 860, "n": 7, "rows": 2, "exprs": ["deadpan", "shock"]}}
Biểu cảm hero: neutral, smug, angry, grit, shock, scared, sad, laugh, determined, deadpan, sly, cry
Biểu cảm extra: deadpan, shock, panic, happy, angry, cry, sleepy
"""
from __future__ import annotations

import random

INK = "#1C1612"
SW = 4.5  # độ dày nét viền

# ------------------------------------------------------------------ hồ sơ nhân vật
# face: hero/extra/kid (teo = cậu bé dẫn chuyện; Tí = châu chấu, vẽ bằng chauchau()) · hat · outfit · màu áo/viền/đai · râu · tóc · da
CAST: dict[str, dict] = {
    "teo":         dict(name="Tèo", face="kid", hat="ti_hair", outfit="kid", coat="#2F4D8F", trim="#F4C430", sash="#D62F3A",
                        beard="", hair="#2A1E16", skin="#F2C9A0", side="host"),
    "leloi":       dict(name="Lê Lợi", face="hero", hat="khan", outfit="robe", coat="#C9932E", trim="#8E2A1E", sash="#8E2A1E",
                        beard="three", hair="#1E1814", skin="#E6B58A", lines=True, side="dv"),
    "nguyentrai":  dict(name="Nguyễn Trãi", face="hero", hat="scholar", outfit="robe", coat="#46667F", trim="#EDE6D3", sash="#2B3E4F",
                        beard="long", hair="#2B2622", skin="#EBC29A", lines=True, side="dv"),
    "lelai":       dict(name="Lê Lai", face="hero", hat="band", outfit="tunic", coat="#7A4E2A", trim="#C0392B", sash="#C0392B",
                        beard="stubble", hair="#1E1814", skin="#DFAE80", side="dv"),
    "tranluu":     dict(name="Trần Lựu", face="hero", hat="dv_helm", outfit="armor", coat="#6E7A4A", trim="#C9A227", sash="#4A3424",
                        beard="mustache", hair="#1E1814", skin="#DDA97C", side="dv"),
    "dv_soldier":  dict(name="Nghĩa quân", face="extra", hat="wrap", outfit="tunic", coat="#8A5A32", trim="#5A3A20", sash="#C0392B",
                        beard="", hair="#1E1814", skin="#E3B387", side="dv"),
    "peasant":     dict(name="Dân phu", face="extra", hat="non", outfit="peasant", coat="#6B5038", trim="#4A3424", sash="#B89A5A",
                        beard="", hair="#1E1814", skin="#D9A57A", side="dv"),
    "scholar":     dict(name="Nho sĩ", face="extra", hat="scholar", outfit="robe", coat="#3F6A8A", trim="#EDE6D3", sash="#22384A",
                        beard="", hair="#1E1814", skin="#EFC9A4", side="dv"),
    "lieuthang":   dict(name="Liễu Thăng", face="hero", hat="minh_helm", outfit="armor", coat="#A8302A", trim="#E0B43A", sash="#5A1612",
                        beard="full", hair="#1A1512", skin="#E9BC92", lines=True, side="minh"),
    "mocthanh":    dict(name="Mộc Thạnh", face="hero", hat="minh_helm_gold", outfit="armor", coat="#3E6B4A", trim="#E0B43A", sash="#22382A",
                        beard="full", beard_color="#8C8680", hair="#8C8680", skin="#E6BC94", lines=True, side="minh"),
    "vuongthong":  dict(name="Vương Thông", face="hero", hat="minh_helm", outfit="armor", coat="#5B3A6E", trim="#D9D2C4", sash="#2E1E3A",
                        beard="goatee", hair="#1A1512", skin="#EDC59E", side="minh"),
    "luongminh":   dict(name="Lương Minh", face="hero", hat="wusha", outfit="official", coat="#B23A30", trim="#E0B43A", sash="#3A2A1A",
                        beard="goatee", hair="#1A1512", skin="#EEC7A0", lines=True, side="minh"),
    "hoangphuc":   dict(name="Hoàng Phúc", face="hero", hat="wusha", outfit="official", coat="#6E2430", trim="#E0B43A", sash="#2A1A14",
                        beard="mustache", hair="#1A1512", skin="#F0CBA6", side="minh"),
    "thoitu":      dict(name="Thôi Tụ", face="hero", hat="minh_helm", outfit="armor", coat="#4A4E58", trim="#C0392B", sash="#22252B",
                        beard="full", hair="#1A1512", skin="#E2B68C", side="minh"),
    "minh_soldier": dict(name="Lính Minh", face="extra", hat="minh_cap", outfit="tunic", coat="#B8443A", trim="#EDE6D3", sash="#2A2420",
                         beard="", hair="#1A1512", skin="#EEC6A0", side="minh"),
}

HERO_EXPR = ("neutral", "smug", "angry", "grit", "shock", "scared", "sad", "laugh", "determined", "deadpan", "sly", "cry")
EXTRA_EXPR = ("deadpan", "shock", "panic", "happy", "angry", "cry", "sleepy")
EXTRA_ALIAS = {"smug": "deadpan", "cool": "deadpan", "wink": "happy", "laugh": "happy", "grit": "angry", "scared": "panic",
               "sad": "cry", "neutral": "deadpan", "determined": "angry", "sly": "deadpan"}


def _shade(c: str, k: float) -> str:
    c = c.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    f = (lambda v: int(min(255, v + (255 - v) * k))) if k > 0 else (lambda v: int(v * (1 + k)))
    return f"#{f(r):02x}{f(g):02x}{f(b):02x}"


# ------------------------------------------------------------------ thân
BODY = "M-62 -150 Q-62 -180 -34 -184 L34 -184 Q62 -180 62 -150 L60 -8 Q0 8 -60 -8 Z"
HEAD_Y = -232


OILP = ('<filter id="oilp" x="-15%" y="-10%" width="130%" height="120%" color-interpolation-filters="sRGB">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.05 0.7" numOctaves="2" seed="4" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="4.5" xChannelSelector="R" yChannelSelector="G" result="d"/>'
        '<feTurbulence type="fractalNoise" baseFrequency="0.05 0.16" numOctaves="3" seed="9" result="n2"/>'
        '<feDiffuseLighting in="n2" surfaceScale="1.5" diffuseConstant="1.0" lighting-color="#ffffff" result="lt">'
        '<feDistantLight azimuth="235" elevation="58"/></feDiffuseLighting>'
        '<feComposite in="lt" in2="d" operator="in" result="lt2"/>'
        '<feBlend in="d" in2="lt2" mode="multiply" result="m"/>'
        '<feComponentTransfer in="m" result="b"><feFuncR type="linear" slope="1.12"/><feFuncG type="linear" slope="1.1"/><feFuncB type="linear" slope="1.06"/></feComponentTransfer>'
        '<feComposite in="b" in2="d" operator="in"/></filter>')


def _defs(uid: str) -> str:
    return (f'<defs>{OILP}<clipPath id="cb{uid}"><path d="{BODY}"/></clipPath>'
            f'<linearGradient id="cy{uid}" x1="0" x2="1" y1="0" y2="0">'
            '<stop offset="0" stop-color="#000" stop-opacity=".34"/><stop offset=".3" stop-color="#000" stop-opacity="0"/>'
            '<stop offset=".42" stop-color="#fff" stop-opacity=".16"/><stop offset=".58" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".38"/></linearGradient>'
            f'<radialGradient id="hs{uid}" cx=".42" cy=".38" r=".7">'
            '<stop offset=".55" stop-color="#7A3A1A" stop-opacity="0"/><stop offset="1" stop-color="#7A3A1A" stop-opacity=".42"/></radialGradient>'
            '</defs>')


def _outfit(c: dict, uid: str) -> str:
    I, coat, trim, sash = INK, c["coat"], c["trim"], c["sash"]
    dark = _shade(coat, -0.3)
    o = c["outfit"]
    g = ""
    if o == "kid":  # áo bà ba chàm, 3 cúc trắng, quần soóc xanh đen, khăn quàng đỏ, đồng hồ thời gian vàng
        g += (f'<path d="M0 -184 V-40" stroke="{dark}" stroke-width="4"/>'
              + "".join(f'<circle cx="8" cy="{y}" r="6" fill="#F6F1E4" stroke="{I}" stroke-width="2"/>' for y in (-150, -118, -86))
              + f'<path d="M-62 -58 h28 M34 -58 h28" stroke="{dark}" stroke-width="3"/>'
              f'<rect x="-70" y="-44" width="140" height="44" fill="#1F2A44"/><path d="M0 -44 V0" stroke="{I}" stroke-width="3"/>'
              f'<path d="M-40 -186 Q0 -164 40 -186 L36 -172 Q0 -150 -36 -172Z" fill="{sash}" stroke="{I}" stroke-width="2.5"/>'
              f'<path d="M-6 -168 l-10 34 l12 -6 l8 8 l2 -36z" fill="{sash}" stroke="{I}" stroke-width="2.5"/>'
              f'<circle cx="-30" cy="-120" r="17" fill="{trim}" stroke="{I}" stroke-width="3"/><circle cx="-30" cy="-120" r="11" fill="#FFF6D0"/>'
              f'<path d="M-30 -120 v-8 M-30 -120 l6 4" stroke="{I}" stroke-width="2.2" stroke-linecap="round"/>')
    elif o in ("robe", "tunic", "peasant"):
        # cổ giao lĩnh (vạt phải đè vạt trái) + nẹp áo
        g += (f'<path d="M-36 -184 L18 -118 L18 0" fill="none" stroke="{dark}" stroke-width="7"/>'
              f'<path d="M-34 -186 L20 -120 L20 0" fill="none" stroke="{trim}" stroke-width="9"/>'
              f'<path d="M34 -186 L6 -150" stroke="{trim}" stroke-width="9"/>'
              f'<path d="M-22 -186 L0 -160 L20 -186" fill="#F3EBDA" stroke="{I}" stroke-width="2"/>')
        if o == "tunic":
            g += "".join(f'<circle cx="30" cy="{y}" r="4.5" fill="{_shade(trim, -0.2)}" stroke="{I}" stroke-width="1.5"/>' for y in (-60, -36))
        belt_y = -100
        g += (f'<rect x="-70" y="{belt_y}" width="140" height="{20 if o == "robe" else 14}" fill="{sash}" stroke="{I}" stroke-width="3"/>'
              f'<path d="M-28 {belt_y + 12} q-8 30 -18 44 M-22 {belt_y + 12} q2 30 -4 48" stroke="{sash}" stroke-width="9" stroke-linecap="round" fill="none"/>')
        if o == "robe":
            g += f'<rect x="-70" y="-34" width="140" height="30" fill="{trim}" opacity=".9"/><path d="M-70 -34 H70" stroke="{I}" stroke-width="2"/>'
        if o == "peasant":
            g += (f'<rect x="-44" y="-62" width="22" height="20" fill="{_shade(coat, 0.18)}" stroke="{I}" stroke-width="2" transform="rotate(-6 -33 -52)"/>'
                  f'<path d="M-66 -96 Q0 -82 66 -96" stroke="#B89A5A" stroke-width="6" fill="none" stroke-dasharray="10 4"/>')
    elif o == "armor":
        scales = ""
        for r, y in enumerate(range(-176, -98, 13)):
            off = 9 if r % 2 else 0
            scales += "".join(f'<path d="M{x - 9} {y} q9 12 18 0" fill="none" stroke="{_shade(coat, -0.4)}" stroke-width="2.4"/>'
                              for x in range(-72 + off, 80, 18))
        skirt = "".join(f'<rect x="{x}" y="-88" width="26" height="80" fill="{coat if i % 2 else _shade(coat, -0.15)}" stroke="{I}" stroke-width="2"/>'
                        for i, x in enumerate(range(-78, 70, 26)))
        g += (skirt + f'<rect x="-70" y="-184" width="140" height="90" fill="{coat}"/>' + scales
              + f'<path d="M-18 -184 L0 -164 L18 -184" fill="{trim}" stroke="{I}" stroke-width="2"/>'
              f'<circle cx="0" cy="-140" r="15" fill="{trim}" stroke="{I}" stroke-width="2.5"/><circle cx="0" cy="-140" r="6" fill="{_shade(trim, -0.35)}"/>'
              f'<rect x="-70" y="-100" width="140" height="16" fill="{sash}" stroke="{I}" stroke-width="3"/>'
              f'<rect x="-14" y="-104" width="28" height="24" rx="4" fill="{trim}" stroke="{I}" stroke-width="2.5"/>'
              f'<path d="M-70 -14 H70" stroke="{trim}" stroke-width="8"/>')
    elif o == "official":
        g += (f'<path d="M-30 -186 Q0 -150 30 -186" fill="none" stroke="{_shade(coat, -0.35)}" stroke-width="9"/>'
              f'<path d="M-30 -186 Q0 -154 30 -186" fill="none" stroke="#F3EBDA" stroke-width="3"/>'
              # bổ tử (miếng thêu hình chim/mây trên ngực)
              f'<rect x="-36" y="-150" width="72" height="62" fill="{trim}" stroke="{I}" stroke-width="2.5"/>'
              f'<rect x="-29" y="-143" width="58" height="48" fill="#3B5E7A"/>'
              f'<path d="M-18 -112 q10 -22 22 -10 q6 -14 16 -6 q-8 4 -10 14 q-10 10 -28 2z" fill="#F3EBDA" stroke="{I}" stroke-width="1.5"/>'
              f'<circle cx="16" cy="-133" r="6" fill="#D9442B"/>'
              # đai ngọc
              f'<path d="M-68 -80 Q0 -62 68 -80" stroke="{sash}" stroke-width="12" fill="none"/>'
              + "".join(f'<rect x="{x - 5}" y="{-80 + abs(x) * 0.0 + (18 - abs(x) * 0.25) - 8}" width="10" height="10" fill="#E8E1C8" stroke="{I}" stroke-width="1.2"/>'
                        for x in (-44, -22, 0, 22, 44)))
    return g


def _body(c: dict, uid: str) -> str:
    return (f'<ellipse cx="0" cy="0" rx="74" ry="13" fill="#000" opacity=".25"/>'
            f'<path d="{BODY}" fill="{c["coat"]}"/>'
            f'<g clip-path="url(#cb{uid})">{_outfit(c, uid)}<rect x="-70" y="-190" width="140" height="200" fill="url(#cy{uid})"/></g>'
            f'<path d="{BODY}" fill="none" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')


# ------------------------------------------------------------------ mặt
HEAD = "M-46 -10 C-48 -50 -30 -62 0 -62 C30 -62 48 -50 46 -10 C45 22 30 52 0 58 C-30 52 -45 22 -46 -10Z"
HEAD_KID = "M-50 -4 C-50 -50 -28 -60 0 -60 C28 -60 50 -50 50 -4 C50 30 30 52 0 54 C-30 52 -50 30 -50 -4Z"


def _eye(cx: float, kind: str, look: float = 0, skin: str = "#E0A97E") -> str:
    """Mắt hero: lòng trắng hình hạnh nhân + tròng + mí trên đậm."""
    I = INK
    sgn = 1 if cx > 0 else -1
    w = 12
    alm = f"M{cx - w} -4 Q{cx} -15 {cx + w} -4 Q{cx} 4 {cx - w} -4Z"
    if kind == "closed":
        return f'<path d="M{cx - w} -4 Q{cx} 4 {cx + w} -4" stroke="{I}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    if kind == "happy":
        return f'<path d="M{cx - w} -2 Q{cx} -12 {cx + w} -2" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    if kind == "wide":
        return (f'<ellipse cx="{cx}" cy="-5" rx="12" ry="11" fill="#fff" stroke="{I}" stroke-width="2.5"/>'
                f'<circle cx="{cx + look}" cy="-5" r="3" fill="{I}"/>')
    iris = (f'<circle cx="{cx + look}" cy="-5" r="5.6" fill="#4A2E1C"/><circle cx="{cx + look}" cy="-5" r="2.8" fill="#0E0A08"/>'
            f'<circle cx="{cx + look + 1.8}" cy="-7" r="1.4" fill="#fff"/>')
    clip = f'<clipPath id="e{int(cx)}{kind}"><path d="{alm}"/></clipPath>'
    out = f'<defs>{clip}</defs><path d="{alm}" fill="#FBF6EC"/><g clip-path="url(#e{int(cx)}{kind})">{iris}'
    if kind in ("half", "narrow"):  # mí sụp (lờ đờ / nheo)
        lid_y = -5 if kind == "half" else -2
        out += f'<rect x="{cx - w - 2}" y="-20" width="{2 * w + 4}" height="{20 + lid_y}" fill="{_shade(skin, -0.08)}"/>'
    out += "</g>"
    top_y = {"half": -5, "narrow": -2}.get(kind)
    if top_y is not None:
        out += f'<path d="M{cx - w - 1} {top_y} H{cx + w + 1}" stroke="{I}" stroke-width="4" stroke-linecap="round"/>'
    else:
        out += f'<path d="M{cx - w - 1} -4 Q{cx} -16 {cx + w + 1} -5" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    out += f'<path d="M{cx - w + 2} -1 Q{cx} 4 {cx + w - 2} -1" stroke="#8A5A3A" stroke-width="1.6" fill="none" opacity=".7"/>'
    return out


def _brows(kind: str, color: str) -> str:
    shapes = {  # (x1,y1, x2,y2) mép ngoài → mép trong, cho mắt trái; mắt phải đối xứng
        "flat": (-32, -22, -9, -21), "angry": (-33, -27, -8, -15), "up": (-32, -22, -9, -31),
        "raised": (-32, -30, -9, -32), "sad": (-32, -19, -9, -29), "down": (-32, -24, -9, -18),
    }
    def one(x1, y1, x2, y2, m=1):
        return (f'<path d="M{x1 * m} {y1} Q{(x1 + x2) / 2 * m} {min(y1, y2) - 5} {x2 * m} {y2} L{x2 * m} {y2 + 6} '
                f'Q{(x1 + x2) / 2 * m} {min(y1, y2) + 1} {x1 * m} {y1 + 5}Z" fill="{color}" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>')
    if isinstance(kind, tuple):
        l, r = kind
    else:
        l = r = kind
    return one(*shapes[l]) + one(*shapes[r], m=-1)


def _mouth(kind: str) -> str:
    I = INK
    return {
        "line": f'<path d="M-12 34 Q0 36 12 33" stroke="{I}" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "firm": f'<path d="M-14 34 H14" stroke="{I}" stroke-width="4" stroke-linecap="round"/><path d="M-6 41 H6" stroke="#9A5A3A" stroke-width="2"/>',
        "smirk": f'<path d="M-12 35 Q4 37 16 27" stroke="{I}" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "frown": f'<path d="M-13 38 Q0 29 13 38" stroke="{I}" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "grit": (f'<path d="M-20 28 Q0 24 20 28 L18 42 Q0 46 -18 42Z" fill="#fff" stroke="{I}" stroke-width="3"/>'
                 + "".join(f'<path d="M{x} 27 V44" stroke="{I}" stroke-width="1.6"/>' for x in (-11, -4, 3, 10))
                 + f'<path d="M-19 35 H19" stroke="{I}" stroke-width="1.6"/>'),
        "open": f'<ellipse cx="0" cy="37" rx="10" ry="13" fill="#4A1414" stroke="{I}" stroke-width="3"/><ellipse cx="0" cy="44" rx="6" ry="4" fill="#C8504A"/>',
        "laugh": (f'<path d="M-20 28 Q0 30 20 28 Q16 54 0 54 Q-16 54 -20 28Z" fill="#4A1414" stroke="{I}" stroke-width="3"/>'
                  f'<path d="M-17 30 Q0 33 17 30 L15 35 Q0 38 -15 35Z" fill="#fff"/>'),
        "wavy": f'<path d="M-15 36 q4 -5 8 0 t8 0 t8 0" stroke="{I}" stroke-width="3.2" fill="none" stroke-linecap="round"/>',
    }[kind]


HERO_MAP = {  # biểu cảm → (mắt, lông mày, miệng, nhìn ngang)
    "neutral": ("open", "flat", "line", 0), "smug": ("half", ("raised", "down"), "smirk", 3),
    "angry": ("narrow", "angry", "frown", 0), "grit": ("narrow", "angry", "grit", 0),
    "shock": ("wide", "raised", "open", 0), "scared": ("wide", "sad", "wavy", -2),
    "sad": ("half", "sad", "frown", 0), "laugh": ("happy", "up", "laugh", 0),
    "determined": ("open", "down", "firm", 0), "deadpan": ("half", "flat", "line", 0),
    "sly": ("narrow", ("flat", "down"), "smirk", 5), "cry": ("closed", "sad", "frown", 0),
}


def _beard(kind: str, color: str) -> str:
    I = INK
    lite = _shade(color, 0.25)
    strands = lambda pts: "".join(f'<path d="{p}" stroke="{lite}" stroke-width="1.6" fill="none" opacity=".8"/>' for p in pts)
    if kind == "three":  # râu ba chòm
        return (f'<path d="M-4 24 Q-20 22 -26 40 Q-18 32 -6 30Z M4 24 Q20 22 26 40 Q18 32 6 30Z" fill="{color}" stroke="{I}" stroke-width="1.5"/>'
                f'<path d="M-9 46 Q0 44 9 46 Q8 80 0 104 Q-8 80 -9 46Z" fill="{color}" stroke="{I}" stroke-width="2"/>'
                + strands(["M-3 52 Q-2 76 0 96", "M4 52 Q4 72 1 92"])
                + f'<path d="M-44 -6 Q-46 18 -38 28 L-34 4Z M44 -6 Q46 18 38 28 L34 4Z" fill="{color}"/>')
    if kind == "long":
        return (f'<path d="M-3 24 Q-16 26 -20 40 M3 24 Q16 26 20 40" stroke="{color}" stroke-width="4" fill="none" stroke-linecap="round"/>'
                f'<path d="M-7 46 Q0 44 7 46 Q6 100 0 136 Q-6 100 -7 46Z" fill="{color}" stroke="{I}" stroke-width="1.5"/>'
                + strands(["M0 54 Q1 90 0 126"]))
    if kind == "full":  # râu quai nón rậm
        return (f'<path d="M-46 -8 Q-50 40 -26 62 Q0 82 26 62 Q50 40 46 -8 Q40 20 26 26 Q0 18 -26 26 Q-40 20 -46 -8Z" fill="{color}" stroke="{I}" stroke-width="2.5"/>'
                f'<path d="M-24 28 Q0 16 24 28 Q12 32 0 28 Q-12 32 -24 28Z" fill="{_shade(color, -0.25)}"/>'
                + strands(["M-36 20 Q-34 40 -24 54", "M-18 44 Q-14 60 -8 70", "M18 44 Q14 60 8 70", "M36 20 Q34 40 24 54", "M0 50 V74"]))
    if kind == "goatee":
        return (f'<path d="M-16 26 Q0 20 16 26 Q8 30 0 28 Q-8 30 -16 26Z" fill="{color}" stroke="{I}" stroke-width="1.5"/>'
                f'<path d="M-8 46 Q0 44 8 46 Q6 66 0 76 Q-6 66 -8 46Z" fill="{color}" stroke="{I}" stroke-width="1.5"/>')
    if kind == "mustache":
        return f'<path d="M-22 30 Q-12 20 0 25 Q12 20 22 30 Q14 28 0 30 Q-14 28 -22 30Z" fill="{color}" stroke="{I}" stroke-width="1.5"/>'
    if kind == "stubble":
        rnd = random.Random(4)
        return "".join(f'<circle cx="{rnd.uniform(-34, 34):.0f}" cy="{rnd.uniform(26, 52):.0f}" r="1.3" fill="#5A4A44" opacity=".55"/>' for _ in range(40))
    return ""


def _hero_face(c: dict, expr: str, uid: str) -> str:
    I = INK
    expr = {"wink": "sly", "cool": "smug", "panic": "scared", "happy": "laugh", "sleepy": "deadpan"}.get(expr, expr)
    eye, brow, mouth, look = HERO_MAP.get(expr, HERO_MAP["neutral"])
    skin = c["skin"]
    bc = c.get("beard_color", c["hair"])
    out = (f'<ellipse cx="-47" cy="2" rx="9" ry="15" fill="{skin}" stroke="{I}" stroke-width="3"/>'
           f'<ellipse cx="47" cy="2" rx="9" ry="15" fill="{skin}" stroke="{I}" stroke-width="3"/>'
           f'<path d="{HEAD}" fill="{skin}"/><path d="{HEAD}" fill="url(#hs{uid})"/>'
           f'<path d="M-44 -22 Q-46 -2 -42 10 M44 -22 Q46 -2 42 10" stroke="{c["hair"]}" stroke-width="6" fill="none"/>')
    if c.get("lines"):
        out += ('<path d="M-14 -40 Q0 -44 14 -40 M-10 -48 Q0 -51 10 -48" stroke="#9A6440" stroke-width="1.8" fill="none" opacity=".6"/>'
                '<path d="M-18 16 Q-24 26 -20 36 M18 16 Q24 26 20 36" stroke="#9A6440" stroke-width="2" fill="none" opacity=".6"/>')
    out += _eye(-19, eye, look, skin) + _eye(19, eye, look, skin)
    out += (f'<path d="M2 -2 Q9 14 6 19 Q1 23 -6 19" stroke="{I}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            '<path d="M-4 20 Q0 24 6 19" stroke="#9A5A3A" stroke-width="3" fill="none" opacity=".5"/>')
    if c["beard"] == "full":
        out += _beard("full", bc) + _mouth(mouth)
    else:
        out += _mouth(mouth) + _beard(c["beard"], bc)
    if expr == "cry":
        out += '<path d="M-19 2 q-4 18 0 36 M19 2 q4 18 0 36" stroke="#7FD0F2" stroke-width="5" fill="none" stroke-linecap="round"/>'
    if expr == "scared":
        out += '<path d="M42 -40 q9 14 0 21 q-9 -7 0 -21z" fill="#9BDCF5" stroke="#2B6F8F" stroke-width="2"/>'
    if expr in ("angry", "grit"):
        out += '<path d="M28 -50 l8 8 M36 -50 l-8 8 M30 -54 v-6 M34 -38 h6" stroke="#C0392B" stroke-width="3" stroke-linecap="round"/>'
    out += f'<path d="{HEAD}" fill="none" stroke="{I}" stroke-width="{SW}"/>'
    return out


def _hero_brows(c: dict, expr: str) -> str:
    expr = {"wink": "sly", "cool": "smug", "panic": "scared", "happy": "laugh", "sleepy": "deadpan"}.get(expr, expr)
    brow = HERO_MAP.get(expr, HERO_MAP["neutral"])[1]
    return _brows(brow, c.get("beard_color", c["hair"]))


def _extra_face(c: dict, expr: str) -> str:
    I = INK
    skin = c["skin"]
    e = lambda cx, r=4.5: f'<circle cx="{cx}" cy="-2" r="{r}" fill="{I}"/>'
    lid = f'<path d="M-27 -8 h17 M10 -8 h17" stroke="{I}" stroke-width="3.5" stroke-linecap="round"/>'
    f = {
        "deadpan": lid + e(-18) + e(18) + f'<path d="M-9 28 h18" stroke="{I}" stroke-width="3.5" stroke-linecap="round"/>',
        "sleepy": f'<path d="M-27 -2 h17 M10 -2 h17" stroke="{I}" stroke-width="3.5" stroke-linecap="round"/><path d="M-6 28 h12" stroke="{I}" stroke-width="3"/>'
                  '<text x="30" y="-40" font-family="Baloo 2, sans-serif" font-weight="800" font-size="22" fill="#4A6A8A">z</text>',
        "shock": (f'<circle cx="-18" cy="-4" r="11" fill="#fff" stroke="{I}" stroke-width="3"/><circle cx="18" cy="-4" r="11" fill="#fff" stroke="{I}" stroke-width="3"/>'
                  + e(-18, 3.5) + e(18, 3.5) + f'<ellipse cx="0" cy="30" rx="8" ry="11" fill="#4A1414" stroke="{I}" stroke-width="3"/>'),
        "panic": (f'<circle cx="-18" cy="-4" r="10" fill="#fff" stroke="{I}" stroke-width="3"/><circle cx="18" cy="-4" r="10" fill="#fff" stroke="{I}" stroke-width="3"/>'
                  + e(-20, 3) + e(16, 3) + f'<path d="M-14 30 q7 -8 14 0 t14 0" stroke="{I}" stroke-width="3.5" fill="none"/>'
                  '<path d="M38 -36 q8 12 0 18 q-8 -6 0 -18z" fill="#9BDCF5" stroke="#2B6F8F" stroke-width="2"/>'),
        "happy": (f'<path d="M-27 -2 q8.5 -9 17 0 M10 -2 q8.5 -9 17 0" stroke="{I}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
                  f'<path d="M-13 22 q13 16 26 0z" fill="#4A1414" stroke="{I}" stroke-width="3"/>'),
        "angry": (f'<path d="M-30 -18 L-8 -8 M8 -8 L30 -18" stroke="{I}" stroke-width="5" stroke-linecap="round"/>' + e(-17) + e(17)
                  + f'<path d="M-12 32 q12 -12 24 0" stroke="{I}" stroke-width="3.5" fill="none"/>'),
        "cry": (lid + e(-18, 3) + e(18, 3) + f'<path d="M-11 34 q11 -11 22 0" stroke="{I}" stroke-width="3.5" fill="none"/>'
                '<path d="M-18 4 q-4 18 0 30 M18 4 q4 18 0 30" stroke="#7FD0F2" stroke-width="5" fill="none" stroke-linecap="round"/>'),
    }.get(EXTRA_ALIAS.get(expr, expr)) or ""
    return (f'<path d="{HEAD}" fill="{skin}"/><path d="M-30 14 Q-34 30 -24 40" stroke="#C98E66" stroke-width="2.5" fill="none" opacity=".5"/>'
            + f + f'<path d="{HEAD}" fill="none" stroke="{I}" stroke-width="{SW}"/>')


def _kid_face(c: dict, expr: str, brows_only: bool = False) -> str:
    """Tèo: đầu to tròn, tai vểnh, tàn nhang, răng thỏ sứt, mắt ốc nhồi – hài kiểu lém lỉnh."""
    I = INK
    sk = c["skin"]
    def big(cx, look=3, r=15):
        return (f'<ellipse cx="{cx}" cy="-2" rx="{r}" ry="{r + 2}" fill="#fff" stroke="{I}" stroke-width="3"/>'
                f'<circle cx="{cx + look}" cy="1" r="6.5" fill="#2A1A10"/><circle cx="{cx + look + 2.5}" cy="-2" r="2.2" fill="#fff"/>')
    ears = (f'<ellipse cx="-58" cy="4" rx="15" ry="20" fill="{sk}" stroke="{I}" stroke-width="3.5" transform="rotate(-14 -58 4)"/>'
            f'<ellipse cx="58" cy="4" rx="15" ry="20" fill="{sk}" stroke="{I}" stroke-width="3.5" transform="rotate(14 58 4)"/>'
            '<path d="M-60 -4 q-6 8 0 16 M60 -4 q6 8 0 16" stroke="#C98E66" stroke-width="2.5" fill="none"/>')
    bl = []
    brow = lambda a, b: bl.append(f'<path d="M-34 {a} q12 -8 24 -2" stroke="{I}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                         f'<path d="M10 {b - 2} q12 -6 24 2" stroke="{I}" stroke-width="5" fill="none" stroke-linecap="round"/>') or ""
    teeth = '<path d="M-7 27 h14 v9 h-14z M0 27 v9" fill="#fff" stroke="#1C1612" stroke-width="2"/>'
    if expr in ("blank", "deadpan", "neutral", "sleepy", "think"):  # mặt đơ: mắt trố, con ngươi chấm nhỏ, miệng 1 nét
        eyes = (f'<ellipse cx="-21" cy="-2" rx="16" ry="19" fill="#FBF8F0" stroke="#5A3A26" stroke-width="1.8"/>'
                f'<ellipse cx="21" cy="-2" rx="16" ry="19" fill="#FBF8F0" stroke="#5A3A26" stroke-width="1.8"/>'
                f'<circle cx="-21" cy="0" r="2.6" fill="{I}"/><circle cx="21" cy="0" r="2.6" fill="{I}"/>')
        if expr == "sleepy":
            eyes += f'<path d="M-37 -2 h32 M5 -2 h32" stroke="{I}" stroke-width="3.5"/><rect x="-38" y="-22" width="34" height="19" fill="{sk}"/><rect x="4" y="-22" width="34" height="19" fill="{sk}"/>'
        bl.append(f'<path d="M-30 -30 h16 M14 -30 h16" stroke="{I}" stroke-width="3.5" stroke-linecap="round"/>')
        mouth = f'<path d="M-9 32 h18" stroke="{I}" stroke-width="3.5" stroke-linecap="round"/>'
        if expr == "think":
            mouth = f'<circle cx="2" cy="32" r="4" fill="none" stroke="{I}" stroke-width="3"/>'
    elif expr in ("smug", "sly"):
        eyes = big(-21, 5) + big(21, 5) + (f'<path d="M-37 -3 Q-21 -10 -5 -3 L-5 -20 L-37 -20Z M5 -3 Q21 -10 37 -3 L37 -20 L5 -20Z" fill="{sk}"/>'
                                           f'<path d="M-37 -3 Q-21 -10 -5 -3 M5 -3 Q21 -10 37 -3" stroke="{I}" stroke-width="4" fill="none"/>')
        eyes += brow(-24, -30)
        mouth = f'<path d="M-14 26 Q6 32 20 20" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>' + '<path d="M2 28 h9 v7 h-9z" fill="#fff" stroke="#1C1612" stroke-width="2"/>'
    elif expr in ("happy", "laugh"):
        eyes = (f'<path d="M-35 0 q14 -16 28 0 M7 0 q14 -16 28 0" stroke="{I}" stroke-width="5" fill="none" stroke-linecap="round"/>' + brow(-26, -26))
        mouth = (f'<path d="M-24 18 Q0 22 24 18 Q20 50 0 50 Q-20 50 -24 18Z" fill="#5A1414" stroke="{I}" stroke-width="3.5"/>' + teeth.replace("27", "19").replace("v9", "v10")
                 + '<ellipse cx="0" cy="42" rx="9" ry="5" fill="#E0605A"/>')
    elif expr in ("shock", "scared", "panic"):
        eyes = big(-21, 0, 18) + big(21, 0, 18) + brow(-36, -36)
        mouth = f'<ellipse cx="0" cy="34" rx="12" ry="16" fill="#5A1414" stroke="{I}" stroke-width="3.5"/>' + teeth.replace("27", "19")
        if expr != "shock":
            mouth += '<path d="M54 -46 q10 16 0 24 q-10 -8 0 -24z" fill="#9BDCF5" stroke="#2B6F8F" stroke-width="2"/>'
    elif expr in ("sad", "cry"):
        bl.append(f'<path d="M-34 -24 q12 -2 24 -10 M10 -34 q12 8 24 10" stroke="{I}" stroke-width="5" fill="none" stroke-linecap="round"/>')
        eyes = big(-21, 0) + big(21, 0)
        mouth = f'<path d="M-14 36 Q0 24 14 36" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        if expr == "cry":
            mouth += '<path d="M-24 14 q-6 18 -2 34 M24 14 q6 18 2 34" stroke="#7FD0F2" stroke-width="6" fill="none" stroke-linecap="round"/>'
    elif expr in ("angry", "determined", "grit"):
        bl.append(f'<path d="M-36 -30 L-8 -18 M8 -18 L36 -30" stroke="{I}" stroke-width="6" stroke-linecap="round"/>')
        eyes = big(-21, 0, 13) + big(21, 0, 13)
        mouth = f'<path d="M-14 32 H14" stroke="{I}" stroke-width="4.5" stroke-linecap="round"/>'
    else:
        eyes = big(-21, 3) + big(21, 3) + brow(-28, -32)
        mouth = f'<path d="M-12 30 Q0 36 14 28" stroke="{I}" stroke-width="4" fill="none" stroke-linecap="round"/>' + teeth.replace("-7 27", "-5 31").replace("h14", "h10").replace("M0 27", "M0 31").replace("v9", "v7")
    if brows_only:
        return "".join(bl)
    freck = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#B5683E" opacity=".7"/>' for x, y in ((-34, 16), (-28, 20), (-38, 22), (34, 16), (28, 20), (38, 22)))
    return (ears + f'<path d="{HEAD_KID}" fill="{sk}"/>'
            '<ellipse cx="-34" cy="22" rx="11" ry="6" fill="#F08A7A" opacity=".5"/><ellipse cx="34" cy="22" rx="11" ry="6" fill="#F08A7A" opacity=".5"/>'
            + freck + eyes + '<path d="M-3 8 q8 6 0 12" stroke="#9A5A3A" stroke-width="3" fill="none" stroke-linecap="round"/>' + mouth
            + f'<path d="{HEAD_KID}" fill="none" stroke="{I}" stroke-width="{SW}"/>')


def chauchau(x: float = 0, y: float = 0, s: float = 1.0, expr: str = "smug", flip: bool = False) -> str:
    """Tí – chú châu chấu xanh, mắt to, râu dài; ngồi trên vai Tèo hoặc đứng riêng để phản ứng.
    expr: smug | shock | happy | deadpan | scared"""
    I = INK
    G, G2, Y = "#7CC242", "#4E8F2A", "#C9E46A"
    eye = {
        "shock": '<circle cx="46" cy="-34" r="13" fill="#fff" stroke="#1C1612" stroke-width="2.5"/><circle cx="47" cy="-34" r="3.5" fill="#1C1612"/>',
        "happy": '<circle cx="46" cy="-34" r="12" fill="#fff" stroke="#1C1612" stroke-width="2.5"/><path d="M38 -34 q8 -9 16 0" stroke="#1C1612" stroke-width="3.5" fill="none"/>',
        "scared": '<circle cx="46" cy="-34" r="13" fill="#fff" stroke="#1C1612" stroke-width="2.5"/><circle cx="42" cy="-32" r="3" fill="#1C1612"/>'
                  '<path d="M66 -56 q6 10 0 15 q-6 -5 0 -15z" fill="#9BDCF5" stroke="#2B6F8F" stroke-width="1.5"/>',
    }.get(expr, '<circle cx="46" cy="-34" r="12" fill="#fff" stroke="#1C1612" stroke-width="2.5"/><circle cx="50" cy="-33" r="5" fill="#1C1612"/>'
                '<path d="M33 -38 Q46 -44 59 -38 L59 -48 L33 -48Z" fill="#7CC242"/><path d="M33 -38 Q46 -44 59 -38" stroke="#1C1612" stroke-width="3" fill="none"/>')
    mouth = {"shock": '<ellipse cx="60" cy="-14" rx="5" ry="6" fill="#4A1414"/>',
             "happy": '<path d="M52 -16 q8 8 14 -2" stroke="#1C1612" stroke-width="3" fill="none"/>',
             "scared": '<path d="M52 -14 q3 -3 6 0 t6 0" stroke="#1C1612" stroke-width="2.5" fill="none"/>'}.get(
        expr, '<path d="M52 -14 q8 2 13 -5" stroke="#1C1612" stroke-width="3" fill="none" stroke-linecap="round"/>')
    body = (f'<path d="M-62 4 L-20 -30 L-6 -8 L-50 14Z" fill="{G2}" stroke="{I}" stroke-width="3" stroke-linejoin="round"/>'  # chân sau
            f'<path d="M-20 -30 L-30 18 L-40 22" stroke="{I}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
            f'<path d="M-70 -2 Q-30 -30 30 -24 Q44 -8 26 6 Q-30 14 -70 -2Z" fill="{G}" stroke="{I}" stroke-width="3.5"/>'
            f'<path d="M-60 -6 Q-20 -22 20 -18" stroke="{Y}" stroke-width="4" fill="none"/>'
            f'<path d="M-50 -14 Q-10 -40 22 -26 Q-10 -20 -50 -8Z" fill="{G2}" stroke="{I}" stroke-width="2.5" opacity=".9"/>'  # cánh
            + "".join(f'<path d="M{x} 6 l-6 18 l-6 2" stroke="{I}" stroke-width="3" fill="none" stroke-linecap="round"/>' for x in (4, 20))
            + f'<ellipse cx="44" cy="-24" rx="26" ry="22" fill="{G}" stroke="{I}" stroke-width="3.5"/>'
            f'<path d="M40 -44 Q30 -90 -10 -104 M50 -44 Q56 -96 30 -118" stroke="{I}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            + eye + mouth)
    sx = -s if flip else s
    return f'<g transform="translate({x:.0f} {y:.0f}) scale({sx:.2f} {s:.2f})">{body}</g>'


# ------------------------------------------------------------------ mũ (toạ độ đầu, tâm 0,0, đỉnh đầu y≈-62)
def _hat(kind: str, c: dict) -> str:
    I = INK
    trim = c["trim"]
    hats = {
        "khan": (f'<path d="M-50 -18 C-56 -70 -26 -86 0 -86 C26 -86 56 -70 50 -18 Q0 -32 -50 -18Z" fill="#221C18" stroke="{I}" stroke-width="{SW}"/>'
                 '<path d="M-48 -30 Q0 -46 48 -30 M-44 -48 Q0 -62 44 -48 M-34 -66 Q0 -76 34 -66" stroke="#4A403A" stroke-width="3" fill="none"/>'),
        "scholar": (f'<path d="M-44 -26 L-40 -92 L40 -92 L44 -26 Q0 -36 -44 -26Z" fill="#1E1A17" stroke="{I}" stroke-width="{SW}"/>'
                    '<path d="M-40 -60 H40" stroke="#3A332E" stroke-width="3"/>'
                    f'<path d="M-30 -92 L-20 -108 L20 -108 L30 -92Z" fill="#2A2420" stroke="{I}" stroke-width="3"/>'),
        "band": (f'<path d="M-50 -24 Q0 -40 50 -24 L50 -10 Q0 -26 -50 -10Z" fill="{trim}" stroke="{I}" stroke-width="3"/>'
                 f'<path d="M-46 -50 C-40 -76 40 -76 46 -50 Q48 -36 46 -24 Q0 -40 -46 -24 Q-48 -36 -46 -50Z" fill="{c["hair"]}" stroke="{I}" stroke-width="3"/>'
                 f'<path d="M48 -18 q22 6 30 30 M48 -16 q14 14 14 38" stroke="{trim}" stroke-width="7" fill="none" stroke-linecap="round"/>'),
        "wrap": (f'<path d="M-50 -16 C-54 -64 -26 -80 0 -80 C26 -80 54 -64 50 -16 Q0 -30 -50 -16Z" fill="#7A5A3A" stroke="{I}" stroke-width="{SW}"/>'
                 '<path d="M-48 -28 Q0 -44 48 -28 M-40 -50 Q0 -64 40 -50" stroke="#5A3E26" stroke-width="3" fill="none"/>'),
        "non": (f'<path d="M-92 -22 L0 -112 L92 -22 Q0 -8 -92 -22Z" fill="#E6C98A" stroke="{I}" stroke-width="{SW}" stroke-linejoin="round"/>'
                '<path d="M-60 -40 L0 -102 M60 -40 L0 -102 M-28 -26 L0 -104 M28 -26 L0 -104" stroke="#B89A5A" stroke-width="2.5"/>'),
        "dv_helm": (f'<path d="M-52 -14 C-56 -84 56 -84 52 -14 Q0 -26 -52 -14Z" fill="#6A6E66" stroke="{I}" stroke-width="{SW}"/>'
                    f'<path d="M-54 -16 Q0 -30 54 -16 L56 -4 Q0 -18 -56 -4Z" fill="{trim}" stroke="{I}" stroke-width="2.5"/>'
                    f'<path d="M-4 -78 L0 -106 L4 -78Z" fill="{trim}" stroke="{I}" stroke-width="2"/><path d="M0 -104 q-16 -20 -4 -30 q4 14 10 20z" fill="#C0392B" stroke="{I}" stroke-width="2"/>'),
        "minh_helm": (f'<path d="M-58 -6 Q-64 18 -52 40 L-40 40 L-44 -6Z M58 -6 Q64 18 52 40 L40 40 L44 -6Z" fill="#8F99A0" stroke="{I}" stroke-width="3"/>'
                      f'<path d="M-52 -12 C-56 -90 56 -90 52 -12 Q0 -26 -52 -12Z" fill="#A9B2B8" stroke="{I}" stroke-width="{SW}"/>'
                      '<path d="M-20 -72 Q-30 -40 -34 -16" stroke="#fff" stroke-width="5" opacity=".45" fill="none" stroke-linecap="round"/>'
                      f'<path d="M-58 -14 Q0 -30 58 -14" stroke="{trim}" stroke-width="8" fill="none"/>'
                      f'<path d="M-3 -82 L0 -134 L3 -82Z" fill="#C9D0D4" stroke="{I}" stroke-width="2"/>'
                      f'<path d="M0 -98 C-16 -96 -24 -86 -26 -72 Q-18 -80 -12 -78 Q-14 -72 -12 -66 Q-4 -76 0 -76 Q4 -76 12 -66 Q14 -72 12 -78 Q18 -80 26 -72 C24 -86 16 -96 0 -98Z" fill="#C8302A" stroke="{I}" stroke-width="2"/>'
                      '<circle cx="0" cy="-100" r="6" fill="#E0B43A" stroke="#1C1612" stroke-width="2"/>'),
        "minh_cap": (f'<path d="M-62 -20 Q0 -40 62 -20 Q60 -8 50 -8 Q0 -24 -50 -8 Q-60 -8 -62 -20Z" fill="#8A2A22" stroke="{I}" stroke-width="3"/>'
                     f'<path d="M-44 -24 C-44 -74 44 -74 44 -24 Q0 -36 -44 -24Z" fill="#C0392B" stroke="{I}" stroke-width="{SW}"/>'
                     f'<circle cx="0" cy="-70" r="7" fill="#E0B43A" stroke="{I}" stroke-width="2"/>'),
        "wusha": (f'<path d="M-44 -24 L-42 -78 Q0 -94 42 -78 L44 -24 Q0 -36 -44 -24Z" fill="#14110F" stroke="{I}" stroke-width="{SW}"/>'
                  f'<path d="M-30 -78 Q0 -112 30 -78" fill="#14110F" stroke="{I}" stroke-width="3"/>'
                  f'<path d="M-44 -50 L-110 -60 Q-118 -52 -110 -44 L-44 -40Z M44 -50 L110 -60 Q118 -52 110 -44 L44 -40Z" fill="#14110F" stroke="{I}" stroke-width="2.5"/>'
                  f'<path d="M-42 -32 Q0 -42 42 -32" stroke="#3A332E" stroke-width="3" fill="none"/>'),
        "ti_hair": (f'<path d="M-54 -2 C-60 -58 -30 -72 0 -72 C30 -72 60 -58 54 -2 L48 -2 L46 -18 Q0 -30 -46 -18 L-48 -2Z" fill="{c["hair"]}" stroke="{I}" stroke-width="3.5"/>'
                    f'<path d="M-40 -20 l8 -10 l6 10 l8 -10 l6 10 l8 -10 l6 10 l8 -10 l6 10 l8 -10 l6 10" stroke="{c["hair"]}" stroke-width="6" fill="none"/>'
                    f'<path d="M-2 -70 q-4 -22 12 -24 q12 2 6 14 q-6 6 -10 0" stroke="{c["hair"]}" stroke-width="6" fill="none" stroke-linecap="round"/>'
                    '<path d="M-26 -58 Q-10 -66 8 -64" stroke="#5A4A40" stroke-width="3" fill="none" opacity=".7"/>'),
    }
    out = hats.get(kind, "")
    if kind == "minh_helm_gold":
        out = hats["minh_helm"].replace("#A9B2B8", "#D9AE48").replace("#8F99A0", "#B88A30")
    return out


def _item(kind: str, c: dict) -> str:
    I = INK
    return {
        "spear": f'<path d="M70 0 L84 -380" stroke="#5A3A22" stroke-width="7"/><path d="M84 -380 l-9 -34 l20 6z" fill="#C9D0D4" stroke="{I}" stroke-width="2"/>'
                 f'<path d="M80 -350 q-12 10 -6 26 q8 -8 12 -24z" fill="#C0392B"/>',
        "sword": f'<path d="M44 -96 L88 -4" stroke="#C9D0D4" stroke-width="9" stroke-linecap="round"/><path d="M38 -108 L58 -84" stroke="{I}" stroke-width="10" stroke-linecap="round"/>'
                 f'<path d="M30 -96 L60 -116" stroke="{c["trim"]}" stroke-width="7" stroke-linecap="round"/>',
        "flag": (f'<path d="M-74 0 L-74 -420" stroke="#5A3A22" stroke-width="8"/>'
                 f'<path d="M-74 -420 q-80 -14 -150 10 q60 26 0 52 q76 -22 150 -6z" fill="{"#E9A92B" if c["side"] != "minh" else "#C0392B"}" stroke="{I}" stroke-width="3"/>'),
        "scroll": f'<rect x="-30" y="-120" width="80" height="54" rx="6" fill="#F3E3BC" stroke="{I}" stroke-width="3"/><path d="M-20 -104 h58 M-20 -92 h48 M-20 -80 h54" stroke="#8A6A3A" stroke-width="2"/>',
        "fan": f'<path d="M30 -100 L80 -160 A70 70 0 0 1 108 -100 Z" fill="#F3EBDA" stroke="{I}" stroke-width="3"/><path d="M30 -100 L92 -150 M30 -100 L104 -124" stroke="#8A6A3A" stroke-width="2"/>',
        "bow": f'<path d="M-70 -230 Q-118 -120 -70 -10" stroke="#6B4226" stroke-width="7" fill="none"/><path d="M-70 -230 L-70 -10" stroke="#ddd" stroke-width="2"/>',
        "torch": f'<path d="M60 -10 L76 -200" stroke="#5A3A22" stroke-width="8"/><path d="M76 -200 q-30 -30 0 -80 q30 50 0 80z" fill="#F39C12" stroke="#C0392B" stroke-width="3"/>',
        "hoe": f'<path d="M66 0 L80 -320" stroke="#7A5A3A" stroke-width="7"/><path d="M80 -320 l40 10 l-6 18 l-36 -10z" fill="#8F99A0" stroke="{I}" stroke-width="2"/>',
    }.get(kind, "")


# ------------------------------------------------------------------ API
_uid_counter = [0]


def peg(who: str = "leloi", x: float = 960, y: float = 900, s: float = 1.0, expr: str = "", flip: bool = False,
        item: str = "", label: str | bool = False, lean: float = 0, head_tilt: float = 0, pet_expr: str = "",
        paint: bool | None = None) -> str:
    """Một nhân vật trong CAST. who="teo" tự có châu chấu Tí trên vai (pet_expr để chỉnh biểu cảm của Tí). label=True → ghi tên dưới chân; label="..." → ghi chữ tuỳ ý."""
    who = {"ti": "teo"}.get(who, who)  # tập cũ gọi "ti" → nay là Tèo (Tí là châu chấu)
    c = CAST[who]
    _uid_counter[0] += 1
    uid = f"{who}{_uid_counter[0]}"
    expr = expr or {"hero": "neutral", "kid": "blank"}.get(c["face"], "deadpan")
    if paint is None:
        paint = who == "teo"  # Tèo vẽ chất sơn dầu cho hợp nền tranh
    face = {"hero": lambda: _hero_face(c, expr, uid), "extra": lambda: _extra_face(c, expr),
            "kid": lambda: _kid_face(c, expr)}[c["face"]]()
    back_items = item in ("spear", "flag", "bow", "hoe", "torch")
    it = _item(item, c)
    brows = _hero_brows(c, expr) if c["face"] == "hero" else ""
    hs = 1.18 if c["face"] == "kid" else 1.0
    head = (f'<g transform="translate(0 {HEAD_Y - (14 if hs > 1 else 0)}) rotate({head_tilt}) scale({hs})">{face}'
            f'<g transform="translate(0 {-12 if c["face"] != "kid" else -6})">{_hat(c["hat"], c)}</g>{brows}'
            + (_kid_face(c, expr, brows_only=True) if c["face"] == "kid" else "") + '</g>')
    if who == "teo":  # châu chấu Tí trên vai trái Tèo (bên phải khung hình)
        head += chauchau(-86 if flip else 86, -178, 0.56, flip=flip, expr=pet_expr or {"shock": "shock", "scared": "scared", "laugh": "happy", "happy": "happy"}.get(expr, "smug"))
    body = (it if back_items else "") + _body(c, uid) + head + ("" if back_items else it)
    sx = -s if flip else s
    g = _defs(uid) + (f'<g filter="url(#oilp)">' if paint else "<g>") + f'<g transform="translate({x:.0f} {y:.0f}) rotate({lean}) scale({sx:.3f} {s:.3f})">{body}</g></g>'
    if label:
        text = c["name"] if label is True else str(label)
        fs = 30
        wdt = len(text) * fs * 0.58 + 30
        col = {"dv": "#C98B2E", "minh": "#B23A30", "host": "#2F6F8F"}.get(c["side"], "#555")
        g += (f'<g transform="translate({x:.0f} {y + 22 * s + 26:.0f})"><rect x="{-wdt / 2:.0f}" y="-24" width="{wdt:.0f}" height="44" rx="10" fill="#FFF7E2" stroke="{INK}" stroke-width="3"/>'
              f'<rect x="{-wdt / 2:.0f}" y="-24" width="12" height="44" rx="4" fill="{col}"/>'
              f'<text x="6" y="9" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="{fs}" fill="{INK}">{text}</text></g>')
    return g


def crowd(who: str = "minh_soldier", x: float = 960, y: float = 880, n: int = 6, s: float = 0.6, gap: float = 95,
          rows: int = 1, flip: bool = False, item: str = "spear", seed: int = 1, exprs: list | None = None, expr: str = "deadpan") -> str:
    """Đám đông (hàng sau nhỏ & mờ hơn một chút)."""
    rnd = random.Random(seed)
    out = ""
    for r in range(rows - 1, -1, -1):
        k = 1 - r * 0.14
        row = ""
        for i in range(n):
            px = x + (i - (n - 1) / 2) * gap * k + (r % 2) * gap * 0.5 + rnd.uniform(-10, 10)
            py = y - r * 60 + rnd.uniform(-6, 6)
            e = rnd.choice(exprs) if exprs else expr
            row += peg(who, px, py, s * k, e, flip, item, lean=rnd.uniform(-3, 3))
        out += f'<g opacity="{1 - r * 0.08:.2f}">{row}</g>'
    return out


def cast_sheet(out_png: str):
    """Bảng nhân vật: mỗi người 1 ô + vài biểu cảm của hero."""
    import subprocess
    import tempfile
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    keys = list(CAST)
    cols = 5
    cw, ch = 380, 520
    rows = (len(keys) + cols - 1) // cols
    W, H = cols * cw, rows * ch + 120
    body = f'<rect width="{W}" height="{H}" fill="#F3E9D2"/>'
    body += (f'<text x="{W / 2}" y="78" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="56" fill="{INK}">'
             'TÍ XUYÊN SỬ – TÈO &amp; CHÂU CHẤU TÍ + DÀN NHÂN VẬT LAM SƠN</text>')
    demo = {"leloi": ("determined", "sword"), "nguyentrai": ("smug", "fan"), "lelai": ("determined", "spear"), "tranluu": ("grit", "sword"),
            "dv_soldier": ("deadpan", "spear"), "peasant": ("sleepy", "hoe"), "scholar": ("deadpan", "scroll"), "lieuthang": ("smug", "sword"),
            "mocthanh": ("scared", ""), "vuongthong": ("angry", ""), "luongminh": ("shock", "scroll"), "hoangphuc": ("sly", ""),
            "thoitu": ("grit", "spear"), "minh_soldier": ("shock", "spear"), "teo": ("blank", "")}
    for i, k in enumerate(keys):
        cx, cy = (i % cols) * cw + cw / 2, 120 + (i // cols) * ch
        bg = {"dv": "#E9D3A8", "minh": "#EBC3B8", "host": "#C9DFE6"}[CAST[k]["side"]]
        body += (f'<defs><clipPath id="sc{i}"><rect x="{cx - cw / 2 + 10}" y="{cy + 10}" width="{cw - 20}" height="{ch - 20}" rx="22"/></clipPath></defs>'
                 f'<rect x="{cx - cw / 2 + 10}" y="{cy + 10}" width="{cw - 20}" height="{ch - 20}" rx="22" fill="{bg}" stroke="{INK}" stroke-width="3"/>')
        e, it = demo.get(k, ("neutral", ""))
        body += f'<g clip-path="url(#sc{i})">' + peg(k, cx - 10, cy + ch - 110, 1.2, e, item=it, label=True) + '</g>'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
    from studio.rasterize import svgs_to_png
    svgs_to_png([(svg, Path(out_png), W, H)])
    return out_png


def expr_sheet(out_png: str, who: str = "lieuthang"):
    import subprocess
    import tempfile
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    ex = HERO_EXPR if CAST[who]["face"] == "hero" else (("blank", "think", "sleepy", "smug", "shock", "scared", "happy", "angry", "sad", "cry")
                                                          if CAST[who]["face"] == "kid" else EXTRA_EXPR)
    cw, W, H = 300, 300 * 6, 2 * 310 + 30
    body = f'<rect width="{W}" height="{H}" fill="#F3E9D2"/>'
    for i, e in enumerate(ex):
        cx, cy = (i % 6) * cw + cw / 2, (i // 6) * 310 + 14
        body += (f'<defs><clipPath id="xc{i}"><rect x="{cx - cw / 2 + 6}" y="{cy}" width="{cw - 12}" height="262" rx="18"/></clipPath></defs>'
                 f'<rect x="{cx - cw / 2 + 6}" y="{cy}" width="{cw - 12}" height="262" rx="18" fill="#E9D3A8"/>'
                 f'<g clip-path="url(#xc{i})">' + peg(who, cx, cy + 130 + 1.3 * 232 + 40, 1.3, e) + '</g>')
        body += f'<text x="{cx}" y="{cy + 290}" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="28" fill="{INK}">{e}</text>'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
    from studio.rasterize import svgs_to_png
    svgs_to_png([(svg, Path(out_png), W, H)])
    return out_png


if __name__ == "__main__":
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    print(cast_sheet(str(root / "channel" / "cast_sheet.png")))
    print(expr_sheet(str(root / "channel" / "cast_expressions.png"), sys.argv[1] if len(sys.argv) > 1 else "lieuthang"))


def fallen_helmet(x: float = 960, y: float = 900, s: float = 1.0, rot: float = 28, who: str = "lieuthang") -> str:
    """Mũ trụ rơi trên đất (thay cho cảnh tử trận – không máu, không đùa)."""
    c = CAST[who]
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"><ellipse cx="0" cy="6" rx="90" ry="14" fill="#000" opacity=".3"/>'
            f'<g transform="rotate({rot}) translate(0 40)">{_hat(c["hat"], c)}</g></g>')


def fallen_flag(x: float = 960, y: float = 900, s: float = 1.0, color: str = "#C0392B", flip: bool = False) -> str:
    sx = -s if flip else s
    return (f'<g transform="translate({x:.0f} {y:.0f}) scale({sx:.2f} {s:.2f})">'
            f'<ellipse cx="60" cy="8" rx="200" ry="14" fill="#000" opacity=".25"/>'
            f'<path d="M-140 0 L260 -40" stroke="#5A3A22" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M150 -30 Q190 10 250 -8 Q230 30 160 30 Q120 20 150 -30Z" fill="{color}" stroke="{INK}" stroke-width="3" opacity=".95"/></g>')


def closeup(who: str = "lieuthang", expr: str = "smug", x: float = 620, s: float = 3.1, flip: bool = False, item: str = "") -> str:
    """Cận cảnh nửa người: mặt rộng ~ 300*s/3 px, thân tràn khỏi đáy khung."""
    return peg(who, x, 450 + 232 * s, s, expr, flip, item)


def medallion(who: str = "lieuthang", x: float = 960, y: float = 300, r: float = 130, expr: str = "neutral", name: str = "",
              gray: bool = True) -> str:
    """Chân dung tròn (mặt nhân vật CAST) – bản xám, viền xám dùng cho khoảnh khắc tử trận (trang nghiêm)."""
    k = r / 95
    ring = "#8A8A8A" if gray else "#E0B43A"
    filt = ('<filter id="gry"><feColorMatrix type="saturate" values="0.15"/></filter>' if gray else "")
    body = peg(who, 0, 232 + 20, 1, expr)
    out = (f'<defs>{filt}<clipPath id="md{who}"><circle cx="0" cy="0" r="{r / k:.0f}"/></clipPath></defs>'
           f'<g transform="translate({x:.0f} {y:.0f}) scale({k:.3f})">'
           f'<circle r="{r / k + 8:.0f}" fill="{ring}" stroke="{INK}" stroke-width="5"/><circle r="{r / k:.0f}" fill="#D8D2C6"/>'
           f'<g clip-path="url(#md{who})"{" filter=&quot;url(#gry)&quot;".replace("&quot;", chr(34)) if gray else ""}>{body}</g></g>')
    if name:
        w = len(name) * 17 + 40
        out += (f'<rect x="{x - w / 2:.0f}" y="{y + r + 14:.0f}" width="{w:.0f}" height="46" rx="10" fill="#2A2A2A" stroke="{INK}" stroke-width="3"/>'
                f'<text x="{x:.0f}" y="{y + r + 47:.0f}" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="30" fill="#EEE">{name}</text>')
    return out
