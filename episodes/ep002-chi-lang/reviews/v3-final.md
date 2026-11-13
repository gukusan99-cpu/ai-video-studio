# Leader review – v3 (bản cuối) – vòng 1
**Điểm:** 4.3/5 (trung bình) · **Kết luận:** ĐẠT

| Tiêu chí | Điểm |
|---|---|
| Giọng đọc (ASR, nhịp) | 4 |
| Bản đồ / hình (cảnh 12, 16) | 4.5 |
| Dựng (qa máy) | 5 |
| Thumbnail | 3.5 |
| Metadata / chương | 4.5 |

## ✅ Điểm tốt
- qa.py `--stage all`: 134 đạt · 0 cảnh báo · 0 lỗi; 1920x1080, 224.6s, không đoạn đen.
- ASR: WER toàn bài 24.4% (761 từ) – dưới ngưỡng 32% và sát mức nền của mô hình nhỏ (~20%; voice_test 23.7%). Giọng NamMinh −10%/−4Hz đạt yêu cầu.
- 2 câu bị đánh dấu là lỗi do tên riêng/mô hình nhỏ, KHÔNG phải giọng hỏng: số âm tiết máy nghe khớp gần đủ, khung câu vẫn đúng ("quân", "theo đường", "thành"), chỉ sai chữ ở tên riêng/từ Hán Việt:
  - c7 câu 3 (3.91s, 13 từ, 3.32 từ/s): "Mộc Thạnh…vạn…Vân Nam" → "một thành…vài…phân ngầm".
  - c13 câu 1 (2.98s, 12 từ, 4.03 từ/s): "Tàn…cố tiến về…Xương Giang để nương tựa" → "an…của tiếng việt…xuân gian đến đường".
- Cảnh 12: nhãn Phố Cát nằm sát dấu ✕ trận, Cần Trạm/Xương Giang/Đông Quan rõ, có map_locator Hoàng Sa–Trường Sa, phụ đề không che chủ thể.
- Cảnh 16: thành Đông Quan đã nâng lên, nằm gọn trên đường chân trời, nhãn + chân dung Vương Thông không chồng phụ đề.
- UPLOAD.md: 7 chương, mốc 0:00 → 0:33 → 1:08 → 1:31 → 2:04 → 2:46 → 3:20 (đoạn ngắn nhất 23s, cuối 24.6s) – đều ≥10s.

## ⚠️ Cần cải thiện
- Thumbnail: "vệt dấu phẩy" VẪN còn – nguyên nhân không phải seed mà là dấu sắc của chữ "Ắ" (MẮC) mọc lên sát chân dòng trên, nằm giữa "10" và "VẠN" nên đọc thành "10,VẠN". Đổi seed không sửa được.
- Cảnh 13 nhịp nhanh nhất bài (4.03–4.33 từ/s, câu 2 vượt 4.0) – trùng với câu ASR nghe sai nặng nhất.

## 🔧 Yêu cầu sửa (không chặn đăng, nên làm nếu còn thời gian)
1. Thumbnail (khâu thumb, chữ tiêu đề) – tăng khoảng cách dòng giữa "10 VẠN QUÂN" và "MẮC BẪY" ~+25–30px (hoặc ép chữ dòng 2 sang phải để dấu sắc không nằm dưới khe "10 VẠN") – bỏ hẳn hình dấu phẩy.
2. episode.json → cảnh 13 câu 1–2: thêm ngắt nghỉ nhẹ (dấu phẩy sau "Tàn quân Minh") hoặc rate riêng −15% để về ≤4.0 từ/s.
3. (Tuỳ chọn) cảnh 7 câu 3: trường `say` "Mộc Thạnh dẫn năm vạn quân, và một vạn ngựa, theo đường Vân Nam" để tách hai số "vạn".

VERDICT: ĐẠT
