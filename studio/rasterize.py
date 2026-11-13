"""Chuyển SVG -> PNG bằng Chromium (Playwright qua Node) – hỗ trợ nền trong suốt."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def svgs_to_png(jobs: list[tuple[str, Path, int, int]]) -> None:
    """jobs = [(svg_text, out_png, width, height), ...]"""
    with tempfile.TemporaryDirectory() as td:
        spec = []
        for i, (svg, out, w, h) in enumerate(jobs):
            p = Path(td) / f"{i}.svg"
            p.write_text(svg, encoding="utf-8")
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            spec.append({"svg": str(p), "out": str(Path(out).resolve()), "w": w, "h": h})
        jf = Path(td) / "jobs.json"
        jf.write_text(json.dumps(spec))
        env = dict(os.environ)
        node_paths = [p for p in ["/opt/node22/lib/node_modules", "/usr/lib/node_modules", "/usr/local/lib/node_modules"] if Path(p).exists()]
        env["NODE_PATH"] = ":".join(node_paths + [env.get("NODE_PATH", "")])
        subprocess.run(["node", str(HERE / "rasterize.js"), str(jf)], check=True, env=env)
