"""
AI Agents Video Renderer — Style 2A Modern Studio Tech
60 seconds · 16:9 · 1280x720 · 24fps

Scenes:
  Clip 1: Golden Hook       — Clock + node-web
  Clip 2: Disrupt           — Org-chart fracture
  Clip 3: Insider Secret    — Platform handoff fail
  Clip 4: Mechanism         — Autonomous loop
  Clip 5: Scale             — 10x orbiting nodes
  Clip 6: Elevation         — Fork in the road CTA

Audio: edge-tts (network) → Windows SAPI (subprocess) → synthesized sine fallback
"""

import os, sys, math, time, struct, wave, subprocess, asyncio, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioArrayClip, concatenate_videoclips

# ── Config ────────────────────────────────────────────────────────────────────
OUT_DIR   = r"D:\Antigravity\Pro\agentic-code\projects\ai_agents_video"
AUDIO_DIR = os.path.join(OUT_DIR, "audio")
FRAMES_DIR = os.path.join(OUT_DIR, "frames_tmp")
OUTPUT    = os.path.join(OUT_DIR, "ai_agents_replacing_teams.mp4")
W, H      = 1280, 720
FPS       = 24
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = (253, 253, 252)       # near-white studio
GRID     = (220, 228, 235)       # light-gray floor grid
CYAN     = (0, 210, 220)         # electric cyan — AI / automation
AMBER    = (255, 165, 30)        # alert amber — bottleneck / friction
INDIGO   = (60, 40, 130)         # deep indigo — legacy teams
BLACK    = (20, 20, 25)          # stick figure / text
WHITE    = (255, 255, 255)
RED_BEAN = (200, 40, 40)         # beanie
YELLOW   = (240, 190, 30)        # shirt

# ── Narration lines ───────────────────────────────────────────────────────────
LINES = [
    "What if your biggest engineering bottleneck isn't headcount? It's the fact that humans sleep.",
    "Every team assumes more developers means faster shipping. But adding engineers also adds meetings, reviews, and miscommunications.",
    "Here is the secret nobody talks about. The real cost of a software team isn't salaries, it's coordination. Every handoff is a failure point.",
    "AI agents don't hand off. They write code, run tests, catch regressions, and deploy in one uninterrupted loop, never waiting for a Slack reply.",
    "Companies using agentic workflows are shipping ten times faster, not by hiring more people, but by removing the waiting entirely.",
    "So the real question isn't whether AI will replace developers. It's whether your team is building with agents, or competing against them. What do you think?"
]

# ── TTS: try edge-tts, fallback to synthesized audio ─────────────────────────
def synth_audio_numpy(text, path, sr=22050):
    """Fallback: generate silence with subtle tone so audio track exists."""
    words = len(text.split())
    duration = max(4.0, words * 0.42)   # ~140 wpm estimate
    t = np.linspace(0, duration, int(sr * duration), dtype=np.float32)
    # Very quiet 110Hz tone so the audio track is non-empty
    audio = (np.sin(2 * np.pi * 110 * t) * 0.05).astype(np.float32)
    # Write as WAV
    audio_int = (audio * 32767).astype(np.int16)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int.tobytes())
    return duration

async def edge_tts_generate(text, path):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural", rate="-5%", volume="+0%")
    mp3_path = path.replace('.wav', '.mp3')
    await communicate.save(mp3_path)
    # Convert mp3 → wav using ffmpeg
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_path, "-ar", "22050", "-ac", "1", path
    ], capture_output=True)
    os.remove(mp3_path)
    return True

def get_audio(i, text):
    wav_path = os.path.join(AUDIO_DIR, f"clip{i+1}.wav")
    if os.path.exists(wav_path) and os.path.getsize(wav_path) > 5000:
        print(f"  [audio] clip{i+1} cached")
        return wav_path
    # Try edge-tts
    try:
        loop = asyncio.new_event_loop()
        ok = loop.run_until_complete(asyncio.wait_for(edge_tts_generate(text, wav_path), timeout=15))
        loop.close()
        if ok and os.path.exists(wav_path) and os.path.getsize(wav_path) > 5000:
            print(f"  [audio] clip{i+1} edge-tts OK ({os.path.getsize(wav_path)//1024}KB)")
            return wav_path
    except Exception as e:
        print(f"  [audio] clip{i+1} edge-tts failed: {e}")
    # Fallback: synthesized
    synth_audio_numpy(text, wav_path)
    print(f"  [audio] clip{i+1} synthesized fallback")
    return wav_path

