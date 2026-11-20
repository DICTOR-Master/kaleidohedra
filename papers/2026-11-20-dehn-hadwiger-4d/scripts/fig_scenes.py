# DICTO · dictospheres.com — the rendered scenes of Figures 1 and 3 (renders/<fig>.html, one scene per shot), from the exact
# polytopes of exact4d.py, with asserts on every drawn geometry (data/fig-scenes.json).
#   Figure 1 (six.html): the six regular 4-polytopes, each by a perspective projection from a point on the axis of one
#     facet, outside the polytope; edges as tubes shaded from light (near the eye in 4D) to dark (far); the facet farthest
#     from the eye (the small one in the middle; for the 5-cell and the 16-cell one of the large tetrahedra, see-through) is drawn in the app colour of its solid: dodecahedron violet,
#     tetrahedron red, cube green, octahedron yellow. Every edge of each polytope is drawn, none added.
#   Figure 3 (caps.html): the 600-cell with the 120 caps of one left orbit. (a) the 20 facets at one corner, projected
#     orthogonally to the corner's axis: the 4 capped facets solid, their tips and cap edges; (b) the whole solid in
#     perspective; (c) the 120 tips with the edges of their own 600-cell, round the 600-cell, at the scale of (b).
# Colours in Figure 3 are labels only (neutral tones), said in the caption.
# Usage: python3 fig_scenes.py   (on a compute host; then node shots.mjs renders/<fig>.html renders/<fig>; fig_compose.py)
import json, os
import numpy as np
from scipy.spatial import ConvexHull
import exact4d as X
from render3d import write, basis, PX

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'renders'); os.makedirs(OUT, exist_ok=True)
DATA = os.path.join(HERE, '..', 'data'); os.makedirs(DATA, exist_ok=True)
CHECKS = []


def check(name, ok, info=''):
    CHECKS.append([name, bool(ok), str(info)]); print(('PASS ' if ok else 'FAIL ') + name + ' ' + str(info), flush=True)
    assert ok, name


APP = {'dodecahedron': '#8a5cc4', 'tetrahedron': '#cd3e28', 'cube': '#488e48', 'octahedron': '#e8c852'}
CELL = {'120-cell': 'dodecahedron', '600-cell': 'tetrahedron', 'tesseract': 'cube', '5-cell': 'tetrahedron',
        '16-cell': 'tetrahedron', '24-cell': 'octahedron'}
CELLN = {'dodecahedron': 20, 'tetrahedron': 4, 'cube': 8, 'octahedron': 6}
NEAR, FAR = np.array([236, 226, 204]) / 255, np.array([110, 98, 82]) / 255
CREAM, AMBER, SLATE, OUTL = '#d2c3a0', '#c99a45', '#8a9bb3', '#16110c'
BRONZE = '#9a7448'                                    # capped facets (darker than the cap edges: lit faces read lighter)
VIEW = np.array([0.42, 0.30, 1.0])


def hexc(c): c = np.clip(np.round(np.asarray(c) * 255), 0, 255).astype(int); return '#%02x%02x%02x' % tuple(c)


def fl(v): return np.array([float(x) for x in v])


def frame4(c):
    """orthonormal e1, e2, e3 perpendicular to the unit vector c (Gram–Schmidt on the coordinate axes)."""
    B = [c]
    for s in ([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]):
        v = np.array(s, float)
        for b in B: v = v - (v @ b) * b
        if np.linalg.norm(v) > 1e-6: B.append(v / np.linalg.norm(v))
        if len(B) == 4: break
    return np.array(B[1:])


def persp(P, c, D, F):
    """perspective projection from the eye D·c (|c| = 1) onto the 3-space through 0 perpendicular to c."""
    w = P @ c; assert (w < D - 1e-9).all(); return (P @ F.T) * (D / (D - w))[:, None], w


def ext(P3, d, frac=0.92):
    x, y, _ = basis(d); Q = np.c_[P3 @ x, P3 @ y]; return float(np.abs(Q).max() / frac)


