# EPAY POS — SEO report

**Run: 2026-09-30** · 80 indexable pages · build succeeded (84 pages, 1.09s)

---

## 1. Automated audit (tools/seo_audit.py)

**0 to fix, 1 to consider.**

### Consider
- `/blog/flat-rate-vs-cash-discount` is indexable but not in the sitemap.

**This one is a false positive — no action needed.** It only appears because
`tools/preview.sh` sets `BLOG_SHOW_DRAFTS=1`, and the sitemap filter in
`astro.config.mjs` drops every `/blog/*` page when drafts are on. The live
sitemap was checked directly and contains the post (80 URLs, post present).
Production never sets the flag.

### Titles and descriptions
No duplicate titles. No duplicate descriptions. All 80 titles are unique and
under 60 characters; all descriptions are within range. Nothing to fix.

---

## 2. Blog status

| | Count |
|---|---|
| Published posts | **1** (`flat-rate-vs-cash-discount`) |
| Drafts waiting | **1** (`cash-discount-program-explained`, `draft: true`) |
| Topics still open in `content/blog-topics.json` | **29** of 30 |

Open topics are well above the 7 floor — the backlog is healthy. The problem is
throughput, not ideas: 29 researched topics are queued and one post is live.

---

## 3. Findings the automated audit does not cover

These came from checking the live site, not just the build. Ordered by impact.

### A. Canonical and sitemap point at a host that redirects — FIX FIRST

`astro.config.mjs` sets `site: "https://www.epaypos.net"`, so every canonical
tag and all 80 sitemap URLs use the `www` host. But Netlify serves the apex:

- `https://www.epaypos.net/` → **301** → `https://epaypos.net/`
- `https://epaypos.net/` → **200**

So the page served at `epaypos.net/` declares its canonical to be
`www.epaypos.net/`, which redirects straight back to it. Every URL in the
sitemap and the `Sitemap:` line in `robots.txt` is a redirect rather than a
final URL.

Google usually resolves this, but it is a self-contradicting signal on all 80
pages and it wastes crawl budget. Pick one host and make config, canonicals,
sitemap and the Netlify redirect all agree. The apex is what currently serves,
so the low-risk direction is to set `site: "https://epaypos.net"`. No URL
slugs change — only the host.

### B. No `llms.txt` (404 on the live site)

AI crawlers reach the site fine — `GPTBot` and `PerplexityBot` both get 200,
and `robots.txt` allows all agents with no `Google-Extended` block. That part
is right. What is missing is a plain-text summary at `/llms.txt` telling an
assistant what EPAY POS is, what it costs, and which pages answer what.

### C. Almost no question-shaped content

Only **8 question headings across 2,028 H2/H3 tags**, on 4 pages. AI answer
engines preferentially quote passages that state a question and answer it
directly underneath.

### D. FAQ is 8 entries on one page

`content/faq.json` holds 8 entries and `FAQPage` schema appears on `/pricing`
only. Nothing on any industry page, product page or `/contact`. Industry pages
average ~1,450 words of real content, so they are strong enough to carry their
own FAQ block — the schema is simply not there.

### E. Six pages are titled with internal nav labels, not search terms

These titles use in-house section names nobody types into a search box:

| Page | Current title |
|---|---|
| `/epay-base-features` | Front of House \| EPAY POS |
| `/customer-kitchen-display` | Kitchen & Display \| EPAY POS |
| `/e-commerce-websites` | Online & Delivery \| EPAY POS |
| `/employee-time-management` | Employee & Time \| EPAY POS |
| `/integrations` | Integrations \| EPAY POS |
| `/grub-hub-doordash-uber-eats` | Delivery Apps \| EPAY POS |

The matching topics in `blog-topics.json` already name the real keywords
(`kitchen display system`, `restaurant online ordering system`,
`employee time clock pos`, `delivery app integration pos`). Titles can be
rewritten freely — this changes no slug.

### F. No `Review` or `aggregateRating` schema, because there are no reviews

