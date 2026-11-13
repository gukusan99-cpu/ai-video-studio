# Leader review – meta – vòng 1
**Điểm:** 4.2/5 (trung bình) · **Kết luận:** ĐẠT

Chấm từng tiêu chí: Tiêu đề gây tò mò, ≤70 ký tự, có từ khoá **4** · Mô tả có tóm tắt + nguồn **4** · Thumbnail đọc được trên màn hình nhỏ **4** · Hashtag/tag hợp lý **4** · Thiết lập "dành cho trẻ em" & "nội dung AI" **5**
qa.py: 7 đạt · 0 cảnh báo · 0 lỗi. Đã đối chiếu với `fact_check` và không thấy lỗi sai sự thật trong tiêu đề, mô tả hay bình luận ghim.

## ✅ Điểm tốt
- Tiêu đề dạng câu hỏi "Vì sao…?" đúng lời hứa của kênh trong bible, có từ khoá chính "quân Nguyên", "sông Bạch Đằng", dài 69 ký tự (≤70).
- Mô tả mở bằng 1 câu giới thiệu, có 4 gạch đầu dòng tóm tắt đúng với `fact_check`, có lời kêu gọi bình luận và đăng ký, ghi nguồn (Đại Việt sử ký toàn thư, khảo cổ bãi cọc Quảng Yên) và có câu "Hình ảnh minh hoạ mang tính tái hiện".
- Thumbnail: chữ "BẪY CỌC / BẠCH ĐẰNG" rất to, tương phản mạnh (trắng và vàng, viền đen), vẫn đọc được ở cỡ thu nhỏ. Mặt Tí to, biểu cảm sốc, có thuyền vỡ và cọc làm bối cảnh. Tí đúng bible: tóc bát úp, áo chàm, khăn đỏ, đồng hồ vàng phát sáng, có Mít.
- 10 tag đúng chủ đề (138/450 ký tự), có cả biến thể tên "trần hưng đạo" và "trần quốc tuấn". 4 hashtag, có #Shorts.
- Thiết lập đúng: `made_for_kids: false` khớp bible (khán giả phổ thông). Nội dung AI ghi "không bắt buộc" vì là hình vector hoạt hình, không giống thật, đúng chính sách nhãn nội dung tổng hợp của YouTube. Danh mục Giáo dục (27).
- Bình luận ghim đưa 3 lựa chọn cụ thể nên dễ kéo người xem bình luận, đồng thời gợi ý tập sau.

## ⚠️ Cần cải thiện
- Tiêu đề: "🌊 #Shorts" chiếm 10/69 ký tự mà gần như không có tác dụng (#Shorts đã có trong hashtag, `qa.py` cũng chấp nhận nếu nằm ở hashtag). Tiêu đề lại thiếu năm "1288", từ khoá hay được tìm cùng "Bạch Đằng".
- Thumbnail "trả lời trước" câu hỏi của tiêu đề: tiêu đề hỏi "Vì sao vỡ tan?" thì thumbnail đã ghi "BẪY CỌC". Dòng phụ "Quân Nguyên thua vì đâu?" lặp lại ý của tiêu đề. Dải y≈650–900 của thumbnail là trời tối trống, phí diện tích.
- Hashtag mới có 4. Có thể thêm 1–2 cái về nhân vật lịch sử (#TranHungDao) để tăng khả năng được tìm thấy.
- Mô tả ghi "Đăng ký kênh để đi xuyên lịch sử Việt **mỗi ngày**", trong khi bible đặt lịch 4–5 Shorts/tuần, nên hứa quá mức. Phần nguồn còn chung chung: nên ghi kỷ (Bản kỷ, Kỷ nhà Trần) hoặc nêu tên Bảo tàng Quảng Ninh.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
1. `episode.json → metadata.title`: đổi thành `"Vì sao thuyền quân Nguyên vỡ tan trên sông Bạch Đằng năm 1288? 🌊"` (64 ký tự). #Shorts vẫn giữ trong `hashtags` nên qa vẫn đạt. Lý do: thêm từ khoá "1288" và hiện đủ tiêu đề trên điện thoại.
2. `episode.json → thumbnail.sub`: đổi thành câu không lặp tiêu đề mà tạo cú sốc, ví dụ `"Cả đoàn thuyền giặc tan tành!"` hoặc `"Thuỷ triều là vũ khí?!"`. Lý do: thumbnail và tiêu đề nên bổ sung cho nhau thay vì nói cùng một câu.
3. `episode.json → metadata.description`: thay "mỗi ngày" bằng "mỗi tuần". Đổi dòng nguồn thành "Tư liệu tham khảo: Đại Việt sử ký toàn thư (Kỷ nhà Trần); hiện vật cọc Bạch Đằng tại Bảo tàng Quảng Ninh và bãi cọc Yên Giang, Đồng Má Ngựa (Quảng Yên)." Lý do: không hứa quá lịch đăng, nguồn cụ thể hơn và tăng độ tin cậy.
4. `episode.json → metadata.hashtags`: thêm `"#TranHungDao"` (tổng 5, vẫn trong khoảng 3–8). `metadata.tags`: thêm `"ô mã nhi"` và `"bạch đằng giang"`. Lý do: phủ thêm các từ khoá tìm kiếm về nhân vật.
5. (Tuỳ chọn) Trong `make.py`, ở khâu thumb, nâng cụm chữ tiêu đề xuống khoảng 80–120px, hoặc phóng cảnh nền để thuyền vỡ lấp dải trời trống y 650–900. Lý do: tận dụng diện tích khi thumbnail bị thu nhỏ.

VERDICT: ĐẠT
