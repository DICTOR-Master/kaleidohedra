#!/usr/bin/env python3
"""The Non-Periodic Table of the Aequi (draft figure), 24 Nov 2026.

Rows: full symmetry group (by group order). Columns: m = number of face orbits.
Each cell: count, up to 3 thumbnails (fewest, median and most faces in the cell), Vacuus kind marker.
Inputs (data/inputs/): the Aequi picker data (1232 dice), the Vacuus classification CSV, the two source count tables.
Outputs: data/cells.csv, data/checks.log, figures/aequi-table.svg, figures/aequi-table.pdf, figures/paper.html (for figcheck).
Usage: python3 make_table.py <study folder>
"""
import csv, json, re, sys, os, collections as C
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle

ROOT = sys.argv[1]
INP = os.path.join(ROOT, 'data', 'inputs')
P = json.load(open(os.path.join(INP, 'aequi-picker-dice.json')))
DICE = P['dice']
CLS = list(csv.DictReader(open(os.path.join(INP, 'aequi_classification.csv'))))
ORDER = {'Ih': 120, 'Oh': 48, 'O': 24, 'Td': 24, 'Th': 24, 'T': 12}
ROWS = ['Ih', 'Oh', 'O', 'Td', 'Th', 'T']          # by group order; ties at 24 in the picker's order
log = []

# ---------- counts and checks ----------
assert len(DICE) == 1232 and len(CLS) == 1232
cnt = C.Counter((d['g'], d['m']) for d in DICE)
MS = sorted({m for _, m in cnt})
log.append(f'picker dice: {len(DICE)}; groups {sorted(set(g for g, _ in cnt))}; m range {MS[0]}..{MS[-1]}')
cnt_csv = C.Counter((r['app_group'], int(r['m'])) for r in CLS)
log.append(f'classification CSV (group, m) table equals picker table: {cnt_csv == cnt}')
same_order = all(r['N'] == str(d['N']) and r['app_group'] == d['g'] and int(r['m']) == d['m'] for r, d in zip(CLS, DICE))
log.append(f'CSV row n matches picker index n-1 (group, m, N) for all 1232: {same_order}')

def read_counts(path, keep=None):
    out = C.Counter(); lines = [l for l in open(path) if l.startswith('|')]
    head = [h.strip() for h in lines[0].strip('|\n').split('|')]
    for l in lines[2:]:
        c = [x.strip() for x in l.strip('|\n').split('|')]
        if c[0] == 'all' or (keep and c[0] not in keep): continue
        for h, v in zip(head, c):
            mm = re.fullmatch(r'm=(\d+)', h)
            if mm and v: out[(c[0], int(mm.group(1)))] += int(v)
    return out
# The 149 main-catalogue Aequi are the frame-group rows (Ih, Oh, Td, Th, T) of the complete study's table.
src = read_counts(os.path.join(INP, 'counts-aequi-complete.md'), keep={'Ih', 'Oh', 'O', 'Td', 'Th', 'T', 'I'})
src2 = read_counts(os.path.join(INP, 'counts-two-placements.md'))
log.append(f'source: complete study frame groups {sum(src.values())}, two placements {sum(src2.values())}, sum {sum(src.values()) + sum(src2.values())}')
srcsum = src + src2
bad = [(k, srcsum[k], cnt[k]) for k in set(srcsum) | set(cnt) if srcsum[k] != cnt[k]]
log.append(f'source tables (complete frame-group rows + two placements) equal picker table cell by cell: {not bad} {bad if bad else ""}')
A = C.Counter((d['g'], d['m']) for d in DICE if d['s'] == 'A'); B = C.Counter((d['g'], d['m']) for d in DICE if d['s'] == 'B')
log.append(f'picker part A (149) equals complete-study frame rows: {A == src}; part B (1083) equals two-placements table: {B == src2}')
kind = C.Counter((r['app_group'], int(r['m']), r['vacuus_kind']) for r in CLS)
total = sum(cnt.values()); log.append(f'table total {total} (expected 1232): {total == 1232}')

# ---------- geometry ----------
DIRS = np.array(P['dirs'])
COL = {'C': '#488e48', 'O': '#e8c852', 'T': '#cd3e28', 'D': '#8a5cc4', 'I': '#3a70cd', 'RD': '#b3a489', 'RT': '#8e9aa5'}
def hexrgb(h): return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])
def colof(key):  # the app's colOf: a '2' key is the base mixed 45 % toward white
    base = hexrgb(COL[key.replace('2', '')])
    return base + (1 - base) * 0.45 if key.endswith('2') else base