`content/testimonials.json` has **0 entries** and is explicitly marked
PLACEHOLDER. The file is correct to stay empty rather than carry invented
quotes, and the site correctly omits the social proof section. But this is the
single biggest missing trust signal, for buyers and for AI engines alike.
**This one needs Matt, not code:** real merchant quotes, with permission.

### G. Merchant count conflicts between two sources

`CLAUDE.md` says the line worth keeping is "20,000+ merchant count".
`content/testimonials.json` has `"merchants": 10000` / `"10,000+"`, which is
what renders. One of the two is out of date. Flagging rather than guessing —
per project rules, a number that isn't verified doesn't get written.

### H. Thin pages: `/contact` and `/about`

Unique content, excluding nav and footer chrome:

| Page | Unique words |
|---|---|
| `/contact` | ~337 |
| `/about` | ~451 |
| industry pages (typical) | ~1,450 |

`/contact` is a local-intent landing page and currently the thinnest indexable
page on the site.

### I. No local landing pages, and `LocalBusiness` is missing local fields

There are no city or region pages. The `LocalBusiness` node is on all 84 pages
with a correct NAP (185 E Big Beaver Rd, Troy, MI 48083) and five `sameAs`
profiles, but it omits `geo`, `openingHoursSpecification`, `areaServed`,
`priceRange` and `description` — the fields that drive local pack and
"near me" results.

### Schema inventory (built site)

`LocalBusiness` 84 · `BreadcrumbList` 79 · `Product` 28 · `Brand` 23 ·
`Offer` 11 · `Question`/`Answer` 8 each · `Organization` 5 · `BlogPosting` 3 ·
`FAQPage` 1 · `WebSite` 1. No `Service`, no `Review`, no `aggregateRating`.

Lead capture is in good shape: a Netlify form is present on 84 of 85 pages.

---

## 4. Changes made (2026-09-30)

Report run first, then these fixes applied and verified against a rebuild.
No URL slug was changed. No content was invented — every number below is read
from `/content`, and the FAQ answers restate facts already on their own page.

| # | Change | Files |
|---|---|---|
| A | `site` now points at the apex. All 84 canonicals and all sitemap URLs are `https://epaypos.net/...` instead of a host that 301s. | `astro.config.mjs`, `content/site.json` (`brand.domain`), `public/robots.txt` |
| — | GA host check widened, since `brand.domain` is no longer the www form and stripping `www.` from the apex yielded one host twice. | `src/layouts/Base.astro` |
| B | `/llms.txt` added — generated from `/content` on every build, so it cannot go stale. 1,507 words: pricing, hardware, features, verticals, all 8 FAQs verbatim, key links. | `src/pages/llms.txt.ts` |
| C | 81 unique question-and-answer pairs added across 22 industry pages and 5 product pages, each with `FAQPage` schema. Question headings went 8 → 125. | `content/industries.json`, `content/products.json`, `src/pages/[slug].astro`, `src/pages/product/[id].astro` |
| D | `FAQPage` schema coverage: 1 page → 28 pages. Product pages now emit `Product` **and** `FAQPage`. | as above |
| E | Six nav-label titles replaced with search-led ones, plus matching descriptions. | `content/features.json`, `src/pages/[slug].astro` |
| I | `LocalBusiness` gained `description`, `priceRange` ($17.99–$74.99/mo, derived from `pricing.json`) and `areaServed`. | `content/site.json` (`local_business`), `src/layouts/Base.astro` |

New feature-page titles:

| Page | Was | Now |
|---|---|---|
| `/epay-base-features` | Front of House | Restaurant POS Software Features |
| `/customer-kitchen-display` | Kitchen & Display | Kitchen Display System for Restaurants |
| `/employee-time-management` | Employee & Time | POS Employee Time Clock & Scheduling |
| `/e-commerce-websites` | Online & Delivery | Restaurant Online Ordering System |
| `/integrations` | Integrations | POS Integrations & Accounting Sync |
| `/grub-hub-doordash-uber-eats` | Delivery Apps | DoorDash, Uber Eats & Grubhub POS Integration |
| `/analytics-app` | Reporting & Analytics | POS Reporting & Sales Analytics |

