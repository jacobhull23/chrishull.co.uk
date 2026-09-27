#!/usr/bin/env python3
"""Make the favicon files from Jacob's ink-splat artwork.

Source: reference/ink-splat-favicon.png (not published). Crops a square
around the main blob, then writes:
  favicon.ico                          16, 32 and 48px
  assets/icons/favicon.svg             black splat, light splat in dark mode
  assets/icons/apple-touch-icon.png    180px on the paper colour (iOS home screen)
"""
import base64, io
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CENTRE, SIDE = (1080, 770), 1000   # square crop around the main blob
PAPER = (245, 240, 230, 255)
LIGHT_INK = (233, 225, 209)  # paper tone, visible on dark browser tabs

src = Image.open(ROOT / "reference/ink-splat-favicon.png").convert("RGBA")
cx, cy = CENTRE
crop = src.crop((cx - SIDE // 2, cy - SIDE // 2, cx + SIDE // 2, cy + SIDE // 2))

crop.resize((48, 48), Image.LANCZOS).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


def png_data_uri(im):
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# SVG favicon: the black splat, swapped for a light copy when the browser is in dark mode.
icon = crop.resize((128, 128), Image.LANCZOS)
light = Image.new("RGBA", icon.size, LIGHT_INK + (255,))
light.putalpha(icon.getchannel("A"))
(ROOT / "assets/icons/favicon.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">'
    "<style>.l{display:none}@media (prefers-color-scheme:dark){.d{display:none}.l{display:inline}}</style>"
    f'<image class="d" width="128" height="128" href="{png_data_uri(icon)}"/>'
    f'<image class="l" width="128" height="128" href="{png_data_uri(light)}"/>'
    "</svg>\n"
)

apple = Image.new("RGBA", (180, 180), PAPER)
inner = crop.resize((150, 150), Image.LANCZOS)
apple.alpha_composite(inner, (15, 15))
apple.convert("RGB").save(ROOT / "assets/icons/apple-touch-icon.png", optimize=True)
print("favicons written")
