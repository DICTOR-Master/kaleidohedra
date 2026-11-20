# DICTO · dictospheres.com — the rendered scenes of Figures 1 to 5 (renders/<fig>.html, one scene per shot) with their labels
# and 2D sections (renders/<fig>.json), and the checks of every drawn geometry (data/fig-scenes.json).
#   Figures 1, 2, 3: one space-time Poisson–Voronoi complex (stc.py): a scutoid between two planes, a block of the moving
#   tiling, and the three kinds of corner (birth, swap, death). Figure 4: the 120-cell cell of fig_tube.py (data/fig-tube.json).
#   Figure 5: a Poisson–Voronoi block and a bcc block (truncated octahedra) in space.
#   Version 2 (20 Nov): in Figures 3 and 4 the cells round the corner and the 120-cell cell are drawn solid with their front walls
#   cut away (back_faces), so every face hides what lies behind it; no see-through faces.
# Space-time (x, y, t) is drawn with t upward: three.js coordinates (x, v t, −y), a rotation after the stretch t -> v t, which
# maps convex cells to convex cells and corners to corners (the Speed paragraph of Section 2).
# Usage: python3 fig_scenes.py      (run on a compute host; then node shots.mjs renders/<fig>.html renders/<fig>; fig_compose.py)
import json, os, sys
import numpy as np
from stc import Complex, Poly
from render3d import poly_part, write, project, basis, PX

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'renders'); os.makedirs(OUT, exist_ok=True)
DATA = os.path.join(HERE, '..', 'data')
CHECKS = []


def check(name, ok, info=''):
    CHECKS.append([name, bool(ok), str(info)]); print(('PASS ' if ok else 'FAIL ') + name + ' ' + str(info), flush=True)


# colours: labels only (said in the captions); neutral warm tones, no solid's app colour except the 120-cell's dodecahedron
CREAM, TAUPE, AMBER = '#d2c3a0', '#7c6d5a', '#c99a45'          # the pair that meets at a swap / the pair that parts / their walls
EV = {'birth': '#f2ead8', 'swap': AMBER, 'death': '#76869c', 'neighbour': '#4a4239'}
TONES = ['#a8967a', '#958468', '#b5a385', '#8a7a62', '#bfae8f', '#9c8b6f', '#ad9c7f']
CUTF = '#c4b594'
BORN, DIES = '#d6c69e', '#6c7d93'                           # a cell born / dying: solid in Figures 2 and 3                                               # faces of the cut (the box)
EDGE = '#2b261e'


def W(P, v):
    """space-time (x, y, t) -> drawing (x, v t, -y)."""
    P = np.atleast_2d(P); return np.c_[P[:, 0], v * P[:, 2], -P[:, 1]]


def framing(Ps, dirv, frac=0.9, E=1.0):
    """offset and scale that centre all points Ps (drawing coordinates) and fill frac of the frame half-width E."""
    P = np.vstack(Ps); x, y, _ = basis(dirv); Q = np.c_[P @ x, P @ y]; c = (Q.max(0) + Q.min(0)) / 2
    off = c[0] * x + c[1] * y; s = frac * E / np.abs(Q - c).max()
    return lambda R: (np.atleast_2d(R) - off) * s


def back_faces(Q, F, d):
    """the faces of a convex cell (corners Q, faces F) whose outward normal points away from the eye on the side d: the cell
    with its front walls cut away (20 Nov, Version 2: drawn solid, so every face hides what lies behind it)."""
    Q = np.asarray(Q, float); c = Q.mean(0); keep = []
    for o in F:
        P = Q[list(o)]; n = np.cross(P[1] - P[0], P[2] - P[0]); n = n if n @ (P.mean(0) - c) > 0 else -n
        if n @ np.asarray(d, float) <= 0: keep.append(o)
    return keep


