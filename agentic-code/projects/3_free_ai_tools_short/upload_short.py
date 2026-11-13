"""
Upload script for '3 Free AI Tools That Feel Illegal for Developers' Short
Channel: @TechStacAI
"""
import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"D:\Antigravity\Pro")
from upload_to_youtube import upload_video

def main():
    video_path = r"D:\Antigravity\Pro\agentic-code\projects\3_free_ai_tools_short\3_FREE_AI_TOOLS_SHORT_9x16.mp4"
    title = "3 Free AI Tools That Feel Illegal for Developers 🤫 #shorts #coding"
    description = (
        "Stop coding boilerplate by hand in 2026! Here are 3 game-changing free AI tools every developer needs:\n\n"
        "0:00 - Stop Hand-Coding Boilerplate\n"
        "0:08 - Tool 1: Antigravity Code Agent (Autonomous Repo & Bug Fixer)\n"
        "0:21 - Tool 2: Bolt.new & Cursor (Instant Full-Stack Cloud Sandbox)\n"
        "0:31 - Tool 3: Gemini 3.1 Flash (1M Token Massive Codebase Ingest)\n"
        "0:40 - Next Step: Which tool are you testing first?\n\n"
        "Subscribe to @TechStacAI for daily AI developer hacks!\n\n"
        "#shorts #coding #developer #ai #programming #softwareengineer #webdev #python #tech"
    )
    tags = [
        "shorts", "coding", "developer", "ai tools", "antigravity",
        "bolt.new", "cursor", "gemini 3.1 flash", "programming",
        "software engineering", "web dev", "techstack ai", "tech"
    ]

    print("Uploading high-retention 9:16 Short to YouTube channel @TechStacAI...")
    video_id = upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="28",
        privacy_status="public"
    )

    if video_id:
        print(f"[COMPLETE] Short is LIVE on YouTube!")
        print(f"URL: https://www.youtube.com/shorts/{video_id}")
    else:
        print("[ERROR] Upload failed.")

if __name__ == '__main__':
    main()
