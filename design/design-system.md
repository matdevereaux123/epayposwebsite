# EPAY POS — Design System

## The direction, in one line

Keep the site the merchants already recognize — white background, EPAY blue,
the same section order — and raise the execution. This is not a redesign. It's
the current site built properly.

## What "built properly" means here

The live Wix site has four fixable problems. Everything below exists to solve them.

1. **Card rows don't align.** The three bundle images are 224px, 311px, and 292px wide at different crops. Fix: every card image uses the `.media` wrapper with a locked 16:10 ratio and `object-fit: cover`.
2. **There is no type scale.** Some section headings outsize the hero subhead; product blurbs range from 20 to 60 words. Fix: one scale, defined below, and body copy capped at ~35 words per card.
3. **Blue means four different things.** It appears in the logo, headings, buttons, and decorative icons at slightly different values. Fix: `--epay` means "this is clickable." `--accent-deep` is for labels and the one blue band. Headings are near-black, never blue.
4. **The company logo is used as a decorative icon.** It appears three times in "Business & Solution Types" as a stand-in for section icons. Fix: those are headings. The logo appears exactly twice on a page — header and footer.

## Palette

| Token | Hex | Use |
|---|---|---|
| `--canvas` | `#FFFFFF` | default page background |
| `--surface` | `#F4F8FB` | tinted band, image wells, footer |
| `--epay` | `#1B9FD8` | brand blue. Buttons, links, active states. Means clickable |
| `--accent-deep` | `#0E6FA0` | brand deep blue. Eyebrow labels, hover, the blue band |
| `--text` | `#0A1520` | headings and body |
| `--text-muted` | `#4A5F70` | supporting copy |
| `--rule` | `#E4EDF3` | hairline borders |
| `--rule-strong` | `#CBDCE7` | emphasized borders, button outlines |

Both blues are your existing brand colors, unchanged.

**Band rhythm:** white → tinted → white down the page, with exactly **one** solid
`--accent-deep` band per page (on the homepage, the four value props). One blue
band reads as deliberate; three read as decoration.

## Logo

The logo is an image asset, not type. It lives at `public/img/epay-logo.png` and
is referenced through `site.brand.logo` in `content/site.json`, so it is set in
one place and used by both the header and the footer.

- Header: 38px tall, auto width
- Footer: 44px tall, auto width
- Never recolor it, never place it on a colored background, never use it as a
  section icon or bullet
- Export at 2x minimum. An SVG is better than a PNG if you have one — update the
  path in `site.json` and nothing else changes

## Typography

**Fonts are configured in exactly one file: `src/lib/fonts.ts`.** Change a family
name there and every page updates. Never hardcode a `font-family` in a component.

| Role | Notes |
|---|---|
| Display | headings only, weights 600–700, tight tracking |
| Body | all running copy, buttons, nav, 400/500 |
| Data | every price, rate, percentage, stat, and eyebrow label. Must stay monospace with `tabular-nums` — that alignment is the point |

The display and body faces should match the existing Wix site so the rebuild
reads as the same company. The data face is a deliberate addition: the current
site has no monospace, and setting money in it is what makes the page read like
a payment processor rather than a template.

Scale is defined in `src/styles/global.css` and is fluid via `clamp()`. Do not
introduce a size outside it.

The one signature detail: **every dollar figure and rate on the site is
monospace with tabular numerals.** It's small, it's consistent, and it makes the
page read like it belongs to a payment processor.

## The batch line

A hairline rule carrying a settlement-style readout — merchant count, flat rate,
starting price — that counts up once on entry and then settles. It reappears as
the divider between major sections. Numbers used here must be real; ask rather
than invent one.

## Motion

Restrained, always gated behind `prefers-reduced-motion`.

- **Allowed:** the batch line's one-time count-up; a 12px fade-and-rise on section entry, staggered ~60ms; button color change on hover; the header border appearing on scroll.
- **Not allowed:** parallax, floating shapes, particles, autoplaying carousels, anything moving while someone is reading.

The current site has an autoplaying product carousel. It should not come back —
it hides content from both merchants and search engines.

**Owner-approved exceptions (Matt, 2026-09-18).** These two move on purpose.
Don't "fix" them back to the rule above:

- **Homepage client-spotlight video** (`VideoSlot.astro`). Plays on its own,
  muted, looping, with no controls and no way to pause. It's always muted
  because browsers block autoplay with sound. Reduce-motion visitors get the
  still poster.
- **Merchant logo strip** (`LogoWall.astro`), directly under the homepage
  banner. Scrolls sideways without end and pauses on hover. Reduce-motion
  visitors get a still, centered row. The product carousel ban still stands.

**Line art (Matt, 2026-09-18).** White sections carry faint outline
drawings of the EPAY mark: the triangle cut into parallel bands, smaller
echoes of it, light rays at the mark's 60° angle, and a small dot grid. The
logo gradient and the fade-out are drawn into the SVG files themselves:
`public/img/art/hero-art.svg` (every page's top banner, on the right) and
`ribbon-art.svg` (small marks along the bottom of every other section,
alternating sides). They're plain background images. **Don't use CSS masks
for this.** Safari rendered them as a solid blue box. Strength is set in the
"Line art" block in `global.css` (`--art-hero`, `--art-ribbon`).

Motion is limited to a slow drift of a few pixels. Matt had the light
streams removed, along with the sweep on the batch line and the self-drawing
stat underlines: each read as a line growing across the page. Don't bring
back anything that grows or travels along a line.

## Components

**Buttons.** Primary: solid `--epay`, white text. Secondary: 1px `--rule-strong`
border, `--accent-deep` text. Two CTAs maximum in view at once.

**Cards.** White, 1px `--rule` border, 12px radius. No drop shadows. Hover
darkens the border only. Card images always use `.media`.

**Pricing.** Plan name in display face, price in mono, features as a plain list
with hairline separators. No checkmark icons on every row.

**Images.** Product photography sits in a `.media` well on `--surface`. Every
image needs real alt text and explicit width/height.

## What to avoid

- Headings set in blue. Headings are `--text`; blue is for what you can click.
- Stock photos of people shaking hands or pointing at laptops.
- Decorative icons that duplicate the heading next to them.
- Drop shadows and gradients. The current site's depth comes from borders and the tinted band.
- Fake testimonials or invented statistics. `content/testimonials.json` is empty on purpose.
