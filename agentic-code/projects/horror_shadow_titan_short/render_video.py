"""
Cinematic Video Renderer for 'The Midnight Colossus of Blackwood Creek' 60s Horror Short
Composites high-res 3D scenes, camera pans, heartbeat camera pulses, earth-shaking stomps,
glowing vignettes, dynamic subtitles, and mixes with the 55.6s master audio.
"""
import os
import sys
import math
import subprocess
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# --- FONTS ---
def get_font(name, size):
    try:
        path = os.path.join("C:/Windows/Fonts", name)
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_title = get_font("arialbd.ttf", 36)
font_badge = get_font("arialbd.ttf", 46)
font_sub_bold = get_font("arialbd.ttf", 44)
font_sub_small = get_font("arial.ttf", 24)
font_cta = get_font("arialbd.ttf", 52)

PROJECT_DIR = r"D:\Antigravity\Pro\agentic-code\projects\horror_shadow_titan_short"
SCENES_DIR = os.path.join(PROJECT_DIR, "scenes")
AUDIO_FILE = os.path.join(PROJECT_DIR, "audio", "horror_master_audio.wav")
OUTPUT_VIDEO = os.path.join(PROJECT_DIR, "THE_MIDNIGHT_COLOSSUS_9x16.mp4")

# Load scenes
def load_and_prep_image(path, target_w=1080, target_h=1920):
    im = Image.open(path).convert('RGB')
    # Fit into 1080x1920 by crop/scale
    w, h = im.size
    aspect = w / h
    target_aspect = target_w / target_h
    
    if aspect > target_aspect:
        # Wider than 9:16 -> scale by height
        new_h = target_h
        new_w = int(target_h * aspect)
    else:
        # Taller than 9:16 -> scale by width
        new_w = target_w
        new_h = int(target_w / aspect)
        
    scaled = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    # Center crop
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return scaled.crop((left, top, left + target_w, top + target_h))

print("Loading scene textures...")
img_scene1 = load_and_prep_image(os.path.join(SCENES_DIR, "scene1_village_mist.jpg"))
img_scene2 = load_and_prep_image(os.path.join(SCENES_DIR, "scene2_hermit_warning.png"))
img_scene3 = load_and_prep_image(os.path.join(SCENES_DIR, "scene3_boy_confusion.png"))
img_scene4 = load_and_prep_image(os.path.join(SCENES_DIR, "scene4_shadow_titan.png"))
img_scene5 = load_and_prep_image(os.path.join(SCENES_DIR, "scene5_screaming_escape.png"))

# Subtitle timeline
subtitles = [
    (0.0, 3.5, "Rule #1 of Blackwood Creek:"),
    (3.5, 7.5, "When the village bells strike thirteen at midnight..."),
    (7.5, 11.0, "You do NOT stay out in the mist. 🌙"),
    (11.0, 15.0, "Old Man Miller slammed open his shutter..."),
    (15.0, 18.5, "Tossing down a rusted iron key! 🗝️"),
    (18.5, 22.0, "\"KID! Get inside! He smells you... and he's off the chain!\""),
    (22.0, 25.5, "Then... the street went dead silent. ⏳"),
    (25.5, 29.0, "The puddles began to ripple... 💧"),
    (29.0, 33.0, "An immense shadow stretched 40 feet across the road!"),
    (33.0, 37.0, "Rising out of the black pines... 🌲"),
    (37.0, 41.0, "The COLOSSUS of Hollow Creek! 💀🔥"),
    (41.0, 44.0, "Two burning red eyes... and a jaw of razor fangs!"),
    (44.0, 47.5, "With a bone-shattering roar, IT CHARGED! 🚨"),
    (47.5, 51.5, "I lunged for the door as giant claws slammed the dirt!"),
    (51.5, 55.6, "DID I MAKE IT IN TIME? COMMENT FOR PART 2! 👇")
]

