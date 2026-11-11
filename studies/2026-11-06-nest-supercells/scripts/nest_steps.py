"""DICTO 11-06 "proceed 1 2 3" after "sounds extremely nestable".
1. UNITY's core: the icosahedron of the 12 cap tips (radius = pentagon circumradius) - does it stay clear of the caps? its nest.
2. Gap volumes round each supercell (Dodeca-13 known: 30 wedges + 20 needles; the 600-cell corner; UNITY).
3. Supercells inside cells: the largest copy of UNITY that fits inside (a) its own heart icosahedron, (b) one of its 12 icosahedra, and
   the largest Dodeca-13 inside one of its dodecahedra; is the scale golden or a halving?"""
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import brentq
phi = (1 + 5 ** .5) / 2
U = json.load(open('../unity-nests.json')); ID = np.array(U['ID']); icos = [np.array(I) for I in U['icos']]; caps = [np.array(c) for c in U['caps']]
apex = np.array([c[-1] for c in caps])
def eqs(V): return ConvexHull(V).equations
def inside_pts(P, V, tol=1e-9): e = eqs(V); return ((P @ e[:, :3].T + e[:, 3]) <= tol).all(1)
rng = np.random.default_rng(1)
def sample(V, n):
    lo, hi = V.min(0), V.max(0); X = rng.uniform(lo, hi, (n * 4, 3)); return X[inside_pts(X, V)][:n]
# 1. heart icosahedron vs caps: sample points of the heart, none may lie strictly inside a cap
H = sample(apex, 200000)
inside_cap = np.zeros(len(H), bool)
for c in caps: inside_cap |= inside_pts(H, c, tol=-1e-9)
print(f"1. heart icosahedron (edge {np.linalg.norm(apex[0]-apex[np.argsort(np.linalg.norm(apex-apex[0],axis=1))[1]]):.6f}): points inside a cap {inside_cap.mean():.6f}")
vH = ConvexHull(apex).volume; vID = ConvexHull(ID).volume; vcaps = sum(ConvexHull(c).volume for c in caps)
print(f"   ID {vID:.6f} = caps {vcaps:.6f} + heart {vH:.6f} + rest of core {vID - vcaps - vH:.6f}")
# 2. gaps
d13 = json.load(open('~/k-research/studies/2026-10-09-dodeca-13/data/c13-parts-pieces-unit.json'))['parts']
vw = sum(ConvexHull(np.array(p['vertices'])).volume for p in d13 if p['role'] != 'dodeca')
vd = sum(ConvexHull(np.array(p['vertices'])).volume for p in d13 if p['role'] == 'dodeca')
print(f"2. Dodeca-13: dodecahedra {vd:.6f}, wedges + needles {vw:.6f} ({vw/(vd+vw):.4f} of the filled cluster)")
T6 = json.load(open('../nest600.json'))['tets']; allT = np.vstack(T6); vT = sum(ConvexHull(np.array(t)).volume for t in T6); vh = ConvexHull(allT).volume
print(f"   600-cell corner: tetrahedra {vT:.6f}, gap inside their hull {vh - vT:.6f} ({(vh - vT)/vh:.4f})")
allU = np.vstack([ID] + icos); vhu = ConvexHull(allU).volume; vI = sum(ConvexHull(I).volume for I in icos)
vpart = vID + vI - vcaps
print(f"   UNITY: ID + 12 J11 {vpart:.6f}; its hull {vhu:.6f}; gap round it inside the hull {vhu - vpart:.6f} ({(vhu - vpart)/vhu:.4f})")
# 3. largest scaled copy inside a cell (same centre); test by corner points of the supercell's parts
def fits(points, cellV, s, centre):
    return inside_pts(centre + s * (points - points.mean(0) * 0), cellV).all()
Upts = np.vstack([ID] + icos)                                   # UNITY's corners (centred at the origin)
def smax(points, cellV, centre):
    lo, hi = 1e-4, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if inside_pts(centre + m * points, cellV).all(): lo = m
        else: hi = m
    return lo
s_heart = smax(Upts, apex, np.zeros(3))
s_cell = max(smax(Upts @ R.T, icos[0], icos[0].mean(0)) for R in [np.eye(3)])
D13 = np.vstack([np.array(p['vertices']) for p in d13]); c13 = [np.array(p['vertices']) for p in d13 if p['role'] == 'dodeca']
cc = min(c13, key=lambda V: np.linalg.norm(V.mean(0)))
s_d13 = smax(D13 - cc.mean(0), cc, cc.mean(0))
def golden(s):
    k = np.log(1 / s) / np.log(phi); return f"1/phi^{k:.4f}"
print(f"3. largest UNITY inside its heart icosahedron: x{s_heart:.6f} ({golden(s_heart)}); inside one of its icosahedra (same orientation as UNITY): x{s_cell:.6f}")
print(f"   largest Dodeca-13 inside its central dodecahedron: x{s_d13:.6f} ({golden(s_d13)})")
print("FINAL ok")
