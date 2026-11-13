// =============================================
// ShortsCraft 2.0 — main.js  (FINAL)
// Video backgrounds: Picsum Photos via seed-per-segment-per-generation
// Each generate click gets a fresh generationId = Date.now()
// → 100% unique images, CORS-safe, no API key
// =============================================

import { renderFrame } from './templates.js';
import { getRandomGradient, getRandomAccent, contentDB } from './generator.js';
import {
    topicMeta, topicBackgrounds, pageBackgrounds,
    startPreloadAll, getTotalLoaded, onLoadProgress,
    buildBgUrl, buildThumbUrl, getRandomPhotoId,
    buildVideoImageUrl, preloadVideoImages, getSegmentAccent,
    preloadTopicImages
} from './backgrounds.js';
import { generateMusic, getMoodName } from './music.js';

// ─────────────────────────────────────────────
// State
// ─────────────────────────────────────────────
const state = {
    selectedCategory : 'all',
    batchCount       : 5,
    selectedDuration : 60,
    isGenerating     : false,
    generatedQueue   : [],
    videoBlobs       : new Map(),
    musicBuffers     : new Map(),
    segmentImages    : new Map(), // videoId → [{img, accent}]
    history          : JSON.parse(localStorage.getItem('sc2-history') || '[]'),
    stats            : JSON.parse(localStorage.getItem('sc2-stats')   || '{"created":0,"exported":0}'),
};

