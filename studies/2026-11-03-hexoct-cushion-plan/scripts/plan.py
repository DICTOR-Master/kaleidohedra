# Knitted HexOct cushion: plan numbers and figures (DICTO proposed the Knitted HexOct; spec studies/2026-11-02-knitted-hexoct).
# Usage: python plan.py <out dir>   -> <out>/figs/*.svg, <out>/data/numbers.json, <out>/data/check.out
# Units: mm. Geometry exact as in #83 part 1; knitting layout rounded to whole stitches/ridges and checked here.
import sys, os, json, math, itertools
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Rectangle, Arc
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'svg.fonttype': 'none'})
out = sys.argv[1]; os.makedirs(out + '/figs', exist_ok=True); os.makedirs(out + '/data', exist_ok=True)
log = open(out + '/data/check.out', 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); log.write(s + '\n')

# ---------- gauge and lattice ----------
S = R = 22.0                       # garter, DK mercerised cotton: stitches and ridges per 10 cm (square gauge; to be measured)
st, rg = 100 / S, 100 / R          # mm per stitch, mm per ridge
N, M = 8, 7                        # node spacing in stitches, node-row spacing in ridges
a = N * st; d = math.sqrt(2 / 3) * a; pitch_true = math.sqrt(3) / 2 * a; pitch = M * rg
t = 3.5                            # garter sheet thickness (estimate; measure)
W, H = 88, 88                      # sheet: 88 stitches x 88 ridges (176 rows)
P(f'a = {a:.2f} mm, d = {d:.2f} mm, row pitch ideal {pitch_true:.2f} mm, knitted {pitch:.2f} mm ({(pitch/pitch_true-1)*100:+.2f} %)')
P(f'link tilt {math.degrees(math.atan(math.sqrt(2))):.4f} deg; plan offset a/sqrt3 = {a/math.sqrt(3):.2f} mm')
depth = 2 * d + t
P(f'sheet {W*st:.1f} x {H*rg:.1f} mm; depth (3 sheets, mid-plane spacing d, plus one sheet thickness) {depth:.1f} mm')
P(f'free cord length between sheet faces a - 1.22 t = {a - 2*(t/2)/math.sin(math.atan(math.sqrt(2))):.1f} mm')

# node positions (stitch, ridge) per sheet; positions: A (0,0), B (+a/2, +1/3 row), C (0, +2/3 row) mod lattice
OFF = {'A': (0.0, 0.0), 'B': (N / 2, 1 / 3), 'C': (0.0, 2 / 3)}
def nodes(pos):
    ox, oy = OFF[pos]; L = []
    for j in range(-2, 16):
        for i in range(-2, 16):
            x = 4 + ox + N * i + (N / 2) * (j % 2); yrow = j + oy
            ridge_true = 4 + M * yrow; ridge = round(ridge_true)
            if 3 <= x <= W - 3 and 2 <= ridge <= H - 2:
                L.append(dict(i=i, j=j, st=x, ridge=ridge, ridge_true=ridge_true,
                              X=x * st, Y=(4 + pitch_true / rg * yrow) * rg))  # X,Y: ideal plan position (mm)
    return L
word = 'ABC'
NS = {p: nodes(p) for p in 'ABC'}
for p in 'ABC':
    rows = sorted(set(n['ridge'] for n in NS[p]))
    P(f'sheet {p}: {len(NS[p])} nodes, node rows at ridges {rows[:3]}... ({len(rows)} rows), true ridges {sorted(set(round(n["ridge_true"],2) for n in NS[p]))[:3]}')
gaps = []
for k in range(2):
    lo, up = NS[word[k]], NS[word[k + 1]]; Lk = []
    for u in lo:
        for v in up:
            if abs(math.hypot(v['X'] - u['X'], v['Y'] - u['Y']) - a / math.sqrt(3)) < 0.05 * a: Lk.append((u, v))
    gaps.append(Lk)
