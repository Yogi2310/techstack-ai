import json

with open(r"D:\Antigravity\Pro\channel_initial_data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract header
header = data.get('header', {}).get('c4TabbedHeaderRenderer', {}) or data.get('header', {}).get('pageHeaderRenderer', {})
metadata = data.get('metadata', {}).get('channelMetadataRenderer', {})

print("=== CHANNEL SUMMARY ===")
print("Title:", metadata.get('title'))
print("Description:", metadata.get('description'))
print("Vanity URL:", metadata.get('vanityChannelUrl'))
print("External ID:", metadata.get('externalId'))

# Extract tabs
tabs = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
print(f"Tabs count: {len(tabs)}")

videos = []

def extract_videos_from_renderer(r):
    items = []
    # search recursively or check contents
    return items

# Search all videoRenderer / gridVideoRenderer in the data
def find_all_keys(obj, key):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                results.append(v)
            elif isinstance(v, (dict, list)):
                results.extend(find_all_keys(v, key))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(find_all_keys(item, key))
    return results

video_renderers = find_all_keys(data, 'videoRenderer') + find_all_keys(data, 'gridVideoRenderer') + find_all_keys(data, 'reelItemRenderer')

print(f"Total video renderers found on channel home: {len(video_renderers)}")

for vr in video_renderers:
    vid_id = vr.get('videoId')
    title = ""
    if 'title' in vr:
        if 'runs' in vr['title']:
            title = "".join(r.get('text', '') for r in vr['title']['runs'])
        elif 'simpleText' in vr['title']:
            title = vr['title']['simpleText']
    
    views = ""
    if 'viewCountText' in vr:
        if 'simpleText' in vr['viewCountText']:
            views = vr['viewCountText']['simpleText']
        elif 'runs' in vr['viewCountText']:
            views = "".join(r.get('text', '') for r in vr['viewCountText']['runs'])

    time_text = ""
    if 'publishedTimeText' in vr:
        if 'simpleText' in vr['publishedTimeText']:
            time_text = vr['publishedTimeText']['simpleText']
        elif 'runs' in vr['publishedTimeText']:
            time_text = "".join(r.get('text', '') for r in vr['publishedTimeText']['runs'])

    length_text = ""
    if 'thumbnailOverlays' in vr:
        for overlay in vr['thumbnailOverlays']:
            time_status = overlay.get('thumbnailOverlayTimeStatusRenderer', {})
            if 'text' in time_status:
                length_text = time_status['text'].get('simpleText', '')

    videos.append({
        'id': vid_id,
        'title': title,
        'views': views,
        'published': time_text,
        'length': length_text
    })

for i, v in enumerate(videos):
    print(f"{i+1}. [{v.get('length')}] {v.get('title')} ({v.get('views')}, {v.get('published')}) - https://youtu.be/{v.get('id')}")

with open(r"D:\Antigravity\Pro\parsed_channel_audit.json", 'w', encoding='utf-8') as f:
    json.dump({
        'metadata': metadata,
        'videos': videos
    }, f, indent=2)
