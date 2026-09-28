#!/usr/bin/env python3
"""
Builds the photo portal's slot list.

Every image and video path in content/*.json is a slot. A built copy of the
site (a `dist/` folder) tells us which pages each slot appears on, its crop
ratio, and the name the page gives it. Slots that no page displays are kept
but marked unused, so nobody spends time on a photo that changes nothing.

    python3 tools/photo-portal/build_slots.py <path-to-dist>

Writes tools/photo-portal/portal.html from portal.template.html with the
slot list inlined. Re-run it after content changes, then republish.
"""

import glob
import html
import json
import os
import re
import sys

TOOL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(TOOL))
CONTENT = os.path.join(ROOT, "content")
MEDIA = re.compile(r"^/(img|video)/")

# Folder -> (section order, section title, what belongs here)
SECTIONS = [
    ("/img/epay-logo", 1, "Logo", "Shows in the header and footer of every page."),
    ("/video/", 2, "Homepage video", "The Pho Street client spotlight on the homepage."),
    ("/img/pages/pho-street-poster", 2, "Homepage video", ""),
    ("/img/pages/", 3, "Page photos", "Main photos for the standalone pages and the homepage promo blocks."),
    ("/img/products/", 4, "Hardware", "Product shots and in-use photos. Each shows on several pages."),
    ("/img/industries/", 5, "Industry pages", "One main photo and three gallery photos per business type."),
    ("/img/features/", 6, "Feature pages", "One main photo per feature page."),
    ("/img/apps/", 7, "Software apps", "One photo per app on the EPAY Software page."),
    ("/img/third-party/", 8, "Third-party platforms", "Clover, NCR, NRS, TSYS, gateways and lodging."),
    ("/img/store/", 9, "Shop", "Supplies and EPAY gear. Square photos on a clean background."),
    ("/img/logos/", 10, "Merchant logos", "The merchant logo strip on the homepage."),
]
UNUSED = (99, "Not on any page yet", "These are listed in the content files, but no page shows them. Uploading one changes nothing on the site until a page uses it.")

FALLBACK_RATIO = {"/img/store/": "1 / 1", "/img/logos/": "8 / 3", "/img/epay-logo": "150 / 69", "/video/": "16 / 9", "/img/pages/pho-street-poster": "16 / 9"}


def section_for(path):
    for prefix, order, title, blurb in SECTIONS:
        if path.startswith(prefix):
            return order, title, blurb
    return 50, "Other", ""


def walk(node, keys, ancestors, fname, out):
    if isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, keys + [i], ancestors, fname, out)
    elif isinstance(node, dict):
        for k, v in node.items():
            if k.startswith("_"):  # notes and shape examples, not real slots
                continue
            walk(v, keys + [k], ancestors + [node], fname, out)
    elif isinstance(node, str) and MEDIA.match(node):
        parent = ancestors[-1] if ancestors else {}
        owner = ""
        for a in reversed(ancestors):
            if isinstance(a.get("name"), str) and (a.get("slug") or a.get("id") or a.get("page")):
                owner = a["name"]
                break
        name = parent.get("name") if isinstance(parent.get("name"), str) else ""
        if name and name == owner and keys[-1] != "file":
            name = f"{owner} — {'main photo' if 'hero' in str(keys[-1]) else 'product shot'}"
        out.setdefault(node, {"path": node, "json": [], "name": name, "owner": owner})
        out[node]["json"].append(f"{fname} → " + ".".join(str(k) for k in keys))


