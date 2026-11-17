"""
Batch Downloader for Zaylento's Top 12 Trending Viral Roblox Stories
"""
import os
import sys
import json
import subprocess

OUT_DIR = r"D:\Antigravity\Pro\zaylento_trending_collection"
os.makedirs(OUT_DIR, exist_ok=True)

TRENDING_VIDEOS = [
    {
        "rank": 1,
        "id": "tJ6CIk70WAg",
        "title": "In This Town, The Rich Live Above the Clouds (Part 1)",
        "views": "1.5M Views",
        "filename": "01_Rich_Live_Above_The_Clouds_Part1.mp4"
    },
    {
        "rank": 2,
        "id": "TfzSeQdWIBw",
        "title": "In This Town, Touching the Ground Costs $10",
        "views": "958K Views",
        "filename": "02_Touching_Ground_Costs_10_Dollars.mp4"
    },
    {
        "rank": 3,
        "id": "CgkUnE5f9B8",
        "title": "In This Town, You Get Paid for Being Unlucky",
        "views": "769K Views",
        "filename": "03_Paid_For_Being_Unlucky.mp4"
    },
    {
        "rank": 4,
        "id": "WOXPexksjzY",
        "title": "In This Town, The Monster Can Only Move in the Dark (Part 2)",
        "views": "681K Views",
        "filename": "04_Monster_Only_Moves_In_Dark_Part2.mp4"
    },
    {
        "rank": 5,
        "id": "8oheA3mvcjM",
        "title": "In This Town, One Cereal Box Contains a Golden Ticket",
        "views": "581K Views",
        "filename": "05_Cereal_Golden_Ticket.mp4"
    },
    {
        "rank": 6,
        "id": "z1fAAK69HYY",
        "title": "In This Town, You Get Paid for Being Embarrassed",
        "views": "548K Views",
        "filename": "06_Paid_For_Being_Embarrassed.mp4"
    },
    {
        "rank": 7,
        "id": "HWUR6ofTgVg",
        "title": "In This Town, Nobody Is Allowed to Look at the Moon",
        "views": "504K Views",
        "filename": "07_Never_Look_At_The_Moon.mp4"
    },
    {
        "rank": 8,
        "id": "q12InRw4yPE",
        "title": "In This Town, Poor People Become Invisible",
        "views": "462K Views",
        "filename": "08_Poor_People_Become_Invisible.mp4"
    },
    {
        "rank": 9,
        "id": "qI68Uy_ZpEY",
        "title": "In This Town, Everyone Must Choose Between Two Pills (Part 1)",
        "views": "461K Views",
        "filename": "09_Choose_Between_Two_Pills_Part1.mp4"
    },
    {
        "rank": 10,
        "id": "iQqzkk6Ntjw",
        "title": "In This Town, Everyone Lives Inside the Backrooms",
        "views": "375K Views",
        "filename": "10_Everyone_Lives_In_Backrooms.mp4"
    },
    {
        "rank": 11,
        "id": "LiXydhGRzeI",
        "title": "In This Town, The Ice Cream Truck Only Comes at Midnight",
        "views": "373K Views",
        "filename": "11_Midnight_Ice_Cream_Truck.mp4"
    },
    {
        "rank": 12,
        "id": "iy0QCjpP43Q",
        "title": "In This Town, One Person Gets Hunted for 10 Days",
        "views": "351K Views",
        "filename": "12_Hunted_For_10_Days.mp4"
    }
]

print(f"=== DOWNLOADING {len(TRENDING_VIDEOS)} TOP TRENDING ZAYLENTO VIDEOS ===")

downloaded_list = []

for idx, item in enumerate(TRENDING_VIDEOS, start=1):
    vid_id = item["id"]
    dest = os.path.join(OUT_DIR, item["filename"])
    yt_url = f"https://www.youtube.com/shorts/{vid_id}"
    
    # Check if mp4 or webm exists
    dest_webm = dest + ".webm"
    if os.path.exists(dest_webm) and not os.path.exists(dest):
        subprocess.run(["ffmpeg", "-y", "-i", dest_webm, "-c", "copy", dest], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(dest_webm):
            try:
                os.remove(dest_webm)
            except:
                pass

    if os.path.exists(dest) and os.path.getsize(dest) > 1000000:
        sz_mb = round(os.path.getsize(dest) / (1024*1024), 2)
        print(f"[{idx}/{len(TRENDING_VIDEOS)}] [EXISTS] {item['title']} ({sz_mb} MB)")
        item["file_path"] = dest
        item["file_size_mb"] = sz_mb
        downloaded_list.append(item)
        continue

    print(f"\n[{idx}/{len(TRENDING_VIDEOS)}] Downloading: {item['title']} ({item['views']})")
    
    cmd = [
        "yt-dlp",
        "--merge-output-format", "mp4",
        "-o", dest,
        yt_url
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000000:
        sz_mb = round(os.path.getsize(dest) / (1024*1024), 2)
        print(f"       [SUCCESS] Downloaded! Size: {sz_mb} MB")
        item["file_path"] = dest
        item["file_size_mb"] = sz_mb
        downloaded_list.append(item)
    else:
        print(f"       [!] Warning: {res.stderr[:160]}")

catalog_path = os.path.join(OUT_DIR, "catalog.json")
with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(downloaded_list, f, indent=2)

print("\n" + "="*50)
print(f"COMPLETE! {len(downloaded_list)}/{len(TRENDING_VIDEOS)} videos saved to {OUT_DIR}")
print("="*50)
