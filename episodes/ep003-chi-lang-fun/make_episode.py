"""Tập thử phong cách "fun" (hình nhộng + ảnh thật + hiệu ứng + meme) – Liễu Thăng và cú lừa ở ải Chi Lăng.
Chạy: python episodes/ep003-chi-lang-fun/make_episode.py"""
import json
from pathlib import Path

DV, MINH = "#E9A92B", "#C4453C"
AS = "episodes/ep003-chi-lang-fun/assets/"


def L(name, elements, motion="none", appear=None, **kw):
    d = {"name": name, "motion": motion, "elements": elements}
    if appear is not None:
        d["appear"] = appear
    d.update(kw)
    return d


def E(fn, **args):
    return {"fn": fn, "args": args}


def N(text, say=None, rate=None):
    d = {"text": text}
    if say:
        d["say"] = say
    if rate:
        d["rate"] = rate
    return d


TI = lambda expr="happy", pose="point", x=1790, y=1000, s=0.42: E("ti", x=x, y=y, s=s, pose=pose, expr=expr, flip=True)

scenes = [
    dict(key="open", bg_motion="still",
         narration=[N("Năm *1427*, nghĩa quân Lam Sơn của *Lê Lợi* đang vây chặt quân Minh trong thành Đông Quan, tức Hà Nội bây giờ.",
                      "Năm một nghìn bốn trăm hai mươi bảy, nghĩa quân Lam Sơn của Lê Lợi đang vây chặt quân Minh trong thành Đông Quan, tức Hà Nội bây giờ."),
                    N("Nhà Minh nhìn xuống và nghĩ: gửi *mười lăm vạn quân* sang, xử đẹp trong một nốt nhạc!")],
         layers=[L("bg", [E("map_base", view="asia", vn=DV, cn=MINH, river=False, cn_label="NHÀ MINH")]),
                 L("faces", [E("nation", which="VN", view="asia", expr="angry", eyes_at=[19.6, 104.0], size=0.55, shape=False),
                             E("map_label", place="Đông Quan", view="asia", kind="fort", text="Đông Quan", dx=-150, dy=40, size=26)]),
                 L("arrow", [E("map_arrow", pts=[[27.5, 109.5], [24.0, 108.2], "Chi Lăng"], view="asia", width=24, label="15 vạn viện binh", label_dy=-46),
                             E("map_label", place="Chi Lăng", view="asia", kind="battle", text="Chi Lăng", dx=120, dy=0, size=26)], appear=1, appear_delay=1.0, fade_in=0.2),
                 L("smug", [E("nation", which="CN", view="asia", expr="smug", eyes_at=[31, 104], size=1.3, shape=False),
                            E("emoji", ch="😎", x=1000, y=300, size=110),
                            E("bubble", x=1350, y=330, text="15 vạn quân,|xử đẹp!", tx=1110, ty=360, kind="shout", size=46)], appear=1, fade_in=0.12),
                 L("vn", [E("bubble", x=560, y=640, text="Ờ… thử xem.", tx=740, ty=560, size=34)], appear=1, appear_delay=3.2, fade_in=0.15)],
         sfx=[{"type": "chime", "at": 0.1, "gain": 0.2}]),
    dict(key="march", bg_motion="left",
         narration=[N("Tướng *Liễu Thăng* dẫn mười vạn quân, ầm ầm tiến qua *ải Chi Lăng*, Lạng Sơn."),
                    N("Ông khinh địch ra mặt, coi nghĩa quân như… không có.")],
         layers=[L("bg", [E("photo", file=AS + "bg2.jpg", crop=[0, 0.05, 1, 0.80]), E("mist_band", y=760, h=320, op=0.85), E("fg_grass", y=960)]),
                 L("army", [E("mob", x=1350, y=930, n=7, outfit="minh_soldier", expr="deadpan", s=0.62, gap=100, rows=2, item="spear", seed=2)], motion="drift_left"),
                 L("lt", [E("doodle_horse", x=620, y=880, s=1.3, rider="lieuthang", expr="smug"),
                          E("caption_box", text="Liễu Thăng · tự tin 200%", x=60, y=60)], motion="bob"),
                 L("cool", [E("emoji", ch="😏", x=830, y=470, size=90), E("bubble", x=1080, y=300, text="Nghĩa quân?|Chưa nghe bao giờ.", tx=760, ty=470, size=32)], appear=1, fade_in=0.15),
                 L("react", [TI("surprised", "think", x=1800, y=640, s=0.36), E("bubble", x=1640, y=330, text="Ông ơi…|cẩn thận cái miệng.", tx=1760, ty=420, size=26)], appear=1, appear_delay=2.0, fade_in=0.12, motion="bob")]),
    dict(key="terrain", bg_motion="push_down",
         narration=[N("Có điều, Chi Lăng là một thung lũng hẹp, hai bên *núi đá dựng đứng*."),
                    N("Lòng thung lũng thì *lầy lội*, quân đông đến mấy cũng phải đi thành hàng dài.")],
         layers=[L("bg", [E("photo", file=AS + "bg3.jpg", crop=[0, 0, 1, 0.58]), E("fg_grass", y=930, color="#2A4528")]),
                 L("c1", [E("callout", text="Núi đá", x=300, y=200, tx=520, ty=380, size=48),
                          E("callout", text="Núi đá", x=1600, y=200, tx=1380, ty=330, size=48)], appear=0, fade_in=0.15),
                 L("c2", [E("callout", text="Lối đi hẹp, lầy", x=520, y=560, tx=820, ty=780, size=46), E("emoji", ch="🫠", x=1000, y=640, size=90)], appear=1, fade_in=0.15),
                 L("queue", [E("mob", x=980, y=900, n=12, outfit="minh_soldier", expr="deadpan", s=0.42, gap=62, item="spear", seed=21),
                             E("caption_box", text="Kẹt xe thế kỷ 15", x=1180, y=720, size=32)], appear=1, appear_delay=1.0, motion="drift_left"),
                 L("ti", [TI("worried", "think"), E("bubble", x=1560, y=640, text="Đi đông mà|vào đây là… toang.", tx=1740, ty=760, size=30)], appear=1, appear_delay=2.0, motion="bob")]),
    dict(key="lure", bg_motion="right",
         narration=[N("Tướng *Trần Lựu* của nghĩa quân ra đánh vài hiệp, rồi… *quay đầu bỏ chạy*."),
                    N("Diễn hơi lố, nhưng Liễu Thăng *tin sái cổ*, hăm hở đuổi theo vào sâu trong ải.")],
         layers=[L("bg", [E("photo", file=AS + "bg6.jpg", crop=[0.08, 0, 1, 0.60]), E("mist_band", y=640, h=300, op=0.55), E("fg_grass", y=900, color="#3A5A2C", h=200)]),
                 L("tl", [E("dude", x=1350, y=880, s=1.25, outfit="tranluu", expr="wink", flip=True, item="sword"),
                          E("mob", x=1650, y=930, n=3, outfit="dv_soldier", expr="wink", s=0.6, gap=110, flip=True, item="spear", seed=5),
                          E("bubble", x=1400, y=380, text="Ối thua rồi!|(diễn đó)", tx=1360, ty=640, size=34)], motion="drift_right"),
                 L("chase", [E("speed_lines", cx=960, cy=540, n=50, inner=420, op=0.55),
                             E("doodle_horse", x=520, y=880, s=1.3, rider="lieuthang", expr="angry"),
                             E("bubble", x=460, y=330, text="ĐUỔI!!!", tx=520, ty=560, kind="shout", size=56)], appear=1, fade_in=0.12, motion="drift_right"),
                 L("rate", [E("caption_box", text="Diễn xuất: 3/10 · Độ tin: 10/10", x=60, y=60, size=32)], appear=1, appear_delay=1.2, fade_in=0.1)],
         sfx=[{"type": "whoosh", "at": 3.4, "gain": 0.3}]),
    dict(key="mayen", bg_motion="push_up",
         narration=[N("Đến *núi Mã Yên*, ông dẫn hơn trăm kỵ binh phóng lên trước."), N("Và rồi…")],
         layers=[L("bg", [E("photo", file=AS + "bg2.jpg", crop=[0.1, 0.1, 0.9, 0.75], tint="#1D2433", tint_op=0.35), E("fg_grass", y=960, color="#22361F")]),
                 L("cav", [E("doodle_horse", x=760, y=890, s=1.15, rider="lieuthang", expr="smug"),
                           E("doodle_horse", x=1100, y=900, s=0.9, rider="minh_soldier", expr="deadpan"),
                           E("doodle_horse", x=1360, y=905, s=0.85, rider="minh_soldier", expr="deadpan")], motion="drift_left"),
                 L("tag", [E("caption_box", text="Núi Mã Yên", x=60, y=60), E("sign", text="Mã Yên →", x=380, y=900)]),
                 L("brag", [E("bubble", x=760, y=420, text="Ta đi trước,|các ngươi theo sau!", tx=760, ty=620, size=32)], appear=0, appear_delay=1.0, fade_in=0.15),
                 L("ti", [TI("worried", "think"), E("bubble", x=1580, y=560, text="Linh cảm|không lành…", tx=1740, ty=760, kind="think", size=30)], appear=1, motion="bob")]),
    dict(key="ambush", bg_motion="still",
         narration=[N("*Trống trận nổi lên!* Phục binh từ hai bên sườn núi ào ra!", "Trống trận nổi lên! Phục binh từ hai bên sườn núi ào ra!"),
                    N("*Liễu Thăng tử trận* ngay tại chỗ.")],
         layers=[L("bg", [E("photo", file=AS + "bg3.jpg", crop=[0, 0, 1, 0.58], tint="#101828", tint_op=0.35), E("fg_grass", y=990, color="#1F331E")]),
                 L("lines", [E("speed_lines", cx=960, cy=560, n=70, inner=380, op=0.7)], motion="shake"),
                 L("amb_l", [E("mob", x=380, y=560, n=4, outfit="dv_soldier", expr="angry", s=0.62, gap=95, item="bow", seed=3)], appear_t=0.25, fade_in=0.1, motion="from_left"),
                 L("amb_r", [E("mob", x=1540, y=560, n=4, outfit="dv_soldier", expr="angry", s=0.62, gap=95, flip=True, item="spear", seed=4)], appear_t=0.35, fade_in=0.1, motion="from_right"),
                 L("arrows", [E("arrow_volley", x0=380, y0=470, x1=900, y1=820, n=16, seed=7), E("arrow_volley", x0=1540, y0=470, x1=1020, y1=820, n=16, seed=8)], appear_t=0.9, fade_in=0.1),
                 L("lt", [E("doodle_horse", x=960, y=900, s=1.2, rider="lieuthang", expr="shock")], motion="shake"),
                 L("boom", [E("boom", text="TÙNG TÙNG!", x=960, y=250, size=150), E("emoji", ch="😱", x=1180, y=600, size=110)], appear_t=0.05, fade_in=0.05, hold=1.8),
                 L("flash", [E("flash", color="#FFFFFF", op=0.9)], appear_t=0.02, fade_in=0.03, hold=0.15),
                 L("rip", [E("portrait", x=960, y=420, r=130, who="lieuthang", name="Liễu Thăng", mark="x", expr="shock")], appear=1, fade_in=0.2)],
         sfx=[{"type": "crash", "at": 0.05, "gain": 0.4}, {"type": "whoosh", "at": 0.9, "gain": 0.3}]),
    dict(key="chaos", bg_motion="left",
         narration=[N("Mất chủ tướng, mười vạn quân Minh *rối như canh hẹ*."), N("Mà đây… mới chỉ là *màn khởi động*.")],
         layers=[L("bg", [E("photo", file=AS + "bg6.jpg", crop=[0.08, 0, 1, 0.60], tint="#3A2A2A", tint_op=0.2), E("mist_band", y=640, h=300, op=0.55), E("fg_grass", y=900, color="#3A5A2C", h=200)]),
                 L("m1", [E("mob", x=640, y=930, n=5, outfit="minh_soldier", s=0.62, gap=95, rows=2, item="spear", seed=11, exprs=["panic", "shock", "cry"])], motion="shake"),
                 L("m2", [E("mob", x=1350, y=930, n=5, outfit="minh_soldier", s=0.62, gap=95, rows=2, flip=True, item="flag", seed=12, exprs=["panic", "shock", "cry"])], motion="shake"),
                 L("fx", [E("emoji", ch="❓", x=640, y=520, size=90), E("emoji", ch="😵", x=1350, y=520, size=90), E("emoji", ch="💨", x=1000, y=640, size=80)], appear=0, appear_delay=0.8, fade_in=0.15),
                 L("cap", [E("caption_box", text="Tình hình: hơi bị toang", x=60, y=60)], appear=0, appear_delay=1.2, fade_in=0.1),
                 L("ti", [TI("excited", "point"), E("bubble", x=1560, y=640, text="Còn căng|hơn nữa!", tx=1740, ty=760, size=32)], appear=1, motion="bob")]),
    dict(key="outro", bg_motion="still",
         narration=[N("Đạo quân Minh mất tướng vẫn còn rất đông. Theo bạn, nghĩa quân sẽ làm gì tiếp theo? Bình luận dự đoán nhé!"),
                    N("Và nhớ *đăng ký kênh* để xem phần sau!")],
         layers=[L("bg", [E("map_base", view="asia", vn=DV, cn=MINH, river=False, cn_label="NHÀ MINH")]),
                 L("faces", [E("nation", which="CN", view="asia", expr="cry", eyes_at=[31, 104], size=1.3, shape=False),
                             E("nation", which="VN", view="asia", expr="cool", eyes_at=[19.6, 104.0], size=0.55, shape=False)]),
                 L("ti", [E("ti", x=300, y=1000, s=0.8, pose="wave", expr="excited", glow=True)], motion="bob")],
         sfx=[{"type": "chime", "at": 0.1, "gain": 0.2}]),
]
for i, sc in enumerate(scenes):
    sc["id"] = i + 1

