#!/usr/bin/env python3
"""The Non-Periodic Table of the Aequi: all subgroups (draft figure), 24 Nov 2026.

All 4553 Aequi of study 2026-11-19-aequi-complete, by full symmetry group (rows, by group order) and m (columns).
Each cell: count, up to 3 thumbnails (fewest, median, most faces), Vacuus kind computed per die from its face planes.
Two panels (groups of order >= 12, < 12), one A4-wide page each.
Usage: python3 make_table_all.py <this study folder> <study 2026-11-19-aequi-complete folder>
Outputs: data/all-cells.csv, data/all-dice-kinds.csv, data/all-checks.log,
         figures/aequi-table-all-a.svg, figures/aequi-table-all-b.svg, figures/aequi-table-all.pdf (two pages), figures/all/paper.html.
"""
import csv, json, re, sys, os, glob, ast, collections as C
from decimal import Decimal, getcontext
import numpy as np
from scipy.spatial import HalfspaceIntersection
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
from matplotlib.backends.backend_pdf import PdfPages

ROOT, SRC = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(SRC, 'scripts'))
from groups import DIRS                      # the 74 frame directions, unit vectors, in the study's index order
getcontext().prec = 70
log = []

# ---------- dice ----------
DICE = []
for f in sorted(glob.glob(os.path.join(SRC, 'data', 'dice', '*.json'))):
    d = json.load(open(f))
    L = lambda v: ast.literal_eval(v) if isinstance(v, str) else v
    sizes = L(d['orbit_sizes']); fd = L(d['face_directions']); dep60 = L(d['depths_60_digits']); labs = L(d['orbits'])
    assert sum(sizes) == len(fd) == int(d['N']) and len(sizes) == len(dep60) == len(labs) == int(d['m'])
    DICE.append(dict(file=os.path.basename(f), label=d['label'], g=d['group'], order=int(d['symmetry_order']), m=int(d['m']),
                     N=int(d['N']), sizes=sizes, fd=fd, dep=[Decimal(x) for x in dep60], labs=labs, hands=d['hands']))
log.append(f'dice records: {len(DICE)}')
assert len(DICE) == 4553

# ---------- Vacuus kind per die, from the face planes ----------
# heart: centrally symmetric (every face n, d has a face -n, d); inherited heart: some two faces parallel (n and -n both faces), no centre;
# non-heart: no two faces parallel.  Directions: the 74 frame directions; -n found by exact index match (frame directions differ by >= 0.1).
NEG = [int(np.argmin(np.linalg.norm(DIRS + v, axis=1))) for v in DIRS]
assert all(np.linalg.norm(DIRS[NEG[i]] + DIRS[i]) < 1e-12 for i in range(len(DIRS)))
mindiff = Decimal(10)
def kind_of(d):
    global mindiff
    depth = {}
    for k, s in enumerate(d['sizes']):
        for j in d['fd'][sum(d['sizes'][:k]):sum(d['sizes'][:k + 1])]: depth[j] = d['dep'][k]
    par = [j for j in depth if NEG[j] in depth]
    if not par: return 'non-heart'
    cs = len(par) == len(depth)
    if cs:
        for j in depth:
            diff = abs(depth[j] - depth[NEG[j]])
            if diff > Decimal('1e-40'): mindiff = min(mindiff, diff); cs = False; break
    return 'heart' if cs else 'inherited heart'
for d in DICE: d['kind'] = kind_of(d)
CENTRO = {'Ci', 'C2h', 'D2h', 'D3d', 'S6', 'D4h', 'D5d', 'D6h', 'D8h', 'D10h', 'Th', 'Oh', 'Ih'}   # groups containing -I
agree = all((d['kind'] == 'heart') == (d['g'] in CENTRO) for d in DICE)
log.append(f'heart (centrally symmetric from the planes) exactly when the full group contains -I: {agree}')
log.append('dice with every face paired by a parallel face but unequal depths: ' + ('none' if mindiff == 10 else f'gap >= {float(mindiff):.3g}') + ' (equal depths agree to 1e-40)')
# cross-check with the Vacuus classification of the 1232 (the 149 main-catalogue dice are in both)
VC = {r['record']: r['vacuus_kind'] for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'inputs', 'aequi_classification.csv')))}
both = [d for d in DICE if d['file'] in VC]
log.append(f'dice also in the 1232 classification: {len(both)}; same Vacuus kind: {sum(VC[d["file"]] == d["kind"] for d in both)}')

