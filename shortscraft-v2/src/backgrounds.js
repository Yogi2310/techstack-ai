// =============================================
// backgrounds.js — ShortsCraft 2.0
//
// TWO separate systems:
//
// 1. PAGE BACKGROUND (CSS only, no canvas):
//    → Unsplash topic-specific photos via <div> background-image
//    → CORS doesn't matter, browser handles it
//
// 2. VIDEO CANVAS BACKGROUNDS:
//    → Picsum Photos  https://picsum.photos/seed/{SEED}/1080/1920
//    → 100% CORS-enabled, free, no API key, reliable
//    → Seed = topic + segIdx + generationId → DIFFERENT image every segment, every generation
// =============================================

// ─── Page BG only (CSS bg-image, not used on canvas) ───────────────────────
export const pageBackgrounds = {
    bjp:        ['https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1547036967-23d11aacaee0?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1605027991685-66406f9c2d6f?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1444080748397-f442aa95c3e5?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=1600&h=900&fit=crop&q=80'],
    cjp:        ['https://images.unsplash.com/photo-1532375810709-75b1da00537c?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1490730141103-6cac27aaab94?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1605027991685-66406f9c2d6f?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=1600&h=900&fit=crop&q=80'],
    politics:   ['https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1605027991685-66406f9c2d6f?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1600&h=900&fit=crop&q=80'],
    motivation: ['https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1505144808419-1957a94ca61e?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1600&h=900&fit=crop&q=80'],
    science:    ['https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=1600&h=900&fit=crop&q=80'],
    sports:     ['https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1593341646782-e0b495cff86d?w=1600&h=900&fit=crop&q=80'],
    technology: ['https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1600&h=900&fit=crop&q=80'],
    facts:      ['https://images.unsplash.com/photo-1444080748397-f442aa95c3e5?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1516339901601-2e1b62dc0c45?w=1600&h=900&fit=crop&q=80'],
    nature:     ['https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=1600&h=900&fit=crop&q=80'],
    rights:     ['https://images.unsplash.com/photo-1605027991685-66406f9c2d6f?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1532375810709-75b1da00537c?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=1600&h=900&fit=crop&q=80'],
    all:        ['https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1600&h=900&fit=crop&q=80','https://images.unsplash.com/photo-1444080748397-f442aa95c3e5?w=1600&h=900&fit=crop&q=80'],
};

// Keep topicBackgrounds as alias for compat
export const topicBackgrounds = pageBackgrounds;

// ─── Accent colors per topic (flows into canvas color grade) ────────────────
export const topicAccents = {
    bjp:        ['#FF6600','#ff4500','#dc143c','#8B0000','#FF8C00','#ff5722'],
    cjp:        ['#ff6b35','#d4af37','#ff9933','#f39c12','#e74c3c','#2ecc71'],
    politics:   ['#e63946','#d4af37','#ff9933','#c0392b','#8e44ad','#2980b9'],
    motivation: ['#fdcb6e','#e17055','#ff7675','#6c5ce7','#00cec9','#fd79a8'],
    science:    ['#47d9ff','#6c5ce7','#00cec9','#a29bfe','#0984e3','#00b894'],
    sports:     ['#00b894','#fdcb6e','#e17055','#0984e3','#d4af37','#3ddc84'],
    technology: ['#a855f7','#00cec9','#e84393','#6c5ce7','#00ff41','#74b9ff'],
    facts:      ['#6c5ce7','#fdcb6e','#0984e3','#e17055','#a29bfe','#fd79a8'],
    nature:     ['#43e97b','#00b894','#00cec9','#0984e3','#55efc4','#fdcb6e'],
    rights:     ['#FF9933','#ff6b35','#d4af37','#e74c3c','#2ecc71','#3498db'],
    all:        ['#ff47a8','#6c47ff','#47d9ff','#43e97b','#fdcb6e','#e63946'],
};

