# 🚀 TechStack AI - Agentic Video Studio & YouTube Automation

An end-to-end autonomous video production and YouTube distribution platform engineered for **TechStack AI** ([`@TechStacAI`](https://www.youtube.com/@TechStacAI)).

---

## 🌟 Overview

This repository contains the complete algorithmic production suite for generating high-retention, developer-focused video content (9:16 vertical Shorts and 16:9 landscape explainers) with custom 3D LEGO character animation, kinetic subtitles, procedural sound design, and automated YouTube Data API v3 publishing.

---

## 📁 Repository Structure

```
.
├── agentic-code/projects/
│   ├── bolt_new_saas_short/        # Day 2 Short: "I Built a Full Stack SaaS in 12 Mins With Bolt.new"
│   │   ├── BOLT_NEW_SAAS_SHORT_9x16.mp4
│   │   ├── render_video.py         # 1080x1920 24fps FFmpeg rawvideo renderer
│   │   ├── build_audio.py          # Narration + procedural D&B synthwave beat
│   │   └── upload_short.py         # YouTube API uploader
│   │
│   ├── 3_free_ai_tools_short/      # Day 1 Short: "3 Free AI Tools That Feel Illegal for Developers"
│   │   ├── 3_FREE_AI_TOOLS_SHORT_9x16.mp4
│   │   ├── render_vertical_short.py
│   │   ├── build_short_audio.py
│   │   └── upload_short.py
│   │
│   ├── lego_agent_fixing_systems/  # 16:9 Brickfilm: "The Autonomous LEGO Agent: Brickfilm Fix"
│   │   ├── LEGO_AGENT_FIXING_SYSTEMS_16x9.mp4
│   │   └── render_lego_agent_video.py
│   │
│   └── proper_3d_tech_explainer/   # 3D Cinematic: "AI Agents vs Human Developers"
│       └── render_proper_3d_explainer.py
│
├── Rico_Style_2D_Comedy/           # 2D Meme Cartoon Slapstick Animation (Rico Style)
│   ├── scripts/render_exam_panic_short.py
│   └── scripts/render_rico_style_short.py
│
├── upload_to_youtube.py            # Universal YouTube Data API v3 video uploader
├── channel_profile_pic.png         # Official channel avatar
├── channel_banner.png              # Official channel banner
└── PROJECT_CONVERSATION_MEMORY.md  # Comprehensive project log & growth playbook
```

---

## ⚡ Core Features

- **3D Articulated LEGO Minifigure Mechanics**: Procedural 2-joint kinematic locomotion, authentic head sheen, studs, C-clamp hands, and animated station interactions.
- **Procedural Sound Engine**: Synthesizes synchronized narration with energetic 132 BPM synthwave/D&B drum patterns, sub-bass lines, and mechanical sound effects.
- **Kinetic Subtitle System**: High-contrast glass container with real-time active word highlighting in neon yellow (`#FFE732`) and cyan (`#00F0FF`).
- **YouTube API Automation**: Resumable video uploading, automated token refresh, and metadata optimization.

---

## 🛠️ Quick Start

### 1. Requirements
- Python 3.10+
- FFmpeg on PATH
- Pillow, NumPy, google-api-python-client, google-auth-oauthlib

```bash
pip install pillow numpy google-api-python-client google-auth-oauthlib google-auth-httplib2 pywin32
```

### 2. Render a 9:16 Vertical Short
```bash
python agentic-code/projects/bolt_new_saas_short/render_video.py
```

### 3. Upload to YouTube
```bash
python agentic-code/projects/bolt_new_saas_short/upload_short.py
```

---

## 📺 Published Productions Live on YouTube
- 🎬 [I Built a Full Stack SaaS in 12 Minutes With Bolt.new](https://www.youtube.com/shorts/d2wVQ2cqEMM)
- 🎬 [3 Free AI Tools That Feel Illegal for Developers](https://www.youtube.com/shorts/YwWiQQ5U0s0)
- 🎬 [When AI Agents Fix Production at 2 AM (LEGO Edition)](https://www.youtube.com/shorts/a84L5be82i4)

---

## 📄 License
MIT License. Created by Yogesh Bandekar for **TechStack AI**.
