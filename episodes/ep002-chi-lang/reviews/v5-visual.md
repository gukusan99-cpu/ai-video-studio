# Leader review – art+render (v5 biểu cảm & bong bóng thoại) – vòng v5
**Điểm:** 4.2/5 (trung bình) · **Kết luận:** ĐẠT

Tiêu chí: Cảm xúc nhân vật rõ 4.5 · Thoại tếu hợp lý/đúng sử/không miệt thị 4.5 · Bong bóng không che chủ thể/phụ đề 4 · Chữ bong bóng đọc được 4.5 · "Trông thực tế" (yêu cầu chủ kênh) 3.5
qa.py --stage render: 6 đạt · 0 cảnh báo · 0 lỗi. Đã xem storyboard, thumbnail, 6 khung final.mp4 (cảnh 2, 8, 10, 11, 15, 19 tại ~85%).

## ✅ Điểm tốt
- Biểu cảm chân dung đọc rõ ngay ở 960px: Liễu Thăng smug→angry (bị nhắm), Mộc Thạnh sweat/scared (cảnh 8, 15), Trần Lựu wink khi giả thua (cảnh 10), Lê Lợi happy ở Bình Ngô đại cáo (cảnh 19). Thumbnail "BẪY RỒI!!" + mặt hoảng của tướng Minh rất mạnh.
- Thoại tếu bám đúng diễn biến: kiêu ngạo khinh địch ("15 vạn quân, dẹp gọn trong một nốt nhạc!", "Mười vạn quân, sợ gì?!"), nhử địch ("Chạy… chạy giả vờ thôi!" vs "ĐUỔI THEO!!"), Xương Giang đã mất ("Ơ… thành mất rồi à?!"), Mộc Thạnh tháo chạy ("CHẠY THÔI!!!"), Vương Thông bị cô lập ("Viện binh đâu hết rồi…"), quân Minh được cấp thuyền ngựa về nước ("Đa tạ! Đa tạ!") – khớp sự kiện Hội thề Đông Quan, giọng nhẹ nhàng, nhân văn.
- Cảnh tử trận (11): không có thoại chế giễu Liễu Thăng; bong bóng "Ơ… lầy quá! PHỤC BINH!!" gán cho đám kỵ binh Minh (đuôi chỉ vào quân), hợp với địa hình lầy lội ở Chi Lăng. Không máu me. Không câu nào miệt thị dân tộc.
- Bong bóng viền đậm, chữ đậm, cỡ 28–36 đọc được; kiểu shout/think phân biệt rõ. Phụ đề không bị bong bóng che ở cả 6 khung.
- Hậu kỳ (vignette, chỉnh màu ấm, hạt phim) làm khung hình có chiều sâu hơn v4, không làm bẩn chữ.

## ⚠️ Cần cải thiện
- Cảnh 15: bong bóng "CHẠY THÔI!!!" (x≈1340,y≈150) chạm/sát chữ "NHÀ MINH" trên bản đồ.
- Cảnh 8: dòng phụ đề "chỉ cần giữ vững, cầm chân…" đè lên mép dưới hai panel ĐÁNH TRƯỚC / CẦM CHÂN (không che mặt nhưng rối).
- Nét mặt lính (charge/panic/smug) quá nhỏ ở cỡ khung toàn cảnh – gần như không thấy cảm xúc của quân, chỉ chân dung mang cảm xúc.
- "Trông thực tế": vẫn là phong cách phẳng hoạt hình; hậu kỳ mới tăng không khí, chưa tăng độ "thật" (bóng đổ, chất liệu). Không chặn, nhưng chưa đáp ứng trọn ý chủ kênh.
- "trong một nốt nhạc" là tiếng lóng hiện đại – chấp nhận được như chất tếu, nhưng nên giữ tối đa 1–2 câu lóng/tập để không lố.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện – không bắt buộc để ĐẠT)
1. episode.json → scenes[14].layers[4].elements[1] (bubble "CHẠY THÔI!!!") – dời sang x≈1420, y≈230 (tx/ty giữ hướng vào Mộc Thạnh) để tách khỏi nhãn "NHÀ MINH".
2. episode.json → scenes[7] (cảnh 8) – hạ đáy hai panel lên ~40px (hoặc thu chiều cao panel) để phụ đề không đè viền panel.
3. Cảnh 10/11 (scenes[9], scenes[10]) – thêm 1 cận cảnh nhỏ (portrait/inset) mặt lính Minh "panic" cạnh bong bóng "Ơ… lầy quá! PHỤC BINH!!" để cảm xúc của quân đọc được; hoặc tăng scale troops ~1.3 ở tiền cảnh.
4. (Tuỳ chọn, hướng "thực tế") svgart/svgextra – thêm bóng đổ mềm dưới người/ngựa và texture giấy/đá nhẹ cho gorge2; giữ phong cách viền #2B1B12.