ep = {
    "id": "ep003-chi-lang-fun",
    "series": "Tí Xuyên Sử",
    "title_working": "Liễu Thăng và cú lừa ở ải Chi Lăng (phong cách fun – bản thử)",
    "format": "long",
    "voice": {"engine": "edge", "edge_voice": "vi-VN-NamMinhNeural", "edge_rate": "+5%", "edge_pitch": "-4Hz", "sentence_gap": 0.32, "scene_tail": 0.45},
    "music": {"file": "", "volume": 0.14, "generate": True, "mood": "adventure"},
    "fact_check": [
        "1427: nghĩa quân Lam Sơn vây quân Minh (Vương Thông) trong thành Đông Quan.",
        "Viện binh Minh khoảng 15 vạn (Liễu Thăng 10 vạn theo sử Việt, Mộc Thạnh 5 vạn).",
        "Liễu Thăng kiêu ngạo, khinh địch (Toàn thư).",
        "Trần Lựu giả thua nhử Liễu Thăng vào ải Chi Lăng.",
        "Liễu Thăng dẫn hơn 100 kỵ binh đi trước, tử trận ở núi Mã Yên (≈10/10/1427).",
    ],
    "scenes": scenes,
    "thumbnail": {"elements": [
        E("photo", file=AS + "bg3.jpg", crop=[0, 0, 1, 0.55], tint="#101828", tint_op=0.3), E("fg_grass", y=930, color="#1F331E", h=200),
        E("speed_lines", cx=1400, cy=560, n=60, inner=300, op=0.6),
        E("doodle_horse", x=1400, y=960, s=1.6, rider="lieuthang", expr="shock"),
        E("emoji", ch="😱", x=1720, y=560, size=150),
        E("boom", text="BẪY!", x=1560, y=230, size=170, rot=8),
        E("ribbon_title", kicker="TÍ XUYÊN SỬ", title="LIỄU THĂNG|MẮC LỪA", x=70, y=300, size=160, sub="Ải Chi Lăng 1427"),
    ]},
    "metadata": {
        "title": "Liễu Thăng mắc lừa ở ải Chi Lăng 😱 | Tí Xuyên Sử",
        "alt_titles": ["15 vạn quân Minh và cú lừa thế kỷ ở Chi Lăng", "Vì sao Liễu Thăng mất mạng ở núi Mã Yên?"],
        "description": "Năm 1427, nghĩa quân Lam Sơn đang vây quân Minh ở Đông Quan. Nhà Minh gửi 15 vạn viện binh sang giải vây… và Liễu Thăng đã mắc một cú lừa ở ải Chi Lăng.\n\n💬 Bạn đoán nghĩa quân sẽ làm gì tiếp theo? Bình luận nhé!\n🔔 Đăng ký kênh để xem phần sau.\n\nTư liệu: Đại Việt sử ký toàn thư; SGK Lịch sử 7; Bảo tàng Lịch sử Quốc gia.\nẢnh nền: \"Chi Lăng 2.jpg\", \"Chi Lăng 3.jpg\" – Bùi Thụy Đào Nguyên, CC BY-SA 3.0, Wikimedia Commons; \"Quymon.JPG\" – Viethavvh, phạm vi công cộng. Bản đồ: Natural Earth; Free-GIS-Data (34 tỉnh thành, gồm quần đảo Hoàng Sa và Trường Sa của Việt Nam).\nHình minh hoạ mang tính hài hước, tái hiện; sự kiện theo sử liệu.",
        "hashtags": ["#LichSuVietNam", "#ChiLang", "#TiXuyenSu"],
        "tags": ["chi lăng", "liễu thăng", "lê lợi", "trần lựu", "khởi nghĩa lam sơn", "lịch sử hài hước", "tí xuyên sử"],
        "category_id": "27", "made_for_kids": False, "language": "vi",
        "pinned_comment": "Dự đoán đi: nghĩa quân sẽ xử lý phần còn lại của đạo quân Minh thế nào? 👇",
    },
}
Path(__file__).with_name("episode.json").write_text(json.dumps(ep, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(scenes), "cảnh")
