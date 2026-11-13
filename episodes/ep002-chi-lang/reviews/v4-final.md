# Leader review – v4 (bản cuối, chỉ sửa âm thanh + thumbnail) – vòng 1
**Điểm:** 4.5/5 (trung bình) · **Kết luận:** ĐẠT

| Tiêu chí | Điểm |
|---|---|
| Giọng đọc (ASR, nhịp) | 4 |
| Bản đồ / hình (không đổi so với v3) | 4.5 |
| Dựng (qa máy) | 5 |
| Thumbnail | 4.5 |
| Metadata / chương (không đổi) | 4.5 |

## ✅ Điểm tốt
- qa.py `--stage all`: 134 đạt · 0 cảnh báo · 0 lỗi.
- ASR: WER 24.5% (v3: 24.4%) – dưới ngưỡng 32%, sát nền mô hình (~20%; voice_test vòng 2 vẫn giữ NamMinh −10%/−4Hz = 23.7%). Số câu bị đánh dấu giảm 2 → 1.
- c13 câu 1 (có dấu phẩy trong `say` + rate −16%) không còn bị đánh dấu: 3.96s, 12 từ = 3.03 từ/s (v3: 4.03).
- c7 câu 3 ("và một vạn ngựa") không còn bị đánh dấu; 3.21 từ/s.
- Câu bị đánh dấu duy nhất – c7 câu 2 (WER 0.71, 5.08s, 3.15 từ/s): máy nghe "theo sự việc liệu thanh vẫn mười vạn quân và hay và ngừa heo rừng làm sân". Khung câu và số âm tiết khớp ("theo sử Việt"→"theo sự việc", "mười vạn quân", "và", "ngựa", "theo đường"), chỉ sai tên riêng Liễu Thăng/Lạng Sơn và "hai vạn" → **lỗi tên riêng của mô hình nhỏ, KHÔNG phải giọng hỏng**. Dù 71% vượt ngưỡng 60%/câu, nguyên nhân là tên riêng nên không chặn.
- Thumbnail: dòng "10 VẠN QUÂN" / "MẮC BẪY" đã giãn, dấu sắc chữ Ắ không còn chạm chân dòng trên → hết vệt dấu phẩy, đọc rõ trên màn nhỏ.

## ⚠️ Cần cải thiện
- c13 câu 2 dù đã −16% vẫn 4.06 từ/s (2.46s/10 từ; v3 4.33), câu 3 4.03 từ/s (không đặt rate) – vượt nhẹ trần 4.0.
- c7 câu 2 vượt ngưỡng 60%/câu của asr_check về mặt máy; cần ghi chú ngoại lệ tên riêng để lần sau không bị hiểu nhầm là lỗi.

## 🔧 Yêu cầu sửa (không chặn đăng)
1. episode.json → cảnh 13 câu 2–3: thêm `say` có dấu phẩy ("Nhưng thành này, đã bị nghĩa quân hạ từ trước." / "Họ đành đóng trại, giữa cánh đồng trống.") và rate −16% cho câu 3.
2. (Tuỳ chọn) c7 câu 2: thêm ngắt "Theo sử Việt, Liễu Thăng, dẫn mười vạn quân…" để tên riêng tách bạch hơn.

VERDICT: ĐẠT
