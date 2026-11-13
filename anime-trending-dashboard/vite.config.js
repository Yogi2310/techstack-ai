import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    proxy: {
      // Piped API proxy (CORS bypass for YouTube data)
      '/proxy/piped': {
        target: 'https://pipedapi.kavin.rocks',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/proxy\/piped/, ''),
        secure: true,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            proxyReq.setHeader('Origin', 'https://piped.kavin.rocks');
            proxyReq.setHeader('Referer', 'https://piped.kavin.rocks/');
          });
        },
      },
      // Reddit JSON proxy
      '/proxy/reddit': {
        target: 'https://www.reddit.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/proxy\/reddit/, ''),
        secure: true,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            proxyReq.setHeader('User-Agent', 'AniTrend/1.0 (anime trending dashboard)');
            proxyReq.removeHeader('Origin');
            proxyReq.removeHeader('Referer');
          });
        },
      },
    },
  },
});
