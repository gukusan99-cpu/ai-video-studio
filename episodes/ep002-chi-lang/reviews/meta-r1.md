# Leader review – meta – vòng 1
**Điểm:** 3.8/5 (trung bình) · **Kết luận:** CẦN SỬA

> Video ngang 1920x1080 (175.6 s). Không cần #Shorts, tiêu đề ≤70 ký tự.
> qa.py --stage meta: 6 đạt · 0 cảnh báo · 0 lỗi (tiêu đề 59 ký tự, tag 137/450 ký tự, 4 hashtag, có bình luận ghim, có thumbnail). Lưu ý: dòng "Có bình luận ghim" của qa.py in giá trị rỗng, nhưng episode.json → metadata.pinned_comment có nội dung, và UPLOAD.md cũng có.
> Đã xem: out/UPLOAD.md, out/metadata.json, out/thumbnail.png (1280x720), episode.json → metadata, make_episode.py dòng 215–232.

| Tiêu chí | Điểm | Ghi chú |
|---|---|---|
| Tiêu đề gây tò mò, ≤70 ký tự, có từ khoá | 4 | "Chi Lăng – Xương Giang 1427: 15 vạn quân Minh thua thế nào?" dài 59 ký tự. Từ khoá chính nằm ở đầu, kết bằng câu hỏi gây tò mò. Hai tiêu đề phụ cũng dưới 70 ký tự. |
| Mô tả có tóm tắt + nguồn | 3 | Có tóm tắt, mốc thời gian, CTA, nguồn và câu rào "các nguồn chưa thống nhất". Nhưng câu 2 vẫn còn **đúng lỗi sai chủ thể đã sửa ở khâu script**: "…15 vạn quân Minh… Chỉ khoảng hai tháng sau, **họ** phải thề rút về nước." Video dài ~3 phút nhưng chưa có chương (timestamps). Chưa ghi Bảo tàng Lịch sử Quốc gia, dù fact_check dùng nguồn này cho các mốc ngày. |
| Thumbnail đọc được trên màn hình nhỏ | 4 | Rất tốt: chữ "10 VẠN QUÂN / MẮC BẪY" cỡ lớn, viền đậm, chân dung Liễu Thăng bị gạch X, mũi tên trên bản đồ, Tí có biểu cảm sốc, đúng bible (Mít, đồng hồ, khăn đỏ). Vẫn đọc được khi thu nhỏ còn khoảng 320 px. Điểm trừ nhỏ: thumbnail ghi "10 vạn" còn tiêu đề ghi "15 vạn". Cả hai đều đúng (10 vạn là đạo Liễu Thăng, 15 vạn là tổng viện binh), nhưng người lướt nhanh có thể thấy lệch nhau. Có thể chấp nhận. |
| Hashtag/tag hợp lý | 4 | 4 hashtag đúng chủ đề, 10 tag tiếng Việt có dấu, không spam. Còn thiếu vài cụm người ta hay tìm: "trận xương giang", "ải chi lăng", "lịch sử lớp 7", "khởi nghĩa lam sơn" (dạng hashtag). |
| Thiết lập "dành cho trẻ em" & "nội dung AI" | 4 | madeForKids=false đúng bible. containsSyntheticMedia=false hợp lý, vì đây là hoạt hình vector không giống thật. privacyStatus=private, category 27 (Giáo dục). Nhưng UPLOAD.md ghi thumbnail là "(Shorts)" và trỏ tới `out/thumbnail_16x9.png`, file **không tồn tại** với video ngang. Người đăng thủ công dễ bị nhầm. |

## ✅ Điểm tốt
- Tiêu đề có từ khoá chính + năm ở đầu (tốt cho SEO) và câu hỏi khép mở ở cuối (tốt cho CTR), độ dài vừa màn hình điện thoại.
- Thumbnail có chủ thể rõ (Liễu Thăng bị gạch X), chữ ít mà mạnh, màu cam/đỏ/xanh tương phản tốt. Thương hiệu Tí nằm ở góc trái và không tranh chỗ với chữ.
- Mô tả có câu rào nguồn rất tốt ("một số mốc ngày giữa các nguồn chưa thống nhất…"), có ghi chú "bản đồ dùng đường biên hiện đại", minh bạch và tăng độ tin cậy.
- Bình luận ghim là câu hỏi 3 lựa chọn, dễ kéo người xem bình luận và khớp với CTA trong video (cảnh 20).
- Phần "Kiểm tra sự thật" trong UPLOAD.md đã cập nhật đầy đủ các chỗ sửa của khâu script (Đại Ngu, 7 vạn theo Minh sử, Cần Trạm/Phố Cát, "theo nhiều tài liệu" Nguyễn Trãi).

