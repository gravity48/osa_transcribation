const {defineConfig} = require('@vue/cli-service')


module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        proxy: `http://${process.env.PROXY_HOST}:${process.env.PROXY_PORT}`,
        port: 5173
    },
})