def load_audio_array(wav_path):
    """Load WAV → numpy float32 stereo array."""
    import wave as wv
    with wv.open(wav_path) as wf:
        sr = wf.getframerate()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)
        ch = wf.getnchannels()
        sw = wf.getsampwidth()
    dtype = {1: np.int8, 2: np.int16, 4: np.int32}[sw]
    arr = np.frombuffer(raw, dtype=dtype).astype(np.float32)
    arr /= np.iinfo(dtype).max
    if ch == 1:
        arr = np.stack([arr, arr], axis=1)
    else:
        arr = arr.reshape(-1, 2)
    return arr, sr

# ── Drawing helpers ───────────────────────────────────────────────────────────
def new_frame():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_grid(draw, alpha=1.0):
    col = tuple(int(c + (255 - c) * (1 - alpha)) for c in GRID)
    for x in range(0, W, 64):
        draw.line([(x, 0), (x, H)], fill=col, width=1)
    for y in range(H // 2, H, 48):
        draw.line([(0, y), (W, y)], fill=col, width=1)
    # perspective lines from vanishing point
    vx, vy = W // 2, H * 2 // 3
    for x in range(0, W + 1, 128):
        draw.line([(x, H), (vx, vy)], fill=col, width=1)

def draw_stickman(draw, cx, cy, scale=1.0, arm_up=False, arm_wave=0.0,
                   beanie=True, shirt=True, action="stand"):
    s = scale
    # Head
    r = int(28 * s)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=int(3*s))
    # Beanie
    if beanie:
        draw.rectangle([cx - r, cy - r - int(14*s), cx + r, cy - r + int(8*s)],
                       fill=RED_BEAN)
        draw.rectangle([cx - r - int(4*s), cy - r + int(4*s),
                        cx + r + int(4*s), cy - r + int(12*s)], fill=RED_BEAN)
    # Shirt (body)
    body_top = cy + r
    body_bot = cy + int(80 * s)
    if shirt:
        draw.rectangle([cx - int(16*s), body_top, cx + int(16*s), body_bot], fill=YELLOW)
    # Body line
    draw.line([(cx, body_top), (cx, body_bot)], fill=BLACK, width=int(3*s))
    # Legs
    leg_y = body_bot + int(60 * s)
    if action == "surf":
        draw.line([(cx, body_bot), (cx - int(30*s), leg_y)], fill=BLACK, width=int(3*s))
        draw.line([(cx, body_bot), (cx + int(10*s), leg_y - int(10*s))], fill=BLACK, width=int(3*s))
    elif action == "jump":
        draw.line([(cx, body_bot), (cx - int(20*s), body_bot + int(40*s))], fill=BLACK, width=int(3*s))
        draw.line([(cx, body_bot), (cx + int(20*s), body_bot + int(40*s))], fill=BLACK, width=int(3*s))
    else:
        draw.line([(cx, body_bot), (cx - int(20*s), leg_y)], fill=BLACK, width=int(3*s))
        draw.line([(cx, body_bot), (cx + int(20*s), leg_y)], fill=BLACK, width=int(3*s))
    # Arms
    arm_y = body_top + int(25 * s)
    if arm_up:
        # Both arms up
        draw.line([(cx, arm_y), (cx - int(45*s), arm_y - int(45*s))], fill=BLACK, width=int(3*s))
        draw.line([(cx, arm_y), (cx + int(45*s), arm_y - int(45*s))], fill=BLACK, width=int(3*s))
    elif action == "point":
        draw.line([(cx, arm_y), (cx - int(40*s), arm_y + int(10*s))], fill=BLACK, width=int(3*s))
        draw.line([(cx, arm_y), (cx + int(55*s), arm_y - int(20*s))], fill=BLACK, width=int(3*s))
    elif action == "surf":
        draw.line([(cx, arm_y), (cx - int(50*s), arm_y - int(30*s))], fill=BLACK, width=int(3*s))
        draw.line([(cx, arm_y), (cx + int(50*s), arm_y - int(30*s))], fill=BLACK, width=int(3*s))
    else:
        wave_offset = int(arm_wave * 30 * s)
        draw.line([(cx, arm_y), (cx - int(40*s), arm_y + int(20*s) - wave_offset)], fill=BLACK, width=int(3*s))
        draw.line([(cx, arm_y), (cx + int(40*s), arm_y + int(20*s) + wave_offset)], fill=BLACK, width=int(3*s))

