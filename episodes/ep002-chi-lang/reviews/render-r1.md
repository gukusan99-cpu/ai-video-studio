# Leader review – render – vòng 1
**Điểm:** 3.9/5 (trung bình) · **Kết luận:** CẦN SỬA

> Định dạng: video ngang 1920x1080, "tóm tắt nhanh". Tiêu chí "Tổng ≤ 60s" được thay bằng "đúng thời lượng mục tiêu ~2:56 và trong khoảng 1.5–20 phút".
> qa.py --stage render: 6 đạt · 0 cảnh báo · 0 lỗi (1920x1080, 30fps, 175.6s, 13.4 MB, 1 track âm thanh, không có đoạn đen).
> Đã xem: out/review_frames.png, out/storyboard.png và 22 khung trích thêm (0.05 · 0.3 · 0.5 · 2.5 · 9.35 · 40 · 47.6 · 50 · 65.3 · 70 · 73.5 · 86 · 90 · 97 · 100 · 115 · 132 · 136 · 162 · 171 · 174 · 175.4 s). Đã đọc build/subs.ass (108 dòng) và build/timing.json.
> Âm thanh: Integrated −15.0 LUFS · True peak −0.8 dBFS · LRA 1.4 LU. Độ to ngắn hạn mỗi 5 giây nằm trong khoảng −14.4 đến −16.6 LUFS. silencedetect (−45 dB, 0.8 s) trên final.mp4 không thấy đoạn im lặng nào. Giọng đọc không có khoảng lặng nào dài quá 1.2 s.

| Tiêu chí | Điểm | Ghi chú |
|---|---|---|
| Chuyển động mượt, không giật/đen | 4 | Lia máy, rise_in, from_left/right đều mượt, chuyển cảnh sạch (ví dụ 47.6 s). Có fade-in rất ngắn ở 0 s. Lỗi: ở cảnh 8, biển "ẢI CHI LĂNG · LẠNG SƠN" bị cắt mất nửa trên ở mép khung trong khoảng 1–2 giây đầu, vì nằm trong lớp nền có `push_down`. |
| Phụ đề dễ đọc, không che mặt | 3 | Phụ đề ExtraBold 62, viền dày, nằm ngay trên dải dòng thời gian (MarginV 175), từ khoá tô vàng rõ, không che mặt nhân vật nào. Nhưng cách ngắt dòng còn kém: 17/108 dòng hiện dưới 0.8 s ("năm 1427." 0.59 s, "nhà Minh." 0.45 s, "Theo sử Việt," 0.67 s…), và từ khoá bị cắt đôi ("…tóm tắt nhanh chiến \| thắng Chi Lăng – Xương Giang"). Ở cảnh 10, phụ đề đè lên chính đoàn kỵ binh của Liễu Thăng. Ở cảnh 20, phụ đề đè lên thân và chân Tí. |
| Âm thanh khớp hình | 3.5 | Âm lượng rất đều, đạt chuẩn YouTube, nhạc không lấn giọng. Phụ đề khớp từng câu thoại. Nhưng ở cảnh 11, hình đi trước lời: chân dung Lương Minh có dấu X chỉ hiện ở câu 3 (câu nói về Phố Cát), muộn một câu so với lời "Lương Minh tử trận". Còn Lý Khánh thì đã bị gạch X ngay khi vừa nói "Đến Phố Cát", trước khi nghe tới "tự vẫn". |
| Thời lượng | 5 | 175.6 s, đúng mục tiêu ~2:56. Không cảnh nào quá 11.6 s. |

