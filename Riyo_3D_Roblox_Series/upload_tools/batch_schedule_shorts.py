"""
Batch Automated YouTube Shorts Scheduler for TaleBlox (Riyo 3D)
Uploads and schedules pending master videos to YouTube during peak viewer hours.
Handles daily YouTube API quotas safely and maintains a persistent upload ledger.
"""

import os
import sys
import json
import re
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

WORKSPACE_DIR = r"D:\Antigravity\Pro"
SERIES_DIR = os.path.join(WORKSPACE_DIR, 'Riyo_3D_Roblox_Series')
MASTER_DIR = os.path.join(SERIES_DIR, 'master_videos')
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')
LEDGER_FILE = os.path.join(SERIES_DIR, 'upload_ledger.json')

# Known metadata overrides for high CTR & viral engagement
CUSTOM_METADATA = {
    "SHORT_10_Everyone_Is_A_Ninja.mp4": {
        "title": "Everyone Is A Ninja Except Me 🥷⛩️ (Roblox 3D Story) #shorts #roblox",
        "description": "In my village, everyone is born with god-tier ninja abilities... but I was born with ZERO skills! 😭🥷\nOr so everyone thought... until the Forbidden Shrine opened its seal! ⛩️🔥\n\n🎬 Watch till the very end to see the legendary secret jutsu unlock!\n⚡ LIKE, SHARE & SUBSCRIBE TO TALEBLOX FOR MORE VIRAL STORIES!\n\n#shorts #roblox #robloxstory #ninja #animation #3danimation #gaming #taleblox #riyo3d",
        "tags": ["shorts", "roblox", "roblox shorts", "roblox story", "ninja", "everyone is a ninja", "animation", "3d animation", "gaming", "taleblox", "riyo 3d"]
    },
    "SHORT_13_You_Get_Paid_for_Being_Unlucky.mp4": {
        "title": "You Get Paid For Being Unlucky 🍀💰 (Roblox 3D Story) #shorts #roblox",
        "description": "In this world, the unluckier you are, the more money gets deposited into your bank account! 💰😭\nWatch what happens when the unluckiest player in town tries to win the lottery! 🤯💸\n\n🎬 Watch till the end!\n⚡ LIKE & SUBSCRIBE to TaleBlox!\n\n#shorts #roblox #robloxstory #luck #gaming #3danimation #viral #taleblox #riyo3d",
        "tags": ["shorts", "roblox", "roblox shorts", "roblox story", "unlucky", "gaming", "animation", "3d animation", "taleblox", "riyo 3d"]
    },
    "SHORT_14_the_Monster_Can_Only_Move_in_the_Dark_Pa.mp4": {
        "title": "The Monster Can Only Move In The Dark! 🌑👁️ (Part 1) #shorts #roblox",
        "description": "The golden rule of survival in this city: NEVER let the lights go out! 💡😱\nThe moment the city power grid fails, the shadow creature strikes...\n\n🎬 Part 1 of the Monster in the Dark series!\n⚡ LIKE & SUBSCRIBE for Part 2!\n\n#shorts #roblox #robloxstory #monster #horror #animation #gaming #taleblox #riyo3d",
        "tags": ["shorts", "roblox", "roblox shorts", "roblox story", "monster", "dark", "horror", "animation", "taleblox", "riyo 3d"]
    },
    "SHORT_15_One_Cereal_Box_Contains_a_Golden_Ticket.mp4": {
        "title": "One Cereal Box Contains A Golden Ticket! 🥣🎫 (Roblox 3D Story) #shorts #roblox",
        "description": "Only ONE box of cereal in the entire country has the Billionaire Golden Ticket! 🎫✨\nI bought the very last dusty box on the bottom shelf... Look what was inside! 😱💎\n\n🎬 Watch till the end to see the reward!\n⚡ SUBSCRIBE to TaleBlox!\n\n#shorts #roblox #robloxstory #goldenticket #cereal #animation #taleblox #riyo3d",
        "tags": ["shorts", "roblox", "roblox shorts", "roblox story", "golden ticket", "animation", "gaming", "taleblox", "riyo 3d"]
    },
    "SHORT_16_You_Get_Paid_for_Being_Embarrassed.mp4": {
        "title": "You Get Paid For Being Embarrassed! 😳💸 (Roblox 3D Story) #shorts #roblox",
        "description": "Every time something cringe or humiliating happens to you, your bank balance EXPLODES! 💸💥\nWatch what this guy did in front of the whole school auditorium! 😭🎒\n\n🎬 Watch till the end!\n⚡ LIKE & SUBSCRIBE to TaleBlox!\n\n#shorts #roblox #robloxstory #cringe #embarrassed #rich #gaming #taleblox #riyo3d",
        "tags": ["shorts", "roblox", "roblox shorts", "roblox story", "embarrassed", "gaming", "animation", "taleblox", "riyo 3d"]
    }
}

