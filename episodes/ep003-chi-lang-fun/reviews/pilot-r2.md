# Leader review – pilot (render+meta, phong cách "fun") – vòng 2
**Điểm:** 4.1/5 (r1: 3.5) · **Kết luận:** CẦN SỬA (nhỏ – 2 lỗi bản đồ, sửa nhanh)

Chấm: Vui/hiệu ứng 4.5 · Dễ hiểu 4 · Tôn trọng 4.5 · Đúng sử 4.5 · Bản đồ HS/TS 3 · Chữ không bị che 4.5 · Ảnh thật sạch chi tiết hiện đại 4.5
Kiểm trên out/final.mp4 (59.1s): khung ~75% mỗi cảnh (8.22/16.54/24.13/32.26/37.49/43.08/48.35/56.76s) + cảnh 6 tại 38.65/39.55/44.5s; thumbnail; UPLOAD.md. Lỗi độ dài/hook của qa.py được miễn (bản thử).

## Yêu cầu r1 → trạng thái
| # | Yêu cầu r1 | Trạng thái | Ghi chú |
|---|---|---|---|
| 1 | Bỏ đường/xe/lan can (bg3, thumbnail), dây/cột điện (bg6) | ✅ Đạt | Thumbnail sạch (núi + cỏ), cảnh 3/4/7 không còn dây/cột điện. |
| 2 | Hạ phụ đề, không đè nhân vật/callout | ✅ Đạt | Sub nằm trên dải cỏ đáy; cảnh 2,4,5,7 không đè người/ngựa; callout "Lối đi hẹp, lầy" lên y≈270/540, tách khỏi sub. |
| 3 | Tách nhãn HS/TS; "Nhà Minh", Đông Quan, Chi Lăng, mũi tên viện binh; bỏ 😎 chồng mặt VN | ⚠️ Một phần | Đã có nhãn NHÀ MINH, chấm Đông Quan/Chi Lăng, mũi tên "15 vạn viện binh"; 😎 trên mặt VN đã bỏ (cảnh 8). NHƯNG: nhãn "QĐ. Hoàng Sa (Việt Nam)" giờ nằm TRÊN ĐẤT LIỀN miền Trung (x≈330–500,y≈355 khung 960) – lệch trái khỏi cụm đảo (x≈535) → dễ hiểu nhầm vị trí; cảnh 8 nhân vật Tí che nhãn Trường Sa thành "QĐ. Trường Sa (Việt N…". |
| 4 | Cảnh 3 đoàn quân hàng một + "kẹt xe thế kỷ 15" | ✅ Đạt | Hàng 12 lính + nhãn vàng "Kẹt xe thế kỷ 15" + emoji 🫠. |
| 5 | Mỗi cảnh ≥1 punch; cảnh 5 biển "Mã Yên →" + bong bóng Liễu Thăng | ✅ Đạt (gần đủ) | Cảnh 2 bong bóng "Chưa nghe bao giờ" + 😏, cảnh 4 "Diễn xuất 3/10 · Độ tin 10/10" + "(diễn đó)", cảnh 5 biển gỗ + "Ta đi trước…", cảnh 7 Tí "Còn căng hơn nữa!". Chưa thấy zoom-in nhanh vào mặt (không bắt buộc). |
| 6 | Bỏ 😱 ở câu "tử trận" | ✅ Đạt | 😱 chỉ ở "Trống trận nổi lên!" (39.55s); từ 43.08s đến cuối cảnh chỉ chân dung + dấu X, không emoji. |

## ✅ Điểm tốt
- Mật độ meme tăng rõ, đúng chất kênh tham khảo; flash trắng "TÙNG TÙNG!" ở 38.65s là chủ ý, 1s sau đã rõ cảnh phục binh.
- Thumbnail mới sạch, chữ to "LIỄU THĂNG MẮC LỪA", bố cục rõ.
- UPLOAD.md ghi nguồn ảnh đủ (tác giả, giấy phép CC BY-SA 3.0 / PD, Wikimedia Commons) + nguồn bản đồ.

## ⚠️ Cần cải thiện (nhỏ)
- Đuôi bong bóng thoại (cảnh 1, 2) xuyên qua emoji 😎/😏 → hơi rối; dời emoji ra khỏi đường đuôi.
- UPLOAD.md ghi "hình hoạt hình vẽ vector" trong khi nền là ảnh chụp thật → sửa câu cho đúng (khai AI vẫn là "Không").

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
1. [scenes[0] & scenes[7] → nhãn Hoàng Sa] – đặt nhãn "QĐ. Hoàng Sa (Việt Nam)" NGOÀI BIỂN, sát bên phải/trên cụm đảo (không đè đất liền) – vì nhãn chủ quyền nằm trên đất liền dễ gây hiểu nhầm vị trí.
2. [scenes[7] → vị trí Tí hoặc nhãn Trường Sa] – dời Tí sang phải/xuống hoặc dời nhãn Trường Sa sang trái để hiện đủ "QĐ. Trường Sa (Việt Nam)" – vì nhãn chủ quyền không được bị che.
3. (tuỳ chọn) [scenes[0], scenes[1]] – dời emoji khỏi đuôi bong bóng; [UPLOAD.md] sửa câu "vẽ vector" thành "hoạt hình trên nền ảnh chụp thật".

VERDICT: CẦN SỬA
