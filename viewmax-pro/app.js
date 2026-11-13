/**
 * ViewMax Pro — Main Application Controller
 * Handles routing, UI interactions, and integrates with VideoEngine
 */

// ============================================================
// GLOBALS
// ============================================================
let engine;
let currentPage = 'home';
let currentSceneIndex = 0;
let isPlaying = false;
let selectedTextIndex = 0;

// ============================================================
// INITIALIZATION
// ============================================================
function init() {
    engine = new VideoEngine();
    initRouter();
    initSidebar();
    initStudio();
    initTimelineEditor();
    initScriptGenerator();
    initVoiceover();
    initCaptions();
    initTemplates();
    initFeaturedPreview();
    renderCurrentScene();
    showToast('Welcome to ViewMax Pro! 🎬', 'success');
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// ============================================================
// TOAST NOTIFICATIONS
// ============================================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icons = {
        success: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M20 6L9 17l-5-5"/></svg>',
        error: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
        info: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
    };
    toast.innerHTML = `${icons[type] || icons.info}<span>${message}</span>`;
    container.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Make showToast globally accessible for inline onclick handlers
window.showToast = showToast;

// ============================================================
// ROUTER / PAGE NAVIGATION
// ============================================================
function initRouter() {
    // Sidebar nav
    document.querySelectorAll('[data-page]').forEach(el => {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(el.dataset.page);
        });
    });
}

function navigateTo(page) {
    if (page === currentPage) return;

    // Stop playback if leaving editor
    if (currentPage === 'scene-editor' && isPlaying) {
        engine.stop();
        isPlaying = false;
        updatePlayButton();
    }

    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));

    // Show target page
    const targetPage = document.getElementById(`page-${page}`);
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // Update sidebar nav
    document.querySelectorAll('.sidebar-nav-item').forEach(n => n.classList.remove('active'));
    const activeNav = document.querySelector(`.sidebar-nav-item[data-page="${page}"]`);
    if (activeNav) activeNav.classList.add('active');

    // Update bottom nav
    document.querySelectorAll('.bottom-nav-item').forEach(n => n.classList.remove('active'));
    const activeBottom = document.querySelector(`.bottom-nav-item[data-page="${page}"]`);
    if (activeBottom) activeBottom.classList.add('active');

    // Update page title
    const titles = {
        'home': 'Home',
        'video-editor': 'AI Studio',
        'scene-editor': 'Timeline Editor',
        'script-generator': 'AI Script Writer',
        'voiceover': 'AI Voiceover',
        'captions': 'Auto Captions',
        'templates': 'Templates',
        'settings': 'Settings'
    };
    document.getElementById('pageTitle').textContent = titles[page] || 'Home';

    currentPage = page;

    // Re-render canvas when entering timeline editor
    if (page === 'scene-editor') {
        setTimeout(() => renderCurrentScene(), 50);
    }

    // Close mobile sidebar
    closeSidebar();
}

// ============================================================
// SIDEBAR
// ============================================================
function initSidebar() {
    const hamburger = document.getElementById('hamburgerBtn');
    const overlay = document.getElementById('sidebarOverlay');
    const toggleBtn = document.getElementById('sidebarToggleBtn');

    hamburger?.addEventListener('click', openSidebar);
    overlay?.addEventListener('click', closeSidebar);
    
    // Sidebar collapse toggle for desktop
    toggleBtn?.addEventListener('click', () => {
        const shell = document.getElementById('appShell');
        shell?.classList.toggle('sidebar-collapsed');
    });

    // Create new video button
    document.getElementById('btnCreateNew')?.addEventListener('click', () => {
        engine.scenes = [];
        engine.addScene();
        currentSceneIndex = 0;
        navigateTo('scene-editor');
        renderCurrentScene();
        renderTimeline();
        showToast('New video project created!', 'success');
    });
}

function openSidebar() {
    document.getElementById('sidebar')?.classList.add('open');
    document.getElementById('sidebarOverlay')?.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeSidebar() {
    document.getElementById('sidebar')?.classList.remove('open');
    document.getElementById('sidebarOverlay')?.classList.remove('active');
    document.body.style.overflow = '';
}

// ============================================================
// TIMELINE EDITOR
// ============================================================
function initTimelineEditor() {
    const canvas = document.getElementById('videoCanvas');

    // Aspect ratio toggle
    document.querySelectorAll('.aspect-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.aspect-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const ratio = btn.dataset.ratio;
            if (ratio === '16:9') {
                canvas.width = 1920; canvas.height = 1080;
            } else {
                canvas.width = 1080; canvas.height = 1920;
            }
            document.getElementById('canvasWrapper').setAttribute('data-ratio', ratio);
            renderCurrentScene();
        });
    });

    // Tab switching
    document.querySelectorAll('.controls-tabs .tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.controls-tabs .tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
        });
    });

    // Background controls
    initBackgroundControls();

    // Text controls
    initTextControls();

    // Scene controls
    initSceneControls();

    // Playback controls
    initPlaybackControls();

    // Export
    initExport();

    // Initial timeline render
    renderTimeline();
    
    // Add editor script generator listener
    initEditorScriptTab();

    // Canvas click focuses the Text editing tab directly
    canvas.addEventListener('click', () => {
        document.querySelector('.tab-btn[data-tab="text"]')?.click();
        document.getElementById('textContent')?.focus();
    });
}

function initBackgroundControls() {
    const bgType = document.getElementById('bgType');
    bgType.addEventListener('change', () => {
        const type = bgType.value;
        document.getElementById('bgSolidGroup').style.display = type === 'solid' ? '' : 'none';
        document.getElementById('bgGradientGroup').style.display = type === 'gradient' ? '' : 'none';
        document.getElementById('bgImageGroup').style.display = type === 'image' ? '' : 'none';
        document.getElementById('bgCartoonGroup').style.display = type === 'cartoon' ? '' : 'none';
        document.getElementById('bgVideoGroup').style.display = type === 'video' ? '' : 'none';
        updateSceneBackground();
    });

    document.getElementById('bgCartoonTheme').addEventListener('change', updateSceneBackground);
    document.getElementById('bgVideoUrl').addEventListener('input', updateSceneBackground);

    // Solid color
    document.getElementById('bgSolidColor').addEventListener('input', (e) => {
        document.getElementById('bgSolidColorText').value = e.target.value;
        updateSceneBackground();
    });
    document.getElementById('bgSolidColorText').addEventListener('change', (e) => {
        document.getElementById('bgSolidColor').value = e.target.value;
        updateSceneBackground();
    });

    // Gradient
    document.getElementById('bgGradFrom').addEventListener('input', updateSceneBackground);
    document.getElementById('bgGradTo').addEventListener('input', updateSceneBackground);
    document.getElementById('bgGradAngle').addEventListener('input', (e) => {
        document.getElementById('bgGradAngleVal').textContent = e.target.value + '°';
        updateSceneBackground();
    });

    // Preset swatches
    document.querySelectorAll('.preset-swatch').forEach(swatch => {
        swatch.addEventListener('click', () => {
            document.getElementById('bgGradFrom').value = swatch.dataset.from;
            document.getElementById('bgGradTo').value = swatch.dataset.to;
            document.getElementById('bgType').value = 'gradient';
            document.getElementById('bgSolidGroup').style.display = 'none';
            document.getElementById('bgGradientGroup').style.display = '';
            document.getElementById('bgImageGroup').style.display = 'none';
            updateSceneBackground();
        });
    });

    // Image upload
    document.getElementById('bgImageUpload').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                const scene = engine.scenes[currentSceneIndex];
                if (scene) {
                    scene.background = { type: 'image', imageUrl: ev.target.result };
                    renderCurrentScene();
                }
            };
            reader.readAsDataURL(file);
        }
    });
}

