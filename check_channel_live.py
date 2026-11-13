import urllib.request, json, re, sys

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
url = 'https://www.youtube.com/@TechStacAI/shorts'
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')
        
    m = re.search(r'var ytInitialData = ({.*?});</script>', html)
    if m:
        data = json.loads(m.group(1))
        tabs = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
        for tab in tabs:
            tab_ren = tab.get('tabRenderer', {})
            content = tab_ren.get('content', {})
            if 'richGridRenderer' in content:
                contents = content['richGridRenderer'].get('contents', [])
                print(f"Total Public Shorts: {len(contents)}")
                for it in contents:
                    vm = it.get('richItemRenderer', {}).get('content', {}).get('shortsLockupViewModel', {})
                    if vm:
                        print(f"• {vm.get('accessibilityText')}")
except Exception as e:
    print('Error:', e)