def wall_face(poly, n):
    """index of the face of poly whose outward normal is n (unit)."""
    k = [i for i, (m, d) in enumerate(poly.planes) if m @ n > 1 - 1e-9]
    return k[0] if k else None


rng = np.random.default_rng(20261120)
L, H = 7.0, 7.0
seeds = rng.uniform([-2, -2, -2], [L + 2, L + 2, H + 2], size=(rng.poisson((L + 4) ** 2 * (H + 4)), 3))
X = Complex(seeds)
inner = lambda p, m=0.0: (p[0] > m and p[0] < L - m and p[1] > m and p[1] < L - m and p[2] > m and p[2] < H - m)
corner = {}
for k in range(len(X.CC)):
    if inner(X.CC[k], 0.5):
        c = X.corner(k)
        if c: corner[k] = c
idx = [c[0] for c in corner.values()]
check('space-time complex: every inner corner has index 1, 2 or 3', set(idx) <= {1, 2, 3}, {i: idx.count(i) for i in range(5)})


def cell_t(i):
    ks = X.corners_of(i); return ks, X.CC[ks][:, 2]


# ================================================================ Figure 1: a scutoid between two planes
area = lambda P: 0.5 * abs((P[:, 0] * np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1) * P[:, 1]).sum())
best = None
for k, (i, ev) in corner.items():
    if ev[0] != 'swap' or not inner(X.CC[k], 1.5): continue
    p = X.CC[k]; gaps = []
    for j in ev[1]['after']:                                # no other corner of either meeting cell between the planes
        ks, ts = cell_t(j)
        if any(X.corner(q) is None for q in ks): gaps = None; break
        gaps.append(min(p[2] - ts[ts < p[2] - 1e-12].max(), ts[ts > p[2] + 1e-12].min() - p[2]))
    if not gaps: continue
    g = min(gaps); t0, t1 = p[2] - 0.8 * g, p[2] + 0.8 * g
    for j in ev[1]['after']:
        C = X.cell(j); s0, s1 = C.section(t0), C.section(t1)
        if s0 is None or s1 is None: continue
        w = np.ptp(s1, 0).mean(); o_ = [x for x in ev[1]['after'] if x != j][0]
        Pc = X.cell(j, ([-1e3, -1e3, t0], [1e3, 1e3, t1])); f_ = wall_face(Pc, (X.S[o_] - X.S[j]) / np.linalg.norm(X.S[o_] - X.S[j]))
        if f_ is None: continue
        tp = [Pc.V[v] for v in Pc.faces[f_] if abs(Pc.V[v][2] - t1) < 1e-9]
        if len(tp) != 2: continue
        wt = np.linalg.norm(tp[0] - tp[1]) / w                       # the gained wall's width at the top, against the cell's
        if wt < 0.2: continue
        a0 = area(s1); secs4 = [X.cell(x).section(tt) for x in X.D.simplices[k] for tt in (t0, t1)]
        if any(x is None for x in secs4) or min(area(x) for x in secs4) < 0.25 * a0: continue     # four cells of good size
        c1, d1 = ev[1]['before']; Pd = X.cell(c1, ([-1e3, -1e3, t0], [1e3, 1e3, t1]))
        fd = wall_face(Pd, (X.S[d1] - X.S[c1]) / np.linalg.norm(X.S[d1] - X.S[c1]))
        if fd is None: continue
        bp = [Pd.V[v] for v in Pd.faces[fd] if abs(Pd.V[v][2] - t0) < 1e-9]
        if len(bp) != 2 or np.linalg.norm(bp[0] - bp[1]) / w < 0.2: continue     # the parting pair's contact, wide at the bottom
        sc = g / w + wt + (0.6 if (len(s0), len(s1)) == (5, 6) else 0)
        if best is None or sc > best[0]: best = (sc, k, j, t0, t1)
