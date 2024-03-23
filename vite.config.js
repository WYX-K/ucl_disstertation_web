import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import Components from 'unplugin-vue-components/vite'
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [
        AntDesignVueResolver({
          importStyle: false, // css in js
        }),
      ],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    // 反向代理
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/', // 代理的地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/'),
      },
    },
    host: '0.0.0.0',
  },
})
