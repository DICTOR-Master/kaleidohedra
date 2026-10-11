# Bodhi seed gap (2026-10-12): its volume, 70.272181, equals 80 prolate + 20 oblate golden rhombohedra of edge 1 exactly. Test
# whether the gap really is tiled by them. Every face of every solid here (RT(phi^2), the 12 RT(1), RT(1/phi)) and of every golden
# rhombohedron is spanned by two of the six 5-fold vectors, so separating-axis tests need only their 15 cross products (exact).
# Candidates: rhombohedra with a corner on a corner of the solids (grown for ROUNDS rounds), inside the outer form, overlapping no
# solid; grouped into orbits of the 120 symmetries; exact cover of sample points by orbits (MILP) with the volume fixed.
import os, sys, itertools, time, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix
exec(open(__file__.replace('bodhi_rhombs.py', 'network_screen.py')).read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
ROUNDS = int(os.environ.get('ROUNDS', '2'))
V = ref['RT']; I = ref['I']
E6 = []
for v in I / np.linalg.norm(I, axis=1)[:, None]:
    if not any(abs(abs(v @ w) - 1) < 1e-9 for w in E6): E6.append(v)
E6 = np.array(E6); assert len(E6) == 6
el = min(np.linalg.norm(V[0] - w) for w in V[1:]); print('RT edge', round(el, 9))
AX = np.array([np.cross(a, b) / np.linalg.norm(np.cross(a, b)) for a, b in itertools.combinations(E6, 2)])
outer = V * PHI ** 2; centre = V / PHI
def faces(W):
    E = []
    for e in ConvexHull(W).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
FO = faces(outer); U5 = I / np.linalg.norm(I, axis=1)[:, None]; copies = []
for u in U5:
    t = min((-f[3] - (V @ f[:3]).max()) / (f[:3] @ u) for f in FO if f[:3] @ u > 1e-9); copies.append(V + t * u)
solids = copies + [centre]
SPR = np.array([[(W @ AX.T).min(0), (W @ AX.T).max(0)] for W in solids])      # (13, 2, 15)
OPR = np.array([(outer @ AX.T).min(0), (outer @ AX.T).max(0)])
shapes = []
SCALES = [float(eval(x)) for x in os.environ.get('SCALES', '1').split(',')]
for sc in SCALES:
    for a, b, c in itertools.combinations(E6, 3):
        base = np.array([i * a + j * b + k * c for i in (0, 1) for j in (0, 1) for k in (0, 1)]) * sc
        base -= base.mean(0); vol = abs(np.linalg.det(np.array([a, b, c]))) * sc ** 3
        shapes.append((('prolate' if abs(np.linalg.det(np.array([a, b, c]))) > 0.6 else 'oblate') + f'@{sc:.4f}', base, vol))
print('shapes', len(shapes))
P = np.unique(np.round(np.vstack([outer, centre] + copies), 7), axis=0)
place = {}
for rnd in range(ROUNDS):
    new = []
    for si, (nm, B, vol) in enumerate(shapes):
        T = np.unique(np.round((P[:, None, :] - B[None, :, :]).reshape(-1, 3), 7), axis=0)
        W = T[:, None, :] + B[None, :, :]; pr = W @ AX.T; lo, hi = pr.min(1), pr.max(1)       # (n, 15)
        ok = np.all(lo >= OPR[0] - 1e-7, axis=1) & np.all(hi <= OPR[1] + 1e-7, axis=1)
        for s in range(13):
            sep = np.any((hi <= SPR[s, 0] + 1e-7) | (lo >= SPR[s, 1] - 1e-7), axis=1); ok &= sep
        for t in T[ok]:
            key = (si, tuple(np.round(t, 6)))
            if key not in place: place[key] = t + B; new.append(t + B)
    if new: P = np.unique(np.round(np.vstack([P] + new), 7), axis=0)
    print(f'round {rnd}: {len(place)} placements, {len(P)} points', flush=True)
# orbits under the 120 symmetries
src = open(__file__.replace('bodhi_rhombs.py', 'lotus_analogs.py')).read()
exec(src[src.index('def _group'):src.index('GROUP = _group()')]); G = _group()
canon = lambda W: tuple(sorted(tuple(np.round(v, 5)) for v in W))
bykey = {canon(W): k for k, W in place.items()}; orbits, seen = [], set()
for k, W in place.items():
    if k in seen: continue
    mem = []
    for g in G:
        kk = bykey.get(canon(W @ g.T))
        if kk is None: mem = None; break
        mem.append(kk)
    if mem is None: continue
    mem = list(dict.fromkeys(mem)); seen.update(mem); orbits.append(mem)
print(f'{len(orbits)} symmetric orbits (sizes {sorted(set(len(o) for o in orbits))})', flush=True)
FS = [faces(W) for W in solids]
rng = np.random.default_rng(3); R = np.abs(outer).max(); S = rng.uniform(-R, R, (900000, 3))
S = S[np.all(S @ FO[:, :3].T + FO[:, 3] < -1e-9, axis=1)]
for F in FS: S = S[~np.all(S @ F[:, :3].T + F[:, 3] <= 1e-9, axis=1)]
S = S[:40000]; print('sample points', len(S), flush=True)
M = lil_matrix((len(S), len(orbits)), dtype=np.int8); vols = np.zeros(len(orbits)); SP = S @ AX.T
for c, mem in enumerate(orbits):
    for k in mem:
        W = place[k]; vols[c] += shapes[k[0]][2]; pr = W @ AX.T
        # inside a rhombohedron: inside its 6 face slabs (faces spanned by pairs of its edges)
        Fw = faces(W); hit = np.where(np.all(S @ Fw[:, :3].T + Fw[:, 3] < -1e-9, axis=1))[0]
        for h in hit: M[h, c] += 1
M = csr_matrix(M); unc = int((np.asarray(M.sum(1)).ravel() == 0).sum()); print('sample points no candidate covers:', unc, flush=True)
gap = ConvexHull(outer).volume - 12 * ConvexHull(V).volume - ConvexHull(centre).volume
t0 = time.time()
res = milp(c=np.ones(len(orbits)), constraints=[LinearConstraint(M, 1, 1), LinearConstraint(vols[None, :], gap - 1e-6, gap + 1e-6)],
           integrality=np.ones(len(orbits)), bounds=Bounds(0, 1), options={'time_limit': 3000})
print('MILP:', res.status, res.message, f'{time.time() - t0:.0f}s', flush=True)
if res.x is None: sys.exit()
chosen = [k for c in np.where(res.x > .5)[0] for k in orbits[c]]; Wc = [place[k] for k in chosen]
bad = 0
for i in range(len(Wc)):
    for j in range(i):
        a, b = Wc[i] @ AX.T, Wc[j] @ AX.T
        if not np.any((a.max(0) <= b.min(0) + 1e-7) | (b.max(0) <= a.min(0) + 1e-7)): bad += 1
from collections import Counter
print('pieces:', dict(Counter(shapes[k[0]][0] for k in chosen)), f'volume {sum(shapes[k[0]][2] for k in chosen):.9f} of gap {gap:.9f}; overlapping pairs {bad}')
np.save('bodhi-rhombs.npy', np.array(Wc))