def solid(d):
    orbs = P['groups'][d['g']]; ns, ds, ks = [], [], []
    for oi, dep in zip(d['o'], d['d']):
        for j in orbs[oi]['dirs']: ns.append(DIRS[j]); ds.append(dep); ks.append(orbs[oi]['col'])
    ns = np.array(ns); ns /= np.linalg.norm(ns, axis=1)[:, None]; ds = np.array(ds)
    hs = HalfspaceIntersection(np.hstack([ns, -ds[:, None]]), np.zeros(3))
    V = hs.intersections; faces = []
    for i, (n, dd) in enumerate(zip(ns, ds)):
        on = np.where(np.abs(V @ n - dd) < 1e-9)[0]
        if len(on) < 3: continue
        # remove duplicate corners
        pts = []
        for q in on:
            if all(np.linalg.norm(V[q] - V[p]) > 1e-9 for p in pts): pts.append(q)
        c = V[pts].mean(0); u = V[pts[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        pts.sort(key=lambda q: np.arctan2((V[q] - c) @ w, (V[q] - c) @ u))
        faces.append((n, ks[i], V[pts]))
    assert len(faces) == d['N'], (d, len(faces))
    return faces

# view: orthographic, a general direction (no symmetry axis end-on)
vdir = np.array([0.42, 0.31, 0.85]); vdir /= np.linalg.norm(vdir)
ex = np.cross([0, 1, 0], vdir); ex /= np.linalg.norm(ex); ey = np.cross(vdir, ex)
LIGHT = 0.55 * ey - 0.35 * ex + 0.75 * vdir; LIGHT /= np.linalg.norm(LIGHT)
EDGE = '#15181c'

def draw_die(ax, d, cx, cy, r):
    faces = solid(d); R = max(np.linalg.norm(f[2], axis=1).max() for f in faces)
    for n, k, pts in faces:
        if n @ vdir <= 1e-9: continue          # convex: front faces only, no overlaps
        xy = np.c_[pts @ ex, pts @ ey] / R * r
        xy[:, 0] += cx; xy[:, 1] = cy - xy[:, 1]   # axes y grows downward
        shade = 0.60 + 0.40 * max(0.0, float(n @ LIGHT))
        ax.add_patch(Polygon(xy, closed=True, fc=np.clip(colof(k) * shade, 0, 1), ec=EDGE, lw=0.28, joinstyle='round'))

# ---------- picks ----------
cells = C.defaultdict(list)
for i, d in enumerate(DICE): cells[(d['g'], d['m'])].append(i)
picks = {}
for key, ids in cells.items():
    s = sorted(ids, key=lambda i: (DICE[i]['N'], i))
    picks[key] = s if len(s) <= 3 else [s[0], s[(len(s) - 1) // 2], s[-1]]

with open(os.path.join(ROOT, 'data', 'cells.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['group', 'order', 'm', 'count', 'heart', 'inherited_heart', 'non_heart', 'thumbnails (picker n: N faces)'])
    for g in ROWS:
        for m in MS:
            if cnt[(g, m)]:
                w.writerow([g, ORDER[g], m, cnt[(g, m)], kind[(g, m, 'heart')], kind[(g, m, 'inherited heart')], kind[(g, m, 'non-heart')],
                            '; '.join(f"{i + 1}: {DICE[i]['N']}" for i in picks[(g, m)])])

# ---------- figure (units: points; A4 text width 180 mm = 510 pt) ----------
W = 510.0; LW = 62.0; TW = 30.0; CW = (W - LW - TW) / len(MS)
TH = 25.0; HEAD_Y = 52.0; RH = 11.0 + 3 * TH + 5.0
FOOT = 70.0; H = HEAD_Y + 16 + RH * len(ROWS) + 20 + FOOT
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none', 'pdf.fonttype': 42})
fig = plt.figure(figsize=(W / 72, H / 72)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
INK, MUTED, CELL, RULE = '#1c1e22', '#5c626a', '#f1eee8', '#d8d3c9'
ax.text(0, 16, 'The Non-Periodic Table of the Aequi', fontsize=13, fontweight='bold', color=INK, va='baseline')
ax.text(0, 30, 'All 1232 Aequi by full symmetry group (rows, by group order) and number of face orbits m (columns).  DRAFT',
        fontsize=6.6, color=MUTED, va='baseline')
ax.text(LW + CW * len(MS) / 2, HEAD_Y - 6, 'number of face orbits m', fontsize=6.4, color=MUTED, ha='center')
for j, m in enumerate(MS):
    ax.text(LW + CW * (j + .5), HEAD_Y + 8, f'{m}', fontsize=8, fontweight='bold', color=INK, ha='center', va='center')
ax.text(LW + CW * len(MS) + TW / 2, HEAD_Y + 8, 'all', fontsize=7.4, fontweight='bold', color=INK, ha='center', va='center')
y0 = HEAD_Y + 16
KIND = {'Ih': 'heart', 'Oh': 'heart', 'Th': 'heart', 'O': 'inherited heart', 'Td': 'inherited heart', 'T': 'inherited heart'}
for r_, g in enumerate(ROWS):
    y = y0 + r_ * RH
    ax.plot([0, W], [y, y], color=RULE, lw=0.5)
    ax.text(2, y + 13, g, fontsize=10, fontweight='bold', color=INK, va='baseline')
    ax.text(2 + 7.2 * len(g) + 3, y + 13, f'order {ORDER[g]}', fontsize=6.2, color=MUTED, va='baseline')
    ax.text(2, y + 24, KIND[g], fontsize=6.0, color=MUTED, va='baseline', style='italic')
    ax.text(2, y + 33, 'chiral, two hands' if g in ('O', 'T') else '', fontsize=5.6, color=MUTED, va='baseline')
    rowtot = 0
    for j, m in enumerate(MS):
        n = cnt[(g, m)]; x = LW + CW * j
        if not n: continue                      # empty cell: left as a gap
        rowtot += n
        ax.add_patch(Rectangle((x + 1.2, y + 2), CW - 2.4, RH - 4, fc=CELL, ec='none'))
        ax.text(x + 4, y + 10.5, f'{n}', fontsize=7.6, fontweight='bold', color=INK, va='baseline')
        nh = kind[(g, m, 'non-heart')]
        if nh:
            ax.add_patch(Circle((x + CW - 13.5, y + 8.2), 2.3, fc='none', ec=INK, lw=0.6))
            ax.text(x + CW - 10, y + 10.5, f'{nh}', fontsize=6.2, color=INK, va='baseline')
        for t, i in enumerate(picks[(g, m)]):
            cy = y + 12 + TH * (t + .5)
            draw_die(ax, DICE[i], x + 3 + TH / 2 - 1, cy, TH / 2 - 1.2)
            ax.text(x + TH + 2.5, cy + 2, f"{DICE[i]['N']}", fontsize=5.2, color=MUTED, va='baseline')
    assert rowtot == sum(v for (gg, _), v in cnt.items() if gg == g)
    ax.text(LW + CW * len(MS) + TW / 2, y + 10.5, f'{rowtot}', fontsize=7.6, fontweight='bold', color=INK, ha='center', va='baseline')
yb = y0 + RH * len(ROWS)
ax.plot([0, W], [yb, yb], color=RULE, lw=0.5)
ax.text(2, yb + 12, 'all', fontsize=7.4, fontweight='bold', color=INK, va='baseline')
for j, m in enumerate(MS):
    ax.text(LW + CW * (j + .5), yb + 12, f"{sum(cnt[(g, m)] for g in ROWS)}", fontsize=7.0, color=INK, ha='center', va='baseline')
ax.text(LW + CW * len(MS) + TW / 2, yb + 12, f'{total}', fontsize=7.6, fontweight='bold', color=INK, ha='center', va='baseline')
# key
yk = yb + 30
ax.text(0, yk, 'Each cell: the number of Aequi, and three of them (fewest, median and most faces) when there are more than three; '
        'faces beside each die.', fontsize=6.0, color=INK, va='baseline')
ax.text(0, yk + 10, 'Empty cell: no Aequus there.   Vacuus kind (under each group): heart = centrally symmetric; '
        'inherited heart = parallel faces, no centre.', fontsize=6.0, color=INK, va='baseline')
ax.add_patch(Circle((3, yk + 17.8), 2.3, fc='none', ec=INK, lw=0.6))
ax.text(8, yk + 20, 'k: k of the cell are non-heart (no two faces parallel; 5 dice in all).', fontsize=6.0, color=INK, va='baseline')
ax.text(0, yk + 34, 'Face colours (app):', fontsize=6.0, color=INK, va='baseline')
xs = 62
for key, lab in [('C', 'cube'), ('O', 'octahedron'), ('T', 'tetrahedron'), ('D', 'dodecahedron'), ('I', 'icosahedron'),
                 ('RD', 'rhombic dodecahedron'), ('RT', 'rhombic triacontahedron')]:
    ax.add_patch(Rectangle((xs, yk + 28.5), 7, 7, fc=colof(key), ec=EDGE, lw=0.3))
    ax.text(xs + 9.5, yk + 34, lab, fontsize=5.8, color=INK, va='baseline'); xs += 13 + 3.35 * len(lab) + 4
ax.text(0, yk + 45, 'Paler tone: the same family in its second place (second icosahedron placement, second tetrahedron, second half of a split orbit).',
        fontsize=6.0, color=INK, va='baseline')
ax.text(W, H - 4, 'DICTO', fontsize=6.4, color=MUTED, ha='right', va='baseline', fontweight='bold')
out = os.path.join(ROOT, 'figures')
fig.savefig(os.path.join(out, 'aequi-table.svg')); fig.savefig(os.path.join(out, 'aequi-table.pdf'))
open(os.path.join(out, 'paper.html'), 'w').write(
    '<!doctype html><meta charset="utf-8"><style>body{margin:0}img{width:100%;display:block}</style>'
    '<figure style="margin:0"><img src="aequi-table.svg" alt="The Non-Periodic Table of the Aequi"></figure>\n')
open(os.path.join(ROOT, 'data', 'checks.log'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(log)); print(f'figure {W:.0f} x {H:.0f} pt; columns m = {MS}')