// ─────────────────────────────────────────────
// Content DB
// ─────────────────────────────────────────────
const extendedContent = {
    bjp: [
        { text: "Electoral Bonds: BJP received ₹6,566 crore — 47% of all donations. Top donors got govt contracts worth lakhs of crore.", article: "Electoral Bond Scam", category: "Corruption", emoji: "💰" },
        { text: "India's press freedom: 140th in 2014 → 159th in 2024 under BJP. One of the sharpest global declines in 10 years.", article: "Press Freedom", category: "Media", emoji: "📰" },
        { text: "PM-CARES Fund: ₹10,000+ crore collected — NOT audited by CAG, NOT under RTI. Zero public accountability.", article: "PM-CARES", category: "Transparency", emoji: "❓" },
        { text: "UAPA arrests increased 72% under BJP. Most arrested: activists, journalists, students — not terrorists.", article: "UAPA Misuse", category: "Civil Liberties", emoji: "🔒" },
        { text: "Unemployment hit 45-year HIGH in 2023. BJP promised 2 crore jobs/year. 10 years later: net job creation is negative.", article: "Unemployment Crisis", category: "Economy", emoji: "📉" },
        { text: "Supreme Court ruled Electoral Bonds unconstitutional in Feb 2024. Largest political funding scandal in Indian history.", article: "SC Verdict", category: "Democracy", emoji: "⚖️" },
        { text: "Adani Group's wealth grew 1600% under BJP. Airports, ports, power plants — all went to PM's closest billionaire.", article: "Adani Connection", category: "Cronyism", emoji: "🤑" },
        { text: "Manipur: 200+ dead, 60,000+ displaced, churches burned. PM Modi was silent for 80+ days. Never visited.", article: "Manipur Crisis", category: "Accountability", emoji: "🔥" },
        { text: "Global Hunger Index 2023: India ranks 111 of 125. BJP called it a 'conspiracy'. 19 crore Indians go hungry daily.", article: "Hunger Index", category: "Development", emoji: "🌾" },
        { text: "Pegasus spyware: journalists, judges, opposition leaders surveilled. Govt refused SC-ordered inquiry.", article: "Pegasus Scandal", category: "Surveillance", emoji: "📱" },
        { text: "CAA excludes Muslims by religion — SC challenge pending 5+ years. Discriminatory by constitutional design.", article: "CAA Discrimination", category: "Constitution", emoji: "📜" },
        { text: "Demonetisation 2016: ₹1.5 lakh crore economic loss, 200+ deaths. 99.3% of banned notes returned — RBI confirmed.", article: "Demonetisation Disaster", category: "Economy", emoji: "💸" },
        { text: "Bulldozer Justice: demolishing homes of people merely accused — SC declared it unconstitutional.", article: "Bulldozer Raj", category: "Rule of Law", emoji: "🏗️" },
        { text: "India's billionaires doubled wealth during COVID. 23 crore fell below poverty line. Historic inequality peak.", article: "Wealth Inequality", category: "Economy", emoji: "📊" },
        { text: "ED raids: 95% of cases targeted opposition politicians. Critics call it the BJP 'washing machine'.", article: "ED Weaponised", category: "Vendetta", emoji: "🫧" },
        { text: "India is a democracy on paper. Under BJP: media captured, EC independence questioned, judiciary under pressure.", article: "Democratic Backslide", category: "Democracy", emoji: "🗳️" },
    ],
    cjp: [
        { text: "Citizens for Justice & Peace has filed 100+ PILs defending civil liberties across India since 2002.", article: "CJP Legacy", category: "Civil Rights", emoji: "⚖️" },
        { text: "NRC-NPR: 19 lakh excluded in Assam. CJP fought for 75,000+ people's citizenship rights in court.", article: "NRC Fight", category: "Citizenship", emoji: "🇮🇳" },
        { text: "UAPA misused to jail activists. CJP tracks every case and provides free legal aid across India.", article: "UAPA Watch", category: "Free Speech", emoji: "📢" },
        { text: "Hate Speech Tracker: CJP filed 1000+ complaints against hate speech targeting minorities since 2019.", article: "Hate Watch", category: "Communal Harmony", emoji: "🕊️" },
        { text: "Article 14: Every person in India has the right to equality before law. It's a right — not a privilege.", article: "Article 14", category: "Fundamental Rights", emoji: "⚖️" },
        { text: "CJP documented 2002 Gujarat violence evidence → conviction of 11 accused. Justice delayed but not denied.", article: "Gujarat 2002", category: "Justice", emoji: "🔥" },
        { text: "CAA protests 2020: CJP provided legal aid to 1,500+ protesters arrested across India.", article: "CAA Protests", category: "Protest Rights", emoji: "✊" },
        { text: "75% of India's prisoners are undertrials — awaiting trial for years. This is unconstitutional.", article: "Bail Crisis", category: "Justice Reform", emoji: "⚖️" },
        { text: "India ranks 159th of 180 in press freedom. CJP fights every journalist's case in court.", article: "Press Freedom", category: "Media Rights", emoji: "📰" },
        { text: "Article 22: Every person has the right to know why they're being arrested. Police cannot secretly detain you.", article: "Article 22", category: "Fundamental Rights", emoji: "👮" },
        { text: "RTI costs ₹10. You can demand answers from any government office. CJP helps you file — it's your power.", article: "RTI Act", category: "Citizen Power", emoji: "📋" },
        { text: "Electoral Bonds ruled unconstitutional. ₹16,000+ crore in anonymous donations exposed by CJP & journalists.", article: "Electoral Bonds", category: "Democracy", emoji: "💰" },
    ],
    politics: [
        { text: "33% of Indians didn't vote in 2024. Their silence shaped the election. Every vote counts.", article: "Voter Turnout", category: "Democracy", emoji: "🗳️" },
        { text: "40% of elected MPs have criminal cases pending. Always check before you vote: myneta.info", article: "Criminal MPs", category: "Accountability", emoji: "⚠️" },
        { text: "Electoral Bonds: ₹16,000+ crore in anonymous donations. SC ruled it unconstitutional in 2024.", article: "Electoral Bonds", category: "Political Funding", emoji: "💰" },
        { text: "Every Indian loses ₹18,000/year to corruption — money that should build schools and hospitals.", article: "Corruption Cost", category: "Awareness", emoji: "🤯" },
        { text: "India's 2019 elections cost ₹55,000 crore — the most expensive election in world history.", article: "Election Cost", category: "Political Facts", emoji: "💸" },
        { text: "Article 19: your right to speak, protest, and criticize the government is fundamental. Non-negotiable.", article: "Article 19", category: "Fundamental Rights", emoji: "🗣️" },
        { text: "NOTA: you can reject ALL candidates if none deserves your vote. It's your constitutional right.", article: "NOTA", category: "Voter Power", emoji: "✋" },
        { text: "Women's Reservation: 33% Parliament seats reserved for women under the 106th Constitutional Amendment.", article: "106th Amendment", category: "Women Power", emoji: "👩" },
    ],
    science: [
        { text: "CRISPR can cure genetic diseases. In 2023, the first CRISPR therapy for sickle cell was FDA-approved.", emoji: "🧬", stat: "2023" },
        { text: "James Webb Telescope sees galaxies 13.8 billion light-years away — near the Big Bang itself.", emoji: "🔭", stat: "13800000000" },
        { text: "mRNA vaccines could cure cancer within a decade. COVID-19 proved the platform works.", emoji: "💉", stat: "10" },
        { text: "Your brain 'washes' itself during deep sleep — clearing Alzheimer's-linked proteins. Sleep is medicine.", emoji: "🧠", stat: "7" },
        { text: "Quantum computers solve in seconds what classical computers would take millions of years.", emoji: "⚛️", stat: "1000000" },
        { text: "38 trillion bacteria live in your body. Your microbiome affects mood, immunity, and intelligence.", emoji: "🦠", stat: "38000000000000" },
        { text: "5,500+ exoplanets discovered. Statistically, billions could support some form of life.", emoji: "🪐", stat: "5500" },
        { text: "Light travels 299,792 km/s — fast enough to circle Earth 7.5 times in one second.", emoji: "💡", stat: "299792" },
    ],
    sports: [
        { text: "Usain Bolt's 9.58s 100m record from 2009 still stands. No human has come close.", emoji: "⚡", stat: "9.58" },
        { text: "Neeraj Chopra: 87.58m throw at Tokyo 2020 — India's first-ever Olympic athletics gold.", emoji: "🥇", stat: "87.58" },
        { text: "Virat Kohli: 80+ international centuries, 27,000+ runs. The greatest run-chaser in cricket history.", emoji: "🏏", stat: "80" },
        { text: "Lionel Messi scored 800+ career goals — once considered physically impossible for one player.", emoji: "⚽", stat: "800" },
        { text: "An F1 car generates enough downforce to drive upside-down at 270 km/h on a ceiling.", emoji: "🏎️", stat: "270" },
        { text: "Mary Kom: 6 World Boxing titles — more than any other boxer in history.", emoji: "🥊", stat: "6" },
        { text: "A tennis serve can reach 263 km/h — faster than most highway speed limits.", emoji: "🎾", stat: "263" },
    ],
    technology: [
        { text: "ChatGPT hit 100 million users in 2 months — fastest product adoption in human history.", emoji: "🤖", stat: "100000000" },
        { text: "AI will displace 85M jobs but create 97M new ones by 2025. Adapt or be left behind.", emoji: "🧠", stat: "97000000" },
        { text: "Your phone has more computing power than all NASA computers during the Moon landing — combined.", emoji: "📱", stat: "1000000" },
        { text: "Tesla Autopilot has driven 500M+ autonomous miles. Self-driving is already here.", emoji: "🚗", stat: "500000000" },
        { text: "The internet transmits 120 zettabytes of data per year — growing 23% annually.", emoji: "🌐", stat: "120" },
        { text: "30 years ago, 1TB storage cost $1.5 million. Today it costs less than ₹1,000.", emoji: "💾", stat: "1000" },
    ],
    nature: [
        { text: "The Amazon produces 20% of Earth's oxygen — and it's burning at 3× the normal rate.", emoji: "🌿", stat: "20" },
        { text: "3 trillion trees on Earth. Humans cut 15 billion per year — net loss every single year.", emoji: "🌲", stat: "15000000000" },
        { text: "The Mariana Trench is 10,994m deep — deeper than Everest is tall. Less than 5% explored.", emoji: "🌊", stat: "10994" },
        { text: "Without bees, 70% of global food supply collapses. They pollinate everything we eat.", emoji: "🐝", stat: "70" },
        { text: "Coral reefs cover 0.1% of the ocean floor but support 25% of ALL marine species.", emoji: "🪸", stat: "25" },
        { text: "The Arctic warms 3× faster than the global average. Ice-free summers possible by 2035.", emoji: "🧊", stat: "2035" },
        { text: "A single large tree absorbs 22kg of CO₂ per year and lives hundreds of years. Plant one.", emoji: "🌳", stat: "22" },
    ],
};

