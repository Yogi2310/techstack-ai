"""
Upload script for 'Microsoft Broke Again Today! 130,000+ Teams & Outlook Crashes Explained' Short
Channel: @TechStacAI
"""
import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"D:\Antigravity\Pro")
from upload_to_youtube import upload_video

def main():
    video_path = r"D:\Antigravity\Pro\agentic-code\projects\microsoft_today_outage_short\MICROSOFT_TODAY_OUTAGE_SHORT_9x16.mp4"
    title = "Microsoft Broke Again Today! 130,000+ Crashes Explained 💥 #shorts #tech"
    description = (
        "Microsoft 365, Teams, Outlook, and Copilot went down globally today in incident MO1550821!\n\n"
        "Here is what actually happened inside Microsoft's backend infrastructure and why automated health checks triggered a cascading failure.\n\n"
        "0:00 - Teams & Outlook Global Crash (130,000+ Reports)\n"
        "0:11 - Incident MO1550821: The Failed Watchdog Health Check\n"
        "0:22 - The Thundering Herd: Dead Nodes Overwhelm Survivors\n"
        "0:32 - Microsoft SRE Emergency Traffic Bypass & Stabilization\n"
        "0:41 - The Golden Rule: Circuit Breaker Max Eviction Rate\n\n"
        "Subscribe to @TechStacAI for real engineering post-mortems and AI breakthroughs!\n\n"
        "#shorts #tech #microsoft #outage #teams #outlook #programming #coding #azure #cloud #softwareengineer #techstackai"
    )
    tags = [
        "shorts", "tech", "microsoft", "outage", "teams",
        "outlook", "copilot", "azure", "programming", "coding",
        "software engineering", "systems design", "techstack ai"
    ]

    print("Uploading Microsoft Today Outage Short to YouTube channel @TechStacAI...")
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
