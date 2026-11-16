"""
Upload Short #4: In My Town, Everything Works Like A Video Game
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

WORKSPACE_DIR = r"D:\Antigravity\Pro"
SERIES_DIR = os.path.join(WORKSPACE_DIR, 'Riyo_3D_Roblox_Series')
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')
VIDEO_PATH = os.path.join(SERIES_DIR, 'master_videos', 'SHORT_4_Video_Game_Town_Level_999.mp4')

TITLE = "In My Town, Everything Works Like A Video Game 🎮 (PART 3) #shorts #roblox"
DESCRIPTION = """PART 3 OF THE RIYO 3D TOWN SERIES! 🎮⚡ In this town, everyone has a health bar, a level, and an inventory. My dad is level 60, my mom is level 85, and my grandma is level 99. But I was stuck at level 1 my whole life... until I glitched into the Town Settings room! 🕹️⚡

🔥 LIKE, SHARE & SUBSCRIBE TO RIYO 3D FOR MORE VIRAL STORIES!
🔔 Turn on ALL notifications so you never miss World 2!

💬 COMMENT BELOW: What level would you be in real life? 👇

---
#shorts #roblox #robloxstory #animation #3danimation #gaming #robloxgames #robloxedit #videogame #glitch #level999 #tutorial #part3 #storytime #fyp #viralvideo #like #share #subscribe #riyo #riyo3d"""

TAGS = [
    "shorts", "roblox", "roblox shorts", "roblox animation", "roblox story", 
    "roblox scary stories", "robloxgames", "roblox edit", "viral", "viral shorts", 
    "trending", "trending shorts", "animation", "3d animation", "cgi animation", 
    "part 3", "videogame", "rpg", "level 1", "level 999", "glitch", "tutorial", 
    "storytime", "like share subscribe", "gaming", "fyp", "riyo", "riyo 3d"
]

def upload(scheduled_time=None):
    if not os.path.exists(VIDEO_PATH):
        print(f"[!] Error: Video file not found: {VIDEO_PATH}")
        sys.exit(1)

    with open(TOKEN_PICKLE, 'rb') as token:
        credentials = pickle.load(token)

    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            with open(TOKEN_PICKLE, 'wb') as token:
                pickle.dump(credentials, token)

    youtube = build('youtube', 'v3', credentials=credentials)

    status_dict = {
        'privacyStatus': 'private' if scheduled_time else 'public',
        'selfDeclaredMadeForKids': False
    }
    if scheduled_time:
        status_dict['publishAt'] = scheduled_time

    body = {
        'snippet': {
            'title': TITLE,
            'description': DESCRIPTION,
            'tags': TAGS,
            'categoryId': '20'  # Gaming
        },
        'status': status_dict
    }

    media = MediaFileUpload(VIDEO_PATH, chunksize=-1, resumable=True, mimetype="video/mp4")

    print(f"\n[+] Uploading '{TITLE}' ({os.path.getsize(VIDEO_PATH) / (1024*1024):.2f} MB)...", flush=True)
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    Upload progress: {int(status.progress() * 100)}%", flush=True)

    video_id = response.get('id')
    print("\n" + "="*50, flush=True)
    print(f"[SUCCESS] Video uploaded to YouTube! (ID: {video_id})", flush=True)
    print(f"Watch URL:  https://youtu.be/{video_id}", flush=True)
    print(f"Shorts URL: https://www.youtube.com/shorts/{video_id}", flush=True)
    if scheduled_time:
        print(f"Scheduled for: {scheduled_time}", flush=True)
    print("="*50 + "\n", flush=True)
    return video_id

if __name__ == '__main__':
    # 7:30 PM IST on Nov 16, 2026 = 14:00:00 UTC
    upload(scheduled_time='2026-11-16T14:00:00Z')
