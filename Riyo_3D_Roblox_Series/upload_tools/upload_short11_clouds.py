"""
Upload Short #11: In This Town, The Rich Live Above The Clouds
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
VIDEO_PATH = os.path.join(SERIES_DIR, 'master_videos', 'SHORT_11_The_Rich_Live_Above_The_Clouds.mp4')

TITLE = "In This Town, The Rich Live Above The Clouds ☁️🏙️ (Roblox 3D Story) #shorts #roblox"
DESCRIPTION = """In this town, the ultimate class divide exists... The billionaires live in floating cyber-cities above the clouds with infinite robux, clean air, and high-tech gravity elevators.
Down on the surface, everyone breathes toxic smog and fights for scraps... 😭☁️
Until one kid builds a homemade glider and scales the Megastructure elevator shaft! 🚀💥

🎬 Watch till the very end to see what's really powering the cloud city!
⚡ LIKE, SHARE & SUBSCRIBE TO TALEBLOX (RIYO 3D) FOR MORE VIRAL STORIES!
🔔 Turn on ALL notifications so you never miss Part 2!

💬 COMMENT BELOW: Would you sneak into the Cloud City or stay on the ground? 👇

---
#shorts #roblox #robloxstory #rich #clouds #animation #3danimation #gaming #robloxgames #robloxedit #cyberpunk #storytime #fyp #viralvideo #like #share #subscribe #taleblox #riyo3d"""

TAGS = [
    "shorts", "roblox", "roblox shorts", "roblox animation", "roblox story", 
    "rich", "the rich live above the clouds", "clouds", "robloxgames", "roblox edit", 
    "viral", "viral shorts", "trending", "trending shorts", "animation", 
    "3d animation", "cgi animation", "storytime", "like share subscribe", 
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
