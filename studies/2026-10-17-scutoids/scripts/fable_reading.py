# Fable 2026-10-17 — schematic side view of DICTO's construction (reading diagram, not to scale).
import numpy as np, sys
INK = '#2a2218'; BG = '#f4f1ea'; GOLD = '#e8b84a'; BLUE = '#7fb3d5'
W, H = 1500, 700
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Georgia, serif">',
     f'<style>.t{{font-size:24px;font-weight:600;fill:{INK}}}.s{{font-size:16px;fill:#5b5040}}.m{{font-size:15px;fill:#6b604f;font-style:italic}}</style>',
     f'<rect width="100%" height="100%" fill="{BG}"/>', '<text x="24" y="40" class="t">DICTO’s construction, side view (sketch, not to scale)</text>']
# left: dome section of a thick shell
cx, cy, Ro, Ri = 380, 720, 560, 380; span = np.radians(26)
def P(r, a): return cx + r * np.sin(a), cy - r * np.cos(a)
angs = np.linspace(-span, span, 11)
for k in range(10):
    a0, a1 = angs[k], angs[k + 1]
    # cells: straight-ish radial walls with a kink (the Y) half-way, alternating
    mid = (Ri + Ro) / 2
    pts = [P(Ri, a0), P(mid, a0 + (0.012 if k % 2 else -0.012)), P(Ro, a0), ]
    arc_o = [P(Ro, a) for a in np.linspace(a0, a1, 6)]
    pts2 = [P(Ro, a1), P(mid, a1 + (0.012 if (k + 1) % 2 else -0.012)), P(Ri, a1)]
    arc_i = [P(Ri, a) for a in np.linspace(a1, a0, 6)]
    poly = pts + arc_o + pts2 + arc_i
    hl = k == 4
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (' '.join(f'{x:.1f},{y:.1f}' for x, y in poly), '#e07a5f' if hl else '#e9e1d2', INK, 2.6 if hl else 1.3))
# surface labels
for k in range(10):
    a = (angs[k] + angs[k + 1]) / 2; x, y = P(Ro + 18, a); x2, y2 = P(Ri - 22, a)
    top5 = k % 2 == 0
    o.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-size="17" font-weight="700" fill="{"#a8761a" if top5 else "#2f6f99"}">{5 if top5 else 6}</text>')
    o.append(f'<text x="{x2:.0f}" y="{y2 + 6:.0f}" text-anchor="middle" font-size="17" font-weight="700" fill="{"#2f6f99" if top5 else "#a8761a"}">{6 if top5 else 5}</text>')
# flat cuts
yt = cy - Ro * np.cos(span) + 6; yb = cy - Ri + 4
for y, lab in ((yt, 'flat cut (top)'), (yb, 'flat cut (bottom)')):
    o.append(f'<line x1="40" y1="{y:.0f}" x2="720" y2="{y:.0f}" stroke="#c0392b" stroke-width="3" stroke-dasharray="12 7"/>')
    o.append(f'<text x="44" y="{y - 8:.0f}" class="s" fill="#c0392b">{lab}</text>')
o.append(f'<text x="380" y="118" text-anchor="middle" class="s">outer dome surface: Goldberg pattern of 5s and 6s</text>')
o.append(f'<text x="380" y="{cy - Ri + 70:.0f}" text-anchor="middle" class="s">inner dome surface: the opposite pattern (5 ↔ 6)</text>')
o.append(f'<text x="380" y="{cy - Ri + 94:.0f}" text-anchor="middle" class="s">one scutoid highlighted; the kink in each wall = the Y</text>')
# arrow
o.append(f'<text x="770" y="330" font-size="44" fill="{INK}">⟶</text>')
# right: flat layer side view, 2 layers
x0, w, hh = 860, 58, 150
for lay, yb0 in enumerate((560, 560 - hh - 18)):
    for k in range(10):
        xa, xb = x0 + k * w, x0 + (k + 1) * w
        hl = (k == 4 and lay == 0)
        o.append(f'<rect x="{xa}" y="{yb0 - hh}" width="{w}" height="{hh}" fill="{"#e07a5f" if hl else "#e9e1d2"}" stroke="{INK}" stroke-width="{2.6 if hl else 1.3}"/>')
        top5 = k % 2 == 0
        o.append(f'<text x="{(xa + xb) / 2}" y="{yb0 - hh - 4 if False else yb0 - hh + 20}" text-anchor="middle" font-size="16" font-weight="700" fill="{"#a8761a" if top5 else "#2f6f99"}">{5 if top5 else 6}</text>')
        o.append(f'<text x="{(xa + xb) / 2}" y="{yb0 - 8}" text-anchor="middle" font-size="16" font-weight="700" fill="{"#2f6f99" if top5 else "#a8761a"}">{6 if top5 else 5}</text>')
        # Y marks on the cut faces: little triangle tips touching the cut
        if k % 2 == 0: o.append(f'<polygon points="{xb},{yb0 - hh} {xb - 9},{yb0 - hh + 46} {xb + 9},{yb0 - hh + 46}" fill="#c0392b" opacity=".85"/>')
        else: o.append(f'<polygon points="{xb},{yb0} {xb - 9},{yb0 - 46} {xb + 9},{yb0 - 46}" fill="#c0392b" opacity=".85"/>')
o.append(f'<text x="{x0 + 290}" y="610" text-anchor="middle" class="s">the group, flattened: flat top, flat bottom, layers stacked straight</text>')
o.append(f'<text x="{x0 + 290}" y="634" text-anchor="middle" class="s">red = the small triangle face; its tip (the Y) sits on the flat cut</text>')
o.append(f'<text x="{W - 20}" y="{H - 16}" text-anchor="end" class="m">DICTO · dictospheres.com</text></svg>')
open(sys.argv[1], 'w').write('\n'.join(o))
