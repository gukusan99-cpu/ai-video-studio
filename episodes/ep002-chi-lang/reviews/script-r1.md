# Leader review – script – vòng 1
**Điểm:** 3.8/5 (trung bình) · **Kết luận:** CẦN SỬA

> Định dạng: video ngang 16:9, "tóm tắt nhanh lịch sử". Thang Shorts được nới: mỗi cảnh ≤14s, tổng 1.5–20 phút.
> qa.py: 25 đạt · 0 cảnh báo · 0 lỗi (680 từ ≈ 2.6 phút, cảnh dài nhất ≈11.2s, Tí xuất hiện 7/20 cảnh).

| Tiêu chí | Điểm | Ghi chú |
|---|---|---|
| Hook 2 giây đầu | 4 | Có tương phản mạnh (15 vạn quân → 2 tháng sau phải rút) và câu hỏi "Chuyện gì đã xảy ra?". Nhưng 2 giây đầu lại là "Năm 1427" (giọng máy đọc "một nghìn bốn trăm hai mươi bảy" mất khoảng 2s), và câu 2 dùng chủ ngữ "họ" chưa đúng. |
| Đúng sự thật | 3 | Phần lớn đã kiểm chứng đúng. Còn 1 lỗi gọi sai tên nước (1407), 1 câu hook sai chủ thể, và 3–4 chỗ cần rào đón hoặc tách cho đúng (số quân, cách Liễu Thăng chết, nơi Lương Minh/Lý Khánh chết, người soạn văn thề). |
| Nhịp kể / cao trào | 4 | Mạch rõ: bối cảnh → kế sách → Chi Lăng → Cần Trạm/Phố Cát → Xương Giang → Hội thề → bài học 3 điều. Cảnh đều 4–11s. Cao trào Mã Yên hơi "phẳng", và cảnh 14 làm dòng thời gian lùi lại. |
| Lời thoại tự nhiên | 4 | Câu ngắn, dễ đọc bằng giọng máy. Mọi số trong text đều có `say` viết bằng chữ. Có một lỗi ngữ pháp nhỏ ("Các tướng Thôi Tụ…" nhưng chỉ có 1 tướng). |
| CTA cuối | 4 | Câu hỏi mở tốt, có kêu gọi đăng ký. Nhưng lời thoại hỏi "mưu kế nào hay nhất" còn hình lại ghi "TẬP SAU ĐI ĐÂU?", hai thứ không khớp nhau. |

## ✅ Điểm tốt
- **Kiểm chứng đã xác nhận đúng** (đối chiếu nhiều nguồn: Bảo tàng Lịch sử Quốc gia, Tạp chí Quốc phòng toàn dân, SGK Lịch sử 7 qua hoc247/colearn, Wikipedia vi/en, Minh thực lục bản NUS):
  - Liễu Thăng 10 vạn quân, 2 vạn ngựa, đi đường Lạng Sơn; Mộc Thạnh 5 vạn quân, 1 vạn ngựa, đi đường Vân Nam. Đây là số liệu theo *Toàn thư* và SGK.
  - Chủ trương diệt Liễu Thăng trước, cầm chân Mộc Thạnh: đúng.
  - Trần Lựu giả thua, nhử Liễu Thăng vào sâu Chi Lăng: đúng. Liễu Thăng tách đi trước với hơn 100 kỵ binh và chết ở núi Mã Yên (Đảo Mã Pha): đúng.
  - Ngày "10 tháng 10" (tức 20/9 âm lịch Đinh Mùi) được Bảo tàng Lịch sử Quốc gia dùng, kịch bản có rào "theo nhiều tài liệu": ổn.
  - Lương Minh lên thay rồi tử trận, Lý Khánh tự vẫn, các trận phục kích ở Cần Trạm và Phố Cát: đúng.
  - Thành Xương Giang đã bị nghĩa quân hạ trước khi viện binh tới (khoảng 8/9 âm lịch): đúng. Quân Minh đóng trại ngoài đồng, bị vây diệt; Thôi Tụ, Hoàng Phúc bị bắt sống: đúng.
  - Mộc Thạnh nghe tin thì rút chạy, bị truy kích: đúng.
  - Hội thề Đông Quan ngày 10/12/1427: đúng. Lê Lợi cấp thuyền (khoảng 500 chiếc), ngựa, lương thực cho quân Minh về nước: đúng. Quân Minh rút từ 29/12/1427, toán cuối rời đi ngày 3/1/1428, nên "đầu năm 1428 rút hết" là đúng.
  - Câu trích Bình Ngô đại cáo "Như nước Đại Việt ta từ trước, / vốn xưng nền văn hiến đã lâu…" khớp bản dịch Bùi Kỷ quen thuộc.
  - "Khoảng hai tháng" là hợp lý: viện binh vào ải khoảng 8/10, hội thề ngày 10/12.