def edge_part(P3, E, cols, rad, alpha=1.0):
    return {'v': np.round(P3, 6).tolist(), 't': [], 'c': [], 'a': alpha, 'tubes': [[int(i), int(j), cols[k], OUTL] for k, (i, j) in enumerate(E)],
            'rad': rad, 'balls': []}


def hull_part(P3, col, alpha=1.0):
    h = ConvexHull(P3); c0 = P3.mean(0); tris = []
    for s, eq in zip(h.simplices, h.equations):
        a, b, cc = [int(x) for x in s]
        if np.cross(P3[b] - P3[a], P3[cc] - P3[a]) @ eq[:3] < 0: b, cc = cc, b
        tris.append([a, b, cc])
    return {'v': np.round(P3, 6).tolist(), 't': tris, 'c': [col] * len(tris), 'a': alpha, 'tubes': [], 'rad': 0.0, 'balls': []}


P = X.six(); LOG = {}
# ---------------- Figure 1: the six polytopes -------------------------------------------------------------------------------
EYE = {'120-cell': 1.32, '600-cell': 2.0, 'tesseract': 1.25, '5-cell': 3.2, '16-cell': 2.4, '24-cell': 2.2}
ALPHA = {'5-cell': 0.5, '16-cell': 0.6}   # simplex facets are large in any projection: drawn see-through so the edges behind show
RAD = {'120-cell': 0.0042, '600-cell': 0.0055, 'tesseract': 0.010, '5-cell': 0.010, '16-cell': 0.010, '24-cell': 0.008}
sc = []
for nm in X.ORDER:
    p = P[nm]; R = float(p.R2) ** 0.5; V = np.array([fl(v) for v in p.V]) / R
    N = np.array([fl(n) for n in p.N]); N /= np.linalg.norm(N, axis=1)[:, None]
    c = N[-1]; F = frame4(c)
    P3, w = persp(V, c, EYE[nm], F)
    a = float(p.a2) ** 0.5 / R
    L = [np.linalg.norm(V[i] - V[j]) for i, j in p.E]
    check(f'{nm}: every drawn edge has the exact length', max(abs(l - a) for l in L) < 1e-12, f'{len(p.E)} edges, length {a:.6f} R')
    t = (w - w.min()) / (w.max() - w.min()); cols = [hexc(FAR + (NEAR - FAR) * (t[i] + t[j]) / 2) for i, j in p.E]
    far = int(np.argmin(N @ c)); cell = sorted(p.cells[far])
    check(f'{nm}: the shaded facet is a {CELL[nm]}', len(cell) == CELLN[CELL[nm]], f'{len(cell)} corners')
    parts = [hull_part(P3[cell], APP[CELL[nm]], ALPHA.get(nm, 1.0)), edge_part(P3, p.E, cols, RAD[nm])]
    sc.append({'E': ext(P3, VIEW), 'dir': VIEW.tolist(), 'parts': parts, 'name': nm})
    LOG[nm] = {'counts': p.counts(), 'eye': EYE[nm], 'shaded': CELL[nm]}
write(os.path.join(OUT, 'six.html'), sc)

# ---------------- Figure 3: the 600-cell with 120 caps -------------------------------------------------------------------
p = P['600-cell']; V = np.array([fl(v) for v in p.V]); orb = X.caps(p)[0]
facts, T = X.cap_checks(p, orb)
for k, v in facts.items(): check('caps: ' + k, v)
TT = np.array([fl(t) for t in T])
check('caps: tips at radius √2 (floats agree)', np.allclose(np.linalg.norm(TT, axis=1), 2 ** 0.5))
cap_edges = [(orb_i, i) for orb_i, k in enumerate(orb) for i in sorted(p.cells[k])]
# (a) the 20 facets at corner 0, orthogonal projection onto the 3-space perpendicular to the corner
v0 = V[0]; F0 = frame4(v0)
star = [k for k, c in enumerate(p.cells) if 0 in c]
check('caps: 20 facets at a corner', len(star) == 20)
capped = [k for k in star if k in set(orb)]
check('caps: 4 of them capped', len(capped) == 4)
nb = sorted(set(i for k in star for i in p.cells[k]))
check('caps: the corner and its 12 neighbours', len(nb) == 13)
ed = [(i, j) for i, j in p.E if i in nb and j in nb]
check('caps: 42 edges among them (12 spokes, 30 of the icosahedron)', len(ed) == 42)
spokes = [e for e in ed if 0 in e]
cov = {}
for k in capped:
    for e in spokes:
        if set(e) <= p.cells[k]: cov[e] = cov.get(e, 0) + 1
