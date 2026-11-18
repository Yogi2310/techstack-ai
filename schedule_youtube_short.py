"""
Automated YouTube Video Scheduler for TaleBlox
Usage: python schedule_youtube_short.py <video_filename> <YYYY-MM-DDTHH:MM:SSZ>
"""
import os
import sys
import pickle
from datetime import datetime
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

WORKSPACE_DIR = r"D:\Antigravity\Pro"
SERIES_DIR = os.path.join(WORKSPACE_DIR, 'Riyo_3D_Roblox_Series')
MASTER_DIR = os.path.join(SERIES_DIR, 'master_videos')
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')

VIDEO_METADATA = {
    "SHORT_12_Touching_the_Ground_Costs_10.mp4": {
        "title": "Touching The Ground Costs $10 💸🏃 (Roblox 3D Story) #shorts #roblox",
        "description": """In this crazy Roblox world, touching the ground costs $10 every single step! 💸🔥
The rich can walk anywhere they want... while poor players have to parkour across lampposts, rooftops, and traffic signs just to survive! 😱🧱
Watch what happens when one parkour master finds a glitch in the city system!

🎬 Watch till the end to see the epic jump!
⚡ LIKE, SUBSCRIBE & COMMENT for more TaleBlox (Riyo 3D) adventures!

#shorts #roblox #robloxstory #parkour #floorislava #gaming #3danimation #viralvideo #taleblox #riyo3d""",
        "tags": ["shorts", "roblox", "roblox shorts", "roblox story", "floor is lava", "parkour", "gaming", "3d animation", "viral shorts", "trending", "taleblox", "riyo 3d"]
    },
    "SHORT_10_Everyone_Is_A_Ninja.mp4": {
        "title": "Everyone Is A Ninja Except Me 🥷⛩️ (Roblox 3D Story) #shorts #roblox",
        "description": """In my village, everyone is born with god-tier ninja abilities... but I was born with ZERO skills! 😭🥷
Or so everyone thought... until the Forbidden Shrine opened its seal! ⛩️🔥

🎬 Watch till the very end to see the legendary secret jutsu unlock!
⚡ LIKE, SHARE & SUBSCRIBE TO TALEBLOX (RIYO 3D) FOR MORE VIRAL STORIES!

#shorts #roblox #robloxstory #ninja #animation #3danimation #gaming #anime #storytime #taleblox #riyo3d""",
        "tags": ["shorts", "roblox", "roblox shorts", "roblox story", "ninja", "everyone is a ninja", "animation", "3d animation", "anime", "taleblox", "riyo 3d"]
    },
    "SHORT_13_You_Get_Paid_for_Being_Unlucky.mp4": {
        "title": "You Get Paid For Being Unlucky 🍀💰 (Roblox 3D Story) #shorts #roblox",
        "description": """In this world, the unluckier you are, the more money you get deposited into your bank account! 💰😭
Watch what happens when the unluckiest person alive tries to win the lottery!

🎬 Watch till the end!
⚡ LIKE & SUBSCRIBE to TaleBlox!

#shorts #roblox #robloxstory #luck #gaming #3danimation #viral #taleblox #riyo3d""",
        "tags": ["shorts", "roblox", "roblox shorts", "roblox story", "unlucky", "gaming", "animation", "3d animation", "taleblox", "riyo 3d"]
    }
}

def schedule_video(video_name, publish_iso_utc):
    video_path = os.path.join(MASTER_DIR, video_name)
    if not os.path.exists(video_path):
        print(f"[!] Video not found: {video_path}")
        return None

    meta = VIDEO_METADATA.get(video_name, {
        "title": f"{video_name.replace('.mp4', '').replace('_', ' ')} #shorts #roblox",
        "description": "Watch till the end! Subscribe to TaleBlox for daily 3D Roblox stories!\n\n#shorts #roblox #taleblox #riyo3d",
        "tags": ["shorts", "roblox", "roblox story", "animation", "taleblox", "riyo 3d"]
    })

    with open(TOKEN_PICKLE, 'rb') as token:
        credentials = pickle.load(token)

    if not credentials.valid and credentials.expired and credentials.refresh_token:
        print("[*] Refreshing YouTube OAuth token...")
        credentials.refresh(Request())
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(credentials, token)

    youtube = build('youtube', 'v3', credentials=credentials)

    body = {
        'snippet': {
            'title': meta['title'],
            'description': meta['description'],
            'tags': meta['tags'],
            'categoryId': '20' # Gaming
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': publish_iso_utc,
            'selfDeclaredMadeForKids': False
        }
    }

    print(f"[*] Uploading and scheduling '{meta['title']}'...")
    print(f"[*] Scheduled release (UTC): {publish_iso_utc}")
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    Progress: {int(status.progress() * 100)}%")

    video_id = response['id']
    print(f"\n[+] SUCCESS! Video Scheduled!")
    print(f"    Video ID: {video_id}")
    print(f"    Watch URL: https://youtu.be/{video_id}")
    print(f"    Scheduled for: {publish_iso_utc}")
    return video_id

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python schedule_youtube_short.py <video_filename> <YYYY-MM-DDTHH:MM:SSZ>")
        sys.exit(1)
    schedule_video(sys.argv[1], sys.argv[2])
