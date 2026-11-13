import os
import glob
import subprocess
import shutil

PROJECT_DIR = r"D:\Antigravity\Pro\Hanuman_Returns_Project"
RAW_CLIPS_DIR = os.path.join(PROJECT_DIR, "raw_clips")
AUDIO_MASTER = os.path.join(PROJECT_DIR, "audio", "hanuman_returns_master_audio.wav")
OUTPUT_VIDEO = os.path.join(PROJECT_DIR, "videos", "hanuman_returns_ai_photorealistic_short.mp4")

def assemble_clips():
    clips = sorted(glob.glob(os.path.join(RAW_CLIPS_DIR, "*.mp4")) + glob.glob(os.path.join(RAW_CLIPS_DIR, "*.mov")))
    if not clips:
        print(f"[!] No video clips found in: {RAW_CLIPS_DIR}")
        print("Please place your generated AI video clips (from Kling, Luma, Runway, or Veo) into that directory.")
        return False

    print(f"[+] Found {len(clips)} video clips to assemble:")
    for c in clips:
        print(f"  - {os.path.basename(c)}")

    # Create concat list with 9:16 normalization (1080x1920 or 720x1280)
    concat_txt = os.path.join(PROJECT_DIR, "scripts", "concat_list.txt")
    norm_clips = []
    
    for i, c in enumerate(clips):
        norm_path = os.path.join(RAW_CLIPS_DIR, f"norm_clip_{i}.mp4")
        cmd_norm = [
            "ffmpeg", "-y", "-i", c,
            "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=24",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-an", norm_path
        ]
        subprocess.run(cmd_norm, check=True)
        norm_clips.append(norm_path)

    with open(concat_txt, "w") as f:
        for nc in norm_clips:
            # Escape path for ffmpeg concat demuxer
            clean_path = nc.replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    # Concatenate and merge with master audio
    cmd_merge = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", AUDIO_MASTER,
        "-c:v", "libx264", "-crf", "18", "-preset", "slow",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    subprocess.run(cmd_merge, check=True)
    print(f"\n[🎉] Assembled Master Photorealistic AI Video:")
    print(f"     {OUTPUT_VIDEO}")
    return True

if __name__ == "__main__":
    assemble_clips()