## ✅ Điểm tốt
- Hook 0–9 s đúng như kịch bản đã sửa: bản đồ, 2 mũi tên Mộc Thạnh/Liễu Thăng và phụ đề "Mười lăm vạn" tô vàng hiện ngay từ giây đầu.
- Dải dòng thời gian ở đáy hoạt động đúng. Mốc chạy tiến dần: 1407 → 1418 → cuối 1426 → 10/1427 → 11/1427 → 10/12/1427 → 1/1428 → 1428, không còn lùi lại như vòng script. Ở cảnh 2 và 20 dải được ẩn hợp lý.
- Phụ đề không bao giờ đè lên dải dòng thời gian, các dòng không chồng nhau và không có khoảng hở nào dài quá 1 s.
- Cảnh 13 (Xương Giang): hai cánh quân nghĩa quân hai bên, trại Minh ở giữa, phụ đề nằm gọn khoảng trống giữa hai cánh. Bố cục tốt.
- Cảnh 16 (Hội thề): cuộn văn thề ở giữa, Lê Lợi và Vương Thông hai bên, Nguyễn Trãi hiện đúng lúc câu "văn thề do Nguyễn Trãi soạn". Phụ đề nằm trong vùng trống dưới cuộn.
- Cảnh 19: ba thẻ hiện lần lượt theo lời "Một / Hai / Ba". Cách này giữ chân người xem tốt.
- Cảnh 10: hai cánh phục binh trượt vào đúng câu "quân phục kích ào ra", chân dung Liễu Thăng có dấu X hiện đúng câu "Liễu Thăng tử trận". Không có máu me.
- Tí đúng bible ở mọi cảnh có mặt: tóc bát úp, áo chàm, khăn đỏ, đồng hồ vàng, Mít trên vai.
- Âm thanh: −15 LUFS, true peak −0.8 dBFS, LRA 1.4. Không clip, không đoạn câm.

## ⚠️ Cần cải thiện
- **Cảnh 5 (36.0–47.6 s):** nhãn "Đông Quan (Hà Nội)" (dy=−56) đè lên chữ "ĐẠI VIỆT" của bản đồ, đọc thành "ĐẠI V[Đông Quan]IỆT". Dấu ⊗ Tốt Động cũng nằm sát ngay đó.
- **Cảnh 8 (64.9–74.9 s):** `map_tag` "ẢI CHI LĂNG · LẠNG SƠN" (y=90) nằm trong lớp `bg` có `bg_motion="push_down"`, nên bị cắt ở mép trên lúc mở cảnh (xem khung 65.3 s và review_frames). Đây lại là cảnh mở màn trận Chi Lăng.
- **Cảnh 10 (82.2–93.3 s):** đoàn kỵ binh `cav` (y=790, 2 hàng) có chân nằm đúng vùng phụ đề (y≈880–910). Câu "Liễu Thăng dẫn hơn một trăm kỵ binh đi trước" đè lên chính chủ thể đang được nói tới.
- **Cảnh 11 (93.3–103.0 s):** hai chân dung có dấu X dùng chung `appear=2`, nên lệch với lời như đã nêu ở bảng điểm. Hai nhãn Cần Trạm và Phố Cát cũng hiện cùng lúc (`appear=1`), trong khi lời nhắc tới từng nơi lần lượt.
- **Ngắt phụ đề (make.py → chunk_words):** dòng lẻ quá ngắn (dưới 0.8 s) và từ khoá bị cắt đôi qua 2 dòng làm mắt người xem phải nhảy liên tục. Lỗi rõ nhất ở 0:12.87 ("chiến \| thắng"), 0:16.37 ("nhà Minh." 0.45 s), 0:03.63 ("năm 1427." 0.59 s).
- **Cảnh 20 (167.3–175.6 s):** Tí (y=1010, s=1.05) chiếm cả vùng đáy, phụ đề đè lên bụng và chân Tí. Không che mặt, nhưng nhìn rối, và đồng hồ vàng/Mít nằm sát dòng chữ.
- (Nhỏ, không bắt buộc) Ở cảnh 1, con trỏ dòng thời gian chạy từ khoảng 1407 tới 10/1427 trong khoảng 2 s đầu, nhưng nhãn đã ghi sẵn "10/1427" (khung 0.3 s và 0.5 s). Nên cho con trỏ đứng yên ở cảnh đầu, hoặc để nhãn đổi theo vị trí con trỏ.
- (Nhỏ) Ở cảnh 6, đuôi `map_tag` "10 vạn quân · 2 vạn ngựa" (x=1370) chạm viền chân dung Liễu Thăng (x=1700, r=95).

