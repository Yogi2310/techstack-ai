import urllib.request
import re
import json

url = "https://www.youtube.com/channel/UCHicNBr7Ytwd7y2wFUKX_XA"
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

    print(f"Fetched channel page: {len(html)} bytes")
    
    # Extract channel name
    title_match = re.search(r'<title>(.*?)</title>', html)
    if title_match:
        print(f"Title: {title_match.group(1)}")

    # Extract ytInitialData
    data_match = re.search(r'var ytInitialData = ({.*?});</script>', html)
    if data_match:
        data = json.loads(data_match.group(1))
        with open(r"D:\Antigravity\Pro\channel_initial_data.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Extracted ytInitialData successfully!")
    else:
        print("ytInitialData not found, looking for alternative patterns...")
        m2 = re.search(r'window\["ytInitialData"\] = ({.*?});', html)
        if m2:
            data = json.loads(m2.group(1))
            with open(r"D:\Antigravity\Pro\channel_initial_data.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print("Extracted via window[ytInitialData]!")

except Exception as e:
    print(f"Error fetching channel page: {e}")
