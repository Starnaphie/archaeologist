import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const awsApiUrl = env.VITE_AWS_API_URL || ''

  return {
    plugins: [react()],
    server: {
      proxy: awsApiUrl ? {
        '/api-gateway': {
          target: awsApiUrl,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api-gateway/, ''),
        },
      } : {},
    },
  }
})
