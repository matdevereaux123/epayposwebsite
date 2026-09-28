# Generated product art

Four images in `public/img/store/` are **vector illustrations, not photographs**:

| File | Why it was drawn |
|---|---|
| `paper-mini.jpg` | Generic thermal roll for the A800 handheld. |
| `paper-station.jpg` | Generic thermal roll for the Epson TM-m30II. |

**Withdrawn:** drawn versions of `cash-drawer` and `card-trays` were rejected by
the owner and moved to `tools/removed-photos/`. Both slots are back to
placeholders, waiting on real photography of the branded units.

The `.svg` sources are here. The brand mark is the real
`public/img/epay-logo.png`, recoloured to flat white by an SVG `feColorMatrix`
filter rather than redrawn, so it is the actual logo.

To regenerate after editing an SVG:

    qlmanage -t -s 1200 -o . cash-drawer.svg
    sips -s format jpeg -s formatOptions 92 cash-drawer.svg.png --out cash-drawer.jpg

Replace all four with real photography once the drawers and trays arrive.
