# Leader review – render – vòng 2
**Điểm:** 4.5/5 (trung bình) · **Kết luận:** ĐẠT

> Định dạng: video ngang 1920x1080, "tóm tắt nhanh". Tiêu chí "Tổng ≤ 60s" được thay bằng "đúng thời lượng mục tiêu ~2:56".
> qa.py --stage render: 6 đạt · 0 cảnh báo · 0 lỗi (1920x1080, 175.6 s, 13.4 MB, 1 track âm thanh, không có đoạn đen).
> Đã xem 14 khung của final.mp4 mới: 0.05 · 0.5 · 40 · 52 · 65.0 · 65.3 · 82.3 · 86 · 91 · 96 · 98.5 · 101.5 · 170 · 174 s.
> build/subs.ass: 91 dòng (vòng 1 có 108 dòng). Có **0 dòng dưới 0.8 s**, dòng ngắn nhất 0.81 s. Đã đối chiếu 57 từ khoá `*…*` trong episode.json: **không từ khoá nào bị cắt đôi**.
> Timing không đổi so với vòng 1 (chỉ đổi hình), nên phần âm thanh vẫn giữ kết quả đo ở vòng 1 (−15 LUFS, true peak −0.8 dBFS).

## Yêu cầu vòng 1 → trạng thái
| # | Yêu cầu vòng 1 | Trạng thái | Bằng chứng |
|---|---|---|---|
| 1 | Cảnh 11: tách nhãn và chân dung, cho hiện theo đúng từng câu | ✅ Đã xử lý | Ở 96 s chưa có nhãn hay chân dung. Ở 98.5 s có nhãn Cần Trạm và chân dung Lương Minh bị gạch X, đúng lúc nói "Lương Minh tử trận". Ở 101.5 s nhãn Phố Cát hiện ra, chân dung Lý Khánh mờ dần vào đúng câu "tự vẫn". |
| 2 | Cảnh 8 và 10: đưa biển tên ra khỏi lớp nền đang có chuyển động | ✅ Đã xử lý | Khung 65.0, 65.3 và 82.3 s đều thấy trọn biển "ẢI CHI LĂNG · LẠNG SƠN" và "NÚI MÃ YÊN". |
| 3 | Cảnh 10: kỵ binh lên y=700 | ✅ Đã xử lý | Ở 86 s và 91 s, đoàn kỵ binh nằm trọn trên dòng phụ đề. |
| 4 | Cảnh 5: bỏ chữ ĐẠI VIỆT trên bản đồ (hoặc dời nhãn) | ✅ Đã xử lý | Ở 40 s, nhãn "Đông Quan (Hà Nội)" và "Tốt Động" hiện rõ, không còn đè lên chữ nào. |
| 5 | chunk_words: không cắt từ khoá, gộp đuôi ≤2 từ, không tách sau dấu phẩy nếu phần còn lại ≤2 từ | ✅ Đã xử lý | 0 dòng dưới 0.8 s (vòng 1 có 17 dòng). Các chỗ "chiến thắng Chi Lăng – Xương Giang", "của nhà Minh.", "sang Đại Việt, năm 1427." đã liền một dòng. |
| 6 | Cảnh 20: Tí nhỏ lại, lên cao hơn, thêm portal | ✅ Đã xử lý | Ở 170 s và 174 s, Tí đứng gọn trong portal, phụ đề CTA nằm ở vùng trống bên dưới. |
| (nhỏ) | Cảnh 1: con trỏ dòng thời gian đứng yên | ✅ Đã xử lý | Ở 0.05 s và 0.5 s, con trỏ đã nằm ở 10/1427, khớp với nhãn. |
| (nhỏ) | Cảnh 6: map_tag chạm viền chân dung | ✅ Đã xử lý | Ở 52 s, thẻ "10 vạn quân · 2 vạn ngựa" cách xa chân dung Liễu Thăng. |

| Tiêu chí | Điểm | Ghi chú |
|---|---|---|
| Chuyển động mượt, không giật/đen | 4.5 | Biển tên không còn bị cắt. Chuyển cảnh sạch, con trỏ dòng thời gian không còn chạy vô lý ở cảnh mở đầu. |
| Phụ đề dễ đọc, không che mặt | 4 | Không còn dòng nháy, không còn từ khoá bị cắt đôi, không đè lên chủ thể ở cảnh 10 và cảnh 20. Còn 2 chỗ tên riêng bị tách qua 2 dòng (xem phần Cần cải thiện). |
| Âm thanh khớp hình | 4.5 | Cảnh 11 đã khớp từng câu. Cảnh 10 vẫn đúng như vòng 1 (phục binh trượt vào, Liễu Thăng bị gạch X đúng câu nói). |
| Thời lượng | 5 | 175.6 s, đúng mục tiêu. |

## ✅ Điểm tốt
- Đã xử lý cả 6 yêu cầu bắt buộc và 2 điểm nhỏ của vòng 1. Sửa đúng chỗ, không làm hỏng cảnh khác.
- Phụ đề gọn hơn hẳn: từ 108 dòng còn 91 dòng, không còn dòng nào nháy qua quá nhanh. Mắt người xem đọc thoải mái hơn.
- Cảnh 11 giờ kể lại theo đúng trình tự Chi Lăng → Cần Trạm (Lương Minh) → Phố Cát (Lý Khánh), khớp với phần đã sửa ở khâu script.
- Cảnh CTA (20) thoáng, cân đối: portal làm khung cho Tí, chữ "đăng ký kênh" tô vàng nổi rõ.

## ⚠️ Cần cải thiện (không chặn đăng – áp dụng cho tập sau)
- **Tên riêng bị tách qua 2 dòng**, gặp 2 chỗ: 0:27.9 "…khởi nghĩa ở Lam \| Sơn, Thanh Hoá." và 0:42.0 "…rút vào thành Đông \| Quan, tức Hà Nội…". Nguyên nhân là chunk_words mới chỉ giữ liền cụm `*…*`. Đề xuất cho make.py: không ngắt giữa 2 tiếng liền nhau mà cả hai đều viết hoa chữ đầu. Cách khác là cho phép đánh dấu cụm không được tách, ví dụ dùng dấu cách không ngắt `Lam Sơn`.
- **Cảnh 11 (~100–103 s):** nhãn "Phố Cát" (dx=−150) rơi ngay trên biểu tượng thành của Xương Giang, còn nhãn "Xương Giang" lại nằm dưới dấu ⊗ Phố Cát. Người xem kỹ có thể nhầm thành nào là thành nào. Gợi ý: cho Phố Cát `dx=170, dy=-10` (đặt bên phải như Cần Trạm), hoặc đổi Xương Giang thành `dy=60`. Ngoài ra, sau khi lia sang trái, chấm "Lạng Sơn" bị mũi tên che mất.
- **Cảnh 6 (~52 s):** đầu mũi tên Liễu Thăng chạm vào nhãn "Đông Quan" (dy=−56). Mũi tên này nên dừng ở Chi Lăng, còn nhãn Đông Quan nên có dy dương.
- UPLOAD.md ghi 175.7 s, qa.py ghi 175.6 s. Lệch là do làm tròn, không cần sửa.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
Không có yêu cầu bắt buộc. Các điểm ở phần "Cần cải thiện" là tuỳ chọn. Nếu sửa cảnh 11 hoặc cảnh 6 thì chỉ cần chạy lại `--stage art` và `--stage render`, không ảnh hưởng tts.

VERDICT: ĐẠT
