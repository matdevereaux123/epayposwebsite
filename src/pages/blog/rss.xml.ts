// RSS feed of published posts, for readers and search engines.
// Hand-written so the site needs no extra package.

import type { APIRoute } from "astro";
import { site } from "../../lib/content";
import { publishedPosts } from "../../lib/blog";

const esc = (s: string) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export const GET: APIRoute = async () => {
  const posts = await publishedPosts();
  const home = site.brand.domain;
  const items = posts
    .map((p) => {
      const link = new URL(`/blog/${p.id}`, home).href;
      return `    <item>
      <title>${esc(p.data.title)}</title>
      <link>${link}</link>
      <guid isPermaLink="true">${link}</guid>
      <description>${esc(p.data.description)}</description>
      <pubDate>${p.data.published.toUTCString()}</pubDate>
    </item>`;
    })
    .join("\n");
  const blog = (site as any).blog;
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>${esc(site.brand.name)} blog</title>
    <link>${new URL("/blog", home).href}</link>
    <description>${esc(blog.meta_description)}</description>
    <language>en-us</language>
${items}
  </channel>
</rss>
`;
  return new Response(xml, { headers: { "Content-Type": "application/rss+xml; charset=utf-8" } });
};
