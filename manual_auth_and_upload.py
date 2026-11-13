"""
Interactive YouTube Uploader with direct URL fallback.
"""

import os
import sys

# Allow HTTP localhost callback without InsecureTransportError
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import pickle
import urllib.parse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
WORKSPACE_DIR = r"D:\Antigravity\Pro"
CLIENT_SECRETS_FILE = os.path.join(WORKSPACE_DIR, 'client_secrets.json')
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')

def get_authenticated_service():
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            credentials = pickle.load(token)
        return build('youtube', 'v3', credentials=credentials)

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        SCOPES,
        redirect_uri='http://localhost:8088/'
    )

    try:
        print("\n>>> Starting local authorization server on port 8088...", flush=True)
        credentials = flow.run_local_server(port=8088, open_browser=True)
    except Exception as e:
        print(f"\n[*] Local server failed ({e}). Using direct URL mode...", flush=True)
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        print("\n" + "="*70, flush=True)
        print("Please visit this URL in your browser:", flush=True)
        print(auth_url, flush=True)
        print("="*70, flush=True)
        redirect_url = input("\nPaste the full URL from your browser address bar: ").strip()
        flow.fetch_token(authorization_response=redirect_url)
        credentials = flow.credentials

    with open(TOKEN_PICKLE, 'wb') as token:
        pickle.dump(credentials, token)
    print("\n[✓] Credentials saved successfully!", flush=True)
    return build('youtube', 'v3', credentials=credentials)

def upload_video(file_path, title, description, tags, category_id="28", privacy_status="public"):
    youtube = get_authenticated_service()

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")

    print(f"\n[+] Uploading '{title}' to YouTube...", flush=True)
    try:
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
        print(f"\n" + "="*50, flush=True)
        print(f"🎉 SUCCESS! Video published to YouTube!", flush=True)
        print(f"👉 Watch URL: https://youtu.be/{video_id}", flush=True)
        print("="*50 + "\n", flush=True)
        return video_id
    except HttpError as e:
        if "accessNotConfigured" in str(e) or "has not been used in project" in str(e):
            print("\n[!] YouTube Data API v3 is not enabled in your Google Cloud Project yet.", flush=True)
            print("👉 Enable it here in 1 click: https://console.cloud.google.com/apis/library/youtube.googleapis.com", flush=True)
        else:
            print(f"\n[!] YouTube API error: {e}", flush=True)
    except Exception as e:
        print(f"\n[!] Unexpected error during upload: {e}", flush=True)

if __name__ == "__main__":
    video_file = os.path.join(WORKSPACE_DIR, "ai_tools_cost_collapse.mp4")
    video_title = "I Cut Production Costs by 80% With Two AI Tools #shorts"
    video_desc = """I replaced three freelancers with two AI tools and cut monthly production spend by 80%.

Tools used:
- ElevenLabs (Voice generation)
- Midjourney (Visuals)

#shorts #aitools #contentcreator #productivity"""
    video_tags = ["ai tools", "elevenlabs", "midjourney", "shorts", "content creator", "save money"]
    
    upload_video(video_file, video_title, video_desc, video_tags)
