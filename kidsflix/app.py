import os
import json
import re
import threading
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect
import yt_dlp

# ─── Google / YouTube ────────────────────────────────────────────────────────
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

app = Flask(__name__)
app.secret_key = os.urandom(24)

BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / 'downloads'
DOWNLOADS_DIR.mkdir(exist_ok=True)
CLIENT_SECRETS = BASE_DIR / 'client_secrets.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# ─── Progress tracking ────────────────────────────────────────────────────────
download_progress = {}   # { video_id: { status, percent, filename } }
upload_progress   = {}   # { filename: { status, video_url } }


# ─── ROUTES ──────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ─── DOWNLOAD ────────────────────────────────────────────────────────────────
@app.route('/api/download', methods=['POST'])
def api_download():
    data = request.get_json(force=True)
    video_id = data.get('videoId', '').strip()
    title    = data.get('title', video_id).strip()

    if not video_id:
        return jsonify({'error': 'videoId required'}), 400

    # Sanitise title for filename
    safe_title = re.sub(r'[^\w\-_. ]', '_', title)[:80]
    out_tmpl = str(DOWNLOADS_DIR / f'{safe_title}_[{video_id}].%(ext)s')

    # Check if already downloaded
    existing = _find_file(video_id)
    if existing:
        return jsonify({'status': 'exists', 'filename': existing.name, 'path': str(existing)})

    download_progress[video_id] = {'status': 'starting', 'percent': 0, 'filename': None}

    def do_download():
        def progress_hook(d):
            if d['status'] == 'downloading':
                pct_str = d.get('_percent_str', '0%').strip().replace('%', '')
                try:
                    download_progress[video_id]['percent'] = float(pct_str)
                except ValueError:
                    pass
                download_progress[video_id]['status'] = 'downloading'
            elif d['status'] == 'finished':
                download_progress[video_id]['status'] = 'processing'

        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
            'outtmpl': out_tmpl,
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.youtube.com/shorts/{video_id}'])
            found = _find_file(video_id)
            if found:
                download_progress[video_id] = {'status': 'done', 'percent': 100, 'filename': found.name}
            else:
                download_progress[video_id] = {'status': 'error', 'percent': 0, 'filename': None}
        except Exception as e:
            download_progress[video_id] = {'status': 'error', 'percent': 0, 'filename': None, 'error': str(e)}

    threading.Thread(target=do_download, daemon=True).start()
    return jsonify({'status': 'started', 'videoId': video_id})


@app.route('/api/download/progress/<video_id>')
def api_download_progress(video_id):
    info = download_progress.get(video_id, {'status': 'unknown', 'percent': 0})
    return jsonify(info)


@app.route('/api/downloads')
def api_list_downloads():
    files = []
    for f in sorted(DOWNLOADS_DIR.iterdir(), key=lambda x: -x.stat().st_mtime):
        if f.is_file() and f.suffix.lower() in ('.mp4', '.webm', '.mkv'):
            # Extract video_id from filename [xxxx]
            m = re.search(r'\[([a-zA-Z0-9_-]{11})\]', f.name)
            vid_id = m.group(1) if m else None
            size_mb = round(f.stat().st_size / (1024 * 1024), 2)
            files.append({
                'filename': f.name,
                'size_mb':  size_mb,
                'videoId':  vid_id,
                'uploaded': upload_progress.get(f.name, {}).get('status') == 'done',
                'ytUrl':    upload_progress.get(f.name, {}).get('video_url'),
            })
    return jsonify({'downloads': files})


@app.route('/api/download/<path:filename>', methods=['DELETE'])
def api_delete_download(filename):
    fpath = DOWNLOADS_DIR / filename
    if fpath.exists() and fpath.is_file():
        fpath.unlink()
        return jsonify({'deleted': True})
    return jsonify({'error': 'not found'}), 404


@app.route('/api/file/<path:filename>')
def serve_download(filename):
    return send_from_directory(str(DOWNLOADS_DIR), filename, as_attachment=True)