const fullContent = { ...contentDB, ...extendedContent };

// ─────────────────────────────────────────────
// Canvas refs
// ─────────────────────────────────────────────
const liveCanvas   = document.getElementById('live-canvas');
const liveCtx      = liveCanvas   ? liveCanvas.getContext('2d')   : null;
const renderCanvas = document.getElementById('render-canvas');
const renderCtx    = renderCanvas ? renderCanvas.getContext('2d') : null;

// ─────────────────────────────────────────────
// PAGE BACKGROUND ROTATION (CSS only, no canvas)
// ─────────────────────────────────────────────
let bgSlotActive  = 0;
let bgRotateTimer = null;
const bgUsed      = new Map();

function getNextPageBg(topic) {
    const pool = pageBackgrounds[topic] || pageBackgrounds.all;
    if (!bgUsed.has(topic)) bgUsed.set(topic, 0);
    const idx = bgUsed.get(topic) % pool.length;
    bgUsed.set(topic, idx + 1);
    return pool[idx];
}

function setPageBackground(topic) {
    const url     = getNextPageBg(topic);
    const nextSlot = 1 - bgSlotActive;
    const curEl    = document.getElementById(`bg-slide-${bgSlotActive}`);
    const nextEl   = document.getElementById(`bg-slide-${nextSlot}`);
    if (!curEl || !nextEl) return;
    nextEl.style.backgroundImage = `url("${url}")`;
    requestAnimationFrame(() => {
        nextEl.classList.add('active');
        curEl.classList.remove('active');
        bgSlotActive = nextSlot;
    });
    const labelEl = document.getElementById('live-bg-label');
    if (labelEl) {
        const meta = topicMeta[topic] || topicMeta.all;
        labelEl.textContent = `${meta.emoji} ${meta.label}`;
    }
}

