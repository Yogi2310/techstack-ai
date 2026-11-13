import urllib.request, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for vid in ['a84L5be82i4', 'YwWiQQ5U0s0', '2DbPvihr8Sc']:
    url = f'https://www.youtube.com/watch?v=vid'
    url = f'https://www.youtube.com/watch?v={vid}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            title_match = re.search(r'<title>(.*?)</title>', html)
            view_match = re.search(r'"viewCount":"(\d+)"', html)
            unlisted_match = re.search(r'"isUnlisted":(true|false)', html)
            private_match = re.search(r'"isPrivate":(true|false)', html)
            
            title = title_match.group(1) if title_match else 'Unknown'
            views = view_match.group(1) if view_match else 'Unknown'
            unlisted = unlisted_match.group(1) if unlisted_match else 'false'
            private = private_match.group(1) if private_match else 'false'
            
            print(f"[{vid}] Title: {title} | Views: {views} | Unlisted: {unlisted} | Private: {private}")
    except Exception as e:
        print(f"[{vid}] Error: {e}")
