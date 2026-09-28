// FONT CONFIGURATION — the only place fonts are set.
//
// Change a family name here and every heading, paragraph, price, and label
// on all 24 pages updates. Base.astro builds the Google Fonts URL from this
// and overrides the CSS variables in global.css.
//
// Current system is two families:
//
//   Effra            — headings only. Self-hosted; see note below.
//   Source Sans Pro  — everything else: running copy, nav, buttons, form
//                      fields, and every figure and eyebrow label.
//
// NOTE ON EFFRA: Effra is a commercial face from Dalton Maag and is NOT on
// Google Fonts (their API returns 400 for it). It has to be licensed and
// self-hosted. Drop the .woff2 files in /public/fonts using the filenames in
// the @font-face block in global.css and it takes effect with no change
// here. Until those files exist, headings fall back to Source Sans Pro,
// which keeps the site coherent rather than dropping to a system font.
//
// NOTE ON WEIGHTS: Source Sans Pro has no 500. Asking for one makes the
// browser round to 400 or synthesise a fake weight, so the UI weight in this
// system is 600.

export interface FontSpec {
  /** Exact family name, as it appears on Google Fonts. */
  family: string;
  /** Weights to load. Fewer weights = faster page. */
  weights: string;
  /** Fallback stack if the webfont fails to load. */
  fallback: string;
  /** Set false for a self-hosted or system font — skips the Google request. */
  google?: boolean;
  /** Override the Google Fonts axis spec for variable fonts. */
  googleSpec?: string;
}

export const fonts: Record<"display" | "body" | "data", FontSpec> = {
  // Headings. Self-hosted — see the note above.
  display: {
    family: "Effra",
    weights: "500;700",
    fallback: '"Source Sans Pro", system-ui, sans-serif',
    google: false,
  },

  // All running copy, buttons, nav, form fields.
  // Self-hosted since 2026-09-28: the Google Fonts stylesheet was render-
  // blocking for 310ms and its `display=swap` reflowed every section below the
  // hero once the face arrived — Lighthouse measured 0.2 CLS from it. The two
  // .woff2 files live in public/fonts and are preloaded in Base.astro.
  // Source Sans Pro is OFL licensed, so self-hosting is permitted.
  body: {
    family: "Source Sans Pro",
    weights: "400;600",
    fallback: "system-ui, -apple-system, sans-serif",
    google: false,
  },

  // Prices, rates, stats, eyebrow labels.
  //
  // This was JetBrains Mono. It is the body face now, because the brief is
  // two families. Figures stay aligned via `font-variant-numeric:
  // tabular-nums` in global.css, but they no longer read as monospace —
  // design-system.md calls that "the one signature detail", so this is a
  // deliberate departure. To restore it, set this back to a monospace family
  // and nothing else needs to change.
  data: {
    family: "Source Sans Pro",
    weights: "400;600",
    fallback: "system-ui, sans-serif",
    google: false,
  },
};

/** Builds the single Google Fonts request for whichever families need it. */
export function googleFontsHref(): string | null {
  const specs = Object.values(fonts)
    .filter((f) => f.google !== false)
    .map((f) => f.googleSpec ?? `${f.family.replace(/ /g, "+")}:wght@${f.weights}`);

  // Two roles share a family — request it once.
  const unique = [...new Set(specs)];

  if (unique.length === 0) return null;
  return `https://fonts.googleapis.com/css2?${unique.map((s) => `family=${s}`).join("&")}&display=swap`;
}

/** CSS custom property block that overrides the defaults in global.css. */
export function fontVars(): string {
  return `:root{
  --font-display:"${fonts.display.family}",${fonts.display.fallback};
  --font-body:"${fonts.body.family}",${fonts.body.fallback};
  --font-data:"${fonts.data.family}",${fonts.data.fallback};
}`;
}
