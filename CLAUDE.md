# Studio "Tí Xuyên Sử" – hướng dẫn cho Claude Code

Đây là xưởng sản xuất video YouTube Shorts tự động. Kênh: **Tí Xuyên Sử** – cậu bé Tèo và chú châu chấu Tí
xuyên không về các sự kiện lịch sử Việt Nam, mỗi tập 45–60 giây. Đọc `channel/bible.md` trước khi viết bất cứ gì.

## Khi người dùng nói "làm tập mới về <chủ đề>" – chạy quy trình 6 khâu, mỗi khâu có LEADER duyệt

```
[1 Nghiên cứu+Kịch bản] → Leader → [2 Giọng đọc] → Leader → [3 Hình ảnh] → Leader
   → [4 Dựng video] → Leader → [5 Thumbnail+Metadata] → Leader → [6 Đăng / gói đăng]
```

Vòng lặp duyệt cho MỖI khâu:
1. Claude Code (vai "Sản xuất") làm khâu đó.
2. Gọi subagent **leader** (`.claude/agents/leader.md`) với: tên khâu + thư mục tập.
3. Đọc `episodes/<id>/reviews/<khâu>-rN.md`. Nếu `CẦN SỬA` → thực hiện từng mục "🔧 Yêu cầu sửa", chạy lại khâu, gọi leader vòng N+1.
4. Tối đa **3 vòng**/khâu. Sau vòng 3 vẫn chưa đạt → dừng, báo người dùng các điểm còn tồn đọng.
5. Chỉ chuyển khâu khi `VERDICT: ĐẠT`.

### Khâu 1 – Nghiên cứu & kịch bản
- Tìm dữ kiện bằng WebSearch (≥2 nguồn đáng tin: sách sử, báo chính thống, bảo tàng). Ghi vào `fact_check`.
- Tạo `episodes/epNNN-<slug>/episode.json` theo mẫu `episodes/ep001-bach-dang/episode.json`
  (6–9 cảnh, mỗi cảnh ≤ 9 giây lời, tổng 110–170 từ). Số năm/tên khó đọc → thêm trường `say` viết bằng chữ.
- Từ khoá cần nhấn mạnh trong phụ đề: bọc bằng `*dấu sao*` (hiện màu vàng).
- QA: `python studio/qa.py episodes/<id> --stage script`

### Khâu 2 – Giọng đọc: `python make.py episodes/<id> --stage tts` rồi `python studio/asr_check.py episodes/<id>` (máy "nghe" lại, WER < 32% và không câu nào > 60%; xem channel/voice_test.md)
### Khâu 3 – Hình ảnh: `python make.py episodes/<id> --preview` → Leader xem `out/storyboard.png`
- Hình vẽ bằng các hàm trong `studio/svgart.py` (fn + args trong `layers`). Lớp đầu = nền (tự lia máy), các lớp sau có `motion`:
  `none | bob | jump | drift_left | drift_right | rise | sink | shake | slide_in`. Nền: `bg_motion`: `still | push_up | push_down | left | right`.
