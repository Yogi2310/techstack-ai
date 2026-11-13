"""
Upload script for 'How a 78-Byte File Crashed 8.5 Million Windows PCs' Short
Channel: @TechStacAI
"""
import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"D:\Antigravity\Pro")
from upload_to_youtube import upload_video

def main():
    video_path = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_outage_short\MICROSOFT_OUTAGE_SHORT_9x16.mp4"
    title = "How a 78-Byte File Crashed 8.5 Million Windows PCs 💥 #shorts #tech"
    description = (
        "The biggest IT outage in human history wasn't a hacker. It was a single 78-byte configuration file!\n\n"
        "0:00 - How 8.5M Computers Died in 1 Second\n"
        "0:09 - The Ring 0 Kernel Pointer Bug (Channel File 291)\n"
        "0:19 - The Infinite BSOD Boot Loop\n"
        "0:28 - The Manual USB Key Safe Mode Recovery\n"
        "0:37 - The Golden Rule: Staged Canary Rollouts\n\n"
        "Subscribe to @TechStacAI for real engineering post-mortems and AI breakthroughs!\n\n"
        "#shorts #tech #microsoft #crowdstrike #programming #coding #windows #softwareengineer #cybersecurity"
    )
    tags = [
        "shorts", "tech", "microsoft", "crowdstrike", "outage",
        "windows", "bsod", "programming", "coding",
        "software engineering", "cybersecurity", "techstack ai"
    ]

    print("Uploading Microsoft/CrowdStrike Outage Short to YouTube channel @TechStacAI...")
    video_id = upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="28",
        privacy_status="public"
    )

    if video_id:
        print(f"\n[COMPLETE] Video is LIVE on YouTube!")
        print(f"URL: https://www.youtube.com/shorts/{video_id}")
    else:
        print("\n[ERROR] Upload failed.")

if __name__ == '__main__':
    main()
