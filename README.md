# EPAY POS website

A working Astro site for epaypos.net. 24 pages, all generated from JSON content
files. Deploys to Netlify as static HTML.

**This is not a scaffold to build — it's a working site to pick up.** It builds
cleanly today. Your job is to finish it and ship it.

---

## Run it first

```bash
npm install
npm run dev
```

Open `http://localhost:4321`.

Then, to see the point of the whole setup: open `content/pricing.json`, change
the Table plan from `69.99` to `79.99`, and save. The homepage, the pricing page,
and every restaurant industry page update at once.

---

## First message to Claude Code

Open a terminal in this folder, run `claude`, and paste:

```
Read CLAUDE.md, then design/design-system.md, then skim /content and /src.

This is a working Astro site — 24 pages already generate from the JSON in
/content, and it builds cleanly. Don't rebuild it.

Run `npm run build` to confirm it works, then tell me:
1. What's built and working
2. What's still missing before this could replace my live Wix site
3. Anything in /src that breaks the "no content in page code" rule in CLAUDE.md

Don't write any code yet. Just report back.
```

Read first, build second. This one habit prevents most wasted work.

---

## What's built

Astro + Netlify config, sitemap, robots. Design tokens and global styles. Header
with mega-menu, keyboard and mobile nav. Footer. The batch line (signature
element). Homepage. 11 industry pages and 7 feature pages, all from one template.
Pricing page with FAQ and schema. Hardware page. Contact and demo forms wired to
Netlify Forms. Thank-you page and 404. LocalBusiness schema, per-page meta tags,
scroll reveal, reduced-motion handling.

## What's missing

**You need to supply:**

| Thing | Where it goes |
|---|---|
| Logo file | `public/img/epay-logo.png` — resize to ~400px wide first, or use SVG and update `logo` in `content/site.json` |
| Product photography | `public/img/products/`, then swap the placeholder blocks in `epay-products-1.astro` |
| Font names from Wix | `src/lib/fonts.ts` — Editor → Site Design → Text Themes |
| Terms of service and privacy text | Paste the existing copy. Don't let Claude Code write legal text |
| Real testimonials | `content/testimonials.json` is empty on purpose |
| GA4 + Search Console IDs | Hand them to Claude Code |
| URLs for your existing tools | Statement analyzer, savings calculator, floor plan generator |

**Claude Code can do:**

- The remaining pages: `/about`, `/sign-up`, `/copy-of-free-processing`, and the two legal page layouts
- Self-hosting the fonts (currently loading from Google, costs ~200ms)
- Embedding your existing tools in the marked slots
- Deployment to Netlify with a preview URL

---

## The four prompts, in order

**1. Finish the missing pages**
```
Build the remaining pages: /about, /sign-up, /copy-of-free-processing,
/terms-of-service-agreement, /privacy-policy. Follow the existing page
patterns exactly and pull all copy from /content. For the two legal pages,
build the layout but leave the body as a clearly marked placeholder —
I'll paste the real text.
```

**2. Self-host the fonts**
```
Move the fonts in src/lib/fonts.ts off Google Fonts and self-host them in
/public/fonts, subset to latin. Preload the display face. Show me the
Lighthouse performance score before and after.
```

**3. Wire in my existing tools**
```
The statement analyzer is at <URL> and the savings calculator is at <URL>.
Embed them in the marked slot on the homepage and on /pricing, styled to
match the design system so the seams don't show. The floor plan generator
calls my Render server at <URL> — keep those fetch calls as they are and
tell me what to add to the server's CORS allowlist.
```

**4. Deploy to a preview URL**
```
Push this to a new private GitHub repo and connect it to Netlify. I want a
preview URL to share with my team. Do NOT configure the custom domain —
epaypos.net stays on Wix until I say otherwise. After deploying, submit the
contact form on the live preview and confirm it reaches the Netlify dashboard.
```

Then see `prompts/` for SEO/launch prep and the everyday update prompts.

---

## Where things live

```
content/            everything you'll ever want to change
  site.json           brand, contact, nav, logo path, URL map
  pricing.json        plans, rates, programs
  products.json       hardware
  features.json       feature categories → generate 7 feature pages
  industries.json     11 verticals → generate 11 pages
  faq.json            FAQ + schema
  testimonials.json   empty on purpose

src/
  pages/
    index.astro             homepage
    [slug].astro            generates industry AND feature pages
    pricing.astro, epay-products-1.astro
    contact.astro, book-a-demo.astro, thank-you.astro, 404.astro
  components/
    Header.astro            nav generated from site.json
    Footer.astro
    BatchLine.astro         the signature element
    LeadForm.astro          Netlify Forms
  layouts/Base.astro        SEO meta, schema, font loading
  lib/content.ts            typed access to all JSON
  lib/fonts.ts              THE only place fonts are set
  styles/global.css         design tokens — colors, type scale, spacing

CLAUDE.md           rules Claude Code reads every session
design/             the visual spec and the reasoning behind it
prompts/            SEO/launch prep and everyday update prompts
netlify.toml        build config and headers
```

---

## Three rules that keep this fast

**1. No content in page code.** Prices, features, and copy go in `/content`. If
Claude Code hardcodes something, say: *"That belongs in /content. Move it and
pull it through content.ts."*

**2. Never change an existing URL.** The map is in `content/site.json`. Those
pages have ranking history, including two misspelled slugs (`/liqour-stores`,
`/pizzeria-s`) that stay misspelled on purpose.

**3. Run this monthly:**
```
Audit for hardcoded prices, feature lists, or copy living outside /content.
Also check for broken internal links, missing meta descriptions, and images
without alt text. Give me the list before fixing anything.
```

---

## Launch sequence

1. Build the missing pages and drop in the logo and photos
2. Deploy to a Netlify preview URL — your Wix site stays live the whole time
3. Test every form and confirm submissions arrive
4. Sit with the preview for a few days; check it on your phone
5. Point the `epaypos.net` A record and `www` CNAME at Netlify — **leave `portal.epaypos.net` alone**
6. Keep the Wix plan active ~30 days as a rollback path
