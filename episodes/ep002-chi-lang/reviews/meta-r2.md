# Leader review – meta – vòng 2
**Điểm:** 3.9/5 (trung bình) · **Kết luận:** CẦN SỬA

> qa.py --stage meta: 6 đạt · 0 cảnh báo · 0 lỗi (tiêu đề 59 ký tự, tag 199/450 ký tự, 5 hashtag, có thumbnail). Dòng "Có bình luận ghim" vẫn in giá trị rỗng, nhưng UPLOAD.md có nội dung. Đây là lỗi hiển thị của qa.py.
> Đã xem: out/UPLOAD.md, out/metadata.json, out/thumbnail.png (1280x720), make_episode.py → chapters/metadata, make.py dòng 541 và 557–560, build/timing.json.

## Yêu cầu vòng 1 → trạng thái
| # | Yêu cầu vòng 1 | Trạng thái | Ghi chú |
|---|---|---|---|
| 1 | Sửa chủ thể "họ phải thề rút về nước" | ✅ Đã xử lý | Câu mới: "Chỉ khoảng hai tháng sau, nhà Minh phải thề rút hết quân về nước." Khớp lời thoại cảnh 1. Hết lỗi sự thật. |
| 2 | Thêm chương (timestamps) | ⚠️ Làm nhưng chưa có hiệu lực | 9 mốc khớp đúng timing.json. Mốc được sinh tự động qua `{CHAPTERS}`, cách làm tốt. Nhưng có **2 chương ngắn hơn 10 s**: "0:57 Kế sách" chỉ dài 7.8 s (57.1 → 64.9 s), "1:33 Cần Trạm – Phố Cát" dài 9.7 s (93.3 → 103.0 s). YouTube yêu cầu mọi chương ≥ 10 s, nếu không sẽ **bỏ qua toàn bộ chương**. Lỗi này nằm ngay trong danh sách mốc tôi đưa ra ở vòng 1, tôi nhận phần sai. |
| 3 | Thêm Bảo tàng Lịch sử Quốc gia vào nguồn | ✅ Đã xử lý | "…SGK Lịch sử 7; Bảo tàng Lịch sử Quốc gia; Báo Pháp luật…" |
| 4 | make.py: dòng Thumbnail theo format | ❌ Lỗi mới | Biểu thức được viết theo kiểu nối chuỗi `" + (… if FMT == "short" else …) + "` nhưng lại nằm **bên trong** chuỗi f-string ba nháy. Vì vậy UPLOAD.md in ra nguyên văn mã Python: `**Thumbnail:** " + ("`out/thumbnail.png` (Shorts) · …" if FMT == "short" else "…") + "`. Người đăng thủ công đọc gói này sẽ thấy lỗi ngay ở dòng thứ 2. |
| 5 | Thêm hashtag #KhoiNghiaLamSon và 4 tag | ✅ Đã xử lý | 5 hashtag, 14 tag, 199/450 ký tự. |

| Tiêu chí | Điểm | Ghi chú |
|---|---|---|
| Tiêu đề gây tò mò, ≤70 ký tự, có từ khoá | 4 | Không đổi: 59 ký tự, có từ khoá và năm ở đầu, kết bằng câu hỏi. |
| Mô tả có tóm tắt + nguồn | 3.5 | Tóm tắt đã đúng sự thật, nguồn đủ. Nhưng khối chương sẽ không được YouTube nhận vì có 2 chương dưới 10 s. |
| Thumbnail đọc được trên màn hình nhỏ | 4 | Không đổi so với vòng 1, vẫn tốt: chữ to, Liễu Thăng bị gạch X, Tí đúng bible. |
| Hashtag/tag hợp lý | 4.5 | Đã bổ sung các cụm học sinh lớp 7 hay tìm. Có 2 tag gần trùng nhau ("hội thề đông quan" và "hội thề đông quan 1427"), chấp nhận được. |
| Thiết lập "dành cho trẻ em" & "nội dung AI" / gói đăng | 3.5 | madeForKids=false, AI=Không, private, category 27 đều đúng. Trừ điểm vì dòng Thumbnail trong UPLOAD.md là mã nguồn bị lộ ra. |

## ✅ Điểm tốt
- Lỗi sự thật ở mô tả đã được sửa, và câu mới khớp lời thoại.
- Chương được sinh tự động từ `chapters` + timing.json. Cách này tốt: nếu chạy lại tts, mốc giây sẽ tự cập nhật.
- Nguồn đã đầy đủ, khớp với fact_check. Hashtag và tag đã bám theo SGK.
- Thumbnail và tiêu đề giữ chất lượng như vòng 1.

## ⚠️ Cần cải thiện
- Hai lỗi ở phần Yêu cầu sửa bên dưới. Cả hai đều sửa được trong vài phút và không cần render lại video.
- (Không bắt buộc) qa.py → check "Có bình luận ghim" nên in nội dung (hoặc độ dài) của metadata.pinned_comment, thay vì in chuỗi rỗng.
- (Không bắt buộc) Câu "xem tập mới mỗi tuần" chỉ nên giữ nếu kênh thật sự đăng hằng tuần.
- (Cho tập sau) make.py có thể tự kiểm tra chương: gộp chương dưới 10 s vào chương trước đó và cảnh báo khi gộp.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
> Không cần render lại. Chỉ cần sửa, chạy `python3 episodes/ep002-chi-lang/make_episode.py`, rồi chạy `python make.py episodes/ep002-chi-lang --stage meta`.
1. **episodes/ep002-chi-lang/make_episode.py → `ep["chapters"]`**: gộp các chương ngắn để mọi chương đều ≥ 10 s.
   - Xoá `{"scene": 7, "title": "Kế sách: đánh Liễu Thăng trước"}`. Đổi chương scene 6 thành `"Viện binh nhà Minh – kế đánh Liễu Thăng trước"`. Chương này sẽ dài 0:47 → 1:04 (17 s).
   - Xoá `{"scene": 11, "title": "Cần Trạm – Phố Cát"}`. Đổi chương scene 12 thành `{"scene": 11, "title": "Truy kích: Cần Trạm – Phố Cát – Xương Giang"}`. Chương này sẽ dài 1:33 → 2:10 (37 s).
   - Kết quả còn 7 chương: 0:00 · 0:17 · 0:47 · 1:04 · 1:33 · 2:10 · 2:38. Chương ngắn nhất dài 17 s.
   - Lý do: YouTube bỏ qua toàn bộ chương nếu có một chương dưới 10 s.
2. **make.py dòng 560 (mẫu UPLOAD.md)**: tính giá trị dòng Thumbnail *trước* khi tạo f-string, rồi chèn vào bằng `{}`:
   ```python
   thumb_line = "`out/thumbnail.png` (Shorts) · `out/thumbnail_16x9.png`" if FMT == "short" else "`out/thumbnail.png` (1280x720, 16:9)"
   # trong f-string:
   **Thumbnail:** {thumb_line}
   ```
   - Lý do: biểu thức hiện nằm trong chuỗi f-string nên bị in ra nguyên văn. Sau khi sửa, kiểm tra lại dòng 2 của out/UPLOAD.md phải là: `**Thumbnail:** \`out/thumbnail.png\` (1280x720, 16:9)`.

VERDICT: CẦN SỬA
