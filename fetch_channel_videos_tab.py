import urllib.request
import re
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://www.youtube.com/@TechStacAI"

for tab in ["videos", "shorts"]:
    url = f"{base_url}/{tab}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')

        m = re.search(r'var ytInitialData = ({.*?});</script>', html)
        if m:
            data = json.loads(m.group(1))
            with open(rf"D:\Antigravity\Pro\channel_{tab}_data.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"SUCCESS: Saved {tab} tab data ({len(html)} bytes)")
        else:
            print(f"FAILED: No ytInitialData in {tab}")
    except Exception as e:
        print(f"Error fetching {tab}: {e}")
