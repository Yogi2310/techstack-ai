# 🤖 Agentic Stickman Video Director & Code Engine

> **Project Root:** `D:\Antigravity\Pro\agentic-code`  
> **Source Origin:** Copied from [`D:\Antigravity\Pro\stickman-video-director`](file:///D:/Antigravity/Pro/stickman-video-director)  
> **Status:** Configured, runtime dependencies installed, and validated.

---

## 🚀 Overview

This project provides an autonomous, agentic coding framework for producing animated stickman videos for YouTube, Shorts, TikTok, and educational explainers.

You can direct the agent to generate scripts, storyboards, voiceovers, aligned subtitles, canvas illustrations, and rendered video clips.

---

## 🎬 Two Production Modes

### 1. Mode A · Director Mode (Prompts & Storyboarding)
- **Input:** Any topic, article, or script.
- **Agent Workflow:**
  1. Structures narrative into the **5-Stage High-Completion Heartbeat Engine**:
     - *Golden Hook* (curiosity trigger)
     - *Disrupting Assumptions* (cognitive conflict)
     - *Unveiling Insider Secrets* (the hidden truth)
     - *Ultimate Truth Revelation* (the punchline / payoff)
     - *Elevation & High-Engagement Discussion* (viral comments trigger)
  2. Generates scene-by-scene video generation prompts (for Gemini Omni Flash, Runway, Kling, or Pika).
  3. Locks voice continuity, character design anchors, and sound effects cues.

### 2. Mode B · Autopilot Mode (End-to-End Local Rendering)
- **Input:** Audio voiceover file or synthesized TTS narration + script.
- **Agent Workflow:**
  1. Initializes project directory: `npm run init:project -- <dir>`
  2. Aligns captions and builds `project.json` manifest.
  3. Defines shots, poses, text layers, and micro-animations.
  4. Renders preview frames and outputs complete captioned MP4 via local canvas and FFmpeg.

---

## 🛠️ CLI Quick Commands (Root Level)

Run these directly from `D:\Antigravity\Pro\agentic-code`:

```bash
# 1. Verify system dependencies (Node, FFmpeg, Canvas, Fonts)
npm run doctor

# 2. Scaffold a new video project
npm run init:project -- projects/my_new_video

# 3. Validate a project's timing, audio, and shot layers
npm run validate -- projects/my_new_video/project.json

# 4. Preview sample shots
npm run preview -- projects/my_new_video/project.json --seconds 10

# 5. Approve sample
npm run approve -- projects/my_new_video/project.json --note "Approved"

# 6. Render full video
npm run render -- projects/my_new_video/project.json
```

---

## 📁 Directory Structure

```
D:\Antigravity\Pro\agentic-code\
├── package.json                   # Root workspace scripts (doctor, validate, render)
├── AGENTIC_WORKFLOW.md            # This agentic guide
├── projects/                      # Your created video projects
│   └── demo/                      # Example scaffolded project
├── skills/
│   └── directing-stickman-videos/ # Core runtime & agent skills
│       ├── scripts/               # autopilot-render.mjs, gemini-media.mjs, etc.
│       ├── assets/                # B1 stickman poses, fonts, crayon illustrations
│       ├── references/            # Style catalogs, narrative rules, voice guides
│       └── examples/              # Ready-to-render B1 sample video
└── assets/                        # Shared preview and visual assets
```

---

## 💡 How to Instruct the Agent

Simply tell the agent:
- *"Create a 30-second Stickman explainer about how compound interest works in Style B1."*
- *"Write a 60-second Director storyboard on Why 90% of Startups Fail in Style 2A (Modern Studio Tech)."*
- *"Render the demo video in projects/demo."*
