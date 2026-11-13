// YouTube via multiple free CORS-friendly approaches:
// 1. YouTube RSS feeds (no key, CORS-friendly via rss2json)
// 2. Piped fallback instances

const RSS2JSON = 'https://api.rss2json.com/v1/api.json?rss_url=';

// YouTube search RSS (uses public YouTube search feed)
const YOUTUBE_RSS_QUERIES = [
  'https://www.youtube.com/feeds/videos.xml?search_term=anime+amv+2024',
  'https://www.youtube.com/feeds/videos.xml?search_term=anime+edit+trending',
  'https://www.youtube.com/feeds/videos.xml?search_term=anime+fight+scene+2024',
];

// Popular anime YouTube channels RSS
const ANIME_CHANNEL_FEEDS = [
  'https://www.youtube.com/feeds/videos.xml?channel_id=UCddiUEpeqJcYeBxX1IVBKvQ', // Crunchyroll
  'https://www.youtube.com/feeds/videos.xml?channel_id=UC0wNSTMWIL3qaorLx0jie6A', // AniplexUSA
];

async function fetchYouTubeRSS(feedUrl) {
  const apiUrl = `${RSS2JSON}${encodeURIComponent(feedUrl)}&count=15&api_key=`;
  const res = await fetch(apiUrl, { signal: AbortSignal.timeout(10000) });
  if (!res.ok) throw new Error(`RSS2JSON ${res.status}`);
  const data = await res.json();
  if (data.status !== 'ok') throw new Error(data.message || 'RSS error');
  return data.items || [];
}

async function fetchPipedSearch(query) {
  const instances = [
    '/proxy/piped',
    'https://pipedapi.adminforge.de',
    'https://pipedapi.kavin.rocks',
    'https://api.piped.yt',
  ];
  for (const base of instances) {
    try {
      const params = new URLSearchParams({ q: query, filter: 'videos' });
      const res = await fetch(`${base}/search?${params}`, {
        headers: { Accept: 'application/json' },
        signal: AbortSignal.timeout(8000),
      });
      if (!res.ok) continue;
      const data = await res.json();
      const results = parsePipedResults(data);
      if (results.length > 0) return results;
    } catch {}
  }
  return [];
}

export async function getTrendingAnime() {
  // Strategy 1: Local backend feed via yt-dlp
  try {
    const res = await fetch('http://127.0.0.1:3001/api/feed?type=trending', { signal: AbortSignal.timeout(10000) });
    if (res.ok) {
      const items = await res.json();
      if (items.length > 0) return items;
    }
  } catch {}

  // Strategy 2: YouTube channel RSS feeds
  try {
    const feed = ANIME_CHANNEL_FEEDS[Math.floor(Math.random() * ANIME_CHANNEL_FEEDS.length)];
    const items = await fetchYouTubeRSS(feed);
    if (items.length > 0) return parseRSSItems(items);
  } catch (e) {
    console.warn('YouTube RSS failed:', e.message);
  }

  // Strategy 3: Piped search
  const queries = ['anime amv 2026', 'anime edit trending', 'anime fight scene'];
  const q = queries[Math.floor(Date.now() / 3600000) % queries.length];
  try {
    const results = await fetchPipedSearch(q);
    if (results.length > 0) return results;
  } catch (e) {
    console.warn('Piped search failed:', e.message);
  }

  return [];
}

export async function getShortsAnime() {
  // Strategy 1: Local backend feed via yt-dlp
  try {
    const res = await fetch('http://127.0.0.1:3001/api/feed?type=shorts', { signal: AbortSignal.timeout(10000) });
    if (res.ok) {
      const items = await res.json();
      if (items.length > 0) return items;
    }
  } catch {}

  // Fallback to Piped search for shorts
  try {
    const results = await fetchPipedSearch('anime shorts edit #animeshorts');
    return results.map(r => ({ ...r, platform: 'shorts', source: 'YouTube Shorts' }));
  } catch {}

  return [];
}

export async function searchAnimeVideos(query = 'anime') {
  // Try Piped first for search (better CORS support)
  const piped = await fetchPipedSearch(query);
  if (piped.length > 0) return piped;

  // Fallback to RSS search
  try {
    const feedUrl = `https://www.youtube.com/feeds/videos.xml?search_term=${encodeURIComponent(query)}`;
    const items = await fetchYouTubeRSS(feedUrl);
    return parseRSSItems(items);
  } catch {}
  return [];
}

function parseRSSItems(items) {
  return items.map(item => {
    // Extract video ID from YouTube URL
    const videoId = item.link?.match(/v=([^&]+)/)?.[1] ||
      item.guid?.match(/([a-zA-Z0-9_-]{11})$/)?.[1] || '';

    return {
      id: videoId || `yt-${Math.random().toString(36).slice(2)}`,
      platform: 'youtube',
      title: item.title || '',
      thumbnail: item.thumbnail || (videoId ? `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg` : ''),
      channelName: item.author || '',
      views: 0,
      likes: 0,
      duration: '',
      publishedAt: item.pubDate ? new Date(item.pubDate).toISOString() : '',
      url: `https://www.youtube.com/watch?v=${videoId}`,
      embedUrl: videoId ? `https://www.youtube.com/embed/${videoId}` : '',
      description: item.description?.replace(/<[^>]+>/g, '').slice(0, 200) || '',
      source: 'YouTube (RSS)',
    };
  }).filter(v => v.id && v.title);
}

function parsePipedResults(data) {
  return (data?.items || [])
    .filter(v => v.url?.startsWith('/watch') || v.type === 'stream')
    .slice(0, 20)
    .map(v => {
      const videoId = (v.url || '').replace('/watch?v=', '');
      return {
        id: videoId || `yt-${Math.random().toString(36).slice(2)}`,
        platform: 'youtube',
        title: v.title || 'Untitled',
        thumbnail: v.thumbnail || `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`,
        channelName: v.uploaderName || '',
        views: v.views || 0,
        likes: 0,
        duration: formatSeconds(v.duration || 0),
        publishedAt: v.uploaded ? new Date(v.uploaded).toISOString() : '',
        url: `https://www.youtube.com/watch?v=${videoId}`,
        embedUrl: `https://www.youtube.com/embed/${videoId}`,
        description: v.shortDescription || '',
        source: 'YouTube (Piped)',
      };
    });
}

function formatSeconds(s) {
  if (!s) return '';
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
  if (h > 0) return `${h}:${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
  return `${m}:${String(sec).padStart(2,'0')}`;
}
