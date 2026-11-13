import os, sys, math, subprocess, json, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

# --- FONTS ---
def get_font(name, size):
    try:
        path = os.path.join("C:/Windows/Fonts", name)
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_brand = get_font("arialbd.ttf", 36)
font_brand_sub = get_font("arial.ttf", 22)
font_category = get_font("arialbd.ttf", 30)
font_tool_badge = get_font("arialbd.ttf", 50)
font_card_sub = get_font("arialbd.ttf", 28)
font_hud_title = get_font("arialbd.ttf", 26)
font_hud_code = get_font("consola.ttf", 22)
font_hud_code_bold = get_font("consolab.ttf", 24)
font_sub_bold = get_font("arialbd.ttf", 44)
font_giant_btn = get_font("arialbd.ttf", 44)

# --- LOGO HELPER ---
def make_circular_logo(img, size, border_color=(0, 220, 255), border_width=4):
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([0, 0, size - 1, size - 1], fill=255)
    
    circ = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circ.paste(img, (0, 0), mask=mask)
    
    draw_circ = ImageDraw.Draw(circ)
    draw_circ.ellipse([border_width//2, border_width//2, size - 1 - border_width//2, size - 1 - border_width//2], outline=border_color, width=border_width)
    return circ


def render_vertical_frame(t, total_d, bg_workstation, bg_mascot, logo_header):
    w, h = 1080, 1920

    # 1. Base Image Selection & Cinematic Camera Movement
    if t < 40.98:
        # Camera zoom & pan effect on workstation
        zoom = 1.0 + (t % 10.0) * 0.015
        bw = int(w * zoom)
        bh = int(h * zoom)
        scaled_bg = bg_workstation.resize((bw, bh), Image.Resampling.BILINEAR)
        
        # Center crop with slight camera drift
        cx = (bw - w) // 2 + int(math.sin(t * 0.5) * 15)
        cy = (bh - h) // 2 + int(math.cos(t * 0.4) * 10)
        
        # Screen shake if in Scene 2 (Crash)
        if 9.52 <= t < 21.31:
            shake_x = int(math.sin(t * 50.0) * 8)
            shake_y = int(math.cos(t * 45.0) * 6)
            cx = max(0, min(bw - w, cx + shake_x))
            cy = max(0, min(bh - h, cy + shake_y))
            
        im = scaled_bg.crop((cx, cy, cx + w, cy + h)).copy()
        
        # Red Alert Lighting Overlay for Scene 2
        if 9.52 <= t < 21.31:
            pulse = (math.sin(t * 8.0) + 1.0) * 0.5
            red_overlay = Image.new('RGB', (w, h), (int(140 + 80*pulse), 10, 20))
            im = Image.blend(im, red_overlay, 0.32 + pulse * 0.15)
        elif 21.31 <= t < 31.56:
            # Darkened for code focus
            dark_overlay = Image.new('RGB', (w, h), (10, 15, 25))
            im = Image.blend(im, dark_overlay, 0.45)
    else:
        # Scene 5: Victory / Mascot Screen
        zoom = 1.0 + ((t - 40.98) % 15.0) * 0.012
        bw = int(w * zoom)
        bh = int(h * zoom)
        scaled_bg = bg_mascot.resize((bw, bh), Image.Resampling.BILINEAR)
        cx = (bw - w) // 2
        cy = (bh - h) // 2
        im = scaled_bg.crop((cx, cy, cx + w, cy + h)).copy()
        
        # Warm ambient blend
        gold_overlay = Image.new('RGB', (w, h), (25, 20, 12))
        im = Image.blend(im, gold_overlay, 0.20)

    draw = ImageDraw.Draw(im)

    # 2. Top Progress Bar
    prog_pct = min(1.0, max(0.0, t / total_d))
    draw.rectangle([40, 45, 1040, 55], fill=(25, 35, 55))
    draw.rounded_rectangle([40, 45, int(40 + 1000 * prog_pct), 55], radius=4, fill=(0, 240, 255))

    # 3. Header Bar
    im.paste(logo_header, (50, 75), mask=logo_header)
    draw.text((150, 85), "TECHSTACK AI", font=font_brand, fill=(255, 255, 255))
    draw.text((150, 128), "Real Engineering Disasters & Hotfixes", font=font_brand_sub, fill=(160, 210, 245))

    card_y = 200

    # 4. Five Cinematic Scenes
    # Scene 1: The Innocent Friday Commit (0.0 - 9.52s)
    if t < 9.52:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(0, 180, 255, 35), outline=(0, 200, 255), width=2)
        draw.text((775, 96), "💀 5:00 PM FRIDAY", font=font_category, fill=(0, 220, 255))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(12, 20, 35, 230), outline=(0, 200, 255), width=3)
        draw.text((80, card_y + 20), "THE INNOCENT COMMIT", font=font_tool_badge, fill=(0, 240, 255))
        draw.text((80, card_y + 85), "Pushing One Quick Fix Straight to Production", font=font_card_sub, fill=(200, 235, 255))

        # Floating Git HUD
        draw.rounded_rectangle([80, 1120, 1000, 1320], radius=16, fill=(10, 16, 26, 235), outline=(0, 220, 255), width=2)
        draw.text((110, 1140), "💻 TERMINAL: main branch", font=font_hud_title, fill=(0, 240, 255))
        draw.line([(100, 1175), (980, 1175)], fill=(0, 140, 180), width=1)
        draw.text((110, 1195), "$ git add . && git commit -m 'quick Friday fix'", font=font_hud_code, fill=(220, 240, 255))
        draw.text((110, 1235), "$ git push origin main", font=font_hud_code_bold, fill=(255, 220, 50))
        draw.text((110, 1275), "> Deploying to production cluster (us-east-1)... [OK]", font=font_hud_code, fill=(0, 255, 160))

        if t < 5.0:
            sub_text = "It is Friday at 5 PM. Your sprint is done, the weekend is calling..."
            hl_word = "Friday at 5 PM."
        else:
            sub_text = "And you decide to push one tiny, innocent commit straight to production."
            hl_word = "straight to production."

    # Scene 2: The Red Alert Crash (9.52 - 21.31s)
    elif t < 21.31:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(255, 50, 50, 45), outline=(255, 60, 60), width=2)
        draw.text((775, 96), "🚨 PAGERDUTY", font=font_category, fill=(255, 80, 80))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(35, 12, 18, 235), outline=(255, 60, 60), width=3)
        draw.text((80, card_y + 20), "500 SERVER ERROR", font=font_tool_badge, fill=(255, 80, 80))
        draw.text((80, card_y + 85), "CPU 100% • Production Database Locked Up", font=font_card_sub, fill=(255, 210, 210))

        # Panic Alert HUD
        draw.rounded_rectangle([80, 1120, 1000, 1330], radius=16, fill=(30, 10, 14, 240), outline=(255, 60, 60), width=3)
        draw.text((110, 1140), "🚨 PAGERDUTY ALERT: SEV-1 CRITICAL INCIDENT", font=font_hud_title, fill=(255, 80, 80))
        draw.line([(100, 1175), (980, 1175)], fill=(180, 40, 40), width=1)
        draw.text((110, 1195), "• API Error Rate: 99.4% [500 INTERNAL SERVER ERROR]", font=font_hud_code_bold, fill=(255, 200, 200))
        draw.text((110, 1235), "• Database: 1,480 active connections [DEADLOCK DETECTED]", font=font_hud_code_bold, fill=(255, 220, 50))
        draw.text((110, 1275), "• Latency: >30,000ms (All user checkouts failing)", font=font_hud_code_bold, fill=(255, 80, 80))

        if t < 15.0:
            sub_text = "Two minutes later... your phone explodes with PagerDuty alerts!"
            hl_word = "PagerDuty alerts!"
        else:
            sub_text = "500 Internal Server Error. CPU at 100%. The database is completely locked!"
            hl_word = "completely locked!"

    # Scene 3: The Desperate Debugging (21.31 - 31.56s)
    elif t < 31.56:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(255, 160, 0, 35), outline=(255, 180, 0), width=2)
        draw.text((775, 96), "🔍 TRACING LOGS", font=font_category, fill=(255, 180, 0))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 20, 12, 235), outline=(255, 180, 0), width=3)
        draw.text((80, card_y + 20), "UNINDEXED SQL QUERY", font=font_tool_badge, fill=(255, 200, 50))
        draw.text((80, card_y + 85), "Tracing Slow Queries Across 10 Million Rows", font=font_card_sub, fill=(255, 235, 200))

        # Big Terminal HUD
        draw.rounded_rectangle([80, 1100, 1000, 1330], radius=16, fill=(15, 15, 22, 240), outline=(255, 180, 0), width=2)
        draw.text((110, 1120), "💻 $ kubectl logs deployment/backend-api --tail=50", font=font_hud_title, fill=(255, 180, 0))
        draw.line([(100, 1155), (980, 1155)], fill=(160, 110, 0), width=1)
        draw.text((110, 1175), "QUERY: SELECT * FROM orders WHERE status = 'pending'", font=font_hud_code, fill=(255, 220, 220))
        draw.text((110, 1215), "EXPLAIN: Seq Scan on orders (rows=10,485,760)", font=font_hud_code_bold, fill=(255, 80, 80))
        draw.text((110, 1255), "⚠️ NO COMPOSITE INDEX! LOCKING TABLE FOR 45 SECONDS!", font=font_hud_code_bold, fill=(255, 220, 50))
        draw.text((110, 1290), "ROOT CAUSE: Missing index on column 'status'", font=font_hud_code, fill=(200, 240, 255))

        if t < 26.5:
            sub_text = "You panic and open the terminal. You run kubectl logs and trace the memory leak."
            hl_word = "open the terminal."
        else:
            sub_text = "And then you see it: an unindexed nested query locking ten million rows!"
            hl_word = "ten million rows!"

    # Scene 4: The Hotfix & Rolling Restart (31.56 - 40.98s)
    elif t < 40.98:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(0, 240, 180, 35), outline=(0, 240, 180), width=2)
        draw.text((775, 96), "🛠️ HOTFIX DEPLOY", font=font_category, fill=(0, 240, 180))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(12, 28, 25, 235), outline=(0, 240, 180), width=3)
        draw.text((80, card_y + 20), "APPLYING INDEX HOTFIX", font=font_tool_badge, fill=(0, 240, 180))
        draw.text((80, card_y + 85), "Killing Zombie Locks & Rolling Restart", font=font_card_sub, fill=(200, 255, 235))

        # Hotfix Terminal HUD
        draw.rounded_rectangle([80, 1120, 1000, 1330], radius=16, fill=(10, 22, 20, 240), outline=(0, 255, 160), width=2)
        draw.text((110, 1140), "⚡ EMERGENCY MIGRATION SCRIPT", font=font_hud_title, fill=(0, 255, 160))
        draw.line([(100, 1175), (980, 1175)], fill=(0, 160, 100), width=1)
        draw.text((110, 1195), "CREATE INDEX CONCURRENTLY idx_orders_status ON orders(status);", font=font_hud_code_bold, fill=(220, 255, 240))
        draw.text((110, 1235), "$ kubectl rollout restart deployment/backend-api", font=font_hud_code, fill=(220, 255, 240))
        draw.text((110, 1275), "Pod 1/3 [READY] • Pod 2/3 [READY] • Pod 3/3 [200 OK]", font=font_hud_code_bold, fill=(0, 255, 140))

        if t < 36.0:
            sub_text = "You quickly write the hotfix migration and add the composite index."
            hl_word = "hotfix migration"
        else:
            sub_text = "Kill the zombie query locks, and execute the emergency rolling restart."
            hl_word = "emergency rolling restart."

    # Scene 5: Senior Dev Rule & CTA (40.98 - 55.60s)
    else:
        draw.rounded_rectangle([750, 85, 1030, 135], radius=12, fill=(255, 200, 0, 35), outline=(255, 215, 0), width=2)
        draw.text((775, 96), "💡 SENIOR RULE", font=font_category, fill=(255, 215, 0))

        draw.rounded_rectangle([50, card_y, 1030, card_y + 140], radius=20, fill=(28, 24, 14, 235), outline=(255, 215, 0), width=3)
        draw.text((80, card_y + 20), "READ-ONLY FRIDAYS", font=font_tool_badge, fill=(255, 225, 50))
        draw.text((80, card_y + 85), "Never Push to Production Before the Weekend", font=font_card_sub, fill=(255, 240, 200))

        # Floating Subscribe Box
        sub_box_y = 1100
        draw.rounded_rectangle([140, sub_box_y, 940, sub_box_y + 240], radius=24, fill=(16, 22, 34, 240), outline=(255, 215, 0), width=4)
        
        btn_pulse = (math.sin(t * 8.0) + 1.0) * 4
        draw.rounded_rectangle([int(200 - btn_pulse), int(sub_box_y + 35 - btn_pulse), int(880 + btn_pulse), int(sub_box_y + 125 + btn_pulse)], radius=18, fill=(255, 0, 0), outline=(255, 255, 255), width=3)
        draw.polygon([(260, sub_box_y + 55), (260, sub_box_y + 105), (305, sub_box_y + 80)], fill=(255, 255, 255))
        draw.text((330, sub_box_y + 53), "SUBSCRIBE TO TECHSTACK AI", font=font_giant_btn, fill=(255, 255, 255))
        
        draw.text((210, sub_box_y + 150), "🔔 Real Developer Disasters & System Architecture", font=font_category, fill=(255, 225, 120))
        draw.text((310, sub_box_y + 190), "@TechStacAI on YouTube & Shorts", font=font_brand_sub, fill=(180, 215, 245))

        if t < 48.0:
            sub_text = "System restored! The golden rule of software engineering: Read-Only Fridays exist for a reason."
            hl_word = "Read-Only Fridays"
        else:
            sub_text = "Subscribe to TechStack AI for real developer sanity!"
            hl_word = "Subscribe"

    # Subtitles container at bottom
    wrapped = textwrap.wrap(sub_text, width=38)
    sub_h = 40 + len(wrapped) * 54
    sub_y = h - sub_h - 70
    draw.rounded_rectangle([40, sub_y, 1040, sub_y + sub_h], radius=24, fill=(10, 16, 26, 245), outline=(0, 240, 255), width=4)
    
    for i, line in enumerate(wrapped):
        words = line.split(" ")
        curr_x = 70
        for word in words:
            w_col = (255, 235, 50) if hl_word.lower() in word.lower() else (255, 255, 255)
            draw.text((curr_x, sub_y + 22 + i * 54), word + " ", font=font_sub_bold, fill=w_col)
            curr_x += int(draw.textlength(word + " ", font=font_sub_bold))

    return im