# ─── YOUTUBE UPLOAD ──────────────────────────────────────────────────────────
@app.route('/auth')
def auth():
    if not CLIENT_SECRETS.exists():
        return jsonify({'error': 'client_secrets.json not found. Please add it to the kidsflix folder.'}), 400
    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRETS),
        scopes=SCOPES,
        redirect_uri=request.host_url.rstrip('/') + '/oauth2callback'
    )
    auth_url, state = flow.authorization_url(prompt='consent', access_type='offline')
    session['oauth_state'] = state
    session['upload_file'] = request.args.get('file', '')
    return redirect(auth_url)


@app.route('/oauth2callback')
def oauth2callback():
    if not CLIENT_SECRETS.exists():
        return 'client_secrets.json missing', 400
    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRETS),
        scopes=SCOPES,
        state=session.get('oauth_state'),
        redirect_uri=request.host_url.rstrip('/') + '/oauth2callback'
    )
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    session['credentials'] = {
        'token':         creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri':     creds.token_uri,
        'client_id':     creds.client_id,
        'client_secret': creds.client_secret,
        'scopes':        list(creds.scopes),
    }
    # Redirect back to app with upload pending
    filename = session.get('upload_file', '')
    return redirect(f'/?upload={filename}')


@app.route('/api/upload', methods=['POST'])
def api_upload():
    data = request.get_json(force=True)
    filename    = data.get('filename', '').strip()
    title       = data.get('title', filename).strip()
    description = data.get('description', '').strip()
    tags        = data.get('tags', ['kids', 'cartoon', 'shorts', 'educational'])

    if not filename:
        return jsonify({'error': 'filename required'}), 400

    fpath = DOWNLOADS_DIR / filename
    if not fpath.exists():
        return jsonify({'error': 'File not found'}), 404

    creds_data = session.get('credentials')
    if not creds_data:
        # Need OAuth — return auth URL
        return jsonify({'auth_required': True,
                        'auth_url': f'/auth?file={filename}'}), 401

    upload_progress[filename] = {'status': 'uploading', 'video_url': None}

    def do_upload():
        try:
            creds = Credentials(**{k: creds_data[k] for k in
                                   ('token','refresh_token','token_uri','client_id','client_secret')},
                                scopes=creds_data['scopes'])
            youtube = build('youtube', 'v3', credentials=creds)

            # Add #Shorts to title & description
            yt_title = (title[:95] + ' #Shorts') if '#Shorts' not in title else title[:100]
            yt_desc  = f'{description}\n\n#Shorts #Kids #Educational #KidsFlix'
            all_tags = list(set(tags + ['Shorts', 'kids', 'educational', 'kidsflix']))

            body = {
                'snippet': {
                    'title':       yt_title,
                    'description': yt_desc,
                    'tags':        all_tags,
                    'categoryId':  '27'  # Education
                },
                'status': {'privacyStatus': 'public'}
            }

            media = MediaFileUpload(str(fpath), mimetype='video/mp4', resumable=True)
            req   = youtube.videos().insert(part='snippet,status', body=body, media_body=media)

            response = None
            while response is None:
                _, response = req.next_chunk()

            vid_id = response.get('id', '')
            upload_progress[filename] = {
                'status':    'done',
                'video_url': f'https://www.youtube.com/shorts/{vid_id}',
            }
        except Exception as e:
            upload_progress[filename] = {'status': 'error', 'error': str(e)}

    threading.Thread(target=do_upload, daemon=True).start()
    return jsonify({'status': 'uploading', 'filename': filename})


@app.route('/api/upload/progress/<path:filename>')
def api_upload_progress(filename):
    return jsonify(upload_progress.get(filename, {'status': 'unknown'}))


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def _find_file(video_id):
    for f in DOWNLOADS_DIR.iterdir():
        if f.is_file() and video_id in f.name:
            return f
    return None


if __name__ == '__main__':
    # Allow OAuth redirect over http locally
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True, port=5000, threaded=True)
