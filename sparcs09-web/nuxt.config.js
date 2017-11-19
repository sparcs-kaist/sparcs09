module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'starter',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Nuxt.js project' },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
    ],
  },
  /*
  ** Global CSS
  */
  css: [
    'bulma',
    '~/assets/css/main.css',
  ],
  loading: { color: '#3B8070' },

  // modules
  modules: [
    '@nuxtjs/proxy',
  ],

  plugins: [
    { src: '~/plugins/nuxt-client-init.js', ssr: false },
  ],

  proxy: [
    [
      '/api',
      {
        target: 'http://localhost:8000/api',
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
    ],
  ],

  env: {
    SPARCS_SSO_DOMAIN: process.env.SPARCS_SSO_DOMAIN || 'https://sparcssso.kaist.ac.kr',
    SPARCS_SSO_API_PREFIX: 'api',
    SPARCS_SSO_DOMAIN_VERSION: 'v2',
    SPARCS_SSO_CLIENT_ID: process.env.SPARCS_SSO_CLIENT_ID || '',
    SPARCS09_API_DOMAIN: process.env.SPARCS09_API_DOMAIN || 'http://localhost:3000/api',
  },
  /*
  ** Add axios globally
  */
  build: {
    vendor: ['axios'],
    postcss: {
      plugins: {
        'postcss-custom-properties': false,
      },
    },
    /*
    ** Run ESLINT on save
    */
    extend(config, ctx) {
      if (ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/,
        });
      }
    },
  },
};
