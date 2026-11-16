import urllib.request
import re
import os

headers = {
    'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

download_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.instagram.com/',
    'Accept': '*/*',
    'Accept-Encoding': 'identity',
    'Sec-Fetch-Dest': 'video',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site'
}

reels_to_fetch = [
    ("DfnxzmToEdg", "reel_videogame_level1.mp4"),
    ("Dfrix2Mts68", "reel_ages_backwards.mp4")
]

out_dir = r"D:/Antigravity/Pro/instagram_downloads"
os.makedirs(out_dir, exist_ok=True)

for code, fname in reels_to_fetch:
    url = f"https://www.instagram.com/reel/{code}/"
    dest_path = os.path.join(out_dir, fname)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000000:
        print(f"[+] Already downloaded: {dest_path}")
        continue

    print(f"\n[*] Fetching metadata for {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        v_escaped = re.findall(r'(https:\\/\\/[^"\'<>\s]+\.mp4[^"\'<>\s]*)', html)
        print(f"    Found {len(v_escaped)} raw mp4 matches for {code}")
        
        saved = False
        for i, raw in enumerate(v_escaped):
            clean = raw.replace('\\u0026', '&').replace('\\/', '/')
            try:
                vid_req = urllib.request.Request(clean, headers=download_headers)
                with urllib.request.urlopen(vid_req, timeout=25) as vid_resp:
                    if vid_resp.status == 200:
                        with open(dest_path, 'wb') as f:
                            while True:
                                chunk = vid_resp.read(65536)
                                if not chunk:
                                    break
                                f.write(chunk)
                        print(f"[SUCCESS] Downloaded {fname} ({os.path.getsize(dest_path)} bytes)")
                        saved = True
                        break
            except Exception as e:
                pass
        if not saved:
            print(f"[!] Could not download video for {code}")
    except Exception as e:
        print(f"[!] Error for {code}: {e}")
