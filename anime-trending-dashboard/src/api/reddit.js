// Reddit — Use RSS feeds + multiple fallback strategies
// RSS is more reliable than JSON API for unauthenticated requests

const SUBREDDITS = ['anime', 'AnimeMemes', 'AnimeEdits', 'animegifs'];

// RSS to JSON converters (free public services)
const RSS2JSON = 'https://api.rss2json.com/v1/api.json?rss_url=';

async function fetchSubredditRSS(subreddit) {
  const rssUrl = `https://www.reddit.com/r/${subreddit}/top/.rss?t=week&limit=20`;
  const apiUrl = `${RSS2JSON}${encodeURIComponent(rssUrl)}&count=20`;

  const res = await fetch(apiUrl, { signal: AbortSignal.timeout(10000) });
  if (!res.ok) throw new Error(`RSS2JSON ${res.status}`);
  const data = await res.json();
  if (data.status !== 'ok') throw new Error(data.message || 'RSS error');
  return data.items || [];
}

async function fetchSubredditJSON(subreddit) {
  const urls = [
    `/proxy/reddit/r/${subreddit}/top.json?t=week&limit=20&raw_json=1`,
    `https://www.reddit.com/r/${subreddit}/top.json?t=week&limit=20&raw_json=1`,
  ];
  for (const url of urls) {
    try {
      const res = await fetch(url, {
        headers: { Accept: 'application/json' },
        signal: AbortSignal.timeout(8000),
      });
      if (!res.ok) continue;
      const data = await res.json();
      if (data?.data?.children?.length > 0) return parseJSONPosts(data);
    } catch {}
  }
  return null;
}

export async function getTrendingAnime(subreddit = 'anime') {
  // Strategy 1: RSS via rss2json (most reliable)
  try {
    const items = await fetchSubredditRSS(subreddit);
    if (items.length > 0) return parseRSSItems(items, subreddit);
  } catch (e) {
    console.warn(`Reddit RSS r/${subreddit}:`, e.message);
  }

  // Strategy 2: JSON with corsproxy
  try {
    const posts = await fetchSubredditJSON(subreddit);
    if (posts) return posts;
  } catch (e) {
    console.warn(`Reddit JSON r/${subreddit}:`, e.message);
  }

  return [];
}

export async function getAllSubreddits() {
  const results = await Promise.allSettled(
    SUBREDDITS.slice(0, 3).map(sub => getTrendingAnime(sub))
  );
  return results.flatMap(r => r.status === 'fulfilled' ? r.value : []);
}

function parseRSSItems(items, subreddit) {
  return items.map(item => {
    // Extract thumbnail from content
    const thumbMatch = item.content?.match(/<img[^>]+src="([^"]+)"/);
    const thumbnail = thumbMatch ? thumbMatch[1] : item.thumbnail || '';

    // Extract YouTube video ID from link
    const ytMatch = item.link?.match(/(?:youtu\.be\/|youtube\.com\/watch\?v=)([^&?]+)/);
    const embedUrl = ytMatch ? `https://www.youtube.com/embed/${ytMatch[1]}` : '';

    return {
      id: `reddit-${btoa(item.guid || item.link || Math.random().toString()).slice(0, 12)}`,
      platform: 'reddit',
      title: item.title?.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>') || '',
      thumbnail: thumbnail.startsWith('http') ? thumbnail : '',
      channelName: `u/${item.author || 'unknown'}`,
      views: 0,
      likes: 0,
      comments: 0,
      duration: '',
      publishedAt: item.pubDate ? new Date(item.pubDate).toISOString() : '',
      url: item.link || `https://reddit.com/r/${subreddit}`,
      embedUrl,
      description: '',
      subreddit,
      source: `r/${subreddit}`,
      flair: item.categories?.[0] || '',
    };
  }).filter(p => p.title);
}

function parseJSONPosts(data) {
  return (data?.data?.children || []).map(p => {
    const d = p.data;
    const previews = d.preview?.images?.[0]?.resolutions || [];
    const thumb =
      previews[previews.length - 1]?.url?.replace(/&amp;/g, '&') ||
      d.preview?.images?.[0]?.source?.url?.replace(/&amp;/g, '&') ||
      (d.thumbnail?.startsWith('http') ? d.thumbnail : '');
    const ytMatch = d.url?.match(/(?:youtu\.be\/|youtube\.com\/watch\?v=)([^&?]+)/);
    return {
      id: `reddit-${d.id}`,
      platform: 'reddit',
      title: d.title,
      thumbnail: thumb,
      channelName: `u/${d.author}`,
      views: d.score || 0,
      likes: d.ups || 0,
      comments: d.num_comments || 0,
      duration: '',
      publishedAt: new Date(d.created_utc * 1000).toISOString(),
      url: `https://reddit.com${d.permalink}`,
      embedUrl: ytMatch ? `https://www.youtube.com/embed/${ytMatch[1]}` : '',
      description: d.selftext || '',
      subreddit: d.subreddit,
      source: `r/${d.subreddit}`,
    };
  });
}
