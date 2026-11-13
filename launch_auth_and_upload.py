import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import pickle
import wsgiref.simple_server
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow, _RedirectWSGIApp, _WSGIRequestHandler
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

WORKSPACE_DIR = r"D:\Antigravity\Pro"
CLIENT_SECRETS_FILE = os.path.join(WORKSPACE_DIR, 'client_secrets.json')
TOKEN_PICKLE = os.path.join(WORKSPACE_DIR, 'youtube_token.pickle')
VIDEO_FILE = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\LEGO_AGENT_FIXING_SYSTEMS_16x9.mp4"
URL_FILE = os.path.join(WORKSPACE_DIR, "auth_url.txt")

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

TITLE = "🧱 When AI Agents Fix Production at 2 AM (LEGO Edition) 🤖 | Autonomous Dev Loop"

DESCRIPTION = """When the server rack crashes at 2 AM and alerts start firing, this Autonomous 3D LEGO Minifigure Agent springs into action! 🤖🧱

Channel: https://studio.youtube.com/channel/UCHicNBr7Ytwd7y2wFUKX_XA

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

def run_flushed_local_server(flow, port=8088):
    host = "localhost"
    wsgi_app = _RedirectWSGIApp("Authorization successful! You can close this tab and return to Antigravity.")
    wsgiref.simple_server.WSGIServer.allow_reuse_address = True
    local_server = wsgiref.simple_server.make_server(host, port, wsgi_app, handler_class=_WSGIRequestHandler)

    flow.redirect_uri = f"http://{host}:{local_server.server_port}/"
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

    # Save to file
    with open(URL_FILE, 'w', encoding='utf-8') as uf:
        uf.write(auth_url)

    print("\n" + "="*70, flush=True)
    print("GOOGLE_AUTH_URL_START", flush=True)
    print(auth_url, flush=True)
    print("GOOGLE_AUTH_URL_END", flush=True)
    print("="*70 + "\n", flush=True)

    try:
        webbrowser.open(auth_url, new=1, autoraise=True)
    except Exception as e:
        print(f"Browser launch note: {e}", flush=True)

    print("[*] Waiting for user approval on localhost:8088...", flush=True)
    local_server.handle_request()

    try:
        auth_response = wsgi_app.last_request_uri.replace("http://", "https://")
    except AttributeError as e:
        print(f"[!] Server error: {e}", flush=True)
        local_server.server_close()
        sys.exit(1)

    flow.fetch_token(authorization_response=auth_response)
    local_server.server_close()
    return flow.credentials

def main():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = run_flushed_local_server(flow, port=8088)

    with open(TOKEN_PICKLE, 'wb') as f:
        pickle.dump(creds, f)

    print("\n[✓] Fresh YouTube token saved to pickle!", flush=True)
    print(f"[+] Starting YouTube upload to channel for: {VIDEO_FILE}", flush=True)

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

if __name__ == '__main__':
    main()
