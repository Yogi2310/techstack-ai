import os, sys, pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

WORKSPACE_DIR = r"D:\Antigravity\Pro"
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')

with open(TOKEN_PICKLE, 'rb') as token:
    credentials = pickle.load(token)

youtube = build('youtube', 'v3', credentials=credentials)

# List of non-tech video IDs discovered from public shorts:
non_tech_ids = [
    ("cu5bNnuuSV4", "O Captain! My Captain!"),
    ("M_tPkYqNtLs", "Chill Lo-fi #finance"),
    ("iL3PchHOlPg", "🎵 Mysterious #quotes"),
    ("N7AeiKm8by0", "poems · 🎵 Dreamy Ambient"),
    ("AOPdzwJL33M", "Harlem"),
    ("pYxcBfXc3wg", "#viralshort #motivation"),
    ("D0m-CHnM6HY", "PM-CARES Jay Modi"),
    ("v643jQ8CBBQ", "trending Screen Time"),
    ("qav4mvQ08E0", "Your limitation—it's only your imagination"),
    ("ozTgU3ZwRik", "Push yourself, because no one else is can do"),
    ("S5DQNjHO2wA", "Good thoughts"),
    ("oq_GwcVXFxA", "Motivate#viral"),
    ("RwhXQNGqftc", "Motivation Great things never come from comfort"),
    ("N68DjeNFKCs", "Uplifting #viral #money"),
    ("X2dQ-ksQTVw", "motivation Uplifting"),
    ("04sCIDETrGg", "facts Mysterious"),
    ("g6iWkAOeQeg", "dangerous to corrupt politician"),
    ("xjdA1zsyLVA", "Trending Energetic"),
    ("JVSY5-_h6fA", "Pollical Facts and awareness")
]

print(f"[+] Testing update on first non-tech video: {non_tech_ids[0][1]} ({non_tech_ids[0][0]})...")

try:
    # Test setting privacyStatus to 'unlisted'
    resp = youtube.videos().update(
        part='status',
        body={
            'id': non_tech_ids[0][0],
            'status': {
                'privacyStatus': 'unlisted',
                'selfDeclaredMadeForKids': False
            }
        }
    ).execute()
    print("[✓] Successfully updated video to unlisted:", resp.get('id'))
except HttpError as e:
    print(f"[!] API HttpError: {e}")
except Exception as e:
    print(f"[!] Error: {e}")
