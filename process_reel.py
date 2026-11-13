import os
import subprocess
import json

video_path = r"D:\Antigravity\Pro\instagram_downloads\video_dfrkkpag.mp4"
out_dir = r"D:\Antigravity\Pro\instagram_downloads\snapshots"
brain_dir = r"C:\Users\Yogesh\.gemini\antigravity\brain\e57b91af-4588-4746-9f1a-89a67c9b0994"

os.makedirs(out_dir, exist_ok=True)

# 1. Extract frames at timestamps: 0.5s, 2.0s, 4.0s, 6.0s, 8.0s, 9.5s
timestamps = [0.5, 2.0, 4.0, 6.0, 8.0, 9.5]
for i, ts in enumerate(timestamps):
    frame_name = f"ig_reel_frame_{i+1:02d}_{ts:.1f}s.png"
    out_frame = os.path.join(out_dir, frame_name)
    brain_frame = os.path.join(brain_dir, frame_name)
    cmd = [
        "ffmpeg", "-y", "-ss", str(ts), "-i", video_path,
        "-vframes", "1", "-q:v", "2", out_frame
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(out_frame):
        # copy to brain
        with open(out_frame, 'rb') as f_in, open(brain_frame, 'wb') as f_out:
            f_out.write(f_in.read())
        print(f"Extracted & copied: {frame_name}")

# 2. Extract audio to WAV
audio_path = r"D:\Antigravity\Pro\instagram_downloads\ig_reel_audio.wav"
cmd_audio = [
    "ffmpeg", "-y", "-i", video_path,
    "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_path
]
subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Extracted audio to:", audio_path)

# 3. Create animated preview GIF of the reel
gif_path = os.path.join(out_dir, "ig_reel_preview.gif")
brain_gif = os.path.join(brain_dir, "ig_reel_preview.gif")
cmd_gif = [
    "ffmpeg", "-y", "-i", video_path,
    "-vf", "fps=10,scale=360:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    "-loop", "0", gif_path
]
subprocess.run(cmd_gif, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if os.path.exists(gif_path):
    with open(gif_path, 'rb') as f_in, open(brain_gif, 'wb') as f_out:
        f_out.write(f_in.read())
    print("Created & copied preview GIF:", gif_path)

# Copy thumbnail to brain
thumb_src = r"D:\Antigravity\Pro\instagram_downloads\thumb_dfrkkpag.jpg"
brain_thumb = os.path.join(brain_dir, "ig_reel_thumb.jpg")
if os.path.exists(thumb_src):
    with open(thumb_src, 'rb') as f_in, open(brain_thumb, 'wb') as f_out:
        f_out.write(f_in.read())
    print("Copied thumbnail to brain")

print("Processing complete!")
