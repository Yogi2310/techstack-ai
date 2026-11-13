"""
AutoMail Downloader — Flask Server
"""
import os
import json
import hashlib
import threading
from pathlib import Path

from flask import Flask, request, jsonify, render_template, send_from_directory

import cache_db
import mail_reader
import downloader

app = Flask(__name__)
app.secret_key = os.urandom(24)

BASE_DIR      = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / 'downloads'
DOWNLOADS_DIR.mkdir(exist_ok=True)

# ── In-memory state ───────────────────────────────────────────────────────────
_conn = {
    'connected': False,
    'email':     None,
    'host':      None,
    'port':      993,
    'password':  None,
    'error':     None,
}
_dl_progress = {}   # { url_hash: progress_dict }
_auto_poll   = {'enabled': False, 'interval': 300, 'timer': None}


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ── Mail connection ────────────────────────────────────────────────────────────
@app.route('/api/guess-host', methods=['POST'])
def api_guess_host():
    email_addr = request.get_json(force=True).get('email', '')
    host, port = mail_reader.guess_host(email_addr)
    return jsonify({'host': host, 'port': port})


@app.route('/api/connect', methods=['POST'])
def api_connect():
    data     = request.get_json(force=True)
    email_addr = data.get('email', '').strip()
    password   = data.get('password', '').strip()
    host       = data.get('host', '').strip()
    port       = int(data.get('port', 993))

    if not email_addr or not password:
        return jsonify({'error': 'Email and password required'}), 400

    if not host:
        host, port = mail_reader.guess_host(email_addr)

    ok, err = mail_reader.test_connection(host, port, email_addr, password)
    if ok:
        _conn.update({'connected': True, 'email': email_addr,
                      'host': host, 'port': port, 'password': password, 'error': None})
        return jsonify({'connected': True, 'email': email_addr, 'host': host})
    else:
        _conn.update({'connected': False, 'error': str(err)})
        return jsonify({'error': str(err)}), 400


@app.route('/api/disconnect', methods=['POST'])
def api_disconnect():
    _conn.update({'connected': False, 'email': None, 'host': None, 'password': None})
    return jsonify({'disconnected': True})


@app.route('/api/status')
def api_status():
    return jsonify({
        'connected':   _conn['connected'],
        'email':       _conn['email'],
        'host':        _conn['host'],
        'error':       _conn['error'],
        'auto_poll':   _auto_poll['enabled'],
        'poll_interval': _auto_poll['interval'],
    })


# ── Email fetching ────────────────────────────────────────────────────────────
@app.route('/api/emails')
def api_emails():
    if not _conn['connected']:
        return jsonify({'error': 'Not connected to mailbox'}), 401

    folder      = request.args.get('folder', 'INBOX')
    limit       = int(request.args.get('limit', 30))
    unread_only = request.args.get('unread', 'false').lower() == 'true'

    emails = mail_reader.fetch_emails(
        _conn['host'], _conn['port'],
        _conn['email'], _conn['password'],
        folder=folder, limit=limit, unread_only=unread_only,
    )

    results = []
    for em in emails:
        cached = cache_db.get_email(em['msg_id'])
        em['cached'] = cached is not None
        if not cached:
            cache_db.save_email(em)
        results.append(em)

    return jsonify({'emails': results, 'count': len(results), 'folder': folder})


@app.route('/api/folders')
def api_folders():
    if not _conn['connected']:
        return jsonify({'folders': ['INBOX']}), 200
    folders = mail_reader.list_folders(_conn['host'], _conn['port'], _conn['email'], _conn['password'])
    return jsonify({'folders': folders})


# ── Auto-poll ─────────────────────────────────────────────────────────────────
def _run_poll():
    if not _conn['connected']:
        return
    mail_reader.fetch_emails(
        _conn['host'], _conn['port'],
        _conn['email'], _conn['password'],
        limit=20,
    )
    if _auto_poll['enabled']:
        t = threading.Timer(_auto_poll['interval'], _run_poll)
        t.daemon = True
        _auto_poll['timer'] = t
        t.start()


@app.route('/api/autopoll', methods=['POST'])
def api_autopoll():
    data = request.get_json(force=True)
    enable   = data.get('enable', False)
    interval = int(data.get('interval', 300))
    _auto_poll['interval'] = max(60, interval)

    if enable and not _auto_poll['enabled']:
        _auto_poll['enabled'] = True
        _run_poll()
    elif not enable:
        _auto_poll['enabled'] = False
        if _auto_poll['timer']:
            _auto_poll['timer'].cancel()

    return jsonify({'auto_poll': _auto_poll['enabled'], 'interval': _auto_poll['interval']})


# ── Downloads ─────────────────────────────────────────────────────────────────
@app.route('/api/download', methods=['POST'])
def api_download():
    data = request.get_json(force=True)
    url  = (data.get('url') or '').strip()
    if not url:
        return jsonify({'error': 'url required'}), 400

    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]

    # Check cache first
    cached = cache_db.get_download(url)
    if cached and cached['status'] == 'done':
        _dl_progress[url_hash] = {'status': 'cached', 'percent': 100,
                                  'filename': cached['filename'], 'cached': True}
        return jsonify({'status': 'cached', 'url_hash': url_hash,
                        'filename': cached['filename'], 'cached': True})

    _dl_progress[url_hash] = {'status': 'starting', 'percent': 0, 'filename': None}

    def do_dl():
        def cb(prog):
            _dl_progress[url_hash] = prog

        result = downloader.download(url, DOWNLOADS_DIR, cb)
        _dl_progress[url_hash] = result
        if result['status'] == 'done':
            cache_db.save_download(url, result['filename'], result.get('size', 0))

    threading.Thread(target=do_dl, daemon=True).start()
    return jsonify({'status': 'started', 'url_hash': url_hash})


@app.route('/api/download/progress/<url_hash>')
def api_dl_progress(url_hash):
    return jsonify(_dl_progress.get(url_hash, {'status': 'unknown'}))


@app.route('/api/downloads')
def api_list_downloads():
    files = []
    for f in sorted(DOWNLOADS_DIR.iterdir(), key=lambda x: -x.stat().st_mtime):
        if f.is_file():
            stat = f.stat()
            files.append({
                'filename':  f.name,
                'size_mb':   round(stat.st_size / (1024 * 1024), 2),
                'size_bytes': stat.st_size,
                'ext':       f.suffix.lower().lstrip('.'),
                'modified':  stat.st_mtime,
            })
    return jsonify({'downloads': files, 'count': len(files)})


@app.route('/api/file/<path:filename>')
def serve_file(filename):
    return send_from_directory(str(DOWNLOADS_DIR), filename, as_attachment=True)


@app.route('/api/file/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    fpath = DOWNLOADS_DIR / filename
    if fpath.exists() and fpath.is_file():
        fpath.unlink()
        return jsonify({'deleted': True})
    return jsonify({'error': 'not found'}), 404


# ── Cache ─────────────────────────────────────────────────────────────────────
@app.route('/api/cache/stats')
def api_cache_stats():
    return jsonify(cache_db.get_stats())


@app.route('/api/cache/clear', methods=['DELETE'])
def api_cache_clear():
    cache_db.clear_all()
    return jsonify({'cleared': True})


# ── Startup ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    cache_db.init()
    print('\nAutoMail Downloader running at http://localhost:5050\n')
    app.run(debug=True, port=5050, threaded=True)
