import os
import sys

# Ensure paths
WORKSPACE_DIR = r"D:\Antigravity\Pro"
STUDIO_DIR = os.path.join(WORKSPACE_DIR, "shorts_studio")
TEMP_DIR = os.path.join(STUDIO_DIR, "temp")
LOGO_PATH = os.path.join(WORKSPACE_DIR, "youtube-shorts-factory", "yts-logo.png")
OUTPUT_MP4 = os.path.join(STUDIO_DIR, "exports", "short_3_ai_tools_devs_2026.mp4")

if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)
if STUDIO_DIR not in sys.path:
    sys.path.insert(0, STUDIO_DIR)

from video_engine import generate_video_from_scenes
from upload_to_youtube import upload_video

scenes = [
    {
        "tag": "THE BIG MISTAKE",
        "script": "If you are still writing repetitive boilerplate code by hand, stop.",
        "headline": "STOP CODING SLOW",
        "subtext": "Manual Boilerplate = Wasted Hours\nWork Smarter, Not Slower",
        "action": "confused",
        "color": "#EF4444"
    },
    {
        "tag": "THE 10X ADVANTAGE",
        "script": "These three free AI tools save senior developers over ten hours every single week.",
        "headline": "SAVE 10 HOURS / WK",
        "subtext": "The Elite Developer AI Stack\nFree & Fast Setup",
        "action": "point_right",
        "color": "#22D3EE"
    },
    {
        "tag": "TOOL 1 · TERMINAL",
        "script": "Tool 1: Claude Code. It turns full terminal tasks into autonomous agents that edit your files.",
        "headline": "1. CLAUDE CODE",
        "subtext": "Autonomous Terminal Agent\nRefactor Entire Repositories",
        "action": "snap",
        "color": "#3B82F6"
    },
    {
        "tag": "TOOL 2 · VS CODE",
        "script": "Tool 2: Continue dot dev. Free, open source local AI autocomplete directly inside VS Code.",
        "headline": "2. CONTINUE.DEV",
        "subtext": "Local LLM Autocomplete\n100% Private Codebase",
        "action": "point_right",
        "color": "#10B981"
    },
    {
        "tag": "TOOL 3 · FASTEST",
        "script": "Tool 3: Supermaven. The fastest AI code autocomplete with a massive 300,000 token context window.",
        "headline": "3. SUPERMAVEN",
        "subtext": "300,000 Token Context\nZero Latency Suggestions",
        "action": "triumph",
        "color": "#F59E0B"
    },
    {
        "tag": "THE PAYOFF",
        "script": "Stack these together and you can build and ship features twice as fast with zero fatigue.",
        "headline": "SHIP 2X FASTER",
        "subtext": "10 Hours Saved Weekly\nBuild Without Burnout",
        "action": "triumph",
        "color": "#10B981"
    },
    {
        "tag": "GET THE CONFIGS",
        "script": "Comment CODE below and I will send you the direct installation checklist and configs for free.",
        "headline": "GET SETUP GUIDE",
        "subtext": "COMMENT: CODE\n[✓] Recommended Settings\n[✓] Shortcut Cheatsheet",
        "action": "point_right",
        "color": "#A855F7"
    }
]

print("="*60)
print("[+] STEP 1: Rendering Stickman Short Video...")
print("="*60)

res = generate_video_from_scenes(
    scenes=scenes,
    output_mp4=OUTPUT_MP4,
    temp_dir=TEMP_DIR,
    logo_path=LOGO_PATH
)

print(f"\n[+] Render completed successfully: {OUTPUT_MP4}")
print(f"    Duration: {res['total_duration']:.2f}s | Frames: {res['total_frames']}")

# Copy to root workspace
import shutil
shutil.copy2(OUTPUT_MP4, os.path.join(WORKSPACE_DIR, "ai_dev_tools_2026.mp4"))

title = "3 AI Tools That Save Devs 10 Hours #shorts"
description = """If you are still writing repetitive code from scratch, stop. 

Here are 3 free AI developer tools that will save you 10+ hours every week:
1. Claude Code: Autonomous terminal agent that executes complex refactors.
2. Continue.dev: Open-source local AI code autocomplete inside VS Code.
3. Supermaven: The fastest autocomplete in the world with a 300k token context window.

Comment CODE below to get the full configuration guide and shortcuts sent directly to you!

#shorts #coding #programming #developer #ai #softwareengineering #webdev #vscode
"""
tags = ["shorts", "coding", "programming", "ai tools", "developer", "softwareengineering", "vscode", "webdev"]

print("\n" + "="*60)
print(f"[+] STEP 2: Uploading '{title}' to YouTube...")
print("="*60)

video_id = upload_video(
    file_path=OUTPUT_MP4,
    title=title,
    description=description,
    tags=tags,
    category_id="28",
    privacy_status="public"
)

if video_id:
    with open(os.path.join(WORKSPACE_DIR, "last_uploaded_video.txt"), "w") as f:
        f.write(f"https://youtu.be/{video_id}\n")
    print("\n" + "="*60)
    print(f"🎉 SUCCESS! Video is live on YouTube: https://www.youtube.com/shorts/{video_id}")
    print("="*60)
else:
    print("[!] Upload returned no video_id.")
