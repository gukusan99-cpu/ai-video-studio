# Leader review – pilot (thiết kế lại hình ảnh: dàn nhân vật + nền sơn dầu) – vòng 1
**Điểm:** 3.4/5 (trung bình) · **Kết luận:** CẦN SỬA

| Tiêu chí | Điểm |
|---|---|
| Giống tinh thần phong cách tham chiếu (thân nhộng không tay, áo vẽ trên thân, mũ to, mặt chính bán tả thực / phụ đơ) mà không chép nhân vật | 3.5 |
| Chất "tranh sơn dầu tự vẽ" của nền | 3.5 |
| Đọc được mặt/biểu cảm ở 1080p | 2.5 |
| Bố cục: bóng thoại/nhãn/phụ đề không đè mặt | 3.0 |
| Tôn trọng lịch sử (không đùa lúc có người chết) | 3.0 |
| Quy tắc bản đồ (Hoàng Sa, Trường Sa) | 5.0 |

qa.py --stage render: 5 đạt · 1 lỗi (thời lượng 59.1s – bỏ qua vì là pilot).

## ✅ Điểm tốt
- **Dàn nhân vật (channel/cast_sheet.png) là bước nhảy lớn so với ep003:** đúng công thức thân trụ không tay, áo/giáp vẽ thẳng lên thân (vảy giáp, bổ tử, đai), mũ to chi tiết (mũ trụ có tua đỏ, phốc đầu cánh chuồn, nón lá). Nhân vật chính có lông mày, râu, mắt có tròng, nghiến răng (Trần Lựu, Thôi Tụ); lính/dân phu mặt đơ chấm-gạch – đúng tinh thần kênh tham chiếu nhưng là nhân vật Việt/Minh của riêng mình, không chép Vasco/lính Bồ.
- **Bảng 12 biểu cảm (cast_expressions.png)** rõ ràng, phân biệt tốt smug / grit / shock / cry – đủ "vốn" để kể chuyện bằng mặt.
- **Nền sơn dầu (oil_backgrounds.jpg)** đã bỏ hẳn ảnh chụp thật: có vân canvas, chuyển màu trời theo giờ (day/dusk/storm/night), núi đá vôi đúng địa hình Lạng Sơn, gorge rất hợp Chi Lăng. Hết lỗi ep003 (ảnh Wikimedia + cỏ dán, dây điện).
- Cảnh 4 Trần Lựu (mặt sly, nhãn tên) và cảnh 7 lính Minh với mix panic/shock/cry là hai khung đẹp nhất – đúng chất "mặt đơ hài" của lính.
- Bản đồ cảnh 1 & 8: nhãn **QĐ. Hoàng Sa (Việt Nam)** và **QĐ. Trường Sa (Việt Nam)** hiện rõ, có chấm đảo, "NHÀ MINH" ghi đúng triều đại. Đạt quy tắc.
- Kịch bản nêu đủ bối cảnh ai–ở đâu–khi nào ở câu đầu.