function updateSceneBackground() {
    const scene = engine.scenes[currentSceneIndex];
    if (!scene) return;

    const type = document.getElementById('bgType').value;
    if (type === 'solid') {
        scene.background = { type: 'solid', color: document.getElementById('bgSolidColor').value };
    } else if (type === 'gradient') {
        scene.background = {
            type: 'gradient',
            gradient: {
                from: document.getElementById('bgGradFrom').value,
                to: document.getElementById('bgGradTo').value,
                angle: parseInt(document.getElementById('bgGradAngle').value)
            }
        };
    } else if (type === 'cartoon') {
        scene.background = {
            type: 'cartoon',
            theme: document.getElementById('bgCartoonTheme').value
        };
    } else if (type === 'video') {
        scene.background = {
            type: 'video',
            videoUrl: document.getElementById('bgVideoUrl').value.trim()
        };
    }
    renderCurrentScene();
    renderTimeline();
}

function initTextControls() {
    // Update text on any control change
    const textInputs = ['textContent', 'textFont', 'textSize', 'textColor', 'textBold', 'textItalic', 'textAlign', 'textAnimation'];
    textInputs.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        const event = el.type === 'checkbox' ? 'change' : 'input';
        el.addEventListener(event, updateSceneText);
    });

    // Position buttons
    document.querySelectorAll('.pos-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.pos-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            updateSceneText();
        });
    });

    // Add text layer
    document.getElementById('addTextBtn').addEventListener('click', () => {
        const scene = engine.scenes[currentSceneIndex];
        if (!scene) return;
        scene.texts.push({
            content: 'New Text',
            x: 0.5, y: 0.5 + (scene.texts.length * 0.15),
            fontSize: 48,
            fontFamily: 'Inter',
            color: '#ffffff',
            bold: false,
            italic: false,
            align: 'center',
            animation: 'fadeIn'
        });
        selectedTextIndex = scene.texts.length - 1;
        loadTextControls();
        renderCurrentScene();
        showToast('Text layer added!', 'info');
    });
}

function updateSceneText() {
    const scene = engine.scenes[currentSceneIndex];
    if (!scene || !scene.texts[selectedTextIndex]) return;

    const activePos = document.querySelector('.pos-btn.active');
    scene.texts[selectedTextIndex] = {
        content: document.getElementById('textContent').value,
        x: activePos ? parseFloat(activePos.dataset.x) : 0.5,
        y: activePos ? parseFloat(activePos.dataset.y) : 0.5,
        fontSize: parseInt(document.getElementById('textSize').value),
        fontFamily: document.getElementById('textFont').value,
        color: document.getElementById('textColor').value,
        bold: document.getElementById('textBold').checked,
        italic: document.getElementById('textItalic').checked,
        align: document.getElementById('textAlign').value,
        animation: document.getElementById('textAnimation').value
    };
    renderCurrentScene();
}

function loadTextControls() {
    const scene = engine.scenes[currentSceneIndex];
    if (!scene) return;
    const text = scene.texts[selectedTextIndex] || scene.texts[0];
    if (!text) return;

    document.getElementById('textContent').value = text.content;
    document.getElementById('textFont').value = text.fontFamily;
    document.getElementById('textSize').value = text.fontSize;
    document.getElementById('textColor').value = text.color;
    document.getElementById('textBold').checked = text.bold;
    document.getElementById('textItalic').checked = text.italic;
    document.getElementById('textAlign').value = text.align;
    document.getElementById('textAnimation').value = text.animation;

    // Update position button
    document.querySelectorAll('.pos-btn').forEach(btn => {
        const bx = parseFloat(btn.dataset.x);
        const by = parseFloat(btn.dataset.y);
        btn.classList.toggle('active', Math.abs(bx - text.x) < 0.1 && Math.abs(by - text.y) < 0.1);
    });
}

function initSceneControls() {
    // Duration
    document.getElementById('sceneDuration').addEventListener('input', (e) => {
        document.getElementById('sceneDurationVal').textContent = e.target.value + 's';
        const scene = engine.scenes[currentSceneIndex];
        if (scene) {
            scene.duration = parseInt(e.target.value);
            updateTimeDisplay();
            renderTimeline();
        }
    });

    // Transition
    document.getElementById('sceneTransition').addEventListener('change', (e) => {
        const scene = engine.scenes[currentSceneIndex];
        if (scene) scene.transition = e.target.value;
    });

    // Delete scene
    document.getElementById('deleteSceneBtn').addEventListener('click', () => {
        if (engine.scenes.length <= 1) {
            showToast('Cannot delete the only scene', 'error');
            return;
        }
        engine.removeScene(currentSceneIndex);
        if (currentSceneIndex >= engine.scenes.length) {
            currentSceneIndex = engine.scenes.length - 1;
        }
        renderCurrentScene();
        renderTimeline();
        loadSceneControls();
        loadTextControls();
        showToast('Scene deleted', 'info');
    });

    // Add scene
    document.getElementById('addSceneBtn').addEventListener('click', () => {
        engine.addScene();
        currentSceneIndex = engine.scenes.length - 1;
        renderCurrentScene();
        renderTimeline();
        loadSceneControls();
        loadTextControls();
        showToast('New scene added!', 'success');
    });
}

function loadSceneControls() {
    const scene = engine.scenes[currentSceneIndex];
    if (!scene) return;

    document.getElementById('sceneDuration').value = scene.duration;
    document.getElementById('sceneDurationVal').textContent = scene.duration + 's';
    document.getElementById('sceneTransition').value = scene.transition;

    // Background
    const bg = scene.background;
    document.getElementById('bgType').value = bg.type;
    document.getElementById('bgSolidGroup').style.display = bg.type === 'solid' ? '' : 'none';
    document.getElementById('bgGradientGroup').style.display = bg.type === 'gradient' ? '' : 'none';
    document.getElementById('bgImageGroup').style.display = bg.type === 'image' ? '' : 'none';
    document.getElementById('bgCartoonGroup').style.display = bg.type === 'cartoon' ? '' : 'none';
    document.getElementById('bgVideoGroup').style.display = bg.type === 'video' ? '' : 'none';

    if (bg.type === 'solid') {
        document.getElementById('bgSolidColor').value = bg.color;
        document.getElementById('bgSolidColorText').value = bg.color;
    } else if (bg.type === 'gradient' && bg.gradient) {
        document.getElementById('bgGradFrom').value = bg.gradient.from;
        document.getElementById('bgGradTo').value = bg.gradient.to;
        document.getElementById('bgGradAngle').value = bg.gradient.angle;
        document.getElementById('bgGradAngleVal').textContent = bg.gradient.angle + '°';
    } else if (bg.type === 'cartoon') {
        document.getElementById('bgCartoonTheme').value = bg.theme || 'space';
    } else if (bg.type === 'video') {
        document.getElementById('bgVideoUrl').value = bg.videoUrl || '';
    }
}