nl = [len(g) for g in gaps]; P(f'links per gap {nl}, total {sum(nl)}')
for k, g in enumerate(gaps):
    deg_lo = {}
    for u, v in g: deg_lo[(u['i'], u['j'])] = deg_lo.get((u['i'], u['j']), 0) + 1
    P(f'gap {k+1}: lower nodes with 3 links {sum(1 for x in deg_lo.values() if x==3)}, fewer {sum(1 for x in deg_lo.values() if x<3)}')
# 3D check of link length and tilt with true heights
for g, k in zip(gaps, range(2)):
    errs = [abs(math.sqrt((v['X']-u['X'])**2 + (v['Y']-u['Y'])**2 + d**2) - a) for u, v in g]
    P(f'gap {k+1}: max |link length - a| (ideal plan positions) {max(errs):.2e} mm')
# c check: at sheet B every link up is opposite a link down (straight through)
straight = 0; tot = 0
for (u, v) in gaps[1]:
    for (w, x) in gaps[0]:
        if (x['i'], x['j']) == (u['i'], u['j']):
            tot += 1
            if abs((v['X']-u['X']) + (x['X']-w['X'])) < 1e-6 and abs((v['Y']-u['Y']) + (x['Y']-w['Y'])) < 1e-6 and \
               abs((v['X']-u['X']) - (x['X']-w['X'])) > 1: pass
            if abs((v['X']-u['X']) - (x['X']-w['X'])) < 1e-6 and abs((v['Y']-u['Y']) - (x['Y']-w['Y'])) < 1e-6: straight += 1
P(f'sheet B is c: link pairs (down, up) through a B node that continue in one straight line: {straight} (each B node with both: 3)')

# cord pieces: per lower-first node a V (two arms to the next node row of the other sheet) and singles for the rest
def pieces(g):
    # group links by their first-knitted end (smaller ridge); a V = two links sharing that first end and the same second-row
    first = {}
    for u, v in g:
        A_, B_ = (u, v) if u['ridge_true'] < v['ridge_true'] else (v, u)
        key = (id(A_),); first.setdefault(key, []).append((A_, B_))
    V = sum(1 for L in first.values() if len(L) == 2); single = sum(1 for L in first.values() if len(L) == 1) \
        + sum(len(L) for L in first.values() if len(L) > 2)
    span = max(B_['ridge'] - A_['ridge'] for L in first.values() for A_, B_ in L)
    return V, single, span
cat = 0; pc = 0
for k, g in enumerate(gaps):
    V, s1, span = pieces(g); P(f'gap {k+1}: V pieces {V}, single pieces {s1}, links {2*V+s1}, catches {3*V+2*s1}, longest open span {span} ridges')
    cat += 3 * V + 2 * s1; pc += V + s1
P(f'cord pieces {pc}, catches {cat}')

# ---------- materials and time ----------
sheet_st = W * 2 * H; wall_st_per_gap = round(2 * (W * st + H * rg) / st) * round(d / (rg / 2))
yarn_m = (3 * sheet_st + 2 * wall_st_per_gap) * 0.01
cord_m = (sum(nl) * a + pc * 2 * 25) / 1000 * 1.1
vol_l = (W * st) * (H * rg) * 2 * d / 1e6
P(f'stitches: sheets 3 x {sheet_st}, side walls 2 x {wall_st_per_gap}; yarn at 1 cm/stitch {yarn_m:.0f} m')
P(f'link cord {cord_m:.0f} m (links x a + 2 x 25 mm per piece for catch and knot, +10 %); fill volume {vol_l:.1f} L')
for p_kpa in (1, 6):
    per_node = p_kpa * 1e3 * (math.sqrt(3) / 2 * (a / 1000) ** 2)
    P(f'pressure {p_kpa} kPa: {per_node:.2f} N per node area; if links alone held it: {per_node/3/math.cos(math.atan(1/math.sqrt(2))):.2f} N per link')
