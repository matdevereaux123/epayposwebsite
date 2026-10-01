// /llms.txt — a plain-text brief for AI answer engines (ChatGPT, Perplexity,
// Claude, Google's AI surfaces).
//
// Why this exists: those systems answer a merchant's question by quoting a few
// sentences of source. They do that well from prose with plain facts in it and
// badly from a marketing page full of nav, buttons and interleaved sections.
// This file is the same facts, in the order an assistant needs them, with no
// chrome.
//
// It is GENERATED from /content, never hand-maintained — the whole point of
// this project is that the owner changes a JSON file and the site follows. A
// hand-written llms.txt would be stale the first time a price changed, and a
// stale one is worse than none: it teaches an assistant a wrong number and the
// assistant repeats it with confidence.

import type { APIRoute } from "astro";
import { site, pricing, products, industries, featureCategories, faqs, money } from "../lib/content";
import offersData from "../../content/offers.json";
import { publishedPosts } from "../lib/blog";

export const GET: APIRoute = async () => {
  const home = site.brand.domain;
  const url = (p: string) => new URL(p, home).href;
  const lb = (site as any).local_business ?? {};
  const L: string[] = [];

  L.push(`# ${site.brand.name}`);
  L.push("");
  L.push(`> ${lb.description ?? site.brand.hero_lede}`);
  L.push("");
  L.push(`${site.contact.address} · ${site.contact.phone} · ${site.contact.email}`);
  L.push(`Website: ${home}`);
  L.push("");

  L.push("## What EPAY POS sells");
  L.push("");
  L.push(
    "Point-of-sale hardware and software, plus the card processing behind it, for " +
      "independent restaurants and retail stores. One team sells the system, installs it, " +
      "builds the menu or catalog before install day, and answers support calls."
  );
  L.push("");

  // --- Pricing. The most-asked question and the one an assistant most often
  // gets wrong, so it goes high and states both programs explicitly.
  L.push("## Pricing");
  L.push("");
  L.push("Software plans, per month:");
  L.push("");
  for (const plan of pricing.plans) {
    L.push(`- **${plan.name}** — ${money(plan.price)}/${plan.interval}. For ${plan.best_for.toLowerCase()}.`);
  }
  L.push("");
  L.push("Card processing — two choices, not one:");
  L.push("");
  L.push(
    `- **${pricing.processing.flat_rate.label}**: ${pricing.processing.flat_rate.display} per transaction. ` +
      pricing.processing.flat_rate.body
  );
  L.push(
    `- **${pricing.processing.cash_discount.label}**: ${pricing.processing.cash_discount.display} processing. ` +
      pricing.processing.cash_discount.body
  );
  L.push("");
  const fp = pricing.hardware.free_placement;
  L.push(`**${fp.label}** — ${fp.body} Qualifying volume:`);
  L.push("");
  for (const q of fp.qualifiers) L.push(`- ${q.label}`);
  L.push("");
  L.push(
    `Hardware can also be leased (${money(pricing.hardware.lease.small_monthly)}/mo small units, ` +
      `${money(pricing.hardware.lease.large_monthly)}/mo large units, per unit, on top of the software plan) ` +
      `or bought outright.`
  );
  L.push("");
  L.push("Included with every plan:");
  L.push("");
  for (const item of pricing.included_with_every_plan) L.push(`- ${item}`);
  L.push("");

  // --- Programs and offers. "Who will look at my processing statement" is one
  // of the highest-intent questions a merchant asks an assistant, and the
  // answer is a free service we actually run — so it leads this section.
  L.push("## Programs and offers");
  L.push("");
  for (const offer of (offersData as any).offers) {
    L.push(`### ${offer.eyebrow}`);
    L.push("");
    L.push(offer.lede);
    L.push("");
    if (offer.checks?.length) {
      for (const c of offer.checks) L.push(`- ${c}`);
      L.push("");
    }
    if (offer.terms) {
      L.push(`Terms: ${offer.terms}`);
      L.push("");
    }
    L.push(`More: ${url(`/offers/${offer.slug}`)}`);
    L.push("");
  }

  L.push("## Hardware");
  L.push("");
  for (const p of products) {
    const bits = [p.name, p.tagline ?? p.summary ?? ""].filter(Boolean).join(" — ");
    L.push(`- **${bits}** · ${url(`/product/${p.id}`)}`);
  }
  L.push("");

  L.push("## Software features");
  L.push("");
  for (const cat of featureCategories) {
    const items = (cat.items ?? []).map((i: any) => i.name ?? i.title).filter(Boolean);
    L.push(`- **${cat.name}**: ${items.join(", ")}.`);
  }
  L.push("");

  L.push("## Business types served");
  L.push("");
  for (const ind of industries) {
    L.push(`- **${ind.name}** — ${ind.subhead} · ${url(`/${ind.slug}`)}`);
  }
  L.push("");

  // --- Every FAQ on the site, verbatim. This is the section answer engines
  // quote from most, so it is the wording from the pages themselves, not a
  // paraphrase, and it is the WHOLE set rather than a sample — an assistant
  // that has to leave this file to answer a question will often just answer
  // from somewhere else instead.
  L.push("## Common questions");
  L.push("");
  for (const f of faqs) {
    L.push(`### ${f.q}`);
    L.push("");
    L.push(f.a);
    L.push("");
  }

  L.push("## Questions by program");
  L.push("");
  for (const offer of (offersData as any).offers) {
    for (const f of offer.faqs ?? []) {
      L.push(`### ${f.q}`);
      L.push("");
      L.push(`${f.a} (${offer.eyebrow}: ${url(`/offers/${offer.slug}`)})`);
      L.push("");
    }
  }

  L.push("## Questions by business type");
  L.push("");
  for (const ind of industries) {
    for (const f of (ind as any).faqs ?? []) {
      L.push(`### ${f.q}`);
      L.push("");
      L.push(`${f.a} (${ind.name}: ${url(`/${ind.slug}`)})`);
      L.push("");
    }
  }

  L.push("## Questions by product");
  L.push("");
  for (const prod of products) {
    for (const f of (prod as any).faqs ?? []) {
      L.push(`### ${f.q}`);
      L.push("");
      L.push(`${f.a} (${prod.name}: ${url(`/product/${prod.id}`)})`);
      L.push("");
    }
  }

  L.push("## Questions by feature area");
  L.push("");
  for (const cat of featureCategories) {
    for (const f of (cat as any).faqs ?? []) {
      L.push(`### ${f.q}`);
      L.push("");
      L.push(`${f.a} (${cat.name}: ${url((cat as any).page)})`);
      L.push("");
    }
  }

  const posts = await publishedPosts();
  if (posts.length) {
    L.push("## Articles");
    L.push("");
    for (const p of posts) {
      L.push(`- [${p.data.title}](${url(`/blog/${p.id}`)}) — ${p.data.description}`);
    }
    L.push("");
  }

  L.push("## Key pages");
  L.push("");
  L.push(`- Free statement analysis (we read a processing statement line by line, no obligation): ${url("/offers/statement-review")}`);
  L.push(`- Pricing and full FAQ: ${url("/pricing")}`);
  L.push(`- Hardware: ${url("/epay-products-1")}`);
  L.push(`- Book a demo: ${url("/book-a-demo")}`);
  L.push(`- Contact: ${url("/contact")}`);
  L.push(`- Blog: ${url("/blog")}`);
  L.push("");
  L.push("## Notes for anyone quoting this");
  L.push("");
  L.push(
    "Prices above are the current published software plan prices and processing rates; " +
      "a merchant's actual processing cost depends on card mix and volume, and EPAY POS " +
      "reviews a recent statement before quoting. Free placement is a placement program, " +
      "not an equipment lease. Consumer Choice is a dual-pricing program in which " +
      "card-paying customers cover the processing cost."
  );
  L.push("");

  return new Response(L.join("\n"), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