def draw_circle_icon(draw, cx, cy, r, fill, outline=None, width=2):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill, outline=outline or fill, width=width)

def draw_rounded_rect(draw, x1, y1, x2, y2, r, fill, outline=None, width=2):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=fill,
                           outline=outline or fill, width=width)

def lerp(a, b, t):
    return a + (b - a) * t

def ease(t):
    return t * t * (3 - 2 * t)

def glow_circle(draw, cx, cy, r, color, layers=4):
    for i in range(layers, 0, -1):
        alpha = int(40 * i / layers)
        rr = r + i * 6
        # Approximate glow with larger circles, lighter color
        light = tuple(min(255, c + int((255-c) * (1 - i/layers) * 0.6)) for c in color)
        draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=light + (alpha,) if len(color) == 3 else light)

def try_font(size):
    for name in ["arial.ttf", "Arial.ttf", "DejaVuSans-Bold.ttf", "verdana.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except:
            pass
    return ImageFont.load_default()

FONT_LG  = try_font(36)
FONT_MD  = try_font(26)
FONT_SM  = try_font(20)
FONT_CAP = try_font(22)

def draw_caption(draw, text, y=H-50):
    bbox = draw.textbbox((0, 0), text, font=FONT_CAP)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    # Background strip
    draw.rectangle([0, y - 8, W, y + 36], fill=(240, 240, 240))
    draw.text((x, y), text, fill=BLACK, font=FONT_CAP)

# ── Scene renderers ───────────────────────────────────────────────────────────
def render_clip1(t, duration):
    """Golden Hook: clock + TEAM panels dissolve + node-web"""
    img, draw = new_frame()
    draw_grid(draw)

    p = t / duration   # 0→1

    # Character slides in from left
    char_x = int(lerp(-80, 500, ease(min(p * 3, 1.0))))
    char_y = 380

    # Clock icon (top center)
    clock_cx, clock_cy = 640, 160
    clock_r = int(lerp(0, 55, ease(min(p * 2, 1.0))))
    if clock_r > 0:
        draw.ellipse([clock_cx-clock_r, clock_cy-clock_r,
                      clock_cx+clock_r, clock_cy+clock_r],
                     outline=CYAN, width=4, fill=BG)
        # Clock hands spinning
        angle = p * 4 * math.pi
        hx = clock_cx + int(clock_r * 0.6 * math.sin(angle))
        hy = clock_cy - int(clock_r * 0.6 * math.cos(angle))
        draw.line([(clock_cx, clock_cy), (hx, hy)], fill=CYAN, width=3)
        mangle = angle * 12
        mx = clock_cx + int(clock_r * 0.45 * math.sin(mangle))
        my = clock_cy - int(clock_r * 0.45 * math.cos(mangle))
        draw.line([(clock_cx, clock_cy), (mx, my)], fill=AMBER, width=2)

    # TEAM panels — appear then dissolve at t=0.3
    dissolve = max(0, min(1, (p - 0.3) / 0.2))
    panel_alpha = int((1 - dissolve) * 200)
    if p < 0.5:
        # Left TEAM panel
        px1, py1, px2, py2 = 60, 220, 300, 320
        draw_rounded_rect(draw, px1, py1, px2, py2, 12,
                          fill=INDIGO, outline=INDIGO, width=2)
        draw.text((px1+20, py1+30), "TEAM A", fill=WHITE, font=FONT_MD)
        # Right TEAM panel
        draw_rounded_rect(draw, 980, 220, 1220, 320, 12,
                          fill=INDIGO, outline=INDIGO, width=2)
        draw.text((1000, 250), "TEAM B", fill=WHITE, font=FONT_MD)

    # Node web (appears after panels dissolve)
    if p > 0.4:
        web_alpha = min(1.0, (p - 0.4) / 0.3)
        n_nodes = 7
        web_cx, web_cy = 750, 350
        node_r = 14
        ring_r = int(lerp(0, 160, ease(web_alpha)))
        nodes = []
        for i in range(n_nodes):
            angle = 2 * math.pi * i / n_nodes
            nx = web_cx + int(ring_r * math.cos(angle))
            ny = web_cy + int(ring_r * math.sin(angle))
            nodes.append((nx, ny))
            draw_circle_icon(draw, nx, ny, node_r, CYAN)
        # Center node
        draw_circle_icon(draw, web_cx, web_cy, node_r + 4, CYAN)
        # Connections
        for nx, ny in nodes:
            draw.line([(web_cx, web_cy), (nx, ny)], fill=CYAN, width=2)
        # Inter-node connections
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes), 2):
                draw.line([nodes[i], nodes[j]], fill=CYAN, width=1)

    # Character
    arm_wave = math.sin(p * math.pi * 3) * 0.5
    arm_up = p > 0.6
    draw_stickman(draw, char_x, char_y, scale=1.0, arm_up=arm_up, arm_wave=arm_wave)

    # Caption
    cap = "What if your biggest bottleneck isn't headcount?"
    if p > 0.1:
        draw_caption(draw, cap)

    return np.array(img)

