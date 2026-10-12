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
for _t in ('t1','t2','t3','t4','t5','t6','T2'):
    _p = rep(_t)
    if _p is not None: kit[_t] = _p
def hull(V):
    H = ConvexHull(V); return H.equations, H.volume
# DICTO's top-down FUJI (2026-10-12): TARGET 'band' = the slab between FUJI and phi*FUJI (scaled about the apex); bands of the
# same shape at smaller sizes join the kit, so a solution reads band = kit pieces + smaller FUJIs + smaller bands.
import os
if TARGET == 'band':
    Fv = kit['fuji']['V']; Hf = ConvexHull(Fv)
    base_eq = [e for e in Hf.equations if np.sum(np.abs(Fv @ e[:3] + e[3]) < 1e-7) == 6][0]
    onb = np.abs(Fv @ base_eq[:3] + base_eq[3]) < 1e-7; apex = Fv[~onb][0]; B = Fv[onb]
    kit['band'] = {'V': np.vstack([B, apex + PHI * (B - apex)])}
# DICTO 2026-10-12: FUJI's recut pieces as extra units (env EXTRA=1): the cube corner, the three CLEO-volume pieces and the two
# right-angled pieces (apex, base centre, base corner, base-edge midpoint; long and short edge), mirror images via the 120 frame maps.
if os.environ.get('EXTRA') == '1':
    Fv = kit['fuji']['V']; Hf = ConvexHull(Fv)
    base_eq = [e for e in Hf.equations if np.sum(np.abs(Fv @ e[:3] + e[3]) < 1e-7) == 6][0]
    onb = np.abs(Fv @ base_eq[:3] + base_eq[3]) < 1e-7; apex = Fv[~onb][0]; B = Fv[onb]; cB = B.mean(0)
    ang = np.arctan2(*(np.linalg.svd(B - cB)[2][:2] @ (B - cB).T)[::-1]); B = B[np.argsort(ang)]
    L = [np.linalg.norm(B[i] - B[(i + 1) % 6]) for i in range(6)]; i0 = int(np.argmax(L))
    B = np.roll(B, -i0, axis=0)                         # B[0]-B[1] is a long edge
    kit['cubecorner'] = {'V': np.vstack([apex, B[0], B[2], B[4]])} if abs(np.linalg.norm(B[0] - B[2]) - np.sqrt(2)) < 1e-6 else {'V': np.vstack([apex, B[1], B[3], B[5]])}
    kit['cleovol'] = {'V': np.vstack([apex, B[0], B[1], B[2]])}
    kit['rlong'] = {'V': np.vstack([apex, cB, B[0], (B[0] + B[1]) / 2])}
    kit['rshort'] = {'V': np.vstack([apex, cB, B[1], (B[1] + B[2]) / 2])}
    for k_ in ('cubecorner', 'cleovol', 'rlong', 'rshort'): print(k_, 'volume', round(ConvexHull(kit[k_]['V']).volume, 6), flush=True)
T = kit[TARGET]; c0 = T['V'].mean(0); TV = c0 + PHI ** UP * (T['V'] - c0)
TE, TVOL = hull(TV)
inside = lambda X, tol=1e-7: np.all(X @ TE[:, :3].T + TE[:, 3] <= tol, axis=-1)
# kit shapes (centred), all orientations and sizes, deduplicated
shapes = []
for name, p in kit.items():
    V0 = p['V'] - p['V'].mean(0); E, vol = hull(V0)
    for k in range(0, -K - 1, -1):
        if name == TARGET and k >= UP: continue
        if name == 'band' and k >= 0: continue
        seen = set()
        for R in G:
            V = PHI ** k * V0 @ R.T
            key = tuple(sorted(tuple(np.round(v, 5)) for v in V))
            if key in seen: continue
            seen.add(key); shapes.append((f'{name}@phi^{k}', V, PHI ** (3 * k) * vol))
_u = {}
for nm, V, vol in shapes:
    _u.setdefault(tuple(sorted(tuple(np.round(v, 5)) for v in V)), (nm, V, vol))