# ---------- counts and checks ----------
cnt = C.Counter((d['g'], d['m']) for d in DICE)
ORD = {}
for d in DICE: ORD.setdefault(d['g'], d['order']); assert ORD[d['g']] == d['order']
def read_counts(path):
    out = C.Counter(); order = {}; lines = [l for l in open(path) if l.startswith('|')]
    head = [h.strip() for h in lines[0].strip('|\n').split('|')]
    for l in lines[2:]:
        c = [x.strip() for x in l.strip('|\n').split('|')]
        if c[0] == 'all': continue
        order[c[0]] = int(c[1])
        for h, v in zip(head, c):
            mm = re.fullmatch(r'm=(\d+)', h)
            if mm and v: out[(c[0], int(mm.group(1)))] += int(v)
    return out, order
SRCN, SRCORD = read_counts(os.path.join(SRC, 'data', 'counts.md'))
ROWS = list(SRCORD)                                  # the source table's row order: by group order
assert [SRCORD[g] for g in ROWS] == sorted(SRCORD.values(), reverse=True)
log.append(f'dice records = counts.md cell by cell: {SRCN == cnt}; group orders agree: {SRCORD == ORD}')
TCSV = C.Counter((r['group'], int(r['m'])) for r in csv.DictReader(open(os.path.join(SRC, 'data', 'table.csv'))))
log.append(f'table.csv = counts.md cell by cell: {TCSV == SRCN}')
total = sum(cnt.values()); log.append(f'total {total} (expected 4553): {total == 4553}')
MS = sorted({m for _, m in cnt})
kinds = C.Counter((d['g'], d['m'], d['kind']) for d in DICE)
for k in ('heart', 'inherited heart', 'non-heart'): log.append(f'{k}: {sum(v for kk, v in kinds.items() if kk[2] == k)}')

# ---------- colours (the app's: a mixed orbit takes its icosahedral family; O8/4 = tetrahedron; repeats paler) ----------
COL = {'C': '#488e48', 'O': '#e8c852', 'T': '#cd3e28', 'D': '#8a5cc4', 'I': '#3a70cd', 'RD': '#b3a489', 'RT': '#8e9aa5'}
def hexrgb(h): return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])
def orbit_key(lab):
    lab = re.sub(r' \(\d+\)$', '', lab); fams = re.split(r'\+', lab.split('/')[0]); size = lab.split('/')[1] if '/' in lab else ''
    for f, k in (('RT24', 'RT'), ('I12', 'I'), ('D12', 'D'), ('RD12', 'RD')):
        if f in fams: return k
    if fams == ['O8'] and size.startswith('4'): return 'T'
    return 'O' if 'O8' in fams else 'C'
def die_colours(d):
    seen = C.Counter(); out = []
    for lab in d['labs']:
        k = orbit_key(lab); base = hexrgb(COL[k]); t = [0, 0.45, 0.70, 0.25, 0.85][min(seen[k], 4)]; seen[k] += 1
        out.append(base + (1 - base) * t)
    return out

