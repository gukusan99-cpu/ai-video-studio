"""Tập thử phong cách "fun" v2 (nhân vật búp bê trụ + nền sơn dầu tự vẽ + hiệu ứng + meme) – Liễu Thăng và cú lừa ở ải Chi Lăng.
Chạy: python episodes/ep004-chi-lang-oil/make_episode.py"""
import json
from pathlib import Path

DV, MINH = "#E9A92B", "#C4453C"



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


TEO = lambda expr="blank", x=1640, y=990, s=1.15, pet="": E("peg", who="teo", x=x, y=y, s=s, expr=expr, flip=True, pet_expr=pet)
TB = lambda text, kind="speech", size=30: E("bubble", x=1470, y=380, text=text, tx=1600, ty=540, kind=kind, size=size)
CU_BG = lambda kind, time, seed: [E("oil_bg", kind=kind, time=time, seed=seed, blur=6), E("flash", color="#1C1612", op=0.18)]

scenes = [
    dict(key="open", bg_motion="still",
         narration=[N("Năm *1427*, nghĩa quân Lam Sơn của *Lê Lợi* đang vây chặt quân Minh trong thành Đông Quan, tức Hà Nội bây giờ.",
                      "Năm một nghìn bốn trăm hai mươi bảy, nghĩa quân Lam Sơn của Lê Lợi đang vây chặt quân Minh trong thành Đông Quan, tức Hà Nội bây giờ."),
                    N("Nhà Minh tính toán: gửi *mười lăm vạn quân* sang, thế nào cũng thắng!")],
         layers=[L("bg", [E("map_base", view="asia", vn=DV, cn=MINH, river=False, cn_label="NHÀ MINH")]),
                 L("faces", [E("nation", which="VN", view="asia", expr="angry", eyes_at=[19.6, 104.0], size=0.55, shape=False),
                             E("map_label", place="Đông Quan", view="asia", kind="fort", text="Đông Quan", dx=-220, dy=40, size=26)]),
                 L("arrow", [E("map_arrow", pts=[[27.5, 109.5], [24.0, 108.2], "Chi Lăng"], view="asia", width=24, label="15 vạn viện binh", label_dy=-46),
                             E("map_label", place="Chi Lăng", view="asia", kind="battle", text="Chi Lăng", dx=120, dy=0, size=26)], appear=1, appear_delay=1.0, fade_in=0.2),
                 L("smug", [E("nation", which="CN", view="asia", expr="smug", eyes_at=[31, 104], size=1.3, shape=False),
                            E("emoji", ch="😎", x=1000, y=300, size=110),
                            E("bubble", x=1350, y=330, text="15 vạn quân|là đủ!", tx=1110, ty=360, kind="shout", size=46)], appear=1, fade_in=0.12),
                 L("vn", [E("bubble", x=560, y=640, text="Ờ… thử xem.", tx=740, ty=560, size=34)], appear=1, appear_delay=3.0, fade_in=0.15)],
         sfx=[{"type": "chime", "at": 0.1, "gain": 0.2}]),
    dict(key="march", bg_motion="left",
         narration=[N("Tướng *Liễu Thăng* dẫn mười vạn quân, ầm ầm tiến qua *ải Chi Lăng*, Lạng Sơn."),
                    N("Ông khinh địch ra mặt, coi nghĩa quân như… không có.")],
         layers=[L("bg", [E("oil_bg", kind="karst_valley", time="day", seed=2)]),
                 L("army", [E("crowd", who="minh_soldier", x=1350, y=958, n=7, s=0.53, gap=100, rows=2, item="spear", seed=2)], motion="drift_left"),
                 L("lt", [E("doodle_horse", x=620, y=880, s=1.3, rider="lieuthang", expr="smug"),
                          E("caption_box", text="Liễu Thăng · tự tin 200%", x=60, y=60)], motion="bob"),
                 # cận cảnh: mặt kiêu ngạo
                 L("cu", CU_BG("karst_valley", "day", 2) + [E("closeup", who="lieuthang", expr="smug", x=640, s=3.0),
                        E("emoji", ch="😏", x=1010, y=230, size=100),
                        E("bubble", x=1100, y=640, text="Nghĩa quân?|Chưa nghe bao giờ.", tx=880, ty=540, size=36)], appear=1, fade_in=0.08),
                 L("teo", [TEO("blank"), TB("Ông ơi…|cẩn thận cái miệng.", size=28),
                           E("callout", text="Tèo (vai: châu chấu Tí)", x=1180, y=860, tx=1560, ty=800, size=30)], appear=1, appear_delay=0.4, fade_in=0.12)]),
    dict(key="terrain", bg_motion="push_down",
         narration=[N("Có điều, Chi Lăng là một thung lũng hẹp, hai bên *núi đá dựng đứng*."),
                    N("Lòng thung lũng thì *lầy lội*, quân đông đến mấy cũng phải đi thành hàng dài.")],
         layers=[L("bg", [E("oil_bg", kind="gorge", time="day", seed=1)]),
                 L("c1", [E("callout", text="Núi đá", x=300, y=200, tx=520, ty=380, size=48),
                          E("callout", text="Núi đá", x=1600, y=200, tx=1380, ty=330, size=48)], appear=0, fade_in=0.15),
                 L("c2", [E("callout", text="Lối đi hẹp, lầy", x=520, y=560, tx=820, ty=780, size=46), E("emoji", ch="🫠", x=1000, y=640, size=90)], appear=1, fade_in=0.15),
                 L("queue", [E("crowd", who="minh_soldier", x=900, y=928, n=12, s=0.36, gap=62, item="spear", seed=21),
                             E("caption_box", text="Kẹt xe thế kỷ 15", x=1000, y=700, size=32)], appear=1, appear_delay=1.0, motion="drift_left"),
                 L("teo", [TEO("think"), TB("Đông thế mà vào đây|thì xoay xở kiểu gì…", size=26)], appear=1, appear_delay=2.0, fade_in=0.12)]),
    dict(key="lure", bg_motion="right",
         narration=[N("Tướng *Trần Lựu* của nghĩa quân ra đánh vài hiệp, rồi… *quay đầu bỏ chạy*."),
                    N("Diễn hơi lố, nhưng Liễu Thăng *tin ngay*, hăm hở đuổi theo vào sâu trong ải.")],
         layers=[L("bg", [E("oil_bg", kind="river", time="dawn", seed=4)]),
                 L("tl", [E("peg", who="tranluu", x=1350, y=920, s=1.1, expr="sly", flip=True, item="sword", label=True),
                          E("crowd", who="dv_soldier", x=1660, y=958, n=3, s=0.52, gap=110, flip=True, item="spear", seed=5, expr="happy"),
                          E("bubble", x=1400, y=360, text="Ối thua rồi!|(diễn đó)", tx=1360, ty=560, size=34)], motion="drift_right"),
                 L("chase", [E("speed_lines", cx=960, cy=540, n=50, inner=420, op=0.55),
                             E("doodle_horse", x=520, y=880, s=1.3, rider="lieuthang", expr="angry")], appear=1, fade_in=0.12, motion="drift_right"),
                 L("cu", CU_BG("river", "dawn", 4) + [E("speed_lines", cx=640, cy=450, n=60, inner=380, op=0.6),
                        E("closeup", who="lieuthang", expr="grit", x=640, s=3.0),
                        E("bubble", x=1280, y=330, text="ĐUỔI!!!", tx=980, ty=400, kind="shout", size=64)], appear=1, appear_delay=2.0, fade_in=0.06),
                 L("rate", [E("caption_box", text="Diễn xuất: 3/10 · Độ tin: 10/10", x=60, y=60, size=32)], appear=1, appear_delay=0.6, fade_in=0.1)],
         sfx=[{"type": "whoosh", "at": 5.6, "gain": 0.3}]),
    dict(key="mayen", bg_motion="push_up",
         narration=[N("Đến *núi Mã Yên*, ông dẫn hơn trăm kỵ binh phóng lên trước."), N("Và rồi…")],
         layers=[L("bg", [E("oil_bg", kind="mountain_pass", time="dusk", seed=3)]),
                 L("cav", [E("doodle_horse", x=760, y=890, s=1.15, rider="lieuthang", expr="smug"),
                           E("doodle_horse", x=1100, y=900, s=0.9, rider="minh_soldier", expr="deadpan"),
                           E("doodle_horse", x=1360, y=905, s=0.85, rider="minh_soldier", expr="deadpan")], motion="drift_left"),
                 L("tag", [E("caption_box", text="Núi Mã Yên", x=60, y=60), E("sign", text="Mã Yên →", x=380, y=900)]),
                 L("brag", [E("bubble", x=760, y=330, text="Ta đi trước,|các ngươi theo sau!", tx=760, ty=500, size=32)], appear=0, appear_delay=1.0, fade_in=0.15),
                 L("teo", [TEO("blank", pet="scared"), TB("Linh cảm|không lành…", kind="think", size=30)], appear=1, fade_in=0.1)]),
    dict(key="ambush", bg_motion="still",
         narration=[N("*Trống trận nổi lên!* Phục binh từ hai bên sườn núi ào ra!", "Trống trận nổi lên! Phục binh từ hai bên sườn núi ào ra!"),
                    N("*Liễu Thăng tử trận* ngay tại chỗ.")],
         layers=[L("bg", [E("oil_bg", kind="gorge", time="storm", seed=1)]),
                 L("lines", [E("speed_lines", cx=960, cy=560, n=70, inner=380, op=0.7)], hide_t=3.85),
                 L("amb_l", [E("crowd", who="dv_soldier", x=380, y=588, n=4, s=0.53, gap=95, item="bow", seed=3, expr="angry")], appear_t=0.25, fade_in=0.1, motion="from_left"),
                 L("amb_r", [E("crowd", who="dv_soldier", x=1540, y=588, n=4, s=0.53, gap=95, flip=True, item="spear", seed=4, expr="angry")], appear_t=0.35, fade_in=0.1, motion="from_right"),
                 L("arrows", [E("arrow_volley", x0=380, y0=470, x1=900, y1=820, n=16, seed=7), E("arrow_volley", x0=1540, y0=470, x1=1020, y1=820, n=16, seed=8)], appear_t=0.9, fade_in=0.1),
                 L("lt", [E("doodle_horse", x=960, y=900, s=1.2, rider="lieuthang", expr="shock")], hide_t=1.8),
                 L("boom", [E("boom", text="TÙNG TÙNG!", x=960, y=250, size=150)], appear_t=0.05, fade_in=0.05, hold=1.6),
                 L("flash", [E("flash", color="#FFFFFF", op=0.9)], appear_t=0.02, fade_in=0.03, hold=0.15),
                 # cận cảnh hoảng hốt (trước câu tử trận)
                 L("cu", CU_BG("gorge", "storm", 1) + [E("closeup", who="lieuthang", expr="shock", x=960, s=3.0),
                        E("arrow_volley", x0=200, y0=200, x1=700, y1=700, n=10, seed=9), E("arrow_volley", x0=1720, y0=200, x1=1220, y1=700, n=10, seed=10)],
                   appear_t=1.8, fade_in=0.06, hide_t=3.85),
                 # khoảnh khắc tử trận: tĩnh, giảm màu, không đùa
                 L("rip", [E("oil_bg", kind="gorge", time="storm", seed=1), E("flash", color="#2A2A2A", op=0.45),
                           E("fallen_flag", x=640, y=900, s=1.2), E("fallen_helmet", x=1180, y=880, s=1.3),
                           E("medallion", who="lieuthang", x=960, y=300, r=130, expr="neutral", name="Liễu Thăng")], appear=1, fade_in=0.4)],
         sfx=[{"type": "crash", "at": 0.05, "gain": 0.4}, {"type": "whoosh", "at": 0.9, "gain": 0.3}]),
    dict(key="chaos", bg_motion="left",
         narration=[N("Mất chủ tướng, mười vạn quân Minh *rối như canh hẹ*."), N("Mà đây… mới chỉ là *màn khởi động*.")],
         layers=[L("bg", [E("oil_bg", kind="karst_valley", time="dusk", seed=6)]),
                 L("m1", [E("crowd", who="minh_soldier", x=640, y=958, n=5, s=0.53, gap=95, rows=2, item="spear", seed=11, exprs=["panic", "shock", "cry"])], motion="shake"),
                 L("m2", [E("crowd", who="minh_soldier", x=1250, y=958, n=5, s=0.53, gap=95, rows=2, flip=True, item="flag", seed=12, exprs=["panic", "shock", "cry"])], motion="shake"),
                 L("fx", [E("emoji", ch="❓", x=640, y=520, size=90), E("emoji", ch="😵", x=1250, y=520, size=90), E("emoji", ch="💨", x=950, y=640, size=80)], appear=0, appear_delay=0.8, fade_in=0.15),
                 L("cap", [E("caption_box", text="Tình hình: hỗn loạn toàn tập", x=60, y=60)], appear=0, appear_delay=1.2, fade_in=0.1),
                 L("teo", [TEO("blank", pet="smug"), TB("Chưa hết đâu.", size=32)], appear=1, fade_in=0.1)]),
    dict(key="outro", bg_motion="still",
         narration=[N("Đạo quân Minh mất tướng vẫn còn rất đông. Theo bạn, nghĩa quân sẽ làm gì tiếp theo? Bình luận dự đoán nhé!"),
                    N("Và nhớ *đăng ký kênh* để xem phần sau!")],
         layers=[L("bg", [E("map_base", view="asia", vn=DV, cn=MINH, river=False, cn_label="NHÀ MINH")]),
                 L("faces", [E("nation", which="CN", view="asia", expr="sad", eyes_at=[31, 104], size=1.3, shape=False),
                             E("nation", which="VN", view="asia", expr="cool", eyes_at=[19.6, 104.0], size=0.55, shape=False)]),
                 L("teo", [E("peg", who="teo", x=320, y=1010, s=1.6, expr="blank", pet_expr="happy"),
                           E("bubble", x=380, y=200, text="Bình luận|dự đoán nhé!", tx=360, ty=330, size=34)], motion="bob")],
         sfx=[{"type": "chime", "at": 0.1, "gain": 0.2}]),
]
for i, sc in enumerate(scenes):
    sc["id"] = i + 1

