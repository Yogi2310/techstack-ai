import urllib.request
import re
import json

url = 'https://www.instagram.com/reel/Dfrkkpag-Ta/'
user_agents = [
    'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
    'Twitterbot/1.0',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

for ua in user_agents:
    print(f"--- Testing UA: {ua[:30]} ---")
    headers = {
        'User-Agent': ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"Status: {resp.status}, Length: {len(html)}")
            
            # Look for og: tags
            og_matches = re.findall(r'<meta[^>]+(?:property|name)=["\'](og:[^"\']+)["\'][^>]+content=["\']([^"\']*)["\']', html)
            if not og_matches:
                og_matches = re.findall(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:property|name)=["\'](og:[^"\']+)["\']', html)
                og_matches = [(m[1], m[0]) for m in og_matches]
            
            for prop, val in og_matches:
                print(f"  {prop}: {val}")
                
            # Look for video URL
            video_urls = re.findall(r'https://[^"\'<>\s]+\.mp4[^"\'<>\s]*', html)
            if video_urls:
                print(f"  Found {len(video_urls)} MP4 URLs! First: {video_urls[0][:100]}")
                break
            
            # Look for title
            title = re.search(r'<title>(.*?)</title>', html)
            if title:
                print(f"  Title: {title.group(1)}")
    except Exception as e:
        print(f"  Error: {e}")
