import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from upload_to_youtube import upload_video

video_path = r"D:\Antigravity\Pro\ai_prompting_framework.mp4"
title = "90% of People Use AI Wrong (Use This 3-Step Formula Instead) #shorts"
description = """Stop asking AI to "write me a script". That’s why your output sounds robotic and generic.

Here is the exact 3-step prompt framework top creators use to produce 10x better content in seconds:

1. ROLE: Give it a strict persona ("Viral YouTube editor who hates fluff")
2. RULE: Negative constraints (Ban buzzwords, pleasantries, filler)
3. RESULT: Feed 1 winning reference to match your exact rhythm

Comment PROMPT below to get the full prompt cheat sheet sent directly to you!

#shorts #ai #chatgpt #productivity #creators #promptengineering #automation
"""

tags = ["shorts", "ai", "chatgpt", "prompt engineering", "ai tools", "productivity", "content creator", "youtube shorts"]

# Scheduled for tomorrow, Saturday October 31, 2026 at 12:00 PM IST (06:30:00 UTC)
publish_time = "2026-10-31T06:30:00Z"

print(f"Target Video: {video_path}")
print(f"Title: {title}")
print(f"Scheduled Publish Time (UTC): {publish_time} (12:00 PM IST tomorrow)")

if os.path.exists(video_path):
    video_id = upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="28",
        publish_at=publish_time
    )
    if video_id:
        with open(r"D:\Antigravity\Pro\last_scheduled_video.txt", "w") as f:
            f.write(f"ID: {video_id}\nScheduled: {publish_time}\nTitle: {title}\n")
        print(f"\n[DONE] Video successfully scheduled with ID: {video_id}")
else:
    print(f"Error: {video_path} not found yet.")
