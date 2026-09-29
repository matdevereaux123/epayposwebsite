// Single entry point for all site content.
// Pages import from here — never read the JSON files directly, and never
// hardcode a price, feature, or piece of copy into a page.

import siteData from "../../content/site.json";
import pricingData from "../../content/pricing.json";
import productsData from "../../content/products.json";
import featuresData from "../../content/features.json";
import industriesData from "../../content/industries.json";
import faqData from "../../content/faq.json";
import testimonialsData from "../../content/testimonials.json";
import capabilitiesData from "../../content/capabilities.json";
import integrationsData from "../../content/integrations.json";
import headingsData from "../../content/headings.json";
import storeData from "../../content/store.json";
import thirdPartyData from "../../content/third-party.json";
import enquiryData from "../../content/enquiry.json";
import statementAnalyzerData from "../../content/statement-analyzer.json";
import partnersData from "../../content/partners.json";

export const site = siteData;
export const pricing = pricingData;
export const products = productsData.products;
export const featureCategories = featuresData.categories;
export const industries = industriesData.industries;
export const faqs = faqData.faqs;
export const testimonials = testimonialsData.testimonials;
export const stats = testimonialsData.stats;
export const capabilities = capabilitiesData.capabilities;
export const integrations = integrationsData.integrations;
export const store = storeData;
export const thirdPartyPlatforms = (thirdPartyData as any).platforms;
export const enquiry = enquiryData;
export const statementAnalyzer = statementAnalyzerData;
export const partners = partnersData;

/** What the browser needs to attribute a visit: ids, slugs, nothing else. */
export function partnerConfig() {
  return {
    param: (partnersData as any).param,
    days: (partnersData as any).window_days,
    partners: (partnersData as any).partners
      .filter((p: any) => p.active)
      .map((p: any) => ({
        id: p.id,
        name: p.name,
        application_slug: p.application_slug || "",
        lead_slug: p.lead_slug || "",
      })),
  };
}

/**
 * Every piece of equipment a merchant can ask about, in one list.
 *
 * The enquiry dropdown and the `data-enquire` hooks on product cards both read
 * from this, so a card can never offer an option the form does not have. Ids
 * are namespaced by source because a shop item and a product could otherwise
 * collide.
 */
export type EquipmentOption = { id: string; name: string; group: string };

export function equipmentOptions(): EquipmentOption[] {
  const g = (enquiryData as any).groups;
  const out: EquipmentOption[] = [];

  for (const p of productsData.products as any[]) {
    out.push({ id: `product:${p.id}`, name: p.name, group: g.epay });
  }
  for (const i of (storeData as any).items as any[]) {
    out.push({ id: `shop:${i.id}`, name: i.name, group: g.shop });
  }
  for (const plat of (thirdPartyData as any).platforms as any[]) {
    for (const it of plat.items ?? []) {
      out.push({
        id: `third-party:${plat.slug}:${slugify(it.name)}`,
        name: `${plat.name} — ${it.name}`,
        group: g.third_party,
      });
    }
  }
  return out;
}

/** Stable id fragment for an item name. Must match what the cards emit. */
export function slugify(s: string): string {
  return s
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

/** Capabilities relevant to a vertical. "both" always applies. */
export function capabilitiesFor(audience: "restaurant" | "retail") {
  return capabilities.filter((c) => c.audience === audience || c.audience === "both");
}

export function integrationsFor(audience: "restaurant" | "retail") {
  return integrations.filter((i) => i.audience === audience || i.audience === "both");
}

/** Money, formatted one way everywhere. Always rendered in the mono face. */
export function money(n: number): string {
  return n.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  });
}

export function planById(id: string) {
  return pricing.plans.find((p) => p.id === id);
}

/**
 * Monthly lease rate for one unit of a product.
 *
 * `lease_monthly` on the product wins when present — some hardware is not on
 * either standard tier. Otherwise it falls back to the small/large rate in
 * pricing.json. Four components derived this independently before; they all
 * call this now, so a rate cannot be right in the builder and wrong on the
 * product page.
 */
export function leaseMonthly(product: any): number {
  if (typeof product?.lease_monthly === "number") return product.lease_monthly;
  const lease = (pricingData as any).hardware.lease;
  return product?.lease_tier === "small" ? lease.small_monthly : lease.large_monthly;
}

export function productById(id: string) {
  return products.find((p) => p.id === id);
}

export function featureCategoryById(id: string) {
  return featureCategories.find((c) => c.id === id);
}

/** Cheapest plan — used in hero copy so the number can never go stale. */
export function startingPrice(): number {
  return Math.min(...pricing.plans.map((p) => p.price));
}

/** Section headings. Never hardcode a heading into a page — add it to headings.json. */
export const headings = headingsData;

/** Fill {name}/{list} tokens in a heading template. */
export function fill(template: string, vars: Record<string, string>): string {
  return template.replace(/\{(\w+)\}/g, (_, k) => vars[k] ?? `{${k}}`);
}

const SMALL_WORDS = new Set(["a","an","the","and","but","or","nor","for","so","yet","as","at","by","in","of","off","on","per","to","via","vs","with","from","into","onto"]);

/** Title Case for heading fragments that come from lists (e.g. product best_for). */
export function titleCase(s: string): string {
  return s
    .split(" ")
    .map((w, i, all) => {
      if (/[A-Z]/.test(w.slice(1))) return w;
      if (i > 0 && i < all.length - 1 && SMALL_WORDS.has(w.toLowerCase())) return w.toLowerCase();
      return w.charAt(0).toUpperCase() + w.slice(1);
    })
    .join(" ");
}