- Cần đạo cụ mới (voi chiến, thành luỹ, ngựa...) → thêm hàm mới vào `svgart.py` theo phong cách sẵn có (viền #2B1B12, màu phẳng).
- Muốn dùng ảnh AI miễn phí thay cho cảnh nào: đặt file `episodes/<id>/visuals/scene_NN.png` (khâu art sẽ tự dùng).
### Khâu 4 – Dựng: `python make.py episodes/<id> --stage art && python make.py episodes/<id> --stage render`
### Khâu 5 – Thumbnail & metadata: `python make.py episodes/<id> --stage thumb && python make.py episodes/<id> --stage meta`
### Khâu 6 – Đăng: KHÔNG tự đăng công khai. Chỉ chạy `python upload.py episodes/<id>` khi người dùng yêu cầu
  (mặc định privacy = private để người dùng xem lại rồi tự bấm công khai).

## Video NGANG dạng "tóm tắt nhanh" (format: "long")
- Tham khảo `channel/reference_longform.md` và mẫu `episodes/ep002-chi-lang/` (episode.json sinh từ `make_episode.py`).
- `"format": "long"` → 1920x1080; thêm `"timeline": {start, end, title, ticks}` để có dòng thời gian ở đáy; mỗi cảnh có `year` + `date_label`.
- Đồ hoạ video ngang ở `studio/svgextra.py`: `map_base / map_label / map_arrow / map_tag` (bản đồ thật Natural Earth, view `north`/`front` –
  thêm view mới trong `VIEWS`), `portrait` (chân dung tròn, mark: x/target/captured/flee), `army` (bộ binh/kỵ binh theo màu phe),
  `fortress, camp, gorge, scroll_doc, panel, ribbon_title, number_badge, horse, boat_supply, white_flag, chains`.
- Lớp có `"appear": k` sẽ hiện ra đúng lúc câu thoại thứ k bắt đầu (`appear_delay` giây thêm); motion thêm: `rise_in, from_left, from_right`.
- **BẢN ĐỒ (bắt buộc):** Việt Nam vẽ bằng ranh giới **34 tỉnh thành sau 2025** (`studio/geo/vn/vn34.topo.json`, nguồn Free-GIS-Data);
  mọi cảnh bản đồ có thấy biển phải đặt **`map_locator`** (khung định vị có **QĐ. Hoàng Sa, QĐ. Trường Sa của Việt Nam**) trong một
  LỚP RIÊNG (không đặt trong lớp nền vì nền bị phóng 8% khi lia máy). Nếu hai quần đảo nằm trong khung chính, `map_base` tự vẽ & ghi nhãn.
- Mở đầu video ngang phải nói rõ **bối cảnh: ai – ở đâu – khi nào – đang làm gì** trước khi vào câu hỏi gây tò mò; có `legend` màu phe.
- Cảnh trận đánh dùng bộ v2: `gorge2`, `troops` (side dv/minh, pose spear/bow/sword/charge/mix, cavalry), `arrow_volley`, `dust`, `rocks`, `tree`, `siege_ring`.
- Giọng đọc mặc định: **edge-tts vi-VN-NamMinhNeural** (cần mạng tới speech.platform.bing.com); Piper chỉ dùng khi offline.
- Nội dung chưa thống nhất giữa các nguồn → nói "theo nhiều tài liệu / theo sử Việt". Không máu me.

## Phong cách "fun" (kiểu kênh Thanh Pahm – xem channel/reference_fun_style.md, mẫu episodes/ep003-chi-lang-fun)
- `format: "long"`, KHÔNG có `timeline` (phụ đề tự xuống sát đáy). Đồ hoạ ở `studio/doodle.py`: `dude/mob/doodle_horse` (hình nhộng),
  `nation` (đất nước có mắt – view `asia`, luôn ghi `cn_label="NHÀ MINH"`/tên triều đại để không bị hiểu là nước hiện đại),
  `photo` (ảnh thật Wikimedia, crop bỏ đường/xe/dây điện + `fg_grass`, `mist_band`), `boom`, `speed_lines`, `flash` (+ `hold`), `emoji`, `callout`, `caption_box`, `sign`.
- Lớp có `hold: giây` sẽ tự tắt (chớp sáng/chữ BÙM). Ghi tác giả + giấy phép ảnh trong mô tả.
- Hài nhưng không đùa ngay khoảnh khắc có người chết; mỗi tập tối đa 1–2 câu lóng.

### Bộ v2 (từ ep004): nhân vật búp bê trụ + nền sơn dầu tự vẽ – mẫu `episodes/ep004-chi-lang-oil`
- **Nhân vật** `studio/cast.py` (đã nạp vào doodle): `peg(who, x, y, s, expr, flip, item, label)` – gốc (x,y) = chân; s=1 cao ~290px.
  Dàn sẵn (`CAST`): teo (cậu bé dẫn chuyện, tự có châu chấu Tí trên vai; châu chấu riêng: `chauchau`), leloi, nguyentrai, lelai, tranluu, dv_soldier, peasant, scholar, lieuthang, mocthanh, vuongthong,
  luongminh, hoangphuc, thoitu, minh_soldier. Hero: neutral/smug/angry/grit/shock/scared/sad/laugh/determined/deadpan/sly/cry;
  lính/dân: deadpan/shock/panic/happy/angry/cry/sleepy. item: spear/sword/flag/scroll/fan/bow/torch/hoe.
  Đám đông: `crowd(who, x, y, n, s, gap, rows, exprs)`. Ngựa: `doodle_horse(rider="lieuthang")`.
  Nhân vật mới → thêm 1 dòng vào `CAST` (mặt hero/extra, mũ, kiểu áo robe/tunic/armor/official/peasant, màu, râu) rồi
  `python -m studio.cast` để xem `channel/cast_sheet.png`, `channel/cast_expressions.png`.
- **Nền** `oil_bg(kind, time, seed)` (studio/paint.py, cache ở assets/paint/): kind = karst_valley, gorge, rice_field, river, citadel,
  forest_camp, sea, mountain_pass; time = day, dusk, dawn, night, storm. Đổi `seed` để có biến thể. Xem mẫu: `python -m studio.paint --sheet`.
  Ưu tiên `oil_bg` thay cho ảnh chụp (không cần ghi nguồn ảnh, không lộ chi tiết hiện đại).

## Quy tắc
- Không bịa dữ kiện lịch sử, không xuyên tạc; sự kiện còn tranh cãi thì nói "theo sử sách ghi lại...".
- Mỗi tập phải khác biệt (bối cảnh, đạo cụ, câu hook) – tránh bị YouTube coi là "nội dung lặp lại".
- Không dùng nhân vật/thương hiệu của người khác.
