"""
Render Episode 1: The Forbidden Black Onion (Eli & Kevin Part 3)
Assembles 5 3D keyframes with cinematic Ken Burns motion, branding overlay,
and broadcast-normalized neural voiceover audio into an MP4 video.
"""
import os
import sys
import subprocess
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE_DIR = r"D:\Antigravity\Pro"
SERIES_DIR = os.path.join(WORKSPACE_DIR, "Riyo_3D_Roblox_Series")
BRAIN_DIR = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994"

AUDIO_PATH = os.path.join(SERIES_DIR, "audio_production", "story1_black_onion.wav")
WATERMARK_PATH = os.path.join(SERIES_DIR, "brand_assets", "riyo_3d_corner_watermark.png")
OUTPUT_VIDEO = os.path.join(SERIES_DIR, "master_videos", "SHORT_6_The_Forbidden_Black_Onion.mp4")

# Scene image slots
SCENES = [
    {
        "name": "scene1_recap",
        "duration": 14.0,
        "zoom_type": "in",  # slow zoom in
    },
    {
        "name": "scene2_carrot",
        "duration": 18.0,
        "zoom_type": "pan_down",
    },
    {
        "name": "scene3_vault",
        "duration": 18.0,
        "zoom_type": "in",
    },
    {
        "name": "scene4_throw",
        "duration": 18.0,
        "zoom_type": "out",
    },
    {
        "name": "scene5_tamed_titan",
        "duration": 21.74,
        "zoom_type": "in",
    }
]

def build_video(image_paths):
    print("=" * 60)
    print("🎬 Rendering SHORT #6: The Forbidden Black Onion (720x1280 @ 30fps)")
    print("=" * 60)
    
    temp_dir = os.path.join(WORKSPACE_DIR, "temp_render_black_onion")
    os.makedirs(temp_dir, exist_ok=True)
    
    clip_files = []
    
    for idx, (sc, img) in enumerate(zip(SCENES, image_paths)):
        clip_out = os.path.join(temp_dir, f"clip_{idx}.mp4")
        dur = sc["duration"]
        fps = 30
        frames = int(dur * fps)
        
        print(f"\n[+] Processing Scene {idx+1}: {img} (Duration: {dur}s, {frames} frames)...")
        
        # Build Ken Burns effect via ffmpeg zoompan
        # Output 720x1280 (9:16)
        if sc["zoom_type"] == "in":
            # zoom from 1.0 to 1.15
            filter_str = f"scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,zoompan=z='min(zoom+0.0003,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=720x1280:fps={fps}"
        elif sc["zoom_type"] == "out":
            filter_str = f"scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,zoompan=z='if(lte(zoom,1.0),1.15,max(1.001,zoom-0.0003))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=720x1280:fps={fps}"
        else:
            filter_str = f"scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,zoompan=z='min(zoom+0.0002,1.10)':x='iw/2-(iw/zoom/2)':y='min(ih/2,ih*0.3+on*0.2)':d={frames}:s=720x1280:fps={fps}"
        
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img,
            "-vf", filter_str,
            "-t", str(dur),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
            clip_out
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clip_files.append(clip_out)
        print(f"    [OK] Clip {idx+1} ready: {clip_out}")

    # Create concat list
    concat_list = os.path.join(temp_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for c in clip_files:
            f.write(f"file '{c.replace(chr(92), '/')}'\n")

    concatenated_video = os.path.join(temp_dir, "video_raw.mp4")
    print("\n[+] Concatenating visual clips...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c", "copy",
        concatenated_video
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Merge audio & watermark
    print(f"\n[+] Merging audio narration & studio branding watermark...")
    final_cmd = [
        "ffmpeg", "-y",
        "-i", concatenated_video,
        "-i", AUDIO_PATH,
        "-i", WATERMARK_PATH,
        "-filter_complex", "[0:v][2:v]overlay=28:36[v]",
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-b:v", "4000k",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    subprocess.run(final_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Cleanup temp
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print("\n" + "=" * 60)
    print(f"✨ MASTER VIDEO GENERATED SUCCESSFULLY!")
    print(f"File: {OUTPUT_VIDEO}")
    print(f"Size: {size_mb:.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 5:
        build_video(sys.argv[1:6])
    else:
        print("Usage: python render_story1_black_onion_video.py <img1> <img2> <img3> <img4> <img5>")
