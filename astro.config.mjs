import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Pages that must never be in search results. They also carry a noindex tag.
const notInSitemap = ["/thank-you", "/404", "/blog/drafts"];

// A drafts-enabled preview (BLOG_SHOW_DRAFTS=1) also renders the draft posts
// themselves. They are noindex, so listing them in the sitemap is a straight
// contradiction — and it made seo_audit.py report a fault on every build with
// a draft in it. A production build never sets the flag, so this is a no-op
// there.
const showingDrafts = process.env.BLOG_SHOW_DRAFTS === "1";

export default defineConfig({
  // The apex is what Netlify serves: www.epaypos.net 301s to epaypos.net.
  // This value drives every canonical tag and every sitemap URL, so pointing
  // it at the www host made all 80 URLs redirect to themselves — each page
  // declaring its real address to be one that bounces back. Keep this and the
  // Netlify host in agreement; changing it changes no page slug.
  site: "https://epaypos.net",

  // Astro's default asset folder is "_astro". The leading underscore is a
  // reserved prefix when the built site is published as a Claude Artifact for
  // preview, so it ships as "astro" instead. Netlify does not care either way.
  build: { assets: "astro" },

  integrations: [
    sitemap({
      filter: (page) => {
        const path = new URL(page).pathname.replace(/\/$/, "");
        if (notInSitemap.includes(path)) return false;
        // Every /blog/* page that exists only because drafts are switched on.
        if (showingDrafts && path.startsWith("/blog/") && path !== "/blog") return false;
        return true;
      },
    }),
  ],
});
