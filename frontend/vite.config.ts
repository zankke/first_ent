import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": "/src",
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    hmr: {
      // host: 'localhost',
    },
    allowedHosts: [
      // '.ngrok-free.app',
      'localhost',
      '127.0.0.1',
      '0.0.0.0',
      'konikt-ai.kr',
    ],
    proxy: {
      '/api': {
        target: 'http://localhost:5002', // Flask backend server
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
    },
  },
});