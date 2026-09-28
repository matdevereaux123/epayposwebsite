#!/usr/bin/env python3
"""
SEO audit of a built copy of the site. Read-only: it reports, it never edits.

    python3 tools/seo_audit.py [dist-folder]      (default: ~/epay-site-preview/dist)

Checks every page for: title (present, unique, <=60), meta description
(present, unique, 70-155), exactly one <h1>, canonical link, images with alt
text and width/height, internal links that go nowhere, valid JSON-LD, and
that noindex pages stay out of the sitemap while every indexable page is in it.
Also checks robots.txt and the sitemap exist. Blog drafts are skipped.
Prints a Markdown report; exit code 1 if anything is marked FIX.
"""
import glob, html, json, os, re, sys
from urllib.parse import urlparse

DIST = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/epay-site-preview/dist")
pages = {}
for f in sorted(glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True)):
    rel = os.path.relpath(f, DIST)
    route = "/" + rel.replace("index.html", "").rstrip("/")
    route = route[:-5] if route.endswith(".html") else route
    pages[route or "/"] = open(f, encoding="utf-8").read()

files = {"/" + os.path.relpath(p, DIST) for p in glob.glob(os.path.join(DIST, "**", "*"), recursive=True) if os.path.isfile(p)}
fix, warn = [], []
titles, descs = {}, {}
indexable = set()

def text(t): return re.sub(r"<!--.*?-->", "", t, flags=re.S)

for route, raw in pages.items():
    t = text(raw)
    noindex = bool(re.search(r'<meta name="robots" content="noindex', t))
    draft = "DRAFT: only visible" in t
    if draft:
        continue
    if not noindex:
        indexable.add(route)
    title = re.search(r"<title>(.*?)</title>", t, re.S)
    title = html.unescape(title.group(1).strip()) if title else ""
    desc = re.search(r'<meta name="description" content="(.*?)"', t, re.S)
    desc = html.unescape(desc.group(1).strip()) if desc else ""
    if noindex:
        continue
    if not title: fix.append(f"`{route}`: no <title>")
    elif len(title) > 60: fix.append(f"`{route}`: title is {len(title)} characters (max 60): {title}")
    titles.setdefault(title, []).append(route)
    if not desc: fix.append(f"`{route}`: no meta description")
    elif len(desc) > 155: fix.append(f"`{route}`: description is {len(desc)} characters (max 155)")
    elif len(desc) < 70: warn.append(f"`{route}`: description is only {len(desc)} characters (aim for 70-155)")
    descs.setdefault(desc, []).append(route)
    h1 = len(re.findall(r"<h1[\s>]", t))
    if h1 != 1: fix.append(f"`{route}`: {h1} <h1> tags (should be exactly 1)")
    if '<link rel="canonical"' not in t: fix.append(f"`{route}`: no canonical link")
    for img in re.findall(r"<img\b[^>]*>", t):
        # `alt=""` is correct for a decorative image, and Astro serialises it as a
        # bare `alt`. Only a genuinely absent attribute is a fault.
        if not re.search(r"\balt\b", img): fix.append(f"`{route}`: image without alt text")
        if not (re.search(r"\bwidth=", img) and re.search(r"\bheight=", img)): warn.append(f"`{route}`: image without width/height")
    for href in set(re.findall(r'href="(/[^"#?]*)', t)):
        h = href.rstrip("/") or "/"
        if h in pages or href in files or h + "/index.html" in files or h.endswith(".xml"):
            continue
        fix.append(f"`{route}`: broken internal link to `{href}`")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: json.loads(html.unescape(block))
        except Exception as e: fix.append(f"`{route}`: structured data doesn't parse ({e})")

for v, rs in titles.items():
    if v and len(rs) > 1: fix.append(f"Duplicate title on {', '.join(rs)}: {v}")
for v, rs in descs.items():
    if v and len(rs) > 1: fix.append(f"Duplicate description on {', '.join(rs)}")

if not os.path.exists(os.path.join(DIST, "robots.txt")): fix.append("robots.txt is missing")
sm = "".join(open(p).read() for p in glob.glob(os.path.join(DIST, "sitemap-*.xml")) if "index" not in p)
if not sm: fix.append("sitemap is missing")
else:
    in_sm = {(urlparse(u).path.rstrip("/") or "/") for u in re.findall(r"<loc>(.*?)</loc>", sm)}
    for r in sorted(indexable - in_sm):
        if r != "/404": warn.append(f"`{r}` is indexable but not in the sitemap")
    for r in sorted(in_sm - indexable):
        if r in pages: fix.append(f"`{r}` is in the sitemap but marked noindex")

print(f"# SEO audit — {len(indexable)} indexable pages\n")
print(f"**{len(fix)} to fix, {len(warn)} to consider.**\n")
if fix: print("## Fix\n" + "\n".join(f"- {x}" for x in sorted(set(fix))) + "\n")
if warn: print("## Consider\n" + "\n".join(f"- {x}" for x in sorted(set(warn))) + "\n")
if not fix and not warn: print("Everything checked out.")
sys.exit(1 if fix else 0)
