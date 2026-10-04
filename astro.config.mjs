import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import { readdirSync, readFileSync } from "node:fs";

// Pages that must never be in search results. They also carry a noindex tag.
const notInSitemap = ["/thank-you", "/404", "/blog/drafts"];

// A drafts-enabled preview (BLOG_SHOW_DRAFTS=1) also renders the draft posts
// themselves. They are noindex, so listing them in the sitemap is a straight
// contradiction. A production build never sets the flag, so this is a no-op
// there.
//
// This used to drop EVERY /blog/* page whenever the flag was on, not just the
// drafts — so the moment a post went live, every drafts-on preview reported it
// missing from the sitemap. That is a false alarm the audit raised for two
// runs on a post that was correctly listed in production all along. Read the
// frontmatter instead and exclude only the posts actually marked draft.
const showingDrafts = process.env.BLOG_SHOW_DRAFTS === "1";

const draftSlugs = new Set(
  showingDrafts
    ? readdirSync("content/blog")
        .filter((f) => f.endsWith(".md"))
        .filter((f) =>
          /^draft:\s*true\s*$/m.test(
            readFileSync(`content/blog/${f}`, "utf8").split(/^---$/m)[1] ?? ""
          )
        )
        .map((f) => `/blog/${f.replace(/\.md$/, "")}`)
    : []
);

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
        // Only the posts that exist because drafts are switched on.
        if (draftSlugs.has(path)) return false;
        return true;
      },
    }),
  ],
});