shapes = list(_u.values())
print('kit shapes (piece x size x orientation), duplicates removed:', len(shapes), flush=True)
# candidate points: closure from the target's corners
P = np.array(TV)
place = {}
for rnd in range(ROUNDS):
    tree = cKDTree(P); newpts = []
    for si, (nm, V, vol) in enumerate(shapes):
        for p in P:
            for j in range(len(V)):
                t = p - V[j]; W = V + t
                if not inside(W).all(): continue
                key = (si, tuple(np.round(t, 5)))
                if key in place: continue
                place[key] = W; newpts.extend(W)
    if newpts:
        Q = np.unique(np.round(np.vstack([P, newpts]), 6), axis=0)
        print(f'round {rnd}: placements {len(place)}, points {len(P)} -> {len(Q)}', flush=True); P = Q
# keep only placements whose vertices are all candidate points (snug placements)
tree = cKDTree(P)
keys = [k for k, W in place.items() if np.all(tree.query(W)[0] < 1e-5)]
print('snug placements', len(keys), flush=True)
# optional symmetry (env SYM=1): choose placements in whole orbits of the target's own symmetries in the frame
import os
if os.environ.get('SYM') == '1':
    same = lambda X, Y: all(np.min(np.linalg.norm(Y - x, axis=1)) < 1e-6 for x in X)
    stab = [g for g in G if same(TV @ g.T, TV)]
    canon = lambda W: tuple(sorted(tuple(np.round(v, 4)) for v in W))
    bykey = {canon(place[k]): k for k in keys}; orbits, seen = [], set()
    for k in keys:
        if k in seen: continue
        mem = [bykey.get(canon(place[k] @ g.T)) for g in stab]
        if any(m is None for m in mem): continue
        mem = list(dict.fromkeys(mem)); seen.update(mem); orbits.append(mem)
    print(f'target symmetries {len(stab)}; orbits {len(orbits)}', flush=True)
else:
    orbits = [[k] for k in keys]
# sample points
rng = np.random.default_rng(1); lo, hi = TV.min(0), TV.max(0)
S = rng.uniform(lo, hi, (400000, 3)); S = S[inside(S, -1e-9)][:40000]
print('sample points', len(S), flush=True)
rows, cols = [], []; vols = np.zeros(len(orbits))
for c, mem in enumerate(orbits):
    for key in mem:
        W = place[key]; E, _ = hull(W); vols[c] += shapes[key[0]][2]
        hit = np.where(np.all(S @ E[:, :3].T + E[:, 3] <= -1e-9, axis=1))[0]
        rows.extend(hit.tolist()); cols.extend([c] * len(hit))
from scipy.sparse import coo_matrix
M = coo_matrix((np.ones(len(rows), dtype=np.int8), (rows, cols)), shape=(len(S), len(orbits))).tocsr()

cons = [LinearConstraint(M, 0, 1), LinearConstraint(vols[None, :], TVOL - 1e-7, TVOL + 1e-7)]
t0 = time.time()
res = milp(c=np.ones(len(orbits)), constraints=cons, integrality=np.ones(len(orbits)), bounds=Bounds(0, 1), options={'time_limit': float(sys.argv[6]), 'disp': False})
print('MILP:', res.status, res.message, f'{time.time() - t0:.0f}s', flush=True)
if res.x is None: sys.exit()
chosen = [k for i in np.where(res.x > 0.5)[0] for k in orbits[i]]
# exact verification: pairwise overlap by separating axis (convex pieces)
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
W = [place[k] for k in chosen]
bad = sum(overlap(W[i], W[j]) for i in range(len(W)) for j in range(i))
tot = sum(shapes[k[0]][2] for k in chosen)
from collections import Counter
print('pieces:', dict(Counter(shapes[k[0]][0] for k in chosen)))
print(f'volume {tot:.12f} vs target {TVOL:.12f}; overlapping pairs: {bad}')
json.dump([{'name': shapes[k[0]][0], 'vertices': place[k].tolist()} for k in chosen], open(f'selfbuild-{TARGET}-{UP}.json', 'w'))
