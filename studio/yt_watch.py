""""Xem" một video YouTube để tham khảo: khung hình + lời thoại → thư mục channel/watch/<id>/.

    python studio/yt_watch.py <link> [--every 6] [--cookies cookies.txt]

1. Thử tải bản 480p + phụ đề tiếng Việt (tự động/thủ công) bằng yt-dlp.
   → contact sheet (1 khung / N giây, có mốc thời gian) + transcript.txt (từ phụ đề, hoặc Vosk nghe lại nếu không có phụ đề).
2. Nếu YouTube chặn máy (lỗi "Sign in to confirm you're not a bot" trên máy chủ đám mây):
   → lấy tiêu đề (oEmbed) + thumbnail + 3 khung hình tự động của YouTube (maxres1..3) → sheet.jpg.
   Muốn xem đủ: chạy trên máy nhà, hoặc tự đặt cookies.txt (tài khoản phụ) và thêm --cookies.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def vid_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
    return m.group(1) if m else url


def fetch(url: str, out: Path) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            out.write_bytes(r.read())
        return out.stat().st_size > 2000
    except Exception:
        return False


def tile(images: list[Path], out: Path, labels: list[str], cols: int = 4, w: int = 480):
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert("RGB") for p in images]
    h = int(w * 9 / 16)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "black")
    d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(ims, labels)):
        x, y = (i % cols) * w, (i // cols) * h
        sheet.paste(im.resize((w, h)), (x, y))
        d.rectangle([x, y, x + 9 * len(lab) + 10, y + 22], fill="black")
        d.text((x + 5, y + 4), lab, fill="white")
    sheet.save(out, quality=88)


def vtt_to_text(vtt: Path) -> str:
    lines, last = [], ""
    stamp = ""
    for ln in vtt.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "-->" in ln:
            stamp = ln.split(".")[0]
            continue
        t = re.sub(r"<[^>]+>", "", ln).strip()
        if not t or t == last or t.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        lines.append(f"[{stamp}] {t}")
        last = t
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--every", type=float, default=6.0, help="giây giữa 2 khung hình")
    ap.add_argument("--cookies", default="")
    a = ap.parse_args()
    vid = vid_id(a.url)
    out = ROOT / "channel" / "watch" / vid
    out.mkdir(parents=True, exist_ok=True)
    info = {}
    try:
        with urllib.request.urlopen(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json", timeout=30) as r:
            info = json.load(r)
    except Exception:
        pass
    print("🎬", info.get("title", vid), "–", info.get("author_name", ""))
    base = ["yt-dlp", "--no-playlist", "-o", str(out / "video.%(ext)s")]
    if a.cookies:
        base += ["--cookies", a.cookies]
    cmd = base + ["-f", "bv*[height<=480]+ba/b[height<=480]/b", "--merge-output-format", "mp4",
                  "--write-subs", "--write-auto-subs", "--sub-langs", "vi.*,vi,en.*", "--sub-format", "vtt",
                  f"https://www.youtube.com/watch?v={vid}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    video = next(iter(out.glob("video.mp4")), None)
    if r.returncode == 0 and video:
        frames = out / "frames"
        frames.mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video), "-vf", f"fps=1/{a.every},scale=480:-1",
                        str(frames / "f%04d.jpg")], check=True)
        fs = sorted(frames.glob("f*.jpg"))
        for k in range(0, len(fs), 24):  # mỗi sheet 24 khung
            part = fs[k:k + 24]
            labels = [f"{int((k + i) * a.every // 60)}:{int((k + i) * a.every % 60):02d}" for i in range(len(part))]
            tile(part, out / f"sheet_{k // 24 + 1:02d}.jpg", labels)
        subs = sorted(out.glob("video*.vtt"))
        if subs:
            (out / "transcript.txt").write_text(vtt_to_text(subs[0]), encoding="utf-8")
        else:  # nghe lại bằng Vosk (offline)
            wav = out / "audio.wav"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video), "-ac", "1", "-ar", "16000", str(wav)], check=True)
            try:
                from vosk import KaldiRecognizer, Model
                import wave
                rec = KaldiRecognizer(Model(str(ROOT / "models" / "vosk-vn")), 16000)
                wf = wave.open(str(wav))
                txt = []
                while True:
                    data = wf.readframes(16000 * 5)
                    if not data:
                        break
                    if rec.AcceptWaveform(data):
                        txt.append(json.loads(rec.Result()).get("text", ""))
                txt.append(json.loads(rec.FinalResult()).get("text", ""))
                (out / "transcript.txt").write_text("\n".join(t for t in txt if t), encoding="utf-8")
            except Exception as e:
                print("   (không nghe lại được:", e, ")")
        print(f"✅ Đã xem đủ: {len(fs)} khung hình, sheet_*.jpg, transcript.txt → {out}")
        return
    err = re.findall(r"ERROR: (.{0,120})", r.stderr)
    print("⚠️  Không tải được video:", err[0] if err else r.stderr[-200:])
    got = [p for p in (out / f"{n}.jpg" for n in ("maxresdefault", "maxres1", "maxres2", "maxres3"))
           if fetch(f"https://i.ytimg.com/vi/{vid}/{p.stem}.jpg", p)]
    if got:
        tile(got, out / "sheet.jpg", [p.stem for p in got], cols=2, w=960)
    (out / "info.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"↩️  Chế độ dự phòng: tiêu đề + {len(got)} ảnh → {out / 'sheet.jpg'}")
    print("   Muốn xem đầy đủ: chạy lệnh này trên máy nhà, hoặc thêm --cookies cookies.txt (tài khoản phụ).")
    sys.exit(2)


if __name__ == "__main__":
    main()
