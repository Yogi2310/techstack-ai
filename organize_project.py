import os
import shutil

BASE_DIR = r"D:\Antigravity\Pro\Riyo_3D_Roblox_Series"
ARTIFACT_DIR = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994"
PRO_DIR = r"D:\Antigravity\Pro"
IG_DIR = os.path.join(PRO_DIR, "instagram_downloads")

dirs = [
    "master_videos",
    "brand_assets",
    "outro_package",
    "scripts_and_transcripts",
    "upload_tools",
    "interactive_players",
    "docs"
]

for d in dirs:
    os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

copies = [
    # 1. Master Videos
    (os.path.join(PRO_DIR, "ROBLOX_STORY_ELI_AND_KEVIN.mp4"), os.path.join(BASE_DIR, "master_videos", "SHORT_1_Throw_Food_For_Pets_Part1.mp4")),
    (os.path.join(PRO_DIR, "ROBLOX_STORY_100_YEAR_OCEAN_RIYO_FINAL.mp4"), os.path.join(BASE_DIR, "master_videos", "SHORT_2_100_Year_Ocean_Tide.mp4")),
    (os.path.join(PRO_DIR, "ROBLOX_STORY_PART2_COLOSSUS_RIYO_FINAL.mp4"), os.path.join(BASE_DIR, "master_videos", "SHORT_3_The_Colossus_Awakens_Part2.mp4")),

    # 2. Brand Assets
    (os.path.join(PRO_DIR, "riyo_3d_master_transparent.png"), os.path.join(BASE_DIR, "brand_assets", "riyo_3d_master_transparent.png")),
    (os.path.join(PRO_DIR, "riyo_3d_corner_watermark.png"), os.path.join(BASE_DIR, "brand_assets", "riyo_3d_corner_watermark.png")),
    (os.path.join(PRO_DIR, "riyo_channel_profile_pic.png"), os.path.join(BASE_DIR, "brand_assets", "riyo_channel_profile_pic.png")),
    (os.path.join(ARTIFACT_DIR, "riyo_studio_logo_3d_1794741520451.jpg"), os.path.join(BASE_DIR, "brand_assets", "riyo_studio_logo_3d_raw.jpg")),

    # 3. Outro Package
    (os.path.join(PRO_DIR, "outro_clip.mp4"), os.path.join(BASE_DIR, "outro_package", "outro_clip.mp4")),
    (os.path.join(PRO_DIR, "outro_audio.wav"), os.path.join(BASE_DIR, "outro_package", "outro_audio.wav")),
    (os.path.join(ARTIFACT_DIR, "outro_card_preview.gif"), os.path.join(BASE_DIR, "outro_package", "outro_card_preview.gif")),
    (os.path.join(PRO_DIR, "generate_outro.py"), os.path.join(BASE_DIR, "outro_package", "generate_outro.py")),

    # 4. Scripts & Transcripts
    (os.path.join(IG_DIR, "transcript_dfo7js8.txt"), os.path.join(BASE_DIR, "scripts_and_transcripts", "Part1_Throw_Food_Transcript.txt")),
    (os.path.join(IG_DIR, "transcript_dfo6ic9.txt"), os.path.join(BASE_DIR, "scripts_and_transcripts", "Ocean_Tide_Transcript.txt")),
    (os.path.join(IG_DIR, "reel_dfqq88n.txt"), os.path.join(BASE_DIR, "scripts_and_transcripts", "Part2_Colossus_Awakens_Transcript.txt")),
    (os.path.join(ARTIFACT_DIR, "ROBLOX_ANIMATION_BREAKDOWN_ANALYSIS.md"), os.path.join(BASE_DIR, "scripts_and_transcripts", "ROBLOX_ANIMATION_BREAKDOWN_ANALYSIS.md")),

    # 5. Upload Tools
    (os.path.join(PRO_DIR, "upload_roblox_short.py"), os.path.join(BASE_DIR, "upload_tools", "upload_part1_short.py")),
    (os.path.join(PRO_DIR, "upload_ocean_short.py"), os.path.join(BASE_DIR, "upload_tools", "upload_ocean_short.py")),
    (os.path.join(PRO_DIR, "upload_part2_short.py"), os.path.join(BASE_DIR, "upload_tools", "upload_part2_short.py")),

    # 6. Interactive Players
    (os.path.join(ARTIFACT_DIR, "watch_ocean_story_riyo.html"), os.path.join(BASE_DIR, "interactive_players", "watch_ocean_story.html")),
    (os.path.join(ARTIFACT_DIR, "watch_part2_colossus_riyo.html"), os.path.join(BASE_DIR, "interactive_players", "watch_part2_colossus.html")),

    # 7. Docs
    (os.path.join(PRO_DIR, "RIYO_3D_OCEAN_STORY_PRODUCTION_DOCS.md"), os.path.join(BASE_DIR, "docs", "RIYO_3D_OCEAN_STORY_PRODUCTION_DOCS.md")),
    (os.path.join(PRO_DIR, "RIYO_3D_PART2_COLOSSUS_STORY_DOCS.md"), os.path.join(BASE_DIR, "docs", "RIYO_3D_PART2_COLOSSUS_STORY_DOCS.md")),
]

copied_count = 0
for src, dst in copies:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"[+] Copied: {os.path.basename(dst)} ({os.path.getsize(dst)} bytes)")
        copied_count += 1
    else:
        print(f"[!] Warning: Missing source: {src}")

print(f"\n[SUCCESS] Successfully organized {copied_count} files into {BASE_DIR}")
