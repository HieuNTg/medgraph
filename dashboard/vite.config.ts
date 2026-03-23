/// <reference types="vitest/config" />
import path from "path"
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"
import type { Plugin } from "vite"

// Inline plugin: injects SW registration script into the HTML entry point.
// vite-plugin-pwa is not installed; this is the manual approach.
function swRegisterPlugin(): Plugin {
  return {
    name: "sw-register",
    transformIndexHtml(html) {
      const script = `
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/sw.js').catch(function (err) {
        console.warn('SW registration failed:', err);
      });
    });
  }
</script>`;
      return html.replace("</body>", `${script}\n</body>`);
    },
  };
}

export default defineConfig({
  plugins: [react(), tailwindcss(), swRegisterPlugin()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setup.ts"],
    css: false,
  },
})
