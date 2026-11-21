# DICTO · dictospheres.com — 3D scenes of the resin solution (tree branch D, bcc at s0, central division R1) for the house
# three.js renderer (render3d.py, copied unchanged from paper #115 / the Dehn Canon paper; shots.mjs takes the frames).
# C1 is rebuilt here in floats exactly as branch D's resin.py builds it (truncated icosahedron, edge 1, apices at
# ((5+sqrt5)/4)(0, 1, phi) and images); the 80 resin pieces are the five kinds of data/resin.json (bcc, scale 1, R1) moved by
# the 24 elements of T_h. Checks (printed, then FINAL ok): lateral edges sqrt3 phi/2, vol C1, 80 distinct pieces, each piece
# sits on one C1 face, sum of piece volumes = mould - C1, every piece inside the mould.
import json, os, sys, itertools
import numpy as np
from render3d import write, solid_part

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, 'renders'); os.makedirs(OUT, exist_ok=True)
DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, '..', '..', 'tree', 'branch-D-resin', 'data', 'resin.json')
PHI = (1 + 5 ** .5) / 2
TOL = 1e-7


class Solid:
    """float polytope: corners V, faces F = (normal, offset, ordered corner indices), edges E"""
    def __init__(s, V, F):
        s.V = np.asarray(V, float); s.F = F
        E = set()
        for _, _, o in F:
            for a, b in zip(o, o[1:] + o[:1]): E.add((min(a, b), max(a, b)))
        s.E = sorted(E)
    def vf(s): return s.V


def hull(P):
    """convex hull of a small point set by planes through triples (exact enough at TOL); returns Solid"""
    P = np.asarray(P, float); U = []
    for p in P:
        if not any(np.linalg.norm(p - q) < 1e-6 for q in U): U.append(p)
    P = np.array(U); c = P.mean(0); F, seen = [], []
    for i, j, k in itertools.combinations(range(len(P)), 3):
        n = np.cross(P[j] - P[i], P[k] - P[i]); L = np.linalg.norm(n)
        if L < 1e-9: continue
        n /= L; d = n @ P[i]; v = P @ n - d
        if v.max() > TOL:
            if v.min() < -TOL: continue
            n, d, v = -n, -d, -v
        if any(np.allclose(n, m, atol=1e-6) for m in seen): continue
        seen.append(n); idx = [t for t in range(len(P)) if abs(v[t]) < TOL]
        fc = P[idx].mean(0); a = P[idx[0]] - fc; a /= np.linalg.norm(a); b = np.cross(n, a)
        idx.sort(key=lambda t: np.arctan2((P[t] - fc) @ b, (P[t] - fc) @ a))
        F.append((n, d, idx))
    return Solid(P, F)


def volume(S):
    c = S.V.mean(0); v = 0
    for n, d, o in S.F:
        for a, b in zip(o[1:-1], o[2:]): v += abs(np.linalg.det([S.V[o[0]] - c, S.V[a] - c, S.V[b] - c])) / 6
    return v


def moved(S, t): return Solid(S.V + t, S.F)


# ---------- C1 (as resin.py build_C1, in floats) ----------
TV = []
for b in [(0, 1, 3 * PHI), (1, 2 + PHI, 2 * PHI), (PHI, 2, 2 * PHI + 1)]:
    for sg in itertools.product((1, -1), repeat=3):
        t = [b[i] * sg[i] / 2 for i in range(3)]
        for c in ([t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]):
            if not any(np.allclose(c, q) for q in TV): TV.append(c)
TV = np.array(TV); assert len(TV) == 60
TI = hull(TV)
pents = [f for f in TI.F if len(f[2]) == 5]; hexes = [f for f in TI.F if len(f[2]) == 6]
assert len(pents) == 12 and len(hexes) == 20
k = (5 + 5 ** .5) / 4; apex = []
for n, d, o in pents:
    A = k * np.sqrt(1 + PHI ** 2) * n
    for i in o: assert abs(np.linalg.norm(A - TV[i]) - 3 ** .5 * PHI / 2) < 1e-12
    apex.append(A)
