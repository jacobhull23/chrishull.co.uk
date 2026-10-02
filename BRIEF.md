# C. J. Hull – Watercolour Artist: website rebuild brief

## Goal
Replace chrishull.co.uk (currently Carrd, paid) with a static site on **GitHub Pages**, maintained by Jacob (Chris's son) using Claude Code. Chris does not edit the site himself.

## Decisions made
- **Paintings only.** Ignore the "Photos" folder on Drive; it holds photographs, not paintings.
- **No sold status, no shop.** Every piece is a one-off original. The gallery shows *examples of past work*. The site's job is to get **commission enquiries**. Originals start from **£300**.
- **Design: option B ("Watercolour Paper"), toned down with option A's restraint.** Clean, and the art does the talking. See `reference/shot-b.png`, and `reference/mock-b.html` for the CSS starting point.
  - Warm paper background (~#f5f0e6) with a very subtle grain.
  - A soft watercolour wash (blue / ochre / mauve from his palette) behind the name in the header only.
  - Paintings in a thin white border with a soft shadow, like mounted prints. **Never crop paintings**: always show them at their true aspect ratio.
  - Type: Cormorant Garamond for the name, headings and titles; Inter for the UI. Self-host the fonts.
  - Accent / ink colour ~#2f3a45 (slate).
  - Rejected: a full-bleed hero (it crops the art).
- **Domain:** chrishull.co.uk is registered by Jacob on **Namecheap**. Jacob's own site (jacobhull.me) already runs on GitHub Pages, so follow the same pattern: apex A records for GitHub Pages, a `www` CNAME, a `CNAME` file in the repo, and Enforce HTTPS.

## Page structure
| Page | Contents |
|---|---|
| **Gallery** (home) | Name/wash header, a one-line intro ("Every painting is an original, one-of-a-kind watercolour. These are examples of past work — commission a scene you love, or ask about something similar."), and filters: All / North Wales / Lake District / Scotland. Use a justified or masonry grid. Clicking a painting opens a lightbox (keyboard + swipe) with the title, region and an **"Enquire about a painting like this"** button that links to Contact with the title pre-filled. |
| **Commissions** | How it works in three steps, originals from £300, and what to send (reference photos, size, occasion/deadline). |
| **About** | Bio (below), a photo of Chris sketching (`profile/`), a press/credentials strip. |
| **Contact** | Enquiry form via **Formspree or Web3Forms** (static-friendly; Jacob picks one). Fields: name, email, painting of interest (prefilled from `?painting=`), message. |

Also needed: responsive layout down to 360px, lazy-loaded responsive images (generate ~800w and ~1600w, WebP + JPEG fallback), good `alt` text, per-page meta/OG tags, a sitemap, and a favicon. The old site used an "ink splat" favicon, which is in Drive under `Logos and Header Images/`; it wasn't downloaded into this kit. There's no build step unless one clearly earns its place: plain HTML/CSS/JS reading `paintings.json` is fine, or Eleventy if templating helps.

## Content
**Bio (from the current site, reword lightly):**
Chris Hull is a watercolour artist based in North Wales, on the edge of Snowdonia National Park. He uses watercolour's fluid spontaneity to capture the dramatic scenery around him. His work has been shown in galleries across North Wales and the Lake District and is held in private collections worldwide. He was the Welsh Regional Final winner and a grand finalist on Channel 4's *Watercolour Challenge*, and has been featured in *Great British Life* magazine.

**Paintings:** 56 in `images/`, with metadata in `paintings.json` (title, region, file, w, h). Regions: North Wales (28, which includes Anglesey/Conwy coast pieces), Lake District (26), Scotland (2). The images are resized to a 1600px long edge. The Drive originals are low-res exports (~0.5–1.4 MB).

**Source (Google Drive, Jacob's account), folder "Dad's Art":** Snowdonia, Lake District and Scotland are the source of truth. "All Pictures" is *not* complete (it's missing Snowdon Horseshoe, Moel Fam and two Rydal paintings). "Slideshow" is a subset. "Photos" is excluded.

## Open items for Jacob to confirm
- [ ] **Titles:** some were cleaned from filenames or taken from "All Pictures" names. Please check these especially:
  - Rydal Water / Rydal Water (II) / Rydal Water (III) / Rydal Water in Autumn: four different paintings.
  - Two "Cwm Idwal and the Devil's Kitchen" and two "Helm Crag Across Grasmere" paintings: need distinct titles.
  - "Castell y Gwynt" (was "Castle y Gwynt") and "Y Garn and Shepherd's Hut" (was "Shephereds").
- [ ] **Painting order:** which 6–8 paintings lead the gallery? The mockup used Llyn Ogwen & Y Garn, Derwent Trees in Autumn, The Glyders, Eilean Donan Castle, Misty Derwent Water, Above Langdale.
- [ ] **Contact email** to receive enquiries, and the choice of form service.
- [ ] Should Scotland be its own filter with only 2 paintings, or fold into "All"?
- [ ] Cut over DNS only after the new site is verified; then cancel Carrd.

## Suggested build order
1. Repo + GitHub Pages skeleton, fonts, base styles (paper, wash, frames).
2. Gallery page from `paintings.json`, with the lightbox.
3. Commissions, About, Contact (with the form service).
4. Image pipeline (sizes/WebP), SEO/meta, favicon, accessibility pass.
5. Preview on `*.github.io`, Jacob reviews, then connect the domain **through Cloudflare** (free plan) so AI-bot blocking is enforced, not just requested:
   1. Add `chrishull.co.uk` to Cloudflare and switch the domain's nameservers in Namecheap to Cloudflare's (the domain stays registered at Namecheap).
   2. In Cloudflare DNS: apex A records to GitHub Pages and a `www` CNAME to `jacobhull23.github.io`, all **DNS only (grey cloud)** at first.
   3. Add a `CNAME` file (`www.chrishull.co.uk`) to the repo; set the custom domain in GitHub **Settings → Pages** and wait for its certificate, then tick **Enforce HTTPS**.
   4. Turn the Cloudflare proxy on (orange cloud), set **SSL/TLS → Full (strict)**, and enable **Security → Bots → Block AI bots** (and AI Labyrinth if offered). Leave search engines allowed.
   5. Check the site, Google Search Console verification and the contact form, then cancel Carrd.
