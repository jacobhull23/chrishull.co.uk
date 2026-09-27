# chrishull.co.uk — notes for Claude

Website for C. J. Hull, watercolour artist (Jacob's dad). Plain HTML/CSS/JS, no
build step. Deployed to GitHub Pages on every push to `main`
(`.github/workflows/deploy.yml`, which copies the public files into `_site`).
Never push to `main`; work on a branch and open a PR.

`BRIEF.md` is the spec: decisions, page structure, content, open items and the
build order. Read it before starting work.

## How the site is built

- All links and asset paths are **relative** so the site works at
  `jacobhull23.github.io/chrishull.co.uk/` and at the custom domain.
- The gallery is rendered by `assets/js/gallery.js` from `paintings.json`;
  array order is gallery order.
- If you add a new top-level file or folder the site needs, add it to the
  "Assemble site" step in the workflow, or it won't be published.
- Fonts are self-hosted from Fontsource (latin subset) in `assets/fonts/`.

## Design

- "Watercolour Paper": warm paper `#f5f0e6`, subtle grain, wash behind the
  name only, slate ink `#2f3a45`, paintings in white mounts with soft shadow.
- **Never crop paintings.** Always show their true aspect ratio.
- Keep the visual design; propose design changes rather than making them.

## Working style

- Work in small chunks, summarise, and wait for Jacob's go-ahead.
- Verify changes in a real browser (Playwright + Chromium) at 360px and
  desktop widths, served from a `/chrishull.co.uk/` subpath.
