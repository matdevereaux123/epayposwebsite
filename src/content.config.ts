// Blog posts live in content/blog/*.md — one Markdown file per post.
// Files starting with "_" are ignored (templates, notes).
//
// A post with `draft: true` is never published. It only shows on the local
// drafts page (/blog/drafts) when the preview is built with BLOG_SHOW_DRAFTS=1.
// Publishing a post = setting `draft: false`.

import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const blog = defineCollection({
  loader: glob({ pattern: "**/[^_]*.md", base: "./content/blog" }),
  schema: z.object({
    title: z.string().max(60, "Keep titles under 60 characters for search results"),
    description: z.string().min(70).max(155, "Meta descriptions must be under 155 characters"),
    published: z.coerce.date(),
    updated: z.coerce.date().optional(),
    author: z.string().default("EPAY POS team"),
    /** Main search phrase the post targets. */
    keyword: z.string(),
    tags: z.array(z.string()).default([]),
    /** Slugs of industry / feature pages this post links to (internal linking). */
    related: z.array(z.string()).default([]),
    draft: z.boolean().default(true),
  }),
});

export const collections = { blog };