## ⚠️ Cần cải thiện
- **Lỗi sự thật trong mô tả:** "họ phải thề rút về nước". Chữ "họ" ở đây chỉ 15 vạn viện binh. Thực tế viện binh đã bị diệt hoặc tan rã, còn bên lập hội thề là Vương Thông, tức quân Minh đang bị vây ở Đông Quan. Đây đúng là lỗi đã bị bắt ở script-r1 mục 1, mới sửa trong lời thoại mà chưa sửa trong mô tả.
- **Thiếu chương:** video ngang ~3 phút nên có YouTube chapters. Chương giúp tăng thời gian xem và hiện "key moments" trên Google.
- **UPLOAD.md** ghi nhãn thumbnail sai ("Shorts") và trỏ tới file không có (`thumbnail_16x9.png`). Với video ngang, thumbnail.png 1280x720 chính là ảnh 16:9 cần tải lên.
- Nguồn tham khảo nên thêm Bảo tàng Lịch sử Quốc gia, vì fact_check dùng nguồn này cho ngày 10/10 và thuyết về cái chết của Liễu Thăng.
- (Không bắt buộc) Câu "xem tập mới mỗi tuần" là một lời hứa lịch đăng. Chỉ giữ nếu kênh thực sự đăng hằng tuần.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
> episode.json → metadata được sinh từ `episodes/ep002-chi-lang/make_episode.py` → dict `"metadata"` (dòng 224–232). Hãy sửa ở đó, chạy lại `python3 episodes/ep002-chi-lang/make_episode.py`, rồi chạy `python make.py episodes/ep002-chi-lang --stage meta`.
1. **make_episode.py dòng 227 → metadata["description"], câu thứ 2** – sửa lỗi sai chủ thể (lỗi sự thật):
   - Từ: `Chỉ khoảng hai tháng sau, họ phải thề rút về nước.`
   - Thành: `Chỉ khoảng hai tháng sau, nhà Minh phải thề rút hết quân về nước.`
   - Lý do: viện binh không phải là bên lập hội thề. Câu mới khớp với lời thoại cảnh 1 đã sửa.
2. **make_episode.py dòng 227 → metadata["description"]** – thêm khối chương ngay sau đoạn tóm tắt, thay cho hoặc đặt trước khối "⏱ Mốc chính". Mốc giây lấy từ build/timing.json → start của từng cảnh. Nếu sau này chạy lại tts thì phải tính lại.
   ```
   ⏱ Nội dung:
   0:00 Mở đầu
   0:17 Hai mươi năm đô hộ (1407–1426)
   0:47 Viện binh nhà Minh tràn sang
   0:57 Kế sách: đánh Liễu Thăng trước
   1:04 Ải Chi Lăng – Liễu Thăng tử trận
   1:33 Cần Trạm – Phố Cát
   1:42 Vây diệt ở Xương Giang
   2:10 Hội thề Đông Quan
   2:38 Vì sao nghĩa quân thắng?
   ```
   Các mốc ứng với cảnh 1, 3, 6, 7, 8, 11, 12, 16, 19. Chương đầu phải là 0:00, mỗi chương dài ≥10 s.
   - Lý do: tăng thời gian xem và độ tìm thấy (key moments) cho video ngang.
3. **make_episode.py dòng 227 → metadata["description"], dòng "Tư liệu tham khảo"** – thêm `Bảo tàng Lịch sử Quốc gia;`. Kết quả: `Tư liệu tham khảo: Đại Việt sử ký toàn thư; SGK Lịch sử 7; Bảo tàng Lịch sử Quốc gia; Báo Pháp luật (Hội thề Đông Quan). …`
   - Lý do: đây là nguồn của các mốc ngày đang dùng (fact_check[5]).
4. **make.py dòng 528 (mẫu UPLOAD.md)** – hiện đang cố định `**Thumbnail:** \`out/thumbnail.png\` (Shorts) · \`out/thumbnail_16x9.png\``. Hãy đổi theo `format`:
   - Khi `format == "long"`: ghi `out/thumbnail.png (1280x720, 16:9)` và bỏ tham chiếu tới `thumbnail_16x9.png`.
   - Khi là short: giữ như cũ.
   - Lý do: file thumbnail_16x9.png không được tạo cho video ngang (đó là nhánh thumbnail dọc ở dòng 494–500), nên người đăng tay sẽ bị nhầm.
5. **make_episode.py dòng 228–229 → metadata["hashtags"] / ["tags"]**:
   - hashtags: thêm `"#KhoiNghiaLamSon"` (tổng 5 hashtag).
   - tags: thêm `"trận xương giang"`, `"ải chi lăng"`, `"lịch sử lớp 7"`, `"hội thề đông quan 1427"`. Tổng vẫn dưới 450 ký tự.
   - Lý do: học sinh lớp 7 là nhóm khán giả chính (bible) và thường tìm theo bài học SGK.

VERDICT: CẦN SỬA
