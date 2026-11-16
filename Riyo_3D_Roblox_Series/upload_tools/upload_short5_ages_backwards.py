"""
Upload Short #5: In This Town, Everyone Ages Backwards
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
VIDEO_PATH = os.path.join(SERIES_DIR, 'master_videos', 'SHORT_5_Ages_Backwards_Grandpa_Egg.mp4')

TITLE = "In This Town, Everyone Ages Backwards 👶👴 #shorts #roblox"
DESCRIPTION = """In this town, you're born looking 80 years old, and every birthday you get one year younger. Toddlers wear suits and carry briefcases to work, and grandpas play in ball pits. But tomorrow, my grandpa turns zero... so I hid under his crib to see the truth! 🍼😱

🔥 LIKE, SHARE & SUBSCRIBE TO TALEBLOX FOR MORE VIRAL STORIES!
🔔 Hit the bell so you never miss an episode!

💬 COMMENT BELOW: Would you rather age backwards or forwards? 👇

---
#shorts #roblox #robloxstory #animation #3danimation #gaming #robloxgames #robloxedit #agingbackwards #mystery #grandpa #benjaminbutton #storytime #fyp #viralvideo #like #share #subscribe #TaleBlox #riyo #riyo3d"""

TAGS = [
    "shorts", "roblox", "roblox shorts", "roblox animation", "roblox story", 
    "roblox scary stories", "robloxgames", "roblox edit", "viral", "viral shorts", 
    "trending", "trending shorts", "animation", "3d animation", "cgi animation", 
    "aging backwards", "benjamin button", "grandpa", "stork", "mystery", 
    "storytime", "like share subscribe", "gaming", "fyp", "TaleBlox", "riyo", "riyo 3d"
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
    # Scheduled for Tuesday Nov 17, 2026 at 8:30 AM IST = 03:00:00 UTC
    upload(scheduled_time="2026-11-17T03:00:00Z")