// ─── Picsum seed pools per topic ─────────────────────────────────────────────
// Each string becomes: https://picsum.photos/seed/{seed}/1080/1920
// Seeds are chosen so the resulting images match the topic's COLOR MOOD
// (Picsum's random images skew toward landscapes, cities, architecture — all great for Shorts)
const topicSeeds = {
    bjp:        ['storm','thunder','fire','parliament','protest','dark-city','night-crowd','torch','rebel','justice','courtroom','democracy','accountability','corruption','press'],
    cjp:        ['candlelight','sunrise-hope','justice-scale','constitution','freedom-march','india-flag','dawn','equality','rights','solidarity','peaceful','law-books','hope','resistance','liberation'],
    politics:   ['capitol','election','vote','governance','parliament-night','debate','democracy','flag-wave','civic','protest-day','campaign','policy','legislation','republic','senate'],
    motivation: ['mountain-summit','sunrise-gold','ocean-power','forest-path','starfield','aurora','waterfall','epic-landscape','golden-hour','misty-peak','dawn-runner','cosmos','infinite','horizon','ascent'],
    science:    ['nebula','galaxy','lab-blue','dna','quantum','microscope','aurora-lab','space-station','deep-space','particle','experiment','discovery','cosmos-bright','telescope','atom'],
    sports:     ['stadium-lights','athlete-sunset','track-action','field-green','boxing-ring','swimming-pool','cycling-speed','gym-dark','basketball','cricket-pitch','tennis-court','football-crowd','sprint','marathon','champion'],
    technology: ['neon-matrix','circuit-glow','ai-neural','cyber-city','code-screen','fiber-optic','robot-blue','digital-wave','hack-green','server-room','satellite','quantum-chip','hologram','network','binary'],
    facts:      ['lightning-bolt','deep-ocean','volcano','milky-way','hurricane','deep-cave','black-hole','tornado','glacier','bioluminescence','comet','earthquake','eclipse','tsunami','arctic'],
    nature:     ['amazon-canopy','coral-reef','mountain-lake','arctic-fox','cherry-blossom','monsoon','savanna','northern-lights','redwood','ocean-wave','meadow','volcano-nature','waterfall-misty','tropical','tundra'],
    rights:     ['constitution-dawn','march-candles','india-gate-night','flag-sunrise','democracy-rally','citizens','equality-sign','protest-peaceful','solidarity-march','vote-power','law-court','freedom','justice-hope','republic','unity'],
    all:        ['cosmos','neon-city','mountain-gold','fire-light','ocean-blue','forest-green','tech-purple','storm-electric','sunrise','aurora-colors'],
};

// ─── Page BG rotation state ──────────────────────────────────────────────────
const bgUsedIdx = new Map();

export function getRandomPageBgUrl(topic) {
    const pool = pageBackgrounds[topic] || pageBackgrounds.all;
    if (!bgUsedIdx.has(topic)) bgUsedIdx.set(topic, 0);
    const idx = bgUsedIdx.get(topic) % pool.length;
    bgUsedIdx.set(topic, idx + 1);
    return pool[idx];
}

export function buildBgUrl(url) {
    if (typeof url === 'string') return url;
    return url?.src || '#';
}

export function buildThumbUrl(url) {
    if (typeof url === 'string') {
        return url.replace('w=1600&h=900', 'w=400&h=711').replace('w=1080&h=1920', 'w=400&h=711');
    }
    return '#';
}

// ─── VIDEO CANVAS IMAGE SYSTEM ───────────────────────────────────────────────
// Uses Picsum with unique seeds per (topic, segment, generationId)
// ✅ CORS-enabled  ✅ Free  ✅ Always different  ✅ No API key

/**
 * Build a Picsum URL that is UNIQUE per segment and per generation.
 * @param {string} topic   - e.g. 'bjp', 'science'
 * @param {number} segIdx  - segment index within video (0, 1, 2, ...)
 * @param {string} genId   - unique ID per Generate click (use Date.now())
 */
export function buildVideoImageUrl(topic, segIdx, genId) {
    const seeds = topicSeeds[topic] || topicSeeds.all;
    // Pick a seed from the topic pool, cycling through them
    const baseSeed = seeds[segIdx % seeds.length];
    // Append genId so every regeneration gets DIFFERENT images
    const fullSeed = `${baseSeed}-${genId}-${segIdx}`;
    return `https://picsum.photos/seed/${encodeURIComponent(fullSeed)}/1080/1920`;
}

