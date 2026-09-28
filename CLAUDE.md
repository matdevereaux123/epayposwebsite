# EPAY POS — Website Project Instructions

You are building and maintaining the marketing site for EPAY POS (epaypos.net), a point-of-sale and payment processing company based in Troy, MI.

**Brand: EPAY POS only.** The site carries no parent-company branding. Do not add "a division of", a parent name in the footer, a `parentOrganization` node in the schema, or a parent brand anywhere else. This is deliberate and temporary — it changes when the external-businesses dropdown is built. See `_note_on_parent` in `content/site.json`. Customers are independent restaurant and retail owners — full service restaurants, bars, pizzerias, cafes, hotel dining, convenience/gas, liquor stores, smoke shops, and grocery.

## The one rule that matters most

**No content lives in page code.** Prices, plan names, feature lists, product specs, industry copy, nav items, phone numbers, testimonials, FAQs — all of it lives in `/content/*.json`. Pages read from those files.

If you are about to type a dollar amount, a plan name, or a feature bullet directly into an `.astro` file, stop and put it in the right JSON file instead. The entire point of this project is that the owner can update the site by asking for a one-line content change.

Before finishing any task, check: did I hardcode anything that belongs in `/content`?

## Stack

- **Astro 7** — static output. No SSR unless there's a real reason.
- **Scoped component CSS** driven by design tokens in `src/styles/global.css`. No Tailwind, no CSS framework. Every color and size references a `var()` — never write a raw hex value in a component.
- **TypeScript** for component logic.
- **No React/Vue/Svelte** unless a specific piece of interactivity genuinely requires it. Islands only, never a full framework page.
- Deploy: **Netlify** (static build, `netlify.toml` is committed).
- Forms: **Netlify Forms**. Each form needs `data-netlify="true"`, a hidden `form-name` field, and the honeypot. See `src/components/LeadForm.astro`.

Keep dependencies minimal. Every package added is a thing that breaks later.

## Routing

`src/pages/[slug].astro` generates **all industry pages and all feature pages** from JSON. Do not create a new page file for a new industry or feature category — add the entry to the JSON and the route generates itself.

Static page files (`pricing.astro`, `contact.astro`, etc.) take precedence over the dynamic route, which is intentional.

## Content files

| File | Holds |
|---|---|
| `content/site.json` | brand, contact info, nav structure, socials, global CTAs, URL map |
| `content/pricing.json` | subscription plans, processing rates, program options |
| `content/products.json` | hardware (EPAY Mini, Table, Retail, Stations, KDS, handheld) |
| `content/features.json` | base features grouped by category |
| `content/industries.json` | one entry per industry page, with hero copy, pain points, features |
| `content/testimonials.json` | social proof |
| `content/faq.json` | FAQ entries, also used for FAQPage schema |

When adding a new item, follow the shape of the existing entries exactly. Don't invent new field names for the same concept.

## Design

`design/design-system.md` is binding. Read it before writing any UI. Colors and type come from `design/tokens.css`.

Do not drift toward generic SaaS defaults: gradient-blob hero, three icon cards, logo bar, testimonial carousel, pricing table, footer. That's the shape everyone else has. The design system defines a specific alternative — follow it.

## Voice

Direct, plain, owner-to-owner. These are people running a restaurant at 11pm, not enterprise buyers.

- Write "you keep more of each sale," not "optimize your revenue capture."
- Specifics beat adjectives: "2.3% + 5¢, flat" beats "competitive rates."
- No "revolutionary," "seamless," "cutting-edge," "empower," "unlock."
- Sentence case for headings. Active voice.
- Never invent a statistic, a customer name, or a case study. If a number is needed and you don't have it, ask.

Existing brand lines worth keeping: "Built for Speed. Designed for Growth." and the 20,000+ merchant count.

## SEO — non-negotiable

- **Never change an existing URL slug.** The map is in `content/site.json`. These pages have ranking history.
- Every page needs a unique `<title>` under 60 characters and a meta description under 155.
- Semantic HTML. One `<h1>` per page. Real heading hierarchy.
- All images need alt text describing the image, not keyword stuffing.
- Maintain `sitemap.xml` and `robots.txt` on every structural change.
- Schema markup: LocalBusiness sitewide, Product on product pages, FAQPage on FAQ.
- Target Lighthouse 95+ on performance and accessibility. Check it before saying a page is done.

## Quality floor

Every page, no exceptions:

- Responsive from 320px up. Test at 390px and 1440px.
- Visible keyboard focus states.
- `prefers-reduced-motion` respected on every animation.
- Real contrast ratios (4.5:1 body text minimum).
- Images in WebP with explicit width/height to prevent layout shift.
- No layout shift on load.

## External pieces — don't rebuild these

- Customer portal: `portal.epaypos.net` (separate, linked from header "Login")
- Floor plan generator: calls a Node/Express server on Render (`epay-pos-server`)
- Savings calculator, statement analyzer, Maverick payment widget: existing embeds
- iOS app: App Store link in footer

Style the containers around these to match. Don't touch their internals without being asked.

## Working style

- Read the relevant content and design files before building.
- For any page, propose the section structure before writing the code.
- Small commits with clear messages.
- After a visual change, take a screenshot and show it rather than describing it.
- When something in `/content` is missing or wrong, say so — don't fill the gap with plausible-sounding invented copy.
