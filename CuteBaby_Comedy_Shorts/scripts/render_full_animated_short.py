import os
import sys
import math
import struct
import wave
import random
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

proj_dir = r"D:\Antigravity\Pro\CuteBaby_Comedy_Shorts"
char_path = os.path.join(proj_dir, "characters", "cute_ai_baby_golgappa.jpg")
audio_path = os.path.join(proj_dir, "audio", "demo_video_master_audio.wav")
output_mp4 = os.path.join(proj_dir, "videos", "full_animated_baby_comedy.mp4")

# 1. Load Audio Envelope for precision Lip Sync
with wave.open(audio_path, 'rb') as w:
    n_frames_audio = w.getnframes()
    fs = w.getframerate()
    audio_raw = w.readframes(n_frames_audio)

total_audio_samples = len(audio_raw) // 2
audio_samples = struct.unpack('<' + 'h' * total_audio_samples, audio_raw)

FPS = 24
samples_per_frame = int(fs / FPS)
TOTAL_FRAMES = int(math.ceil(total_audio_samples / samples_per_frame))
TOTAL_DURATION = TOTAL_FRAMES / float(FPS)

envelope = []
for f in range(TOTAL_FRAMES):
    st = f * samples_per_frame
    en = min(total_audio_samples, (f + 1) * samples_per_frame)
    chk = audio_samples[st:en]
    if len(chk) > 0:
        rms = math.sqrt(sum(x*x for x in chk) / len(chk))
        # Normalize speech envelope
        val = min(1.0, max(0.0, (rms - 600.0) / 10000.0))
        envelope.append(val)
    else:
        envelope.append(0.0)

# Smooth envelope
smoothed_env = []
for i in range(len(envelope)):
    w_sum = 0.0
    k_sum = 0.0
    for j in range(max(0, i - 2), min(len(envelope), i + 3)):
        wt = 1.0 - abs(i - j) * 0.25
        w_sum += envelope[j] * wt
        k_sum += wt
    smoothed_env.append(w_sum / k_sum if k_sum > 0 else 0.0)

print(f"[+] Loaded audio: {TOTAL_DURATION:.2f}s, {TOTAL_FRAMES} frames. Max smoothed RMS: {max(smoothed_env):.3f}")

# 2. Base Character Image & Dimensions
raw_char = Image.open(char_path).convert("RGBA")
# Base resolution for Short
WIDTH = 720
HEIGHT = 1280

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
font_hi = ImageFont.truetype(r"C:\Windows\Fonts\Nirmala.ttc", 44)
font_en = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 30)
font_pop = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 36)
font_btn = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 32)

# Subtitle Schedule matching the voice
scenes_sub = [
    {
        "start": 0.0,
        "end": 2.5,
        "hi": "🤤 गोलगप्पे का लालच!",
        "en": "Golgappa Craving!",
        "speaker": "AI Baby Comedy"
    },
    {
        "start": 2.5,
        "end": 7.09,
        "hi": "भैया! एक प्लेट गोलगप्पे... तीखा कम!",
        "en": "Bhaiya! 1 Plate Golgappe... Less Spicy!",
        "speaker": "BABY 👶"
    },
    {
        "start": 7.09,
        "end": 12.00,
        "hi": "वाह! इतना टेस्टी! मज़ा आ गया! 😋",
        "en": "Mmm! So Tasty! Give 3 More!",
        "speaker": "BABY 👶"
    },
    {
        "start": 12.00,
        "end": 17.75,
        "hi": "अरे बाप रे! बहुत तीखा है! धुआं निकल गया! 🔥",
        "en": "Too Spicy!! Ears On Fire! Sweet Water!",
        "speaker": "BABY 👶 (SPICY SHOCK)"
    },
    {
        "start": 17.75,
        "end": 22.72,
        "hi": "पर टेस्टी बहुत था! एक प्लेट और मेरे लिए! 🤣",
        "en": "Still So Tasty! Pack 1 More For Me!",
        "speaker": "BABY 👶"
    },
    {
        "start": 22.72,
        "end": 28.00,
        "hi": "लाइक और सब्सक्राइब करो! ❤️🔔",
        "en": "Like & Subscribe For More!",
        "speaker": "SUBSCRIBE"
    }
]