mins_knit = (3 * sheet_st + 2 * wall_st_per_gap) / 25; mins_cat = cat * 0.5 + pc * 0.5
P(f'time: knitting at 25 st/min {mins_knit/60:.0f} h (+25 % for working three needles in step {mins_knit*1.25/60:.0f} h); '
  f'cord work at 30 s per catch and 30 s per piece {mins_cat/60:.0f} h')
mech = {}
for lab in ('c', 'h', 'cc', 'hh'):
    for v in ('links', 'full'):
        f = os.path.join(os.path.dirname(__file__), '..', 'data', f'out_{lab}_{v}.json')
        if os.path.exists(f):
            D = json.load(open(f)); mech[f'{lab}_{v}'] = {k: D[k] * 1e3 for k in ('C33_bonded', 'E3_free', 'G13_bonded', 'G13_free')}
for k, v in mech.items(): P('mech', k, {q: round(x, 4) for q, x in v.items()})
if mech:
    P(f'3 sheets, links only, rigid joints: free shear h/c = {mech["h_links"]["G13_free"]/mech["c_links"]["G13_free"]:.1f}; '
      f'4 sheets hh/cc = {mech["hh_links"]["G13_free"]/mech["cc_links"]["G13_free"]:.1f}; sheets as stiff as links (3): '
      f'{mech["h_full"]["G13_free"]/mech["c_full"]["G13_free"]:.3f}')
json.dump(dict(a=a, d=d, depth=depth, pitch=pitch, pitch_true=pitch_true, nodes={p: len(NS[p]) for p in 'ABC'}, links=nl,
               pieces=pc, catches=cat, yarn_m=yarn_m, cord_m=cord_m, fill_l=vol_l, mech=mech), open(out + '/data/numbers.json', 'w'), indent=1)

# ---------- figures ----------
COL = {'A': '#3b6ea8', 'B': '#c08a1e', 'C': '#a8433b'}
z_of = {p: t / 2 + k * d for k, p in enumerate(word)}

def save(fig, name):
    fig.savefig(out + f'/figs/{name}.svg')
    if len(sys.argv) > 2: fig.savefig(sys.argv[2] + f'/{name}.png', dpi=170)  # check renders (scratch only)

