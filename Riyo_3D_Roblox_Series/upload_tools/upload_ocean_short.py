"""
Upload Riyo 3D Ocean Story Short to YouTube
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

WORKSPACE_DIR = r"D:\Antigravity\Pro"
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')
VIDEO_PATH = os.path.join(WORKSPACE_DIR, 'ROBLOX_STORY_100_YEAR_OCEAN_RIYO_FINAL.mp4')

TITLE = "The Ocean Disappeared For 24 Hours... 🌊😱 #shorts #roblox #viral"
DESCRIPTION = """Once every 100 years, the ocean pulls back for one day, letting the town walk on the seafloor between forgotten shipwrecks. But when the shells began to sing hours early, Sam realized the terrifying truth: the sea didn't leave... it pulled back to take a breath! 🌊⚡

🔥 LIKE, SHARE & SUBSCRIBE TO RIYO 3D FOR MORE VIRAL EPISODES!
🔔 Turn on ALL notifications so you never miss the next animated story!

💬 COMMENT BELOW: Would you dare walk on the seafloor between the shipwrecks? 👇

---
#shorts #roblox #robloxstory #animation #3danimation #gaming #robloxgames #robloxedit #viral #trending #trendingshorts #tsunami #ocean #mystery #scarystories #creepypasta #storytime #fyp #viralvideo #like #share #subscribe #riyo #riyo3d"""

TAGS = [
    "shorts", "roblox", "roblox shorts", "roblox animation", "roblox story", 
    "roblox scary stories", "robloxgames", "roblox edit", "viral", "viral shorts", 
    "trending", "trending shorts", "animation", "3d animation", "cgi animation", 
    "ocean", "tsunami", "megatsunami", "seafloor", "storytime", "like share subscribe", 
    "gaming", "fyp", "riyo", "riyo 3d"
]

def upload():
    if not os.path.exists(VIDEO_PATH):
        print(f"[!] Error: Video file not found: {VIDEO_PATH}")
        sys.exit(1)

    if not os.path.exists(TOKEN_PICKLE):
        print(f"[!] Error: {TOKEN_PICKLE} not found.")
        sys.exit(1)

    with open(TOKEN_PICKLE, 'rb') as token:
        credentials = pickle.load(token)

    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            print("[*] Refreshing expired YouTube token...", flush=True)
            credentials.refresh(Request())
            with open(TOKEN_PICKLE, 'wb') as token:
                pickle.dump(credentials, token)
            print("[+] Token refreshed successfully!", flush=True)

    youtube = build('youtube', 'v3', credentials=credentials)

    body = {
        'snippet': {
            'title': TITLE,
            'description': DESCRIPTION,
            'tags': TAGS,
            'categoryId': '20'  # Gaming
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(VIDEO_PATH, chunksize=-1, resumable=True, mimetype="video/mp4")

    print(f"\n[+] Uploading '{TITLE}' ({os.path.getsize(VIDEO_PATH) / (1024*1024):.2f} MB) to YouTube...", flush=True)
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
    print("[SUCCESS] Video published to YouTube!", flush=True)
    print(f"Watch URL:  https://youtu.be/{video_id}", flush=True)
    print(f"Shorts URL: https://www.youtube.com/shorts/{video_id}", flush=True)
    print("="*50 + "\n", flush=True)
    return video_id

if __name__ == '__main__':
    upload()
