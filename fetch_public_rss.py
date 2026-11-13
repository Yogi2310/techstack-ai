import urllib.request
import xml.etree.ElementTree as ET
import json
import re

channel_id = "UCHicNBr7Ytwd7y2wFUKX_XA"
rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

req = urllib.request.Request(
    rss_url,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)

try:
    with urllib.request.urlopen(req) as resp:
        xml_data = resp.read()

    root = ET.fromstring(xml_data)
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'yt': 'http://www.youtube.com/xml/schemas/2015',
        'media': 'http://search.yahoo.com/mrss/'
    }

    ch_title = root.find('atom:title', ns).text
    print(f"Channel Title: {ch_title}")

    videos = []
    for entry in root.findall('atom:entry', ns):
        vid_id = entry.find('yt:videoId', ns).text
        title = entry.find('atom:title', ns).text
        published = entry.find('atom:published', ns).text
        media_group = entry.find('media:group', ns)
        desc = media_group.find('media:description', ns).text if media_group is not None else ""
        community = media_group.find('media:community', ns) if media_group is not None else None
        views = 0
        if community is not None:
            stats = community.find('media:statistics', ns)
            if stats is not None:
                views = stats.attrib.get('views', 0)

        videos.append({
            'videoId': vid_id,
            'title': title,
            'published': published,
            'views': views,
            'description': desc
        })

    print(f"Found {len(videos)} videos in public feed:")
    for v in videos:
        print(f"- [{v['views']} views] {v['title']} (https://youtu.be/{v['videoId']})")

    with open(r"D:\Antigravity\Pro\public_channel_videos.json", 'w', encoding='utf-8') as f:
        json.dump({'title': ch_title, 'videos': videos}, f, indent=2)

except Exception as e:
    print(f"Error fetching RSS: {e}")