### Verified after the change

- Build clean, 84 pages. `seo_audit.py`: **0 to fix**, same single preview-only flag.
- 84/84 canonicals on the apex; 79 sitemap URLs on the apex; robots.txt sitemap on the apex.
- 81 FAQ pairs, **no duplicate question or answer anywhere on the site**.
- Every price quoted in an FAQ checked against `pricing.json`: all 27 plan, purchase
  and lease figures match. No stray processing rate other than `2.3% + 5¢`.
- Forms still on 84 of 85 pages; `LocalBusiness` still on all 84. No console errors.
- FAQ blocks render and expand correctly on industry and product pages (checked in
  the browser), reusing the existing `.faqs` component — no new CSS, no layout change.

### Follow-up round (same day)

| Ask | Status |
|---|---|
| Merchant count is 10,000+ | Done. `CLAUDE.md` said 20,000+ and disagreed with `testimonials.json`, which is what renders. Corrected to 10,000+ with a note to keep both in step. |
| Hours 9–9 every day | Done. `site.json > local_business.hours` set to 09:00–21:00, all seven days; `openingHoursSpecification` now emits on all 84 pages. |
| Netlify | Nothing to change. Checked via the Netlify CLI: the `epayposwebsite` project already has `custom_domain: epaypos.net` with `www.epaypos.net` as an alias and `force_ssl: true`. The apex was always primary — the code was the side that disagreed, and that is now fixed. |
| Testimonials | Not written. See below. |

**Testimonials — not invented.** Fabricated endorsements are an FTC matter in
the US and invented review markup is a Google spam signal, so writing them
would put the rankings this report exists to protect at risk. What was built
instead: the whole pipeline, dormant until real quotes arrive.

- `src/components/Testimonials.astro` — homepage band, renders nothing until
  `testimonials.json` has 3+ entries, then appears with no code change.
- `reviewSchema()` in `src/lib/content.ts`, merged into `LocalBusiness` —
  emits `Review` nodes from the first entry. `aggregateRating` is computed
  **only** from entries that carry a real `rating`; an unrated quote still gets
  a Review node and simply shows no stars.
- `testimonials.json` shape gained optional `rating` and `date`, and a required
  `permission` field for recording written consent.
- `prompts/testimonial-request.md` — who to ask first (Pho Street already
  approved their video), the email to send, and the checks before publishing.

Verified by loading three throwaway entries into the preview copy only: band
rendered, 3 Review nodes, aggregateRating 4.5 from the 2 rated entries, the
unrated one correctly starless. Test data never touched the repo and the build
is dormant again.

Worth knowing: Google does not show rich-result stars for self-serving reviews.
The gain here is on-page conversion and AI engines having something concrete to
quote. Stars in search come from Google Business Profile, a separate job.

### Still open — these need Matt, not code

1. **Testimonials.** `content/testimonials.json` is still an empty placeholder, so
   there is still no `Review` or `aggregateRating` schema. Real merchant quotes with
   permission are the biggest remaining trust signal. Nothing was invented here.
2. **Merchant count.** `CLAUDE.md` says "20,000+"; `testimonials.json` says `10,000+`,
   and 10,000 is what renders and what `/llms.txt` implies. Which is current?
3. **`geo` and opening hours.** Both added to `content/site.json > local_business` as
   blank fields with notes, and both are omitted from the schema while empty. Real
   coordinates and real hours would strengthen local pack and "near me" results.
   Neither may be guessed.
4. **Netlify host.** The code now says the apex is canonical. Confirm the apex stays
   the primary domain in Netlify so the two do not disagree again.
5. **Blog throughput.** 29 researched topics still open, 1 post live.
6. **Thin pages.** `/contact` (~337 words) and `/about` (~451) are untouched —
   `/about` is thin because `founded`, `team_size` and `story` are deliberately blank
   pending real facts.

---

## 5. AI visibility round (2026-09-30)

Goal: be the thing an assistant quotes when someone asks about statement
analysis, processing rates, or restaurant and retail POS.