function startBgRotation(topic, ms = 5000) {
    stopBgRotation();
    setPageBackground(topic);
    bgRotateTimer = setInterval(() => setPageBackground(topic), ms);
}
function stopBgRotation() {
    if (bgRotateTimer) { clearInterval(bgRotateTimer); bgRotateTimer = null; }
}

// ─────────────────────────────────────────────
// Content retrieval
// ─────────────────────────────────────────────
function getContent(cat, count) {
    const pool = fullContent[cat] || fullContent.motivation || [];
    return [...pool].sort(() => Math.random() - 0.5).slice(0, Math.min(count, pool.length));
}

// ─────────────────────────────────────────────
// Music
// ─────────────────────────────────────────────
async function getMusic(cat) {
    if (state.musicBuffers.has(cat)) return state.musicBuffers.get(cat);
    try { const b = await generateMusic(cat, 10); state.musicBuffers.set(cat, b); return b; }
    catch { return null; }
}

// ─────────────────────────────────────────────
// UI helpers
// ─────────────────────────────────────────────
function setLabel(txt) { const el = document.getElementById('progress-label'); if (el) el.textContent = txt; }
function setCount(txt) { const el = document.getElementById('progress-count'); if (el) el.textContent = txt; }
function setFill(pct)  { const el = document.getElementById('progress-fill');  if (el) el.style.width  = `${pct}%`; }

