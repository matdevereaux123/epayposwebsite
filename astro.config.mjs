import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Pages that must never be in search results. They also carry a noindex tag.
const notInSitemap = ["/thank-you", "/404", "/blog/drafts"];

export default defineConfig({
  site: "https://www.epaypos.net",

  // Astro's default asset folder is "_astro". The leading underscore is a
  // reserved prefix when the built site is published as a Claude Artifact for
  // preview, so it ships as "astro" instead. Netlify does not care either way.
  build: { assets: "astro" },

  integrations: [
    sitemap({
      filter: (page) => !notInSitemap.some((p) => new URL(page).pathname.replace(/\/$/, "") === p),
    }),
  ],
});