def generate_default_metadata(filename):
    name = filename.replace('.mp4', '')
    m = re.match(r'SHORT_(\d+)_(.*)', name)
    if m:
        num = m.group(1)
        raw = m.group(2).replace('_', ' ').strip()
        # Clean up trailing 'Pa' or 'Part'
        if raw.endswith(' Pa'):
            raw = raw[:-3] + ' (Part 1)'
        title_str = raw.title()
        title = f"{title_str} 🎮🔥 (Roblox 3D Story) #shorts #roblox"
        if len(title) > 95:
            title = f"{title_str} #shorts #roblox"
    else:
        title = f"{name} #shorts #roblox"

    description = f"""{title}

🎬 Watch till the very end to see what happens next!
⚡ LIKE, SHARE & SUBSCRIBE TO TALEBLOX (RIYO 3D) FOR DAILY 3D STORIES!
🔔 Turn on ALL notifications so you never miss an episode!

💬 COMMENT BELOW your favorite part! 👇

---
#shorts #roblox #robloxstory #animation #3danimation #gaming #taleblox #riyo3d #fyp #viral
"""
    tags = ["shorts", "roblox", "roblox shorts", "roblox story", "animation", "3d animation", "gaming", "taleblox", "riyo 3d", "viral shorts"]
    return {"title": title, "description": description, "tags": tags}

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    # Initial seed ledger
    return {
        "SHORT_1_Throw_Food_For_Pets_Part1.mp4": {"status": "published", "video_id": "existing"},
        "SHORT_2_100_Year_Ocean_Tide.mp4": {"status": "published", "video_id": "existing"},
        "SHORT_3_The_Colossus_Awakens_Part2.mp4": {"status": "published", "video_id": "existing"},
        "SHORT_4_Video_Game_Town_Level_999.mp4": {"status": "published", "video_id": "existing"},
        "SHORT_5_Ages_Backwards_Grandpa_Egg.mp4": {"status": "published", "video_id": "existing"},
        "SHORT_11_The_Rich_Live_Above_The_Clouds.mp4": {"status": "published", "video_id": "oxX9R_XLZd4"},
        "SHORT_12_Touching_the_Ground_Costs_10.mp4": {"status": "scheduled", "video_id": "n8EViLFGln0", "publish_at": "2026-11-18T03:30:00Z"}
    }

def save_ledger(ledger):
    with open(LEDGER_FILE, 'w', encoding='utf-8') as f:
        json.dump(ledger, f, indent=2)

def generate_schedule_slots(count=30):
    """
    Generates peak schedule slots starting from today afternoon:
    - Daily slot 1: 11:30 AM IST (06:00 UTC)
    - Daily slot 2: 05:00 PM IST (11:30 UTC)
    """
    slots = []
    # Current time: 2026-11-18 10:05 IST
    base_date = datetime(2026, 11, 18)
    
    # Slot today at 5:00 PM IST (11:30 UTC)
    slots.append({
        "label": "Today (Wed Nov 18) @ 5:00 PM IST",
        "iso_utc": "2026-11-18T11:30:00Z"
    })
    
    current_day = base_date + timedelta(days=1)
    for _ in range(count):
        day_str = current_day.strftime("%a %b %d")
        # Morning slot: 11:30 AM IST -> 06:00 UTC (11:00 AM on weekends)
        is_weekend = current_day.weekday() in [5, 6]
        m_time_ist = "11:00 AM" if is_weekend else "11:30 AM"
        m_utc = "05:30:00Z" if is_weekend else "06:00:00Z"
        
        slots.append({
            "label": f"{day_str} @ {m_time_ist} IST",
            "iso_utc": f"{current_day.strftime('%Y-%m-%d')}T{m_utc}"
        })
        
        # Evening slot: 5:00 PM IST -> 11:30 UTC
        slots.append({
            "label": f"{day_str} @ 5:00 PM IST",
            "iso_utc": f"{current_day.strftime('%Y-%m-%d')}T11:30:00Z"
        })
        current_day += timedelta(days=1)
        
    return slots