def scan_dist(dist):
    pages, titles = {}, {}
    for f in glob.glob(os.path.join(dist, "**", "*.html"), recursive=True):
        rel = os.path.relpath(f, dist)
        route = "/" + rel.replace("index.html", "").rstrip("/")
        route = route[:-5] if route.endswith(".html") else route
        route = route or "/"
        raw = open(f, encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", raw, re.S)
        titles[route] = html.unescape(t.group(1).split("|")[0].strip()) if t else route
        text = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
        for m in re.finditer(r'<span class="imgslot[^"]*"([^>]*)>.*?imgslot__name[^>]*>(.*?)</span>.*?imgslot__path[^>]*>(.*?)</span>', text, re.S):
            ratio = re.search(r"aspect-ratio:\s*([^;\"]+)", m.group(1))
            rec = pages.setdefault(m.group(3), {"pages": set(), "names": set(), "ratio": None})
            rec["pages"].add(route)
            rec["names"].add(html.unescape(m.group(2)))
            if ratio:
                rec["ratio"] = ratio.group(1).strip()
        for m in re.finditer(r"<(?:img|video|source)\b[^>]*>", text):
            for attr in ("src", "poster"):
                a = re.search(attr + r'="(/(?:img|video)/[^"]+)"', m.group(0))
                if a:
                    pages.setdefault(a.group(1), {"pages": set(), "names": set(), "ratio": None})["pages"].add(route)
    return pages, titles


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    dist = sys.argv[1]
    slots = {}
    for f in sorted(glob.glob(os.path.join(CONTENT, "*.json"))):
        walk(json.load(open(f)), [], [], os.path.basename(f), slots)
    found, titles = scan_dist(dist)
    site = json.load(open(os.path.join(CONTENT, "site.json")))
    video = site.get("home_video", {})
    video_paths = {video.get("file"), video.get("poster")}

    rows = []
    for path, s in slots.items():
        seen = found.get(path, {"pages": set(), "names": set(), "ratio": None})
        pages = set(seen["pages"])
        notes = []
        if path in video_paths:
            pages = {"/"}
            if path == video.get("file"):
                notes.append("Plays on its own on the homepage, looping, with no sound and no controls. If the video is over 20 MB, skip this one: Matthew is pulling it from Google Drive.")
            else:
                notes.append("A still frame from the video. It shows while the video loads, and to visitors whose device is set to reduce motion.")
        order, title, blurb = section_for(path)
        if not pages:
            order, title, blurb = UNUSED
        if path.startswith("/img/logos/"):
            notes.append("Only upload a merchant's logo once they've given written permission.")
        name = sorted(seen["names"])[0] if seen["names"] else s["name"]
        name = re.sub(r"\s+hero$", " — main photo", name or "", flags=re.I)
        if not name:
            name = os.path.splitext(os.path.basename(path))[0].replace("-", " ").capitalize()
        ext = os.path.splitext(path)[1].lower()
        kind = "video" if ext in (".mp4", ".webm", ".mov") else "image"
        ratio = seen["ratio"] or next((r for p, r in FALLBACK_RATIO.items() if path.startswith(p)), "4 / 3")
        max_edge = 1200 if path.startswith(("/img/logos/", "/img/epay-logo")) else 1600
        rows.append({
            "path": path,
            "name": name,
            "owner": s["owner"],
            "section": title,
            "sectionOrder": order,
            "sectionBlurb": blurb,
            "pages": sorted(pages, key=lambda r: (r != "/", r)),
            "ratio": ratio,
            "kind": kind,
            "format": "png" if ext == ".png" else ("video" if kind == "video" else "jpeg"),
            "maxEdge": max_edge,
            "notes": notes,
            "source": s["json"],
        })
    rows.sort(key=lambda r: (r["sectionOrder"], r["path"] if r["section"] not in ("Industry pages", "Hardware", "Third-party platforms") else ""))
    # keep JSON order inside owner-grouped sections so galleries sit under their page
    order_index = {p: i for i, p in enumerate(slots)}
    rows.sort(key=lambda r: (r["sectionOrder"], order_index[r["path"]]))

    data = {
        "pageTitles": {r: titles.get(r, r) for r in sorted({p for row in rows for p in row["pages"]})},
        "slots": rows,
    }
    template = open(os.path.join(TOOL, "portal.template.html"), encoding="utf-8").read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = template.replace("/*__SLOTS__*/null", payload)
    open(os.path.join(TOOL, "portal.html"), "w", encoding="utf-8").write(out)

    used = [r for r in rows if r["sectionOrder"] != UNUSED[0]]
    print(f"{len(rows)} slots ({len(used)} on pages, {len(rows) - len(used)} unused) -> portal.html")
    for sec in sorted({(r['sectionOrder'], r['section']) for r in rows}):
        print(f"  {sec[1]}: {sum(1 for r in rows if r['section'] == sec[1])}")


if __name__ == "__main__":
    main()
