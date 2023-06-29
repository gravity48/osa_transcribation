export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'OSA transcription',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
    bodyAttrs:{
      class: 'p-0 m-0'
    }
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
      'primeflex/primeflex.css'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // Doc: https://www.primefaces.org/primevue/showcase-v2/#/setup
    'primevue/nuxt',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],

  //Auth settings module
  auth: {
    strategies: {
      local: {
        scheme: 'refresh',
        localStorage: {
          prefix: 'auth.'
        },
        token: {
          prefix: 'access.',
          property: 'access',
          maxAge: 86400,
          type: 'Bearer'
        },
        refreshToken: {
          prefix: 'refresh.',
          property: 'refresh',
          data: 'refresh',
          maxAge: 60 * 60 * 24 * 15
        },
        endpoints: {
          login: { url: 'api/v1/token/', method: 'post'},
          refresh: { url: 'api/v1/token/refresh/', method: 'post' },
          user: false,
          logout: false
        }
      }
    }

  },
  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    proxy: true // Can be also an object with default options
  },

  proxy: {
    '/api/': 'http://127.0.0.1:8000/'
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    // https://github.com/primefaces/primevue/issues/844
    transpile: ['primevue']
  }
}