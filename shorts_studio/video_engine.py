import os
import sys
import math
import wave
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
import win32com.client
import pythoncom

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

def draw_3d_sphere(draw, cx, cy, radius, base_col=(20, 25, 40), highlight_col=(180, 215, 250)):
    # Realistic 3D Phong shaded sphere with specular highlight
    for r in range(radius, 0, -2):
        t = (radius - r) / float(radius)
        ox = int((radius - r) * -0.35)
        oy = int((radius - r) * -0.35)
        cr = int(base_col[0] + t * (highlight_col[0] - base_col[0]))
        cg = int(base_col[1] + t * (highlight_col[1] - base_col[1]))
        cb = int(base_col[2] + t * (highlight_col[2] - base_col[2]))
        draw.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=(cr, cg, cb, 255))

def draw_3d_limb(draw, x1, y1, x2, y2, thickness=16, base_col=(20, 25, 38), highlight_col=(140, 175, 215), glow_col=None):
    draw.line([x1, y1, x2, y2], fill=base_col, width=thickness)
    draw.line([x1 - 2, y1 - 2, x2 - 2, y2 - 2], fill=highlight_col, width=max(4, thickness // 3))
    if glow_col:
        draw.ellipse([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=glow_col)
        draw.ellipse([x2 - 7, y2 - 7, x2 + 7, y2 + 7], fill=glow_col)

def draw_3d_stickman(draw, cx, cy, action="idle", frame_t=0.0):
    head_r = 44
    head_cy = cy - 130
    
    # 1. Torso (3D shaded core)
    draw_3d_limb(draw, cx, cy - 75, cx, cy + 35, thickness=22, base_col=(18, 24, 38), highlight_col=(140, 175, 215))

    # 2. Poses
    if action == "confused":
        # Left hand on hip, right hand scratching head
        draw_3d_limb(draw, cx - 10, cy - 50, cx - 65, cy - 20, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx - 65, cy - 20, cx - 55, cy + 20, thickness=14, glow_col="#A855F7")
        draw_3d_limb(draw, cx + 10, cy - 50, cx + 75, cy - 70, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx + 75, cy - 70, cx + 45, cy - 135, thickness=14, glow_col="#EF4444")
        # Floating 3D Glowing Question Mark
        q_pulse = math.sin(frame_t * 6.0) * 8
        draw.text((cx + 65, cy - 190 + q_pulse), "?", font=ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 60), fill="#EF4444")
    elif action == "triumph":
        # Both arms up in V shape
        draw_3d_limb(draw, cx - 10, cy - 50, cx - 75, cy - 100, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx - 75, cy - 100, cx - 110, cy - 160, thickness=14, glow_col="#10B981")
        draw_3d_limb(draw, cx + 10, cy - 50, cx + 75, cy - 100, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx + 75, cy - 100, cx + 110, cy - 160, thickness=14, glow_col="#10B981")
        # Energy spark above
        draw.ellipse([cx - 8, cy - 190, cx + 8, cy - 174], fill="#F59E0B")
    elif action == "snap":
        # Snap with electric aura
        draw_3d_limb(draw, cx - 10, cy - 50, cx - 60, cy - 10, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx + 10, cy - 50, cx + 70, cy - 75, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx + 70, cy - 75, cx + 95, cy - 115, thickness=14, glow_col="#22D3EE")
        draw.ellipse([cx + 90, cy - 125, cx + 110, cy - 105], fill="#22D3EE")
        draw.line([cx + 80, cy - 115, cx + 120, cy - 115], fill="#38BDF8", width=3)
    elif action == "shrug":
        # Both arms raised in shrug
        draw_3d_limb(draw, cx - 10, cy - 50, cx - 65, cy - 70, thickness=16, glow_col="#F59E0B")
        draw_3d_limb(draw, cx - 65, cy - 70, cx - 95, cy - 100, thickness=14, glow_col="#F59E0B")
        draw_3d_limb(draw, cx + 10, cy - 50, cx + 65, cy - 70, thickness=16, glow_col="#F59E0B")
        draw_3d_limb(draw, cx + 65, cy - 70, cx + 95, cy - 100, thickness=14, glow_col="#F59E0B")
    elif action == "point_right":
        # Right arm pointing forward
        draw_3d_limb(draw, cx - 10, cy - 50, cx - 60, cy - 20, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx - 60, cy - 20, cx - 90, cy - 60, thickness=14, glow_col="#A855F7")
        draw_3d_limb(draw, cx + 10, cy - 50, cx + 80, cy - 30, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx + 80, cy - 30, cx + 175, cy - 30, thickness=14, glow_col="#22D3EE")
        # Cyan beam
        draw.ellipse([cx + 170, cy - 36, cx + 188, cy - 18], fill="#22D3EE")
    else:  # idle
        sway = math.sin(frame_t * 3.5) * 8
        draw_3d_limb(draw, cx - 10, cy - 50, cx - 45, cy + 15 + sway, thickness=16, glow_col="#22D3EE")
        draw_3d_limb(draw, cx + 10, cy - 50, cx + 45, cy + 15 - sway, thickness=16, glow_col="#22D3EE")

    # Legs (3D Shaded)
    draw_3d_limb(draw, cx - 10, cy + 35, cx - 45, cy + 140, thickness=18, glow_col="#22D3EE")
    draw_3d_limb(draw, cx + 10, cy + 35, cx + 45, cy + 140, thickness=18, glow_col="#22D3EE")

    # 3. 3D Head (Rendered in front of limbs)
    draw_3d_sphere(draw, cx, head_cy, head_r, base_col=(18, 24, 38), highlight_col=(180, 215, 250))

    # 4. Glowing 3D Cyber Visor
    vx1, vy1, vx2, vy2 = cx - 36, head_cy - 10, cx + 36, head_cy + 14
    draw.rounded_rectangle([vx1, vy1, vx2, vy2], radius=10, fill=(34, 211, 238, 255), outline=(168, 85, 247, 255), width=2)
    draw.line([vx1 + 8, vy1 + 4, vx1 + 35, vy1 + 4], fill="white", width=3)

    # 5. 3D Cyber Headphones
    draw.arc([cx - 50, head_cy - 48, cx + 50, head_cy + 30], 190, 350, fill=(45, 55, 80), width=6)
    draw.rounded_rectangle([cx - 52, head_cy - 12, cx - 40, head_cy + 18], radius=6, fill=(168, 85, 247, 255), outline="#22D3EE", width=2)
    draw.rounded_rectangle([cx + 40, head_cy - 12, cx + 52, head_cy + 18], radius=6, fill=(168, 85, 247, 255), outline="#22D3EE", width=2)


def generate_video_from_scenes(scenes, output_mp4, temp_dir, logo_path=None, progress_callback=None):
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. Synthesize Audio with Windows SAPI
    pythoncom.CoInitialize()
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Rate = 0
        for idx, sc in enumerate(scenes):
            wav_path = os.path.join(temp_dir, f"scene_{idx}.wav")
            stream = win32com.client.Dispatch("SAPI.SpFileStream")
            stream.Open(wav_path, 3, False)
            speaker.AudioOutputStream = stream
            speaker.Speak(sc["script"])
            stream.Close()
    finally:
        pythoncom.CoUninitialize()

    WIDTH = 720
    HEIGHT = 1280
    FPS = 24

    audio_data_list = []
    scene_schedule = []
    current_start = 0.0

    for idx, sc in enumerate(scenes):
        wav_path = os.path.join(temp_dir, f"scene_{idx}.wav")
        with wave.open(wav_path, 'rb') as w:
            nframes = w.getnframes()
            rate = w.getframerate()
            nchannels = w.getnchannels()
            sampwidth = w.getsampwidth()
            data = w.readframes(nframes)
            duration = nframes / float(rate)
            audio_data_list.append((data, nchannels, sampwidth, rate))
            scene_schedule.append({
                "idx": idx,
                "tag": sc.get("tag", "SHORTS · TECH").upper(),
                "script": sc["script"],
                "headline": sc.get("headline", ""),
                "subtext": sc.get("subtext", ""),
                "action": sc.get("action", "idle"),
                "color": sc.get("color", "#22D3EE"),
                "start": current_start,
                "end": current_start + duration,
                "duration": duration
            })
            current_start += duration

    total_duration = current_start
    master_audio_wav = os.path.join(temp_dir, "master_audio.wav")
    with wave.open(master_audio_wav, 'wb') as out_w:
        out_w.setnchannels(audio_data_list[0][1])
        out_w.setsampwidth(audio_data_list[0][2])
        out_w.setframerate(audio_data_list[0][3])
        for data, _, _, _ in audio_data_list:
            out_w.writeframes(data)

    total_frames = int(math.ceil(total_duration * FPS))

    # Logo watermark
    logo_img = None
    logo_mask = None
    if logo_path and os.path.exists(logo_path):
        raw_logo = Image.open(logo_path).convert("RGBA")
        logo_size = 64
        logo_img = raw_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        logo_mask = Image.new("L", (logo_size, logo_size), 0)
        m_draw = ImageDraw.Draw(logo_mask)
        m_draw.ellipse([0, 0, logo_size, logo_size], fill=255)

    # Fonts
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 36)
    font_subtitle = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
    font_big = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 48)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 22)
    font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 17)

    ffmpeg_cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", master_audio_wav,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    for frame_idx in range(total_frames):
        t = frame_idx / float(FPS)
        
        cur_scene = scene_schedule[-1]
        for sc in scene_schedule:
            if sc["start"] <= t < sc["end"]:
                cur_scene = sc
                break
                
        scene_rel_t = t - cur_scene["start"]
        accent = cur_scene["color"]
        
        img = Image.new("RGBA", (WIDTH, HEIGHT), color=(10, 12, 22, 255))
        draw = ImageDraw.Draw(img)
        
        # 1. Background Cyber Matrix Grid & Glows
        for x in range(0, WIDTH, 60):
            draw.line([x, 0, x, HEIGHT], fill=(18, 24, 40, 255), width=1)
        for y in range(0, HEIGHT, 60):
            draw.line([0, y, WIDTH, y], fill=(18, 24, 40, 255), width=1)

        # Ambient Glow behind character
        draw.ellipse([WIDTH//2 - 250, 500, WIDTH//2 + 250, 1050], fill=(22, 32, 65, 100))

        # 2. Top HUD Tag & Timecode
        tag_text = cur_scene["tag"]
        draw.rounded_rectangle([30, 40, 390, 82], radius=15, fill=(24, 30, 50, 240), outline=(65, 75, 110, 255), width=2)
        draw.text((48, 50), tag_text, font=font_tag, fill=accent)
        
        time_str = f"{int(t//60)}:{int(t%60):02d} / 0:{int(total_duration):02d}"
        draw.text((WIDTH - 245, 52), time_str, font=font_tag, fill=(150, 155, 175, 255))
        
        # 3. Logo Watermark
        if logo_img and logo_mask:
            lx = WIDTH - 90
            ly = 28
            img.paste(logo_img, (lx, ly), logo_mask)
            draw.ellipse([lx - 2, ly - 2, lx + 66, ly + 66], outline="#22D3EE", width=3)
            
        # 4. Floating 3D Holographic Card in Foreground
        headline = cur_scene["headline"]
        subtext = cur_scene["subtext"]
        
        card_pulse = math.sin(t * 4.5) * 4
        c_x1, c_y1 = int(70 - card_pulse), int(190 - card_pulse)
        c_x2, c_y2 = int(650 + card_pulse), int(480 + card_pulse)
        
        # Hologram Glass Body
        draw.rounded_rectangle([c_x1, c_y1, c_x2, c_y2], radius=24, fill=(16, 22, 38, 245), outline=accent, width=3)
        
        # Tech Lines inside Hologram
        for gx in range(c_x1 + 40, c_x2, 80):
            draw.line([gx, c_y1 + 10, gx, c_y2 - 10], fill=(25, 35, 60, 80), width=1)
            
        if headline:
            draw.text((c_x1 + 35, c_y1 + 25), headline, font=font_big, fill="white")
            
        if subtext:
            lines = subtext.split("\n")
            for l_idx, line in enumerate(lines):
                col = accent if l_idx == 0 else (210, 225, 245, 255)
                draw.text((c_x1 + 35, c_y1 + 95 + l_idx * 48), line, font=font_title, fill=col)
        else:
            draw.text((c_x1 + 35, c_y1 + 100), cur_scene["script"][:45] + "...", font=font_subtitle, fill="white")

        # 5. Render 3D Shaded Character
        draw_3d_stickman(draw, 360, 800, action=cur_scene["action"], frame_t=t)

        # 6. Bottom Kinetic Subtitle Ribbon
        draw.rounded_rectangle([30, 1120, WIDTH - 30, 1220], radius=18, fill=(15, 20, 35, 255), outline=(34, 211, 238, 200), width=2)
        sub_text = cur_scene["script"]
        if len(sub_text) > 40:
            words = sub_text.split()
            half = len(words) // 2
            line1 = " ".join(words[:half])
            line2 = " ".join(words[half:])
            draw.text((50, 1132), line1, font=font_small, fill="white")
            draw.text((50, 1165), line2, font=font_small, fill=accent)
        else:
            draw.text((50, 1150), sub_text, font=font_small, fill="white")
            
        # 7. Bottom Continuous Progress Bar
        prog_pct = min(1.0, t / total_duration)
        draw.rectangle([0, HEIGHT - 10, int(WIDTH * prog_pct), HEIGHT], fill=accent)
        
        rgb_img = img.convert("RGB")
        proc.stdin.write(rgb_img.tobytes())
        
        if progress_callback and frame_idx % 48 == 0:
            progress_callback(int((frame_idx / total_frames) * 100))

    proc.stdin.close()
    proc.wait()
    if progress_callback:
        progress_callback(100)
        
    return {
        "output_mp4": output_mp4,
        "total_duration": total_duration,
        "total_frames": total_frames,
        "scenes_count": len(scenes)
    }
