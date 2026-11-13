/**
 * VideoEngine - Core Canvas Video Rendering, Playback, and Export Engine
 * Built for ViewMax Pro. Runs entirely in-browser.
 */

class VideoEngine {
    constructor() {
        this.scenes = [];
        this.isPlaying = false;
        this.playbackStartTime = 0;
        this.pausedTime = 0;
        this.animationFrameId = null;
        this.currentPlayTime = 0;
        
        // Callbacks
        this.onTimeUpdate = null;
        this.onPlaybackEnd = null;
        
        // Image cache to avoid reloading images on every frame
        this.imageCache = new Map();
        
        // Video cache for drawing video frames on canvas
        this.videoCache = new Map();
        
        // Add a default scene to start
        this.addScene();
    }

    /**
     * Creates a new blank scene with default styles
     */
    addScene() {
        const scene = {
            id: 'scene_' + Math.random().toString(36).substr(2, 9),
            background: {
                type: 'gradient',
                color: '#1a1a2e',
                gradient: {
                    from: '#6C5CE7',
                    to: '#a855f7',
                    angle: 135
                },
                imageUrl: ''
            },
            texts: [
                {
                    content: 'Double click to edit text',
                    x: 0.5,
                    y: 0.5,
                    fontSize: 64,
                    fontFamily: 'Inter',
                    color: '#ffffff',
                    bold: true,
                    italic: false,
                    align: 'center',
                    animation: 'fadeIn'
                }
            ],
            duration: 5, // default 5 seconds
            transition: 'fade' // fade, slideLeft, slideRight, zoomIn, none
        };
        
        this.scenes.push(scene);
        return scene;
    }

    /**
     * Removes a scene at the specified index
     */
    removeScene(index) {
        if (index >= 0 && index < this.scenes.length) {
            this.scenes.splice(index, 1);
        }
        if (this.scenes.length === 0) {
            this.addScene();
        }
    }

    /**
     * Updates scene properties
     */
    updateScene(index, data) {
        if (index >= 0 && index < this.scenes.length) {
            this.scenes[index] = { ...this.scenes[index], ...data };
        }
    }

    /**
     * Reorders scenes
     */
    reorderScenes(fromIndex, toIndex) {
        if (fromIndex >= 0 && fromIndex < this.scenes.length && 
            toIndex >= 0 && toIndex < this.scenes.length) {
            const temp = this.scenes[fromIndex];
            this.scenes.splice(fromIndex, 1);
            this.scenes.splice(toIndex, 0, temp);
        }
    }

    /**
     * Helper to load/get images in cache
     */
    loadImage(url) {
        if (this.imageCache.has(url)) {
            return this.imageCache.get(url);
        }
        const img = new Image();
        img.src = url;
        this.imageCache.set(url, img);
        return img;
    }

    /**
     * Helper to load/get video element in cache for canvas rendering
     */
    loadVideo(url) {
        if (this.videoCache.has(url)) {
            return this.videoCache.get(url);
        }
        const video = document.createElement('video');
        video.src = url;
        video.muted = true;
        video.loop = true;
        video.playsInline = true;
        video.crossOrigin = 'anonymous';
        video.load();
        
        // Auto play to load frames
        video.play().catch(() => {});
        
        this.videoCache.set(url, video);
        return video;
    }