## 🔧 Yêu cầu sửa (cho Claude Code thực hiện)
> episode.json được sinh từ `episodes/ep002-chi-lang/make_episode.py`. Hãy sửa trong file .py, chạy lại `python3 episodes/ep002-chi-lang/make_episode.py`, rồi chạy lại `--stage art` và `--stage render`. Các mục 1–4 và 6 chỉ đổi hình, không ảnh hưởng tts/timing.
1. **make_episode.py → scenes id=11 (dòng ~118–121) → layers "hits" và "p"**: tách thành các lớp theo đúng câu thoại.
   - `L("hit1", [map_label Cần Trạm …], appear=1, motion="rise_in")`
   - `L("hit2", [map_label Phố Cát …], appear=2, motion="rise_in")`
   - `L("p1", [portrait luongminh, mark="x"], appear=1, appear_delay=1.6, motion="rise_in")`, để dấu X hiện cùng lúc nói "Lương Minh tử trận".
   - `L("p2", [portrait lykhanh, mark="x"], appear=2, appear_delay=1.8, motion="rise_in")`, để dấu X hiện cùng lúc nói "tự vẫn".
   - Lý do: hình phải khớp lời (Lương Minh chết ở Cần Trạm, Lý Khánh ở Phố Cát). Đây cũng là chỗ khâu script đã sửa để người xem không hiểu lầm.
2. **make_episode.py → scenes id=8 (dòng ~88) → layers[0] "bg"**: bỏ `E("map_tag", text="ẢI CHI LĂNG · LẠNG SƠN", …)` khỏi lớp bg và đưa sang lớp riêng: `L("tag", [E("map_tag", text="ẢI CHI LĂNG · LẠNG SƠN", x=960, y=100, size=44, fill="#2B1B12")], motion="none")`. Cách khác là đổi `bg_motion` thành `"still"`. Lý do: biển tên bị cắt ở mép trên trong 1–2 s đầu cảnh. Kiểm tra cả cảnh id=10 ("NÚI MÃ YÊN", bg `push_up`) và áp dụng cách tương tự cho chắc.
3. **make_episode.py → scenes id=10 (dòng ~103) → layer "cav"**: `army(x=790, y=790, …)` → `y=700`. Vẫn nằm trên nền thung lũng (floor=600). Lý do: kỵ binh của Liễu Thăng đang bị phụ đề đè lên. Sau khi sửa, kiểm tra khung ở 86 s.
4. **make_episode.py → scenes id=5 (dòng ~59–61)**: trong layers[0], đổi `map_base(... vn_label="ĐẠI VIỆT")` thành `vn_label=""` (cảnh 1 và cảnh 3 đã giới thiệu tên nước). Nếu muốn giữ tên nước, đổi `map_label Đông Quan` thành `dy=60` và `map_label Tốt Động` thành `dx=-150, dy=90`. Lý do: nhãn đang đè lên chữ ĐẠI VIỆT.
5. **make.py → chunk_words() (dòng 292–321) và lời gọi ở dòng 349 `chunk_words(ln["text"], 10, 46)`** (mã dựng chung, cần sửa để đạt):
   - (a) Không ngắt dòng khi đang ở giữa cặp `*…*`, trừ khi chính từ khoá đó dài hơn max_chars.
   - (b) Gộp đuôi khi chunk cuối có ≤ 2 từ (hiện chỉ gộp khi đuôi có 1 từ) và tổng ≤ max_chars + 8.
   - (c) Không tách chunk sau dấu phẩy nếu phần còn lại của câu có ≤ 2 từ.
   - Kết quả cần đạt: không còn dòng nào dưới 0.8 s. Các dòng "chiến \| thắng", "của \| nhà Minh.", "Đại Việt, \| năm 1427." phải liền trên một dòng.
   - Kiểm tra lại bằng cách đếm trong build/subs.ass.
6. **make_episode.py → scenes id=20 (dòng ~189) → layer "ti"**: `ti(x=960, y=1010, s=1.05)` → `y=900, s=0.9`. Có thể thêm `portal(cy=430, r=330)` cho cân. Lý do: phụ đề cuối (CTA đăng ký kênh) đang đè lên thân và chân Tí. Cảnh CTA cần chữ thoáng để người xem đọc kịp.

VERDICT: CẦN SỬA