ep = {
    "id": "ep004-chi-lang-oil",
    "series": "Tí Xuyên Sử",
    "title_working": "Liễu Thăng và cú lừa ở ải Chi Lăng (phong cách fun v2 – nhân vật mới + nền sơn dầu)",
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
        E("oil_bg", kind="gorge", time="storm", seed=1),
        E("speed_lines", cx=1420, cy=420, n=60, inner=300, op=0.6),
        E("closeup", who="lieuthang", expr="shock", x=1420, s=3.3),
        E("emoji", ch="😱", x=1800, y=200, size=130),
        E("boom", text="BẪY!", x=1000, y=170, size=150, rot=-8),
        E("ribbon_title", kicker="TÍ XUYÊN SỬ", title="LIỄU THĂNG|MẮC LỪA", x=70, y=330, size=150, sub="Ải Chi Lăng 1427", kicker_dy=-22),
    ]},
    "metadata": {
        "title": "Liễu Thăng mắc lừa ở ải Chi Lăng 😱 | Tí Xuyên Sử",
        "alt_titles": ["15 vạn quân Minh và cú lừa thế kỷ ở Chi Lăng", "Vì sao Liễu Thăng mất mạng ở núi Mã Yên?"],
        "description": "Năm 1427, nghĩa quân Lam Sơn đang vây quân Minh ở Đông Quan. Nhà Minh gửi 15 vạn viện binh sang giải vây… và Liễu Thăng đã mắc một cú lừa ở ải Chi Lăng.\n\n💬 Bạn đoán nghĩa quân sẽ làm gì tiếp theo? Bình luận nhé!\n🔔 Đăng ký kênh để xem phần sau.\n\nTư liệu: Đại Việt sử ký toàn thư; SGK Lịch sử 7; Bảo tàng Lịch sử Quốc gia.\nẢnh nền & nhân vật: tự vẽ (tranh sơn dầu kỹ thuật số). Bản đồ: Natural Earth; Free-GIS-Data (34 tỉnh thành, gồm quần đảo Hoàng Sa và Trường Sa của Việt Nam).\nHình minh hoạ mang tính hài hước, tái hiện; sự kiện theo sử liệu.",
        "hashtags": ["#LichSuVietNam", "#ChiLang", "#TiXuyenSu"],
        "tags": ["chi lăng", "liễu thăng", "lê lợi", "trần lựu", "khởi nghĩa lam sơn", "lịch sử hài hước", "tí xuyên sử"],
        "category_id": "27", "made_for_kids": False, "language": "vi",
        "pinned_comment": "Dự đoán đi: nghĩa quân sẽ xử lý phần còn lại của đạo quân Minh thế nào? 👇",
    },
}
Path(__file__).with_name("episode.json").write_text(json.dumps(ep, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(scenes), "cảnh")