// ─────────────────────────────────────────────
// ✅ MAIN GENERATE FLOW
// ─────────────────────────────────────────────
async function startAutoGenerate() {
    if (state.isGenerating) return;
    state.isGenerating = true;

    // NEW generationId every click = fresh Picsum seeds = DIFFERENT images
    const genId = String(Date.now());

    document.getElementById('btn-auto-generate')?.classList.add('generating');
    document.getElementById('batch-progress')?.classList.remove('hidden');
    document.getElementById('queue-preview')?.classList.add('hidden');
    document.getElementById('done-area')?.classList.add('hidden');
    setFill(0);

    const templateMap = {
        bjp: 'rights', cjp: 'rights', politics: 'rights', motivation: 'quotes',
        facts: 'facts', tips: 'tips', trending: 'trending', poems: 'poems',
        science: 'facts', sports: 'trending', technology: 'trending',
        nature: 'facts', animation: 'animation', rights: 'rights', all: 'quotes',
    };
    const segDurMap = {
        bjp: 10, cjp: 10, politics: 10, motivation: 7, facts: 9, tips: 8,
        science: 9, sports: 7, technology: 8, nature: 9, trending: 8, poems: 10, rights: 10,
    };

    const allCats   = Object.keys(fullContent).filter(k => k !== 'animation');
    const cat       = state.selectedCategory;
    const videoPlans = Array.from({ length: state.batchCount }, () =>
        cat === 'all' ? allCats[Math.floor(Math.random() * allCats.length)] : cat
    );
    const neededCats = [...new Set(videoPlans)];

    // ── STEP 1: Music ─────────────────────────
    setLabel('🎵 Generating music…');
    setFill(5);
    for (const c of neededCats) await getMusic(c);

    // ── STEP 2: Build video plans + preload images ──
    setFill(10);
    const batch = [];
    state.segmentImages.clear();

    for (let i = 0; i < videoPlans.length; i++) {
        const useCat = videoPlans[i];
        const meta   = topicMeta[useCat] || topicMeta.all;
        const segDur = segDurMap[useCat] || 8;
        const segCnt = Math.max(2, Math.ceil(state.selectedDuration / segDur));

        setLabel(`📷 Loading ${meta.emoji} ${meta.label} — Video ${i + 1}/${videoPlans.length} (${segCnt} unique images)…`);
        setFill(10 + (i / videoPlans.length) * 55);

        // ✅ Picsum: unique URL per segment per generationId
        const segImgs = await preloadVideoImages(useCat, segCnt, genId + '-v' + i, (done, tot) => {
            setLabel(`📷 ${meta.emoji} ${meta.label} video ${i + 1}: ${done}/${tot} images…`);
        });

        const items   = getContent(useCat, segCnt);
        const shortId = Date.now() + i;

        const segments = items.map((content, idx) => {
            const { img, accent } = segImgs[idx] || { img: null, accent: getSegmentAccent(useCat, idx) };
            return {
                content,
                style: {
                    gradient:        getRandomGradient(),
                    textColor:       '#ffffff',
                    accentColor:     accent,
                    backgroundImage: img || null,
                },
                templateId: templateMap[useCat] || 'quotes',
                duration:   segDur,
            };
        });

        const uniqueBgs = segImgs.filter(s => s.img).length;
        batch.push({
            id:              shortId,
            category:        useCat,
            content:         segments[0]?.content || items[0],
            style:           segments[0]?.style   || { gradient: getRandomGradient(), textColor: '#fff', accentColor: meta.color },
            duration:        state.selectedDuration,
            segmentDuration: segDur,
            segments,
            templateId:      templateMap[useCat] || 'quotes',
            uniqueBgs,
        });
    }

    state.generatedQueue = batch;
    state.videoBlobs.clear();

    // ── STEP 3: Render videos ─────────────────
    for (let i = 0; i < batch.length; i++) {
        const short = batch[i];
        const meta  = topicMeta[short.category] || topicMeta.all;
        setLabel(`🎬 Rendering ${i + 1}/${batch.length} — ${meta.emoji} ${meta.label} · 🖼️ ${short.uniqueBgs} unique images`);
        setCount(`${i + 1}/${batch.length}`);
        setFill(65 + ((i + 0.5) / batch.length) * 35);

        document.getElementById('current-title').textContent = getShortTitle(short);
        document.getElementById('current-text').textContent  = short.content.text?.substring(0, 100) || '';
        document.getElementById('current-badge').textContent =
            `${meta.emoji} ${meta.label} · 🖼️ ${short.uniqueBgs} BGs · 🎵 ${getMoodName(short.category)}`;

        const blob = await recordVideo(short);
        state.videoBlobs.set(short.id, blob);
        setFill(65 + ((i + 1) / batch.length) * 35);
        state.stats.created++;
        updateStats();
    }

    saveStats();
    setFill(100);
    document.getElementById('batch-progress')?.classList.add('hidden');
    document.getElementById('btn-auto-generate')?.classList.remove('generating');
    state.isGenerating = false;
    showQueuePreview();
}

