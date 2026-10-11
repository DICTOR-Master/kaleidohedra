# Can phi^up x TARGET be built from the same kit at sizes phi^0..phi^-K (I, AXE, FUJI, CLEO)?  Placements: kit pieces in
# the 120 icosahedral orientations, translated so one vertex sits on a candidate point and all vertices land on candidate
# points inside the target. Selection: MILP packing over dense sample points, volume must equal the target's; any
# solution is then verified exactly (pairwise separating-axis, containment, volume).
import json, sys, itertools, time, numpy as np
from scipy.spatial import ConvexHull, cKDTree
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix
PHI = (1 + 5 ** .5) / 2
L = json.load(open(sys.argv[1])); TARGET = sys.argv[2]; UP = int(sys.argv[3]); K = int(sys.argv[4]); ROUNDS = int(sys.argv[5])
allV = np.array([v for p in L if p['role'] in ('ico','axe','fuji','cleo') for v in p['vertices']]); O = allV.mean(0)
for p in L: p['V'] = np.array(p['vertices']) - O
d = np.linalg.norm(allV - O, axis=1); I0 = np.unique(np.round((allV - O)[d > d.max() - 1e-6], 9), axis=0)
# the 120 symmetries of the Lotus seed's frame
G = []
A = None
for i, j, k in itertools.permutations(range(12), 3):
    if A is None:
        e = np.min([np.linalg.norm(I0[0] - I0[m]) for m in range(1, 12)])
        nb = [m for m in range(12) if abs(np.linalg.norm(I0[m] - I0[0]) - e) < 1e-6]; b = nb[0]
        c = [m for m in nb if abs(np.linalg.norm(I0[m] - I0[b]) - e) < 1e-6][0]; A = np.array([I0[0], I0[b], I0[c]]).T; Ai = np.linalg.inv(A)
    R = np.array([I0[i], I0[j], I0[k]]).T @ Ai
    if not np.allclose(R @ R.T, np.eye(3), atol=1e-6): continue
    Y = I0 @ R.T
    if all(np.min(np.linalg.norm(I0 - y, axis=1)) < 1e-6 for y in Y): G.append(R)
print('symmetries', len(G), flush=True)
def rep(role, small=False):
    for p in L:
        if p['role'] != role: continue
        if role == 'ico':
            e = np.min([np.linalg.norm(p['V'][0] - q) for q in p['V'][1:]])
            if (e < 0.9) != small: continue
        return p
kit = {'I': rep('ico'), 'axe': rep('axe'), 'fuji': rep('fuji'), 'cleo': rep('cleo')}
TAU_ = PHI
DZ = {'A': [(0, 0, 0), (TAU_**3, 0, TAU_**2), (TAU_**2, TAU_**2, TAU_**2), (TAU_**2, 1, 0)],
      'B': [(0, 0, 0), (TAU_**3, 0, TAU_**2), (TAU_**2, TAU_**2, TAU_**2), (TAU_**2, TAU_, 1)],
      'C': [(0, 0, 0), (-TAU_, 0, 1), (TAU_**2, TAU_**2, TAU_**2), (0, TAU_**2, 1)],
      'K': [(0, 0, 0), (-1, TAU_, 0), (TAU_, TAU_, TAU_), (-0.5, 0.5 / TAU_, TAU_ / 2)]}
for _k, _v in DZ.items(): kit[_k] = {'V': np.array(_v, float) / 2, 'faces': [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]}
for _t in ('t1','t2','t3','t4','t5','t6','T2','j2'):
    _p = rep(_t)
    if _p is not None: kit[_t] = _p
def hull(V):
    H = ConvexHull(V); return H.equations, H.volume
if TARGET == 'jsides':   # DICTO 2026-10-11: the pentagonal pyramid (J2) by the same tip + mirror rule
    Fv = kit['j2']['V']; apex = Fv[0]; base = Fv[1:]
    TV = np.vstack([base, apex + PHI ** UP * (base - apex)])
elif TARGET in ('band', 'sides'):   # DICTO 2026-10-11: phi^UP x FUJI minus the FUJI tip at its apex; the band between them
    F = kit['fuji']; Fv = F['V']; hexf = [f for f in F['faces'] if len(f) == 6][0]
    apex = Fv[[i for i in range(len(Fv)) if i not in hexf][0]]; base = Fv[hexf]
    TV = np.vstack([base, apex + PHI ** UP * (base - apex)])
else:
    T = kit[TARGET]; c0 = T['V'].mean(0); TV = c0 + PHI ** UP * (T['V'] - c0)
TE, TVOL = hull(TV)
inside = lambda X, tol=1e-7: np.all(X @ TE[:, :3].T + TE[:, 3] <= tol, axis=-1)
def overlap(A, B):
    EA, _ = hull(A); EB, _ = hull(B); axes = list(EA[:, :3]) + list(EB[:, :3])
    ea = [A[i] - A[j] for i in range(len(A)) for j in range(i)]; eb = [B[i] - B[j] for i in range(len(B)) for j in range(i)]
    for u in ea:
        for v in eb:
            w = np.cross(u, v)
            if np.linalg.norm(w) > 1e-9: axes.append(w / np.linalg.norm(w))
    for ax in axes:
        a, b = A @ ax, B @ ax
        if a.max() <= b.min() + 1e-7 or b.max() <= a.min() + 1e-7: return False
    return True