// ============================================================
// PLAYBACK
// ============================================================
function initPlaybackControls() {
    document.getElementById('playBtn').addEventListener('click', togglePlay);
    document.getElementById('prevSceneBtn').addEventListener('click', () => {
        if (currentSceneIndex > 0) {
            currentSceneIndex--;
            renderCurrentScene();
            renderTimeline();
            loadSceneControls();
            loadTextControls();
        }
    });
    document.getElementById('nextSceneBtn').addEventListener('click', () => {
        if (currentSceneIndex < engine.scenes.length - 1) {
            currentSceneIndex++;
            renderCurrentScene();
            renderTimeline();
            loadSceneControls();
            loadTextControls();
        }
    });
}

function togglePlay() {
    const canvas = document.getElementById('videoCanvas');
    if (isPlaying) {
        engine.pause();
        isPlaying = false;
    } else {
        engine.onTimeUpdate = (currentTime, totalDuration, sceneIdx) => {
            currentSceneIndex = sceneIdx;
            updateTimeDisplay(currentTime, totalDuration);
            const progress = totalDuration > 0 ? (currentTime / totalDuration) * 100 : 0;
            document.getElementById('progressBar').style.width = progress + '%';
            highlightTimelineScene(sceneIdx);
        };
        engine.onPlaybackEnd = () => {
            isPlaying = false;
            updatePlayButton();
            updateTimeDisplay(0, getTotalDuration());
            document.getElementById('progressBar').style.width = '0%';
            currentSceneIndex = 0;
            renderCurrentScene();
            renderTimeline();
        };
        engine.play(canvas);
        isPlaying = true;
    }
    updatePlayButton();
}

function updatePlayButton() {
    const playIcon = document.querySelector('.play-icon');
    const pauseIcon = document.querySelector('.pause-icon');
    if (isPlaying) {
        playIcon.style.display = 'none';
        pauseIcon.style.display = '';
    } else {
        playIcon.style.display = '';
        pauseIcon.style.display = 'none';
    }
}

function getTotalDuration() {
    return engine.scenes.reduce((sum, s) => sum + s.duration, 0);
}

function updateTimeDisplay(current, total) {
    if (current === undefined) {
        current = 0;
        total = getTotalDuration();
    }
    const fmt = (s) => {
        const m = Math.floor(s / 60);
        const sec = Math.floor(s % 60);
        return `${m}:${sec.toString().padStart(2, '0')}`;
    };
    document.getElementById('timeDisplay').textContent = `${fmt(current)} / ${fmt(total)}`;
}

// ============================================================
// TIMELINE
// ============================================================
function renderTimeline() {
    const timeline = document.getElementById('sceneTimeline');
    timeline.innerHTML = '';

    engine.scenes.forEach((scene, i) => {
        const thumb = document.createElement('div');
        thumb.className = `scene-thumb ${i === currentSceneIndex ? 'active' : ''}`;
        const isVideo = scene.background.type === 'video';
        thumb.innerHTML = `
            <div class="scene-thumb-preview" style="${getSceneBgCSS(scene)}; display:flex; align-items:center; justify-content:center;">
                <span class="scene-num">${i + 1}</span>
                ${isVideo ? '<span style="font-size: 16px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">🎥</span>' : ''}
            </div>
            <span class="scene-dur">${scene.duration}s</span>
        `;
        thumb.addEventListener('click', () => {
            if (isPlaying) {
                engine.stop();
                isPlaying = false;
                updatePlayButton();
            }
            currentSceneIndex = i;
            renderCurrentScene();
            renderTimeline();
            loadSceneControls();
            loadTextControls();
        });
        timeline.appendChild(thumb);
    });

    updateTimeDisplay();
}

function highlightTimelineScene(idx) {
    document.querySelectorAll('.scene-thumb').forEach((t, i) => {
        t.classList.toggle('active', i === idx);
    });
}

function getSceneBgCSS(scene) {
    const bg = scene.background;
    if (bg.type === 'solid') return `background:${bg.color}`;
    if (bg.type === 'gradient' && bg.gradient) {
        return `background:linear-gradient(${bg.gradient.angle}deg, ${bg.gradient.from}, ${bg.gradient.to})`;
    }
    if (bg.type === 'image' && bg.imageUrl) {
        return `background:url(${bg.imageUrl}) center/cover`;
    }
    if (bg.type === 'video') {
        return `background:#000000`;
    }
    if (bg.type === 'cartoon') {
        const colors = {
            space: '#0a0a1e',
            forest: '#ffeaa7',
            ocean: '#5f27cd'
        };
        return `background:${colors[bg.theme || 'space'] || '#0a0a1e'}`;
    }
    return 'background:#1a1a2e';
}

// ============================================================
// RENDER
// ============================================================
function renderCurrentScene() {
    const canvas = document.getElementById('videoCanvas');
    if (!canvas) return;
    engine.renderScene(canvas, currentSceneIndex);
}

