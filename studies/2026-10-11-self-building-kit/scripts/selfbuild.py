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
allV = np.array([v for p in L for v in p['vertices']]); O = allV.mean(0)
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
def hull(V):
    H = ConvexHull(V); return H.equations, H.volume
T = kit[TARGET]; c0 = T['V'].mean(0); TV = c0 + PHI ** UP * (T['V'] - c0)
TE, TVOL = hull(TV)
inside = lambda X, tol=1e-7: np.all(X @ TE[:, :3].T + TE[:, 3] <= tol, axis=-1)
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
# sample points
rng = np.random.default_rng(1); lo, hi = TV.min(0), TV.max(0)
S = rng.uniform(lo, hi, (400000, 3)); S = S[inside(S, -1e-9)][:40000]
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
