import json, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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

def extract_video_info(vr):
    vid_id = vr.get('videoId')
    title = ""
    if 'title' in vr:
        if isinstance(vr['title'], dict):
            if 'runs' in vr['title']:
                title = "".join(r.get('text', '') for r in vr['title']['runs'])
            elif 'simpleText' in vr['title']:
                title = vr['title']['simpleText']
        elif isinstance(vr['title'], str):
            title = vr['title']

    views = ""
    if 'viewCountText' in vr:
        vct = vr['viewCountText']
        if isinstance(vct, dict):
            if 'simpleText' in vct:
                views = vct['simpleText']
            elif 'runs' in vct:
                views = "".join(r.get('text', '') for r in vct['runs'])
        elif isinstance(vct, str):
            views = vct

    published = ""
    if 'publishedTimeText' in vr:
        ptt = vr['publishedTimeText']
        if isinstance(ptt, dict):
            if 'simpleText' in ptt:
                published = ptt['simpleText']
            elif 'runs' in ptt:
                published = "".join(r.get('text', '') for r in ptt['runs'])

    length = ""
    if 'thumbnailOverlays' in vr:
        for overlay in vr['thumbnailOverlays']:
            time_status = overlay.get('thumbnailOverlayTimeStatusRenderer', {})
            if 'text' in time_status:
                length = time_status['text'].get('simpleText', '')

    return {
        'id': vid_id,
        'title': title,
        'views': views,
        'published': published,
        'length': length
    }

print("=== LONG-FORM VIDEOS ===")
try:
    with open(r"D:\Antigravity\Pro\channel_videos_data.json", 'r', encoding='utf-8') as f:
        v_data = json.load(f)
    v_renderers = find_all_keys(v_data, 'videoRenderer') + find_all_keys(v_data, 'gridVideoRenderer')
    print(f"Found {len(v_renderers)} long-form video entries:")
    seen = set()
    for vr in v_renderers:
        info = extract_video_info(vr)
        if info['id'] and info['id'] not in seen:
            seen.add(info['id'])
            print(f"- [{info['length'] or 'Video'}] {info['title']} | {info['views']} | {info['published']} | https://youtu.be/{info['id']}")
except Exception as e:
    print(f"Error parsing videos: {e}")

print("\n=== SHORTS ===")
try:
    with open(r"D:\Antigravity\Pro\channel_shorts_data.json", 'r', encoding='utf-8') as f:
        s_data = json.load(f)
    s_renderers = find_all_keys(s_data, 'reelItemRenderer') + find_all_keys(s_data, 'shortsLockupViewModel')
    print(f"Found {len(s_renderers)} shorts entries:")
    seen_s = set()
    for sr in s_renderers:
        s_id = sr.get('videoId')
        # Check shortsLockupViewModel structure
        if not s_id and 'entityId' in sr:
            s_id = sr['entityId'].replace('shorts-shelf-item-', '')
        
        headline = ""
        if 'headline' in sr:
            headline = sr['headline'].get('simpleText', '')
        elif 'overlayMetadata' in sr:
            headline = sr.get('overlayMetadata', {}).get('primaryText', {}).get('content', '')

        view_count = ""
        if 'viewCountText' in sr:
            view_count = sr['viewCountText'].get('simpleText', '')
        elif 'overlayMetadata' in sr:
            view_count = sr.get('overlayMetadata', {}).get('secondaryText', {}).get('content', '')

        if s_id and s_id not in seen_s:
            seen_s.add(s_id)
            print(f"- [Short] {headline} | {view_count} | https://www.youtube.com/shorts/{s_id}")
except Exception as e:
    print(f"Error parsing shorts: {e}")
