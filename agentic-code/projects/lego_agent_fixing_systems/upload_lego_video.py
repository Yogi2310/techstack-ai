import os, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add root directory to sys.path to import upload_to_youtube
sys.path.append(r"D:\Antigravity\Pro")
from upload_to_youtube import upload_video

VIDEO_FILE = r"D:\Antigravity\Pro\agentic-code\projects\lego_agent_fixing_systems\LEGO_AGENT_FIXING_SYSTEMS_16x9.mp4"

TITLE = "🧱 When AI Agents Fix Production at 2 AM (LEGO Edition) 🤖 | Autonomous Dev Loop"

DESCRIPTION = """When the server rack crashes at 2 AM and alerts start firing, this Autonomous 3D LEGO Minifigure Agent springs into action! 🤖🧱

Watch the full closed-loop autonomous repair:
0:00 - Critical server connection leak alert
0:10 - Laser diagnostic & 1x2 hotfix brick snap-in
0:22 - Cyber terminal typing & 42 regression tests pass
0:32 - Technic master deployment lever pull & power surge
0:42 - Cloud payload rocket launch & victory celebration!

Would you trust an AI agent with your production servers? Drop your thoughts below! 👇
Like & Subscribe for more autonomous agentic workflows and animations.

#ai #agents #lego #softwareengineering #devops #automation #coding #python #tech #animation
"""

TAGS = [
    "ai agents",
    "autonomous agents",
    "lego animation",
    "software engineering",
    "coding",
    "devops",
    "cloud computing",
    "lego brickfilm",
    "tech animation",
    "ai automation",
    "programming",
    "antigravity",
    "developer humor"
]

print(f"[+] Starting YouTube upload for: {VIDEO_FILE}")
video_id = upload_video(
    file_path=VIDEO_FILE,
    title=TITLE,
    description=DESCRIPTION,
    tags=TAGS,
    category_id="28",
    privacy_status="public"
)

if video_id:
    print(f"\n[+] Video successfully published! ID: {video_id}")
    print(f"[+] Watch Link: https://youtu.be/{video_id}")
else:
    print("\n[!] Upload failed or did not return video ID.")