# Fig 1: finished cushion and cut-away (projection u = (x - y) cos30, v = (x + y) sin30 + z)
def pr(x, y, z): return ((x - y) * 0.866, (x + y) * 0.5 + z * 1.0)
Wm, Hm, Z = W * st, H * rg, depth + 4
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.3))
for ax, cut in zip(axs, (False, True)):
    ax.set_aspect('equal'); ax.axis('off')
    def poly(pts, fc, ec='#555', lw=0.6, alpha=1, z=1):
        ax.add_patch(Polygon([pr(*p) for p in pts], closed=True, fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z))
    q = 200.0 if cut else 0
    top = '#efe6d2'; side = '#d9ccae'; side2 = '#c9bb98'
    if not cut:
        poly([(0, 0, 0), (Wm, 0, 0), (Wm, 0, Z), (0, 0, Z)], side)
        poly([(0, 0, 0), (0, Hm, 0), (0, Hm, Z), (0, 0, Z)], side2)
        poly([(0, 0, Z), (Wm, 0, Z), (Wm, Hm, Z), (0, Hm, Z)], top)
    else:
        poly([(q, 0, 0), (Wm, 0, 0), (Wm, 0, Z), (q, 0, Z)], side)
        poly([(0, q, 0), (0, Hm, 0), (0, Hm, Z), (0, q, Z)], side2)
        poly([(q, 0, 0), (q, q, 0), (q, q, Z), (q, 0, Z)], side2, z=1)
        poly([(0, q, 0), (q, q, 0), (q, q, Z), (0, q, Z)], side, z=1)
        poly([(q, 0, Z), (Wm, 0, Z), (Wm, Hm, Z), (0, Hm, Z), (0, q, Z), (q, q, Z)], top, z=1)
        # sheet lines on the cut faces
        for p in word:
            zz = z_of[p] + 2
            for (x0, y0, x1, y1) in ((q, 0, q, q), (0, q, q, q)):
                ax.plot(*zip(pr(x0, y0, zz), pr(x1, y1, zz)), color=COL[p], lw=1.6, zorder=2)
        # inside the removed quarter: sheets, nodes and links, bottom to top
        inq = lambda n: n['X'] < q and n['Y'] < q
        for k, p in enumerate(word):
            zz = z_of[p] + 2
            poly([(0, 0, zz), (q, 0, zz), (q, q, zz), (0, q, zz)], COL[p], ec=COL[p], lw=0.8, alpha=0.16, z=3 + 3 * k)
            xs = [pr(n['X'], n['Y'], zz) for n in NS[p] if inq(n)]
            ax.scatter([u for u, v in xs], [v for u, v in xs], s=5, color=COL[p], zorder=4 + 3 * k)
            if k < 2:
                for u, v in gaps[k]:
                    if inq(u) and inq(v):
                        ax.plot(*zip(pr(u['X'], u['Y'], zz), pr(v['X'], v['Y'], z_of[word[k + 1]] + 2)), color='#333', lw=0.6, zorder=5 + 3 * k)
    # dimples of the top sheet (C nodes) and a cover seam
    for n in NS['C']:
        if cut and n['X'] < q and n['Y'] < q: continue
        u, v = pr(n['X'], n['Y'], Z); ax.add_patch(plt.Circle((u, v), 1.6, color='#8a7a55', zorder=20))
    ax.set_xlim(-Hm * 0.9, Wm * 0.9); ax.set_ylim(-5, Z + Hm + 5)
    ax.set_title(('(b) cut-away: the front quarter removed' if cut else '(a) the finished cushion, 40 × 40 cm, about 6.5 cm deep'), fontsize=8)
axs[1].text(*pr(5, -40, 0), 'sheet A (bottom)', color=COL['A'], fontsize=7)
axs[1].text(*pr(5, -40, 26), 'sheet B (middle, c)', color=COL['B'], fontsize=7)
axs[1].text(*pr(5, -40, 52), 'sheet C (top)', color=COL['C'], fontsize=7)
fig.tight_layout(); save(fig, 'cushion'); plt.close(fig)

# Fig 2: section seen along a row of nodes, true scale, near one edge (with side wall and fill)
fig, ax = plt.subplots(figsize=(7.2, 2.5)); ax.set_aspect('equal'); ax.axis('off')
y0, y1 = -6, 5.2 * pitch_true
ax.add_patch(Rectangle((y0, z_of['A']), y1 - y0, z_of['C'] - z_of['A'], fc='#f3eedf', ec='none', zorder=0))
for p in word:
    ax.add_patch(Rectangle((y0, z_of[p] - t / 2), y1 - y0, t, fc=COL[p], alpha=0.35, ec='none', zorder=1))
    ax.text(y1 + 3, z_of[p], f'sheet {p}' + (' (c)' if p == 'B' else ''), va='center', color=COL[p], fontsize=7.5)
# side wall at y0
ax.add_patch(Rectangle((y0 - t, z_of['A'] - t / 2), t, z_of['C'] - z_of['A'] + t, fc='#888', alpha=0.5, ec='none'))
ax.text(y0 - t - 2, z_of['B'], 'side wall\n(picked up,\nknitted)', ha='right', va='center', fontsize=6.5)
def row_y(p, j): return j * pitch_true + OFF[p][1] * pitch_true
for k, p in enumerate(word):
    for j in range(0, 6):
        yy = row_y(p, j)
        if y0 < yy < y1: ax.plot(yy, z_of[p], 'o', ms=3, color=COL[p], zorder=5)
    if k < 2:
        q2 = word[k + 1]
        for j in range(-1, 7):
            ya = row_y(p, j)
            # forward step: pair of links to +1/3 row (thick, front and back), single link to -2/3 row (thin)
            for dy, lw in ((pitch_true / 3, 2.0), (-2 * pitch_true / 3, 0.8)):
                yb = ya + dy
                if y0 <= min(ya, yb) and max(ya, yb) <= y1: ax.plot([ya, yb], [z_of[p], z_of[q2]], color='#333', lw=lw, zorder=3)