_, kA, jA, t0, t1 = best
pA = X.CC[kA]; evA = corner[kA][1][1]; a_, b_ = jA, [q for q in evA['after'] if q != jA][0]; c_, d_ = evA['before']
BIG = 1e3
slab = lambda lo_xy=(-BIG, -BIG), hi_xy=(BIG, BIG): ([lo_xy[0], lo_xy[1], t0], [hi_xy[0], hi_xy[1], t1])
four = {q: X.cell(q, slab()) for q in (a_, b_, c_, d_)}
sc_ = four[a_]
n_ab = (X.S[b_] - X.S[a_]) / np.linalg.norm(X.S[b_] - X.S[a_]); n_cd = (X.S[d_] - X.S[c_]) / np.linalg.norm(X.S[d_] - X.S[c_])
fa = wall_face(sc_, n_ab)
bot = [k for k, (m, dd) in enumerate(sc_.planes) if m[2] < -1 + 1e-9][0]; top = [k for k, (m, dd) in enumerate(sc_.planes) if m[2] > 1 - 1e-9][0]
nb, nt = len(sc_.faces[bot]), len(sc_.faces[top])
mid = [v for v in range(len(sc_.V)) if t0 + 1e-9 < sc_.V[v][2] < t1 - 1e-9]
check('Figure 1: the scutoid has %d sides at the bottom and %d at the top' % (nb, nt), nt == nb + 1, (nb, nt))
check('Figure 1: the scutoid has one corner between the planes, the swap corner', len(mid) == 1 and np.linalg.norm(sc_.V[mid[0]] - pA) < 1e-9)
tri = sc_.faces[fa]
check('Figure 1: the wall it gains at the swap is a triangle from the corner to the top plane',
      len(tri) == 3 and sum(abs(sc_.V[v][2] - t1) < 1e-9 for v in tri) == 2 and mid[0] in tri)
fcd = wall_face(four[c_], n_cd); tri2 = four[c_].faces[fcd]
check('Figure 1: the wall the other pair loses is a triangle from the bottom plane to the corner',
      len(tri2) == 3 and sum(abs(four[c_].V[v][2] - t0) < 1e-9 for v in tri2) == 2)
check('Figure 1: the scutoid is convex (Euler and every corner inside every face plane)', sc_.convex_ok())
# the two slices: every cell within a window round the scutoid
cA = sc_.V[[v for v in range(len(sc_.V)) if abs(sc_.V[v][2] - t1) < 1e-9]].mean(0)
RW = 1.9 * np.abs(sc_.V[:, :2] - cA[:2]).max()
win = ([cA[0] - RW, cA[1] - RW, -BIG], [cA[0] + RW, cA[1] + RW, BIG])
near = set()
for q in (a_, b_, c_, d_):
    near |= set(X.nb[q])
    for r in X.nb[q]: near |= set(X.nb[r])
slices = {'bottom': [], 'top': []}
for q in sorted(near):
    Pq = X.cell(q, win)
    if Pq is None: continue
    for nm, tt in (('bottom', t0), ('top', t1)):
        s = Pq.section(tt)
        if s is not None:
            slices[nm].append({'cell': int(q), 'role': 'scutoid' if q == a_ else 'meet' if q == b_ else 'part' if q in (c_, d_) else 'other',
                               'poly': ((s - cA[:2]) / RW).round(6).tolist()})


def touch(sl, q1, q2):
    """two section polygons share an edge of positive length"""
    P1 = [np.array(s['poly']) for s in sl if s['cell'] == q1][0]; P2 = [np.array(s['poly']) for s in sl if s['cell'] == q2][0]
    sh = [p for p in P1 if np.min(np.linalg.norm(P2 - p, axis=1)) < 1e-6]
    return len(sh) >= 2 and max(np.linalg.norm(a - b) for a in sh for b in sh) > 1e-4