# DICTO 2026-10-11: the sides = band minus a FUJI(1/phi) turned upside down by a point-mirror through the centre of the
# tip's base (stays in the icosahedral frame; a flat mirror would not). Its apex touches the band's floor.
c1 = base.mean(0); HV = c1 - (Fv - c1) / PHI
HE, HVOL = hull(HV)
TVOL = TVOL - HVOL
print(f'sides volume {TVOL:.12f} = {TVOL / hull(Fv)[1]:.9f} FUJI', flush=True)
def in_hole(X, tol=-1e-9): return np.all(X @ HE[:, :3].T + HE[:, 3] <= tol, axis=-1)
def clear_of_hole(W):
    for e in HE:                                     # quick: whole piece outside one hole face
        if np.all(W @ e[:3] + e[3] >= -1e-7): return True
    return not overlap(W, HV)
# kit shapes (centred), all orientations and sizes, deduplicated
shapes = []
for name, p in kit.items():
    V0 = p['V'] - p['V'].mean(0); E, vol = hull(V0)
    for k in range(0, -K - 1, -1):
        if name == TARGET and k >= UP: continue
        seen = set()
        for R in G:
            V = PHI ** k * V0 @ R.T
            key = tuple(sorted(tuple(np.round(v, 5)) for v in V))
            if key in seen: continue
            seen.add(key); shapes.append((f'{name}@phi^{k}', V, PHI ** (3 * k) * vol))
print('kit shapes (piece x size x orientation):', len(shapes), flush=True)
# candidate points: closure from the target's corners
P = np.vstack([TV, HV])
place = {}
# vectorised (2026-10-11): for each shape, all translations putting one of its corners on a candidate point at once
NB, DB = TE[:, :3], TE[:, 3]; NH, DH = HE[:, :3], HE[:, 3]
for rnd in range(ROUNDS):
    newpts = []
    for si, (nm, V, vol) in enumerate(shapes):
        smax = (V @ NB.T).max(0)                          # per band face: farthest corner of the shape
        hmin = (V @ NH.T).min(0)                          # per hole face: nearest corner of the shape
        T = (P[:, None, :] - V[None, :, :]).reshape(-1, 3)   # not rounded before the test (points carry ~1e-6 noise)
        ok = np.all(T @ NB.T + smax + DB <= 5e-6, axis=1)
        T = T[ok]
        if not len(T): continue
        clear = np.any(T @ NH.T + hmin + DH >= -5e-6, axis=1)   # whole piece beyond one hole face
        for t, c in zip(T, clear):
            key = (si, tuple(np.round(t, 5)))
            if key in place: continue
            W = V + t
            if not c and overlap(W, HV): continue
            place[key] = W; newpts.append(W)
    if newpts:
        Q = np.unique(np.round(np.vstack([P] + newpts), 6), axis=0)
        print(f'round {rnd}: placements {len(place)}, points {len(P)} -> {len(Q)}', flush=True); P = Q
# keep only placements whose vertices are all candidate points (snug placements)
tree = cKDTree(P)
keys = [k for k, W in place.items() if np.all(tree.query(W)[0] < 1e-5)]
print('snug placements', len(keys), flush=True)
# sample points
rng = np.random.default_rng(1); lo, hi = TV.min(0), TV.max(0)
S = rng.uniform(lo, hi, (400000, 3)); S = S[inside(S, -1e-9) & ~in_hole(S, 1e-9)][:40000]
print('sample points', len(S), flush=True)
M = lil_matrix((len(S), len(keys)), dtype=np.int8); vols = np.zeros(len(keys))
for c, key in enumerate(keys):
    W = place[key]; E, _ = hull(W); vols[c] = shapes[key[0]][2]
    hit = np.where(np.all(S @ E[:, :3].T + E[:, 3] <= -1e-9, axis=1))[0]
    M[hit, c] = 1
M = csr_matrix(M)
cons = [LinearConstraint(M, 0, 1), LinearConstraint(vols[None, :], TVOL - 1e-7, TVOL + 1e-7)]
t0 = time.time()
res = milp(c=np.ones(len(keys)), constraints=cons, integrality=np.ones(len(keys)), bounds=Bounds(0, 1), options={'time_limit': float(sys.argv[6]), 'disp': False})
print('MILP:', res.status, res.message, f'{time.time() - t0:.0f}s', flush=True)
if res.x is None: sys.exit()
chosen = [keys[i] for i in np.where(res.x > 0.5)[0]]
# exact verification: pairwise overlap by separating axis (convex pieces)
W = [place[k] for k in chosen]
bad = sum(overlap(W[i], W[j]) for i in range(len(W)) for j in range(i)) + sum(overlap(w, HV) for w in W)
tot = sum(shapes[k[0]][2] for k in chosen)
from collections import Counter
print('pieces:', dict(Counter(shapes[k[0]][0] for k in chosen)))
print(f'volume {tot:.12f} vs target {TVOL:.12f}; overlapping pairs: {bad}')
json.dump([{'name': shapes[k[0]][0], 'vertices': place[k].tolist()} for k in chosen], open(f'selfbuild-{TARGET}-{UP}.json', 'w'))