# straight-through trace at the c sheet
jt = 2; ya = row_y('A', jt); yb = ya + pitch_true / 3; yc = yb + pitch_true / 3
ax.plot([ya, yc], [z_of['A'], z_of['C']], color='#000', lw=2.6, zorder=4, alpha=0.6)
ax.annotate('straight on through the c sheet', (yb, z_of['B']), (yb + 22, z_of['B'] + 8), fontsize=6.5, arrowprops=dict(arrowstyle='-', lw=0.5))
# fill dots
rng = np.random.default_rng(1)
for _ in range(220):
    yy = rng.uniform(y0, y1); zz = rng.uniform(z_of['A'] + t, z_of['C'] - t)
    if abs(zz - z_of['B']) > t: ax.plot(yy, zz, '.', ms=1.2, color='#b5a172', zorder=0.5)
# dimensions
yd = y1 - 8
ax.annotate('', (yd, z_of['A']), (yd, z_of['B']), arrowprops=dict(arrowstyle='<->', lw=0.6))
ax.text(yd + 1.5, (z_of['A'] + z_of['B']) / 2, f'd = {d:.1f} mm', fontsize=6.5, va='center')
ya = row_y('A', 4); yb = ya - 2 * pitch_true / 3
ax.add_patch(Arc((ya, z_of['A']), 16, 16, theta1=180 - 54.74, theta2=180, lw=0.6))
ax.text(ya - 14, z_of['A'] + 2.2, '54.74°', fontsize=6.5, ha='right')
ax.text((ya + yb) / 2 + 2, (z_of['A'] + z_of['B']) / 2 - 3, f'a = {a:.1f} mm', fontsize=6.5, rotation=-50)
ax.set_xlim(y0 - 32, y1 + 30); ax.set_ylim(-6, z_of['C'] + 8)
fig.tight_layout(); save(fig, 'section'); plt.close(fig)

# Fig 3: in-step knitting (schematic side view) and the node catch
fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.7), gridspec_kw=dict(width_ratios=[1.5, 1]))
ax = axs[0]; ax.axis('off')
# side view along a column of the work: x = ridges knitted, sheets on three needles at the live edge (right)
zs = {'A': 0, 'B': 6, 'C': 12}; xe = 30
first = {'A': 4, 'B': 6, 'C': 2}
for p in word:
    ax.add_patch(Rectangle((0, zs[p] - 0.45), xe, 0.9, fc=COL[p], alpha=0.45, ec='none'))
    ax.plot([xe, xe + 2.5], [zs[p], zs[p] + 1.2], color='#444', lw=2.4, solid_capstyle='round')
    ax.text(xe + 3.2, zs[p] + 1.2, f'needle {"ABC".index(p)+1}: sheet {p}', fontsize=6.5, va='center', color=COL[p])
    for x in range(first[p], xe, M):
        ax.plot(x, zs[p], 'o', ms=3.2, color=COL[p], zorder=5)
def sag(x0, z0, x1, z1, lw=0.9, ls='-'):
    tt = np.linspace(0, 1, 30); xm, zm = (x0 + x1) / 2 + 2.2, (z0 + z1) / 2
    xx = (1 - tt) ** 2 * x0 + 2 * (1 - tt) * tt * xm + tt ** 2 * x1; zz = (1 - tt) ** 2 * z0 + 2 * (1 - tt) * tt * zm + tt ** 2 * z1
    ax.plot(xx, zz, color='#222', lw=lw, ls=ls, zorder=4)
