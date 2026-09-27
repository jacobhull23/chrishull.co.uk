#!/usr/bin/env python3
"""Generate responsive image variants for the site.

For every JPEG in images/ and profile/ this writes:
  <dir>/<name>.webp        full size, WebP
  <dir>/800/<name>.webp    800px wide, WebP
  <dir>/800/<name>.jpg     800px wide, JPEG (fallback)
The original <dir>/<name>.jpg is kept as the full-size JPEG fallback.

Run after adding or replacing images:  python3 scripts/build-images.py
Requires Pillow (pip install pillow). Existing up-to-date outputs are skipped.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["images", "profile"]
SMALL = 800


def fresh(out: Path, src: Path) -> bool:
    return out.exists() and out.stat().st_mtime >= src.stat().st_mtime


def save(im: Image.Image, out: Path, fmt: str) -> None:
    out.parent.mkdir(exist_ok=True)
    if fmt == "WEBP":
        im.save(out, "WEBP", quality=82, method=6)
    else:
        im.save(out, "JPEG", quality=84, optimize=True, progressive=True)


def main() -> None:
    made = 0
    for d in DIRS:
        for src in sorted((ROOT / d).glob("*.jpg")):
            outs = {
                src.with_suffix(".webp"): ("WEBP", None),
                src.parent / "800" / (src.stem + ".webp"): ("WEBP", SMALL),
                src.parent / "800" / (src.stem + ".jpg"): ("JPEG", SMALL),
            }
            todo = {o: v for o, v in outs.items() if not fresh(o, src)}
            if not todo:
                continue
            im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
            for out, (fmt, width) in todo.items():
                img = im
                if width and im.width > width:
                    img = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
                save(img, out, fmt)
                made += 1
    print(f"wrote {made} files")


if __name__ == "__main__":
    main()
