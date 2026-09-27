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
- **Images:** after adding or replacing any JPEG in `images/` or `profile/`,
  run `python3 scripts/build-images.py` to make the WebP and 800px copies.
  Each painting in `paintings.json` needs `title`, `region`, `file`, `w`, `h`
  and a descriptive `alt` (what the painting shows, not just its title).
- **SEO:** every page has canonical + Open Graph tags pointing at
  `https://www.chrishull.co.uk/`. New pages need the same head block and an
  entry in `sitemap.xml`. `assets/og-image.jpg` is the share image.
- `404.html` sets a `<base>` so its relative links work from any missing URL.
- Favicon: Jacob's ink-splat artwork (`reference/ink-splat-favicon.png`, not
  published). `scripts/make-favicons.py` crops it and writes `favicon.ico`,
  `assets/icons/favicon.svg` (light version in dark mode) and
  `apple-touch-icon.png`. Don't redraw it.
- `privacy.html` describes exactly what data the site handles. Update it
  (and its "Last updated" date) if that changes, e.g. analytics or a new
  form provider.
- Canonical domain is **www.chrishull.co.uk** (same pattern as jacobhull.me).
- Pages share one header/footer; if you change it, change it in all four
  HTML files.

## Contact form (FormSubmit)

- `contact.html` posts to FormSubmit using the **hashed form ID**
  (in the form's `action` and `data-form-id` in `contact.html`). `contact.js`
  sends it via the AJAX endpoint; without JS it posts normally and FormSubmit
  redirects to `contact.html?sent=1`.
- **Never commit the real receiving email address** (not in code, docs or
  commit messages). The repo is public and it would be scraped for spam.
- Spam protection: `_honey` honeypot field. `?painting=` prefills the
  painting field and the email subject.

## Voice

- The site is Chris's own: write in the **first person as Chris** ("I paint…",
  "I'll reply…"), warm and personal, so visitors feel they're dealing with the
  artist directly. Third person only in meta descriptions and alt text.
- Commissions usually take a week or two; new, never-painted scenes can take
  longer; a painting like one already in the gallery is quicker.
- Paintings are sold **unframed**; no framing service is offered.
- Don't name the dog in the photos anywhere on the site.


## Design

- "Watercolour Paper": warm paper `#f5f0e6`, subtle grain, wash behind the
  name only, slate ink `#2f3a45`, paintings in white mounts with soft shadow.
- **Never crop paintings.** Always show their true aspect ratio.
- Keep the visual design; propose design changes rather than making them.

## Working style

- Work in small chunks, summarise, and wait for Jacob's go-ahead.
- Verify changes in a real browser (Playwright + Chromium) at 360px and
  desktop widths, served from a `/chrishull.co.uk/` subpath.
