#!/usr/bin/env python3
"""Make the favicon files from Jacob's ink-splat artwork.

Source: reference/ink-splat-favicon.png (not published). Crops a square
around the main blob, then writes:
  favicon.ico                          16, 32 and 48px
  assets/icons/favicon-192.png         for browsers that prefer PNG icons
  assets/icons/apple-touch-icon.png    180px on the paper colour (iOS home screen)
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CENTRE, SIDE = (1080, 770), 1000   # square crop around the main blob
PAPER = (245, 240, 230, 255)

src = Image.open(ROOT / "reference/ink-splat-favicon.png").convert("RGBA")
cx, cy = CENTRE
crop = src.crop((cx - SIDE // 2, cy - SIDE // 2, cx + SIDE // 2, cy + SIDE // 2))

crop.resize((48, 48), Image.LANCZOS).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
crop.resize((192, 192), Image.LANCZOS).save(ROOT / "assets/icons/favicon-192.png", optimize=True)

apple = Image.new("RGBA", (180, 180), PAPER)
inner = crop.resize((150, 150), Image.LANCZOS)
apple.alpha_composite(inner, (15, 15))
apple.convert("RGB").save(ROOT / "assets/icons/apple-touch-icon.png", optimize=True)
print("favicons written")
