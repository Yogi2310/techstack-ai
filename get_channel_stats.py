import os, sys, pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

with open(r"D:\Antigravity\Pro\youtube_token.pickle", "rb") as f:
    creds = pickle.load(f)

if not creds.valid and creds.expired and creds.refresh_token:
    creds.refresh(Request())

youtube = build("youtube", "v3", credentials=creds)

ch_res = youtube.channels().list(mine=True, part="snippet,statistics,contentDetails").execute()
items = ch_res.get("items", [])
if items:
    ch = items[0]
    print("CHANNEL:", ch["snippet"]["title"], ch["snippet"].get("customUrl", ""))
    print("TOTAL STATS:", ch["statistics"])
    uploads_playlist = ch["contentDetails"]["relatedPlaylists"]["uploads"]

    pl_res = youtube.playlistItems().list(playlistId=uploads_playlist, part="snippet,contentDetails", maxResults=20).execute()
    v_ids = [it["contentDetails"]["videoId"] for it in pl_res.get("items", [])]

    v_res = youtube.videos().list(id=",".join(v_ids), part="snippet,statistics,status").execute()
    print("\nRECENT VIDEOS:")
    for v in v_res.get("items", []):
        sn = v["snippet"]
        st = v["statistics"]
        status = v["status"]
        print(f"[{status.get('privacyStatus')}] {sn['title'][:55]} | Views: {st.get('viewCount', 0)} | Likes: {st.get('likeCount', 0)} | Published: {sn['publishedAt']}")
