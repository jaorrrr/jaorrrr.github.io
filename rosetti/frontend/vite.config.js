import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  // Build estático (GitHub Pages) é servido em um subcaminho do domínio,
  // então os assets precisam de um base relativo em vez da raiz "/".
  base: mode === 'static' ? './' : '/',
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:4000',
        changeOrigin: true,
      },
    },
  },
}));
