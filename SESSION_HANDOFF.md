# Bàn giao phiên – Studio "Tí Xuyên Sử" (cập nhật 13/11/2026)

Đọc file này + `CLAUDE.md` + `channel/bible.md` trước khi làm tiếp.

## Mục tiêu người dùng
- Kiếm ~20 triệu VNĐ/tháng từ YouTube bằng video AI do Claude Code tự sản xuất. Chỉ dùng công cụ **miễn phí** (không Kling).
- Kênh hiện tại: **lịch sử Việt Nam, phong cách "fun"** (tham khảo kênh Thanh Pahm – @ThanhPahm). Kênh nhà cửa/thiết kế để sau.
- Mỗi khâu phải có **Leader** duyệt (`.claude/agents/leader.md`), tối đa 3 vòng.

## Quy tắc đã chốt
- Mở đầu nói rõ bối cảnh (ai – ở đâu – khi nào). Bản đồ Việt Nam vẽ 34 tỉnh sau 2025; có biển là phải có **QĐ. Hoàng Sa, QĐ. Trường Sa (Việt Nam)**.
- Giọng: edge-tts `vi-VN-NamMinhNeural`, rate `+5%`, pitch `-4Hz` (đã nhanh hơn 15% theo yêu cầu). Cần mạng tới speech.platform.bing.com.
- Mỗi ý (thuế nặng / lao dịch / đồng hoá...) có 1 hình minh hoạ riêng.
- Không đùa lúc có người chết, không miệt thị; lóng tối đa 1–2 câu/tập.
- Không tự đăng YouTube công khai. Không dùng cookie/tài khoản của người dùng khi chưa được đồng ý. Người dùng **không cung cấp** API key Pollinations – đừng hỏi lại.

## Nhân vật (bible mới)
- **Tèo** – cậu bé dẫn chuyện: đầu to, tai vểnh, tóc bát úp có lọn xoăn, răng thỏ, tàn nhang, áo bà ba chàm, khăn đỏ, đồng hồ vàng.
  Mặt mặc định **"blank"**: đơ, mắt trố, con ngươi chấm (người dùng muốn kiểu đơ đơ hài hài). Có chất sơn dầu (filter `oilp`).
- **Tí** – chú **châu chấu** xanh trên vai trái Tèo (bên phải khung hình), `chauchau()`.
- Tên kênh vẫn "Tí Xuyên Sử".

## Công cụ đã có (ai-video-studio/)
| File | Việc |
|---|---|
| `make.py` | pipeline: `--stage tts / art / render / thumb / meta`, `--preview` (storyboard) |
| `studio/cast.py` | dàn nhân vật búp bê trụ: `peg`, `crowd`, `closeup`, `medallion`, `fallen_helmet`, `fallen_flag`, `chauchau`; `python -m studio.cast` → bảng nhân vật |
| `studio/paint.py` | nền sơn dầu tự vẽ `oil(kind,time,seed)` – 8 kind × 5 time; `python -m studio.paint --sheet` |
| `studio/doodle.py` | hiệu ứng fun: `oil_bg`, `doodle_horse`, `nation` (đất nước có mắt), `boom`, `speed_lines`, `flash`, `emoji`, `callout`, `caption_box`, `sign` |
| `studio/svgextra.py` | bản đồ (`map_base/label/arrow/locator`), `bubble`, `troops`, `ribbon_title`... |
| `studio/qa.py`, `studio/asr_check.py` | kiểm tra máy; Vosk nghe lại giọng (WER) |
| `studio/yt_watch.py` | "xem" YouTube: tải video+phụ đề → khung hình + transcript; bị chặn thì lấy tiêu đề + 4 khung hình |

## Các tập
- `episodes/ep002-chi-lang` – tóm tắt dài kiểu EZ Sử, 3:41, Leader 4.1.
- `episodes/ep003-chi-lang-fun` – fun v1 (ảnh thật Wikimedia), 59s, Leader 4.1.
- `episodes/ep004-chi-lang-oil` – **fun v2 (mẫu chuẩn hiện tại)**: nhân vật mới + nền sơn dầu + cận cảnh, 58s, Leader **4.4 ĐẠT**.
  Sinh episode.json bằng `python episodes/ep004-chi-lang-oil/make_episode.py`.

## Hạn chế môi trường
- Máy đám mây bị YouTube chặn ("Sign in to confirm you're not a bot") → chỉ xem được thumbnail/khung hình tự động.
  Mở khoá: chạy `yt_watch.py` trên máy nhà, hoặc người dùng tự đặt `cookies.txt` (tài khoản phụ).
- Không có GPU. Pexels/Unsplash chặn bot; Wikimedia dùng được (thumb 1920px).
- Trang tổng hợp: https://claude.ai/artifact/CxpTRffK5pmWa3YrSCfhaC (video trên trang phải ≤16 MB → nén crf 27).

## Việc tiếp theo (đề xuất)
1. Làm **tập đầy đủ 8–10 phút** theo bộ v2 (series Khởi nghĩa Lam Sơn nhiều tập).
2. Leader còn góp ý nhỏ: chữ chú thích "Tèo (vai: châu chấu Tí)" ở ep004 cảnh 2 bị mũi tên cắt ngang.
3. Thêm nhân vật/nền mới khi kịch bản cần (thêm dòng vào `CAST`, thêm `kind` trong paint.py).

## Khởi động lại môi trường (máy mới)
```
pip install edge-tts piper-tts vosk opencv-contrib-python-headless scipy pillow numpy "yt-dlp[default]"
```
Node + Playwright Chromium có sẵn trên máy đám mây. Model Vosk (`models/vosk-vn`) và Piper (`models/vits-piper-vi_VN-vais1000-medium`)
không nằm trong gói code – tải lại nếu cần (Vosk vosk-model-small-vn-0.4; Piper vi_VN-vais1000-medium).