// ─────────────────────────────────────────────
// Record one video
// ─────────────────────────────────────────────
function recordVideo(short) {
    return new Promise(async (resolve) => {
        const fps         = 30;
        const totalFrames = short.duration * fps;
        const segments    = short.segments;
        const segDur      = short.segmentDuration;
        let frame = 0;

        const musicBuf = await getMusic(short.category);
        const audioCtx = new AudioContext({ sampleRate: 44100 });
        const dest     = audioCtx.createMediaStreamDestination();
        if (musicBuf) {
            const src  = audioCtx.createBufferSource();
            src.buffer = musicBuf; src.loop = true;
            src.connect(dest); src.start(0);
        }

        const videoStream = renderCanvas.captureStream(fps);
        const combined    = new MediaStream();
        videoStream.getVideoTracks().forEach(t => combined.addTrack(t));
        if (musicBuf) dest.stream.getAudioTracks().forEach(t => combined.addTrack(t));

        const chunks = [];
        let mime = 'video/webm;codecs=vp9,opus';
        if (!MediaRecorder.isTypeSupported(mime)) mime = 'video/webm;codecs=vp8,opus';
        if (!MediaRecorder.isTypeSupported(mime)) mime = 'video/webm';

        const rec = new MediaRecorder(combined, { mimeType: mime, videoBitsPerSecond: 5_000_000 });
        rec.ondataavailable = e => { if (e.data.size > 0) chunks.push(e.data); };
        rec.onstop = () => { audioCtx.close(); resolve(new Blob(chunks, { type: 'video/webm' })); };
        rec.start();

        function nextFrame() {
            if (frame >= totalFrames) { rec.stop(); return; }
            const t      = frame / fps;
            const segIdx = Math.min(Math.floor(t / segDur), segments.length - 1);
            const seg    = segments[segIdx];
            const segT   = t - segIdx * segDur;

            renderFrame(renderCtx, seg.templateId, segT, segDur, seg.content, seg.style);
            renderFrame(liveCtx,   seg.templateId, segT, segDur, seg.content, seg.style);

            const segEl = document.getElementById('current-title');
            if (segEl) segEl.textContent = `Segment ${segIdx + 1}/${segments.length}`;

            frame++;
            requestAnimationFrame(nextFrame);
        }
        nextFrame();
    });
}

// ─────────────────────────────────────────────
// Queue Preview
// ─────────────────────────────────────────────
function showQueuePreview() {
    document.getElementById('queue-preview')?.classList.remove('hidden');
    const listEl = document.getElementById('queue-list');
    if (!listEl) return;

    listEl.innerHTML = state.generatedQueue.map((short, i) => {
        const meta = topicMeta[short.category] || topicMeta.all;
        const mood = getMoodName(short.category);
        return `
        <div class="queue-card" style="animation-delay:${i * 0.08}s">
          <div class="queue-card-preview" data-id="${short.id}" data-idx="${i}">
            <div class="play-overlay"><svg viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg></div>
            <canvas id="qc-${i}" width="1080" height="1920"></canvas>
          </div>
          <div class="queue-card-info">
            <span class="queue-cat">${meta.emoji} ${short.category}</span>
            <span class="music-badge">🖼️ ${short.uniqueBgs} unique BGs · 🎵 ${mood}</span>
            <div class="queue-text">${short.content.text.substring(0, 80)}</div>
          </div>
        </div>`;
    }).join('');

    state.generatedQueue.forEach((short, i) => {
        const canvas = document.getElementById(`qc-${i}`);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const mid = short.segments[Math.floor(short.segments.length / 2)] || short.segments[0];
        if (mid) renderFrame(ctx, short.templateId, short.duration * 0.4, short.duration, short.content, mid.style);
    });

    listEl.querySelectorAll('.queue-card-preview').forEach(el =>
        el.addEventListener('click', () => openModal(+el.dataset.id, +el.dataset.idx)));
}