// ============================================================
// EXPORT
// ============================================================
function initExport() {
    document.getElementById('exportBtn').addEventListener('click', async () => {
        const canvas = document.getElementById('videoCanvas');
        const progressEl = document.getElementById('exportProgress');
        const fillEl = document.getElementById('exportProgressFill');
        const textEl = document.getElementById('exportProgressText');
        const btn = document.getElementById('exportBtn');

        btn.disabled = true;
        btn.textContent = 'Exporting...';
        progressEl.style.display = '';

        try {
            const blob = await engine.exportVideo(canvas, {
                fps: 30,
                videoBitsPerSecond: 2500000,
                onExportProgress: (pct) => {
                    fillEl.style.width = pct + '%';
                    textEl.textContent = Math.round(pct) + '%';
                }
            });

            // Download
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'viewmax-video.webm';
            a.click();
            URL.revokeObjectURL(url);

            showToast('Video exported successfully! 🎉', 'success');
        } catch (err) {
            console.error('Export error:', err);
            showToast('Export failed: ' + err.message, 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                Export Video
            `;
            progressEl.style.display = 'none';
            fillEl.style.width = '0%';

            // Re-render
            currentSceneIndex = 0;
            renderCurrentScene();
            renderTimeline();
        }
    });
}

// ============================================================
// SCRIPT GENERATOR
// ============================================================
function initScriptGenerator() {
    document.getElementById('generateScriptBtn').addEventListener('click', () => {
        const topic = document.getElementById('scriptTopic').value.trim();
        if (!topic) {
            showToast('Please enter a topic or idea', 'error');
            return;
        }

        const style = document.getElementById('scriptStyle').value;
        const platform = document.getElementById('scriptPlatform').value;
        const duration = parseInt(document.getElementById('scriptDuration').value);

        const btn = document.getElementById('generateScriptBtn');
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> Generating...';

        // Simulate AI generation delay
        setTimeout(() => {
            const script = engine.generateScript(topic, style, duration, platform);
            const outputCard = document.getElementById('scriptOutputCard');
            const outputBody = document.getElementById('scriptOutputBody');

            outputBody.innerHTML = `<pre class="script-text">${escapeHtml(script)}</pre>`;
            outputCard.style.display = '';
            outputCard.classList.add('fade-in');

            btn.disabled = false;
            btn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
                Generate Script
            `;

            showToast('Script generated! ✍️', 'success');
        }, 1500);
    });

    // Copy script
    document.getElementById('copyScriptBtn').addEventListener('click', () => {
        const text = document.querySelector('.script-text')?.textContent;
        if (text) {
            navigator.clipboard.writeText(text).then(() => {
                showToast('Script copied to clipboard!', 'success');
            });
        }
    });

    // Use in video
    document.getElementById('useInVideoBtn').addEventListener('click', () => {
        const text = document.querySelector('.script-text')?.textContent;
        if (text) {
            // Split script into scenes by paragraphs
            const paragraphs = text.split('\n\n').filter(p => p.trim());
            engine.scenes = [];

            const gradients = [
                { from: '#6C5CE7', to: '#a855f7' },
                { from: '#00b894', to: '#00cec9' },
                { from: '#fd79a8', to: '#e84393' },
                { from: '#fdcb6e', to: '#e17055' },
                { from: '#74b9ff', to: '#0984e3' }
            ];

            paragraphs.forEach((para, i) => {
                const cleanText = para.replace(/^\[.*?\]\s*/gm, '').trim();
                if (cleanText.length > 0) {
                    engine.addScene();
                    const scene = engine.scenes[engine.scenes.length - 1];
                    const grad = gradients[i % gradients.length];
                    scene.background = { type: 'gradient', gradient: { from: grad.from, to: grad.to, angle: 135 } };
                    scene.texts = [{
                        content: cleanText.substring(0, 100),
                        x: 0.5, y: 0.5,
                        fontSize: 48,
                        fontFamily: 'Inter',
                        color: '#ffffff',
                        bold: true,
                        italic: false,
                        align: 'center',
                        animation: 'fadeIn'
                    }];
                    scene.duration = Math.max(3, Math.ceil(cleanText.length / 20));
                    scene.transition = 'fade';
                }
            });

            if (engine.scenes.length === 0) engine.addScene();

            currentSceneIndex = 0;
            navigateTo('video-editor');
            renderCurrentScene();
            renderTimeline();
            loadSceneControls();
            loadTextControls();
            showToast(`Created ${engine.scenes.length} scenes from script!`, 'success');
        }
    });
}

// ============================================================
// VOICEOVER
// ============================================================
function initVoiceover() {
    // Populate voices
    function loadVoices() {
        const voices = engine.getAvailableVoices();
        const select = document.getElementById('voiceSelect');
        select.innerHTML = '';
        voices.forEach((v, i) => {
            const opt = document.createElement('option');
            opt.value = i;
            opt.textContent = `${v.name} (${v.lang})`;
            select.appendChild(opt);
        });
        if (voices.length === 0) {
            const opt = document.createElement('option');
            opt.textContent = 'Default Voice';
            select.appendChild(opt);
        }
    }

    // Voices may load async
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = loadVoices;
    }
    setTimeout(loadVoices, 200);

    // Speed/pitch display
    document.getElementById('voiceSpeed').addEventListener('input', (e) => {
        document.getElementById('voiceSpeedVal').textContent = parseFloat(e.target.value).toFixed(1) + 'x';
    });
    document.getElementById('voicePitch').addEventListener('input', (e) => {
        document.getElementById('voicePitchVal').textContent = parseFloat(e.target.value).toFixed(1);
    });

    // Generate waveform bars
    const barsContainer = document.getElementById('waveformBars');
    for (let i = 0; i < 50; i++) {
        const bar = document.createElement('div');
        bar.className = 'voiceover-waveform-bar';
        bar.style.height = '4px';
        barsContainer.appendChild(bar);
    }

    // Speak button
    document.getElementById('speakBtn').addEventListener('click', () => {
        const text = document.getElementById('voiceText').value.trim();
        if (!text) {
            showToast('Please enter text to speak', 'error');
            return;
        }

        const voices = engine.getAvailableVoices();
        const voiceIdx = parseInt(document.getElementById('voiceSelect').value) || 0;
        const rate = parseFloat(document.getElementById('voiceSpeed').value);
        const pitch = parseFloat(document.getElementById('voicePitch').value);

        engine.speakText(text, {
            voice: voices[voiceIdx]?.name,
            rate,
            pitch
        });

        document.getElementById('speakBtn').style.display = 'none';
        document.getElementById('stopSpeakBtn').style.display = '';

        // Animate waveform
        animateWaveform(true);

        // When speech ends
        const checkEnd = setInterval(() => {
            if (!speechSynthesis.speaking) {
                clearInterval(checkEnd);
                document.getElementById('speakBtn').style.display = '';
                document.getElementById('stopSpeakBtn').style.display = 'none';
                animateWaveform(false);
            }
        }, 200);
    });

    // Stop button
    document.getElementById('stopSpeakBtn').addEventListener('click', () => {
        speechSynthesis.cancel();
        document.getElementById('speakBtn').style.display = '';
        document.getElementById('stopSpeakBtn').style.display = 'none';
        animateWaveform(false);
    });
}

let waveformInterval;
function animateWaveform(active) {
    const bars = document.querySelectorAll('.voiceover-waveform-bar');
    if (active) {
        waveformInterval = setInterval(() => {
            bars.forEach(bar => {
                bar.style.height = (Math.random() * 36 + 4) + 'px';
            });
        }, 100);
    } else {
        clearInterval(waveformInterval);
        bars.forEach(bar => {
            bar.style.height = '4px';
        });
    }
}

