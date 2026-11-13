// AniList GraphQL API — completely free, no API key required
// Provides trending anime metadata to enrich video cards

const ANILIST_API = 'https://graphql.anilist.co';

const TRENDING_QUERY = `
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: TRENDING_DESC, status: RELEASING) {
      id
      title { romaji english native }
      coverImage { large medium color }
      bannerImage
      averageScore
      popularity
      trending
      episodes
      status
      genres
      season
      seasonYear
      trailer { id site }
      siteUrl
      description(asHtml: false)
    }
  }
}`;

export async function getTrendingAnime(page = 1, perPage = 20) {
  try {
    const res = await fetch(ANILIST_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ query: TRENDING_QUERY, variables: { page, perPage } }),
      signal: AbortSignal.timeout(10000),
    });
    const json = await res.json();
    const media = json?.data?.Page?.media || [];

    return media.map(m => {
      const ytTrailer = (m.trailer?.site === 'youtube' && m.trailer?.id)
        ? `https://www.youtube.com/watch?v=${m.trailer.id}`
        : '';

      return {
        id: `anilist-${m.id}`,
        platform: 'anilist',
        title: m.title.english || m.title.romaji,
        titleJP: m.title.native,
        thumbnail: m.coverImage?.large || m.coverImage?.medium || '',
        bannerImage: m.bannerImage || '',
        score: m.averageScore,
        popularity: m.popularity,
        trending: m.trending,
        genres: m.genres || [],
        episodes: m.episodes,
        status: m.status,
        season: m.season,
        seasonYear: m.seasonYear,
        trailerUrl: ytTrailer ? `https://www.youtube.com/embed/${m.trailer.id}` : '',
        siteUrl: m.siteUrl,
        description: m.description?.replace(/<[^>]+>/g, '') || '',
        color: m.coverImage?.color || '#8b5cf6',
        source: 'AniList',
        views: m.popularity,
        likes: m.trending,
        url: ytTrailer || m.siteUrl,
        embedUrl: ytTrailer ? `https://www.youtube.com/embed/${m.trailer.id}` : '',
        duration: m.episodes ? `${m.episodes} eps` : '',
      };
    });
  } catch (e) {
    console.error('AniList API error:', e);
    return [];
  }
}

export async function searchAnime(query, page = 1) {
  const SEARCH_QUERY = `
  query ($search: String, $page: Int) {
    Page(page: $page, perPage: 15) {
      media(type: ANIME, search: $search, sort: POPULARITY_DESC) {
        id title { romaji english } coverImage { large color }
        averageScore popularity genres trailer { id site } siteUrl
      }
    }
  }`;
  try {
    const res = await fetch(ANILIST_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: SEARCH_QUERY, variables: { search: query, page } }),
    });
    const json = await res.json();
    return json?.data?.Page?.media || [];
  } catch { return []; }
}