check('Figure 1: bottom slice: the parting pair touches, the meeting pair does not', touch(slices['bottom'], c_, d_) and not touch(slices['bottom'], a_, b_))
check('Figure 1: top slice: the meeting pair touches, the parting pair does not', touch(slices['top'], a_, b_) and not touch(slices['top'], c_, d_))
for nm in ('bottom', 'top'):
    tot = sum(area(np.array(s['poly'])) for s in slices[nm])
    check('Figure 1: the %s slice tiles its window (areas sum to 4)' % nm, abs(tot - 4) < 1e-6, tot)
gw = np.ptp(sc_.V[:, :2], 0).mean(); vA = 1.7 * gw / (t1 - t0)
nt3 = W(sc_.planes[fa][0], 1.0)[0]; hz = np.array([nt3[0], 0, nt3[2]]); hz /= np.linalg.norm(hz)
rot = lambda u, a: np.array([u[0] * np.cos(a) + u[2] * np.sin(a), u[1], -u[0] * np.sin(a) + u[2] * np.cos(a)])
DIR1 = rot(hz, np.radians(32)) + [0, 0.42, 0]                   # facing the gained wall, a little from the side and above
# scene 1: the scutoid
P1 = W(sc_.V - [cA[0], cA[1], (t0 + t1) / 2], vA)
fr = framing([P1], DIR1, 0.84)
cols = [AMBER if k == fa else (CUTF if k in (bot, top) else CREAM) for k in range(len(sc_.faces))]
scene1 = {'E': 1.0, 'dir': DIR1.tolist(), 'parts': [poly_part(fr(P1), sc_.faces, cols, rad=0.0045, balls=[(mid[0], AMBER, 4.0)])]}
lab1 = {'top': project(fr(P1[[v for v in sc_.faces[top]]]).mean(0), DIR1, 1.0)[0].tolist(),
        'bottom': project(fr(P1[[v for v in sc_.faces[bot]]]).mean(0), DIR1, 1.0)[0].tolist(),
        'tri': project(fr(P1[tri]).mean(0), DIR1, 1.0)[0].tolist(), 'corner': project(fr(P1[mid[0]]), DIR1, 1.0)[0].tolist()}
write(os.path.join(OUT, 'scutoid.html'), [scene1])
json.dump({'labels': lab1, 'slices': slices, 'sides': [nb, nt]}, open(os.path.join(OUT, 'scutoid.json'), 'w'))
FIG = {'fig1': {'bottom_sides': nb, 'top_sides': nt}}

# ================================================================ Figure 3: birth, swap, death at a corner
def local(k):
    p = X.CC[k]; sd = [int(q) for q in X.D.simplices[k]]
    others = set()
    for q in sd: others |= set(X.corners_of(q))
    others.discard(k); r = 0.62 * min(np.abs(X.CC[o] - p).max() for o in others)
    nbr = X.D.neighbors[k]; dirs = X.CC[nbr] - p; dirs /= np.linalg.norm(dirs, axis=1)[:, None]
    return p, sd, r, np.abs(dirs[:, 2]).min()


from scipy.spatial import ConvexHull