// ============================================================
// CAPTIONS
// ============================================================
function initCaptions() {
    const canvas = document.getElementById('captionCanvas');
    const ctx = canvas.getContext('2d');

    function previewCaption() {
        const text = document.getElementById('captionText').value || 'Sample caption text';
        const size = parseInt(document.getElementById('captionSize').value);
        const color = document.getElementById('captionColor').value;
        const style = document.getElementById('captionStyle').value;
        const position = document.getElementById('captionPosition').value;

        // Draw scene background
        const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
        gradient.addColorStop(0, '#6C5CE7');
        gradient.addColorStop(1, '#a855f7');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Caption position
        let y = canvas.height * 0.8;
        if (position === 'center') y = canvas.height * 0.5;
        if (position === 'top') y = canvas.height * 0.2;

        const scaledSize = size * (canvas.width / 1920);
        ctx.font = `bold ${scaledSize}px Inter, sans-serif`;
        ctx.textAlign = 'center';

        const firstLine = text.split('\n')[0];

        if (style === 'boxed') {
            const metrics = ctx.measureText(firstLine);
            const padding = 12;
            ctx.fillStyle = 'rgba(0,0,0,0.7)';
            ctx.roundRect(
                canvas.width / 2 - metrics.width / 2 - padding,
                y - scaledSize / 2 - padding,
                metrics.width + padding * 2,
                scaledSize + padding * 2,
                8
            );
            ctx.fill();
        }

        if (style === 'karaoke' || style === 'highlight') {
            const words = firstLine.split(' ');
            let xPos = canvas.width / 2 - ctx.measureText(firstLine).width / 2;
            words.forEach((word, i) => {
                ctx.fillStyle = i === 0 ? '#feca57' : color;
                ctx.textAlign = 'left';
                ctx.fillText(word + ' ', xPos, y);
                xPos += ctx.measureText(word + ' ').width;
            });
        } else {
            ctx.fillStyle = color;
            ctx.fillText(firstLine, canvas.width / 2, y);
        }

        // Shadow for readability
        if (style === 'classic') {
            ctx.shadowColor = 'rgba(0,0,0,0.8)';
            ctx.shadowBlur = 6;
            ctx.fillStyle = color;
            ctx.fillText(firstLine, canvas.width / 2, y);
            ctx.shadowBlur = 0;
        }
    }

    ['captionText', 'captionSize', 'captionColor', 'captionStyle', 'captionPosition'].forEach(id => {
        document.getElementById(id).addEventListener('input', previewCaption);
        document.getElementById(id).addEventListener('change', previewCaption);
    });

    previewCaption();

    // Apply captions to video
    document.getElementById('applyCaptionsBtn').addEventListener('click', () => {
        const text = document.getElementById('captionText').value.trim();
        if (!text) {
            showToast('Please enter caption text', 'error');
            return;
        }

        const lines = text.split('\n').filter(l => l.trim());
        const size = parseInt(document.getElementById('captionSize').value);
        const color = document.getElementById('captionColor').value;
        const position = document.getElementById('captionPosition').value;

        let posY = 0.8;
        if (position === 'center') posY = 0.5;
        if (position === 'top') posY = 0.2;

        // Add captions to scenes
        lines.forEach((line, i) => {
            const sceneIdx = Math.min(i, engine.scenes.length - 1);
            const scene = engine.scenes[sceneIdx];
            if (scene) {
                scene.texts.push({
                    content: line.trim(),
                    x: 0.5, y: posY,
                    fontSize: size,
                    fontFamily: 'Inter',
                    color: color,
                    bold: true,
                    italic: false,
                    align: 'center',
                    animation: 'fadeIn'
                });
            }
        });

        navigateTo('video-editor');
        renderCurrentScene();
        renderTimeline();
        showToast(`Added ${lines.length} captions to your video!`, 'success');
    });
}

// ============================================================
// TEMPLATES
// ============================================================
function initTemplates() {
    const templates = engine.getTemplates();

    // Render templates grid (full page)
    renderTemplatesGrid(templates, 'templatesGrid');

    // Render home preview (first 3)
    renderTemplatesGrid(templates.slice(0, 3), 'homeTemplatesGrid');

    // Filter chips (scoped to template filters only)
    document.querySelectorAll('#templateFilters .filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('#templateFilters .filter-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            const category = chip.dataset.category;
            const filtered = category === 'all' ? templates : templates.filter(t => t.category === category);
            renderTemplatesGrid(filtered, 'templatesGrid');
        });
    });
}

function renderTemplatesGrid(templates, containerId) {
    const grid = document.getElementById(containerId);
    if (!grid) return;
    grid.innerHTML = '';

    templates.forEach(template => {
        const card = document.createElement('div');
        card.className = 'template-card';
        const gradColors = template.thumbnailGradient || ['#6C5CE7', '#a855f7'];
        card.innerHTML = `
            <div class="template-card-preview" style="background: linear-gradient(135deg, ${gradColors[0]}, ${gradColors[1]});">
                <span class="template-icon" style="font-size: 3rem; color: #fff;">${template.icon || '🎬'}</span>
                <div class="template-card-overlay">
                    <button class="template-card-use-btn">Use Template</button>
                </div>
            </div>
            <div class="template-card-body">
                <h3 class="template-card-title">${template.name}</h3>
                <div class="template-card-meta">
                    <span class="badge">${template.category}</span>
                    <span class="badge">${template.scenes?.length || 0} scenes</span>
                </div>
            </div>
        `;

        // Click handler for card or use button
        const handleUse = (e) => {
            e.stopPropagation();
            engine.loadTemplate(template.id);
            currentSceneIndex = 0;
            selectedTextIndex = 0;
            navigateTo('video-editor');
            renderCurrentScene();
            renderTimeline();
            loadSceneControls();
            loadTextControls();
            showToast(`Template "${template.name}" loaded! 🎨`, 'success');
        };

        card.addEventListener('click', handleUse);
        card.querySelector('.template-card-use-btn')?.addEventListener('click', handleUse);

        grid.appendChild(card);
    });
}

// ============================================================
// FEATURED PREVIEW (Home page)
// ============================================================
function initFeaturedPreview() {
    const canvas = document.getElementById('featuredCanvas');
    if (!canvas) return;

    // Create a mini demo scene
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, '#6C5CE7');
    gradient.addColorStop(1, '#a855f7');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 48px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('✨ Your Viral Video Starts Here ✨', canvas.width / 2, canvas.height / 2 - 20);

    ctx.font = '24px Inter, sans-serif';
    ctx.fillStyle = 'rgba(255,255,255,0.8)';
    ctx.fillText('Click Play to Preview • Built with ViewMax Pro', canvas.width / 2, canvas.height / 2 + 30);

    // Play overlay click
    document.getElementById('featuredPlayOverlay').addEventListener('click', () => {
        navigateTo('video-editor');
    });
}

// ============================================================
// UTILS
// ============================================================
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ============================================================
// EDITOR SCRIPT TAB GENERATOR
// ============================================================
function initEditorScriptTab() {
    const generateBtn = document.getElementById('btnGenerateFromEditorScript');
    if (!generateBtn) return;

    generateBtn.addEventListener('click', () => {
        const text = document.getElementById('editorScriptText').value.trim();
        if (!text) {
            showToast('Please enter or paste a script first!', 'error');
            return;
        }

        // Split text into paragraphs by blank lines or standard newlines
        const paragraphs = text.split(/\n\s*\n/).filter(p => p.trim());
        if (paragraphs.length === 0) {
            showToast('Please enter some valid paragraphs!', 'error');
            return;
        }

        const theme = document.getElementById('editorScriptTheme').value;
        const themes = {
            purple: { from: '#6C5CE7', to: '#a855f7' },
            teal: { from: '#00b894', to: '#00cec9' },
            pink: { from: '#fd79a8', to: '#e84393' },
            dark: { from: '#1a1a2e', to: '#16213e' },
            blue: { from: '#74b9ff', to: '#0984e3' }
        };

        const selectedTheme = themes[theme] || themes.purple;

        engine.scenes = [];
        paragraphs.forEach(para => {
            engine.addScene();
            const scene = engine.scenes[engine.scenes.length - 1];
            scene.background = {
                type: 'gradient',
                gradient: {
                    from: selectedTheme.from,
                    to: selectedTheme.to,
                    angle: 135
                }
            };
            scene.texts = [
                {
                    content: para.trim(),
                    x: 0.5,
                    y: 0.5,
                    fontSize: 54,
                    fontFamily: 'Inter',
                    color: '#ffffff',
                    bold: true,
                    italic: false,
                    align: 'center',
                    animation: 'fadeIn'
                }
            ];
            scene.duration = Math.max(3, Math.ceil(para.length / 18));
            scene.transition = 'fade';
        });

        currentSceneIndex = 0;
        selectedTextIndex = 0;
        renderCurrentScene();
        renderTimeline();
        loadSceneControls();
        loadTextControls();
        
        // Auto-switch to Background tab so they can tweak styles
        document.querySelector('.tab-btn[data-tab="background"]')?.click();
        
        showToast(`Successfully generated ${engine.scenes.length} video scenes! 🎬`, 'success');
    });
}