// ─────────────────────────────────────────────
// Video Modal
// ─────────────────────────────────────────────
function openModal(id, idx) {
    const blob  = state.videoBlobs.get(id);
    const short = state.generatedQueue.find(s => s.id === id);
    if (!blob || !short) return;

    const modal = document.getElementById('video-modal');
    const video = document.getElementById('video-player');
    const url   = URL.createObjectURL(blob);
    video.src   = url;
    video.onloadeddata = () => video.play();

    const meta = topicMeta[short.category] || topicMeta.all;
    document.getElementById('video-info-badge').textContent =
        `${meta.emoji} ${short.category} · 🖼️ ${short.uniqueBgs} BGs · 🎵 ${getMoodName(short.category)}`;
    document.getElementById('video-info-title').textContent = getShortTitle(short);
    document.getElementById('video-info-text').textContent  = short.content.text;
    modal.dataset.url  = url;
    modal.dataset.name = `short-${short.category}-${idx + 1}-${Date.now()}.webm`;
    modal.classList.remove('hidden');
}

function closeModal() {
    const modal = document.getElementById('video-modal');
    const video = document.getElementById('video-player');
    video.pause(); video.src = '';
    if (modal.dataset.url) URL.revokeObjectURL(modal.dataset.url);
    modal.classList.add('hidden');
}

function dlFile(url, name) {
    const a = Object.assign(document.createElement('a'), { href: url, download: name, style: 'display:none' });
    document.body.appendChild(a); a.click();
    setTimeout(() => document.body.removeChild(a), 200);
}

// ─────────────────────────────────────────────
// Export All
// ─────────────────────────────────────────────
async function exportAll() {
    document.getElementById('batch-progress')?.classList.remove('hidden');
    document.getElementById('queue-preview')?.classList.add('hidden');
    setFill(0);

    for (let i = 0; i < state.generatedQueue.length; i++) {
        const s = state.generatedQueue[i];
        setLabel(`⬇️ Exporting ${i + 1}/${state.generatedQueue.length}…`);
        setFill(((i + 1) / state.generatedQueue.length) * 100);
        const blob = state.videoBlobs.get(s.id);
        if (blob) {
            const url = URL.createObjectURL(blob);
            dlFile(url, `short-${s.category}-${i + 1}-${Date.now()}.webm`);
            setTimeout(() => URL.revokeObjectURL(url), 4000);
        }
        state.stats.exported++;
        await new Promise(r => setTimeout(r, 1500));
    }
    updateStats(); saveStats();
    state.generatedQueue.forEach(s => {
        state.history.unshift({ ...s, exportedAt: new Date().toISOString() });
    });
    state.history = state.history.slice(0, 50);
    localStorage.setItem('sc2-history', JSON.stringify(state.history));
    document.getElementById('batch-progress')?.classList.add('hidden');
    document.getElementById('done-area')?.classList.remove('hidden');
    const doneEl = document.getElementById('done-count');
    if (doneEl) doneEl.textContent = state.generatedQueue.length;
    renderGallery();
}

// ─────────────────────────────────────────────
// Gallery
// ─────────────────────────────────────────────
function renderGallery() {
    const grid = document.getElementById('gallery-grid');
    if (!grid) return;
    if (!state.history.length) {
        grid.innerHTML = `<div class="gallery-empty"><p>No videos yet — generate your first batch!</p></div>`;
        return;
    }
    grid.innerHTML = state.history.map((s, i) => {
        const meta = topicMeta[s.category] || topicMeta.all;
        const date = new Date(s.exportedAt).toLocaleDateString();
        return `<div class="gallery-card">
          <div class="gallery-card-preview"><canvas id="gc-${i}" width="1080" height="1920"></canvas></div>
          <div class="gallery-card-info"><span>${meta.emoji} ${s.category} · ${date}</span></div>
        </div>`;
    }).join('');

    state.history.forEach((s, i) => {
        const c = document.getElementById(`gc-${i}`);
        if (!c) return;
        renderFrame(c.getContext('2d'), s.templateId, s.duration * 0.3, s.duration, s.content, s.style);
    });
}

