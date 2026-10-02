#!/usr/bin/env python3
"""Generate responsive image variants for the site, with copyright metadata.

For every JPEG in images/ and profile/ this:
  1. stamps the original <dir>/<name>.jpg with Chris's copyright (EXIF + XMP),
     losslessly, without re-compressing the image;
  2. writes, each carrying the same metadata:
       <dir>/<name>.webp        full size, WebP
       <dir>/800/<name>.webp    800px wide, WebP
       <dir>/800/<name>.jpg     800px wide, JPEG (fallback)
The original <dir>/<name>.jpg is kept as the full-size JPEG fallback.

The metadata names Chris as creator and copyright holder and links to the
contact page. Google Images reads it (creator, credit, copyright notice), and
it travels with the file if someone saves the image.

Run after adding or replacing images:  python3 scripts/build-images.py
Requires Pillow and piexif (pip install pillow piexif).
Existing up-to-date outputs are skipped.
"""
from pathlib import Path

import piexif
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["images", "profile"]
SMALL = 800

CREATOR = "Chris Hull"
COPYRIGHT = "© Chris Hull. All rights reserved. Do not reproduce without permission."
EXIF_COPYRIGHT = "Copyright Chris Hull. All rights reserved. Do not reproduce without permission."  # EXIF is ASCII-only
CONTACT_URL = "https://www.chrishull.co.uk/contact.html"

XMP = f"""<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
    xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/"
    xmlns:plus="http://ns.useplus.org/ldf/xmp/1.0/"
    photoshop:Credit="{CREATOR}"
    xmpRights:Marked="True"
    xmpRights:WebStatement="{CONTACT_URL}">
   <dc:creator><rdf:Seq><rdf:li>{CREATOR}</rdf:li></rdf:Seq></dc:creator>
   <dc:rights><rdf:Alt><rdf:li xml:lang="x-default">{COPYRIGHT}</rdf:li></rdf:Alt></dc:rights>
   <plus:Licensor><rdf:Seq><rdf:li rdf:parseType="Resource"><plus:LicensorURL>{CONTACT_URL}</plus:LicensorURL></rdf:li></rdf:Seq></plus:Licensor>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>""".encode("utf-8")
XMP_HEADER = b"http://ns.adobe.com/xap/1.0/\x00"


def exif_bytes(existing: bytes | None = None) -> bytes:
    """EXIF with Artist and Copyright set, keeping any existing tags (e.g. orientation)."""
    data = piexif.load(existing) if existing else {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    data["0th"][piexif.ImageIFD.Artist] = CREATOR.encode()
    data["0th"][piexif.ImageIFD.Copyright] = EXIF_COPYRIGHT.encode("ascii")
    return piexif.dump(data)


def stamp_original(path: Path) -> bool:
    """Add EXIF + XMP to a JPEG without re-encoding it. Returns True if it changed."""
    raw = path.read_bytes()
    if XMP_HEADER in raw and EXIF_COPYRIGHT.encode("ascii") in raw:
        return False
    with Image.open(path) as im:
        existing = im.info.get("exif")
    piexif.insert(exif_bytes(existing), str(path))
    raw = path.read_bytes()
    if XMP_HEADER not in raw:
        # Insert an APP1 XMP segment straight after the JPEG start marker.
        payload = XMP_HEADER + XMP
        segment = b"\xff\xe1" + (len(payload) + 2).to_bytes(2, "big") + payload
        raw = raw[:2] + segment + raw[2:]
        path.write_bytes(raw)
    return True


def fresh(out: Path, src: Path) -> bool:
    return out.exists() and out.stat().st_mtime >= src.stat().st_mtime


def save(im: Image.Image, out: Path, fmt: str) -> None:
    out.parent.mkdir(exist_ok=True)
    meta = {"exif": exif_bytes(), "xmp": XMP}
    if fmt == "WEBP":
        im.save(out, "WEBP", quality=82, method=6, **meta)
    else:
        im.save(out, "JPEG", quality=84, optimize=True, progressive=True, **meta)


def main() -> None:
    stamped = made = 0
    for d in DIRS:
        for src in sorted((ROOT / d).glob("*.jpg")):
            stamped += stamp_original(src)
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
    print(f"stamped {stamped} originals, wrote {made} files")


if __name__ == "__main__":
    main()