// ============================================================
// AI VIDEO STUDIO
// ============================================================
let creations = [
    {
        id: 'create_1',
        prompt: '3D Pixar-style animation Cute baby with big blue eyes Bright colorful forest Soft lighting',
        model: 'Kling 2.5',
        theme: 'baby',
        videoUrl: '/videos/sintel.mp4',
        aspect: '16:9',
        duration: 5,
        resolution: '1080p',
        seed: '8172648',
        motion: 'static'
    },
    {
        id: 'create_2',
        prompt: 'A cute cartoon astronaut floating in space with neon twinkling starfields, 3d vector style',
        model: 'Kling 2.5 Turbo',
        theme: 'space',
        videoUrl: '/videos/space.mp4',
        aspect: '16:9',
        duration: 5,
        resolution: '720p',
        seed: '1928471',
        motion: 'tilt-up'
    },
    {
        id: 'create_3',
        prompt: 'A fantasy fox hopping in a colorful forest with falling orange leaves and drifting clouds, flat vector style',
        model: 'Sora 2',
        theme: 'forest',
        videoUrl: '/videos/forest.mp4',
        aspect: '9:16',
        duration: 5,
        resolution: '1080p',
        seed: '5412938',
        motion: 'zoom-in'
    },
    {
        id: 'create_4',
        prompt: 'A cute submarine bobbing in ocean wave water layers under a giant retro sunset sun, minimalist vector style',
        model: 'Veo 3.1',
        theme: 'ocean',
        videoUrl: '/videos/ocean.mp4',
        aspect: '16:9',
        duration: 5,
        resolution: '1080p',
        seed: '9081273',
        motion: 'static'
    }
];

let activeModalCreation = null;
let modalIsPlaying = false;
let modalStartTime = 0;
let modalPausedTime = 0;
let modalAnimId = null;
let modalCurrentTime = 0;
let uploadedImageSrc = '';

