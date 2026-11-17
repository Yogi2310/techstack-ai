"""
Sync Master Theater with All Available Master Videos
Automatically updates watch_all_videos.html with every SHORT_*.mp4 in master_videos/
"""
import os
import sys
import re
import json

SERIES_DIR = r"D:\Antigravity\Pro\Riyo_3D_Roblox_Series"
MASTER_DIR = os.path.join(SERIES_DIR, "master_videos")
THEATER_FILE = os.path.join(SERIES_DIR, "interactive_players", "watch_all_videos.html")

# Base metadata for core episodes
BASE_VIDEOS = {
    1: {
        "tag": "VIRAL BREAKOUT (PART 1)",
        "title": "In This Town, You Throw Food To Get Pets... 😱",
        "desc": "Eli trains to throw the legendary Golden Cheese over the mountains. A giant pure-gold dragon bows before him, making him the richest kid in town. But that night, skyscraper-sized food crashes into the town square...",
        "statusText": "🟢 LIVE ON YOUTUBE (20,880+ VIEWS)",
        "statusClass": "status-live",
        "ytId": "23UgMKnyiWw",
        "views": "20.8K Views",
        "retention": "87.6% Retention"
    },
    2: {
        "tag": "VIRAL SPECIAL FEATURE",
        "title": "The Ocean Disappeared For 24 Hours... 🌊😱",
        "desc": "A mysterious siren sounds and the entire ocean vanishes, exposing sunken galleons, bioluminescent trenches, and deep-sea creatures. Eli ventures into the abyss with Kevin, but the tidal timer is ticking down...",
        "statusText": "🟢 LIVE ON YOUTUBE (1,620+ VIEWS)",
        "statusClass": "status-live",
        "ytId": "8uqNHiG5wzo",
        "views": "1.6K Views",
        "retention": "70.1% Retention"
    },
    3: {
        "tag": "OFFICIAL PART 2",
        "title": "The Giant Carrot Woke Up The Titan... 😱🥕 (PART 2)",
        "desc": "Direct continuation of Part 1! A skyscraper-sized carrot crashes into the village, followed by colossal footsteps. Eli and Kevin confront the awakening Colossus as the town prepares for war.",
        "statusText": "🟢 LIVE ON YOUTUBE",
        "statusClass": "status-live",
        "ytId": "qlE3DMDswn8",
        "views": "Premiered Mon Nov 16",
        "retention": "High Watch Time"
    },
    4: {
        "tag": "STANDALONE VIRAL HIT",
        "title": "In My Town, Everything Works Like A Video Game 🎮",
        "desc": "Everyone has a floating health bar, a level, and an inventory. Eli is stuck at Level 1 while toddlers are Level 50. But when he glitches behind the map into the Town Settings room, he finds the developer console!",
        "statusText": "🟢 LIVE ON YOUTUBE (7:30 PM DROP)",
        "statusClass": "status-live",
        "ytId": "j0fBOXT8yjE",
        "views": "Published Tonight",
        "retention": "Optimized Hook"
    },
    5: {
        "tag": "SCHEDULED PREMIERE",
        "title": "In This Town, Everyone Ages Backwards 👶👴",
        "desc": "You are born 80 years old with a grey beard and get one year younger every birthday. Toddlers wear briefcases to work while grandpas play in ball pits. But tomorrow, Eli's grandpa turns zero... so Eli hides under the crib to see the secret truth!",
        "statusText": "⏰ SCHEDULED: TUE NOV 17 @ 8:30 AM IST",
        "statusClass": "status-sched",
        "ytId": "04nx3n98XiI",
        "views": "Premiere Tomorrow",
        "retention": "Full Retention Script"
    },
    6: {
        "tag": "🔥 NEW PRODUCTION (ELI & KEVIN PART 3)",
        "title": "I Threw The Forbidden Black Onion At The Colossus... 🧅😱",
        "desc": "PART 3 DIRECT CONTINUATION! The mountain giants throw skyscraper-sized carrots at the town. Eli breaks into the cryogenic vault, steals the pulsing Black Onion, and hurls it from the water tower. The colossal Titan gets tamed like a puppy... but its collar reveals the secret of SECTOR 9!",
        "statusText": "✨ NEW MASTER VIDEO (READY TO PUBLISH)",
        "statusClass": "status-special",
        "ytId": "",
        "views": "Fresh 3D Master",
        "retention": "High-Octane Pacing"
    },
    7: {
        "tag": "🤖 100% AUTONOMOUS 3D ANIMATION",
        "title": "Eli Throws The Golden Cheese (Full-Motion 3D Roblox Animation) 🧀✨",
        "desc": "BUILT 100% BY OUR 3D ENGINE! Eli physically runs through the Roblox town with Kevin the frog, plants his feet at the cliff edge, winds up, and throws the glowing Golden Cheese. Watch the cheese soar through the clouds and awaken the giant Golden Dragon bowing with 200 exploding gold coins!",
        "statusText": "🌟 FULL-MOTION 3D (RENDERED ON YOUR PC)",
        "statusClass": "status-live",
        "ytId": "",
        "views": "100% Autonomous",
        "retention": "60 FPS 3D Motion"
    },
    8: {
        "tag": "🧅 100% AUTONOMOUS 3D ANIMATION (PART 3)",
        "title": "The Forbidden Black Onion (Full-Motion 3D Roblox Animation) 🧅⚡",
        "desc": "DIRECT SEQUEL TO GOLDEN CHEESE! Giants throw giant food back at the town. Eli runs past a skyscraper carrot while Grandma bench-presses a tank. He breaks into the cryogenic vault, steals the pulsing Black Onion, leaps off the water tower, and tames the Colossus like an obedient puppy with blue eyes!",
        "statusText": "🌟 FULL-MOTION 3D ACTION (RENDERED ON PC)",
        "statusClass": "status-special",
        "ytId": "",
        "views": "100% Autonomous",
        "retention": "High Pacing"
    },
    9: {
        "tag": "📏 100% AUTONOMOUS 3D SIZE COMPARISON",
        "title": "Roblox Character to Cosmic Titan Size Scale Comparison 📏💥",
        "desc": "AUTONOMOUS 3D RUNWAY SCALE COMPARISON! High-energy viral scale video comparing Roblox sizes: Noob (1.7m), Golden Bacon Boy (2.4m), Giant Carrot (15m), Mega Frost Golem (45m), Colossal Titan (180m), up to the Cosmic Void Entity (1,000m)!",
        "statusText": "🌟 FULL-MOTION 3D SCALE (RENDERED ON PC)",
        "statusClass": "status-live",
        "ytId": "",
        "views": "100% Autonomous",
        "retention": "Extreme Retention Format"
    },
    10: {
        "tag": "🥷 3D ROBLOX VIRAL MASTER (ZAYLENTO STYLE)",
        "title": "Everyone Is A Ninja Except Me 🥷⛩️ (Roblox 3D Story)",
        "desc": "THE VIRAL 3D NINJA MASTERPIECE! In my village, everyone is born with god-tier ninja abilities—jumping over pagodas, summoning shadow clones, and slicing boulders. But I was born with ZERO ninja skills! Or so everyone thought... until the Forbidden Shrine opened its ancient seal!",
        "statusText": "✨ NEW 3D MASTERPIECE (READY TO PUBLISH)",
        "statusClass": "status-special",
        "ytId": "",
        "views": "Viral Potential",
        "retention": "Extreme Retention Hook"
    },
    11: {
        "tag": "👑 #1 VIRAL HIT (1.5M VIEWS)",
        "title": "The Rich Live Above The Clouds ☁️🏙️ (Part 1)",
        "desc": "THE #1 VIRAL HIT WITH 1.5 MILLION VIEWS! In this town, the ultimate class divide exists: the billionaire elite live in sky-cities above the clouds with clean air and endless robux, while everyone on the ground breathes toxic smog. But when one kid builds a homemade glider and scales the Megastructure elevator shaft, he discovers the dark secret powering the sky cities!",
        "statusText": "🟢 LIVE ON YOUTUBE (JUST PUBLISHED)",
        "statusClass": "status-live",
        "ytId": "oxX9R_XLZd4",
        "views": "1.5M Viral Hit",
        "retention": "Extreme Retention Hook"
    }
}

