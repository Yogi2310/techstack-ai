"""
Upload script for 'When The Village Bell Strikes 13... RUN. 💀🔥 #shorts #horror #animation'
Channel: @TechStacAI
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"D:\Antigravity\Pro")
from upload_to_youtube import upload_video

def main(schedule_peak=False):
    video_path = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short\THE_MIDNIGHT_COLOSSUS_9x16.mp4"
    title = "When The Village Bell Strikes 13... RUN. 💀🔥 #shorts #horror #animation"
    description = (
        "Rule number one of Blackwood Creek: When the village bells strike thirteen at midnight... you do NOT stay out in the mist. 🌙💀\n\n"
        "Old Man Miller tossed down a rusted iron key, but it was already too late. "
        "Emerging through the black pines was the Colossus of Hollow Creek—burning red eyes, razor fangs, and 40 feet of pure nightmare.\n\n"
        "⏱️ SCENE BREAKDOWN:\n"
        "0:00 - The Midnight Mist & Cursed Thirteenth Bell\n"
        "0:11 - Old Man Miller's Frantic Shutter Warning\n"
        "0:22 - Dead Silence & The Tremor\n"
        "0:33 - The 40-Foot Colossus Rises\n"
        "0:44 - The Screaming Sprint & Claw Slam Climax\n\n"
        "💬 Did I make it inside the cabin in time?\n"
        "Drop a comment below if you want PART 2! 👇🔥\n\n"
        "🔔 Subscribe to @TechStacAI for original 3D animated cinematic stories and AI creative projects!\n\n"
        "#shorts #animation #3danimation #horror #horrormovies #creepy #storytime #cgi #blender3d #unrealengine #monster #techstackai #viral"
    )
    tags = [
        "shorts", "animation", "3d animation", "horror", "horrormovies", "creepy",
        "storytime", "cgi", "blender 3d", "unreal engine", "monster", "colossus",
        "shadow titan", "viral shorts", "trending", "techstack ai"
    ]

    privacy = "public"
    publish_at = None

    print(f"Uploading The Midnight Colossus Short to YouTube channel @TechStacAI...")
    video_id = upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="1",  # Film & Animation
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
    main()
