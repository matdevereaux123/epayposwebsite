# Prompt 4 — Everyday updates

This is the payoff. Copy, edit, send. Each of these is one message.

---

**Change a price**
> In pricing.json, change the Lite plan to $44.99 and add "unlimited menu items" to its feature list. Rebuild and deploy.

**Add a feature you just launched**
> We launched direct Uber Eats integration. Add it to the integrations category in features.json, surface it on the pizzeria and full service restaurant pages, and add a short section to /integrations. Match the existing voice — plain and specific, no marketing adjectives.

**Add a whole new industry page**
> Add a "Food Truck" entry to industries.json following the exact shape of the pizzeria entry. Write the copy yourself: quick service, mobile, tight counter space, needs to work offline when signal drops, cash-heavy. Recommended plan is Lite. Then confirm the page generated at /food-truck and add it to the Restaurant nav dropdown.

**Seasonal promo**
> Add a dismissible announcement bar above the header: "Free terminal placement through March 31." Links to /pricing. Store the dismissal in sessionStorage. Put the text in site.json so it's easy to change or remove later.

**New hardware**
> Add the new EPAY Kiosk to products.json. Self-order kiosk, works for quick service and cafes. Put it on the products page and the cafe/bakery industry page. I'll send the product photo separately.

**Turn on social proof**
> Add this testimonial to testimonials.json: [quote, name, business, city]. Once there are at least three, turn on the social proof section on the homepage.

**Health check — run this monthly**
> Audit the site: any hardcoded prices, feature lists, or copy living outside /content? Any broken internal links? Any page missing a unique meta title or description? Any image without alt text? Give me the list first, then fix them.
