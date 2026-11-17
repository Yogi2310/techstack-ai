"""
Upload Short #10: Everyone Is A Ninja Except Me
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
VIDEO_PATH = os.path.join(SERIES_DIR, 'master_videos', 'SHORT_10_Everyone_Is_A_Ninja.mp4')

TITLE = "Everyone Is A Ninja Except Me 🥷⛩️ (Roblox 3D Story) #shorts #roblox"
DESCRIPTION = """In my village, everyone is born with god-tier ninja abilities... jumping over pagodas, summoning cherry blossom shadows, and passing the high trials. But I was born with ZERO ninja skills! 😭🥷
Or so everyone thought... until the Forbidden Shrine opened its seal! ⛩️🔥

🎬 Watch till the very end to see the legendary secret jutsu unlock!
⚡ LIKE, SHARE & SUBSCRIBE TO TALEBLOX (RIYO 3D) FOR MORE VIRAL STORIES!
🔔 Turn on ALL notifications so you never miss Chapter 2!

💬 COMMENT BELOW: If you were in this village, what would your Ninja Element be? 👇

---
#shorts #roblox #robloxstory #ninja #animation #3danimation #gaming #robloxgames #robloxedit #anime #naruto #dojo #viralvideo #like #share #subscribe #taleblox #riyo3d"""

TAGS = [
    "shorts", "roblox", "roblox shorts", "roblox animation", "roblox story", 
    "ninja", "roblox ninja", "everyone is a ninja", "robloxgames", "roblox edit", 
    "viral", "viral shorts", "trending", "trending shorts", "animation", 
    "3d animation", "anime", "naruto", "dojo", "storytime", "like share subscribe", 
    "gaming", "fyp", "taleblox", "riyo 3d"
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
            'categoryId': '20' # Gaming
        },
        'status': status_dict
    }

    media = MediaFileUpload(VIDEO_PATH, chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    print(f"[*] Uploading {VIDEO_PATH}...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print("\n[+] SUCCESS! Video uploaded!")
    print(f"    Video ID: {response['id']}")
    print(f"    Watch URL: https://youtu.be/{response['id']}")
    return response['id']

if __name__ == '__main__':
    upload()