    /**
     * Renders a static scene to the canvas at a specific progress state (0 to 1)
     */
    renderFrame(canvas, sceneIndex, sceneProgress, prevSceneIndex = -1, transitionProgress = 0) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // If doing a transition, draw previous scene to an offscreen canvas first
        if (prevSceneIndex >= 0 && transitionProgress > 0) {
            const tempCanvas1 = document.createElement('canvas');
            tempCanvas1.width = width;
            tempCanvas1.height = height;
            this.drawSceneToContext(tempCanvas1.getContext('2d'), this.scenes[prevSceneIndex], width, height, 1);

            const tempCanvas2 = document.createElement('canvas');
            tempCanvas2.width = width;
            tempCanvas2.height = height;
            this.drawSceneToContext(tempCanvas2.getContext('2d'), this.scenes[sceneIndex], width, height, sceneProgress);

            // Apply transition effects
            const transition = this.scenes[sceneIndex].transition;
            ctx.save();
            if (transition === 'fade') {
                // Draw bottom scene (prev)
                ctx.drawImage(tempCanvas1, 0, 0);
                // Draw top scene with opacity
                ctx.globalAlpha = transitionProgress;
                ctx.drawImage(tempCanvas2, 0, 0);
            } else if (transition === 'slideLeft') {
                // Slide in from right
                ctx.drawImage(tempCanvas1, -transitionProgress * width, 0);
                ctx.drawImage(tempCanvas2, width - (transitionProgress * width), 0);
            } else if (transition === 'slideRight') {
                // Slide in from left
                ctx.drawImage(tempCanvas1, transitionProgress * width, 0);
                ctx.drawImage(tempCanvas2, -width + (transitionProgress * width), 0);
            } else if (transition === 'zoomIn') {
                // Zoom in from center
                ctx.drawImage(tempCanvas1, 0, 0);
                ctx.globalAlpha = transitionProgress;
                const scale = 0.5 + 0.5 * transitionProgress;
                const w = width * scale;
                const h = height * scale;
                const x = (width - w) / 2;
                const y = (height - h) / 2;
                ctx.drawImage(tempCanvas2, x, y, w, h);
            } else {
                // Default fallback (no transition)
                ctx.drawImage(tempCanvas2, 0, 0);
            }
            ctx.restore();
        } else {
            // Standard render without transition
            this.drawSceneToContext(ctx, this.scenes[sceneIndex], width, height, sceneProgress);
        }
    }

    /**
     * Low-level method to draw a single scene on a canvas context
     */
    drawSceneToContext(ctx, scene, width, height, progress) {
        if (!scene) return;

        // 1. Draw Background
        const bg = scene.background;
        if (bg.type === 'solid') {
            ctx.fillStyle = bg.color || '#1a1a2e';
            ctx.fillRect(0, 0, width, height);
        } else if (bg.type === 'gradient' && bg.gradient) {
            const g = bg.gradient;
            // Calculate gradient coordinates based on angle
            const angleRad = (g.angle * Math.PI) / 180;
            const r = Math.sqrt(width * width + height * height) / 2;
            const cx = width / 2;
            const cy = height / 2;
            const x0 = cx - Math.cos(angleRad) * r;
            const y0 = cy - Math.sin(angleRad) * r;
            const x1 = cx + Math.cos(angleRad) * r;
            const y1 = cy + Math.sin(angleRad) * r;

            const grad = ctx.createLinearGradient(x0, y0, x1, y1);
            grad.addColorStop(0, g.from || '#6C5CE7');
            grad.addColorStop(1, g.to || '#a855f7');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, width, height);
        } else if (bg.type === 'image' && bg.imageUrl) {
            const img = this.loadImage(bg.imageUrl);
            if (img.complete) {
                // Cover behavior
                const imgRatio = img.width / img.height;
                const canvasRatio = width / height;
                let drawWidth, drawHeight, x, y;

                if (imgRatio > canvasRatio) {
                    drawHeight = height;
                    drawWidth = height * imgRatio;
                    x = (width - drawWidth) / 2;
                    y = 0;
                } else {
                    drawWidth = width;
                    drawHeight = width / imgRatio;
                    x = 0;
                    y = (height - drawHeight) / 2;
                }
                ctx.drawImage(img, x, y, drawWidth, drawHeight);
            } else {
                // Fallback while loading
                ctx.fillStyle = '#161a2b';
                ctx.fillRect(0, 0, width, height);
                img.onload = () => {
                    // Force refresh if playing or editing
                    this.drawSceneToContext(ctx, scene, width, height, progress);
                };
            }
        } else if (bg.type === 'cartoon') {
            this.drawCartoonBackground(ctx, bg.theme || 'space', width, height, progress);
        } else if (bg.type === 'video' && bg.videoUrl) {
            const video = this.loadVideo(bg.videoUrl);
            if (video) {
                const targetTime = progress * scene.duration;
                // Sync video playback time with timeline progress
                if (Math.abs(video.currentTime - targetTime) > 0.15) {
                    video.currentTime = targetTime;
                }
                
                if (video.readyState >= 2) {
                    // Cover behavior for video
                    const videoRatio = video.videoWidth / video.videoHeight;
                    const canvasRatio = width / height;
                    let drawWidth, drawHeight, x, y;

                    if (videoRatio > canvasRatio) {
                        drawHeight = height;
                        drawWidth = height * videoRatio;
                        x = (width - drawWidth) / 2;
                        y = 0;
                    } else {
                        drawWidth = width;
                        drawHeight = width / videoRatio;
                        x = 0;
                        y = (height - drawHeight) / 2;
                    }
                    ctx.drawImage(video, x, y, drawWidth, drawHeight);
                } else {
                    ctx.fillStyle = '#000000';
                    ctx.fillRect(0, 0, width, height);
                }
            }
        }

        // 2. Draw Text Overlays
        scene.texts.forEach(text => {
            ctx.save();
            
            // Apply text styles
            let fontStyle = '';
            if (text.italic) fontStyle += 'italic ';
            if (text.bold) fontStyle += 'bold ';
            ctx.font = `${fontStyle}${text.fontSize}px ${text.fontFamily || 'Inter'}, sans-serif`;
            ctx.fillStyle = text.color || '#ffffff';
            ctx.textAlign = text.align || 'center';
            ctx.textBaseline = 'middle';

            // Shadow for maximum readability
            ctx.shadowColor = 'rgba(0,0,0,0.5)';
            ctx.shadowBlur = 8;
            ctx.shadowOffsetX = 2;
            ctx.shadowOffsetY = 2;

            // Handle alignment positioning offset
            let textX = text.x * width;
            let textY = text.y * height;

            // Handle word wrap
            const maxWidth = width * 0.85;
            const words = text.content.split(' ');
            let line = '';
            const lines = [];

            for (let n = 0; n < words.length; n++) {
                let testLine = line + words[n] + ' ';
                let metrics = ctx.measureText(testLine);
                let testWidth = metrics.width;
                if (testWidth > maxWidth && n > 0) {
                    lines.push(line.trim());
                    line = words[n] + ' ';
                } else {
                    line = testLine;
                }
            }
            lines.push(line.trim());

            // Handle Animations based on scene progress
            let opacity = 1;
            let yOffset = 0;
            let charLimit = text.content.length;

            if (text.animation === 'fadeIn') {
                // Fade in over first 0.8 seconds
                const animDuration = 0.8 / scene.duration;
                opacity = Math.min(1, progress / animDuration);
            } else if (text.animation === 'typewriter') {
                // Characters print out over first 1.5 seconds
                const animDuration = 1.5 / scene.duration;
                const animProgress = Math.min(1, progress / animDuration);
                charLimit = Math.floor(text.content.length * animProgress);
            } else if (text.animation === 'slideUp') {
                // Slide up over first 0.6 seconds
                const animDuration = 0.6 / scene.duration;
                const animProgress = Math.min(1, progress / animDuration);
                opacity = animProgress;
                yOffset = (1 - animProgress) * 50; // slide up 50px
            }

            ctx.globalAlpha = opacity;

            // Draw line by line
            const lineHeight = text.fontSize * 1.25;
            const startY = textY - ((lines.length - 1) * lineHeight) / 2;

            let totalCharsDrawn = 0;

            lines.forEach((lineText, lineIdx) => {
                let lineToDraw = lineText;
                
                // Truncate line for typewriter animation
                if (text.animation === 'typewriter') {
                    if (totalCharsDrawn + lineText.length <= charLimit) {
                        lineToDraw = lineText;
                    } else {
                        const drawLength = Math.max(0, charLimit - totalCharsDrawn);
                        lineToDraw = lineText.substring(0, drawLength);
                    }
                    totalCharsDrawn += lineText.length;
                }

                ctx.fillText(lineToDraw, textX, startY + (lineIdx * lineHeight) + yOffset);
            });

            ctx.restore();
        });
    }

    /**
     * Renders a static scene instantly on the canvas
     */
    renderScene(canvas, index) {
        if (index >= 0 && index < this.scenes.length) {
            this.renderFrame(canvas, index, 0.5); // Render scene mid-frame
        }
    }

    /**
     * Starts preview playback on a canvas
     */
    play(canvas) {
        if (this.isPlaying) return;
        this.isPlaying = true;
        
        // Calculate total time
        const totalDuration = this.scenes.reduce((acc, scene) => acc + scene.duration, 0);

        this.playbackStartTime = performance.now() - (this.pausedTime || 0);
        this.pausedTime = 0;

        const loop = (timestamp) => {
            if (!this.isPlaying) return;

            const elapsedSeconds = (timestamp - this.playbackStartTime) / 1000;
            this.currentPlayTime = elapsedSeconds;

            if (elapsedSeconds >= totalDuration) {
                this.stop();
                if (this.onPlaybackEnd) this.onPlaybackEnd();
                return;
            }

            // Find current scene index and scene progress
            let accumulatedTime = 0;
            let currentSceneIdx = 0;
            
            for (let i = 0; i < this.scenes.length; i++) {
                const scene = this.scenes[i];
                if (elapsedSeconds < accumulatedTime + scene.duration) {
                    currentSceneIdx = i;
                    break;
                }
                accumulatedTime += scene.duration;
            }

            const currentScene = this.scenes[currentSceneIdx];
            const timeInCurrentScene = elapsedSeconds - accumulatedTime;
            const progress = timeInCurrentScene / currentScene.duration;

            // Transition logic
            const transitionTime = 0.5; // Half-second transitions
            let prevSceneIdx = -1;
            let transProgress = 0;

            if (currentSceneIdx > 0 && timeInCurrentScene < transitionTime && currentScene.transition !== 'none') {
                prevSceneIdx = currentSceneIdx - 1;
                transProgress = timeInCurrentScene / transitionTime;
            }

            this.renderFrame(canvas, currentSceneIdx, progress, prevSceneIdx, transProgress);

            if (this.onTimeUpdate) {
                this.onTimeUpdate(elapsedSeconds, totalDuration, currentSceneIdx);
            }

            this.animationFrameId = requestAnimationFrame(loop);
        };

        this.animationFrameId = requestAnimationFrame(loop);
    }

    /**
     * Pauses the preview playback
     */
    pause() {
        if (!this.isPlaying) return;
        this.isPlaying = false;
        cancelAnimationFrame(this.animationFrameId);
        this.pausedTime = performance.now() - this.playbackStartTime;
    }

    /**
     * Stops the preview playback completely and resets
     */
    stop() {
        this.isPlaying = false;
        cancelAnimationFrame(this.animationFrameId);
        this.pausedTime = 0;
        this.currentPlayTime = 0;
    }

    /**
     * Generates standard text script templates based on styles & topics
     */
    generateScript(topic, style, duration, platform) {
        const platformLabel = {
            'tiktok': 'TikTok Video',
            'youtube-shorts': 'YouTube Shorts',
            'instagram-reels': 'Instagram Reels',
            'youtube': 'YouTube Video'
        }[platform] || 'Viral Video';

        const introTemplates = [
            `[Scene 1 - Visual: Strong gradient background. Text: The Truth About ${topic}]\nHere is the shocking truth about ${topic} that most experts refuse to tell you...`,
            `[Scene 1 - Visual: Vibrant colors. Text: Stop Doing This!]\nIf you are still trying to master ${topic} the old way, you need to stop immediately. Here is why...`,
            `[Scene 1 - Visual: Sleek minimal typography. Text: Master ${topic} Today]\nWant to know the secret to winning at ${topic}? It's simpler than you think. Let's break it down...`,
            `[Scene 1 - Visual: High contrast. Text: 3 Hacks For ${topic}]\nHere are three simple, science-backed hacks to instantly level up your ${topic} starting today.`
        ];

        const bodyTemplates = [
            `\n\n[Scene 2 - Visual: Highlight card. Text: Hack 1: Consistency]\nFirst, consistency is key. You can't get results unless you make it a daily habit. Even 5 minutes a day makes a difference.`,
            `\n\n[Scene 2 - Visual: Informational chart layout. Text: Step 1: Foundation]\nStep one is to lay down a solid foundation. Focus on the core principles before you try to optimize the small details.`,
            `\n\n[Scene 3 - Visual: Accent highlights. Text: Hack 2: Clear Focus]\nSecond, eliminate all distractions. Choose one clear path and follow it until you succeed. Multi-tasking is the enemy.`,
            `\n\n[Scene 3 - Visual: Dynamic bold text. Text: Step 2: Automation]\nStep two: Automate the boring parts. Use modern tools so you can spend your valuable energy on creative strategy and high-impact tasks.`
        ];

        const ctaTemplates = [
            `\n\n[Scene 4 - Visual: Clean exit design. Text: Follow for more!]\nIf you found this useful, hit that follow button and drop a comment on what topic we should cover next!`,
            `\n\n[Scene 4 - Visual: Vibrant buttons layout. Text: Share & Save!]\nSave this video for later reference and share it with a friend who needs to see this today. Let's win together!`,
            `\n\n[Scene 4 - Visual: Text: Link in Bio!]\nWant to learn the full step-by-step framework? Click the link in my profile bio to get started now!`
        ];

        // Random pick & compile script
        const rand = (arr) => arr[Math.floor(Math.random() * arr.length)];
        const intro = rand(introTemplates);
        const body1 = rand(bodyTemplates);
        const body2 = rand(bodyTemplates);
        const cta = rand(ctaTemplates);

        let finalScript = `// VIEWMAX PRO GENERATED SCRIPT FOR ${platformLabel.toUpperCase()}\n// Style: ${style} | Duration: ${duration}s\n\n` + intro + body1 + body2 + cta;
        return finalScript;
    }

    /**
     * Returns pre-configured templates
     */
    getTemplates() {
        return [
            {
                id: 'motivational',
                name: 'Daily Motivation',
                description: 'Bold text overlays with inspiring gradients for daily quote channels.',
                category: 'motivational',
                icon: '⚡',
                thumbnailGradient: ['#ff6b6b', '#feca57'],
                scenes: [
                    {
                        background: { type: 'gradient', gradient: { from: '#ff6b6b', to: '#feca57', angle: 135 } },
                        texts: [{ content: 'THE HARDER YOU WORK...', x: 0.5, y: 0.5, fontSize: 64, fontFamily: 'Inter', color: '#ffffff', bold: true, align: 'center', animation: 'slideUp' }],
                        duration: 4,
                        transition: 'fade'
                    },
                    {
                        background: { type: 'gradient', gradient: { from: '#f12711', to: '#f5af19', angle: 135 } },
                        texts: [{ content: '...THE LUCKIER YOU GET.', x: 0.5, y: 0.5, fontSize: 64, fontFamily: 'Inter', color: '#ffffff', bold: true, align: 'center', animation: 'fadeIn' }],
                        duration: 4,
                        transition: 'slideLeft'
                    },
                    {
                        background: { type: 'gradient', gradient: { from: '#240b36', to: '#c31432', angle: 135 } },
                        texts: [{ content: 'START TODAY.', x: 0.5, y: 0.5, fontSize: 72, fontFamily: 'Inter', color: '#ffffff', bold: true, align: 'center', animation: 'typewriter' }],
                        duration: 4,
                        transition: 'zoomIn'
                    }
                ]
            },
            {
                id: 'educational',
                name: 'Quick Facts',
                description: 'Sleek dark mode template perfect for educational facts or trivia channel.',
                category: 'educational',
                icon: '📚',
                thumbnailGradient: ['#1a1a2e', '#16213e'],
                scenes: [
                    {
                        background: { type: 'gradient', gradient: { from: '#1a1a2e', to: '#16213e', angle: 135 } },
                        texts: [{ content: '3 Mindblowing Space Facts 🪐', x: 0.5, y: 0.5, fontSize: 54, fontFamily: 'Inter', color: '#ffffff', bold: true, align: 'center', animation: 'fadeIn' }],
                        duration: 5,
                        transition: 'fade'
                    },
                    {
                        background: { type: 'gradient', gradient: { from: '#0f0c20', to: '#201a30', angle: 135 } },
                        texts: [{ content: '1. One day on Venus is longer than a year on Earth.', x: 0.5, y: 0.5, fontSize: 48, fontFamily: 'Inter', color: '#00cec9', bold: true, align: 'center', animation: 'slideUp' }],
                        duration: 5,
                        transition: 'slideLeft'
                    },
                    {
                        background: { type: 'gradient', gradient: { from: '#020024', to: '#090979', angle: 135 } },
                        texts: [{ content: '2. Sound cannot travel in space because there is no atmosphere.', x: 0.5, y: 0.5, fontSize: 44, fontFamily: 'Inter', color: '#fd79a8', bold: true, align: 'center', animation: 'typewriter' }],
                        duration: 5,
                        transition: 'zoomIn'
                    }
                ]
            },
            {
                id: 'product',
                name: 'SaaS Showcase',
                description: 'Show off your application benefits with premium modern gradients.',
                category: 'product',
                icon: '💻',
                thumbnailGradient: ['#6C5CE7', '#a855f7'],
                scenes: [
                    {
                        background: { type: 'gradient', gradient: { from: '#6C5CE7', to: '#a855f7', angle: 135 } },
                        texts: [{ content: 'Launch Your Business Faster 🚀', x: 0.5, y: 0.5, fontSize: 56, fontFamily: 'Inter', color: '#ffffff', bold: true, align: 'center', animation: 'fadeIn' }],
                        duration: 4,
                        transition: 'fade'
                    },
                    {
                        background: { type: 'gradient', gradient: { from: '#00b894', to: '#00cec9', angle: 135 } },
                        texts: [{ content: 'Automate 90% of your workflow.', x: 0.5, y: 0.5, fontSize: 48, fontFamily: 'Inter', color: '#ffffff', bold: true, align: 'center', animation: 'slideUp' }],
                        duration: 4,
                        transition: 'slideLeft'
                    },
                    {
                        background: { type: 'gradient', gradient: { from: '#fd79a8', to: '#e84393', angle: 135 } },
                        texts: [{ content: 'Get started for free today!', x: 0.5, y: 0.5, fontSize: 52, fontFamily: 'Inter', color: '#ffffff', bold: true, align: 'center', animation: 'zoomIn' }],
                        duration: 4,
                        transition: 'fade'
                    }
                ]
            }
        ];
    }

    /**
     * Loads a pre-built template
     */
    loadTemplate(templateId) {
        const templates = this.getTemplates();
        const template = templates.find(t => t.id === templateId);
        if (template) {
            // Create deep copy of template scenes
            this.scenes = JSON.parse(JSON.stringify(template.scenes));
        }
    }

    /**
     * Browser Web Speech Synthesis Voice List
     */
    getAvailableVoices() {
        if (typeof window !== 'undefined' && window.speechSynthesis) {
            return window.speechSynthesis.getVoices();
        }
        return [];
    }

    /**
     * Simple Voiceover preview speaker
     */
    speakText(text, options = {}) {
        if (typeof window === 'undefined' || !window.speechSynthesis) return;
        window.speechSynthesis.cancel(); // Stop current speech
        
        const utterance = new SpeechSynthesisUtterance(text);
        const voices = this.getAvailableVoices();
        
        if (options.voice) {
            const foundVoice = voices.find(v => v.name === options.voice);
            if (foundVoice) utterance.voice = foundVoice;
        }
        
        utterance.rate = options.rate || 1.0;
        utterance.pitch = options.pitch || 1.0;
        
        window.speechSynthesis.speak(utterance);
    }

    /**
     * Browser Canvas Video Export (creates actual WebM video)
     */
    exportVideo(canvas, options = {}) {
        return new Promise((resolve, reject) => {
            const fps = options.fps || 30;
            const bitRate = options.videoBitsPerSecond || 2500000;
            const onProgress = options.onExportProgress || null;

            // Generate total frames
            const totalDuration = this.scenes.reduce((acc, scene) => acc + scene.duration, 0);
            const totalFrames = Math.ceil(totalDuration * fps);
            
            // Set up Canvas Capture Stream
            const stream = canvas.captureStream(fps);
            let mediaRecorder;

            try {
                mediaRecorder = new MediaRecorder(stream, {
                    mimeType: 'video/webm;codecs=vp9,opus',
                    videoBitsPerSecond: bitRate
                });
            } catch (e) {
                try {
                    mediaRecorder = new MediaRecorder(stream, {
                        mimeType: 'video/webm',
                        videoBitsPerSecond: bitRate
                    });
                } catch (err) {
                    return reject(new Error('MediaRecorder not supported in this browser.'));
                }
            }

            const chunks = [];
            mediaRecorder.ondataavailable = (e) => {
                if (e.data && e.data.size > 0) {
                    chunks.push(e.data);
                }
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: 'video/webm' });
                resolve(blob);
            };

            // Start recording
            mediaRecorder.start();

            // Frame-by-frame rendering loop to record exact frames
            let currentFrame = 0;
            
            const recordFrame = () => {
                if (currentFrame >= totalFrames) {
                    mediaRecorder.stop();
                    return;
                }

                const elapsedSeconds = currentFrame / fps;
                
                // Find scene index
                let accumulatedTime = 0;
                let currentSceneIdx = 0;
                for (let i = 0; i < this.scenes.length; i++) {
                    const scene = this.scenes[i];
                    if (elapsedSeconds < accumulatedTime + scene.duration) {
                        currentSceneIdx = i;
                        break;
                    }
                    accumulatedTime += scene.duration;
                }

                const currentScene = this.scenes[currentSceneIdx];
                const timeInCurrentScene = elapsedSeconds - accumulatedTime;
                const progress = timeInCurrentScene / currentScene.duration;

                // Transition logic
                const transitionTime = 0.5;
                let prevSceneIdx = -1;
                let transProgress = 0;
                if (currentSceneIdx > 0 && timeInCurrentScene < transitionTime && currentScene.transition !== 'none') {
                    prevSceneIdx = currentSceneIdx - 1;
                    transProgress = timeInCurrentScene / transitionTime;
                }

                this.renderFrame(canvas, currentSceneIdx, progress, prevSceneIdx, transProgress);

                currentFrame++;
                if (onProgress) {
                    onProgress((currentFrame / totalFrames) * 100);
                }

                // Small delay to let canvas capture
                setTimeout(recordFrame, 1000 / fps);
            };

            // Start recording loops
            recordFrame();
        });
    }

    /**
     * Draws an animated cartoon background on the canvas
     */
    drawCartoonBackground(ctx, theme, width, height, progress) {
        ctx.save();
        
        // Define a simple hash function to get deterministic layout based on current scene duration/id
        const hash = (str) => {
            let h = 17957;
            for (let i = 0; i < str.length; i++) {
                h = (h << 5) - h + str.charCodeAt(i);
                h |= 0;
            }
            return Math.abs(h);
        };
        
        const seed = hash(theme + (this.scenes[0]?.id || 'scene'));

        if (theme === 'space') {
            // Space background
            ctx.fillStyle = '#0a0a1e';
            ctx.fillRect(0, 0, width, height);

            // Draw nebula clouds (gradients)
            ctx.globalAlpha = 0.35;
            const nebColors = ['#6c5ce7', '#fd79a8', '#00cec9'];
            for (let i = 0; i < 3; i++) {
                const cloudX = width * (0.25 + 0.25 * i);
                const cloudY = height * (0.3 + 0.2 * ((seed + i) % 3));
                const rad = width * 0.3;
                const cloudGrad = ctx.createRadialGradient(cloudX, cloudY, 0, cloudX, cloudY, rad);
                cloudGrad.addColorStop(0, nebColors[i]);
                cloudGrad.addColorStop(1, 'transparent');
                ctx.fillStyle = cloudGrad;
                ctx.beginPath();
                ctx.arc(cloudX, cloudY, rad, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.globalAlpha = 1.0;

            // Twinkling stars
            ctx.fillStyle = '#ffffff';
            for (let i = 0; i < 40; i++) {
                const starX = ((seed * (i + 13)) % width);
                const starY = ((seed * (i + 47)) % height);
                const starOffset = (i * 0.5);
                const scale = 0.4 + 0.6 * Math.sin(progress * 15 + starOffset);
                const starSize = ((seed + i) % 3 + 1) * scale;
                ctx.beginPath();
                ctx.arc(starX, starY, Math.max(0.5, starSize), 0, Math.PI * 2);
                ctx.fill();
            }

            // Draw a cute cartoon astronaut
            const astroX = width * 0.5;
            const astroY = height * 0.5 + Math.sin(progress * Math.PI * 2) * 24;

            ctx.save();
            ctx.translate(astroX, astroY);
            ctx.rotate(Math.sin(progress * Math.PI) * 0.05);

            // Backpack (Oxygen tank)
            ctx.fillStyle = '#dcdde1';
            ctx.beginPath();
            ctx.roundRect(-35, -20, 20, 50, 6);
            ctx.fill();

            // Suit body
            ctx.fillStyle = '#f5f6fa';
            ctx.beginPath();
            ctx.roundRect(-25, -25, 50, 55, 15);
            ctx.fill();

            // Orange stripes on arms/legs
            ctx.fillStyle = '#ff7f50';
            ctx.fillRect(-22, -15, 6, 4);
            ctx.fillRect(16, -15, 6, 4);

            // Left Arm (waving)
            ctx.save();
            ctx.translate(-25, -15);
            ctx.rotate(0.5 + Math.sin(progress * 14) * 0.3);
            ctx.fillStyle = '#f5f6fa';
            ctx.beginPath();
            ctx.roundRect(-10, -25, 12, 30, 6);
            ctx.fill();
            // glove
            ctx.fillStyle = '#7f8c8d';
            ctx.beginPath();
            ctx.arc(-4, -25, 6, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Right Arm (resting)
            ctx.save();
            ctx.translate(25, -15);
            ctx.rotate(-0.5);
            ctx.fillStyle = '#f5f6fa';
            ctx.beginPath();
            ctx.roundRect(-2, -5, 12, 30, 6);
            ctx.fill();
            ctx.restore();

            // Legs
            ctx.fillStyle = '#f5f6fa';
            ctx.beginPath();
            ctx.roundRect(-20, 25, 15, 20, 6);
            ctx.roundRect(5, 25, 15, 20, 6);
            ctx.fill();

            // Helmet
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(0, -35, 28, 0, Math.PI * 2);
            ctx.fill();
            // Helmet border/details
            ctx.strokeStyle = '#dcdde1';
            ctx.lineWidth = 3;
            ctx.stroke();

            // Visor (faceplate)
            ctx.fillStyle = '#2f3542';
            ctx.beginPath();
            ctx.roundRect(-18, -45, 36, 22, 8);
            ctx.fill();
            // Visor reflection
            ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
            ctx.beginPath();
            ctx.ellipse(-8, -39, 6, 3, Math.PI / 4, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();

        } else if (theme === 'forest') {
            // Fantasy Forest sky
            const skyGrad = ctx.createLinearGradient(0, 0, 0, height);
            skyGrad.addColorStop(0, '#ffeaa7');
            skyGrad.addColorStop(1, '#ff9f43');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, width, height);

            // Drifting Clouds
            ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
            for (let i = 0; i < 3; i++) {
                const cloudSpeed = 80 + i * 40;
                const cloudX = ((seed + progress * cloudSpeed) % (width + 200)) - 100;
                const cloudY = height * (0.15 + i * 0.1);
                const cloudW = 100 + i * 30;
                ctx.beginPath();
                ctx.roundRect(cloudX, cloudY, cloudW, 30, 15);
                ctx.fill();
            }

            // Mountain Silhouettes
            ctx.fillStyle = '#10ac84';
            ctx.beginPath();
            ctx.moveTo(0, height);
            ctx.lineTo(width * 0.2, height * 0.55);
            ctx.lineTo(width * 0.4, height * 0.75);
            ctx.lineTo(width * 0.65, height * 0.5);
            ctx.lineTo(width * 0.9, height * 0.7);
            ctx.lineTo(width, height * 0.6);
            ctx.lineTo(width, height);
            ctx.closePath();
            ctx.fill();

            // Forest Front Trees
            ctx.fillStyle = '#0a3d62';
            const numTrees = 12;
            for (let i = 0; i <= numTrees; i++) {
                const treeX = (width / numTrees) * i + Math.sin(i * 123) * 20;
                const treeH = height * 0.35 + Math.sin(i * 543) * 50;
                const treeY = height - treeH;
                
                // Trunk
                ctx.fillStyle = '#576574';
                ctx.fillRect(treeX - 4, treeY + treeH * 0.5, 8, treeH * 0.5);
                
                // Leaves (Triangle layers)
                ctx.fillStyle = '#0f8a5f';
                ctx.beginPath();
                ctx.moveTo(treeX, treeY);
                ctx.lineTo(treeX - 35, treeY + treeH * 0.4);
                ctx.lineTo(treeX + 35, treeY + treeH * 0.4);
                ctx.closePath();
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(treeX, treeY + treeH * 0.2);
                ctx.lineTo(treeX - 45, treeY + treeH * 0.65);
                ctx.lineTo(treeX + 45, treeY + treeH * 0.65);
                ctx.closePath();
                ctx.fill();
            }

            // Cute bouncing animal (Fox/Cat)
            const animalX = width * 0.5;
            // Bounce Math.abs(Math.sin)
            const bounceY = Math.abs(Math.sin(progress * Math.PI * 3.5)) * -30;
            const animalY = height * 0.8 + bounceY;

            ctx.save();
            ctx.translate(animalX, animalY);

            // Tail
            ctx.save();
            ctx.translate(15, 0);
            ctx.rotate(Math.sin(progress * 15) * 0.3);
            ctx.fillStyle = '#ff7f50';
            ctx.beginPath();
            ctx.ellipse(10, -5, 18, 8, Math.PI / 6, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Body
            ctx.fillStyle = '#ff6b6b';
            ctx.beginPath();
            ctx.arc(0, -10, 22, 0, Math.PI * 2);
            ctx.fill();

            // Head
            ctx.beginPath();
            ctx.arc(0, -32, 18, 0, Math.PI * 2);
            ctx.fill();

            // Ears
            ctx.fillStyle = '#ff4757';
            ctx.beginPath();
            // Left Ear
            ctx.moveTo(-16, -38);
            ctx.lineTo(-24, -58);
            ctx.lineTo(-4, -46);
            ctx.closePath();
            ctx.fill();
            // Right Ear
            ctx.beginPath();
            ctx.moveTo(16, -38);
            ctx.lineTo(24, -58);
            ctx.lineTo(4, -46);
            ctx.closePath();
            ctx.fill();

            // Inner ears (pink)
            ctx.fillStyle = '#ff9ff3';
            ctx.beginPath();
            ctx.moveTo(-13, -40);
            ctx.lineTo(-20, -53);
            ctx.lineTo(-5, -45);
            ctx.closePath();
            ctx.fill();
            ctx.beginPath();
            ctx.moveTo(13, -40);
            ctx.lineTo(20, -53);
            ctx.lineTo(5, -45);
            ctx.closePath();
            ctx.fill();

            // Face details (Eyes/Nose)
            ctx.fillStyle = '#2f3542';
            ctx.beginPath();
            ctx.arc(-6, -32, 2, 0, Math.PI * 2);
            ctx.arc(6, -32, 2, 0, Math.PI * 2);
            ctx.fill();
            // Cheeks
            ctx.fillStyle = '#ff9ff3';
            ctx.beginPath();
            ctx.arc(-11, -28, 3, 0, Math.PI * 2);
            ctx.arc(11, -28, 3, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();

            // Falling Leaves
            ctx.fillStyle = '#ff9f43';
            for (let i = 0; i < 8; i++) {
                const leafSpeedX = 60 + i * 20;
                const leafSpeedY = 120 + i * 30;
                const leafX = ((seed + i * 153 + progress * leafSpeedX) % (width + 50)) - 25;
                const leafY = ((seed + i * 345 + progress * leafSpeedY) % (height + 50)) - 25;
                ctx.save();
                ctx.translate(leafX, leafY);
                ctx.rotate(progress * 4 + i);
                ctx.beginPath();
                ctx.ellipse(0, 0, 8, 4, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }

        } else if (theme === 'ocean') {
            // Retro sunset ocean gradient
            const skyGrad = ctx.createLinearGradient(0, 0, 0, height);
            skyGrad.addColorStop(0, '#5f27cd');
            skyGrad.addColorStop(0.5, '#ff4757');
            skyGrad.addColorStop(1, '#ff9f43');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, width, height);

            // Giant Neon Sun
            const sunX = width * 0.5;
            const sunY = height * 0.65;
            const sunR = width * 0.15;
            const sunGrad = ctx.createLinearGradient(0, sunY - sunR, 0, sunY);
            sunGrad.addColorStop(0, '#feca57');
            sunGrad.addColorStop(1, '#ff4757');
            ctx.fillStyle = sunGrad;
            ctx.beginPath();
            ctx.arc(sunX, sunY, sunR, Math.PI, 0); // half circle above horizon
            ctx.fill();

            // Sun Retro Stripes (horizontal slits)
            ctx.fillStyle = '#ff4757';
            for (let i = 1; i <= 6; i++) {
                const stripeY = sunY - (i * 12);
                const stripeH = 2.5 * i;
                ctx.fillRect(sunX - sunR, stripeY, sunR * 2, stripeH);
            }

            // Draw a cute bobbing yellow submarine
            const subX = width * 0.5;
            const subY = height * 0.72 + Math.sin(progress * Math.PI * 2.5) * 15;

            ctx.save();
            ctx.translate(subX, subY);
            ctx.rotate(Math.sin(progress * Math.PI * 2) * 0.05);

            // Propeller
            ctx.save();
            ctx.translate(-35, 0);
            ctx.rotate(progress * 40);
            ctx.fillStyle = '#95afc0';
            ctx.fillRect(-4, -12, 8, 24);
            ctx.restore();

            // Propeller shaft
            ctx.fillStyle = '#57606f';
            ctx.fillRect(-35, -3, 8, 6);

            // Submarine hull (yellow capsule)
            ctx.fillStyle = '#ffc048';
            ctx.beginPath();
            ctx.roundRect(-30, -18, 60, 36, 18);
            ctx.fill();
            // Outlines
            ctx.strokeStyle = '#e57e25';
            ctx.lineWidth = 2.5;
            ctx.stroke();

            // Periscope
            ctx.fillStyle = '#57606f';
            ctx.fillRect(-5, -28, 6, 12);
            ctx.fillRect(-5, -32, 12, 6);

            // Windows (Port holes)
            ctx.fillStyle = '#00d2d3';
            ctx.beginPath();
            ctx.arc(-10, 0, 7, 0, Math.PI * 2);
            ctx.arc(10, 0, 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#e57e25';
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.restore();

            // Layers of waves
            const drawWave = (waveY, color, speed, amp, freq) => {
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.moveTo(0, height);
                ctx.lineTo(0, waveY);
                for (let x = 0; x <= width; x += 10) {
                    const y = waveY + Math.sin(x * freq + progress * speed) * amp;
                    ctx.lineTo(x, y);
                }
                ctx.lineTo(width, height);
                ctx.closePath();
                ctx.fill();
            };

            // Back wave
            drawWave(height * 0.74, '#2e86de', 6, 8, 0.01);
            // Mid wave
            drawWave(height * 0.78, '#1b1464', -8, 12, 0.015);
            // Front wave
            drawWave(height * 0.83, '#0652dd', 10, 6, 0.02);
        }

        ctx.restore();
    }
}

// Export global class
window.VideoEngine = VideoEngine;
