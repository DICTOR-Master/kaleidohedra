# DICTO 2026-10-18 octet study -- STEP 8: the middle piece trimmed round the keys, with notched caps and tetrahedra (DICTO's choice).
# M(c) = hull(star at corner c + star at the facing corner of the OCD across the shared edge) minus both OCDs minus all their keys.
# Float checks (sampling): the Ms on different edges never overlap each other; M is one piece; volumes of every piece of the new set:
# keyed OCD (unchanged), M, notched cap, notched tetrahedron; pieces add up to the cell. -> data/step8-trimmed.json
import itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy import ndimage
from q5 import *
S1 = load('step1-ocd-exact.json'); S2 = load('step2-octet-frame.json'); S5 = load('step5-keyed-octet.json')
V = np.array([[qf(q(x)) for x in v] for v in S1['V']]); R = qf(q(S1['R'])); E_o = ConvexHull(V).equations
Ek = [ConvexHull(np.array([[qf(q(x)) for x in p] for p in K])).equations for K in S5['keys'].values()]
Tp = np.array([[qf(q(x)) for x in v] for v in S2['Tplus']]); E_tp = ConvexHull(Tp).equations; E_tm = ConvexHull(-Tp).equations
Lf = np.array([[qf(q(x)) for x in v] for v in S2['lattice']])
ins = lambda X, Eq: np.all(X @ Eq[:, :3].T + Eq[:, 3] <= 1e-12, axis=1)
r = np.linalg.norm(V, axis=1); five = [i for i in range(len(V)) if r[i] > r.max() - 1e-9]
def first_sign(v):
    for x in v:
        if abs(x) > 1e-9: return x > 0
canon = [i for i in five if first_sign(V[i])]           # 6 corners, one of each +/- pair
Ms = []
for i in canon:
    c = V[i]; o = R * np.sign(np.where(np.abs(c) < 1e-9, 0, c)); star = V[sorted({j for f in S1['faces'] if i in f for j in f})]
    Ms.append((o, ConvexHull(np.vstack([star, o - star])).equations))
shifts = [np.array(ijk) @ Lf for ijk in itertools.product(range(-3, 4), repeat=3)]; shifts = [s for s in shifts if np.linalg.norm(s) < 4.5]
def classify(P):
    if len(P) > 40000:   # chunks keep memory small on the Pi
        parts = [classify(P[i:i + 40000]) for i in range(0, len(P), 40000)]
        return tuple(np.concatenate([p[j] for p in parts]) for j in range(5))
    ocd = np.zeros(len(P), int); key = np.zeros(len(P), int); mid = np.zeros(len(P), int); octa = np.zeros(len(P), int); tet = np.zeros(len(P), int)
    for s in shifts:
        X = P - s; ocd += ins(X, E_o); octa += np.abs(X).sum(1) <= R + 1e-12; tet += ins(X, E_tp).astype(int) + ins(X, E_tm)
        for Eq in Ek: key += ins(X, Eq)
    keyed = (ocd + key) > 0
    for s in shifts:
        X = P - s
        for o, Eh in Ms: mid += ins(X, Eh) & ~keyed
    return ocd, key, mid, octa, tet
# one lattice cell (parallelepiped of the 3 lattice vectors), uniform sample
rng = np.random.default_rng(5); N = 300000; U = rng.random((N, 3)); P = U @ Lf
ocd, key, mid, octa, tet = classify(P)
cellV = abs(np.linalg.det(Lf))
frac = lambda b: float(b.mean() * cellV)
keyedOCD = (ocd + key) > 0; M = mid >= 1; cap = (octa >= 1) & ~keyedOCD & ~M; T = (tet >= 1) & ~keyedOCD & ~M
checks = dict(cell=cellV, samples=N, middle_overlaps_between_edges=int((mid >= 2).sum()),
              vol_keyed_OCD=frac(keyedOCD), vol_M_per_cell=frac(M), vol_one_M=frac(M) / 6, vol_caps_per_cell=frac(cap), vol_one_notched_cap=frac(cap) / 6,
              vol_tets_per_cell=frac(T), vol_one_notched_tet=frac(T) / 2, unassigned=int((~(keyedOCD | M | cap | T)).sum()),
              assigned_twice=int(((keyedOCD.astype(int) + M + cap + T) >= 2).sum()))
# is one M a single piece? voxel test round the edge midpoint of corner canon[0]
o, Eh = Ms[0]; m = o / 2; n = 70; g = np.linspace(-0.45, 0.45, n); G = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3) + m
o_, k_, mid_, *_ = classify(G); inM = ins(G, Eh) & ~((o_ + k_) > 0)
lab, k = ndimage.label(inM.reshape(n, n, n)); sz = np.sort(np.bincount(lab.ravel())[1:])[::-1]
checks['M_components'] = int(k); checks['M_component_sizes'] = sz[:5].tolist()
print(checks)
save('step8-trimmed.json', dict(mark=MARK, step=8, status='float (sampling)', checks=checks))
