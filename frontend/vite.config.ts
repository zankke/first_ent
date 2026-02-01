import { defineConfig } from 'vite' // Removed loadEnv
import react from '@vitejs/plugin-react'
import path from 'path'; // Import path module

export default defineConfig(({ mode }) => {
  // Directly access process.env, assuming start_firstent.sh exports these
  const VITE_SUPABASE_URL = process.env.VITE_SUPABASE_URL;
  const VITE_SUPABASE_ANON_KEY = process.env.VITE_SUPABASE_ANON_KEY;

  console.log('--- Vite Config Debug ---');
  console.log('Mode:', mode);
  console.log('VITE_SUPABASE_URL from process.env:', VITE_SUPABASE_URL);
  console.log('VITE_SUPABASE_ANON_KEY from process.env:', VITE_SUPABASE_ANON_KEY);
  console.log('--- End Vite Config Debug ---');

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": "/src",
      },
    },
    server: {
      host: '0.0.0.0',
      port: 3002, // Hardcoded to 3002 for consistency with start_firstent.sh
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
          logLevel: 'debug', // Add debug logging for proxy
        },
      },
    },
    define: {
      'import.meta.env.VITE_SUPABASE_URL': JSON.stringify(VITE_SUPABASE_URL),
      'import.meta.env.VITE_SUPABASE_ANON_KEY': JSON.stringify(VITE_SUPABASE_ANON_KEY),
      // Add other VITE_ variables if necessary
    },
    // Removed envDir as we are now directly accessing process.env
  };
});