check('caps: each of the 12 edges at the corner in exactly one capped facet', len(cov) == 12 and set(cov.values()) == {1})
loc = {i: n for n, i in enumerate(nb)}
Pa = np.r_[V[nb] @ F0.T, TT[[orb.index(k) for k in capped]] @ F0.T]
tipidx = {k: len(nb) + n for n, k in enumerate(capped)}
partsA = [hull_part(Pa[[loc[i] for i in sorted(p.cells[k])]], BRONZE) for k in capped]
partsA.append(edge_part(Pa, [(loc[i], loc[j]) for i, j in ed], [CREAM] * len(ed), 0.009))
ce = [(tipidx[k], loc[i]) for k in capped for i in sorted(p.cells[k])]
partsA.append(edge_part(Pa, ce, [AMBER] * len(ce), 0.009))
partsA[-1]['balls'] = [[tipidx[k], AMBER] for k in capped]
# (b), (c): perspective from a point on the axis of corner 0, outside the sphere of the tips
c = V[0] / np.linalg.norm(V[0]); Fb = frame4(c)
D = 3.0
allP = np.r_[V, TT]; P3, w = persp(allP, c, D, Fb)
t = (w - w.min()) / (w.max() - w.min())
colsP = [hexc(FAR + (NEAR - FAR) * (t[i] + t[j]) / 2) for i, j in p.E]
ceB = [(120 + n, i) for n, i in cap_edges]
check('caps: 480 cap edges, each of length = the edge', len(ceB) == 480 and
      max(abs(np.linalg.norm(allP[a] - allP[b]) - float(p.a2) ** 0.5) for a, b in ceB) < 1e-12)
partB = [edge_part(P3, p.E, colsP, 0.0045), edge_part(P3, ceB, [AMBER] * len(ceB), 0.0045)]
partB[-1]['balls'] = [[120 + n, AMBER] for n in range(120)]
# tips' own edges: pairs at distance √2/φ (= √2 × the edge)
tE = [(i, j) for i in range(120) for j in range(i + 1, 120) if abs(np.linalg.norm(TT[i] - TT[j]) - 2 ** 0.5 * float(p.a2) ** 0.5) < 1e-9]
check('caps: the tips span 720 edges of length √2 × edge (a 600-cell)', len(tE) == 720)
partC = [edge_part(P3, p.E, [hexc(FAR)] * len(p.E), 0.003), edge_part(P3, [(120 + i, 120 + j) for i, j in tE], [SLATE] * 720, 0.0045)]
partC[-1]['balls'] = [[120 + n, SLATE] for n in range(120)]
EB = ext(P3, VIEW)
dA = np.array([0.30, 0.42, 1.0])
write(os.path.join(OUT, 'caps.html'), [{'E': ext(Pa, dA, 0.86), 'dir': dA.tolist(), 'parts': partsA},
                                         {'E': EB, 'dir': VIEW.tolist(), 'parts': partB},
                                         {'E': EB, 'dir': VIEW.tolist(), 'parts': partC}])
LOG['caps'] = {'orbit_size': len(orb), 'facts': facts, 'eye': D}
json.dump({'checks': CHECKS, 'log': LOG}, open(os.path.join(DATA, 'fig-scenes.json'), 'w'), indent=1, default=str)
print('FIG SCENES OK', len(CHECKS), 'checks')
