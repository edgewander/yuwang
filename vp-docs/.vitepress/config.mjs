import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: '狱望 Prison Art',
  description: '汇集监狱与人文艺术相关的内容，探讨人性、救赎与自由。',
  ignoreDeadLinks: true,

  head: [
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Noto+Serif+SC:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap' }],
    ['meta', { name: 'theme-color', content: '#0e0c0b' }],
    ['meta', { property: 'og:site_name', content: '狱望 Prison Art' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:locale', content: 'zh_CN' }],
    ['meta', { property: 'og:url', content: 'https://prison-art.cn' }],
    ['link', { rel: 'icon', type: 'image/webp', href: '/images/logo.webp' }],
  ],

  cleanUrls: true,

  sitemap: {
    hostname: 'https://prison-art.cn',
  },

  themeConfig: {
    logo: '/images/logo.webp',
    siteTitle: '狱望 Prison Art',

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索文章', buttonAriaLabel: '搜索' },
          modal: {
            noResultsText: '没有找到相关内容',
            resetButtonTitle: '清除搜索条件',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },

    nav: [
      { text: '首页', link: '/' },
      { text: '全部文章', link: '/cat-art' },
      {
        text: '监狱地图',
        link: 'https://map.prison-art.cn',
      },
    ],

    sidebar: [
      { text: '首页', link: '/' },
      { type: 'separator' },
      {
        items: [
          { text: '艺术介入监狱', link: '/cat-art' },
          { text: '监狱摄影', link: '/cat-photo' },
          { text: '监狱绘画', link: '/cat-painting' },
          { text: '监狱诗歌', link: '/cat-poetry' },
          { text: '监狱旅游', link: '/cat-travel' },
          { text: '监狱历史', link: '/cat-history' },
          { text: '监狱音乐', link: '/cat-music' },
          { text: '杂谈', link: '/cat-misc' },
          { text: '播客', link: '/podcast' },
        ],
      },
      { type: 'separator' },
      {
        items: [
          { text: '投稿', link: '/contribute' },
        ],
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/edgewander/prison-art' },
    ],

    footer: {
      message: '狱望 Prison Art — 探讨人性、救赎与自由',
    },
  },
})
