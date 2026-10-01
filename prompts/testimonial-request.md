# Collecting real merchant testimonials

The site is wired for these already: add entries to `content/testimonials.json`
and the homepage band and the Review schema switch on by themselves. No code
change needed. What is missing is the quotes.

## Why these have to be real

Published testimonials are advertising. In the US the FTC's rule on consumer
reviews and testimonials (in force since 2024) treats fabricated endorsements
as a deceptive practice carrying civil penalties per violation, and Google's
structured data policy treats invented review markup as spam — a manual action
risks the organic rankings the rest of this work is meant to protect. Beyond
the rules: a merchant who switches because of a quote from a restaurant that
does not exist is a chargeback-and-churn problem later.

One real line from Pho Street is worth more than twelve invented ones.

## Start with the merchants who already said yes to something

- **Pho Street** (Lake Orion, MI) already approved publishing their install
  video — confirmed by Matt, 2026-09-16, see `site.json > home_video`. They are
  the warmest ask on the list.
- Anyone who has had a statement review and switched: they already know the
  number they saved, which makes `metric` easy.
- Anyone who called support at 9pm and got a person. That is the actual
  differentiator and it is what a quote should say.

## The ask (email or text)

> Subject: One line from you for our site?
>
> Hi [name] — quick favour, no pressure.
>
> We're putting a short section on the EPAY POS site with a few words from
> owners who actually run the system. Would you be up for one or two sentences
> on what changed for you after switching? Anything honest is useful — the
> install, the rates, the support, whatever stands out.
>
> If it's easier, just answer one of these and I'll tidy it into a sentence for
> you to approve before anything goes up:
>
> - What was the worst part of your old setup?
> - What does the system do now that you'd miss?
> - Roughly what are you saving a month, if you're happy to say?
>
> I'd put your name, your business and your city next to it. Nothing goes live
> until you've seen the exact wording and said yes.
>
> Thanks either way,
> Matt

## Before anything goes on the site

1. They have seen the **exact** wording and approved it.
2. You have that approval in writing — record it in the `permission` field
   (e.g. `"email 2026-10-04"`). This is the field that protects you later.
3. Do not polish a quote into something they did not say. Tightening grammar is
   fine; adding a claim is not.
4. `rating` is optional and only goes in if they actually gave a number. A quote
   with no rating still renders and still gets Review schema — it simply shows
   no stars. Never fill this in to make the average look better.
5. `metric` only if they said the figure themselves.

## Then

Add the entries to `content/testimonials.json` following `_shape_example`, and
drop a photo at `/img/testimonials/` if they are happy to provide one. Three
entries is the threshold for the homepage band; the schema emits from the
first. Run `bash tools/preview.sh` and the section appears.

**One caveat worth knowing:** Google does not show rich-result stars for
self-serving reviews — a business publishing reviews about itself. The value
here is on-page conversion and AI answer engines having something concrete to
quote, not stars in the search listing. For stars in search, the route is
Google Business Profile reviews, which is a separate job (and the
"Google Business Profile & Reviews Checklist" lead magnet on the site already
walks through it).
