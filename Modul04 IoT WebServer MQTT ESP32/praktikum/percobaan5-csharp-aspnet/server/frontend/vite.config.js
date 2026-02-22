import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Teruskan semua request /api ke ASP.NET Core backend
      '/api': {
        target:    'http://localhost:5000',
        changeOrigin: true,
        secure:    false,
      },
    },
  },
});