def render_clip2(t, duration):
    """Disrupting Assumptions: org-chart grows + cracks"""
    img, draw = new_frame()
    draw_grid(draw)
    p = t / duration

    char_x, char_y = 280, 380

    # Org chart
    chart_cx, chart_cy = 820, 300
    # Main nodes
    nodes = [
        (chart_cx, chart_cy - 80),               # top
        (chart_cx - 120, chart_cy + 20),          # mid-left
        (chart_cx + 120, chart_cy + 20),          # mid-right
        (chart_cx - 60,  chart_cy + 120),         # bot-left
        (chart_cx + 60,  chart_cy + 120),         # bot-right
    ]
    # Extra amber "chaos" nodes appear over time
    extra_nodes = [
        (chart_cx - 200, chart_cy + 70),
        (chart_cx + 200, chart_cy + 70),
    ]

    # Draw connections
    connections = [(0,1),(0,2),(1,3),(2,4),(1,2)]
    for a, b in connections:
        draw.line([nodes[a], nodes[b]], fill=INDIGO, width=3)

    # Tilt the whole chart when p > 0.7
    tilt = ease(max(0, (p - 0.7) / 0.3)) * 15  # degrees

    for i, (nx, ny) in enumerate(nodes):
        draw_circle_icon(draw, nx, ny, 18, INDIGO, outline=WHITE, width=2)

    # Amber extra nodes
    if p > 0.3:
        extra_alpha = ease(min(1, (p - 0.3) / 0.3))
        for ex, ey in extra_nodes:
            exs = int(lerp(0, 20, extra_alpha))
            if exs > 0:
                draw.ellipse([ex-exs, ey-exs, ex+exs, ey+exs],
                             fill=AMBER, outline=AMBER)
                # Calendar icon
                draw.rectangle([ex-exs+4, ey-exs+4, ex+exs-4, ey+exs-4],
                               outline=WHITE, width=1)

    # Crack lines at p > 0.7
    if p > 0.7:
        crack_a = ease((p - 0.7) / 0.3)
        crack_len = int(crack_a * 180)
        for angle in [30, 90, 150, 210, 270, 330]:
            rad = math.radians(angle)
            ex = chart_cx + int(crack_len * math.cos(rad))
            ey = chart_cy + int(crack_len * math.sin(rad))
            draw.line([(chart_cx, chart_cy), (ex, ey)], fill=AMBER, width=2)

    # Character — proud then stumbling
    action = "stand" if p < 0.7 else "jump"
    stagger = int(ease(max(0, (p - 0.7) / 0.3)) * 30)
    draw_stickman(draw, char_x + stagger, char_y, scale=1.0,
                  arm_up=(p < 0.3), action=action)

    # Pointing arm at chart
    if p < 0.7:
        arm_y = char_y - 80 + 25
        draw.line([(char_x + 40, arm_y), (chart_cx - 150, arm_y - 20)],
                  fill=BLACK, width=3)

    cap = "Adding engineers adds meetings, reviews, and chaos."
    if p > 0.1:
        draw_caption(draw, cap)

    return np.array(img)