# Random particles for crumbs and steam
random.seed(42)
crumb_particles = []
for i in range(25):
    ang = random.uniform(0.2, 2.9)
    spd = random.uniform(60, 220)
    crumb_particles.append({
        "vx": math.cos(ang) * spd,
        "vy": -math.sin(ang) * spd,
        "size": random.randint(3, 8),
        "rot": random.uniform(0, 360)
    })

ffmpeg_cmd = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", audio_path,
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_mp4
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
print(f"[+] Rendering {TOTAL_FRAMES} frames of full animated 3D character video...")

# Helper: Draw text with thick stroke outline
def draw_outlined_text(draw, pos, text, font, fill_color, stroke_color="black", stroke_width=4):
    x, y = pos
    draw.text((x, y), text, font=font, fill=fill_color, stroke_fill=stroke_color, stroke_width=stroke_width)

for f in range(TOTAL_FRAMES):
    t = f / float(FPS)
    amp = smoothed_env[f] if f < len(smoothed_env) else 0.0

    # Scene determination
    cur_sub = scenes_sub[-1]
    for sc in scenes_sub:
        if sc["start"] <= t < sc["end"]:
            cur_sub = sc
            break

    # 1. BASE BACKGROUND & CHARACTER
    # Character scale to fill vertical 9:16 screen (880x880 or zoomed)
    # Head breathing / bobbing
    head_bob_y = int(math.sin(t * 5.0) * 4)
    head_bob_x = int(math.sin(t * 2.5) * 3)

    # Spicy panic camera & body shake in Scene 3 (12.0s to 16.5s)
    is_spicy = (12.0 <= t <= 17.0)
    shake_x = 0
    shake_y = 0
    if is_spicy:
        shake_intensity = min(1.0, (t - 12.0) * 1.5) * max(0.0, 1.0 - (t - 16.0) / 1.0)
        shake_x = int(math.sin(t * 38.0) * 16 * shake_intensity)
        shake_y = int(math.cos(t * 32.0) * 10 * shake_intensity)

    # Canvas
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), color=(20, 14, 30, 255))

    # Base character layer - scaled up to fill upper 75% of screen
    char_w = 820
    char_h = 820
    char_scaled = raw_char.resize((char_w, char_h), Image.Resampling.LANCZOS)
    
    char_x = (WIDTH - char_w) // 2 + head_bob_x + shake_x
    char_y = 110 + head_bob_y + shake_y
    canvas.paste(char_scaled, (char_x, char_y), char_scaled)

    # DRAW CONTEXT ON TOP OF CHARACTER
    draw = ImageDraw.Draw(canvas)

    # Scale mapping from 1024x1024 to char_w/char_h
    scale_fac = char_w / 1024.0

    # 2. EYE BLINKING & ANIMATION
    # Blinking schedule: every 2.8 seconds, lasts 0.16s (4 frames)
    # Also during spicy shock, eyes squint/water
    blink_cycle = (t % 3.0)
    is_blinking = (blink_cycle < 0.16)
    blink_factor = 0.0
    if is_blinking:
        # 0.0 -> 1.0 -> 0.0
        blink_factor = math.sin((blink_cycle / 0.16) * math.pi)

    # Eye positions on canvas
    lex = char_x + int(440 * scale_fac)
    ley = char_y + int(440 * scale_fac)
    rex = char_x + int(580 * scale_fac)
    rey = char_y + int(440 * scale_fac)
    eye_r = int(28 * scale_fac)

    if blink_factor > 0.1:
        # Draw realistic skin-tone eyelids closing over eyes
        lid_h = int(eye_r * 2 * blink_factor)
        lid_color = (215, 155, 125, 255)
        crease_color = (160, 100, 75, 230)
        
        # Left Eyelid
        draw.ellipse([lex - eye_r - 2, ley - eye_r, lex + eye_r + 2, ley - eye_r + lid_h], fill=lid_color)
        draw.arc([lex - eye_r, ley - eye_r, lex + eye_r, ley - eye_r + lid_h], start=0, end=180, fill=crease_color, width=2)
        # Right Eyelid
        draw.ellipse([rex - eye_r - 2, rey - eye_r, rex + eye_r + 2, rey - eye_r + lid_h], fill=lid_color)
        draw.arc([rex - eye_r, rey - eye_r, rex + eye_r, rey - eye_r + lid_h], start=0, end=180, fill=crease_color, width=2)
    else:
        # Subtle sparkling eye highlight shimmer
        shimmer = int(math.sin(t * 8.0) * 2)
        draw.ellipse([lex - 8 + shimmer, ley - 10, lex - 4 + shimmer, ley - 6], fill=(255, 255, 255, 230))
        draw.ellipse([rex - 8 + shimmer, rey - 10, rex - 4 + shimmer, rey - 6], fill=(255, 255, 255, 230))

    # 3. LIP-SYNC & MOUTH ANIMATION (AUDIO DRIVEN)
    mx = char_x + int(512 * scale_fac)
    my = char_y + int(585 * scale_fac)
    
    # Chewing motion in Scene 2 (7.2s to 9.5s)
    is_chewing = (7.2 <= t <= 9.8)
    chew_offset = int(abs(math.sin(t * 14.0)) * 10) if is_chewing else 0

    # Mouth opening depends on audio volume (or chewing)
    mouth_open = int(amp * 26 * scale_fac) + (chew_offset if is_chewing else 0)

    if mouth_open > 3:
        # Draw realistic open mouth cavity
        mw = int(46 * scale_fac + mouth_open * 0.4)
        mh = int(mouth_open)
        
        # Dark red mouth interior
        draw.ellipse([mx - mw//2, my - mh//3, mx + mw//2, my + mh], fill=(130, 24, 34, 255))
        
        # Cute little baby upper teeth
        teeth_w = int(14 * scale_fac)
        draw.rounded_rectangle([mx - teeth_w, my - mh//3, mx + teeth_w, my - mh//3 + int(8 * scale_fac)], radius=3, fill=(250, 250, 250, 255))
        
        # Pink baby tongue
        tongue_w = int(22 * scale_fac)
        draw.ellipse([mx - tongue_w//2, my + mh - int(10 * scale_fac), mx + tongue_w//2, my + mh + int(2 * scale_fac)], fill=(235, 115, 135, 255))
        
        # Lip crease
        draw.arc([mx - mw//2, my - mh//3, mx + mw//2, my + mh], start=0, end=180, fill=(160, 85, 70, 220), width=2)

    # 4. HAND & GOLGAPPA MOTION (SCENE 2 BITE & CRUNCH)
    # Golgappa position
    gx = char_x + int(400 * scale_fac)
    gy = char_y + int(730 * scale_fac)
    gr = int(60 * scale_fac)

    # At t=5.0s to 7.1s, hand lifts up to mouth
    if 5.0 <= t < 7.1:
        lift_prog = (t - 5.0) / 2.1
        lift_y = int(math.sin(lift_prog * math.pi / 2.0) * 85 * scale_fac)
        gy -= lift_y

    # At t >= 7.1s, golgappa has a crispy BITE taken out of it!
    has_bitten = (t >= 7.1)
    if has_bitten:
        # Carve bite mark (crescent cutout) on top of golgappa
        bite_x = gx + int(25 * scale_fac)
        bite_y = gy - int(20 * scale_fac)
        bite_r = int(28 * scale_fac)
        # Inner tasty filling color (dark tangy tamarind pani puri)
        draw.ellipse([bite_x - bite_r, bite_y - bite_r, bite_x + bite_r, bite_y + bite_r], fill=(90, 45, 25, 255))

    # Crumb particles flying on bite (7.1s to 8.2s)
    if 7.1 <= t <= 8.3:
        crunch_t = (t - 7.1)
        for p_idx, p in enumerate(crumb_particles):
            px = gx + p["vx"] * crunch_t
            py = gy + p["vy"] * crunch_t + 0.5 * 450 * (crunch_t ** 2) # gravity
            p_alpha = max(0, int(255 * (1.0 - crunch_t / 1.2)))
            draw.ellipse([px - p["size"], py - p["size"], px + p["size"], py + p["size"]], fill=(225, 160, 50, p_alpha))

    # 5. SPICY SHOCK SPECIAL FX (SCENE 3: 12.0s to 17.0s)
    if is_spicy:
        # A. Fiery Red Glowing Cheeks
        flush_alpha = int(140 + math.sin(t * 12.0) * 45)
        # Left cheek
        lcx = char_x + int(370 * scale_fac)
        lcy = char_y + int(530 * scale_fac)
        draw.ellipse([lcx - 45, lcy - 35, lcx + 45, lcy + 35], fill=(235, 45, 45, flush_alpha))
        # Right cheek
        rcx = char_x + int(630 * scale_fac)
        rcy = char_y + int(530 * scale_fac)
        draw.ellipse([rcx - 45, rcy - 35, rcx + 45, rcy + 35], fill=(235, 45, 45, flush_alpha))

        # B. Animated Teardrops from Eyes
        tear_drop_1 = (t * 180) % 70
        draw.ellipse([lex + 15, ley + 10 + tear_drop_1, lex + 23, ley + 22 + tear_drop_1], fill=(56, 189, 248, 240))
        tear_drop_2 = ((t + 0.3) * 180) % 70
        draw.ellipse([rex - 23, rey + 10 + tear_drop_2, rex - 15, rey + 22 + tear_drop_2], fill=(56, 189, 248, 240))

        # C. Animated Steam Puffs Rising from Ears
        steam_offset_1 = int((t * 90) % 80)
        draw.ellipse([char_x + 80, char_y + 360 - steam_offset_1, char_x + 130 + steam_offset_1//2, char_y + 400 - steam_offset_1], fill=(255, 255, 255, 210))
        steam_offset_2 = int(((t + 0.4) * 90) % 80)
        draw.ellipse([char_x + char_w - 140 - steam_offset_2//2, char_y + 360 - steam_offset_2, char_x + char_w - 90, char_y + 400 - steam_offset_2], fill=(255, 255, 255, 210))

    # 6. SCENE 4 & 5 FLOATING HEARTS & SPARKLES (17.5s - 28.0s)
    if t >= 17.5:
        # Floating heart bubbles
        for h_idx in range(4):
            ht = (t * 0.8 + h_idx * 1.5) % 5.0
            hx = 120 + h_idx * 160 + int(math.sin(ht * 3.0) * 20)
            hy = HEIGHT - 280 - int(ht * 160)
            h_alpha = max(0, int(220 * (1.0 - ht / 5.0)))
            draw.text((hx, hy), "❤️", font=font_title, fill=(236, 72, 153, h_alpha))

    # 7. CINEMATIC OVERLAYS & AUTO-CAPTIONS (7M VIEW STYLE)
    # Top Headline Bar
    draw.rounded_rectangle([30, 40, WIDTH - 30, 110], radius=18, fill=(24, 16, 36, 230), outline="#F59E0B", width=3)
    draw.text((55, 52), "🤣 Golgappe Ka Lalach 😂", font=font_title, fill="#FBBF24")
    draw.text((WIDTH - 180, 58), "3D COMEDY", font=font_en, fill="#38BDF8")

    # Animated Punchline Subtitles on Lower Third
    sub_y = 920
    # Semi-transparent dark background for punchy subtitle contrast
    draw.rounded_rectangle([30, sub_y, WIDTH - 30, sub_y + 190], radius=24, fill=(18, 12, 28, 240), outline="#FBBF24", width=3)

    # Speaker tag
    draw.text((55, sub_y + 16), cur_sub["speaker"], font=font_en, fill="#EC4899")

    # Kinetic Pop Scale on Hindi text
    pop_scale = 1.0 + math.sin(min(1.0, (t - cur_sub["start"]) * 6.0) * math.pi) * 0.05
    hi_text = cur_sub["hi"]
    draw_outlined_text(draw, (55, sub_y + 55), hi_text, font_hi, "#FBBF24", "black", stroke_width=5)

    # English subtitle underneath
    en_text = cur_sub["en"]
    draw_outlined_text(draw, (55, sub_y + 125), en_text, font_en, "#38BDF8", "black", stroke_width=3)

    # Bottom Subscribe / Progress Bar
    draw.rounded_rectangle([30, 1140, WIDTH - 30, 1225], radius=18, fill=(220, 38, 38, 240), outline="#FBBF24", width=3)
    draw.text((65, 1160), "▶ SUBSCRIBE FOR DAILY FUNNY SHORTS!", font=font_btn, fill="white")

    # Bottom Video Progress Bar
    prog_pct = min(1.0, t / TOTAL_DURATION)
    draw.rectangle([0, HEIGHT - 10, int(WIDTH * prog_pct), HEIGHT], fill="#F59E0B")

    # Pipe frame to FFmpeg
    rgb_frame = canvas.convert("RGB")
    proc.stdin.write(rgb_frame.tobytes())

proc.stdin.close()
proc.wait()

print("\n" + "="*60)
print(f"🎉 FULL ANIMATED 3D CHARACTER VIDEO RENDERED!")
print(f"Output File: {output_mp4}")
print(f"Duration: {TOTAL_DURATION:.2f}s ({TOTAL_FRAMES} frames)")
print("="*60)
