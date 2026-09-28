// Blog helpers. Posts come from content/blog/*.md (see src/content.config.ts).

import { getCollection, type CollectionEntry } from "astro:content";
import { industries, featureCategories } from "./content";
import offersData from "../../content/offers.json";

export type Post = CollectionEntry<"blog">;

/** Drafts are only rendered in the local preview build (BLOG_SHOW_DRAFTS=1). */
export const showDrafts = process.env.BLOG_SHOW_DRAFTS === "1";

const newestFirst = (a: Post, b: Post) => b.data.published.getTime() - a.data.published.getTime();

export async function publishedPosts(): Promise<Post[]> {
  return (await getCollection("blog", (p) => !p.data.draft)).sort(newestFirst);
}

export async function draftPosts(): Promise<Post[]> {
  return (await getCollection("blog", (p) => p.data.draft)).sort(newestFirst);
}

export function readingMinutes(post: Post): number {
  const words = (post.body ?? "").trim().split(/\s+/).length;
  return Math.max(1, Math.round(words / 220));
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });
}

/** Turn a post's `related` slugs into links to real pages on the site. */
export function relatedLinks(slugs: string[]): { name: string; href: string }[] {
  const out: { name: string; href: string }[] = [];
  for (const slug of slugs) {
    const ind = (industries as any[]).find((i) => i.slug === slug);
    if (ind) { out.push({ name: ind.name, href: `/${ind.slug}` }); continue; }
    const feat = (featureCategories as any[]).find((c) => c.page.replace(/^\//, "") === slug);
    if (feat) { out.push({ name: feat.name, href: feat.page }); continue; }
    // "offers-<slug>" points at an offer page; the badge's first part names it.
    if (slug.startsWith("offers-")) {
      const offer = (offersData as any).offers.find((o: any) => `offers-${o.slug}` === slug);
      if (offer) { out.push({ name: offer.badge.split(" · ")[0], href: `/offers/${offer.slug}` }); continue; }
    }
    const fixed: Record<string, string> = {
      pricing: "Pricing", "epay-terminal": "EPAY Terminal", "epay-products-1": "EPAY hardware",
      "epay-software": "EPAY Software", "book-a-demo": "Book a demo", contact: "Contact us",
    };
    if (fixed[slug]) out.push({ name: fixed[slug], href: `/${slug}` });
  }
  return out;
}