## ⚠️ Cần cải thiện
1. **Không có một cận cảnh nào.** Tham chiếu sống nhờ cận mặt (khung mặt lấp 1/3–1/2 màn hình, nghiến răng). Ở ep004 mặt Liễu Thăng chỉ rộng ~70 px (s=1.3 trên ngựa), Tí ~55 px – ở 1080p xem trên điện thoại thì "smug"/"angry" đều trông như nhắm mắt; toàn bộ công sức vẽ mắt/râu/răng bị phí. Thumbnail cũng vậy: mặt Liễu Thăng chỉ ~90 px trên 1280.
2. **Khoảnh khắc tử trận (cảnh 6, câu 1 lúc ~42.5s):** Liễu Thăng VẪN ngồi trên ngựa, lắc (shake) giữa speed lines, trong khi phía trên hiện huy hiệu chân dung gạch chéo đỏ kiểu "game over" + nhãn "Liễu Thăng" đè lên mũ của chính ông. Vừa mâu thuẫn hình ảnh (chết mà vẫn cưỡi ngựa) vừa mang chất hề đúng lúc có người chết – trái quy tắc kênh.
3. **Đè bố cục:**
   - Cảnh 4 (~31s): đuôi bóng "ĐUỔI!!!" (layer `chase`) đâm thẳng xuống mặt/mũ Liễu Thăng (vùng x≈520, y≈540–600).
   - Cảnh 5 (~35s): đuôi bóng "Ta đi trước…" (tx=760, ty=620) cắm vào mắt/mũ Liễu Thăng.
   - Cảnh 1: nhãn "Đông Quan" (≈x 330–410, y 313 trên khung 1920) chạm mắt trái của mặt Việt Nam (eyes_at 19.6,104).
   - Cảnh 6: nhãn tên của portrait (y≈570) nằm trên mũ trụ Liễu Thăng (y≈600).
   - Cảnh 2/3/5/7: Tí bị nhét vào mép phải x=1790–1800, nửa người chìm trong bụi cây đen của vignette (`_foreground corners`); cảnh 2 Tí y=650 **lơ lửng** trên ngọn bụi (lỗi vật lý). Cảnh 2 Tí chỉ hiện ~1 giây (appear 1 + delay 2.0s, câu kết thúc 17.96s).