def try_corner(k, kind, r):
    """the four cells of corner k in the box p ± r and their sections just before and after; the list of checks."""
    p = X.CC[k]; sd = [int(q) for q in X.D.simplices[k]]; ev = corner[k][1][1]; box = (p - r, p + r)
    pcs = {q: X.cell(q, box) for q in sd}
    if any(P is None for P in pcs.values()): return None
    ck = []
    for q in sd:
        P = pcs[q]; pk = [v for v in range(len(P.V)) if np.linalg.norm(P.V[v] - p) < 1e-9]
        inside = [v for v in range(len(P.V)) if (np.abs(P.V[v] - p) < r - 1e-9).all()]
        ck.append(('the corner is the one corner of each of its four cells inside the box', len(pk) == 1 and inside == pk))
    vol = sum(ConvexHull(P.V).volume for P in pcs.values())
    ck.append(('the four cells fill the box (volumes sum to its volume)', abs(vol - (2 * r) ** 3) < 1e-9 * (2 * r) ** 3))
    secs = {}
    for nm, tt in (('before', p[2] - 0.45 * r), ('after', p[2] + 0.45 * r)):
        secs[nm] = []
        for q in sd:
            sct = pcs[q].section(tt)
            if sct is not None: secs[nm].append({'cell': q, 'poly': ((sct - p[:2]) / r).round(6).tolist()})
        tot = sum(area(np.array(x['poly'])) for x in secs[nm])
        ck.append(('the section %s fills its square' % nm, abs(tot - 4) < 1e-6))
    nbf, naf = len(secs['before']), len(secs['after'])
    if kind == 'birth':
        newp = [x for x in secs['after'] if x['cell'] == ev[0]]
        ck.append(('3 cells before, 4 after, the new one a triangle', nbf == 3 and naf == 4 and len(newp) == 1 and len(newp[0]['poly']) == 3))
    if kind == 'death':
        oldp = [x for x in secs['before'] if x['cell'] == ev[0]]
        ck.append(('4 cells before, the dying one a triangle, 3 after', nbf == 4 and naf == 3 and len(oldp) == 1 and len(oldp[0]['poly']) == 3))
    if kind == 'swap':
        b4, af = ev['before'], ev['after']
        ck.append(('4 cells before and after', nbf == 4 and naf == 4))
        if nbf == 4 and naf == 4:
            ck.append(('before, the parting pair touches and the meeting pair does not', touch(secs['before'], *b4) and not touch(secs['before'], *af)))
            ck.append(('after, the meeting pair touches and the parting pair does not', touch(secs['after'], *af) and not touch(secs['after'], *b4)))
    return p, sd, ev, pcs, secs, ck


sc3, lab3, FIG['fig3'] = [], [], {}
DIR3 = np.array([0.58, 0.40, 0.71]); v3 = 1.0
for kind in ('birth', 'swap', 'death'):
    def spread(k):                                          # the smallest angle between two edges at the corner (wide walls read best)
        d_ = X.CC[X.D.neighbors[k]] - X.CC[k]; d_ /= np.linalg.norm(d_, axis=1)[:, None]
        return min(np.arccos(np.clip(d_[i] @ d_[j], -1, 1)) for i in range(4) for j in range(i + 1, 4))
    cand = sorted([(local(k), k) for k, (i, ev) in corner.items() if ev[0] == kind and inner(X.CC[k], 1.5)],
                  key=lambda c: -c[0][2] * min(c[0][3], 0.45) * min(spread(c[1]), 0.9))
    got = None
    for (p, sd, r, slope), k in cand[:40]:
        for f in (1.0, 0.8, 0.65, 0.5):
            res = try_corner(k, kind, r * f)
            if res and all(c[1] for c in res[-1]): got = (res, r * f, k); break
        if got: break
    (p, sd, ev, pcs, secs, ck), r, k = got
    for nm, okk in ck: check('Figure 3 %s: %s' % (kind, nm), okk)
    role = {}
    for q in sd:
        if kind == 'swap': role[q] = CREAM if q in ev['after'] else TAUPE
        else: role[q] = (BORN if kind == 'birth' else DIES) if q == ev[0] else TONES[sd.index(q) + 1]
    for nm in secs:
        for x in secs[nm]: x['col'] = role[x['cell']]
    parts, allP = [], []
    for q in sd:
        Pq = pcs[q]; Q = W(Pq.V - p, v3); pk = [v for v in range(len(Pq.V)) if np.linalg.norm(Pq.V[v] - p) < 1e-9][0]
        allP.append(Q)
        if kind != 'swap' and q == ev[0]:                   # the cell born or dying: solid
            parts.append(('solid', Q, Pq.faces, role[q], pk))
        else:
            parts.append(('glass', Q, Pq.faces, role[q], pk))
        if kind == 'swap':                                  # the wall of each pair: solid, amber above the corner, taupe below
            o = [x for x in sd if x != q and ((q in ev['after']) == (x in ev['after']))][0]
            if q < o:
                n = (X.S[o] - X.S[q]) / np.linalg.norm(X.S[o] - X.S[q]); fw = wall_face(Pq, n)
                parts.append(('solid', Q, [Pq.faces[fw]], AMBER if q in ev['after'] else TAUPE, pk))
    dv = DIR3
    if kind == 'swap':                                      # face the two walls
        a1, b1 = ev['after']; c1, d1 = ev['before']
        n1 = W(X.S[b1] - X.S[a1], 1.0)[0]; n2 = W(X.S[d1] - X.S[c1], 1.0)[0]
        n1 /= np.linalg.norm(n1); n2 /= np.linalg.norm(n2); n2 = n2 if n1 @ n2 > 0 else -n2
        hz = n1 + n2; hz[1] = 0; hz /= np.linalg.norm(hz); dv = rot(hz, np.radians(28)) + [0, 0.36, 0]
    fr3 = framing(allP, dv, 0.86)
    sc3.append({'E': 1.0, 'dir': list(map(float, dv)), 'parts':
                [poly_part(fr3(Q), F if m == 'solid' else back_faces(Q, F, dv), c, edge_col=EDGE if m == 'solid' else '#cfc4ae', rad=0.0035,
                           edges=None if m == 'solid' else sorted({tuple(sorted((int(a), int(b)))) for o in F for a, b in zip(o, list(o[1:]) + [o[0]])}),
                           balls=[(pk, EV[kind], 6.5)] if m == 'solid' or kind == 'swap' else []) for m, Q, F, c, pk in parts]})
    lab3.append({'kind': kind, 'index': int(corner[k][0]), 'secs': secs})
