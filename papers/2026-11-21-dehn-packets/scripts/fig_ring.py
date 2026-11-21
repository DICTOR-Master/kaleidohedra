#!/usr/bin/env python3
"""Figure 1: the smallest ring of dihedral angles whose irrational parts cancel, for the two leads.
Angles from their exact forms (alpha = arctan(phi), beta = arccos(1/sqrt 6)); asserts that each ring is exactly 540 degrees."""
import math, json, os
phi = (1 + 5 ** 0.5) / 2
a = math.degrees(math.atan(phi)); b = math.degrees(math.acos(1 / 6 ** 0.5))
L1 = [("pyramid base", a), ("TI pent–hex", 135 - a + b), ("TI hex–hex", 270 - 2 * b), ("TI pent–hex", 135 - a + b), ("pyramid base", a)]
L2 = [("pyramid base", 135 - b), ("TD tri–dec", 135 - a + b), ("TD dec–dec", 2 * a), ("TD tri–dec", 135 - a + b), ("pyramid base", 135 - b)]
for L in (L1, L2):
    assert abs(sum(x for _, x in L) - 540) < 1e-9, sum(x for _, x in L)
FILL = {"pyramid base": "#d9d4c7", "TI pent–hex": "#9aa7b1", "TI hex–hex": "#5d6d7a", "TD tri–dec": "#9aa7b1", "TD dec–dec": "#5d6d7a"}
def pt(cx, cy, r, d):
    t = math.radians(d); return cx + r * math.cos(t), cy - r * math.sin(t)
def wedge(cx, cy, r, d0, d1, fill):
    x0, y0 = pt(cx, cy, r, d0); x1, y1 = pt(cx, cy, r, d1); big = 1 if d1 - d0 > 180 else 0
    return f'<path d="M{cx:.2f},{cy:.2f} L{x0:.2f},{y0:.2f} A{r},{r} 0 {big} 0 {x1:.2f},{y1:.2f} Z" fill="{fill}" stroke="#222" stroke-width="1"/>'
def panel(cx, cy, L, title):
    R1, R2 = 112, 70
    out = [f'<text x="{cx}" y="{cy - 150}" text-anchor="middle" font-size="13" font-weight="600">{title}</text>']
    s = 0.0; labels = []
    for name, x in L:
        d0, d1 = s, s + x
        parts = [(d0, min(d1, 360), R1)] if d0 < 360 else []
        if d1 > 360: parts.append((max(d0, 360), d1, R2))
        for p0, p1, r in parts:
            out.append(wedge(cx, cy, r, p0 % 360 if p0 >= 360 else p0, (p1 - 360) if p0 >= 360 else p1, FILL[name]))
        mid = (d0 + d1) / 2
        r = R1 + 16 if mid < 360 else R2 * 0.55
        lx, ly = pt(cx, cy, r, mid % 360)
        labels.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle" font-size="11">{x:.2f}°</text>')
        s = d1
    x0, y0 = pt(cx, cy, R1 + 4, 0); out.append(f'<line x1="{cx}" y1="{cy}" x2="{x0:.1f}" y2="{y0:.1f}" stroke="#a00" stroke-width="2"/>')
    out += labels
    out.append(f'<text x="{cx}" y="{cy + 150}" text-anchor="middle" font-size="12">sum 540° = 3π: one and a half turns</text>')
    return out
W, H = 640, 330
body = panel(160, 165, L1, "Lead 1: dodecahedron pyramid + TI") + panel(480, 165, L2, "Lead 2: icosahedron pyramid + TD")
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="DejaVu Sans, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>' + "".join(body) + "</svg>"
here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here, "..", "figures", "fig-ring.svg"), "w").write(svg)
json.dump({"lead1": L1, "lead2": L2, "alpha_deg": a, "beta_deg": b}, open(os.path.join(here, "..", "data", "fig-ring.json"), "w"), indent=1)
print("FIG RING OK", round(a, 4), round(b, 4))
