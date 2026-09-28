# Daily blog draft — instructions for Claude

You are drafting one blog post for epaypos.net (EPAY POS, Troy MI). Matt reviews
every draft before it goes live. Your job is a post he can approve without edits.

## Where things are

- Project: `~/Desktop/EPAY website /epaypos-site/` (note the space after "website").
- Rules for the whole site: `CLAUDE.md`. The voice rules there apply to every post.
- Facts you may use: ONLY what is in `content/*.json` (pricing, products, programs,
  industries, features, FAQ, offers, terminal). Read the files you need.
- Topic backlog: `content/blog-topics.json`.
- Posts: `content/blog/<id>.md`.

## Steps

1. Open `content/blog-topics.json`. Take the first topic with `"status": "open"`.
   If none are open, write no post. Add 10 new topics built from pages on the
   site, set them to open, and stop.
2. Read the pages its `related` slugs point to (in `content/industries.json`,
   `features.json`, `offers.json`, `pricing.json`, `terminal.json`, `faq.json`).
3. Write `content/blog/<id>.md` using the template below.
4. In `content/blog-topics.json`, set that topic's status to `"drafted"`.
5. Build the preview: `bash tools/preview.sh`. The build must pass. If it fails
   because of the post (title/description length, missing field), fix the post
   and build again.
6. Tell Matt: the title, one sentence on the angle, and the review link
   http://localhost:4321/blog/drafts

## Hard rules

- `draft: true`, always. Never publish. Publishing happens only when Matt says
  "approve".
- Never invent a number, statistic, customer, quote, review, case study or
  result. If a point needs a number the content files don't have, write the
  point without a number.
- Prices, rates, fees and program terms must match `content/*.json` exactly.
  Don't round them, and don't promise anything the site doesn't promise.
- Don't state competitors' prices or fees, and make no claims about specific
  competitors. General comparisons are fine.
- No legal, tax or compliance advice. On cash discount and dual pricing,
  describe how EPAY's program works as the site does. Say rules vary and
  owners should confirm what applies to them.
- Voice: direct, plain, owner to owner. None of "revolutionary", "seamless",
  "cutting-edge", "empower" or "unlock". Sentence case for headings. Active voice.

## SEO rules

- `title`: 60 characters max, contains the keyword or a close variant, reads
  naturally.
- `description`: 70 to 155 characters, a real summary with the keyword.
- Filename / id is the URL (`/blog/<id>`). Keep the one from the backlog, and
  never change it after publishing.
- 900 to 1,400 words. The keyword goes in the first 100 words and in one H2.
  No stuffing.
- The body starts with a short intro paragraph. The page supplies the title as
  the H1, so never write an H1 (`#`) in the body. Use `##` and `###` only.
- Link to at least 3 related pages on the site with normal Markdown links, e.g.
  `[Bar & Lounge POS](/bar-lounge)`. Use real paths from `content/site.json` >
  `url_map_do_not_change` or the industry and feature slugs.
- End with a `## Common questions` section of 2 to 4 short Q&As, answered only
  from the content files.
- Final line: one sentence inviting the reader to book a demo or ask for a
  statement review, linking `/book-a-demo` or `/contact`.

## Template

```markdown
---
title: "..."
description: "..."
published: YYYY-MM-DD
keyword: "..."
tags: ["...", "..."]
related: ["slug-one", "slug-two", "slug-three"]
draft: true
---

Intro paragraph...

## ...
```
