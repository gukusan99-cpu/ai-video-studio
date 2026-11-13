# Leader review – pilot (dàn nhân vật + nền sơn dầu + host Tèo mới) – vòng 2
**Điểm:** 4.4/5 (trung bình) · **Kết luận:** ĐẠT

| Tiêu chí | Vòng 1 | Vòng 2 |
|---|---|---|
| Giống tinh thần phong cách tham chiếu mà không chép nhân vật | 3.5 | 4.5 |
| Chất "tranh sơn dầu tự vẽ" của nền | 3.5 | 4.0 |
| Đọc được mặt/biểu cảm ở 1080p | 2.5 | 4.5 |
| Bố cục: bóng thoại/nhãn/phụ đề không đè mặt | 3.0 | 4.0 |
| Tôn trọng lịch sử (không đùa lúc có người chết) | 3.0 | 5.0 |
| Quy tắc bản đồ (Hoàng Sa, Trường Sa) | 5.0 | 5.0 |
| Tèo & châu chấu Tí đúng bible MỚI | – | 4.0 |

qa.py --stage render: 5 đạt · 1 lỗi (thời lượng 58.3s – bỏ qua vì là pilot, theo chỉ đạo).
Khung tự trích thêm: 15.5s, 23s, 31.5s, 37s, 40.5s, 43s, 48s, 55s (scratchpad/r2/).

## Kiểm tra từng yêu cầu vòng 1
| # | Yêu cầu | Kết quả |
|---|---|---|
| 1 | Cận cảnh mặt (cảnh 2, 4, 6, thumbnail) | ✅ Cảnh 2 (smug, ~15.5s), cảnh 4 (grit, ~31.5s), cảnh 6 (shock, ~40.5s): mặt Liễu Thăng cao ~1/3 khung, đọc rõ mắt/râu/răng. Thumbnail: mặt shock chiếm nửa phải, cao > 600/720 px, badge không còn chạm dấu ngã. |
| 2 | Khoảnh khắc tử trận | ✅ 43s: nền gorge giảm bão hoà, cờ đổ + mũ trụ rơi tĩnh, huy hiệu xám "Liễu Thăng" không gạch chéo, không emoji; cận shock đã tắt trước câu. Cảnh 7 Tèo không cười, bóng "Chưa hết đâu." – đúng mực. |
| 3 | Gỡ đè bố cục | ✅ cơ bản: "ĐUỔI!!!" và "Ta đi trước…" không còn cắm vào mặt; "Đông Quan" đã tách khỏi mắt bản đồ; portrait cách xa đạo cụ. Tèo đứng trên đất, không còn chìm trong bụi góc. Còn 1 lỗi nhỏ (xem mục 🔧1). |
| 4 | Nhân vật dẫn chuyện đúng bible | ✅ theo bible MỚI (quyết định của người dùng): Tèo tai vểnh, bát úp + lọn xoăn, áo bà ba chàm 3 cúc, khăn đỏ, đồng hồ vàng, châu chấu xanh trên vai; mặt "blank" mắt to trống, chấm đồng tử – rất đúng chất deadpan; texture sơn dầu giúp Tèo nổi bật thành "nhân vật thương hiệu" khác hẳn dàn cast. |
| 5 | Nâng chất sơn dầu + ngựa | ✅ oil_backgrounds.jpg: thấy hướng nét cọ, viền mực ở núi/cây, 3 dạng tán (tán tròn, thông, cây dù), bụi góc sáng hơn, không còn mảng đen chết. Ngựa đã có yên. Biển (sea/dusk) hơi xám nâu như bùn – chấp nhận cho pilot. |
| 6 | Văn bản: UPLOAD.md + lóng | ✅ UPLOAD.md ghi đúng "nhân vật và nền đều là tranh vẽ…", ghi chú AI có điều kiện. Lóng còn "Kẹt xe thế kỷ 15", "rối như canh hẹ", "hỗn loạn toàn tập" – trong hạn mức, không rơi vào lúc có người chết. |

## ✅ Điểm tốt
- Cận cảnh là thay đổi đáng giá nhất: ba nhịp smug → grit → shock của Liễu Thăng kể chuyện bằng mặt rất rõ, đúng thứ giữ chân người xem.
- Cảnh tử trận giờ là một "khoảng lặng" có chủ ý – tương phản tốt với nhịp hài trước và sau, tôn trọng lịch sử.
- Tèo deadpan + lời thoại cà khịa tỉnh bơ ("Ờ… thử xem.", "Ông ơi… cẩn thận cái miệng.", "Linh cảm không lành…", "Chưa hết đâu.") hài hơn hẳn mà không lố.
- Thumbnail đọc được ngay trên màn hình nhỏ: chữ to bên trái, mặt to bên phải, "BẪY!" nổi bật.

## ⚠️ Cần cải thiện
1. Bóng suy nghĩ "Linh cảm không lành…" (cảnh 5, ~37s) có một mảng chữ nhật trắng lòi ra ở góc trên trái đám mây – lỗi vẽ bubble kiểu "think".
2. Viền mắt của Tèo dày và đen nên ở cỡ nhỏ (cảnh toàn) trông như **đeo kính**, không phải "mắt to trống". Bible không có kính.
3. Châu chấu Tí đổi bên: cảnh 5 (37s) nằm bên TRÁI khung hình (Tèo bị flip), cảnh 8 (55s) bên PHẢI. Bible khoá "vai trái Tèo – phía bên phải khung hình".
4. channel/bible.md vẫn còn sót chỗ cũ: đoạn "mô tả khoá" prompt AI còn ghi *boy named Tí … green gecko*; danh sách biểu cảm chưa có `blank`; CTA mẫu "Bạn muốn Tí đến…" (giờ Tèo là người dẫn).
5. Trong tập, Tèo chưa từng được giới thiệu tên (lời đọc lẫn chữ) – người xem mới không biết host là ai.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện – không chặn ĐẠT, làm trước khi sản xuất tập chính thức)
1. `studio/doodle.py` (hàm callout/bubble kiểu think) – bỏ hình chữ nhật nền thừa phía sau đám mây; kiểm lại scenes[4] layer bóng "Linh cảm|không lành…".
2. `studio/cast.py` → mặt Tèo `expr="blank"`: giảm độ dày viền tròng mắt (≈ 1/2 hiện tại) và đổi màu viền sang nâu `#2B1B12` mỏng, hoặc thêm mí trên nhẹ, để không bị đọc thành kính; xuất lại `channel/cast_sheet.png`.
3. `studio/cast.py` → khi `flip=True` với `who="teo"`, giữ châu chấu ở bên phải khung hình (không lật theo thân), hoặc bỏ flip cho Tèo ở scenes[4].
4. `channel/bible.md` – sửa đoạn prompt khoá thành "boy named Tèo … big blank eyes with dot pupils … a small green grasshopper named Tí on his left shoulder"; thêm `blank` vào danh sách biểu cảm; CTA mẫu → "Bạn muốn Tèo và Tí đến… tiếp theo?".
5. episode.json → lần đầu Tèo xuất hiện (scenes[1]): thêm `label="Tèo"` dưới chân 1.5s (hoặc 1 câu bóng "Mình là Tèo. Đây là Tí." ở tập mở màn chính thức).

VERDICT: ĐẠT