pyramids = [hull(np.vstack([TV[o], A])) for (n, d, o), A in zip(pents, apex)]
vC1 = volume(TI) + sum(volume(p) for p in pyramids)
LOG = [f'C1: 60 TI corners + 12 apices; lateral edges = sqrt3 phi/2 (checked); vol C1 = {vC1:.10f} (exact 35 + 25 sqrt5/2 = {35 + 12.5 * 5 ** .5:.10f})']
assert abs(vC1 - (35 + 12.5 * 5 ** .5)) < 1e-9
# C1 as one non-convex solid: 20 hexagons + 60 triangles, for the cell scenes
V1 = np.vstack([TV, apex]); F1 = []
for n, d, o in hexes: F1.append((n, d, list(o)))
for p, (n, d, o) in enumerate(pents):
    for i in range(5):
        tri = [o[i], o[(i + 1) % 5], 60 + p]; m = np.cross(V1[tri[1]] - V1[tri[0]], V1[tri[2]] - V1[tri[0]]); m /= np.linalg.norm(m)
        if m @ V1[tri[0]] < 0: tri = tri[::-1]; m = -m
        F1.append((m, m @ V1[tri[0]], tri))
C1 = Solid(V1, F1)

# ---------- the resin: bcc at s0, rule R1 ----------
D = json.load(open(DATA))
A = [a for a in D['arrangements'] if a['lattice'] == 'bcc' and a['scale_factor'] == '1' and a['rule'] == 'R1'][0]
s = A['s']; assert abs(s - (10 + 4 * 5 ** .5) / 3) < 1e-12
TH = [(c, sg) for c in range(3) for sg in itertools.product((1, -1), repeat=3)]
def act(g, X):
    c, sg = g; X = np.atleast_2d(X); Y = X[:, [(i - c) % 3 for i in range(3)]]; return Y * np.array(sg)
pieces = []                               # (kind number 1..5, Solid)
for kn, kd in enumerate(A['kinds'], 1):
    base = np.array(kd['verts']); imgs = []
    for g in TH:
        Y = act(g, base); key = tuple(sorted(map(tuple, np.round(Y, 6) + 0.0)))
        if key not in imgs: imgs.append(key); pieces.append((kn, hull(Y)))
    assert len(imgs) == kd['orbit'], (kn, len(imgs), kd['orbit'])
assert len(pieces) == 80
mould = hull([p for q in itertools.permutations((0, 1, 2)) for sg in itertools.product((1, -1), repeat=2)
              for p in [np.array([0, sg[0] * s / 4, sg[1] * s / 2])[list(q)]]])
assert len(mould.V) == 24 and len(mould.F) == 14
vm = volume(mould); vp = sum(volume(p) for _, p in pieces)
LOG.append(f'bcc s0 = {s:.9f}: mould vol {vm:.9f} (s^3/2 = {s ** 3 / 2:.9f}); 80 pieces, sum vol {vp:.9f} = mould - C1 {vm - vC1:.9f}')
assert abs(vm - s ** 3 / 2) < 1e-9 and abs(vp - (vm - vC1)) < 1e-8
for _, p in pieces:
    assert all((p.V @ n - d).max() < 1e-7 for n, d, o in mould.F)
    # each piece has one face lying on a C1 face
    cnt = sum(1 for n, d, o in p.F if any(np.allclose(-n, m, atol=1e-6) and abs(d + e) < 1e-6 for m, e, oo in C1.F)); assert cnt == 1, (cnt, len(p.V), len(p.F), sorted(len(o) for n, d, o in p.F))
LOG.append('every piece inside the mould and on exactly one C1 face (checked); kinds 1-5 = T_h face orbits hex 8, hex 12, tri 24, tri 24, tri 12')

# ---------- colours ----------
VIOLET = '#8a5cc4'                        # the dodecahedron colour (element-colours.md): C1's pyramids are dodecahedron centre pyramids
PEARL = '#e2ded6'                         # the truncated icosahedron: neutral
KIND = ['#d6b46a', '#9c7448', '#7f93a8', '#c99e95', '#8f8a80']   # kinds 1-5: neutral labels only (sand, bronze, slate, rose-beige, ash)
GLASS = '#cfd8dc'; EDGE = '#2b261e'; LIGHT = '#efe6d0'


def c1_parts(t_pyr=0.0, rad=0.005):
    parts = [solid_part(TI, PEARL, rad=rad, edge_col=EDGE)]
    for (n, d, o), P in zip(pents, pyramids):
        parts.append(solid_part(moved(P, t_pyr * n), VIOLET, rad=rad, edge_col=EDGE))
    return parts


def c1_whole(rad=0.004, shift=np.zeros(3)):
    cols = [PEARL if len(o) == 6 else VIOLET for n, d, o in C1.F]
    return solid_part(moved(C1, shift), cols, rad=rad, edge_col=EDGE)


def ext(parts, dirv, pad=1.07):
    from render3d import basis
    x, y, _ = basis(dirv); P = np.vstack([p['v'] for p in parts])
    return float(max(np.abs(P @ x).max(), np.abs(P @ y).max()) * pad)


