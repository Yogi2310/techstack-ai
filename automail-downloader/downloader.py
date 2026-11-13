"""
Smart file downloader.
- Direct file URLs  → requests (streaming, progress)
- Video URLs        → yt-dlp
- Detects type from Content-Type or URL extension
"""
import os
import re
import hashlib
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote

VIDEO_DOMAINS = [
    'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
    'tiktok.com', 'instagram.com', 'twitter.com', 'x.com',
    'facebook.com', 'rumble.com', 'twitch.tv',
]

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )
}


def is_video_url(url: str) -> bool:
    return any(d in url.lower() for d in VIDEO_DOMAINS)


def _url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:10]


def _safe_name(name: str) -> str:
    name = unquote(name)
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', name)
    return name[:200].strip()


def _filename_from_response(url: str, resp: requests.Response) -> str:
    # 1. Content-Disposition header
    cd = resp.headers.get('Content-Disposition', '')
    m = re.search(r"filename\*?=['\"]?(?:UTF-8'')?([^'\";\r\n]+)", cd, re.IGNORECASE)
    if m:
        return _safe_name(m.group(1).strip())

    # 2. URL path
    path = urlparse(url).path
    name = os.path.basename(path)
    if name and '.' in name:
        return _safe_name(name)

    # 3. Guess extension from Content-Type
    ct = resp.headers.get('Content-Type', '').split(';')[0].strip()
    ext_map = {
        'application/pdf': '.pdf',
        'application/zip': '.zip',
        'application/x-rar-compressed': '.rar',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'image/jpeg': '.jpg', 'image/png': '.png', 'image/gif': '.gif',
        'video/mp4': '.mp4', 'audio/mpeg': '.mp3',
        'text/plain': '.txt', 'text/html': '.html',
    }
    ext = ext_map.get(ct, '')
    return f'download_{_url_hash(url)}{ext}'


def download(url: str, out_dir: Path, progress_cb=None) -> dict:
    """Entry point — routes to video or file downloader."""
    try:
        out_dir = Path(out_dir)
        out_dir.mkdir(exist_ok=True)

        if is_video_url(url):
            return _download_video(url, out_dir, progress_cb)
        else:
            return _download_file(url, out_dir, progress_cb)
    except Exception as e:
        result = {'status': 'error', 'error': str(e), 'percent': 0, 'filename': None}
        if progress_cb:
            progress_cb(result)
        return result


def _download_file(url: str, out_dir: Path, progress_cb=None) -> dict:
    resp = requests.get(url, headers=HEADERS, stream=True, timeout=30, allow_redirects=True)
    resp.raise_for_status()

    filename = _filename_from_response(url, resp)
    out_path = out_dir / filename

    # Avoid collision
    stem, ext = os.path.splitext(filename)
    counter = 1
    while out_path.exists():
        out_path = out_dir / f'{stem}_{counter}{ext}'
        counter += 1

    total = int(resp.headers.get('Content-Length', 0))
    downloaded = 0

    with open(out_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total and progress_cb:
                    pct = round(downloaded / total * 100, 1)
                    progress_cb({'status': 'downloading', 'percent': pct,
                                 'filename': out_path.name, 'downloaded': downloaded, 'total': total})

    size = out_path.stat().st_size
    result = {'status': 'done', 'percent': 100, 'filename': out_path.name, 'size': size}
    if progress_cb:
        progress_cb(result)
    return result


def _download_video(url: str, out_dir: Path, progress_cb=None) -> dict:
    try:
        import yt_dlp
    except ImportError:
        # Fallback to direct download if yt-dlp unavailable
        return _download_file(url, out_dir, progress_cb)

    filename_holder = [None]

    def hook(d):
        if d['status'] == 'downloading':
            raw = d.get('_percent_str', '0%').strip().replace('%', '').replace('\x1b[0;94m', '').replace('\x1b[0m', '')
            try:
                pct = float(raw)
            except ValueError:
                pct = 0
            if progress_cb:
                progress_cb({
                    'status': 'downloading',
                    'percent': pct,
                    'filename': d.get('filename', 'video'),
                    'downloaded': d.get('downloaded_bytes', 0),
                    'total': d.get('total_bytes') or d.get('total_bytes_estimate', 0),
                })
        elif d['status'] == 'finished':
            filename_holder[0] = Path(d.get('filename', '')).name

    opts = {
        'outtmpl':              str(out_dir / '%(title).80s_%(id)s.%(ext)s'),
        'format':               'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]/best',
        'merge_output_format':  'mp4',
        'progress_hooks':       [hook],
        'quiet':                True,
        'no_warnings':          True,
        'nocheckcertificate':   True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)

    filename = filename_holder[0]
    if not filename:
        title   = re.sub(r'[<>:"/\\|?*]', '_', info.get('title', 'video'))[:80]
        vid_id  = info.get('id', _url_hash(url))
        filename = f'{title}_{vid_id}.mp4'

    out_path = out_dir / filename
    size = out_path.stat().st_size if out_path.exists() else 0
    result = {'status': 'done', 'percent': 100, 'filename': filename, 'size': size}
    if progress_cb:
        progress_cb(result)
    return result
