import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'

const root = fileURLToPath(new URL('.', import.meta.url))

// base 與站台網址由環境變數決定，預設值在 website/.env（GitHub Pages）。
// 鏡像站在 CI 以 VITE_BASE=/ VITE_SITE_URL=https://… 覆寫，見 docs/deployment.md。
// index.html 與 404.html 內以 %BASE_URL%、%VITE_SITE_URL% 取得同一組值。
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, root, 'VITE_')
  return {
    plugins: [react()],
    base: env.VITE_BASE,
    build: {
      rollupOptions: {
        input: {
          main: fileURLToPath(new URL('./index.html', import.meta.url)),
          viewer: fileURLToPath(new URL('./viewer.html', import.meta.url)),
          // 404.html 列為入口，Vite 才會替它套 base 與替換 %BASE_URL%
          notFound: fileURLToPath(new URL('./404.html', import.meta.url)),
        },
      },
    },
  }
})