for x in range(4, xe - 2, M): sag(x, 0, x + 2, 6, 1.3)            # gap 1 V (two arms, drawn as one thick line)
for x in range(6, xe - 2, M): sag(x, 6, x + 5, 0, 0.7, '--')      # gap 1 single, B row to the next A row
for x in range(6, xe - 3, M): sag(x, 6, x + 3, 12, 1.3)           # gap 2 V
for x in range(2, xe - 4, M): sag(x, 12, x + 4, 6, 0.7, '--')     # gap 2 single, C row to the next B row
ax.text(15, -3.3, 'ridges knitted (all three sheets move on together, one ridge at a time)', ha='center', fontsize=6.3)
ax.text(0, 15.6, 'thick: a V (one cord, middle caught first, two arms of length a)   dashed: a single link', fontsize=6.3)
ax.set_xlim(-1, 46); ax.set_ylim(-5, 17); ax.set_aspect(1.0)
ax = axs[1]; ax.set_aspect('equal'); ax.axis('off')
# the catch: knit the node stitch with yarn and cord held together; arm measured on a card gauge
for i in range(5):
    for j in range(3):
        ax.add_patch(matplotlib.patches.Ellipse((i * 4, j * 3), 3.2, 2.6, fill=False, lw=0.7, ec='#666'))
ax.add_patch(matplotlib.patches.Ellipse((8, 3), 3.2, 2.6, fill=False, lw=1.6, ec=COL['A']))
ax.plot([6.2, 8, 9.8], [2.4, 3.6, 2.4], color='#222', lw=1.4)
ax.plot([9.8, 15, 18], [2.4, 9, 13], color='#222', lw=1.0); ax.plot([6.2, 2, -1], [2.4, 9, 13], color='#222', lw=1.0)
ax.add_patch(Rectangle((15.6, 4.5), 1.6, 9.5, angle=0, fc='#e8dcc0', ec='#8a7a55', lw=0.6))
ax.text(17.8, 6.0, 'card gauge:\none arm = a\nbetween catches', fontsize=6)
ax.text(8, -5.2, 'node stitch knitted with\nyarn + link cord held together', ha='center', fontsize=6)
ax.set_xlim(-4, 30); ax.set_ylim(-8, 15)
fig.tight_layout(); save(fig, 'instep'); plt.close(fig)

# Fig 4: press and shear test
fig, ax = plt.subplots(figsize=(7.2, 1.7)); ax.set_aspect('equal'); ax.axis('off')
for x0, lab in ((0, 'press: 5 kg bag on a board,\nread the sink on a ruler'), (110, 'shear: same load, pull the board sideways\nwith a luggage scale; read the shift per newton')):
    ax.add_patch(Rectangle((x0, 0), 60, 9, fc='#efe6d2', ec='#555', lw=0.6))
    ax.add_patch(Rectangle((x0 + 10, 9), 40, 1.5, fc='#b9a77d', ec='#555', lw=0.6))
    ax.add_patch(Rectangle((x0 + 22, 10.5), 16, 7, fc='#ddd', ec='#555', lw=0.6))
    ax.plot([x0 + 66, x0 + 66], [0, 16], color='#333', lw=0.8)
    for k in range(0, 17, 2): ax.plot([x0 + 65, x0 + 67], [k, k], color='#333', lw=0.4)
    ax.text(x0 + 30, -6, lab, ha='center', fontsize=6.5)
ax.annotate('', (110 + 50 + 14, 9.75), (110 + 50, 9.75), arrowprops=dict(arrowstyle='->', lw=0.8))
ax.set_xlim(-5, 190); ax.set_ylim(-11, 19)
fig.tight_layout(); save(fig, 'test'); plt.close(fig)
P('figures written')
