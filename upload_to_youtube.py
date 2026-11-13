"""
YouTube Automatic Video Uploader with Scheduling Support
Uses official Google YouTube Data API v3.
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

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
WORKSPACE_DIR = r"D:\Antigravity\Pro"
CLIENT_SECRETS_FILE = os.path.join(WORKSPACE_DIR, 'client_secrets.json')
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')

def get_authenticated_service():
    if not os.path.exists(TOKEN_PICKLE):
        print(f"[!] Error: {TOKEN_PICKLE} not found.", flush=True)
        sys.exit(1)

    with open(TOKEN_PICKLE, 'rb') as token:
        credentials = pickle.load(token)

    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            print("[*] Refreshing expired YouTube token...", flush=True)
            credentials.refresh(Request())
            with open(TOKEN_PICKLE, 'wb') as token:
                pickle.dump(credentials, token)

    return build('youtube', 'v3', credentials=credentials)

def upload_video(file_path, title, description, tags, category_id="28", privacy_status="public", publish_at=None):
    if not os.path.exists(file_path):
        print(f"[!] Video file not found: {file_path}", flush=True)
        return

    youtube = get_authenticated_service()

    status_dict = {
        'selfDeclaredMadeForKids': False
    }

    if publish_at:
        # Scheduled upload requires private + publishAt
        status_dict['privacyStatus'] = 'private'
        status_dict['publishAt'] = publish_at
        print(f"[+] Video will be SCHEDULED to go live at: {publish_at}", flush=True)
    else:
        status_dict['privacyStatus'] = privacy_status

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': status_dict
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
        print("\n" + "="*50, flush=True)
        if publish_at:
            print(f"[SCHEDULED] Video uploaded and scheduled for {publish_at}!", flush=True)
        else:
            print("[SUCCESS] Video published to YouTube!", flush=True)
            
        print(f"Watch URL: https://youtu.be/{video_id}", flush=True)
        print(f"Shorts URL: https://www.youtube.com/shorts/{video_id}", flush=True)
        print("="*50 + "\n", flush=True)
        return video_id
    except HttpError as e:
        print(f"\n[!] YouTube API error: {e}", flush=True)
    except Exception as e:
        print(f"\n[!] Unexpected error during upload: {e}", flush=True)

if __name__ == "__main__":
    video_file = os.path.join(WORKSPACE_DIR, "ai_tools_cost_collapse.mp4")
    video_title = "I Cut Production Costs by 80% With Two AI Tools #shorts"
    video_desc = "Test upload"
    video_tags = ["shorts", "test"]
    # upload_video(video_file, video_title, video_desc, video_tags)