def get_authenticated_youtube():
    with open(TOKEN_PICKLE, 'rb') as token:
        credentials = pickle.load(token)

    if not credentials.valid and credentials.expired and credentials.refresh_token:
        print("[*] Refreshing YouTube OAuth token...")
        credentials.refresh(Request())
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(credentials, token)

    return build('youtube', 'v3', credentials=credentials)

def schedule_batch(max_uploads=5):
    ledger = load_ledger()
    slots = generate_schedule_slots(count=30)
    
    # Find all master files sorted numerically
    def get_num(fname):
        m = re.search(r'SHORT_(\d+)', fname)
        return int(m.group(1)) if m else 999

    all_files = sorted([f for f in os.listdir(MASTER_DIR) if f.endswith('.mp4')], key=get_num)
    
    # Filter pending files
    pending_files = [f for f in all_files if f not in ledger or ledger[f].get('status') not in ['published', 'scheduled']]
    print(f"Total master videos: {len(all_files)}")
    print(f"Already in ledger: {len(ledger)}")
    print(f"Pending to schedule: {len(pending_files)}")
    
    if not pending_files:
        print("[!] No pending videos found!")
        return

    # Count how many slots are already taken
    scheduled_count = len([v for v in ledger.values() if v.get('status') == 'scheduled' and v.get('publish_at', '') >= '2026-11-18T11:30:00Z'])
    available_slots = slots[scheduled_count:]
    
    youtube = get_authenticated_youtube()
    
    uploads_done = 0
    for idx, filename in enumerate(pending_files):
        if uploads_done >= max_uploads:
            print(f"\n[*] Reached max uploads limit for this run ({max_uploads}). Saving state...")
            break
            
        slot = available_slots[uploads_done]
        meta = CUSTOM_METADATA.get(filename, generate_default_metadata(filename))
        video_path = os.path.join(MASTER_DIR, filename)
        
        print("\n" + "="*60)
        print(f"[{uploads_done+1}/{max_uploads}] Scheduling: {filename}")
        print(f"Title: {meta['title']}")
        print(f"Slot: {slot['label']} ({slot['iso_utc']})")
        print("="*60)
        
        body = {
            'snippet': {
                'title': meta['title'],
                'description': meta['description'],
                'tags': meta['tags'],
                'categoryId': '20' # Gaming
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': slot['iso_utc'],
                'selfDeclaredMadeForKids': False
            }
        }
        
        try:
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
                    print(f"    Progress: {int(status.progress() * 100)}%", flush=True)
                    
            video_id = response['id']
            print(f"[+] SUCCESS! Video ID: {video_id}")
            print(f"    Watch URL: https://youtu.be/{video_id}")
            print(f"    Shorts URL: https://www.youtube.com/shorts/{video_id}")
            
            ledger[filename] = {
                "status": "scheduled",
                "video_id": video_id,
                "title": meta['title'],
                "publish_at": slot['iso_utc'],
                "slot_label": slot['label'],
                "scheduled_at": datetime.utcnow().isoformat() + "Z"
            }
            save_ledger(ledger)
            uploads_done += 1
            
        except HttpError as e:
            if "quotaExceeded" in str(e):
                print(f"\n[!] YouTube API daily quota reached (10,000 units limit).")
                print("    Remaining videos will be processed automatically after quota resets!")
                break
            else:
                print(f"\n[!] HttpError uploading {filename}: {e}")
                break
        except Exception as e:
            print(f"\n[!] Unexpected error: {e}")
            break

    print("\n" + "#"*60)
    print(f"FINISHED RUN: {uploads_done} videos successfully scheduled!")
    print(f"Persistent ledger updated: {LEDGER_FILE}")
    print("#"*60)

if __name__ == '__main__':
    max_u = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    schedule_batch(max_uploads=max_u)