function initStudio() {
    const btnTabTxt2Vid = document.getElementById('btnTabTxt2Vid');
    const btnTabImg2Vid = document.getElementById('btnTabImg2Vid');
    const groupTxtPrompt = document.getElementById('groupTxtPrompt');
    const groupImgPrompt = document.getElementById('groupImgPrompt');

    if (!btnTabTxt2Vid) return;

    // Tabs toggle
    btnTabTxt2Vid.addEventListener('click', () => {
        btnTabTxt2Vid.classList.add('active');
        btnTabImg2Vid.classList.remove('active');
        groupTxtPrompt.style.display = '';
        groupImgPrompt.style.display = 'none';
    });

    btnTabImg2Vid.addEventListener('click', () => {
        btnTabImg2Vid.classList.add('active');
        btnTabTxt2Vid.classList.remove('active');
        groupTxtPrompt.style.display = 'none';
        groupImgPrompt.style.display = '';
    });

    // Surprise Me Prompts
    const surprisePrompts = [
        "A cute cartoon astronaut floating in space with neon twinkling starfields, 3d vector style",
        "A fantasy fox hopping in a colorful forest with falling orange leaves and drifting clouds, pastel flat vector style",
        "A cute submarine bobbing in ocean wave water layers under a giant retro sunset sun, minimalist vector style",
        "A futuristic tiny drone flying over a cyber-punk city with neon lights and purple rain, flat color cartoon style",
        "A magical tree with glowing flowers and friendly fireflies in a mysterious night garden, colorful children book style"
    ];
    document.getElementById('btnSurpriseMe')?.addEventListener('click', () => {
        const p = surprisePrompts[Math.floor(Math.random() * surprisePrompts.length)];
        document.getElementById('studioPrompt').value = p;
    });

    // Aspect Ratio & Duration & Resolution toggles
    document.querySelectorAll('.btn-studio-aspect').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.btn-studio-aspect').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    document.querySelectorAll('.btn-studio-dur').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.btn-studio-dur').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    document.querySelectorAll('.btn-studio-res').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.btn-studio-res').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Image Upload Zone
    const dropZone = document.getElementById('dropZone');
    const imageUploadInput = document.getElementById('studioImageUpload');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const uploadedImagePreview = document.getElementById('uploadedImagePreview');
    const btnRemoveUploadedImage = document.getElementById('btnRemoveUploadedImage');

    dropZone?.addEventListener('click', () => imageUploadInput.click());

    imageUploadInput?.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                uploadedImageSrc = ev.target.result;
                uploadedImagePreview.src = uploadedImageSrc;
                imagePreviewContainer.style.display = 'block';
                dropZone.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });

    btnRemoveUploadedImage?.addEventListener('click', () => {
        imageUploadInput.value = '';
        uploadedImageSrc = '';
        imagePreviewContainer.style.display = 'none';
        dropZone.style.display = 'block';
    });

    // Generate Button Action
    document.getElementById('btnGenerateStudioVideo')?.addEventListener('click', () => {
        try {
            const txtActive = btnTabTxt2Vid.classList.contains('active');
            const promptText = document.getElementById('studioPrompt').value.trim();

            if (txtActive && !promptText) {
                showToast('Please enter a description prompt first!', 'error');
                return;
            }
            if (!txtActive && !uploadedImageSrc) {
                showToast('Please upload a reference image first!', 'error');
                return;
            }

            // Unlimited Credits - started message
            showToast('AI Video generation started... 🪄', 'success');

            const modelVal = document.getElementById('studioModel').value;
            const modelMap = { kling: 'Kling 2.5', sora: 'Sora 2', hailuo: 'Hailuo 2.3', veo: 'Veo 3.1' };
            const aspectEl = document.querySelector('.btn-studio-aspect.active');
            const durEl = document.querySelector('.btn-studio-dur.active');
            const resEl = document.querySelector('.btn-studio-res.active');
            const aspect = aspectEl ? aspectEl.dataset.aspect : '16:9';
            const duration = durEl ? parseInt(durEl.dataset.dur) : 5;
            const resolution = resEl ? resEl.dataset.res : '1080p';
            const motion = document.getElementById('studioMotion').value;

            // Add loading placeholder to grid
            const tempId = 'temp_' + Date.now();
            const loadingItem = {
                id: tempId,
                prompt: txtActive ? promptText : 'Image-to-Video generation using reference image',
                model: modelMap[modelVal] || 'Kling 2.5',
                aspect: aspect,
                duration: duration,
                progress: 0,
                isLoading: true
            };

            creations.unshift(loadingItem);
            renderStudioCreations();

            // Simulate 3 seconds progress bar
            let percent = 0;
            const interval = setInterval(() => {
                percent += 10;
                const item = creations.find(c => c.id === tempId);
                if (item) {
                    item.progress = percent;
                    renderStudioCreations();
                }

                if (percent >= 100) {
                    clearInterval(interval);

                    // Determine matching cartoon theme & high-fidelity video link
                    let detectedTheme = 'space';
                    let videoUrl = '/videos/space.mp4';
                    
                    const lower = promptText.toLowerCase();
                    if (lower.includes('forest') || lower.includes('fox') || lower.includes('tree') || lower.includes('nature') || lower.includes('cat') || lower.includes('rabbit')) {
                        detectedTheme = 'forest';
                        videoUrl = '/videos/forest.mp4';
                    } else if (lower.includes('ocean') || lower.includes('sea') || lower.includes('water') || lower.includes('submarine') || lower.includes('sunset')) {
                        detectedTheme = 'ocean';
                        videoUrl = '/videos/ocean.mp4';
                    } else if (lower.includes('baby') || lower.includes('pixar') || lower.includes('cute') || lower.includes('leo')) {
                        detectedTheme = 'baby';
                        videoUrl = '/videos/sintel.mp4';
                    } else {
                        // Random pick
                        const themes = [
                            { theme: 'space', url: '/videos/space.mp4' },
                            { theme: 'forest', url: '/videos/forest.mp4' },
                            { theme: 'ocean', url: '/videos/ocean.mp4' }
                        ];
                        const pick = themes[Math.floor(Math.random() * themes.length)];
                        detectedTheme = pick.theme;
                        videoUrl = pick.url;
                    }

                    // Final creation object
                    const finalItem = {
                        id: 'create_' + Date.now(),
                        prompt: txtActive ? promptText : 'Image animation: ' + promptText,
                        model: modelMap[modelVal] || 'Kling 2.5',
                        theme: detectedTheme,
                        videoUrl: videoUrl,
                        aspect: aspect,
                        duration: duration,
                        resolution: resolution,
                        seed: Math.floor(Math.random() * 90000000) + 10000000,
                        motion: motion
                    };

                    // Swap loading card
                    const index = creations.findIndex(c => c.id === tempId);
                    if (index !== -1) {
                        creations[index] = finalItem;
                    }
                    renderStudioCreations();
                    showToast('Video Generated Successfully! 🎉', 'success');
                }
            }, 300);
        } catch (err) {
            console.error("Studio Generation Error:", err);
            showToast("Failed to start generation: " + err.message, "error");
        }
    });

    // Bind Player Modal Elements
    document.getElementById('btnModalClose')?.addEventListener('click', closePlayerModal);
    document.getElementById('playerModalOverlay')?.addEventListener('click', (e) => {
        if (e.target.id === 'playerModalOverlay') closePlayerModal();
    });

    document.getElementById('btnModalPlay')?.addEventListener('click', toggleModalPlay);
    document.getElementById('btnModalDownload')?.addEventListener('click', downloadModalVideo);
    document.getElementById('btnModalFullscreen')?.addEventListener('click', toggleModalFullscreen);
    document.getElementById('modalPlayerVideo')?.addEventListener('dblclick', toggleModalFullscreen);
    document.getElementById('btnModalEdit')?.addEventListener('click', () => {
        if (!activeModalCreation) return;
        
        // Import this creation into the Scene timeline editor
        const videoUrl = activeModalCreation.videoUrl;
        const dur = activeModalCreation.duration;
        
        // Clear scenes and push this animation
        engine.scenes = [];
        engine.addScene();
        const scene = engine.scenes[0];
        scene.background = {
            type: 'video',
            videoUrl: videoUrl
        };
        scene.duration = dur;
        scene.texts = [
            {
                content: 'Double click to edit overlay text',
                x: 0.5,
                y: 0.5,
                fontSize: 54,
                fontFamily: 'Inter',
                color: '#ffffff',
                bold: true,
                italic: false,
                align: 'center',
                animation: 'fadeIn'
            }
        ];

        currentSceneIndex = 0;
        selectedTextIndex = 0;

        closePlayerModal();
        navigateTo('scene-editor');
        
        // Load configurations
        renderCurrentScene();
        renderTimeline();
        loadSceneControls();
        loadTextControls();
        
        showToast('Video imported into Editor Timeline! 🎬', 'success');
    });

    // Initial render
    renderStudioCreations();
}