write(os.path.join(OUT, 'corners.html'), sc3); json.dump(lab3, open(os.path.join(OUT, 'corners.json'), 'w'))

# ================================================================ Figure 2: a block of the moving tiling in space-time
LB, HB = 3.4, 2.4; o = np.array([1.8, 1.8, 2.3]); vB = 2.5
blo, bhi = o, o + [LB, LB, HB]
inb = lambda P: (P > blo + 1e-12).all() and (P < bhi - 1e-12).all()
cells = {}
for q in range(len(X.S)):
    if np.abs(X.S[q] - (blo + bhi) / 2).max() > max(LB, HB) / 2 + 2.5: continue
    Pq = X.cell(q, (blo, bhi))
    if Pq is not None: cells[q] = Pq
cks = [k for k in range(len(X.CC)) if inb(X.CC[k])]
evs = {k: X.corner(k) for k in cks}
check('Figure 2: every corner in the block has index 1, 2 or 3', all(e and e[0] in (1, 2, 3) for e in evs.values()), len(cks))
nB = sum(e[0] == 1 for e in evs.values()); nS = sum(e[0] == 2 for e in evs.values()); nD = sum(e[0] == 3 for e in evs.values())
low = {q: X.corners_of(q)[int(np.argmin(X.CC[X.corners_of(q)][:, 2]))] for q in cells}
high = {q: X.corners_of(q)[int(np.argmax(X.CC[X.corners_of(q)][:, 2]))] for q in cells}
bornat = {k: e[1][1][0] for k, e in evs.items() if e[0] == 1}; diedat = {k: e[1][1][0] for k, e in evs.items() if e[0] == 3}
check('Figure 2: the births in the block are exactly the lowest corners of cells in the block, cell by cell',
      bornat == {low[q]: q for q in cells if inb(X.CC[low[q]])})
check('Figure 2: the deaths in the block are exactly the highest corners of cells in the block, cell by cell',
      diedat == {high[q]: q for q in cells if inb(X.CC[high[q]])})