DIR = np.array([0.36, 0.30, 1.0])         # a general view (no symmetry axis along the line of sight)
sc = []
# 1. C1 clean, C1 pyramids pulled out along their axes
p = c1_parts(0); sc.append({'E': ext(c1_parts(1.0), DIR), 'dir': DIR.tolist(), 'parts': p})
p = c1_parts(1.0); sc.append({'E': ext(p, DIR), 'dir': DIR.tolist(), 'parts': p})
write(os.path.join(OUT, 'c1.html'), sc); LOG.append('c1.html: 2 scenes (whole; pyramids pulled out by 1.0 along their axes)')

# 2. one cell pulled apart: pieces moved by f x their centroid; mould drawn see-through at (1+f) x, which holds every moved piece
f = 0.85
parts = [c1_whole(0.0028)]
for kn, P in pieces: parts.append(solid_part(moved(P, f * P.V.mean(0)), KIND[kn - 1], rad=0.0022, edge_col=EDGE))
shell = Solid(mould.V * (1 + f), [(n, d * (1 + f), o) for n, d, o in mould.F])
parts.append(solid_part(shell, GLASS, alpha=0.16, rad=0.0018, edge_col=LIGHT))
sc = [{'E': ext(parts, DIR, 1.04), 'dir': DIR.tolist(), 'parts': parts}]
# the same cell together (mould see-through, resin solid)
parts2 = [c1_whole(0.0028)] + [solid_part(P, KIND[kn - 1], rad=0.0022, edge_col=EDGE) for kn, P in pieces]
sc.append({'E': sc[0]['E'], 'dir': DIR.tolist(), 'parts': parts2})
write(os.path.join(OUT, 'cell.html'), sc); LOG.append(f'cell.html: 2 scenes (pulled apart, f = {f}; together)')

# 3. a few cells together: bcc translates; the front-top cell shows C1 in its see-through mould, the others their resin
T = [np.array(v) * s for v in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (.5, .5, -.5), (.5, .5, .5)]]
parts = []
for t in T[:-1]:
    for kn, P in pieces: parts.append(solid_part(moved(P, t), KIND[kn - 1], rad=0.0016, edge_col=EDGE))
parts.append(c1_whole(0.0016, T[-1]))
parts.append(solid_part(moved(mould, T[-1]), GLASS, alpha=0.22, rad=0.0016, edge_col=LIGHT))
cen = np.mean(T, 0); DT = np.array([0.55, 0.42, 1.0])
for q in parts: q['v'] = (np.array(q['v']) - cen).round(6).tolist()
sc = [{'E': ext(parts, DT, 1.04), 'dir': DT.tolist(), 'parts': parts}]
write(os.path.join(OUT, 'tiling.html'), sc); LOG.append('tiling.html: 6 cells of the bcc lattice (5 with resin, 1 with C1 in its see-through mould)')

# 4. kinds 1-5 alone, each turned to stand on its C1 face (outer side up), one view direction, one scale
sc = []
for kn in range(1, 6):
    P = [q for k_, q in pieces if k_ == kn][0]; c = P.V.mean(0)
    bot = [ (n, d) for n, d, o in P.F if any(np.allclose(-n, m, atol=1e-6) and abs(d + e) < 1e-6 for m, e, oo in C1.F)][0]
    n = -bot[0]                                   # outward normal of the piece's C1 face
    y = np.array([0., 1, 0]); v = np.cross(n, y); cth = n @ y; K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R = np.eye(3) + K + K @ K / (1 + cth)          # rotation taking n to +y: every piece stands on its C1 face, outer side up
    assert np.allclose(R @ n, y) and np.allclose(R @ R.T, np.eye(3))
    VD = np.array([0.7, 0.32, 1.0]); VD /= np.linalg.norm(VD); best = None
    for a in np.radians(np.arange(0, 360, 5)):      # turn about the vertical so that no face is seen square on
        Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]); M = Ry @ R
        score = max((M @ nn) @ VD for nn, dd, oo in P.F)
        if best is None or score < best[0]: best = (score, M)
    q = solid_part(Solid((P.V - c) @ best[1].T, P.F), KIND[kn - 1], rad=0.006, edge_col=EDGE)
    sc.append({'E': 0, 'dir': VD.tolist(), 'parts': [q]})
E = max(ext(x['parts'], x['dir'], 1.12) for x in sc)
for x in sc: x['E'] = E
write(os.path.join(OUT, 'kinds.html'), sc); LOG.append('kinds.html: 5 scenes, one piece of each kind, same scale')
open(os.path.join(H, 'scenes.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