- Cấu trúc kiểu "EZ Sử" (bản đồ + mũi tên + dòng thời gian + chân dung) hợp với video ngang. Cảnh 19 tổng kết "3 điều" rất tốt cho việc ghi nhớ và bình luận.
- Trường `say` xử lý đủ mọi năm và ngày, không còn chữ số để giọng máy đọc sai.
- Phần mô tả đã ghi nguồn và nói rõ các nguồn lệch nhau về ngày. Đây là điểm cộng cho độ tin cậy.

## ⚠️ Cần cải thiện
- **Cảnh 3:** năm 1407, nước ta mang quốc hiệu **Đại Ngu** (nhà Hồ, 1400–1407), không phải Đại Việt. Nói "nhà Minh chiếm Đại Việt" là sai tên nước.
- **Cảnh 1:** "**họ** phải xin thề rút" khiến người xem hiểu rằng chính 15 vạn viện binh đã thề. Thực tế viện binh đã bị diệt hoặc tan rã; người lập hội thề là Vương Thông, tức quân Minh đang bị vây ở Đông Quan.
- **Số quân:** *Minh sử* chỉ ghi đạo Liễu Thăng khoảng 7 vạn. Nên rào "theo sử Việt" ở cảnh 6. Hook và thumbnail giữ "15 vạn" vẫn được, vì đây là số liệu SGK.
- **Cảnh 10:** về cái chết của Liễu Thăng có 2 thuyết (bị chém, hoặc bị phóng lao đâm). Bible cũng yêu cầu không máu me, nên nói "tử trận" vừa an toàn vừa đúng. Ngoài ra fact_check[5] đang ghi "Wikipedia EN 18/9" như một mâu thuẫn. Thực ra 18/9 là ngày **âm lịch** Liễu Thăng tới Chi Lăng (≈ 8/10 dương lịch), không mâu thuẫn gì. Nên sửa lại ghi chú này.
- **Cảnh 11:** gộp chung khiến người xem tưởng cả hai người chết cùng một chỗ. Theo các nguồn: Lương Minh tử trận ở **Cần Trạm**, Lý Khánh tự vẫn ở **Phố Cát**.
- **Cảnh 16:** việc Nguyễn Trãi soạn văn thề đến từ các bài báo và nghiên cứu, *Toàn thư* không ghi rõ. Nên thêm "theo nhiều tài liệu".
- **Cảnh 14:** `year` = 1427.82 và `date_label` "10/1427" làm dòng thời gian lùi lại sau cảnh 13 (1427.84, "11/1427"). Ming thực lục cho thấy giữa tháng 11 Mộc Thạnh vẫn còn ở biên giới. Gợi ý `year` 1427.86, `date_label` "11/1427".
- **Cảnh 20:** lời thoại hỏi về mưu kế, nhưng hình hiện "TẬP SAU ĐI ĐÂU?". Nên thêm 1 câu ngắn hỏi điểm đến tập sau để khớp với hình (đúng công thức CTA trong bible), hoặc đổi chữ trên hình.
- **Cao trào cảnh 10:** có thể thêm 1 nhịp căng trước câu "quân phục kích ào ra", ví dụ "Bỗng trống trận nổi lên…", để giữ chân người xem ở khoảng giữa video.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
1. **episode.json → scenes[0] (id 1) → narration[0..1]** – Hook: đưa con số lên đầu và sửa chủ ngữ "họ", vì 2 giây đầu cần gây sốc và chủ thể phải đúng.
   - narration[0].text: `*Mười lăm vạn* quân Minh chia hai đường tràn sang Đại Việt, năm *1427*.`
   - narration[0].say: `Mười lăm vạn quân Minh chia hai đường tràn sang Đại Việt, năm một nghìn bốn trăm hai mươi bảy.`
   - narration[1].text: `Chỉ khoảng hai tháng sau, nhà Minh phải *thề rút hết quân về nước*.`
