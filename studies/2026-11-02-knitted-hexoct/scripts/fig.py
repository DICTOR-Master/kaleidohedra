# Construction schematics for the Knitted HexOct spec (line drawings only). Writes figs/section.svg and figs/plan.svg.
import math, os
out = os.path.join(os.path.dirname(__file__), '..', 'figs')
p, d = math.sqrt(3) / 2, math.sqrt(2 / 3)
U = 92  # px per node spacing a
def svg(w, h, body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="DejaVu Sans, sans-serif">{body}</svg>'
def line(x1, y1, x2, y2, w=1.2, c='#555', dash=None):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + ' stroke-linecap="round"/>'
def text(x, y, s, size=11, anchor='middle', weight='normal', c='#000'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{c}">{s}</text>'
def dot(x, y, r=3.2, c='#000'): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
# ---- Figure 1: section seen along a row of nodes. Horizontal = across the rows (pitch p a), vertical = through the sheets.
OFF = {'A': 0, 'B': 1 / 3, 'C': 2 / 3}
def panel(x0, word, kind):
    b = []; ymin, ymax = -0.15, 3.15  # in units of the row pitch p
    X = lambda t: x0 + 40 + (t - ymin) * p * U
    Z = lambda k: 225 - k * d * U
    for k, L in enumerate(word):
        b.append(line(X(ymin), Z(k), X(ymax), Z(k), 1.6, '#000'))
        b.append(text(X(ymin) - 8, Z(k) + 4, f'{L}', 13, 'end', 'bold'))
    # links: from sheet k (letter lo) to sheet k+1 (letter hi): horizontal shift +1/3 p (pair of links, fore and aft of the
    # section plane) and -2/3 p (single link in the section plane) when hi = next letter after lo (A->B, B->C, C->A); mirrored otherwise
    for k in range(len(word) - 1):
        lo, hi = word[k], word[k + 1]; s = 1 if abs((OFF[hi] - OFF[lo]) % 1 - 1 / 3) < 1e-9 else -1
        for r in range(-2, 6):
            t = r + OFF[lo]
            for dt, w in ((s / 3, 2.6), (-2 * s / 3, 1.1)):
                t2 = t + dt
                if ymin <= t <= ymax and ymin <= t2 <= ymax: b.append(line(X(t), Z(k), X(t2), Z(k + 1), w, '#777'))
    # one traced chain of paired links through the middle sheet
    t0 = 1 + OFF[word[0]]; s1 = 1 / 3; s2 = 1 / 3 if kind == 'c' else -1 / 3
    b.append(line(X(t0), Z(0), X(t0 + s1), Z(1), 3.4, '#000'))
    b.append(line(X(t0 + s1), Z(1), X(t0 + s1 + s2), Z(2), 3.4, '#000'))
    for k, L in enumerate(word):
        for r in range(-2, 6):
            t = r + OFF[L]
            if ymin <= t <= ymax: b.append(dot(X(t), Z(k)))
    b.append(text(X(ymax) + 10, Z(1) + 4, kind, 15, 'start', 'bold'))
    b.append(text(x0 + 40 + (ymax - ymin) * p * U / 2, 50, f'{"-".join(word)}: middle sheet {kind} — links {"run straight on" if kind == "c" else "turn back"}', 12, 'middle', 'bold'))
    return ''.join(b)
W1 = 2 * (80 + 3.3 * p * U) + 30
body = panel(0, 'ABC', 'c') + panel(W1 / 2 + 10, 'ABA', 'h')
# dimension marks (left panel)
x0 = 40; Xl = lambda t: x0 + (t + 0.15) * p * U; Z = lambda k: 225 - k * d * U
body += line(Xl(0), 240, Xl(1), 240, 0.8, '#000') + text((Xl(0) + Xl(1)) / 2, 253, 'row pitch (√3/2) a', 10)
body += line(Xl(3.05) + 6, Z(0), Xl(3.05) + 6, Z(1), 0.8, '#000') + text(Xl(3.05) + 10, (Z(0) + Z(1)) / 2 + 4, '√(2/3) a', 10, 'start')
W1 = int(W1) + 40
open(os.path.join(out, 'section.svg'), 'w').write(svg(W1, 262, body))
# ---- Figure 2: plan view at one node of sheet B: projections of its 3 links down (dashed, to A) and 3 links up (solid)
def plan(cx, cy, kind):
    b = []; R = U * 0.9
    for i in range(-3, 4):
        for j in range(-3, 4):
            x = cx + (i + j / 2) * R; y = cy - j * p * R
            if math.hypot(x - cx, y - cy) < 1.25 * R: b.append(dot(x, y, 2.2, '#999'))
    dn = [-30, 90, 210]; up = [a + 180 for a in dn] if kind == 'c' else dn
    L = R / math.sqrt(3)
    for a in dn:
        b.append(line(cx, cy, cx + L * math.cos(math.radians(a)), cy - L * math.sin(math.radians(a)), 1.4, '#000', '4 3'))
    for a in up:
        ex, ey = cx + L * math.cos(math.radians(a)), cy - L * math.sin(math.radians(a))
        b.append(line(cx, cy, ex, ey, 2.2, '#000'))
        b.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="none" stroke="#000" stroke-width="1.3"/>')
    b.append(dot(cx, cy, 4.2))
    b.append(text(cx, cy - 1.35 * R, f'sheet B {kind}: links up {"opposite the links down" if kind == "c" else "over the links down"}', 11.5, 'middle', 'bold'))
    return ''.join(b)
body = plan(170, 175, 'c') + plan(520, 175, 'h')
body += text(345, 330, 'dot: node of sheet B · grey: other nodes of B · dashed: links down to A · solid: links up · ring: foot of a link up', 10)
open(os.path.join(out, 'plan.svg'), 'w').write(svg(690, 340, body))
print('figs written')