4. **Tí lệch bible:** channel/bible.md quy định Tí *tóc bát úp, áo bà ba chàm, khăn đỏ, đồng hồ vàng*; cast.py vẽ Tí búi tó, áo cam, băng đô xanh, không đồng hồ. Đây là nhân vật thương hiệu – phải thống nhất.
5. **Nền "sơn dầu" mới ở mức tranh màu nước mờ:** nét cọ quá mịn/nhoè (paint_strokes radii nhỏ nhất 4 px bị finish() làm mềm), không thấy hướng nét cọ; cây là cùng một cụm tròn lặp lại; bụi góc gần như đen tuyền (#0x0x0x) thành mảng chết, ăn mất ~15% khung. Nhân vật viền đậm sắc nét đặt trên nền mờ nên trông như "dán", chưa hoà như tham chiếu (tham chiếu có nét mực trên nền).
6. **Ngựa (`doodle_horse`) còn là kiểu doodle phẳng của ep003**, không bóng, không vân – lệch chất lượng hẳn so với cast mới; người trụ đứng trên lưng ngựa không có yên.
7. **Câu lóng quá hạn mức (1–2/tập):** "xử đẹp", "toang" (2 lần: bóng Tí cảnh 3 + caption cảnh 7), "tin sái cổ", "kẹt xe thế kỷ 15", "rối như canh hẹ", "căng". Ngay sau cái chết (cảnh 7, ~47s) Tí cười "laugh" – nên bớt.
8. **UPLOAD.md sai ghi nguồn:** mục "Nội dung AI" vẫn ghi *"ảnh nền (nếu có) là ảnh chụp thật có giấy phép"* – nay nền là tự vẽ bằng code (paint.py), cần sửa. Phần "Mô tả" đã ghi đúng "tự vẽ (tranh sơn dầu kỹ thuật số)".

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
1. **Thêm cận cảnh mặt (ưu tiên số 1 – giữ chân người xem).** Trong `make_episode.py` → episode.json:
   - scenes[1] (cảnh 2, câu 1 "khinh địch ra mặt"): thay layer `lt` bằng `peg(who="lieuthang", x=700, y=1350, s=3.2, expr="smug")` (cắt ngang ngực, mặt ≥ 350 px), bỏ emoji 😏; bóng "Nghĩa quân? Chưa nghe bao giờ." đặt x=1250, y=260, tx=980, ty=420 (ngoài mặt).
   - scenes[3] (cảnh 4, câu 1 "tin sái cổ"): chèn khung cận `peg(lieuthang, s=3.2, expr="grit")` 1.5s trước khi chuyển sang toàn cảnh ngựa đuổi.
   - scenes[5] (cảnh 6, câu 0 "Trống trận"): cận `expr="shock"` s=3.0 ở giữa, giữ chữ TÙNG TÙNG ở y≤220.
   - `out/thumbnail.png`: thay ngựa+người nhỏ bằng mặt Liễu Thăng `shock` chiếm nửa phải (cao ≥ 600/720 px), giữ chữ trái; dời badge "TÍ XUYÊN SỬ" lên trên 20 px (dấu ngã của "LIỄU" đang chạm badge).
2. **Làm lại khoảnh khắc tử trận – scenes[5] (cảnh 6):** layer `lt` và `lines` thêm `"hide_t": 3.9` (tắt trước câu 1 bắt đầu ~4.0s trong cảnh) và bỏ `shake`; câu 1 hiện nền gorge/storm giảm bão hoà + một chiếc mũ trụ có tua đỏ rơi trên đất + lá cờ Minh đổ (đạo cụ tĩnh, `motion: none`), nhạc hạ. Layer `rip`: `mark=""`, `expr="neutral"`, ring xám, nhãn "Liễu Thăng (tử trận, 1427)" – không gạch chéo, không emoji. Cảnh 7 Tí đổi `expr` từ `laugh` → `determined`, bóng "Còn căng hơn nữa!" → "Chuyện chưa hết đâu…".
3. **Gỡ đè bố cục:**
   - scenes[3] layer `chase` bubble "ĐUỔI!!!": đặt x=300, y=300, tx=470, ty=470 (đuôi dừng trên tua mũ).
   - scenes[4] layer `brag`: ty 620 → 520, y 420 → 360.
   - scenes[0] map_label "Đông Quan": thêm dx=-70 (hoặc dời `eyes_at` VN sang [20.6,105.2]) để nhãn cách mắt ≥ 20 px.
   - scenes[5] portrait: y=300, r=120 (nhãn tên ở ~y 440, cách mũ ≥ 100 px) – áp dụng cùng mục 2.
   - Tí (scenes[1], [2], [4], [6]): đưa về x≈1640, y≈980 (đứng trên đất, không trên bụi), s ≥ 1.2; scenes[1] y=650 → 980 và `appear_delay` 2.0 → 0.3 để Tí hiện ≥ 2s.
   - Thêm kiểm tra vào `studio/qa.py`: bbox mặt (peg/portrait) không giao bbox bubble/caption/label/vùng phụ đề y>1000.
4. **Thống nhất Tí với bible:** trong `studio/cast.py` nhân vật `ti` → tóc đen bát úp + 1 lọn xoăn, áo bà ba chàm 3 cúc trắng, khăn quàng đỏ, đồng hồ vàng trên ngực, Mít `#62C462` trên vai trái (bên phải khung hình). Nếu muốn giữ áo cổ đại "xuyên không" thì phải sửa `channel/bible.md` trước và hỏi người dùng – không tự đổi thương hiệu. Xuất lại `channel/cast_sheet.png`.
5. **Nâng chất sơn dầu – `studio/paint.py`:** `paint_strokes` radii → (40, 22, 12, 6) với nét dài theo hướng gradient (độ dài 3–4× bán kính) để thấy hướng cọ; `finish(ink=0.5)` thêm nét mực sẫm mảnh viền núi/cây; `_trees` thêm ≥ 3 dạng tán (tre, thông, cây bụi) và lệch màu ±10%; `_foreground(corners=True)` nâng độ sáng bụi góc tối thiểu L≈18% và thu bán kính còn ≤ 12% chiều rộng để không nuốt nhân vật. Thay `doodle_horse` bằng ngựa kiểu cast (bóng đổ, viền #2B1B12, có yên) trong `studio/cast.py`.
6. **Văn bản:** `out/UPLOAD.md` (và mẫu sinh meta) mục "Nội dung thay đổi/tổng hợp" → "nhân vật và ảnh nền đều tự vẽ bằng code (vector + tranh sơn dầu kỹ thuật số), không có ảnh chụp/AI giống thật". Giảm lóng còn 2: giữ "rối như canh hẹ" (lời đọc) + "Kẹt xe thế kỷ 15"; caption cảnh 7 "Tình hình: hơi bị toang" → "Tình hình: rối loạn"; bóng Tí cảnh 3 "…toang" → "…khó thoát lắm".

VERDICT: CẦN SỬA