2. **episode.json → scenes[2] (id 3) → narration[0]** – sửa lỗi tên nước (năm 1407 nước ta là Đại Ngu).
   - text: `Năm *1407*, nhà Minh đánh bại nhà Hồ và đặt ách đô hộ lên nước ta.`
   - say: `Năm một nghìn bốn trăm linh bảy, nhà Minh đánh bại nhà Hồ và đặt ách đô hộ lên nước ta.`
   - Đồng thời đổi fact_check[0] thành: `1407: nhà Minh đánh bại nhà Hồ (quốc hiệu Đại Ngu), đặt ách đô hộ (Giao Chỉ) đến 1427.`
3. **episode.json → scenes[5] (id 6) → narration[1]** – rào đón số quân vì Minh sử ghi khác.
   - text: `Theo sử Việt, *Liễu Thăng* dẫn mười vạn quân, hai vạn ngựa, theo đường Lạng Sơn.`
   - Thêm vào cuối fact_check[3]: `; Minh sử ghi đạo Liễu Thăng khoảng 7 vạn.`
4. **episode.json → scenes[9] (id 10) → narration[2] và fact_check[5]** – có 2 thuyết về cái chết và bible không cho phép máu me.
   - narration[2].text: `*Liễu Thăng tử trận* ngay tại chỗ.`
   - (Tuỳ chọn, để tăng cao trào) narration[1].text: `Đến *núi Mã Yên*, trống trận bỗng nổi lên, quân phục kích từ hai bên sườn núi ào ra.`
   - fact_check[5]: `Trần Lựu giả thua nhử địch vào Chi Lăng; 18/9 âm lịch (≈8/10/1427) Liễu Thăng vào ải, 20/9 âm lịch (≈10/10/1427) tử trận ở núi Mã Yên (Đảo Mã Pha) – thuyết bị chém / bị phóng lao (Bảo tàng LSQG).`
5. **episode.json → scenes[10] (id 11) → narration[1..2] và scenes[12] (id 13) → narration[2]** – tách đúng nơi chết của từng người và sửa lỗi ngữ pháp "Các tướng".
   - scenes[10].narration[1].text: `Ở *Cần Trạm*, họ lại bị phục kích, Lương Minh tử trận.`
   - scenes[10].narration[2].text: `Đến *Phố Cát*, thượng thư *Lý Khánh* cùng đường phải tự vẫn.`
   - scenes[12].narration[2].text: `Tướng *Thôi Tụ* và thượng thư *Hoàng Phúc* bị bắt sống.`
6. **episode.json → scenes[15] (id 16) → narration[1] và scenes[19] (id 20) → narration** – rào đón người soạn văn thề và cho CTA khớp với hình "TẬP SAU ĐI ĐÂU?".
   - scenes[15].narration[1].text: `Theo nhiều tài liệu, văn thề do *Nguyễn Trãi* soạn. Quân Minh cam kết *đình chỉ chiến sự* và *rút hết về nước*.`
   - scenes[19]: giữ narration[0], đổi narration[1].text thành `Và tập sau, bạn muốn Tí xuyên không tới đâu? Nhớ *đăng ký kênh* để không bỏ lỡ nhé!`
   - (Kèm theo) scenes[13] (id 14): `year` 1427.86, `date_label` "11/1427" để dòng thời gian không lùi.

Sau khi sửa, chạy lại `python3 studio/qa.py episodes/ep002-chi-lang --stage script` để kiểm tra độ dài cảnh 10, 11 (≤14s) rồi gửi duyệt vòng 2.

VERDICT: CẦN SỬA
