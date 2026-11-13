# Leader review – meta – vòng 3
**Điểm:** 4.3/5 (trung bình) · **Kết luận:** ĐẠT

> qa.py --stage meta: 6 đạt · 0 cảnh báo · 0 lỗi (tiêu đề 59 ký tự, tag 199/450, 5 hashtag, có thumbnail).
> Đã xem: out/UPLOAD.md, out/metadata.json, out/thumbnail.png (1280x720), episode.json (chapters, fact_check), build/timing.json, make.py dòng 578.
> Tổng thời lượng: ffprobe out/final.mp4 = 175.63 s. UPLOAD.md ghi 175.7 s, khớp.

## Yêu cầu vòng 2 → trạng thái
| # | Yêu cầu vòng 2 | Trạng thái | Ghi chú |
|---|---|---|---|
| 1 | Gộp chương để mọi chương ≥ 10 s, chương đầu 0:00 | ✅ Đã xử lý | Còn 7 chương, chương đầu 0:00. Độ dài tính từ timing.json và ffprobe: 0:00 Mở đầu 17.4 s · 0:17 Hai mươi năm đô hộ 30.3 s · 0:47 Viện binh – kế đánh Liễu Thăng trước 17.3 s · 1:04 Ải Chi Lăng 28.4 s · 1:33 Truy kích Cần Trạm – Phố Cát – Xương Giang 36.8 s · 2:10 Hội thề Đông Quan 28.4 s · 2:38 Vì sao nghĩa quân thắng? 17.1 s (đến hết video ở 175.6 s). Chương ngắn nhất dài 17.1 s. Các mốc tăng dần, khớp nhau ở UPLOAD.md và metadata.json. |
| 2 | Dòng Thumbnail không in mã Python | ✅ Đã xử lý | Dòng 4 của UPLOAD.md là `**Thumbnail:** \`out/thumbnail.png\` (1280x720, 16:9)`. make.py dòng 578 đã đưa biểu thức vào `{…}` của f-string, kết quả đúng với FMT=long. |

| Tiêu chí | Điểm | Ghi chú |
|---|---|---|
| Tiêu đề gây tò mò, ≤70 ký tự, có từ khoá | 4 | 59 ký tự, có từ khoá và năm, kết bằng câu hỏi. |
| Mô tả có tóm tắt + nguồn | 4.5 | Tóm tắt đúng sự thật. 7 chương hợp lệ. Mốc chính và nguồn khớp với fact_check. Có câu thận trọng về các mốc ngày chưa thống nhất. |
| Thumbnail đọc được trên màn hình nhỏ | 4 | Chữ to, tương phản tốt. Liễu Thăng bị gạch X. Tí đúng bible: tóc bát úp, áo chàm, khăn đỏ, đồng hồ vàng, có Mít. Con số "10 vạn" đúng với đạo quân Liễu Thăng (fact_check), nhưng hơi lệch với "15 vạn" trên tiêu đề (xem mục Cần cải thiện). |
| Hashtag/tag hợp lý | 4.5 | 5 hashtag, 14 tag, bám theo SGK lớp 7. |
| Thiết lập "dành cho trẻ em" & "nội dung AI" / gói đăng | 4.5 | madeForKids=false, containsSyntheticMedia=false (hình vector), private, category 27, vi. Gói đăng không còn lỗi định dạng. |

## ✅ Điểm tốt
- Cả 2 yêu cầu vòng 2 đã được xử lý đúng, không phát sinh lỗi mới.
- Chương được sinh tự động từ timing.json. Nếu chạy lại TTS, mốc giây sẽ tự cập nhật.
- Đã đối chiếu UPLOAD.md và metadata.json với fact_check: không còn lỗi sai sự thật (15 vạn = 10 + 5 vạn; Liễu Thăng tử trận 10/1427; Hội thề 10/12/1427; 1418 Lam Sơn; 1428 Bình Ngô đại cáo).
- metadata.json và UPLOAD.md nhất quán: tiêu đề, mô tả, tag và bình luận ghim giống nhau.

## ⚠️ Cần cải thiện
Các mục dưới đây không chặn việc đăng.
- Thumbnail ghi "10 VẠN QUÂN MẮC BẪY" (đạo quân Liễu Thăng), còn tiêu đề 1 ghi "15 vạn quân Minh". Cả hai đều đúng sự thật. Nếu muốn nhất quán, có thể chọn tiêu đề 3 ("Vì sao Liễu Thăng mất mạng ở ải Chi Lăng?") để đi cùng thumbnail này.
- qa.py: check "Có bình luận ghim" vẫn in giá trị rỗng. Đây là lỗi hiển thị của qa.py, nội dung thật thì có.
- Chỉ nên giữ câu "xem tập mới mỗi tuần" nếu kênh thật sự đăng hằng tuần.
- Cho các tập sau: make.py có thể tự gộp chương dưới 10 s và in cảnh báo khi gộp.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
Không có yêu cầu bắt buộc. Khâu meta đạt và có thể chuyển sang khâu 6 (gói đăng, mặc định private).

VERDICT: ĐẠT
