# SEO and launch prep

Run this after the missing pages are built and before DNS cutover.

---

**SEO audit**

```
Audit the site for SEO:

1. Verify every generated route matches url_map_do_not_change in
   content/site.json. Report any mismatch — do NOT silently "fix" a slug.
   Two are misspelled on purpose (/liqour-stores, /pizzeria-s).
2. Check every page has a unique title under 60 chars and a description
   under 155. Flag duplicates.
3. Confirm sitemap.xml and robots.txt are generating correctly.
4. Confirm the LocalBusiness, Product, and FAQPage schema all validate.
5. Check every image has descriptive alt text and explicit width/height.
6. Run Lighthouse on the homepage, /pricing, and one industry page.
   Show me the scores. Fix anything under 95 on performance or accessibility.

Give me the findings before making changes.
```

**Analytics**

```
Add Google Analytics 4 (measurement ID: <ID>) and the Search Console
verification meta tag (<TOKEN>) to Base.astro. Load GA4 async so it
doesn't block rendering.
```

**Forms — test these, don't assume**

```
Deploy, then submit the contact form, the demo request, and the statement
upload on the live preview URL. Confirm each one appears in the Netlify
dashboard under Forms. Set up email notifications to info@epaypos.net.
```

Forms silently failing is the most common way a relaunch loses a month of leads.
Test them on the deployed site, not locally — Netlify Forms only work once
deployed.

**Cutover**

```
Walk me through pointing epaypos.net at Netlify. I need the exact DNS
records to change in Wix. Remind me what NOT to touch.
```

The answer should be: change the A record and the `www` CNAME. Leave
`portal.epaypos.net` alone — it's a separate subdomain and must keep pointing
where it points now.
