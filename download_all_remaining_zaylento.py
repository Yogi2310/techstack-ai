"""
Download ALL Remaining Zaylento Shorts (Completing Full Library of 35 Videos)
"""
import os
import sys
import json
import subprocess
import re

OUT_DIR = r"D:\Antigravity\Pro\zaylento_trending_collection"
os.makedirs(OUT_DIR, exist_ok=True)

# Full raw dump from YouTube
RAW_VIDEOS = [
    ("tJ6CIk70WAg", "In This Town, The Rich Live Above the Clouds (Part 1)", 1500000),
    ("TfzSeQdWIBw", "In This Town, Touching the Ground Costs $10", 958000),
    ("CgkUnE5f9B8", "In This Town, You Get Paid for Being Unlucky", 772000),
    ("WOXPexksjzY", "In This Town, the Monster Can Only Move in the Dark (Part 2)", 696000),
    ("8oheA3mvcjM", "In This Town, One Cereal Box Contains a Golden Ticket", 581000),
    ("z1fAAK69HYY", "In This Town, You Get Paid for Being Embarrassed", 548000),
    ("HWUR6ofTgVg", "In This Town, Nobody Is Allowed to Look at the Moon", 504000),
    ("q12InRw4yPE", "In This Town, Poor People Become Invisible", 463000),
    ("qI68Uy_ZpEY", "In This Town, Everyone Must Choose Between Two Pills (Part 1)", 463000),
    ("PxbSw432cUc", "In This Town, We Can Never Stop Moving", 427000),
    ("LiXydhGRzeI", "In This Town, the Ice Cream Truck Only Comes at Midnight", 386000),
    ("iQqzkk6Ntjw", "In This Town, Everyone Lives Inside the Backrooms", 375000),
    ("iy0QCjpP43Q", "In This Town, One Person Gets Hunted for 10 Days", 351000),
    ("lPZLVGPjTjE", "In This Town, Everyone Has a Bunker Except Me (Part 1)", 254000),
    ("CX1ZZEL4InY", "In This Town, Everyone Has a Mammoth Except Me", 248000),
    ("EFJSaxS2Dxg", "In This Town, Everyone's Goal Is to Steal Land", 235000),
    ("V7D63U_P4z0", "In This Town, the Monster Can Only Move in the Dark (Part 1)", 143000),
    ("ZDKtfjE8EeE", "In This Town, Everyone Must Choose Between Two Pills (Part 2)", 115000),
    ("h9j9mwFqLj8", "In This Town, Everyone Is a Ninja Except Me", 91000),
    ("UST7V2d3gtw", "In This World, Everyone Lives on a Train That Never Stops", 88000),
    ("FY1HVKVJ2Ro", "In This Town, You Wake Up in a Different Era Every Day", 55000),
    ("j3JwqsQs5Y8", "In This World, Something Different Rains Every Day (Part 1)", 51000),
    ("2bEm0CrU9iE", "In This Town, Everyone Sleepwalks at Night Except Me", 49000),
    ("rI6_aCyq7WU", "In This Town, You Can Enter Any Book", 49000),
    ("lfKVkXmY7WI", "In This Town, the Floor Turns Into Lava Every Hour", 47000),
    ("OPDWiG0ByDw", "In This Town, If You Lie, You Turn Into Stone", 45000),
    ("CobwGntx_n0", "In This Town, The Rich Live Above the Clouds (Part 2)", 42000),
    ("mpilfnbMJ9g", "In This Town, Everyone Has a Bunker Except Me (Part 2)", 41000),
    ("gXOgDlJOIhw", "In This Town, Every Living Thing Is the Opposite Size", 38000),
    ("2OLQrTPmMhc", "In This Town, We All Live Inside a TV", 36000),
    ("pwD72S7n5p0", "In This Town, Nobody Is Locked In Except Me", 33000),
    ("6xdNuIcV-E4", "In This Town, Everyone Is Watching These In This Town Videos", 31000),
    ("KF2x66Jkw-Y", "In This World, Something Different Rains Every Day (Part 2)", 28000),
    ("prK4MCunvXM", "In This Town, Everyone Believes in Christmas Except Me", 22000),
    ("JdkX4FtdGx0", "In This Town, We Live on a Giant Capybara", 4500)
]

def sanitize_filename(title):
    clean = re.sub(r'[^\w\s-]', '', title).strip()
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean[:45]

catalog = []

for idx, (vid_id, title, views) in enumerate(RAW_VIDEOS, start=1):
    safe_name = f"{idx:02d}_{sanitize_filename(title)}.mp4"
    dest = os.path.join(OUT_DIR, safe_name)
    yt_url = f"https://www.youtube.com/shorts/{vid_id}"

    # Check if already downloaded under old or new name
    found = False
    for existing in os.listdir(OUT_DIR):
        if existing.endswith(".mp4") and (vid_id in existing or safe_name in existing or f"{idx:02d}_" in existing):
            full_path = os.path.join(OUT_DIR, existing)
            if os.path.getsize(full_path) > 1000000:
                dest = full_path
                found = True
                break

    item = {
        "rank": idx,
        "id": vid_id,
        "title": title,
        "views": f"{views:,} Views",
        "views_raw": views,
        "file": os.path.basename(dest)
    }

    if found and os.path.exists(dest) and os.path.getsize(dest) > 1000000:
        sz_mb = round(os.path.getsize(dest) / (1024*1024), 2)
        print(f"[{idx}/35] [EXISTS] {title} ({sz_mb} MB)")
        item["size_mb"] = sz_mb
        catalog.append(item)
        continue

    print(f"\n[{idx}/35] Downloading: {title} ({views:,} views)...")
    cmd = [
        "yt-dlp",
        "--no-update",
        "--merge-output-format", "mp4",
        "-o", dest,
        yt_url
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000000:
        sz_mb = round(os.path.getsize(dest) / (1024*1024), 2)
        print(f"       [SUCCESS] Downloaded! Size: {sz_mb} MB")
        item["size_mb"] = sz_mb
        catalog.append(item)
    else:
        print(f"       [!] Warning: {res.stderr[:160]}")

catalog_path = os.path.join(OUT_DIR, "full_catalog.json")
with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print(f"\nALL 35 VIDEOS PROCESSED! Catalog saved to {catalog_path}")