/**
 * Get accent color for a given topic+segment
 */
export function getSegmentAccent(topic, segIdx) {
    const pool = topicAccents[topic] || topicAccents.all;
    return pool[segIdx % pool.length];
}

/**
 * Preload a batch of video images for a topic.
 * Returns array of { img: HTMLImageElement, accent: string }
 */
export async function preloadVideoImages(topic, segCount, genId, onProgress) {
    const results = [];

    const promises = Array.from({ length: segCount }, (_, segIdx) => {
        return new Promise((resolve) => {
            const url    = buildVideoImageUrl(topic, segIdx, genId);
            const accent = getSegmentAccent(topic, segIdx);
            const img    = new Image();
            // ✅ Picsum supports CORS — crossOrigin works fine
            img.crossOrigin = 'anonymous';

            const timer = setTimeout(() => {
                // Timeout fallback: resolve without image, use gradient
                resolve({ img: null, accent, url });
                if (onProgress) onProgress(segIdx + 1, segCount);
            }, 12000);

            img.onload = () => {
                clearTimeout(timer);
                img._accent = accent;
                results[segIdx] = { img, accent, url };
                if (onProgress) onProgress(segIdx + 1, segCount);
                resolve({ img, accent, url });
            };
            img.onerror = () => {
                clearTimeout(timer);
                // Try without crossOrigin as fallback
                const img2 = new Image();
                img2.onload  = () => { img2._accent = accent; results[segIdx] = { img: img2, accent, url }; if (onProgress) onProgress(segIdx + 1, segCount); resolve({ img: img2, accent, url }); };
                img2.onerror = () => { results[segIdx] = { img: null, accent, url }; if (onProgress) onProgress(segIdx + 1, segCount); resolve({ img: null, accent, url }); };
                img2.src = url;
            };

            img.src = url;
        });
    });

    await Promise.all(promises);
    return Array.from({ length: segCount }, (_, i) => results[i] || { img: null, accent: getSegmentAccent(topic, i) });
}

// ─── Legacy compat exports ───────────────────────────────────────────────────
let _totalLoaded  = 0;
const _loadCbs    = [];
export function onLoadProgress(cb) { _loadCbs.push(cb); }
export function getLoadProgress()  { return Math.min(100, _totalLoaded * 5); }
export function getTotalLoaded()   { return _totalLoaded; }
export function startPreloadAll()  { _totalLoaded = 5; _loadCbs.forEach(cb => cb(5, 100)); }
export function getRandomImage()   { return null; }
export function buildUnsplashUrl() { return ''; }
export function getRandomPhotoId(topic) {
    const pool = pageBackgrounds[topic] || pageBackgrounds.all;
    return pool[Math.floor(Math.random() * pool.length)];
}
export function preloadTopicImages() { return Promise.resolve([]); }

// ─── Topic metadata ──────────────────────────────────────────────────────────
export const topicMeta = {
    bjp:        { emoji: '🪳', label: 'BJP Watch',      color: '#FF6600' },
    cjp:        { emoji: '⚖️', label: 'CJP Justice',    color: '#ff6b35' },
    politics:   { emoji: '🏛️', label: 'Politics',        color: '#e63946' },
    motivation: { emoji: '💪', label: 'Motivation',      color: '#fdcb6e' },
    science:    { emoji: '🔬', label: 'Science',         color: '#47d9ff' },
    sports:     { emoji: '⚽', label: 'Sports',          color: '#00b894' },
    technology: { emoji: '💻', label: 'Tech & AI',       color: '#a855f7' },
    facts:      { emoji: '🧠', label: 'Facts',           color: '#6c5ce7' },
    nature:     { emoji: '🌿', label: 'Nature',          color: '#43e97b' },
    rights:     { emoji: '🇮🇳', label: 'Citizen Rights', color: '#FF9933' },
    all:        { emoji: '🎲', label: 'Random Mix',      color: '#ff47a8' },
};
