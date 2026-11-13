#!/usr/bin/env python3
"""Leader "nghe" giọng đọc bằng máy: nhận dạng lại từng câu (Vosk tiếng Việt, offline) và đo tỷ lệ lỗi từ (WER).
WER thấp = giọng rõ chữ. Mô hình nhỏ nên có sai số nền ~20%; dùng để SO SÁNH và bắt câu bị đọc hỏng (WER > 60%).

    python studio/asr_check.py episodes/ep002-chi-lang
Cài: pip install --no-deps vosk ; mô hình: models/vosk-vn (vosk-model-small-vn-0.4 từ alphacephei.com)
"""
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm(t: str) -> list[str]:
    return " ".join(re.sub(r"[^\w\s]", " ", t.lower()).split()).split()


def lev(a, b) -> int:
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


def main() -> None:
    from vosk import KaldiRecognizer, Model, SetLogLevel
    SetLogLevel(-1)
    ep_dir = ROOT / sys.argv[1]
    ep = json.loads((ep_dir / "episode.json").read_text(encoding="utf-8"))
    timing = json.loads((ep_dir / "build" / "timing.json").read_text())
    says = {s["id"]: [l.get("say") or l["text"].replace("*", "") for l in s["narration"]] for s in ep["scenes"]}
    model = Model(str(ROOT / "models" / "vosk-vn"))
    tot_e = tot_w = 0
    bad = []
    with tempfile.TemporaryDirectory() as td:
        for t in timing:
            for i, ln in enumerate(t["lines"]):
                w16 = Path(td) / "a.wav"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ln["file"], "-ar", "16000", "-ac", "1", str(w16)], check=True)
                wf = wave.open(str(w16))
                rec = KaldiRecognizer(model, 16000)
                while True:
                    data = wf.readframes(4000)
                    if not data:
                        break
                    rec.AcceptWaveform(data)
                hyp = json.loads(rec.FinalResult()).get("text", "")
                ref = norm(says[t["scene"]][i])
                e = lev(ref, norm(hyp))
                tot_e += e
                tot_w += len(ref)
                if e / max(len(ref), 1) > 0.6:
                    bad.append((t["scene"], i + 1, round(e / len(ref), 2), hyp))
    wer = tot_e / max(tot_w, 1)
    print(f"WER toàn bài: {wer*100:.1f}% ({tot_w} từ)")
    for b in bad:
        print(f"❌ cảnh {b[0]} câu {b[1]}: WER {b[2]*100:.0f}% – máy nghe thành: {b[3]}")
    print("KẾT LUẬN:", "ĐẠT" if wer < 0.32 and not bad else "CẦN KIỂM TRA")
    (ep_dir / "build" / "asr.json").write_text(json.dumps({"wer": wer, "bad": bad}, ensure_ascii=False))


if __name__ == "__main__":
    main()
