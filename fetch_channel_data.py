import os, sys, pickle, json
from googleapiclient.discovery import build

WORKSPACE_DIR = r"D:\Antigravity\Pro"
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')
CHANNEL_ID = "UCHicNBr7Ytwd7y2wFUKX_XA"

with open(TOKEN_PICKLE, 'rb') as token:
    credentials = pickle.load(token)

youtube = build('youtube', 'v3', credentials=credentials)

# 1. Fetch Channel Info
print("[+] Querying channel info...")
ch_resp = youtube.channels().list(
    part='snippet,statistics,brandingSettings,contentDetails',
    id=CHANNEL_ID
).execute()

ch_items = ch_resp.get('items', [])
if not ch_items:
    # Try querying "mine=True"
    print("[*] ID query returned empty, querying mine=True...")
    ch_resp = youtube.channels().list(
        part='snippet,statistics,brandingSettings,contentDetails',
        mine=True
    ).execute()
    ch_items = ch_resp.get('items', [])

if ch_items:
    channel = ch_items[0]
    print(f"Channel Title: {channel['snippet'].get('title')}")
    print(f"Subscribers: {channel['statistics'].get('subscriberCount')}")
    print(f"Total Views: {channel['statistics'].get('viewCount')}")
    print(f"Total Videos: {channel['statistics'].get('videoCount')}")
    print(f"Custom URL: {channel['snippet'].get('customUrl')}")
    print(f"Description:\n{channel['snippet'].get('description')}\n")

    # 2. Fetch Uploaded Videos
    uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']
    print(f"[+] Fetching recent videos from uploads playlist: {uploads_playlist_id}...")
    
    playlist_resp = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=20
    ).execute()

    videos = []
    video_ids = []
    for item in playlist_resp.get('items', []):
        v_id = item['contentDetails']['videoId']
        video_ids.append(v_id)
        videos.append({
            'videoId': v_id,
            'title': item['snippet']['title'],
            'publishedAt': item['snippet']['publishedAt'],
            'description': item['snippet']['description'][:200]
        })

    # Fetch statistics and details for these videos
    if video_ids:
        v_resp = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(video_ids)
        ).execute()

        stat_map = {}
        for vi in v_resp.get('items', []):
            stat_map[vi['id']] = {
                'views': vi['statistics'].get('viewCount', '0'),
                'likes': vi['statistics'].get('likeCount', '0'),
                'comments': vi['statistics'].get('commentCount', '0'),
                'duration': vi['contentDetails'].get('duration', ''),
                'tags': vi['snippet'].get('tags', [])
            }

        for v in videos:
            v_id = v['videoId']
            if v_id in stat_map:
                v.update(stat_map[v_id])

    # Save to JSON for analysis
    output_path = os.path.join(WORKSPACE_DIR, "channel_audit_data.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'channel': channel,
            'videos': videos
        }, f, indent=2)

    print(f"[+] Saved audit data for {len(videos)} videos to: {output_path}")

else:
    print("[!] Could not retrieve channel items.")
