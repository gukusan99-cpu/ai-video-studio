#!/usr/bin/env python3
"""Dây chuyền sản xuất video "Tí Xuyên Sử".

Dùng:
    python make.py episodes/ep001-bach-dang            # chạy tất cả các khâu
    python make.py episodes/ep001-bach-dang --stage art # chỉ 1 khâu: tts | art | render | thumb | meta
    python make.py episodes/ep001-bach-dang --preview   # xuất ảnh xem trước từng cảnh (không dựng video)

Khâu:
  1. tts     – đọc lời thoại -> build/audio/*.wav  (Piper offline, miễn phí; hoặc edge-tts)
  2. art     – vẽ từng cảnh bằng SVG -> build/art/sNN_<layer>.png
               (nếu có visuals/scene_NN.png|jpg do bạn tự tạo bằng Gemini/Bing... thì dùng ảnh đó)
  3. render  – chuyển động lớp + ghép cảnh + phụ đề + nhạc -> out/final.mp4
  4. thumb   – ảnh thumbnail -> out/thumbnail.png
  5. meta    – tiêu đề / mô tả / tag -> out/metadata.json + out/UPLOAD.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from studio import svgart as A  # noqa: E402
from studio.rasterize import svgs_to_png  # noqa: E402
from studio import svgextra as X  # noqa: E402
from studio import doodle as D  # noqa: E402

CFG = json.loads((ROOT / "studio" / "config.json").read_text(encoding="utf-8"))
FPS = CFG.get("fps", 30)
BG_SCALE = 1.08
FMT = "short"
W, H = 1080, 1920
BW, BH = int(W * BG_SCALE) // 2 * 2, int(H * BG_SCALE) // 2 * 2


def set_format(fmt: str) -> None:
    """short = 1080x1920 (Shorts) · long = 1920x1080 (video ngang)"""
    global FMT, W, H, BW, BH
    FMT = fmt
    W, H = (1920, 1080) if fmt == "long" else (1080, 1920)
    BW, BH = int(W * BG_SCALE) // 2 * 2, int(H * BG_SCALE) // 2 * 2
    A.W, A.H = W, H


HAS_TIMELINE = True


def sub_cfg() -> dict:
    st = dict(CFG.get("subtitle_long", CFG["subtitle"]) if FMT == "long" else CFG["subtitle"])
    if FMT == "long" and not HAS_TIMELINE:
        st["margin_v"] = 46   # không có dòng thời gian -> phụ đề sát đáy, không đè nhân vật
    return st


def scene_layers(ep: dict, sc: dict, idx: int) -> list[dict]:
    """Các lớp của cảnh + lớp dòng thời gian tự động (nếu tập có 'timeline')."""
    layers = list(sc.get("layers", []))
    tl = ep.get("timeline")
    if tl and sc.get("timeline", True):
        at = sc.get("year", tl["start"])
        prev = ep["scenes"][idx - 1].get("year", at) if idx > 0 else at
        span = (W - 240) / (tl["end"] - tl["start"])
        layers.append({"name": "tlbar", "motion": "none", "elements": [
            {"fn": "timeline_bar", "args": {"start": tl["start"], "end": tl["end"], "title": tl["title"], "ticks": tl.get("ticks", [])}}]})
        layers.append({"name": "tlmark", "motion": "tl", "dx": (prev - at) * span, "elements": [
            {"fn": "timeline_marker", "args": {"start": tl["start"], "end": tl["end"], "at": at, "label": sc.get("date_label", f"{at:g}")}}]})
    return layers
FONT_DIR = ROOT / "assets" / "fonts"
SR = 44100


def log(msg: str) -> None:
    print(f"\033[1;36m▶ {msg}\033[0m", flush=True)


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(f"Lệnh lỗi: {' '.join(cmd[:6])} ...")


def strip_marks(t: str) -> str:
    return t.replace("*", "")


# ============================================================ 1. TTS
def tts_line(text: str, out: Path, voice: dict) -> None:
    engine = voice.get("engine", CFG["tts"]["engine"])
    if engine == "edge":
        # chạy được trên máy cá nhân (cần internet tới speech.platform.bing.com)
        cmd = ["edge-tts", "--voice", voice.get("edge_voice", CFG["tts"]["edge_voice"]),
               f"--rate={voice.get('edge_rate', '+0%')}", f"--pitch={voice.get('edge_pitch', '+0Hz')}", "--text", text, "--write-media", str(out.with_suffix(".mp3"))]
        if os.environ.get("HTTPS_PROXY"):
            cmd[1:1] = ["--proxy", os.environ["HTTPS_PROXY"]]
        import time
        for attempt in range(6):  # mạng chập chờn / máy chủ nghẽn -> thử lại, chờ tăng dần
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode == 0 and out.with_suffix(".mp3").exists() and out.with_suffix(".mp3").stat().st_size > 1000:
                break
            time.sleep(3 * (attempt + 1))
        else:
            print(r.stderr[-1500:])
            raise SystemExit("edge-tts lỗi")
        run(["ffmpeg", "-y", "-i", str(out.with_suffix(".mp3")), "-af",
             "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
             "loudnorm=I=-15:TP=-1.5", "-ar", str(SR), "-ac", "1", str(out)])
        out.with_suffix(".mp3").unlink(missing_ok=True)
        return
    model = ROOT / CFG["tts"]["piper_model"]
    tmp = out.with_suffix(".raw.wav")
    p = subprocess.run(
        [sys.executable, "-m", "piper", "-m", str(model), "-f", str(tmp),
         "--length-scale", str(voice.get("length_scale", 1.0)), "--sentence-silence", "0.15"],
        input=text, text=True, capture_output=True)
    if p.returncode != 0:
        print(p.stderr[-2000:])
        raise SystemExit("Piper lỗi")
    # chuẩn hoá: 44.1k mono, cắt khoảng lặng đầu/cuối, tăng âm lượng nhẹ
    run(["ffmpeg", "-y", "-i", str(tmp), "-af",
         "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
         "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
         "highpass=f=70,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-15:TP=-1.5",
         "-ar", str(SR), "-ac", "1", str(out)])
    tmp.unlink(missing_ok=True)


def stage_tts(ep: dict, b: Path) -> dict:
    log("1/5 Lồng tiếng (TTS)")
    voice_base = ep.get("voice", {})
    voice = voice_base
    gap, tail = voice.get("sentence_gap", 0.22), voice.get("scene_tail", 0.35)
    adir = b / "audio"
    adir.mkdir(parents=True, exist_ok=True)
    timing, t = [], 0.0
    for sc in ep["scenes"]:
        lines, start = [], t
        for i, ln in enumerate(sc["narration"]):
            say = ln.get("say") or strip_marks(ln["text"])
            voice = dict(voice_base, **({"edge_rate": ln["rate"]} if ln.get("rate") else {}))
            f = adir / f"s{sc['id']:02d}_l{i}.wav"
            key = f.with_suffix(".txt")
            sig = json.dumps([say, voice.get("engine"), voice.get("edge_voice"), voice.get("edge_rate"), voice.get("length_scale")], ensure_ascii=False)
            min_d = 0.14 * len(say.split())  # file cụt (mạng chập chờn) -> tạo lại
            if not (f.exists() and key.exists() and key.read_text(encoding="utf-8") == sig and sf.info(str(f)).duration >= min_d):
                for attempt in range(4):
                    tts_line(say, f, voice)
                    if sf.info(str(f)).duration >= min_d:
                        break
                    print(f"   ⚠️  câu bị cụt ({sf.info(str(f)).duration:.2f}s) – tạo lại lần {attempt+2}")
                else:
                    raise SystemExit(f"Giọng đọc lỗi ở cảnh {sc['id']} câu {i+1}")
                key.write_text(sig, encoding="utf-8")
            d = sf.info(str(f)).duration
            lines.append({"file": str(f), "start": round(t, 3), "dur": round(d, 3), "text": ln["text"]})
            print(f"   cảnh {sc['id']} câu {i+1}: {d:4.1f}s  {strip_marks(ln['text'])[:60]}")
            t += d + gap
        t += tail - gap
        timing.append({"scene": sc["id"], "start": round(start, 3), "dur": round(t - start, 3), "lines": lines})
    (b / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
    # ghép giọng đọc thành 1 track
    total = int((t + 0.3) * SR)
    track = np.zeros(total, dtype=np.float32)
    for sc in timing:
        for ln in sc["lines"]:
            a, _ = sf.read(ln["file"], dtype="float32")
            s0 = int(ln["start"] * SR)
            track[s0:s0 + len(a)] += a[: max(0, total - s0)]
    sf.write(str(b / "narration.wav"), track, SR)
    print(f"   tổng thời lượng: {t:.1f}s")
    return {"timing": timing, "total": t}


# ============================================================ 2. ART
def compose_layer(elements: list[dict]) -> str:
    body = ""
    for el in elements:
        fn = getattr(A, el["fn"], None) or getattr(X, el["fn"], None) or getattr(D, el["fn"], None)
        if fn is None:
            raise SystemExit(f"Không có hàm vẽ '{el['fn']}' trong studio/svgart.py")
        body += fn(**el.get("args", {}))
    return body


def dropin_for(ep_dir: Path, sid: int) -> Path | None:
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = ep_dir / "visuals" / f"scene_{sid:02d}.{ext}"
        if p.exists():
            return p
    return None


def cover_resize(src: Path, out: Path, w: int, h: int) -> None:
    im = Image.open(src).convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im.crop((l, t, l + w, t + h)).save(out)


def stage_art(ep: dict, ep_dir: Path, b: Path) -> None:
    log("2/5 Vẽ cảnh (SVG → PNG)")
    art = b / "art"
    if art.exists():
        shutil.rmtree(art)
    art.mkdir(parents=True)
    jobs = []
    for idx, sc in enumerate(ep["scenes"]):
        sid = sc["id"]
        drop = dropin_for(ep_dir, sid)
        if drop:
            print(f"   cảnh {sid}: dùng ảnh có sẵn {drop.name}")
            cover_resize(drop, art / f"s{sid:02d}_00_bg.png", BW, BH)
            layers = [l for l in scene_layers(ep, sc, idx) if l["name"] in ("tlbar", "tlmark")]
            start = 1
        else:
            layers, start = scene_layers(ep, sc, idx), 0
        for li, layer in enumerate(layers if start == 0 else [None] + layers):
            if layer is None:
                continue
            bgl = li == 0
            svg = A.svg_doc(compose_layer(layer["elements"]), w=BW if bgl else W, h=BH if bgl else H)
            jobs.append((svg, art / f"s{sid:02d}_{li:02d}_{layer['name']}.png", BW if bgl else W, BH if bgl else H))
    if jobs:
        svgs_to_png(jobs)
    print(f"   đã vẽ {len(jobs)} lớp hình")


# ============================================================ 3. RENDER
def bg_xy(kind: str, D: float) -> tuple[str, str]:
    dx, dy = W - BW, H - BH  # số âm
    p = f"(t/{D:.3f})"
    return {
        "still": (f"{dx/2:.0f}", f"{dy/2:.0f}"),
        "push_up": (f"{dx/2:.0f}", f"{dy}*{p}"),
        "push_down": (f"{dx/2:.0f}", f"{dy}*(1-{p})"),
        "left": (f"{dx}*{p}", f"{dy/2:.0f}"),
        "right": (f"{dx}*(1-{p})", f"{dy/2:.0f}"),
    }.get(kind, (f"{dx/2:.0f}", f"{dy/2:.0f}"))


def layer_xy(motion: str, D: float, k: int, layer: dict | None = None) -> tuple[str, str]:
    ph = k * 0.9
    layer = layer or {}
    if motion == "tl":
        return (f"{layer.get('dx', 0):.1f}*(1-min(t/0.9\\,1))", "0")
    if motion in ("from_left", "from_right"):
        sgn = -1 if motion == "from_left" else 1
        return (f"{sgn*700}*max(0\\,1-(t-{layer.get('_t0', 0):.3f})/0.7)", "0")
    if motion == "rise_in":  # trồi lên nhẹ khi xuất hiện
        return ("0", f"40*max(0\\,1-(t-{layer.get('_t0', 0):.3f})/0.4)")
    return {
        "none": ("0", "0"),
        "bob": ("0", f"9*sin(2*PI*t/1.7+{ph})"),
        "jump": ("0", f"-34*abs(sin(2*PI*t/1.3+{ph}))"),
        "drift_left": (f"40-80*t/{D:.3f}", f"6*sin(2*PI*t/2.2+{ph})"),
        "drift_right": (f"-40+80*t/{D:.3f}", "0"),
        "rise": ("0", f"520*(1-min(t/({D:.3f}*0.55)\\,1))"),
        "sink": ("0", f"50*t/{D:.3f}"),
        "shake": (f"7*sin(2*PI*t*7)", f"30*t/{D:.3f}+4*sin(2*PI*t*5)"),
        "slide_in": (f"-900*max(0\\,1-t/0.5)", f"9*sin(2*PI*t/1.7)"),
    }.get(motion, ("0", "0"))


def render_scene(sc: dict, b: Path, D: float, idx: int, n: int, ep: dict | None = None, tm: dict | None = None) -> Path:
    sid = sc["id"]
    art = b / "art"
    files = sorted(art.glob(f"s{sid:02d}_*.png"))
    out = b / "clips" / f"s{sid:02d}.mp4"
    out.parent.mkdir(exist_ok=True)
    cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={D:.3f}"]
    for f in files:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-i", str(f)]
    layers = {l["name"]: l for l in (scene_layers(ep, sc, idx) if ep else sc.get("layers", []))}
    chain, prev = [], "0:v"
    for i, f in enumerate(files):
        name = f.stem.split("_", 2)[2]
        L = layers.get(name, {})
        src = f"{i+1}:v"
        # xuất hiện đúng lúc lời đọc nhắc tới: appear = số thứ tự câu (0,1,..) hoặc appear_t = giây
        t0 = None
        if "appear_t" in L:
            t0 = float(L["appear_t"])
        elif "appear" in L and tm:
            li_ = min(int(L["appear"]), len(tm["lines"]) - 1)
            t0 = tm["lines"][li_]["start"] - tm["start"] + float(L.get("appear_delay", 0))
        fin = float(L.get("fade_in", 0.35))
        if t0 is not None and t0 > 0.02:
            chain.append(f"[{src}]format=rgba,fade=t=in:st={t0:.3f}:d={fin:.2f}:alpha=1[a{i}]")
            src = f"a{i}"
            L = dict(L, _t0=t0)
        # ẩn đi sau một lúc (chớp sáng, chữ BÙM...): hide_t = giây, hoặc hold = số giây hiện
        t1 = None
        if "hide_t" in L:
            t1 = float(L["hide_t"])
        elif "hold" in L:
            t1 = (t0 or 0) + float(L["hold"])
        if t1 is not None:
            chain.append(f"[{src}]format=rgba,fade=t=out:st={t1:.3f}:d=0.2:alpha=1[h{i}]")
            src = f"h{i}"
        if i == 0:
            x, y = bg_xy(sc.get("bg_motion", "still"), D)
        else:
            x, y = layer_xy(L.get("motion", "none"), D, i, L)
        chain.append(f"[{prev}][{src}]overlay=x='{x}':y='{y}':eval=frame:shortest=1[v{i}]")
        prev = f"v{i}"
    fades = []
    if idx == 0:
        fades.append("fade=t=in:st=0:d=0.25")
    if idx == n - 1:
        fades.append(f"fade=t=out:st={max(D-0.5,0):.3f}:d=0.5")
    chain.append(f"[{prev}]" + (",".join(fades) + "," if fades else "") + "format=yuv420p[vout]")
    cmd += ["-filter_complex", ";".join(chain), "-map", "[vout]", "-t", f"{D:.3f}", "-r", str(FPS),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", str(out)]
    run(cmd)
    return out


def ass_time(t: float) -> str:
    h, m = int(t // 3600), int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def chunk_words(text: str, max_words: int = 6, max_chars: int = 30) -> list[str]:
    """Chia phụ đề thành cụm dễ đọc:
    - không cắt giữa *từ khoá* (trừ khi bản thân từ khoá dài hơn max_chars)
    - không tách sau dấu phẩy nếu phần còn lại của câu chỉ ≤2 từ
    - cụm cuối ≤2 từ thì gộp vào cụm trước."""
    clen = lambda xs: len(strip_marks(" ".join(xs)))
    tokens, buf = [], []
    for w in text.split():
        if buf:
            buf.append(w)
            if "*" in w:
                if clen(buf) <= max_chars:
                    tokens.append(" ".join(buf))
                else:
                    tokens.extend(buf)
                buf = []
        elif w.count("*") == 1:
            buf = [w]
        else:
            tokens.append(w)
    tokens.extend(buf)
    # gom tên riêng (các tiếng viết hoa liền nhau, vd "Lam Sơn", "Đông Quan") thành 1 token
    merged_t = []
    for tk in tokens:
        prev = merged_t[-1] if merged_t else ""
        if (merged_t and "*" not in tk and "*" not in prev and strip_marks(tk)[:1].isupper()
                and strip_marks(prev.split()[-1])[:1].isupper() and not re.search(r"[,.!?…:;]$", prev)):
            merged_t[-1] = prev + " " + tk
        else:
            merged_t.append(tk)
    tokens = merged_t
    nwords = lambda t: len(t.split())
    chunks, cur = [], []
    for i, tk in enumerate(tokens):
        cw = sum(nwords(t) for t in cur)
        if cur and (cw >= max_words or clen(cur + [tk]) > max_chars):
            chunks.append(" ".join(cur)); cur = []
        cur.append(tk)
        if re.search(r"[,.!?…:;]$", strip_marks(tk)) and sum(nwords(t) for t in cur) >= 3:
            rest = sum(nwords(t) for t in tokens[i + 1:])
            if rest == 0 or rest > 2 or not strip_marks(tk).endswith(","):
                chunks.append(" ".join(cur)); cur = []
    if cur:
        chunks.append(" ".join(cur))
    while len(chunks) >= 2 and len(chunks[-1].split()) <= 2 and clen([chunks[-2], chunks[-1]]) <= max_chars + 8:
        chunks[-2:] = [chunks[-2] + " " + chunks[-1]]
    # gộp cụm ≤2 từ ở giữa vào cụm trước nếu vừa
    out = []
    for c in chunks:
        if out and len(c.split()) <= 2 and clen([out[-1], c]) <= max_chars + 8:
            out[-1] += " " + c
        else:
            out.append(c)
    return out


def to_ass_markup(chunk: str) -> str:
    # *từ khoá* -> màu vàng. Dấu * có thể mở ở chunk này và đóng ở chunk sau, nên xử lý theo trạng thái.
    return chunk


def build_ass(timing: list, b: Path) -> Path:
    st = sub_cfg()
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{st['font']},{st['size']},&H00FFFFFF,&H00FFFFFF,&H00120A05,&H96000000,-1,0,0,0,100,100,0,0,1,{st['outline']},3,2,{st.get('margin_lr', 70)},{st.get('margin_lr', 70)},{st['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev, hl = [], False
    yellow = "{\\c&H0030C4F4&}"
    white = "{\\c&H00FFFFFF&}"
    for sc in timing:
        for ln in sc["lines"]:
            chunks = chunk_words(ln["text"], 9, 38) if FMT == "long" else chunk_words(ln["text"])
            total_chars = sum(len(strip_marks(c)) for c in chunks) or 1
            # gộp cụm hiện quá nhanh (<0.8s) vào cụm kề bên
            merged = []
            for c in chunks:
                if merged and ln["dur"] * len(strip_marks(c)) / total_chars < 0.8:
                    merged[-1] += " " + c
                else:
                    merged.append(c)
            if len(merged) >= 2 and ln["dur"] * len(strip_marks(merged[0])) / total_chars < 0.8:
                merged[:2] = [merged[0] + " " + merged[1]]
            chunks = merged
            t = ln["start"]
            for c in chunks:
                d = ln["dur"] * len(strip_marks(c)) / total_chars
                txt = ""
                if hl:
                    txt += yellow
                for ch in c:
                    if ch == "*":
                        hl = not hl
                        txt += yellow if hl else white
                    else:
                        txt += ch
                pop = "{\\fscx82\\fscy82\\t(0,110,\\fscx100\\fscy100)}"
                ev.append(f"Dialogue: 0,{ass_time(t)},{ass_time(t + d)},Cap,,0,0,0,,{pop}{txt}")
                t += d
            hl = False
    p = b / "subs.ass"
    p.write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    return p


def stage_render(ep: dict, ep_dir: Path, b: Path) -> Path:
    log("3/5 Dựng video (chuyển động + phụ đề + âm thanh)")
    timing = json.loads((b / "timing.json").read_text())
    durs = {t["scene"]: t["dur"] for t in timing}
    tms = {t["scene"]: t for t in timing}
    clips = []
    n = len(ep["scenes"])
    for i, sc in enumerate(ep["scenes"]):
        clips.append(render_scene(sc, b, durs[sc["id"]], i, n, ep, tms[sc["id"]]))
        print(f"   cảnh {sc['id']} xong ({durs[sc['id']]:.1f}s)")
    lst = b / "clips" / "list.txt"
    lst.write_text("".join(f"file '{c.name}'\n" for c in clips))
    silent = b / "video_silent.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(silent)])
    subs = build_ass(timing, b)

    # âm thanh: giọng đọc + SFX + nhạc nền (file của bạn, hoặc tự tổng hợp) – nhạc tự hạ nhỏ khi có lời
    from studio import audiogen
    total = sum(t["dur"] for t in timing)
    starts = {t["scene"]: t["start"] for t in timing}
    voice, _ = sf.read(str(b / "narration.wav"), dtype="float32")
    fx = np.zeros_like(voice)
    for sc in ep["scenes"]:
        for e in sc.get("sfx", []):
            clip = audiogen.sfx(e["type"]) * e.get("gain", 0.35)
            p0 = int((starts[sc["id"]] + e.get("at", 0)) * SR)
            fx[p0:p0 + len(clip)] += clip[: max(0, len(fx) - p0)]
    sf.write(str(b / "voice_fx.wav"), voice + fx, SR)
    mcfg = ep.get("music", {})
    music = mcfg.get("file") or ""
    mpath = (ep_dir / music) if music else None
    if not (mpath and mpath.exists()):
        cands = sorted((ROOT / "assets" / "music").glob("*.mp3")) + sorted((ROOT / "assets" / "music").glob("*.wav"))
        mpath = cands[0] if cands else None
    if not mpath and mcfg.get("generate", True):
        mpath = b / "music_gen.wav"
        sf.write(str(mpath), audiogen.music(total + 0.5, mcfg.get("mood", "adventure")), SR)
        print("   🎵 đã tự tổng hợp nhạc nền ngũ cung (không bản quyền)")
    audio = b / "mix.wav"
    if mpath:
        vol = mcfg.get("volume", 0.12)
        run(["ffmpeg", "-y", "-i", str(b / "voice_fx.wav"), "-stream_loop", "-1", "-i", str(mpath), "-filter_complex",
             f"[1:a]volume={vol}[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];"
             f"[0:a][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-2:LRA=9,aresample=44100,alimiter=limit=0.8:level=0[a]", "-map", "[a]", "-ar", str(SR), str(audio)])
    else:
        shutil.copy(b / "voice_fx.wav", audio)

    out = ep_dir / "out"
    out.mkdir(exist_ok=True)
    final = out / "final.mp4"
    subs_arg = str(subs).replace(":", "\\:")
    run(["ffmpeg", "-y", "-i", str(silent), "-i", str(audio),
         "-vf", (CFG.get("look", "eq=contrast=1.05:saturation=1.08:gamma=0.98,vignette=angle=PI/5:mode=forward,noise=alls=4:allf=u") + ",")
                + f"ass='{subs_arg}':fontsdir='{FONT_DIR}'",
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", "-shortest", str(final)])
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(final)]))
    print(f"   ✅ {final.relative_to(ROOT)}  ({d:.1f}s, {final.stat().st_size/1e6:.1f} MB)")
    if ep.get("format") == "short" and d > 180:
        print("   ⚠️  Dài hơn 3 phút – YouTube sẽ không coi là Shorts")
    return final


# ============================================================ 4. THUMB
def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / "BeVietnamPro-ExtraBold.ttf"), size)


def stage_thumb(ep: dict, ep_dir: Path, b: Path) -> Path:
    log("4/5 Thumbnail")
    th = ep.get("thumbnail", {})
    if th.get("elements"):  # thumbnail tự bố cục bằng SVG (dùng cho video ngang)
        out = ep_dir / "out" / "thumbnail.png"
        tmp = b / "thumb"
        tmp.mkdir(exist_ok=True)
        svgs_to_png([(A.svg_doc(compose_layer(th["elements"])), tmp / "full.png", W, H)])
        Image.open(tmp / "full.png").convert("RGB").resize((1280, 720) if FMT == "long" else (1080, 1920), Image.LANCZOS).save(out)
        print(f"   ✅ {out.relative_to(ROOT)}")
        return out
    sid = th.get("scene", ep["scenes"][0]["id"])
    sc = next(s for s in ep["scenes"] if s["id"] == sid)
    tmp = b / "thumb"
    tmp.mkdir(exist_ok=True)
    drop = dropin_for(ep_dir, sid)
    bg_els = sc["layers"][0]["elements"] if not drop else []
    rest = [e for l in sc["layers"][1:] for e in l["elements"] if e["fn"] != "ti"] if not drop else []
    tiargs = {"x": 540, "y": 1880, "s": 1.25, "pose": th.get("ti", {}).get("pose", "shock"),
              "expr": th.get("ti", {}).get("expr", "surprised"), "glow": True}
    svgs_to_png([
        (A.svg_doc(compose_layer(bg_els + rest)), tmp / "bg.png", W, H),
        (A.svg_doc(A.ti(**tiargs)), tmp / "ti.png", W, H),
    ])
    base = Image.open(drop).convert("RGB") if drop else Image.open(tmp / "bg.png").convert("RGB")
    if drop:
        cover_resize(drop, tmp / "bgd.png", W, H)
        base = Image.open(tmp / "bgd.png").convert("RGB")
    base = base.filter(ImageFilter.GaussianBlur(1.2))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    for y in range(H):  # gradient tối ở trên cho chữ nổi
        a = int(170 * max(0, 1 - y / 900))
        d.line([(0, y), (W, y)], fill=(10, 8, 20, a))
    img = Image.alpha_composite(base.convert("RGBA"), shade)
    img = Image.alpha_composite(img, Image.open(tmp / "ti.png").convert("RGBA"))
    d = ImageDraw.Draw(img)
    y = 250
    for i, line in enumerate(th.get("headline", ["TÍ XUYÊN SỬ"])):
        size = 150 if len(line) <= 9 else 118
        f = _font(size)
        w = d.textlength(line, font=f)
        color = (255, 255, 255) if i == 0 else (244, 196, 48)
        d.text(((W - w) / 2, y), line, font=f, fill=color, stroke_width=12, stroke_fill=(20, 10, 5))
        y += size + 25
    if th.get("sub"):
        f = _font(62)
        w = d.textlength(th["sub"], font=f)
        pad = 28
        d.rounded_rectangle([(W - w) / 2 - pad, y + 20, (W + w) / 2 + pad, y + 20 + 62 + pad * 1.6], radius=40, fill=(214, 47, 58))
        d.text(((W - w) / 2, y + 20 + pad * .55), th["sub"], font=f, fill=(255, 255, 255))
    out = ep_dir / "out" / "thumbnail.png"
    out.parent.mkdir(exist_ok=True)
    img.convert("RGB").save(out, quality=95)
    # bản ngang 1280x720 (dùng khi gộp thành video dài / Facebook)
    land = Image.new("RGB", (1280, 720), (20, 16, 30))
    small = img.convert("RGB").resize((405, 720), Image.LANCZOS)
    blur = img.convert("RGB").resize((1280, 2276)).crop((0, 778, 1280, 1498)).filter(ImageFilter.GaussianBlur(25))
    land.paste(blur, (0, 0))
    land.paste(small, (437, 0))
    land.save(ep_dir / "out" / "thumbnail_16x9.png")
    print(f"   ✅ {out.relative_to(ROOT)}")
    return out


# ============================================================ 5. META
def stage_meta(ep: dict, ep_dir: Path, b: Path) -> None:
    log("5/5 Metadata + gói đăng bài")
    m = ep["metadata"]
    timing = json.loads((b / "timing.json").read_text())
    desc = m["description"]
    if ep.get("chapters"):  # mục lục chương tự tính theo thời gian thực của giọng đọc
        st = {t["scene"]: t["start"] for t in timing}
        total = sum(t["dur"] for t in timing)
        marks = []  # (giây, tiêu đề) – YouTube yêu cầu chương đầu 0:00 và mỗi chương ≥ 10s
        for ch in ep["chapters"]:
            t = 0 if not marks else int(st[ch["scene"]])
            if marks and t - marks[-1][0] < 10:
                marks[-1] = (marks[-1][0], marks[-1][1] + " · " + ch["title"])  # gộp chương quá ngắn
            else:
                marks.append((t, ch["title"]))
        if len(marks) >= 2 and total - marks[-1][0] < 10:
            last = marks.pop()
            marks[-1] = (marks[-1][0], marks[-1][1] + " · " + last[1])
        lines = [f"{t//60}:{t%60:02d} {title}" for t, title in marks]
        desc = desc.replace("{CHAPTERS}", "⏱ Nội dung:\n" + "\n".join(lines))
    desc += "\n\n" + " ".join(m.get("hashtags", []))
    meta = {
        "title": m["title"][:100],
        "description": desc[:5000],
        "tags": m.get("tags", []),
        "categoryId": m.get("category_id", "27"),
        "defaultLanguage": m.get("language", "vi"),
        "madeForKids": m.get("made_for_kids", False),
        "containsSyntheticMedia": False,
        "privacyStatus": "private",
        "pinned_comment": m.get("pinned_comment", ""),
        "duration_sec": round(sum(t["dur"] for t in timing), 1),
    }
    out = ep_dir / "out"
    (out / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    uses_photo = '"photo"' in json.dumps(ep)
    bg_note = ("nhân vật là hoạt hình vẽ, ảnh nền là ảnh chụp thật có giấy phép, không có cảnh AI giống thật." if uses_photo
               else "nhân vật và nền đều là tranh vẽ (hoạt hình / sơn dầu kỹ thuật số), không có cảnh AI giống thật.")
    md = f"""# Gói đăng bài – {ep.get('series','')} | {ep['id']}

