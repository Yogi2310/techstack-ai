"""
Upload script for 'Why You NEVER Deploy on Friday 💀🔥 #shorts #programming #coding' Short
Channel: @TechStacAI
Starring: Pixar 3D Senior Dev Mascot
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"D:\Antigravity\Pro")
from upload_to_youtube import upload_video

def main(schedule_peak=False):
    video_path = r"D:\Antigravity\Pro\agentic-code\projects\friday_deploy_disaster_short\FRIDAY_DEPLOY_DISASTER_9x16.mp4"
    title = "Why You NEVER Deploy on Friday 💀🔥 #shorts #programming #coding"
    description = (
        "It's 4:59 PM on a Friday. The junior engineer whispers: 'It's just a one-line config change...' 🚨💀\n\n"
        "Watch our 3D developer mascot race against time to debug an unindexed SQL deadlock, "
        "kill ghost database locks, and deploy an emergency hotfix before the weekend begins!\n\n"
        "⏱️ SCENE BREAKDOWN:\n"
        "0:00 - The 4:59 PM Innocent Git Push\n"
        "0:12 - Red Alert! Production 500 Spike & PagerDuty Alarm\n"
        "0:24 - Root Cause: Table Scan Deadlock on Unindexed Column\n"
        "0:36 - Emergency Hotfix: Index Created & Pods Restarted\n"
        "0:46 - The Senior Dev Golden Rule: Read-Only Fridays!\n\n"
        "💬 QUESTION: What is the worst production bug YOU ever pushed before a weekend?\n"
        "Drop your story in the comments! 👇\n\n"
        "🔔 Subscribe to @TechStacAI for relatable 3D developer animations, system architecture, and AI engineering insights!\n\n"
        "#shorts #programming #coding #softwareengineering #developer #programmer #webdevelopment #tech #humor #python #javascript #sql #devops #database #techstackai #funny #storytime"
    )
    tags = [
        "shorts", "programming", "coding", "software engineering", "developer",
        "programmer", "web development", "tech humor", "devops", "sql deadlock",
        "friday deploy", "database", "python", "javascript", "code", "tech",
        "animation", "3d animation", "pixar developer", "techstack ai"
    ]

    # If scheduling for Friday Peak Time (e.g., 6:30 PM IST = 13:00:00Z)
    publish_at = "2026-11-13T13:00:00Z" if schedule_peak else None
    privacy = "private" if schedule_peak else "public"

    print(f"Uploading Friday Deploy Disaster Short to YouTube channel @TechStacAI...")
    if schedule_peak:
        print(f"Scheduled for Peak Time: {publish_at} (6:30 PM IST)")
    else:
        print("Publishing immediately as PUBLIC...")

    video_id = upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="28",
        privacy_status=privacy,
        publish_at=publish_at
    )

    if video_id:
        print(f"\n[COMPLETE] Video uploaded successfully!")
        print(f"URL: https://www.youtube.com/shorts/{video_id}")
        return video_id
    else:
        print("\n[ERROR] Upload failed.")
        return None

if __name__ == '__main__':
    # Check if --schedule flag was passed
    schedule = "--schedule" in sys.argv
    main(schedule_peak=schedule)
