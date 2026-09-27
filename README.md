# chrishull.co.uk

Static site for C. J. Hull, watercolour artist. Hosted on GitHub Pages; no build step.

| Path | What it is |
|---|---|
| `index.html` | Gallery (home) — renders `paintings.json` |
| `paintings.json` | Painting list. **Array order = gallery order.** Fields: `title`, `region`, `file`, `w`, `h` |
| `images/` | Painting images |
| `assets/css/site.css` | All styles (paper, wash, frames, gallery, lightbox) |
| `assets/js/gallery.js` | Justified grid, region filters, lightbox (keyboard + swipe) |
| `assets/fonts/` | Self-hosted Cormorant Garamond + Inter (OFL) |

All links are relative, so the site works at `<user>.github.io/chrishull.co.uk/` and at `chrishull.co.uk`.

**Add a painting:** drop the JPEG in `images/`, add an entry to `paintings.json` with its pixel width/height.

**Preview locally:** `python3 -m http.server` in the repo root, then open http://localhost:8000 (opening the file directly won't load `paintings.json`).
