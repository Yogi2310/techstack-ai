import urllib.request
import re
import os

url = 'https://www.instagram.com/reel/Dfo6IC9BXKb/'
headers = {
    'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}
print(f"Fetching metadata for {url}...")
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=12) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

os.makedirs(r"D:\Antigravity\Pro\instagram_downloads", exist_ok=True)
with open(r"D:\Antigravity\Pro\instagram_downloads\page_dfo6ic9.html", "w", encoding="utf-8") as f:
    f.write(html)

v_escaped = re.findall(r'(https:\\/\\/[^"\'<>\s]+\.mp4[^"\'<>\s]*)', html)
print(f"Found {len(v_escaped)} raw mp4 matches:")

download_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.instagram.com/',
    'Accept': '*/*',
    'Accept-Encoding': 'identity',
    'Sec-Fetch-Dest': 'video',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site'
}

dest_file = r"D:\Antigravity\Pro\instagram_downloads\reel_dfo6ic9.mp4"

success = False
for i, raw in enumerate(v_escaped):
    clean = raw.replace('\\u0026', '&').replace('\\/', '/')
    print(f"\n--- Trying URL #{i+1} ---")
    print(clean[:150])
    try:
        vid_req = urllib.request.Request(clean, headers=download_headers)
        with urllib.request.urlopen(vid_req, timeout=20) as resp:
            content_type = resp.headers.get('Content-Type')
            content_length = resp.headers.get('Content-Length')
            print(f"Response status: {resp.status}, Content-Type: {content_type}, Size: {content_length} bytes")
            if resp.status == 200:
                with open(dest_file, 'wb') as f:
                    total = 0
                    while True:
                        chunk = resp.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
                        total += len(chunk)
                print(f"[SUCCESS] Downloaded {total} bytes to {dest_file}")
                success = True
                break
    except Exception as e:
        print(f"Failed URL #{i+1}: {e}")

if not success:
    print("[!] Could not download video from matches.")
