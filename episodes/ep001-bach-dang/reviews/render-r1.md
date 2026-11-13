# Leader review – render – vòng 1
**Điểm:** 4.0/5 (trung bình) · **Kết luận:** ĐẠT

Chấm từng tiêu chí: Chuyển động mượt, không giật/đen **4** · Phụ đề dễ đọc, không che mặt nhân vật **3** · Âm thanh khớp hình **4** · Tổng ≤ 60s **5**
qa.py: 6 đạt · 0 cảnh báo · 0 lỗi. Kiểm tra thêm bằng ffmpeg: không có khung đứng hình > 1.5s (freezedetect), không có khoảng lặng > 0.4s (silencedetect), loudness tích hợp −15.4 LUFS, các điểm cắt cảnh (5.27s, 12.63s, 17.5s, 30.17s, 35.07s, 41.93s, 50.33s) khớp đúng `start` trong `build/timing.json`.

## ✅ Điểm tốt
- 54.0s, 1080x1920, 30fps: nằm gọn trong chuẩn Shorts, vẫn còn 6s dư nếu cần thêm nhịp.
- Không có màn hình đen, không đứng hình; cảnh nào cũng có lớp chuyển động (bob, drift, shake, jump, rise), nhìn có sức sống.
- Hình cắt đúng lúc giọng đọc sang cảnh mới, phụ đề chạy theo lời nên âm và hình khớp nhau.
- Phụ đề Be Vietnam Pro ExtraBold 76px, viền dày, có hiệu ứng pop, từ khoá tô vàng (1288, Hưng Đạo Vương Trần Quốc Tuấn, thuỷ triều rút, Ô Mã Nhi): đọc tốt trên điện thoại. Trong mọi khung đã xem, phụ đề (đáy chữ ở y≈1420) không đè lên mặt Tí.
- Giọng đọc rõ, âm lượng đều (−15.4 LUFS, gần mức −14 của YouTube).

## ⚠️ Cần cải thiện
- **Cảnh 8 (≈42–50s):** phụ đề đè thẳng lên biển tên "CỌC BẠCH ĐẰNG" của tủ trưng bày, hai lớp chữ chồng nhau thành rối (xem khung 44s). Đây là chỗ xấu nhất của video.
- **Mẩu phụ đề lóe quá nhanh:** "Bắc." chỉ hiện 0.16s (14.74–14.90). Tên riêng bị cắt đôi qua hai mẩu: "Hưng Đạo Vương Trần / Quốc Tuấn", "Ô Mã / Nhi", "trận / thuỷ chiến lừng lẫy nhất". Người xem bị vấp mắt.
- **Phụ đề đè lên thân Tí** ở cảnh 3, 5, 6 và 9 (Tí đặt ở y 1340–1500). Mặt không bị che, nhưng chữ vẫn cắt ngang ngực hoặc chân. Ở cảnh 6, chữ "lủng đáy" đè lên thân Tí.
- **Không có nhạc nền hay hiệu ứng âm thanh:** `music.file` rỗng và `assets/music/` trống, nên cả 54s chỉ có giọng đọc trên nền im. Cảnh cao trào 6 (thuyền vỡ, rung lắc) không có tiếng nào, cảm xúc tụt và khả năng giữ chân người xem giảm.
- Các cảnh nối nhau bằng cắt cứng. Chấp nhận được với Shorts, nhưng riêng chỗ chuyển 5→6 ("Rồi thuỷ triều rút") nên có nhấn (rung hoặc chớp sáng) để đẩy cao trào.

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
1. `make.py` → `chunk_words()`: nếu mẩu cuối của một câu chỉ còn 1 từ, gộp nó vào mẩu trước (có thể vượt `max_chars` tối đa +6); và không cắt giữa cụm từ khoá đang bọc `*…*` nếu cụm đó ≤ 5 từ. Lý do: bỏ mẩu "Bắc." 0.16s và các tên riêng bị cắt đôi (Ô Mã Nhi, Trần Quốc Tuấn).
2. `episode.json` → `scenes[7].layers[0]` (cảnh 8, `museum_room`): dời biển tên/tủ trưng bày lên trên vùng phụ đề (đáy biển tên ≤ y 1250). Nếu `museum_room` không có tham số thì thêm arg `plaque_y` trong `studio/svgart.py`. Một cách khác là thêm override `sub_margin_v: 300` cho riêng cảnh 8. Lý do: phụ đề đang chồng lên chữ "CỌC BẠCH ĐẰNG".
3. Thêm 1 file nhạc nền không bản quyền (YouTube Audio Library, nhạc dân tộc hoặc phiêu lưu nhẹ) vào `assets/music/` hoặc khai báo ở `episode.json → music.file`, giữ `volume: 0.12`. `make.py` đã có sẵn sidechain để nhạc tự hạ khi có lời. Lý do: nền im làm giảm cảm xúc và khả năng giữ chân người xem.
4. (Nên làm) Thêm SFX "rắc/ùm" ở đầu cảnh 6 (≈30.2s) và 31.3s khi thuyền mắc cọc, trộn ở mức −12 dB so với giọng đọc. Lý do: cảnh cao trào hiện không có âm thanh hỗ trợ.
5. (Nên làm) `episode.json` → `scenes[2].layers[2].elements[0]` (Tí cảnh 3, y 1340), `scenes[5].layers[2].elements[1]` (Tí cảnh 6, y 1420) và `scenes[8].layers[1].elements[0]` (Tí cảnh 9, y 1420): nâng y lên khoảng 80–120px, hoặc đặt Tí lệch hẳn sang mép để dải phụ đề ở giữa (y 1330–1420) không cắt ngang người Tí.

Ghi chú cho khâu art (không tính vào điểm render): ở cảnh 3, Tí đang đứng giữa mặt nước (chân chìm trong sông, sau khóm sậy), sai yêu cầu logic vật lý. Mít đang ngồi trên vai TRÁI của Tí (phía phải khung hình), trong khi bible ghi vai phải. Đề nghị kiểm tra lại hàm `ti()` trong `svgart.py` ở tập sau.

VERDICT: ĐẠT
