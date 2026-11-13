"""
Upload & Schedule script for 'How a 78-Byte File Crashed 8.5M PCs 💥 #shorts #crowdstrike #tech' Short
Channel: @TechStacAI
Scheduled for Peak Time: Saturday, Nov 14, 2026 at 6:30 PM IST (13:00:00Z)
"""
import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"D:\Antigravity\Pro")
from upload_to_youtube import upload_video

def main():
    video_path = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_outage_short\MICROSOFT_OUTAGE_SHORT_9x16.mp4"
    title = "How a 78-Byte File Crashed 8.5M PCs 💥 #shorts #crowdstrike #tech"
    description = (
        "The biggest IT crash in human history wasn't a sophisticated cyberattack. It was a single 78-byte configuration file! 💥\n\n"
        "Here is what actually happened inside Windows Ring 0 kernel memory and why Channel File 291 took down 8.5 million machines in a single second.\n\n"
        "⏱️ TIMESTAMPS:\n"
        "0:00 - The Global IT Disaster (8.5M Computers Down)\n"
        "0:11 - Ring 0 Kernel Bug (Channel File 291 Pointer Crash)\n"
        "0:21 - The Infinite Blue Screen Boot Loop (No Wi-Fi for Patches)\n"
        "0:32 - The Physical USB Thumb Drive Safe Mode Rescue\n"
        "0:42 - The Golden Rule: Staged Canary Rollouts\n\n"
        "🔔 Subscribe to @TechStacAI for real engineering post-mortems and systems architecture!\n\n"
        "#shorts #crowdstrike #microsoft #windows #bsod #tech #trending #programming #coding #softwareengineer #cybersecurity #systemdesign #techstackai"
    )
    tags = [
        "shorts", "crowdstrike", "microsoft", "windows", "bsod", "outage",
        "tech", "trending", "programming", "coding", "software engineering",
        "cybersecurity", "systems design", "techstack ai"
    ]

    # Global Peak Viewing Window: Saturday at 6:30 PM IST (13:00:00 UTC)
    publish_at = "2026-11-14T13:00:00Z"

    print("Uploading and SCHEDULING CrowdStrike Outage Short to YouTube channel @TechStacAI...")
    video_id = upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="28",
        privacy_status="private",
        publish_at=publish_at
    )

    if video_id:
        print(f"\n[COMPLETE] Video is SCHEDULED on YouTube!")
        print(f"URL: https://www.youtube.com/shorts/{video_id}")
        print(f"Scheduled to go public at: {publish_at} (6:30 PM IST Saturday)")
        return video_id
    else:
        print("\n[ERROR] Upload failed.")
        return None

if __name__ == '__main__':
    main()