def render_frame(t, total_d):
    w, h = 1080, 1920
    
    # 1. Determine active scene & transitions
    if t < 11.0:
        base_img = img_scene1
        # Slow creeping zoom-in
        zoom = 1.0 + (t / 11.0) * 0.08
        shake_x, shake_y = 0, 0
        badge_text = "THE CURSED VILLAGE OF BLACKWOOD 🌙"
        badge_col = (255, 180, 50)
    elif t < 22.0:
        base_img = img_scene2
        local_t = t - 11.0
        zoom = 1.0 + (local_t / 11.0) * 0.06
        shake_x = int(math.sin(t * 15.0) * 2)
        shake_y = int(math.cos(t * 12.0) * 2)
        badge_text = "⚠️ THE HERMIT'S WARNING: GET INSIDE!"
        badge_col = (255, 80, 80)
    elif t < 33.0:
        base_img = img_scene3
        local_t = t - 22.0
        # Heartbeat pulse zoom!
        hb_phase = (local_t % 0.85)
        pulse = math.exp(-hb_phase * 10) * 0.02
        zoom = 1.02 + pulse
        shake_x, shake_y = 0, 0
        badge_text = "THE GROUND BEGINS TO VIBRATE... ⏳"
        badge_col = (100, 200, 255)
    elif t < 44.0:
        base_img = img_scene4
        local_t = t - 33.0
        zoom = 1.0 + (local_t / 11.0) * 0.07
        # Earthquake stomp shake at stomps
        stomp_phase = (local_t % 4.0)
        stomp_impact = max(0, 1.0 - stomp_phase * 3.0)
        shake_x = int(math.sin(t * 40.0) * (6 * stomp_impact))
        shake_y = int(math.cos(t * 35.0) * (5 * stomp_impact))
        badge_text = "💀 THE SHADOW COLOSSUS EMERGES 💀"
        badge_col = (255, 40, 40)
    else:
        base_img = img_scene5
        local_t = t - 44.0
        zoom = 1.04 + (local_t / 11.6) * 0.08
        # Intense chase camera shake
        shake_x = int(math.sin(t * 55.0) * 9 + math.cos(t * 33.0) * 5)
        shake_y = int(math.cos(t * 48.0) * 8 + math.sin(t * 27.0) * 4)
        badge_text = "🚨 SPRINT FOR THE DOOR! RUN! 🚨"
        badge_col = (255, 30, 30)

    # 2. Apply Zoom & Camera Shake
    bw = int(w * zoom)
    bh = int(h * zoom)
    scaled = base_img.resize((bw, bh), Image.Resampling.BILINEAR)
    
    cx = (bw - w) // 2 + shake_x
    cy = (bh - h) // 2 + shake_y
    cx = max(0, min(bw - w, cx))
    cy = max(0, min(bh - h, cy))
    
    frame = scaled.crop((cx, cy, cx + w, cy + h)).copy()
    
    # 3. Horror Lighting Overlays
    if 33.0 <= t < 44.0:
        # Subtle ominous red vignette pulsing
        pulse_red = (math.sin(t * 6.0) + 1.0) * 0.5
        red_tint = Image.new('RGB', (w, h), (180, 10, 10))
        frame = Image.blend(frame, red_tint, 0.12 * pulse_red)
    elif t >= 44.0:
        # High-intensity red alert pulse during chase
        chase_pulse = (math.sin(t * 12.0) + 1.0) * 0.5
        red_tint = Image.new('RGB', (w, h), (220, 20, 20))
        frame = Image.blend(frame, red_tint, 0.18 + 0.14 * chase_pulse)
        
    draw = ImageDraw.Draw(frame)
    
    # 4. Cinematic Vignette (darken top & bottom for high contrast)
    draw.rectangle([0, 0, w, 220], fill=(0, 0, 0, 160))
    draw.rectangle([0, h - 380, w, h], fill=(0, 0, 0, 190))
    
    # 5. Top Header Card
    badge_bg = (15, 18, 26, 220)
    draw.rounded_rectangle([40, 60, w - 40, 150], radius=18, fill=(15, 18, 25), outline=badge_col, width=3)
    
    # Text in header
    bbox = draw.textbbox((0, 0), badge_text, font=font_title)
    bw_txt = bbox[2] - bbox[0]
    draw.text(((w - bw_txt) // 2, 85), badge_text, font=font_title, fill=badge_col)
    
    # 6. Dynamic Subtitles in Lower Third
    cur_sub = ""
    for s_start, s_end, text in subtitles:
        if s_start <= t < s_end:
            cur_sub = text
            break
            
    if cur_sub:
        lines = textwrap.wrap(cur_sub, width=28)
        card_h = len(lines) * 58 + 36
        card_top = 1580 - card_h // 2
        
        # Subtitle background bubble
        draw.rounded_rectangle([50, card_top, w - 50, card_top + card_h], radius=22, fill=(10, 12, 18), outline=(255, 200, 50) if t < 33 else (255, 60, 60), width=3)
        
        for idx, line in enumerate(lines):
            l_bbox = draw.textbbox((0, 0), line, font=font_sub_bold)
            l_w = l_bbox[2] - l_bbox[0]
            ly = card_top + 18 + idx * 58
            # Glowing shadow
            draw.text(((w - l_w) // 2 + 2, ly + 2), line, font=font_sub_bold, fill=(0, 0, 0))
            draw.text(((w - l_w) // 2, ly), line, font=font_sub_bold, fill=(255, 255, 255))
            
    # 7. Progress Bar at very bottom
    prog = min(1.0, t / total_d)
    draw.rectangle([0, h - 12, int(w * prog), h], fill=badge_col)
    
    return frame

def main():
    total_duration = 55.60
    fps = 24
    total_frames = int(total_duration * fps)
    
    print(f"Rendering {total_frames} frames ({total_duration:.2f}s @ {fps}fps)...", flush=True)
    
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",  # pipe from stdin
        "-i", AUDIO_FILE,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    
    proc = subprocess.Popen(cmd_ffmpeg, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for frame_idx in range(total_frames):
        t = frame_idx / float(fps)
        img = render_frame(t, total_duration)
        proc.stdin.write(img.tobytes())
        
        if frame_idx % 120 == 0 or frame_idx == total_frames - 1:
            pct = (frame_idx + 1) / total_frames * 100
            print(f"Render progress: {pct:.1f}% ({frame_idx + 1}/{total_frames} frames, t={t:.1f}s)", flush=True)
            
    proc.stdin.close()
    proc.wait()
    
    if proc.returncode == 0:
        sz_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        print(f"\n[SUCCESS] Render complete!", flush=True)
        print(f"Output video: {OUTPUT_VIDEO}", flush=True)
        print(f"Size: {sz_mb:.2f} MB", flush=True)
    else:
        print(f"\n[ERROR] FFmpeg failed with code {proc.returncode}", flush=True)

if __name__ == '__main__':
    main()
