#!/usr/bin/env python3
"""Tải video lên YouTube (chạy trên MÁY CỦA BẠN, cần trình duyệt để đăng nhập lần đầu).

Chuẩn bị 1 lần:
  1. https://console.cloud.google.com → tạo Project → "APIs & Services" → bật "YouTube Data API v3".
  2. "OAuth consent screen" → External → thêm email của bạn vào Test users.
  3. "Credentials" → Create credentials → OAuth client ID → loại "Desktop app" → tải JSON
     → lưu thành  secrets/client_secret.json  trong thư mục studio.
  4. pip install google-api-python-client google-auth-oauthlib

Dùng:
  python upload.py episodes/ep001-bach-dang            # đăng ở chế độ RIÊNG TƯ (mặc định)
  python upload.py episodes/ep001-bach-dang --schedule 2026-11-15T19:00:00+07:00   # hẹn giờ công khai
Lưu ý: dự án Google Cloud chưa xác minh thì video đăng qua API có thể bị khoá ở chế độ riêng tư
cho tới khi bạn gửi xác minh (audit) – khi đó cứ mở YouTube Studio và bấm Công khai thủ công.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]


def creds():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    tok = ROOT / "secrets" / "token.json"
    c = Credentials.from_authorized_user_file(str(tok), SCOPES) if tok.exists() else None
    if not c or not c.valid:
        if c and c.expired and c.refresh_token:
            c.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(ROOT / "secrets" / "client_secret.json"), SCOPES)
            c = flow.run_local_server(port=0)
        tok.parent.mkdir(exist_ok=True)
        tok.write_text(c.to_json())
    return c


def main() -> None:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--schedule", help="thời điểm công khai, ISO 8601 (vd 2026-11-15T19:00:00+07:00)")
    a = ap.parse_args()
    ep_dir = ROOT / a.episode
    meta = json.loads((ep_dir / "out" / "metadata.json").read_text(encoding="utf-8"))
    yt = build("youtube", "v3", credentials=creds())
    status = {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": meta["madeForKids"],
        "containsSyntheticMedia": meta.get("containsSyntheticMedia", False),
    }
    if a.schedule:
        status["publishAt"] = a.schedule
    body = {
        "snippet": {"title": meta["title"], "description": meta["description"], "tags": meta["tags"],
                    "categoryId": meta["categoryId"], "defaultLanguage": meta["defaultLanguage"],
                    "defaultAudioLanguage": meta["defaultLanguage"]},
        "status": status,
    }
    media = MediaFileUpload(str(ep_dir / "out" / "final.mp4"), chunksize=8 * 1024 * 1024, resumable=True, mimetype="video/mp4")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        st, resp = req.next_chunk()
        if st:
            print(f"  đang tải… {int(st.progress()*100)}%")
    vid = resp["id"]
    print(f"✅ Đã tải lên: https://youtu.be/{vid}  (riêng tư{' – hẹn giờ ' + a.schedule if a.schedule else ''})")
    try:  # thumbnail tuỳ chỉnh (cần kênh đã xác minh số điện thoại)
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(ep_dir / "out" / "thumbnail.png"))).execute()
        print("✅ Đã đặt thumbnail")
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  Chưa đặt được thumbnail: {e}")
    if meta.get("pinned_comment"):
        try:
            yt.commentThreads().insert(part="snippet", body={"snippet": {"videoId": vid, "topLevelComment": {
                "snippet": {"textOriginal": meta["pinned_comment"]}}}}).execute()
            print("✅ Đã đăng bình luận (vào YouTube Studio để Ghim)")
        except Exception as e:  # noqa: BLE001
            print(f"⚠️  Chưa đăng được bình luận: {e}")
    (ep_dir / "out" / "youtube.json").write_text(json.dumps({"video_id": vid}, indent=1))


if __name__ == "__main__":
    main()
