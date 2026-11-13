#!/usr/bin/env python3
"""Bộ kiểm tra tự động cho LEADER (vòng duyệt sau mỗi khâu).

    python studio/qa.py episodes/ep001-bach-dang --stage script|tts|art|render|meta|all

In ra bảng kiểm (PASS/WARN/FAIL) và xuất tư liệu để Leader *nhìn* bằng mắt:
  - out/storyboard.png          (khâu art – tạo bằng make.py --preview)
  - out/review_frames.png       (khâu render – 12 khung hình cắt từ video cuối)
Kết quả máy ghi vào build/qa_<stage>.json; nhận xét của Leader ghi vào reviews/.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS: list[dict] = []


def check(ok: bool | None, item: str, detail: str = "", fix: str = "") -> None:
    lvl = "PASS" if ok else ("WARN" if ok is None else "FAIL")
    RESULTS.append({"level": lvl, "item": item, "detail": detail, "fix": fix})


def words(t: str) -> int:
    return len(t.replace("*", "").split())


# ---------------------------------------------------------------- script
def qa_script(ep: dict) -> None:
    sc = ep["scenes"]
    allw = sum(words(l.get("say") or l["text"]) for s in sc for l in s["narration"])
    fmt = ep.get("format", "short")
    est = allw / 4.3  # tiếng Việt (đơn âm tiết) TTS ~4.3 từ/giây – đã hiệu chỉnh theo thực đo
    if fmt == "long":
        check(90 <= est <= 1200, "Độ dài kịch bản video ngang", f"{allw} từ ≈ {est/60:.1f} phút (mục tiêu 1.5–20 phút)", "Video dài nên ≥ 1.5 phút")
    if fmt == "short":
        check(35 <= est <= 62, "Độ dài kịch bản Shorts", f"{allw} từ ≈ {est:.0f}s (mục tiêu 40–60s)",
              "Cắt bớt/gộp câu nếu >60s; thêm chi tiết nếu <35s")
    hook = sc[0]["narration"][0]["text"]
    check(words(hook) <= 14, "Câu mở đầu (hook) ngắn gọn", hook, "Hook ≤ 14 từ, nói ngay điều gây tò mò trong 2 giây đầu")
    last = " ".join(l["text"] for l in sc[-1]["narration"])
    check("?" in last or "bình luận" in last.lower(), "Kêu gọi tương tác ở cuối (CTA)", last[:80], "Kết bằng 1 câu hỏi để người xem bình luận")
    max_scene = 14.5 if fmt == "long" else 9.5
    check(len(ep.get("fact_check", [])) >= 3, "Có danh sách kiểm chứng sự thật", f"{len(ep.get('fact_check', []))} mục",
          "Thêm ≥3 dữ kiện kèm nguồn vào fact_check")
    for s in sc:
        n = sum(words(l.get("say") or l["text"]) for l in s["narration"])
        check(n / 4.3 <= max_scene, f"Cảnh {s['id']} không quá dài", f"≈{n/4.3:.1f}s",
              "Tách cảnh >9s thành 2 cảnh để giữ nhịp hình ảnh thay đổi")
        has_ti = any(e["fn"] == "ti" for l in s.get("layers", []) for e in l["elements"])
        if fmt == "short":
          check(True if has_ti else None, f"Cảnh {s['id']} có nhân vật Tí", "" if has_ti else "không có Tí",
              "Nên có Tí trong mỗi cảnh để giữ nhận diện kênh")
    if fmt == "long":
        n_ti = sum(any(e["fn"] == "ti" for l in s.get("layers", []) for e in l["elements"]) for s in sc)
        check(n_ti >= max(3, len(sc) // 4), "Tí xuất hiện đủ để giữ nhận diện (≥1/4 số cảnh)", f"{n_ti}/{len(sc)} cảnh")
        for l in s["narration"]:
            if re.search(r"\d", l.get("say") or l["text"]) and not l.get("say"):
                check(False, f"Cảnh {s['id']}: số chưa viết thành chữ cho TTS", l["text"],
                      "Thêm trường 'say' viết số bằng chữ (vd 1288 → một nghìn hai trăm tám mươi tám)")


# ---------------------------------------------------------------- tts
def qa_tts(ep: dict, b: Path) -> None:
    tf = b / "timing.json"
    if not tf.exists():
        return check(False, "Chưa có timing.json", fix="Chạy make.py --stage tts")
    tm = json.loads(tf.read_text())
    total = sum(t["dur"] for t in tm)
    check(total <= 60 if ep.get("format") == "short" else True, "Tổng thời lượng giọng đọc", f"{total:.1f}s",
          "Shorts nên ≤60s để tối ưu tỷ lệ xem hết; giảm length_scale hoặc cắt lời")
    says = {s["id"]: [l.get("say") or l["text"] for l in s["narration"]] for s in ep["scenes"]}
    for t in tm:
        for i, l in enumerate(t["lines"]):
            rate = words(says[t["scene"]][i]) / max(l["dur"], .1)
            check(2.6 <= rate <= 5.6, f"Tốc độ đọc cảnh {t['scene']} câu {i+1}", f"{rate:.1f} từ/s",
                  "Quá nhanh/chậm: chỉnh voice.length_scale (0.85–1.05)")
    # âm lượng
    r = subprocess.run(["ffmpeg", "-i", str(b / "narration.wav"), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?\d+\.\d) LUFS", r.stderr)
    if m:
        lufs = float(m[-1])
        check(-20 <= lufs <= -12, "Độ to giọng đọc (LUFS)", f"{lufs} LUFS (mục tiêu -16 ±3)", "Chỉnh loudnorm trong make.py")


# ---------------------------------------------------------------- art
def qa_art(ep: dict, ep_dir: Path, b: Path) -> None:
    from PIL import Image, ImageStat

    sb = ep_dir / "out" / "storyboard.png"
    check(sb.exists(), "Có storyboard để Leader xem", str(sb.relative_to(ROOT)) if sb.exists() else "",
          "Chạy make.py --preview")
    for s in ep["scenes"]:
        files = sorted((b / "art").glob(f"s{s['id']:02d}_*.png"))
        check(bool(files), f"Cảnh {s['id']} đã có hình", f"{len(files)} lớp")
        if files:
            pvf = ep_dir / "out" / "preview" / f"scene_{s['id']:02d}.png"
            st = ImageStat.Stat(Image.open(pvf if pvf.exists() else files[0]).convert("L"))
            check(st.stddev[0] > 18, f"Cảnh {s['id']} nền đủ chi tiết/tương phản", f"độ lệch sáng {st.stddev[0]:.0f}",
                  "Nền quá phẳng: thêm núi/sông/đạo cụ hoặc đổi tông màu")


# ---------------------------------------------------------------- render
def qa_render(ep: dict, ep_dir: Path) -> None:
    f = ep_dir / "out" / "final.mp4"
    if not f.exists():
        return check(False, "Chưa có video final.mp4", fix="Chạy make.py --stage render")
    pr = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(f)]))
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    d = float(pr["format"]["duration"])
    want = (1920, 1080) if ep.get("format") == "long" else (1080, 1920)
    check((v["width"], v["height"]) == want, f"Độ phân giải {want[0]}x{want[1]}", f"{v['width']}x{v['height']}")
    check(bool(a), "Có âm thanh", f"{len(a)} track")
    check(d <= 60 if ep.get("format") == "short" else 90 <= d <= 1500, "Thời lượng video", f"{d:.1f}s")
    check(f.stat().st_size / 1e6 < 200, "Dung lượng file", f"{f.stat().st_size/1e6:.1f} MB")
    # khung đen
    r = subprocess.run(["ffmpeg", "-i", str(f), "-vf", "blackdetect=d=0.4:pix_th=0.08", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    blacks = re.findall(r"black_start:(\S+)", r.stderr)
    check(len([x for x in blacks if float(x) > 0.5]) == 0, "Không có đoạn màn hình đen giữa video", ", ".join(blacks) or "không")
    # contact sheet 12 khung hình cho Leader xem
    out = ep_dir / "out" / "review_frames.png"
    fps = 12 / d
    tile_vf = f"fps={fps:.4f},scale=" + ("480:270,tile=4x3" if ep.get("format") == "long" else "270:480,tile=6x2") + ":padding=8:color=0x222222"
    subprocess.run(["ffmpeg", "-y", "-i", str(f), "-vf", tile_vf,
                    "-frames:v", "1", str(out)], capture_output=True)
    check(out.exists(), "Đã xuất review_frames.png cho Leader", str(out.relative_to(ROOT)))


# ---------------------------------------------------------------- meta
def qa_meta(ep: dict, ep_dir: Path) -> None:
    m = ep["metadata"]
    check(len(m["title"]) <= 100, "Tiêu đề ≤ 100 ký tự", f"{len(m['title'])} ký tự")
    check(len(m["title"]) <= 70, "Tiêu đề hiển thị đủ trên điện thoại (≤70)", f"{len(m['title'])} ký tự", "Rút gọn tiêu đề")
    check(sum(len(t) for t in m.get("tags", [])) <= 450, "Tổng tag ≤ 450 ký tự", f"{sum(len(t) for t in m.get('tags', []))}")
    check(3 <= len(m.get("hashtags", [])) <= 8, "Số hashtag 3–8", f"{len(m.get('hashtags', []))}")
    if ep.get("format", "short") == "short":
        check("#Shorts" in m["title"] + " ".join(m.get("hashtags", [])), "Có #Shorts", "")
    check(bool(m.get("pinned_comment")), "Có bình luận ghim kéo tương tác", (m.get("pinned_comment") or "")[:50])
    th = ep_dir / "out" / "thumbnail.png"
    check(th.exists(), "Có thumbnail", str(th.relative_to(ROOT)) if th.exists() else "", "Chạy make.py --stage thumb")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--stage", default="all", choices=["script", "tts", "art", "render", "meta", "all"])
    a = ap.parse_args()
    ep_dir = (ROOT / a.episode).resolve()
    ep = json.loads((ep_dir / "episode.json").read_text(encoding="utf-8"))
    b = ep_dir / "build"
    st = a.stage
    if st in ("script", "all"):
        qa_script(ep)
    if st in ("tts", "all"):
        qa_tts(ep, b)
    if st in ("art", "all"):
        qa_art(ep, ep_dir, b)
    if st in ("render", "all"):
        qa_render(ep, ep_dir)
    if st in ("meta", "all"):
        qa_meta(ep, ep_dir)
    icon = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌"}
    for r in RESULTS:
        print(f"{icon[r['level']]} {r['item']}: {r['detail']}" + (f"\n      → {r['fix']}" if r["level"] != "PASS" and r["fix"] else ""))
    fails = sum(r["level"] == "FAIL" for r in RESULTS)
    warns = sum(r["level"] == "WARN" for r in RESULTS)
    print(f"\nKẾT QUẢ MÁY: {len(RESULTS)-fails-warns} đạt · {warns} cảnh báo · {fails} lỗi")
    b.mkdir(exist_ok=True)
    (b / f"qa_{st}.json").write_text(json.dumps(RESULTS, ensure_ascii=False, indent=1))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
