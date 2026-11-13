"""
Upload script for 'I Built a Full Stack SaaS in 12 Minutes With Bolt.new' Short
Channel: @TechStacAI
"""
import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"D:\Antigravity\Pro")
from upload_to_youtube import upload_video

def main():
    video_path = r"D:\Antigravity\Pro\agentic-code\projects\bolt_new_saas_short\BOLT_NEW_SAAS_SHORT_9x16.mp4"
    title = "I Built a Full Stack SaaS in 12 Minutes With Bolt.new 🚀 #shorts #coding"
    description = (
        "Stop spending 3 days configuring Docker, Webpack, and database migrations! "
        "Watch how to build and deploy a full-stack SaaS in 12 minutes using Bolt.new.\n\n"
        "0:00 - Stop Spending 3 Days on Config\n"
        "0:11 - WebContainer Engine (Zero Local Setup)\n"
        "0:22 - English Prompt to Architecture (React 19 + Supabase)\n"
        "0:31 - One-Click Production Cloud Deploy\n"
        "0:40 - What will you build first?\n\n"
        "Subscribe to @TechStacAI for daily developer hacks and AI breakthroughs!\n\n"
        "#shorts #coding #developer #boltnew #webdev #programming #ai #softwareengineer #react #tech"
    )
    tags = [
        "shorts", "coding", "developer", "bolt.new", "bolt new",
        "ai tools", "web development", "react", "supabase",
        "software engineering", "programming", "techstack ai", "tech"
    ]

    print("Uploading high-retention 9:16 Short #2 to YouTube channel @TechStacAI...")
    video_id = upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="28",
        privacy_status="public"
    )

    if video_id:
        print(f"\n[COMPLETE] Short #2 is LIVE on YouTube!")
        print(f"URL: https://www.youtube.com/shorts/{video_id}")
    else:
        print("\n[ERROR] Upload failed.")

if __name__ == '__main__':
    main()