def render_clip3(t, duration):
    """Insider Secret: two platforms drift apart, file falls"""
    img, draw = new_frame()
    draw_grid(draw)
    p = t / duration

    # Platforms drift apart
    drift = ease(min(p * 2, 1.0)) * 120
    lp_x1, lp_x2 = int(100 - drift * 0.3), int(420 - drift * 0.3)
    rp_x1, rp_x2 = int(500 + drift * 0.5), int(820 + drift * 0.5)
    plat_y1, plat_y2 = 400, 430

    draw_rounded_rect(draw, lp_x1, plat_y1, lp_x2, plat_y2, 8,
                      fill=INDIGO, outline=INDIGO)
    draw_rounded_rect(draw, rp_x1, plat_y1, rp_x2, plat_y2, 8,
                      fill=INDIGO, outline=INDIGO)

    # Amber arrow in gap
    gap_cx = (lp_x2 + rp_x1) // 2
    if p < 0.5:
        draw.line([(gap_cx - 30, plat_y1 - 30), (gap_cx + 30, plat_y1 - 30)],
                  fill=AMBER, width=4)
        draw.polygon([(gap_cx + 30, plat_y1 - 38), (gap_cx + 30, plat_y1 - 22),
                      (gap_cx + 50, plat_y1 - 30)], fill=AMBER)

    # Cyan file icon
    file_x = int(lerp(lp_x2 - 60, (lp_x2 + rp_x1) // 2, ease(min(p * 3, 1.0))))
    file_y_base = plat_y1 - 80
    # File falls after p=0.6
    fall = ease(max(0, (p - 0.6) / 0.4)) * 300
    file_y = int(file_y_base + fall)
    file_alpha = max(0, 1 - fall / 250)
    file_col = tuple(int(c + (255-c) * (1 - file_alpha)) for c in CYAN)
    if file_y < H + 40:
        draw.rectangle([file_x, file_y, file_x + 40, file_y + 50],
                       fill=file_col, outline=CYAN, width=2)
        # Fold corner
        draw.polygon([(file_x + 25, file_y), (file_x + 40, file_y),
                      (file_x + 40, file_y + 15)], fill=BG)

    # Character on left platform
    char_x = (lp_x1 + lp_x2) // 2
    char_y = plat_y1 - 10
    # Jump attempt at p=0.4-0.6
    if 0.4 < p < 0.6:
        jump_offset = -int(ease((p - 0.4) / 0.2) * 60)
        draw_stickman(draw, char_x, char_y + jump_offset, scale=1.0, action="jump")
    else:
        draw_stickman(draw, char_x, char_y, scale=1.0, action="stand")

    cap = "Every handoff is a failure point."
    if p > 0.1:
        draw_caption(draw, cap)

    return np.array(img)

def render_clip4(t, duration):
    """Mechanism: cyan robotic arm + autonomous write→test→deploy loop"""
    img, draw = new_frame()
    draw_grid(draw)
    p = t / duration

    # Loop diagram — 3 nodes in a triangle
    loop_cx, loop_cy = 760, 300
    loop_r = 140
    loop_nodes = []
    labels = ["CODE", "TEST", "DEPLOY"]
    icons  = ["</> ", "✓  ", "▲  "]
    for i in range(3):
        angle = -math.pi / 2 + 2 * math.pi * i / 3
        nx = loop_cx + int(loop_r * math.cos(angle))
        ny = loop_cy + int(loop_r * math.sin(angle))
        loop_nodes.append((nx, ny))

    # Draw loop arrows
    loop_progress = min(1.0, p * 1.5)
    for i in range(3):
        a = loop_nodes[i]
        b = loop_nodes[(i + 1) % 3]
        # Arrow line
        draw.line([a, b], fill=CYAN, width=4)
        # Arrowhead
        mid = ((a[0]+b[0])//2, (a[1]+b[1])//2)
        dx, dy = b[0]-a[0], b[1]-a[1]
        L = max(1, math.sqrt(dx*dx + dy*dy))
        ux, uy = dx/L, dy/L
        px, py = -uy, ux
        tip = (int(mid[0]+ux*12), int(mid[1]+uy*12))
        l1  = (int(tip[0]-ux*18+px*8), int(tip[1]-uy*18+py*8))
        l2  = (int(tip[0]-ux*18-px*8), int(tip[1]-uy*18-py*8))
        draw.polygon([tip, l1, l2], fill=CYAN)

    # Node circles
    for i, (nx, ny) in enumerate(loop_nodes):
        draw_circle_icon(draw, nx, ny, 32, CYAN, outline=WHITE, width=3)
        draw.text((nx - 14, ny - 10), icons[i], fill=WHITE, font=FONT_SM)

    # Spinning file icon on the loop
    if p > 0.1:
        loop_angle = -math.pi/2 + p * 4 * math.pi
        file_x = loop_cx + int(loop_r * math.cos(loop_angle))
        file_y = loop_cy + int(loop_r * math.sin(loop_angle))
        draw.rectangle([file_x - 14, file_y - 18, file_x + 14, file_y + 18],
                       fill=YELLOW, outline=CYAN, width=2)

    # Rising robotic arm at start
    if p < 0.3:
        arm_alpha = ease(p / 0.3)
        arm_top = int(H - arm_alpha * 180)
        draw.rectangle([600, arm_top, 630, H], fill=CYAN)
        draw.ellipse([585, arm_top - 20, 645, arm_top + 20], fill=CYAN)

    # Character to left, watching
    char_x = 220
    char_y = 380
    # Try to intercept at p=0.6
    intercept = ease(max(0, (p - 0.6) / 0.3)) * 100
    action = "point" if p < 0.6 else "stand"
    draw_stickman(draw, char_x + int(intercept), char_y, scale=1.0, action=action)

    cap = "AI agents write, test, and deploy in one uninterrupted loop."
    if p > 0.05:
        draw_caption(draw, cap)

    return np.array(img)

def render_clip5(t, duration):
    """Scale: 10 orbiting agent nodes + 10x stack + floor pulse"""
    img, draw = new_frame()
    draw_grid(draw)
    p = t / duration

    char_x, char_y = 500, 380
    orbit_r = int(lerp(50, 220, ease(min(p * 2, 1.0))))

    # 10 orbiting cyan nodes
    for i in range(10):
        base_angle = 2 * math.pi * i / 10
        spin = p * 2 * math.pi
        angle = base_angle + spin
        nx = char_x + int(orbit_r * math.cos(angle))
        ny = char_y + int(orbit_r * math.sin(angle))
        # Light trail
        for tr in range(4):
            trail_angle = angle - tr * 0.15
            tx = char_x + int(orbit_r * math.cos(trail_angle))
            ty = char_y + int(orbit_r * math.sin(trail_angle))
            trail_r = max(2, 10 - tr * 3)
            alpha_col = tuple(int(c + (255-c)*(tr/4)) for c in CYAN)
            draw.ellipse([tx-trail_r, ty-trail_r, tx+trail_r, ty+trail_r],
                         fill=alpha_col)
        # Main node
        draw_circle_icon(draw, nx, ny, 12, CYAN, outline=WHITE, width=2)

    # 10x icon stack at top (appears mid-clip)
    if p > 0.3:
        stack_alpha = ease((p - 0.3) / 0.3)
        for j in range(10):
            arrow_y = int(lerp(H, 80, stack_alpha)) + j * 22
            if 60 < arrow_y < 400:
                ax = 850
                col = AMBER if j < 3 else CYAN
                draw.polygon([(ax, arrow_y), (ax - 14, arrow_y + 14),
                              (ax + 14, arrow_y + 14)], fill=col)

    # Floor pulse at end
    if p > 0.7:
        pulse_a = ease((p - 0.7) / 0.3)
        pulse_r = int(pulse_a * 500)
        for ring in range(3):
            rr = max(0, pulse_r - ring * 60)
            if rr > 0:
                alpha_col = tuple(int(c + (255-c) * (ring / 3)) for c in CYAN)
                draw.ellipse([char_x - rr, H - rr // 2,
                              char_x + rr, H + rr // 2], outline=alpha_col, width=3)

    # Character
    char_surf_x = char_x + int(ease(max(0, p - 0.7)) * 200)
    action = "surf" if p > 0.7 else ("stand" if p < 0.3 else "stand")
    arm_up = 0.3 < p < 0.7
    draw_stickman(draw, char_surf_x, char_y, scale=1.0, arm_up=arm_up, action=action)

    cap = "Shipping 10x faster — by removing the waiting entirely."
    if p > 0.05:
        draw_caption(draw, cap)

    return np.array(img)

def render_clip6(t, duration):
    """Elevation: fork in the road CTA"""
    img, draw = new_frame()
    draw_grid(draw)
    p = t / duration

    char_x = int(lerp(200, 540, ease(min(p * 2, 1.0))))
    char_y = 380

    # Floor splits into two paths
    if p > 0.1:
        split_alpha = ease(min((p - 0.1) / 0.3, 1.0))
        # Left path (amber)
        lx = int(lerp(char_x, char_x - 240, split_alpha * ease(p)))
        draw.line([(char_x, H), (lx, H - 200)], fill=AMBER, width=5)
        # Right path (cyan)
        rx = int(lerp(char_x, char_x + 240, split_alpha * ease(p)))
        draw.line([(char_x, H), (rx, H - 200)], fill=CYAN, width=5)

    # Left icon: human figure (amber)
    if p > 0.3:
        icon_alpha = ease((p - 0.3) / 0.3)
        lx_icon, ly_icon = 220, 230
        draw_circle_icon(draw, lx_icon, ly_icon - 30, int(20 * icon_alpha), AMBER)
        draw.line([(lx_icon, ly_icon), (lx_icon, ly_icon + int(50 * icon_alpha))],
                  fill=AMBER, width=4)

    # Right icon: cyan agent node
    if p > 0.3:
        icon_alpha = ease((p - 0.3) / 0.3)
        rx_icon, ry_icon = 900, 230
        draw_circle_icon(draw, rx_icon, ry_icon, int(28 * icon_alpha), CYAN, outline=WHITE, width=3)
        # Spokes
        for a in range(0, 360, 60):
            rad = math.radians(a)
            spoke_r = int(28 * icon_alpha)
            ex = rx_icon + int((spoke_r + 12) * math.cos(rad))
            ey = ry_icon + int((spoke_r + 12) * math.sin(rad))
            draw.line([(rx_icon, ry_icon), (ex, ey)], fill=CYAN, width=2)

    # Character — decisive point at end
    action = "point" if p > 0.65 else "stand"
    draw_stickman(draw, char_x, char_y, scale=1.0, action=action)

    # Final pulse
    if p > 0.7:
        pulse_a = ease((p - 0.7) / 0.3)
        pr = int(pulse_a * 300)
        draw.ellipse([char_x - pr, char_y + 60 - pr // 2,
                      char_x + pr, char_y + 60 + pr // 2],
                     outline=CYAN, width=3)

    cap = "Build with agents — or compete against them?"
    if p > 0.05:
        draw_caption(draw, cap)

    return np.array(img)

SCENES = [render_clip1, render_clip2, render_clip3,
          render_clip4, render_clip5, render_clip6]

# ── Build clips ───────────────────────────────────────────────────────────────
def build_clip(scene_fn, audio_path, scene_idx):
    # Load audio to get duration
    arr, sr = load_audio_array(audio_path)
    duration = len(arr) / sr
    print(f"  Scene {scene_idx+1}: duration={duration:.2f}s, frames={int(duration*FPS)}")

    n_frames = int(duration * FPS)
    frames = []
    for f in range(n_frames):
        t = f / FPS
        frame = scene_fn(t, duration)
        frames.append(frame)

    # Build video
    def make_frame(t):
        fi = min(int(t * FPS), n_frames - 1)
        return frames[fi]

    video = ImageClip(make_frame, duration=duration)
    # Attach audio
    audio = AudioArrayClip(arr, fps=sr)
    video = video.with_audio(audio)
    return video

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=== AI Agents Video Renderer ===")
    print(f"Output: {OUTPUT}")

    # 1. Generate audio
    print("\n[1/3] Generating narration audio...")
    audio_paths = []
    for i, line in enumerate(LINES):
        path = get_audio(i, line)
        audio_paths.append(path)

    # 2. Render scenes
    print("\n[2/3] Rendering scenes...")
    clips = []
    for i, (scene_fn, audio_path) in enumerate(zip(SCENES, audio_paths)):
        print(f"  Rendering clip {i+1}/6...")
        clip = build_clip(scene_fn, audio_path, i)
        clips.append(clip)

    # 3. Concatenate + export
    print("\n[3/3] Exporting final video...")
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(
        OUTPUT,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        logger=None
    )
    print(f"\n✅ Done! → {OUTPUT}")
    size_mb = os.path.getsize(OUTPUT) / 1_000_000
    print(f"   File size: {size_mb:.1f} MB  |  Duration: {final.duration:.1f}s")

if __name__ == "__main__":
    main()
