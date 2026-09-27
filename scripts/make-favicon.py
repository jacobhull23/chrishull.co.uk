#!/usr/bin/env python3
"""Draw the ink-splat favicon as SVG (assets/icons/favicon.svg).

A seeded random splat: a round body with uneven lobes and a few spikes,
plus some separate droplets. Change SEED for a different splat.
"""
import math, random
from pathlib import Path

SEED = 7
INK, INK_DARK_MODE = "#2f3a45", "#e9e1d1"
random.seed(SEED)
C = 32  # centre of a 64x64 viewBox


def blob_path(cx, cy, pts):
    """Smooth closed curve through polar points (Catmull-Rom -> cubic Bezier)."""
    xy = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a, r in pts]
    n = len(xy)
    d = f"M{xy[0][0]:.2f},{xy[0][1]:.2f}"
    for i in range(n):
        p0, p1, p2, p3 = xy[i - 1], xy[i], xy[(i + 1) % n], xy[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}"
    return d + "Z"


# Body: 28 points around a circle; a few become spikes, the rest wobble.
pts, spikes = [], {2, 7, 11, 16, 20, 25}
for i in range(28):
    a = 2 * math.pi * i / 28 + random.uniform(-0.05, 0.05)
    if i in spikes:
        r = random.uniform(25, 29.5)
    elif (i - 1) % 28 in spikes or (i + 1) % 28 in spikes:
        r = random.uniform(17, 19)
    else:
        r = random.uniform(18.5, 22)
    pts.append((a, r))
body = blob_path(C, C, pts)

# Droplets flung out beyond the spikes.
drops = []
for a_deg, dist, r in [(-62, 27.5, 3.2), (35, 27.5, 2.6), (148, 27, 3.4), (262, 27.5, 2.6)]:
    a = math.radians(a_deg)
    drops.append((C + dist * math.cos(a), C + dist * math.sin(a), r))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<style>path,circle{{fill:{INK}}}@media (prefers-color-scheme:dark){{path,circle{{fill:{INK_DARK_MODE}}}}}</style>
<path d="{body}"/>
{"".join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}"/>' for x, y, r in drops)}
</svg>
'''
out = Path(__file__).resolve().parent.parent / "assets/icons/favicon.svg"
out.write_text(svg)
print("wrote", out)