check('Figure 2: swaps = corners - births - deaths', nS == len(cks) - nB - nD, (len(cks), nB, nS, nD))
FIG['fig2'] = {'cells': len(cells), 'corners': len(cks), 'births': int(nB), 'swaps': int(nS), 'deaths': int(nD)}
DIR2 = np.array([0.66, 0.36, 0.64])
from scipy.spatial import cKDTree
KT = cKDTree(X.CC[cks])
born_in = {q for q in cells if inb(X.CC[low[q]])}; dies_in = {q for q in cells if inb(X.CC[high[q]])}
FATE = {'born': BORN, 'dies': DIES, 'both': '#b9b2a3', 'through': None}
THRU = ['#7d6f5c', '#746754', '#857662', '#6e624f', '#807160']
fate = lambda q: 'both' if q in born_in and q in dies_in else 'born' if q in born_in else 'dies' if q in dies_in else 'through'
FIG['fig2'].update({k: sum(fate(q) == k for q in cells) for k in ('born', 'dies', 'both', 'through')})
parts, allP = [], []
ctr = (blo + bhi) / 2; NS = 3; gap = 0.16 * HB * vB * 2.0
for sl in range(NS):
    lo_, hi_ = blo.copy(), bhi.copy(); lo_[2] = blo[2] + HB * sl / NS; hi_[2] = blo[2] + HB * (sl + 1) / NS
    for q in sorted(cells):
        Pq = X.cell(q, (lo_, hi_))
        if Pq is None: continue
        Q = W(Pq.V - ctr, vB) + [0, (sl - (NS - 1) / 2) * gap, 0]; allP.append(Q)
        fc = FATE[fate(q)] or THRU[q % len(THRU)]
        balls = []
        for v in range(len(Pq.V)):
            dd, kk = KT.query(Pq.V[v])
            if dd < 1e-9: balls.append((v, EV[{1: 'birth', 2: 'swap', 3: 'death'}[evs[cks[kk]][0]]], 3.4))
        parts.append((Q, Pq.faces, fc, balls))
fr2b = framing(allP, DIR2, 0.90)
write(os.path.join(OUT, 'block.html'), [{'E': 1.0, 'dir': DIR2.tolist(), 'parts': [poly_part(fr2b(Q), F, c, rad=0.0024, balls=b) for Q, F, c, b in parts]}])
json.dump({'axis': [project(fr2b(W(np.array([blo, [blo[0], blo[1], bhi[2]]]) - ctr, vB)), DIR2, 1.0).tolist()]}, open(os.path.join(OUT, 'block.json'), 'w'))

# ================================================================ Figure 4: the 120-cell cell, swept in two directions
FT = json.load(open(os.path.join(DATA, 'fig-tube.json')))
check('Figure 4: fig_tube.py checks all pass', all(c[1] for c in FT['checks']) and len(FT['checks']) == 20)
VIO, VIO_E = '#8a5cc4', '#d8c8f0'
KCOL = {'birth': EV['birth'], 'death': EV['death'], 'swap': AMBER, 'neighbour born': EV['neighbour'], 'neighbour dies': EV['neighbour']}
sc4, lab4 = [], []
for d in FT['directions']:
    V = np.array(d['corners']); Q = np.c_[V[:, 0], V[:, 2], -V[:, 1]]
    dirv = np.array([0.55, 0.30, 0.78])
    walls = []
    for w in d['walls']:                                    # order each pentagon round its centre
        P = V[w]; c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n); u = (P[0] - c) / np.linalg.norm(P[0] - c)
        walls.append([w[i] for i in np.argsort(np.arctan2((P - c) @ np.cross(n, u), (P - c) @ u))])
    secP = [np.array(s) for s in d['sections']]; secQ = [np.c_[s[:, 0], s[:, 2], -s[:, 1]] for s in secP]
    fr4 = framing([Q], dirv, 0.80)
    parts = [poly_part(fr4(Q), back_faces(Q, walls, dirv), VIO, edges=[tuple(e) for e in d['edges']], edge_col=VIO_E, rad=0.0042,
                       balls=[(i, KCOL[d['kind'][i]], 5.0 if d['kind'][i] in ('birth', 'death') else 3.6) for i in range(len(Q))])]
    for s in secQ:
        n = len(s); parts.append(poly_part(fr4(s), [list(range(n))], '#d9c7a3', edge_col='#e9dcc0', rad=0.0024))
    sc4.append({'E': 1.0, 'dir': dirv.tolist(), 'parts': parts})
    lab4.append({'sections': [[len(s), project(fr4(s), dirv, 1.0)[:, 0].max(), project(fr4(s), dirv, 1.0)[:, 1].mean()] for s in secQ]})