vdir = np.array([0.42, 0.31, 0.85]); vdir /= np.linalg.norm(vdir)
ex = np.cross([0, 1, 0], vdir); ex /= np.linalg.norm(ex); ey = np.cross(vdir, ex)
LIGHT = 0.55 * ey - 0.35 * ex + 0.75 * vdir; LIGHT /= np.linalg.norm(LIGHT)
EDGE = '#15181c'
def draw_die(ax, d, cx, cy, r):
    cols = die_colours(d); ns, ds, cs = [], [], []
    for k, s in enumerate(d['sizes']):
        for j in d['fd'][sum(d['sizes'][:k]):sum(d['sizes'][:k + 1])]: ns.append(DIRS[j]); ds.append(float(d['dep'][k])); cs.append(cols[k])
    ns = np.array(ns); ds = np.array(ds)
    V = HalfspaceIntersection(np.hstack([ns, -ds[:, None]]), np.zeros(3)).intersections
    R = np.linalg.norm(V, axis=1).max(); nf = 0
    for n, dd, col in zip(ns, ds, cs):
        on = np.where(np.abs(V @ n - dd) < 1e-9)[0]; pts = []
        for q in on:
            if all(np.linalg.norm(V[q] - V[p]) > 1e-9 for p in pts): pts.append(q)
        if len(pts) < 3: continue
        nf += 1
        if n @ vdir <= 1e-9: continue
        c = V[pts].mean(0); u = V[pts[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        pts.sort(key=lambda q: np.arctan2((V[q] - c) @ w, (V[q] - c) @ u))
        xy = np.c_[V[pts] @ ex, V[pts] @ ey] / R * r; xy[:, 0] += cx; xy[:, 1] = cy - xy[:, 1]
        ax.add_patch(Polygon(xy, closed=True, fc=np.clip(col * (0.60 + 0.40 * max(0.0, float(n @ LIGHT))), 0, 1), ec=EDGE, lw=0.28, joinstyle='round'))
    assert nf == d['N'], (d['label'], nf)

cells = C.defaultdict(list)
for i, d in enumerate(DICE): cells[(d['g'], d['m'])].append(i)
picks = {}
for key, ids in cells.items():
    s = sorted(ids, key=lambda i: (DICE[i]['N'], i))
    picks[key] = s if len(s) <= 3 else [s[0], s[(len(s) - 1) // 2], s[-1]]
with open(os.path.join(ROOT, 'data', 'all-cells.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['group', 'order', 'm', 'count', 'heart', 'inherited_heart', 'non_heart', 'drawn dice (record file: N faces)'])
    for g in ROWS:
        for m in MS:
            if cnt[(g, m)]:
                w.writerow([g, ORD[g], m, cnt[(g, m)], kinds[(g, m, 'heart')], kinds[(g, m, 'inherited heart')], kinds[(g, m, 'non-heart')],
                            '; '.join(f"{DICE[i]['file']}: {DICE[i]['N']}" for i in picks[(g, m)])])
with open(os.path.join(ROOT, 'data', 'all-dice-kinds.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['record', 'label', 'group', 'order', 'm', 'N', 'vacuus_kind'])
    for d in DICE: w.writerow([d['file'], d['label'], d['g'], d['order'], d['m'], d['N'], d['kind']])

# ---------- figure: two panels, one page each (units: points; 510 pt = 180 mm) ----------
W = 510.0; LW = 74.0; TW = 34.0; CW = (W - LW - TW) / len(MS); TH = 24.0; RH = 12.0 + TH + 9.0
INK, MUTED, CELL, RULE = '#1c1e22', '#5c626a', '#f1eee8', '#d8d3c9'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none', 'pdf.fonttype': 42})
PANELS = [('a', 'groups of order 12 or more', [g for g in ROWS if ORD[g] >= 12]), ('b', 'groups of order less than 12', [g for g in ROWS if ORD[g] < 12])]
CHIRAL = {g for g in ROWS if all(d['hands'] == 'two hands' for d in DICE if d['g'] == g)}
def kind_text(g):
    k = C.Counter(d['kind'] for d in DICE if d['g'] == g)
    if len(k) == 1: return next(iter(k))
    return ' · '.join(f'{n} {kk}' for kk, n in sorted(k.items(), key=lambda t: -t[1]) if kk != 'non-heart') + (f" · {k['non-heart']} non-heart (○)" if k['non-heart'] else '')
pdf = PdfPages(os.path.join(ROOT, 'figures', 'aequi-table-all.pdf'))
for tag, sub, rows in PANELS:
    last = tag == 'b'; HEAD_Y = 54.0; FOOT = 74.0 if last else 6.0
    H = HEAD_Y + 16 + RH * len(rows) + (22 if last else 0) + FOOT
    fig = plt.figure(figsize=(W / 72, H / 72)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
    ax.text(0, 16, 'The Non-Periodic Table of the Aequi — all subgroups', fontsize=13, fontweight='bold', color=INK, va='baseline')
    ax.text(0, 30, f'({tag}) {sub}.  All 4553 Aequi by full symmetry group (rows, by group order) and number of face orbits m.  DRAFT',
            fontsize=6.6, color=MUTED, va='baseline')
    ax.text(LW + CW * len(MS) / 2, HEAD_Y - 6, 'number of face orbits m', fontsize=6.4, color=MUTED, ha='center')
    for j, m in enumerate(MS): ax.text(LW + CW * (j + .5), HEAD_Y + 8, f'{m}', fontsize=8, fontweight='bold', color=INK, ha='center', va='center')
    ax.text(LW + CW * len(MS) + TW / 2, HEAD_Y + 8, 'all', fontsize=7.4, fontweight='bold', color=INK, ha='center', va='center')
    y0 = HEAD_Y + 16
    for r_, g in enumerate(rows):
        y = y0 + r_ * RH; ax.plot([0, W], [y, y], color=RULE, lw=0.5)
        ax.text(2, y + 13, g, fontsize=9.5, fontweight='bold', color=INK, va='baseline')
        ax.text(2, y + 22.5, f'order {ORD[g]}' + ('  ·  two hands' if g in CHIRAL else ''), fontsize=5.8, color=MUTED, va='baseline')
        kt = kind_text(g); parts = kt.split(' · ')
        for q, ptxt in enumerate(parts): ax.text(2, y + 31 + 7 * q, ptxt, fontsize=5.6, color=MUTED, va='baseline', style='italic')
        rowtot = 0
        for j, m in enumerate(MS):
            n = cnt[(g, m)]; x = LW + CW * j
            if not n: continue
            rowtot += n
            ax.add_patch(Rectangle((x + 1.2, y + 2), CW - 2.4, RH - 4, fc=CELL, ec='none'))
            ax.text(x + 4, y + 10.5, f'{n}', fontsize=7.6, fontweight='bold', color=INK, va='baseline')
            nh = kinds[(g, m, 'non-heart')]
            if nh:
                ax.add_patch(Circle((x + CW - 15, y + 8.2), 2.3, fc='none', ec=INK, lw=0.6))
                ax.text(x + CW - 11.5, y + 10.5, f'{nh}', fontsize=6.2, color=INK, va='baseline')
            for t, i in enumerate(picks[(g, m)]):
                cx = x + 4 + (CW - 8) * (t + .5) / 3
                draw_die(ax, DICE[i], cx, y + 13 + TH / 2, TH / 2 - 1.2)
                ax.text(cx, y + 13 + TH + 6, f"{DICE[i]['N']}", fontsize=5.2, color=MUTED, ha='center', va='baseline')
        assert rowtot == sum(v for (gg, _), v in cnt.items() if gg == g)
        ax.text(LW + CW * len(MS) + TW / 2, y + 10.5, f'{rowtot}', fontsize=7.6, fontweight='bold', color=INK, ha='center', va='baseline')
    yb = y0 + RH * len(rows); ax.plot([0, W], [yb, yb], color=RULE, lw=0.5)
    if last:
        ax.text(2, yb + 12, 'all (a + b)', fontsize=7.4, fontweight='bold', color=INK, va='baseline')
        for j, m in enumerate(MS): ax.text(LW + CW * (j + .5), yb + 12, f"{sum(cnt[(g, m)] for g in ROWS)}", fontsize=7.0, color=INK, ha='center', va='baseline')
        ax.text(LW + CW * len(MS) + TW / 2, yb + 12, f'{total}', fontsize=7.6, fontweight='bold', color=INK, ha='center', va='baseline')
        yk = yb + 32
        ax.text(0, yk, 'Each cell: the number of Aequi, and three of them (fewest, median and most faces) when there are more than three; faces under each die.',
                fontsize=6.0, color=INK, va='baseline')
        ax.text(0, yk + 10, 'Empty cell: no Aequus there.   Vacuus kind (under each group): heart = centrally symmetric; inherited heart = parallel faces, no centre.',
                fontsize=6.0, color=INK, va='baseline')
        ax.add_patch(Circle((3, yk + 17.8), 2.3, fc='none', ec=INK, lw=0.6))
        ax.text(8, yk + 20, f"k: k of the cell are non-heart (no two faces parallel; {sum(v for kk, v in kinds.items() if kk[2] == 'non-heart')} dice in all).",
                fontsize=6.0, color=INK, va='baseline')
        ax.text(0, yk + 34, 'Face colours (app):', fontsize=6.0, color=INK, va='baseline'); xs = 62
        for key, lab in [('C', 'cube'), ('O', 'octahedron'), ('T', 'tetrahedron'), ('D', 'dodecahedron'), ('I', 'icosahedron'),
                         ('RD', 'rhombic dodecahedron'), ('RT', 'rhombic triacontahedron')]:
            ax.add_patch(Rectangle((xs, yk + 28.5), 7, 7, fc=hexrgb(COL[key]), ec=EDGE, lw=0.3))
            ax.text(xs + 9.5, yk + 34, lab, fontsize=5.8, color=INK, va='baseline'); xs += 13 + 3.35 * len(lab) + 4
        ax.text(0, yk + 45, 'An orbit mixing two families takes the colour of its icosahedral family; a second orbit of one colour in a die is drawn paler.',
                fontsize=6.0, color=INK, va='baseline')
    ax.text(W, H - 4, 'DICTO', fontsize=6.4, color=MUTED, ha='right', va='baseline', fontweight='bold')
    fig.savefig(os.path.join(ROOT, 'figures', f'aequi-table-all-{tag}.svg')); pdf.savefig(fig); plt.close(fig)
    log.append(f'panel {tag}: {len(rows)} rows, {W:.0f} x {H:.0f} pt')
pdf.close()
os.makedirs(os.path.join(ROOT, 'figures', 'all'), exist_ok=True)
open(os.path.join(ROOT, 'figures', 'all', 'paper.html'), 'w').write(
    '<!doctype html><meta charset="utf-8"><style>body{margin:0}img{width:100%;display:block}</style>'
    '<figure style="margin:0"><img src="../aequi-table-all-a.svg" alt="panel a"></figure>'
    '<figure style="margin:0"><img src="../aequi-table-all-b.svg" alt="panel b"></figure>\n')
open(os.path.join(ROOT, 'data', 'all-checks.log'), 'w').write('\n'.join(log) + '\n')
print('\n'.join(log))