// ─────────────────────────────────────────────
// Category card thumbnails
// ─────────────────────────────────────────────
function loadCategoryPreviews() {
    Object.keys(pageBackgrounds).forEach(topic => {
        const el = document.getElementById(`prev-${topic}`);
        if (!el) return;
        const pool = pageBackgrounds[topic];
        if (!pool?.length) return;
        const url = pool[Math.floor(Math.random() * Math.min(3, pool.length))];
        el.style.backgroundImage = `url("${buildThumbUrl(url)}")`;
        el.classList.add('loaded');
    });
}

// ─────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────
function getShortTitle(short) {
    const cat = short.category;
    if (cat === 'poems')      return `📝 ${short.content.title || 'Poem'}`;
    if (cat === 'motivation') return `"${short.content.text?.substring(0, 40)}…"`;
    if (['bjp','politics','rights','cjp'].includes(cat))
        return `${(topicMeta[cat] || topicMeta.all).emoji} ${short.content.article || short.content.category || cat}`;
    if (['facts','science','nature','technology','sports'].includes(cat))
        return `${short.content.emoji || '🧠'} ${short.content.text?.substring(0, 40)}…`;
    return short.content.text?.substring(0, 40) || cat;
}

function updateStats() {
    const c = document.getElementById('stat-created');
    const e = document.getElementById('stat-exported');
    if (c) c.textContent = state.stats.created;
    if (e) e.textContent = state.stats.exported;
}
function saveStats() { localStorage.setItem('sc2-stats', JSON.stringify(state.stats)); }

// ─────────────────────────────────────────────
// Nav / Controls init
// ─────────────────────────────────────────────
function initNav() {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.getElementById(`page-${btn.dataset.page}`)?.classList.add('active');
        });
    });
}
function initCategories() {
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', () => {
            document.querySelectorAll('.category-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            state.selectedCategory = card.dataset.cat;
            startBgRotation(state.selectedCategory, 5000);
        });
    });
}
function initCountSelector() {
    document.querySelectorAll('.count-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.count-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.batchCount = parseInt(btn.dataset.count);
        });
    });
}
function initDurationSelector() {
    document.querySelectorAll('.duration-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.duration-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.selectedDuration = parseInt(btn.dataset.duration);
        });
    });
}
function initEvents() {
    document.getElementById('btn-auto-generate')?.addEventListener('click', startAutoGenerate);
    document.getElementById('btn-export-all')?.addEventListener('click', exportAll);
    document.getElementById('btn-regenerate')?.addEventListener('click', () => {
        document.getElementById('queue-preview')?.classList.add('hidden');
        startAutoGenerate();
    });
    document.getElementById('btn-make-more')?.addEventListener('click', () =>
        document.getElementById('done-area')?.classList.add('hidden'));
    document.getElementById('modal-close')?.addEventListener('click', closeModal);
    document.getElementById('modal-backdrop')?.addEventListener('click', closeModal);
    document.getElementById('btn-download-single')?.addEventListener('click', () => {
        const m = document.getElementById('video-modal');
        if (m?.dataset.url) dlFile(m.dataset.url, m.dataset.name);
    });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
}

// ─────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────
function init() {
    initNav();
    initCategories();
    initCountSelector();
    initDurationSelector();
    initEvents();
    updateStats();
    renderGallery();
    startBgRotation('all', 5000);
    setTimeout(loadCategoryPreviews, 400);

    const sub = document.getElementById('mega-btn-sub');
    if (sub) sub.textContent = '✅ Ready! Every segment gets a unique background — guaranteed';
}

document.fonts.ready.then(() => init());
