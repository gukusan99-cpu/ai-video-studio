# 🎬 Studio "Tí Xuyên Sử" – xưởng làm YouTube Shorts tự động, 0 đồng

Kênh hoạt hình lịch sử Việt Nam: cậu bé **Tí** và chú thạch sùng **Mít** xuyên không về các sự kiện có thật.
Toàn bộ hình ảnh, giọng đọc, dựng phim, thumbnail, tiêu đề do Claude Code làm; có **Leader** duyệt sau mỗi khâu.

## Cấu trúc thư mục
```
ai-video-studio/
├─ CLAUDE.md               ← quy trình cho Claude Code (6 khâu + Leader)
├─ .claude/agents/leader.md← vai Leader: chấm điểm, nhận xét, yêu cầu sửa
├─ make.py                 ← dây chuyền: tts → art → render → thumb → meta
├─ upload.py               ← đăng YouTube qua API (chạy trên máy bạn)
├─ studio/
│  ├─ svgart.py            ← thư viện vẽ: nhân vật Tí, thuyền, cọc, núi, sông, lính...
│  ├─ qa.py                ← bộ kiểm tra tự động cho Leader
│  ├─ rasterize.*          ← SVG → PNG (Chromium)
│  └─ config.json          ← giọng đọc, phụ đề, fps
├─ channel/                ← bible.md (nhận diện kênh), ideas.md (40 ý tưởng), character_sheet.png
├─ assets/fonts, assets/music (bỏ nhạc nền .mp3 không bản quyền vào đây)
├─ models/                 ← giọng đọc tiếng Việt offline (Piper)
└─ episodes/ep001-bach-dang/
   ├─ episode.json         ← kịch bản + bố cục cảnh + metadata (FILE DUY NHẤT cần viết cho mỗi tập)
   ├─ visuals/             ← (tuỳ chọn) ảnh AI tự tạo: scene_01.png ... sẽ thay hình vẽ vector
   ├─ reviews/             ← nhận xét của Leader từng vòng
   └─ out/  final.mp4 · thumbnail.png · UPLOAD.md · metadata.json · storyboard.png
```

## Cài đặt trên máy của bạn (Windows/Mac)
1. Cài Python 3.11+, Node.js 18+, ffmpeg.
2. Trong thư mục studio:
   ```bash
   pip install piper-tts soundfile numpy pillow edge-tts google-api-python-client google-auth-oauthlib
   ```
   ```bash
   npm install playwright && npx playwright install chromium
   ```
3. Tải giọng đọc tiếng Việt (1 lần, ~60MB):
   ```bash
   mkdir -p models && curl -L https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-vi_VN-vais1000-medium.tar.bz2 | tar xj -C models
   ```
4. Mở Claude Code tại thư mục này và gõ: **"Làm tập mới về trận Chi Lăng"**. Claude sẽ tự đi hết 6 khâu, có Leader duyệt.

Hoặc chạy tay:
```bash
python make.py episodes/ep001-bach-dang
```
```bash
python studio/qa.py episodes/ep001-bach-dang --stage all
```

## Giọng đọc
- Mặc định **Piper** (offline, miễn phí, giọng nữ miền Bắc vais1000).
- Giọng hay hơn, vẫn miễn phí: **edge-tts** (giọng Microsoft `vi-VN-NamMinhNeural` / `vi-VN-HoaiMyNeural`, cần internet).
  Sửa `studio/config.json` → `"engine": "edge"` hoặc trong episode.json → `"voice": {"engine": "edge"}`.
- Tốt nhất cho kênh lâu dài: **tự thu giọng thật** – đặt file `build/audio/sNN_lK.wav` rồi chạy từ khâu render.

## Ảnh đẹp hơn mà vẫn miễn phí (tuỳ chọn)
Hình vector của studio đã dùng được ngay. Nếu muốn ảnh "phim hoạt hình 3D", tạo ảnh miễn phí trên web rồi bỏ vào `visuals/scene_NN.png`:
| Công cụ | Miễn phí | Ghi chú |
|---|---|---|
| Google Gemini (gemini.google.com) / Google AI Studio | Có, giới hạn theo ngày | Tải `channel/character_sheet.png` lên làm ảnh tham chiếu → nhân vật giữ nguyên khá tốt |
| Microsoft Bing Image Creator / Designer | Có | Dán "mô tả khoá" nhân vật trong bible.md |
| Meta AI, Ideogram, Leonardo (token miễn phí hằng ngày) | Có | Tương tự |
| Stable Diffusion / ComfyUI / Fooocus chạy trên máy | Hoàn toàn miễn phí | Cần card NVIDIA ≥ 8GB VRAM |
Mỗi cảnh đều có sẵn `image_prompt` trong episode.json để copy.

## Đăng YouTube
- Thủ công: mở `out/UPLOAD.md`, copy tiêu đề/mô tả/tag vào YouTube Studio.
- Tự động: làm theo hướng dẫn đầu file `upload.py` (tạo OAuth client trên Google Cloud, lưu `secrets/client_secret.json`).
  Video luôn đăng ở chế độ **riêng tư** trước để bạn xem lại.