# Scan master_videos directory
all_files = os.listdir(MASTER_DIR)
short_files = {}

for f in all_files:
    m = re.match(r'^SHORT_(\d+)_(.+)\.mp4$', f, re.IGNORECASE)
    if m:
        num = int(m.group(1))
        # Ensure file has non-zero size
        fp = os.path.join(MASTER_DIR, f)
        if os.path.getsize(fp) > 500000:
            short_files[num] = f

sorted_nums = sorted(short_files.keys())
print(f"[*] Found {len(sorted_nums)} valid master videos in {MASTER_DIR} (Short #{min(sorted_nums)} to #{max(sorted_nums)})")

video_entries = []

for num in sorted_nums:
    filename = short_files[num]
    fp = os.path.join(MASTER_DIR, filename)
    sz_mb = round(os.path.getsize(fp) / (1024*1024), 1)

    if num in BASE_VIDEOS:
        base = BASE_VIDEOS[num]
        entry = {
            "id": f"short{num}",
            "number": f"Short #{num}",
            "tag": base["tag"],
            "title": base["title"],
            "desc": base["desc"],
            "src": f"../master_videos/{filename}",
            "statusText": base["statusText"],
            "statusClass": base["statusClass"],
            "duration": f"Master • {sz_mb} MB",
            "ytId": base["ytId"],
            "views": base["views"],
            "retention": base["retention"]
        }
    else:
        # Generate clean title from filename
        raw_slug = filename.replace(f"SHORT_{num}_", "").replace(".mp4", "")
        pretty_title = raw_slug.replace("_", " ").title()
        entry = {
            "id": f"short{num}",
            "number": f"Short #{num}",
            "tag": f"🔥 MASTER EPISODE #{num}",
            "title": f"In This Town, {pretty_title} 😱🎬",
            "desc": f"MASTERPIECE EPISODE #{num}! Remastered in full vertical format with TaleBlox 3D corner watermark and animated cinema outro card. Complete story with full high-retention audio and sound effects.",
            "src": f"../master_videos/{filename}",
            "statusText": "✨ MASTER VIDEO (READY TO PUBLISH)",
            "statusClass": "status-special",
            "duration": f"Master • {sz_mb} MB",
            "ytId": "",
            "views": "Viral Master",
            "retention": "High Retention"
        }
    video_entries.append(entry)

total_count = len(video_entries)
print(f"[*] Generated {total_count} player entries.")

# Read existing HTML template
with open(THEATER_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Replace total count
html = re.sub(
    r'<div class="playlist-header">🎬 Master Video Library \(<span id="totalVideosCount">\d+</span> Episodes\)</div>',
    f'<div class="playlist-header">🎬 Master Video Library (<span id="totalVideosCount">{total_count}</span> Episodes)</div>',
    html
)

# Replace videos JS array safely using string split
start_marker = "const videos = ["
end_marker = "const player = document.getElementById(\"mainVideo\");"

if start_marker in html and end_marker in html:
    part1 = html[:html.find(start_marker)]
    part2 = html[html.find(end_marker):]
    html = part1 + f"const videos = {json.dumps(video_entries, indent=6)};\n\n    let currentIndex = {total_count - 1};\n    " + part2

with open(THEATER_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[SUCCESS] Updated {THEATER_FILE} with all {total_count} master videos!")