def main():
    proj_dir = r"D:\Antigravity\Pro\agentic-code\projects\friday_deploy_disaster_short"
    audio_path = os.path.join(proj_dir, "audio", "short_master_audio.wav")
    output_video = os.path.join(proj_dir, "FRIDAY_DEPLOY_DISASTER_9x16.mp4")
    
    bg_workstation_path = os.path.join(proj_dir, "scene1_typing_pc.jpg")
    bg_mascot_path = r"D:\Antigravity\Pro\pixar_tech_developer_mascot.jpg"
    logo_path = r"D:\Antigravity\Pro\channel_profile_pic.png"

    bg_workstation = Image.open(bg_workstation_path).convert("RGB")
    bg_mascot = Image.open(bg_mascot_path).convert("RGB")
    logo_raw = Image.open(logo_path).convert("RGBA")
    logo_header = make_circular_logo(logo_raw, 84, border_color=(0, 240, 255), border_width=3)

    total_duration = 55.60
    fps = 24
    total_frames = int(round(total_duration * fps))

    print(f"--- RENDERING 3D DEVELOPER 'FRIDAY DEPLOY DISASTER' SHORT (1080x1920) ---", flush=True)
    print(f"Total Duration: {total_duration:.2f}s | FPS: {fps} | Frames: {total_frames}", flush=True)
    print(f"Workstation BG: {bg_workstation_path}", flush=True)
    print(f"Mascot BG: {bg_mascot_path}", flush=True)
    print(f"Audio Source: {audio_path}", flush=True)
    print(f"Output Video: {output_video}", flush=True)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video
    ]

    ffmpeg_log = os.path.join(proj_dir, "ffmpeg_render.log")
    with open(ffmpeg_log, "wb") as err_log:
        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=err_log)

        for frame_idx in range(total_frames):
            t = frame_idx / fps
            im = render_vertical_frame(t, total_duration, bg_workstation, bg_mascot, logo_header)
            proc.stdin.write(im.tobytes())

            if frame_idx % 120 == 0 or frame_idx == total_frames - 1:
                pct = (frame_idx + 1) / total_frames * 100.0
                print(f"Rendered frame {frame_idx + 1}/{total_frames} ({pct:.1f}%) [t={t:.2f}s]", flush=True)

        proc.stdin.close()
        proc.wait()

    if proc.returncode == 0:
        file_size_mb = os.path.getsize(output_video) / (1024 * 1024)
        print(f"\n[SUCCESS] Render complete! Video saved to:", flush=True)
        print(f"Path: {output_video}", flush=True)
        print(f"Size: {file_size_mb:.2f} MB", flush=True)
    else:
        with open(ffmpeg_log, "r", encoding="utf-8", errors="ignore") as f:
            err_text = f.read()
        print(f"\n[ERROR] FFmpeg failed with code {proc.returncode}:", flush=True)
        print(err_text[-1000:], flush=True)

if __name__ == '__main__':
    main()
