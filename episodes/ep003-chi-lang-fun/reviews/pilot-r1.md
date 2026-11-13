# Leader review – pilot (render+meta, phong cách "fun") – vòng 1
**Điểm:** 3.5/5 (trung bình) · **Kết luận:** CẦN SỬA

Chấm: Vui/hiệu ứng 4 · Dễ hiểu 3.5 · Tôn trọng 4 · Đúng sử 4.5 · Bản đồ HS/TS 3.5 · Chữ không bị che 2.5 · Ảnh thật sạch chi tiết hiện đại 2.5
qa.py: 57 đạt · 0 cảnh báo · 3 lỗi – cả 3 thuộc diện được miễn cho bản thử (độ dài kịch bản ngang, hook ≤14 từ, thời lượng 59.1s).

## ✅ Điểm tốt
- Đúng tinh thần kênh tham khảo: đất nước có mắt/cảm xúc (Minh 😎 → khóc, VN "Ở... thử xem"), nền ảnh thật núi đá Chi Lăng, nhân vật hình nhộng, bong bóng thoại, emoji, speed lines, chữ "TÙNG TÙNG!", flash, nhãn "Liễu Thăng · tự tin 200%", "Tình hình: hơi bị toang".
- Mở đầu nói rõ ai–ở đâu–khi nào–đang làm gì (1427, Lê Lợi, Đông Quan = Hà Nội) như chủ kênh yêu cầu; CTA cuối có câu hỏi dự đoán.
- Đúng sử: 15 vạn (Liễu Thăng 10 vạn), Liễu Thăng khinh địch, Trần Lựu giả thua, hơn 100 kỵ binh, tử trận ở Mã Yên – khớp fact_check, không bịa số.
- Cảnh tử trận xử lý nhẹ nhàng: chân dung + dấu X, không máu; lời đọc trung tính "tử trận ngay tại chỗ".
- Bản đồ cảnh 1 và 8 có QĐ. Hoàng Sa, QĐ. Trường Sa (Việt Nam).

## ⚠️ Cần cải thiện
- **Chi tiết hiện đại lộ ra:** thumbnail có đường cao tốc + xe khách + lan can ở đáy (ảnh bg3); cảnh 4 và 7 (bg6) thấy dây điện chạy ngang và cột điện bên trái (~x140,y880 khung 1080p).
- **Phụ đề đè lên nhân vật:** dòng sub ở y≈880/1080 rơi đúng vào vùng ngựa/lính đứng (cảnh 2, 4, 5, 7) và đè callout "Lối đi hẹp, lầy" + emoji ở cảnh 3.
- **Nhãn HS/TS chồng nhau:** "QĐ. Hoàng Sa (Việt Nam)" bị nhãn Trường Sa che mất nửa dưới (cảnh 1, 8).
- Cảnh 8: emoji 😎 đặt chồng lên mặt VN (mặt đã đeo kính) → rối, che miền Bắc. Bản đồ chưa đánh dấu Đông Quan/Chi Lăng và mũi tên viện binh → người xem khó hình dung đường hành quân.
- Cảnh 3 kể "phải đi thành hàng dài" nhưng không có hình đoàn quân xếp hàng; cảnh 5 nền xám, trống, ít trò.
- Tôn trọng: mặt "nước Trung Quốc hiện đại" khóc lóc, không ghi "Nhà Minh" → dễ bị hiểu là chế giễu quốc gia hiện nay; nên gắn nhãn triều đại.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
1. [make_episode.py → ảnh nền bg3 (cảnh 3, 6, thumbnail) và bg6 (cảnh 4, 7)] – crop bỏ phần đáy chứa đường/xe/lan can (crop y ≤ 0.6) và che dây/cột điện bằng `mist_band`/`fg_grass` cao hơn hoặc đổi ảnh khác; thumbnail đổi `crop` thành [0,0,1,0.6] hoặc dùng bg2 – vì lộ xe khách, dây điện phá cảm giác thế kỷ 15.
2. [subs.ass / cấu hình phụ đề format long] – hạ phụ đề xuống dải đáy y≈1000–1040 có nền mờ, hoặc nâng nhân vật/đám lính lên y≤820; tránh đè callout cảnh 3 (dời callout "Lối đi hẹp" lên y≈700) – vì chữ đè mặt nhân vật làm khó đọc và khó xem.
3. [scenes[0] & scenes[7] → map_base/map_locator] – tách 2 nhãn Hoàng Sa/Trường Sa (đặt Hoàng Sa phía trên-trái, Trường Sa phía dưới, không chồng); thêm `map_label` "Nhà Minh" lên lãnh thổ đỏ, chấm "Đông Quan" và "Chi Lăng" + `map_arrow` viện binh từ Bắc xuống; bỏ emoji 😎 chồng lên mặt VN ở cảnh 8.
4. [scenes[2] terrain] – thêm `troops`/`mob` xếp hàng một chui qua khe núi (dùng `gorge2` hoặc mob n=10 rows=1 nhỏ dần), kèm chữ nhỏ "kẹt xe thế kỷ 15" – để hình khớp lời và thêm một miếng hài.
5. [toàn tập – nhịp hiệu ứng] – mỗi cảnh thêm ≥1 "punch": zoom-in nhanh vào mặt khi có câu đùa (cảnh 2 "như… không có", cảnh 4 "diễn hơi lố"), sticker reaction tỉnh bơ của Tí, freeze-frame + nhãn; cảnh 5 thêm biển gỗ "Mã Yên →" và bong bóng tự tin của Liễu Thăng – để đạt mật độ meme như kênh tham khảo.
6. [scenes[5] ambush] – giữ dấu X nhưng thay 😱 cạnh câu "tử trận" bằng không emoji (hoặc chỉ giữ ở câu "Trống trận nổi lên") – tránh đùa ngay khoảnh khắc có người chết.

VERDICT: CẦN SỬA