function renderStudioCreations() {
    try {
        const grid = document.getElementById('studioCreationsGrid');
        if (!grid) return;

        grid.innerHTML = '';

        creations.forEach(item => {
            const card = document.createElement('div');
            card.className = 'tool-card';
            card.style.overflow = 'hidden';

            if (item.isLoading) {
                // Skeleton Loader for video generation
                card.innerHTML = `
                    <div class="tool-card-thumb" style="background:#09090e; display:flex; flex-direction:column; justify-content:center; align-items:center; gap: 10px; height: 160px; position:relative;">
                        <div style="width: 32px; height: 32px; border: 4px solid var(--color-border); border-top: 4px solid var(--color-primary); border-radius:50%; animation: spin 1s linear infinite;"></div>
                        <div style="font-size: var(--font-xs); font-weight: 600; color: #fff;">Generating Video (${item.progress}%)</div>
                        <div style="position:absolute; bottom:0; left:0; right:0; height:4px; background:rgba(255,255,255,0.1);">
                            <div style="height:100%; width:${item.progress}%; background:var(--color-primary); transition: width 0.2s;"></div>
                        </div>
                    </div>
                    <div class="tool-card-body" style="padding:15px;">
                        <span class="badge" style="background:rgba(255,255,255,0.1); color:#fff; border-radius:4px;">${item.model}</span>
                        <p style="font-size:var(--font-sm); margin-top:10px; color:var(--color-text-muted); text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">${item.prompt}</p>
                    </div>
                `;
                grid.appendChild(card);
                return;
            }

            card.innerHTML = `
                <div class="tool-card-thumb" style="position:relative; height:160px; background:#000; overflow:hidden; cursor:pointer;">
                    <video src="${item.videoUrl}" autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover; pointer-events:none;"></video>
                    <div style="position:absolute; top:8px; right:8px; display:flex; gap:4px; z-index:5;">
                        <span class="badge" style="background:rgba(0,0,0,0.6); color:#fff;">${item.model}</span>
                        <span class="badge" style="background:rgba(0,0,0,0.6); color:#fff;">${item.aspect}</span>
                        <span class="badge" style="background:var(--color-primary); color:#fff; font-weight:700;">${item.resolution || '1080p'}</span>
                    </div>
                    <!-- Play Hover Overlay -->
                    <div style="position:absolute; inset:0; background:rgba(0,0,0,0.3); display:flex; align-items:center; justify-content:center; opacity:0; transition:opacity 0.2s;" class="play-hover-overlay">
                        <span style="font-size: 32px; color:#fff; text-shadow:0 2px 10px rgba(0,0,0,0.5);">▶</span>
                    </div>
                </div>
                <div class="tool-card-body" style="padding:15px; display:flex; flex-direction:column; justify-content:space-between; height:110px;">
                    <p style="font-size:var(--font-sm); color:var(--color-text); font-weight:500; margin:0; line-height:1.4; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">${item.prompt}</p>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                        <span class="form-hint" style="margin:0;">Duration: ${item.duration}s</span>
                        <div style="display:flex; gap:6px;">
                            <button class="filter-chip btn-play-trigger" style="padding: 4px 8px; font-size:11px; margin:0; cursor:pointer;">Play</button>
                            <button class="filter-chip btn-download-trigger" style="padding: 4px 8px; font-size:11px; margin:0; cursor:pointer; background:var(--color-primary); color:#fff; border:none;">Download</button>
                            <button class="filter-chip btn-delete-trigger" style="padding: 4px 8px; font-size:11px; margin:0; background:none; color:var(--color-danger); border:1px solid var(--color-danger); cursor:pointer;">✕</button>
                        </div>
                    </div>
                </div>
            `;

            const thumb = card.querySelector('.tool-card-thumb');
            const playBtn = card.querySelector('.btn-play-trigger');
            const dlBtn = card.querySelector('.btn-download-trigger');
            const delBtn = card.querySelector('.btn-delete-trigger');

            // Bind Hover Overlay
            thumb.addEventListener('mouseenter', (e) => {
                const overlay = e.currentTarget.querySelector('.play-hover-overlay');
                if (overlay) overlay.style.opacity = '1';
            });
            thumb.addEventListener('mouseleave', (e) => {
                const overlay = e.currentTarget.querySelector('.play-hover-overlay');
                if (overlay) overlay.style.opacity = '0';
            });

            const handlePlayClick = () => openPlayerModal(item);
            thumb.addEventListener('click', handlePlayClick);
            if (playBtn) playBtn.addEventListener('click', handlePlayClick);

            // Bind Download click
            if (dlBtn) {
                dlBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    dlBtn.disabled = true;
                    dlBtn.textContent = '...';
                    
                    fetch(item.videoUrl + "?t=" + Date.now())
                        .then(response => {
                            if (!response.ok) throw new Error("Network response was not ok");
                            return response.blob();
                        })
                        .then(blob => {
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `viewmax-ai-${item.theme}-${Date.now()}.mp4`;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            URL.revokeObjectURL(url);
                            
                            dlBtn.disabled = false;
                            dlBtn.textContent = 'Download';
                            showToast('Download completed successfully! 🎉', 'success');
                        })
                        .catch(err => {
                            console.error("Download Error:", err);
                            dlBtn.disabled = false;
                            dlBtn.textContent = 'Download';
                            showToast('Download failed: ' + err.message, 'error');
                        });
                });
            }

            // Bind Delete click
            if (delBtn) {
                delBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    creations = creations.filter(c => c.id !== item.id);
                    renderStudioCreations();
                    showToast('Video creation deleted', 'info');
                });
            }

            grid.appendChild(card);
        });
    } catch (err) {
        console.error("renderStudioCreations Error:", err);
        showToast("Failed to render gallery: " + err.message, "error");
    }
}

function openPlayerModal(creation) {
    activeModalCreation = creation;
    const overlay = document.getElementById('playerModalOverlay');
    if (!overlay) return;

    // Set texts
    document.getElementById('modalVideoTitle').textContent = `Video Studio Loop`;
    document.getElementById('modalVideoPrompt').textContent = creation.prompt;
    document.getElementById('modalBadgeModel').textContent = creation.model;
    document.getElementById('modalBadgeAspect').textContent = creation.aspect;
    document.getElementById('modalBadgeDur').textContent = `${creation.duration}s`;
    document.getElementById('modalVideoSeed').textContent = creation.seed;
    document.getElementById('modalVideoMotion').textContent = creation.motion;

    // Configure Video Element
    const video = document.getElementById('modalPlayerVideo');
    const container = document.getElementById('modalPlayerContainer');
    const aspect = creation.aspect;

    if (aspect === '16:9') {
        container.style.aspectRatio = '16/9';
    } else if (aspect === '9:16') {
        container.style.aspectRatio = '9/16';
    } else {
        container.style.aspectRatio = '1/1';
    }

    overlay.style.display = 'flex';
    
    // Playback state
    modalIsPlaying = true;
    document.getElementById('btnModalPlay').textContent = '▮▮';

    // Set source and play
    video.src = creation.videoUrl;
    video.currentTime = 0;
    video.play().catch(err => console.error("Video Play Error:", err));

    // Listen to timeupdate to sync custom progress bar and time display
    const onTimeUpdate = () => {
        if (!video.duration) return;
        const progress = video.currentTime / video.duration;
        document.getElementById('modalProgressBar').style.width = `${progress * 100}%`;
        
        const format = (seconds) => {
            const m = Math.floor(seconds / 60);
            const s = Math.floor(seconds % 60);
            return `${m}:${s < 10 ? '0' : ''}${s}`;
        };
        document.getElementById('modalTimeDisplay').textContent = `${format(video.currentTime)} / ${format(video.duration || creation.duration)}`;
    };

    video.removeEventListener('timeupdate', video._timeUpdateHandler);
    video._timeUpdateHandler = onTimeUpdate;
    video.addEventListener('timeupdate', onTimeUpdate);
}

function closePlayerModal() {
    const video = document.getElementById('modalPlayerVideo');
    if (video) {
        video.pause();
        video.src = '';
    }
    document.getElementById('playerModalOverlay').style.display = 'none';
    activeModalCreation = null;
}

function toggleModalPlay() {
    const video = document.getElementById('modalPlayerVideo');
    const playBtn = document.getElementById('btnModalPlay');
    if (!video) return;

    if (!video.paused) {
        video.pause();
        playBtn.textContent = '▶';
    } else {
        video.play().catch(err => console.error(err));
        playBtn.textContent = '▮▮';
    }
}

function toggleModalFullscreen() {
    const video = document.getElementById('modalPlayerVideo');
    if (!video) return;

    if (video.requestFullscreen) {
        video.requestFullscreen();
    } else if (video.webkitRequestFullscreen) {
        video.webkitRequestFullscreen();
    } else if (video.msRequestFullscreen) {
        video.msRequestFullscreen();
    }
}

function downloadModalVideo() {
    if (!activeModalCreation) return;
    const downloadBtn = document.getElementById('btnModalDownload');

    downloadBtn.disabled = true;
    downloadBtn.textContent = 'Downloading... 📥';

    fetch(activeModalCreation.videoUrl + "?t=" + Date.now())
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `viewmax-ai-${activeModalCreation.theme}-${Date.now()}.mp4`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            downloadBtn.disabled = false;
            downloadBtn.textContent = 'Download Video (.mp4)';
            showToast('Download completed successfully! 🎉', 'success');
        })
        .catch(err => {
            console.error("Download Error:", err);
            downloadBtn.disabled = false;
            downloadBtn.textContent = 'Download Video (.mp4)';
            showToast('Download failed: ' + err.message, 'error');
        });
}