write(os.path.join(OUT, 'tube.html'), sc4); json.dump(lab4, open(os.path.join(OUT, 'tube.json'), 'w'))

# ================================================================ Figure 5: a Poisson–Voronoi block and a bcc block in space
LE = 4.4; DIR5 = np.array([0.62, 0.48, 0.62])
r5 = np.random.default_rng(5)
pv = r5.uniform(-2.5, LE + 2.5, size=(r5.poisson((LE + 5) ** 3), 3))
a = 2 ** (1 / 3)                                           # bcc spacing for one seed per unit volume, as the Poisson seeds
g = np.arange(-4, 9) * a; G = np.array(np.meshgrid(g, g, g)).reshape(3, -1).T
bcc = np.vstack([G, G + a / 2]) + 0.37 * a                  # offset so the cube's faces cut the cells off-centre
sc5, FIG['fig5'] = [], {}
for nm, S in (('pv', pv), ('bcc', bcc)):
    Y = Complex(S); lo, hi = np.zeros(3), np.full(3, LE)
    parts, allP, Fs = [], [], []
    for q in range(len(S)):
        if np.abs(S[q] - LE / 2).max() > LE / 2 + 2: continue
        if (np.abs(S[q] - LE / 2) < LE / 2 + 0.5).all():             # whole cells round the block, for the wall counts
            full = Y.cell(q); Fs.append(len(full.faces) if nm == 'pv' else sorted(len(f) for f in full.faces))
        Pq = Y.cell(q, (lo, hi))
        if Pq is None: continue
        if S[q][0] > LE / 2 and S[q][2] > LE / 2 and S[q][1] < LE / 2: continue    # the top front octant, removed
        Q = W(Pq.V - LE / 2, 1.0); allP.append(Q)
        fc = [CUTF if np.abs(m).max() > 1 - 1e-9 else TONES[q % len(TONES)] for m, dd in Pq.planes]
        parts.append(poly_part(Q, Pq.faces, fc, rad=0.0030))
    fr5 = framing(allP, DIR5, 0.9)
    for pt in parts: pt['v'] = np.round(fr5(np.array(pt['v'])), 6).tolist()
    sc5.append({'E': 1.0, 'dir': DIR5.tolist(), 'parts': parts})
    if nm == 'bcc':
        check('Figure 5: every whole bcc cell has 14 walls (6 squares, 8 hexagons)', all(f == [4] * 6 + [6] * 8 for f in Fs), len(Fs))
    else:
        FIG['fig5']['pv_cells_counted'] = len(Fs); FIG['fig5']['pv_mean_walls'] = float(np.mean(Fs))
        check('Figure 5: Poisson–Voronoi cells drawn, mean walls of the whole inner cells near 2 + 48π²/35', abs(np.mean(Fs) - (2 + 48 * np.pi ** 2 / 35)) < 1.0, (len(Fs), np.mean(Fs)))
write(os.path.join(OUT, 'law.html'), sc5)

json.dump({'checks': CHECKS, 'figures': FIG}, open(os.path.join(DATA, 'fig-scenes.json'), 'w'), indent=1)
nf = sum(not c[1] for c in CHECKS)
print('%d checks, %d failed' % (len(CHECKS), nf)); print('FINAL ok' if nf == 0 else 'FINAL FAIL'); sys.exit(1 if nf else 0)
