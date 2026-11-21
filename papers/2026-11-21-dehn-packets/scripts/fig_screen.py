#!/usr/bin/env python3
"""Figure 2: the 47 centre pyramids of the screen by class (Proposition 6). Counts asserted: 3 + 10 + 17 + 17 = 47."""
import os
rows = [("packet zero, no partner needed", 3, "#d9d4c7"), ("one helper in the library", 10, "#9aa7b1"),
        ("two helpers, no single one", 17, "#5d6d7a"), ("none in the library (one or two helpers)", 17, "#c9b9a6")]
assert sum(n for _, n, _ in rows) == 47
W, x0, u = 640, 250, 11
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 168" font-family="DejaVu Sans, sans-serif" font-size="11">']
for i, (t, n, c) in enumerate(rows):
    y = 14 + i * 32
    out.append(f'<text x="{x0 - 8}" y="{y + 15}" text-anchor="end">{t}</text><rect x="{x0}" y="{y}" width="{n * u}" height="22" fill="{c}" stroke="#222"/>'
               f'<text x="{x0 + n * u + 6}" y="{y + 15}" font-weight="600">{n}</text>')
out.append(f'<text x="{x0}" y="160" font-size="10" fill="#444">pyramids of the 5 Platonic, 13 Archimedean and 13 Catalan solids (47 in all)</text></svg>')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "fig-screen.svg"), "w").write("\n".join(out))
print("fig-screen ok")