**File video:** `out/final.mp4` ({meta['duration_sec']}s, {W}x{H}, {'dạng Shorts' if FMT == 'short' else 'video ngang'})
**Thumbnail:** {"`out/thumbnail.png` (Shorts) · `out/thumbnail_16x9.png`" if FMT == "short" else "`out/thumbnail.png` (1280x720, 16:9)"}

## Tiêu đề (chọn 1)
1. {m['title']}
""" + "".join(f"{i+2}. {t}\n" for i, t in enumerate(m.get("alt_titles", []))) + f"""
## Mô tả
```
{desc}
```

## Tags
```
{', '.join(m.get('tags', []))}
```

## Bình luận ghim
```
{m.get('pinned_comment','')}
```

## Cài đặt khi đăng
- Danh mục: Giáo dục (27) · Ngôn ngữ: Tiếng Việt
- Dành cho trẻ em: **Không** (để được bật bình luận & quảng cáo đầy đủ)
- Nội dung thay đổi/tổng hợp (AI): **Không bắt buộc** – {bg_note} Nếu dùng ảnh AI giống thật (Gemini...), hãy chọn **Có**.
- Lịch đăng gợi ý: 18:30–20:30 (giờ VN)

## Kiểm tra sự thật
""" + "".join(f"- {f}\n" for f in ep.get("fact_check", [])) + """
## Đăng
- Cách 1 (thủ công): YouTube Studio → Tạo → Tải video lên → dán các mục trên.
- Cách 2 (tự động): `python upload.py """ + str(ep_dir.relative_to(ROOT)) + """` (xem README, cần client_secret.json).
"""
    (out / "UPLOAD.md").write_text(md, encoding="utf-8")
    print(f"   ✅ {(out / 'UPLOAD.md').relative_to(ROOT)}")


# ============================================================ preview
def preview(ep: dict, ep_dir: Path, b: Path) -> None:
    """Ảnh tĩnh từng cảnh (đã ghép lớp) để duyệt nhanh, + contact sheet."""
    stage_art(ep, ep_dir, b)
    pv = ep_dir / "out" / "preview"
    pv.mkdir(parents=True, exist_ok=True)
    thumbs = []
    for sc in ep["scenes"]:
        files = sorted((b / "art").glob(f"s{sc['id']:02d}_*.png"))
        bg = Image.open(files[0]).convert("RGBA")
        img = bg.crop(((BW - W) // 2, (BH - H) // 2, (BW - W) // 2 + W, (BH - H) // 2 + H))
        for f in files[1:]:
            img = Image.alpha_composite(img, Image.open(f).convert("RGBA"))
        p = pv / f"scene_{sc['id']:02d}.png"
        img.convert("RGB").save(p)
        thumbs.append(img.convert("RGB").resize((270, 480) if FMT == "short" else (480, 270)))
    tw, th_ = thumbs[0].size
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 10, rows * th_ + (rows + 1) * 10), (30, 30, 30))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th_ + 10)))
    sheet.save(ep_dir / "out" / "storyboard.png")
    print(f"   ✅ {(ep_dir / 'out' / 'storyboard.png').relative_to(ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", help="thư mục tập, vd episodes/ep001-bach-dang")
    ap.add_argument("--stage", default="all", choices=["all", "tts", "art", "render", "thumb", "meta"])
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    ep_dir = (ROOT / a.episode).resolve() if not Path(a.episode).is_absolute() else Path(a.episode)
    ep = json.loads((ep_dir / "episode.json").read_text(encoding="utf-8"))
    set_format(ep.get("format", "short"))
    global HAS_TIMELINE
    HAS_TIMELINE = bool(ep.get("timeline"))
    b = ep_dir / "build"
    b.mkdir(exist_ok=True)
    (ep_dir / "out").mkdir(exist_ok=True)
    if a.preview:
        return preview(ep, ep_dir, b)
    st = a.stage
    if st in ("all", "tts"):
        stage_tts(ep, b)
    if st in ("all", "art"):
        stage_art(ep, ep_dir, b)
    if st in ("all", "render"):
        stage_render(ep, ep_dir, b)
    if st in ("all", "thumb"):
        stage_thumb(ep, ep_dir, b)
    if st in ("all", "meta"):
        stage_meta(ep, ep_dir, b)
    log("Hoàn tất 🎬")


if __name__ == "__main__":
    main()
