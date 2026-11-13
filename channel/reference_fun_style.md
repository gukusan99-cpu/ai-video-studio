# Phong cách "fun" – tham khảo kênh Thanh Pahm (@ThanhPahm)

Đã xem: danh sách 40 video gần nhất (lượt xem, thời lượng) + thumbnail và 3 khung hình tự động của 9 video
(Pháp – Đại Nam ×2, Bồ Đào Nha chiến ký, Hải chiến Cannanore, Thế chiến 1, Hitler, Thế chiến 2, Tân Thế Giới, Leonardo da Vinci).
Không tải được video/phụ đề: YouTube yêu cầu đăng nhập (chặn robot) với máy chủ đám mây.

## Số liệu
- Lịch sử thế giới/Việt Nam: 2–15 triệu lượt/video (World War 1: 14 Tr; Hitler: 15 Tr; Pháp – Nam Kỳ: 8,7 Tr).
- Làm **series nhiều tập** ("Ấn Độ Du Ký" 11 tập, 1,6–3,7 Tr/tập), video dài 8–60 phút.

## Công thức hình ảnh
1. Nhân vật **hình nhộng** (thân trụ, đầu to), nét vẽ tay, **mắt lờ đờ tỉnh bơ** – hài vì vô cảm.
2. **Ghép mặt/ảnh chân dung thật** lên thân hoạt hình; ảnh tư liệu đen trắng.
3. **Đất nước có mắt và cảm xúc** (bản đồ Việt Nam/Pháp có mắt giận, cầm vũ khí).
4. **Nền ảnh chụp thật** (sa mạc, rừng, lâu đài) + nhân vật vẽ.
5. Hiệu ứng: lửa/khói/nổ, ánh sáng lóe, rung, ô video lồng.
6. Meme & pop culture, emoji, gân tức, trái tim, chữ chú thích nhỏ cà khịa.
7. Người dẫn (biếm hoạ chủ kênh) phản ứng ở góc.
8. Thumbnail: ảnh ghép đông, chữ trắng viền đen rất to, mặt nhân vật tức/hoảng.

## Bản của Tí Xuyên Sử (không sao chép nhân vật/người dẫn của kênh khác)
| Yếu tố | Công cụ trong studio |
|---|---|
| Nhân vật hình nhộng, nét rung tay | `doodle.dude`, `doodle.mob`, `doodle.doodle_horse` (bộ lọc SVG turbulence) |
| Đất nước có cảm xúc | `doodle.nation` (view `asia`, luôn kèm nhãn QĐ. Hoàng Sa, QĐ. Trường Sa) |
| Ảnh thật | `doodle.photo` (Wikimedia Commons – ghi tác giả & giấy phép trong mô tả) + `fg_grass`, `mist_band` che chi tiết hiện đại |
| Hiệu ứng | `boom` (TÙNG TÙNG!/BÙM!), `speed_lines`, `flash` (+ `hold` để chỉ lóe 0,15s), `emoji`, `callout`, `caption_box`, motion `shake` |
| Người dẫn | Tí ở góc, bong bóng tỉnh bơ |

Thoại: câu ngắn, giọng kể dí dỏm (“tin sái cổ”, “rối như canh hẹ”, “hơi bị toang”), nhưng **không chế giễu cái chết, không miệt thị dân tộc**, sự kiện đúng sử.
Ảnh mặt người thật: chỉ dùng tranh/ảnh phạm vi công cộng hoặc giấy phép tự do; không dùng ảnh người nổi tiếng hiện đại (quyền hình ảnh).

## Cập nhật – xem thêm "Vasco Viễn Chinh | Ấn Độ Du Ký – Tập 10" (thumbnail + 3 khung hình tự động)
- Nhân vật là **khối trụ như búp bê gỗ, không tay**; áo vẽ trên thân (nút, đai, viền), đổ bóng hình trụ.
- Nhân vật chính: mặt **bán tả thực** (râu đánh bóng từng sợi, lông mày rậm, nghiến răng, mắt có tròng); lính: mặt chấm đơn giản.
- Mũ to, nhiều chi tiết, có điểm sáng. Nền **vẽ tay kiểu tranh màu** có nét mực, màu trầm (không phải ảnh chụp).
- Studio đáp lại bằng `studio/cast.py` (dàn nhân vật Lam Sơn tự thiết kế) + `studio/paint.py` (nền sơn dầu tự vẽ).

## Xem YouTube đầy đủ (video + phụ đề)
Máy chủ đám mây bị YouTube chặn ("Sign in to confirm you're not a bot") – chỉ lấy được tiêu đề (oEmbed), danh sách video,
thumbnail và 3 khung hình tự động. Hai cách mở khoá:
1. Chạy studio trên máy của bạn (IP nhà, không bị chặn): `yt-dlp --write-auto-subs --sub-langs vi -f "bv*[height<=720]" <link>`.
2. Hoặc xuất cookie YouTube (tiện ích "Get cookies.txt LOCALLY") thành `cookies.txt` và **tự tay** đặt vào máy, rồi dùng
   `yt-dlp --cookies cookies.txt ...`. Cookie = quyền đăng nhập tài khoản → chỉ dùng tài khoản phụ, xoá file sau khi dùng.
