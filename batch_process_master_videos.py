"""
Batch Master Video Production Engine
Converts all downloaded viral Roblox videos into branded TaleBlox Master Shorts with:
1. 3D Corner Watermark
2. 3.5s Cinema Outro Card
3. Audio Normalization & Concat
4. Saves to D:\Antigravity\Pro\Riyo_3D_Roblox_Series\master_videos\SHORT_{N}_...
"""
import os
import sys
import json
import re
import subprocess

SRC_DIR = r"D:\Antigravity\Pro\zaylento_trending_collection"
MASTER_DIR = r"D:\Antigravity\Pro\Riyo_3D_Roblox_Series\master_videos"
WATERMARK = r"D:\Antigravity\Pro\riyo_3d_corner_watermark.png"
OUTRO = r"D:\Antigravity\Pro\outro_clip.mp4"

os.makedirs(MASTER_DIR, exist_ok=True)

with open(os.path.join(SRC_DIR, "full_catalog.json"), "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Exclude already mastered videos:
# Rank 1: tJ6CIk70WAg (SHORT_11)
# Rank 19: h9j9mwFqLj8 (SHORT_10)
EXCLUDE_IDS = {"tJ6CIk70WAg", "h9j9mwFqLj8"}

to_process = [v for v in catalog if v["id"] not in EXCLUDE_IDS]

def clean_title(title):
    clean = re.sub(r'In This Town,\s*', '', title, flags=re.IGNORECASE)
    clean = re.sub(r'In This World,\s*', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'[^\w\s-]', '', clean).strip()
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean[:40]

print(f"=== BATCH PROCESSING {len(to_process)} MASTER VIDEOS (SHORT_12 to SHORT_{11 + len(to_process)}) ===")

processed_records = []

for i, item in enumerate(to_process, start=12):
    short_num = i
    vid_id = item["id"]
    raw_title = item["title"]
    views = item["views"]
    
    slug = clean_title(raw_title)
    out_filename = f"SHORT_{short_num}_{slug}.mp4"
    out_path = os.path.join(MASTER_DIR, out_filename)
    
    # Locate source video
    src_file = None
    for fname in os.listdir(SRC_DIR):
        if fname.endswith(".mp4") and (item["file"] == fname or vid_id in fname or f"{item['rank']:02d}_" in fname):
            full_src = os.path.join(SRC_DIR, fname)
            if os.path.getsize(full_src) > 1000000:
                src_file = full_src
                break
                
    if not src_file:
        print(f"\n[!] Source file not found for Short #{short_num}: {raw_title} (ID: {vid_id})")
        continue

    item_record = {
        "short_number": short_num,
        "title": raw_title,
        "views": views,
        "out_file": out_filename,
        "out_path": out_path
    }

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000000:
        sz_mb = round(os.path.getsize(out_path) / (1024*1024), 2)
        print(f"[Short #{short_num:02d}] [EXISTS] {out_filename} ({sz_mb} MB)")
        processed_records.append(item_record)
        continue

    print(f"\n[Short #{short_num:02d}] Processing: {raw_title} ({views})")
    print(f"            Source: {os.path.basename(src_file)} ({round(os.path.getsize(src_file)/(1024*1024), 1)} MB)")
    print(f"            Target: {out_filename}")

    # Standardize to 720x1280 30fps for ultra-fast render & universal playback
    cmd = [
        "ffmpeg", "-y",
        "-i", src_file,
        "-i", WATERMARK,
        "-i", OUTRO,
        "-filter_complex",
        "[0:v]scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[main_v]; "
        "[1:v]scale=180:-1[wm]; "
        "[main_v][wm]overlay=28:36[branded_v]; "
        "[2:v]scale=720:1280,setsar=1,fps=30[outro_v]; "
        "[0:a]aformat=sample_rates=44100:channel_layouts=stereo[a0]; "
        "[2:a]aformat=sample_rates=44100:channel_layouts=stereo[a1]; "
        "[branded_v][a0][outro_v][a1]concat=n=2:v=1:a=1[outv][outa]",
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000000:
        sz_mb = round(os.path.getsize(out_path) / (1024*1024), 2)
        print(f"            [SUCCESS] Created {out_filename} ({sz_mb} MB)!")
        processed_records.append(item_record)
    else:
        print(f"            [!] FFmpeg Error: {res.stderr[-300:] if res.stderr else 'Unknown'}")

print("\n" + "="*50)
print(f"BATCH COMPLETE! {len(processed_records)} master videos ready in {MASTER_DIR}")
print("="*50)