| Change | Detail |
|---|---|
| FAQ coverage | **1 page → 46.** 150 unique Q&A pairs, every one checked against the facts already on its page. |
| Question headings | **8 → 154.** |
| `Service` schema | Added to all 6 offer pages via `serviceSchema()`. "Who will read my processing statement" matches a *service*, not a product — the site previously offered no such node. |
| Offer-page FAQs | 6 pages: statement review, Consumer Choice, flat rate, free placement, switch bonus, menu buildout. These carry the highest-intent questions on the site. |
| Feature-page FAQs | All 7, each now with schema (they previously showed the shared subset and emitted nothing). |
| Standalone pages | `/epay-terminal`, `/epay-software`, `/epay-payment-portal`, `/capital-loans`, `/contact`. |
| Global FAQ | `faq.json` 8 → 15. Added effective rate, flat vs interchange-plus, switching time, which systems EPAY replaces, retail coverage, contract terms. |
| `/llms.txt` | **1,507 → 6,885 words, 143 Q&As.** Now carries the programs section and every FAQ on the site, each with its source URL so an assistant can cite the page. |
| `/contact` | Was the thinnest indexable page (~337 words). Now carries hours, address, both extensions and 4 FAQs. |
| Refactor | `FaqBlock.astro` replaces the FAQ markup that had been copy-pasted into five pages; `faqSchema()` and `serviceSchema()` live in `content.ts`. |
| robots.txt | Points AI crawlers at `/llms.txt`. |

### The statement-analysis path specifically

An assistant asked "who will analyse my merchant statement" now finds, on
`/offers/statement-review`: a `Service` node naming the provider, address and
phone; four FAQs in the exact words someone would ask ("Will you analyze my
credit card processing statement for free?"); and the same answers again in
`/llms.txt` with the URL attached. The global FAQ adds the effective-rate
explanation, which is the question underneath the question.

### Verified

- Clean rebuild, 84 pages. `seo_audit.py`: **0 to fix**.
- **150 Q&A pairs, zero duplicate questions and zero duplicate answers.** One
  collision was caught during the pass (`"When do I get my money?"` existed in
  both `faq.json` and the flat-rate offer) and reworded.
- Every price quoted in an FAQ matches `pricing.json`.
- 84/84 apex canonicals, 84 LocalBusiness, 46 FAQPage, 6 Service, forms still on 84.
- Rendered and expanded correctly on desktop and at 375px; no horizontal
  scroll, no console errors.

---

## For Matt

**Everything on the code side is done. Three things still need you.**

The site is now built to be quoted. Where it stood this morning and where it
stands now:

| | Before | Now |
|---|---|---|
| Pages with FAQ schema | 1 | 46 |
| Question-shaped headings | 8 | 154 |
| `/llms.txt` | none | 6,885 words, 143 Q&As |
| `Service` schema | none | 6 offer pages |
| Canonical tags pointing at a redirect | all 80 | none |

**On the queries you named.** Someone asking an assistant to analyse their
processing statement now hits a page that says so in their words, backed by a
Service node with your address and phone in it, and the same answers sit in
`/llms.txt` with the link attached so the assistant can cite you. Same for
processing rates (flat vs interchange-plus, effective rate, 0% Consumer
Choice), restaurant POS (22 verticals, each with its own three questions) and
retail POS (convenience, liquor, smoke shop, grocery, pharmacy, boutique, pet).

**What that buys you, honestly:** this is the groundwork that makes you
quotable. AI engines still need to re-crawl, and they weight brand mentions off
your own site too — directories, your Google Business Profile, press. The site
side is no longer the bottleneck.

Still yours:

1. **Real testimonials.** Pipeline is built and dormant; `prompts/testimonial-request.md`
   has the email. Start with Pho Street.
2. **Map coordinates** for 185 E Big Beaver Rd — the last local field missing.
3. **The blog.** 29 researched topics, 1 post live. Your 29 topics map almost
   one-to-one onto the questions assistants get asked, so this is now the
   highest-leverage content work left.

Nothing is deployed. Review and push when you're happy.
