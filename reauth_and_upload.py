import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

WORKSPACE_DIR = r"D:\Antigravity\Pro"
CLIENT_SECRETS_FILE = os.path.join(WORKSPACE_DIR, 'client_secrets.json')
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')
VIDEO_FILE = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\LEGO_AGENT_FIXING_SYSTEMS_16x9.mp4"

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

TITLE = "🧱 When AI Agents Fix Production at 2 AM (LEGO Edition) 🤖 | Autonomous Dev Loop"

DESCRIPTION = """When the server rack crashes at 2 AM and alerts start firing, this Autonomous 3D LEGO Minifigure Agent springs into action! 🤖🧱

Watch the full closed-loop autonomous repair:
0:00 - Critical server connection leak alert
0:10 - Laser diagnostic & 1x2 hotfix brick snap-in
0:22 - Cyber terminal typing & 42 regression tests pass
0:32 - Technic master deployment lever pull & power surge
0:42 - Cloud payload rocket launch & victory celebration!

Would you trust an AI agent with your production servers? Drop your thoughts below! 👇
Like & Subscribe for more autonomous agentic workflows and animations.

#ai #agents #lego #softwareengineering #devops #automation #coding #python #tech #animation
"""

TAGS = [
    "ai agents",
    "autonomous agents",
    "lego animation",
    "software engineering",
    "coding",
    "devops",
    "cloud computing",
    "lego brickfilm",
    "tech animation",
    "ai automation",
    "programming",
    "antigravity",
    "developer humor"
]

def authenticate_youtube():
    credentials = None
    if os.path.exists(TOKEN_PICKLE):
        try:
            with open(TOKEN_PICKLE, 'rb') as token:
                credentials = pickle.load(token)
            if credentials and credentials.valid:
                return credentials
            if credentials and credentials.expired and credentials.refresh_token:
                print("[*] Attempting token refresh...", flush=True)
                credentials.refresh(Request())
                with open(TOKEN_PICKLE, 'wb') as token:
                    pickle.dump(credentials, token)
                return credentials
        except Exception as e:
            print(f"[*] Cached token refresh failed ({e}). Re-authorizing...", flush=True)
            # Remove or backup invalid token
            try:
                os.replace(TOKEN_PICKLE, TOKEN_PICKLE + ".bak")
            except Exception:
                pass

    print("\n" + "="*60, flush=True)
    print("[*] Launching browser for 1-click Google authorization...", flush=True)
    print("="*60, flush=True)
    
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        SCOPES,
        redirect_uri='http://localhost:8088/'
    )
    
    try:
        credentials = flow.run_local_server(port=8088, open_browser=True)
    except Exception as e:
        print(f"[*] Local server error ({e}). Trying port 0...", flush=True)
        credentials = flow.run_local_server(port=0, open_browser=True)

    with open(TOKEN_PICKLE, 'wb') as token:
        pickle.dump(credentials, token)
        
    print("\n[✓] Fresh YouTube authorization token saved successfully!\n", flush=True)
    return credentials

def upload():
    creds = authenticate_youtube()
    youtube = build('youtube', 'v3', credentials=creds)

    body = {
        'snippet': {
            'title': TITLE,
            'description': DESCRIPTION,
            'tags': TAGS,
            'categoryId': '28'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True, mimetype="video/mp4")
    print(f"[+] Uploading '{TITLE}' ({os.path.getsize(VIDEO_FILE)/(1024*1024):.2f} MB)...", flush=True)

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
    print("\n" + "="*60, flush=True)
    print("🎉 SUCCESS! Video published live to YouTube!", flush=True)
    print(f"👉 Watch URL:  https://youtu.be/{video_id}", flush=True)
    print(f"👉 Shorts URL: https://www.youtube.com/shorts/{video_id}", flush=True)
    print("="*60 + "\n", flush=True)
    return video_id

if __name__ == '__main__':
    upload()
