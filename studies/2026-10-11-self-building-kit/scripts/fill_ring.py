# Fill the inside of the side ring (2026-10-11): the outer layer (face_cover_sym.py, outer-layer-<target>-<n>.npy) is fixed; the
# space left is filled by kit pieces in the kit's turns, the solution kept symmetric under the ring's own turns (5-fold for the
# pentagonal pyramid, 3-fold for FUJI): every placement is chosen together with its turned copies. Exact cover is checked on
# sample points, then every pair of pieces is checked for overlap and the volumes are summed.
import sys, os, itertools, time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'selfbuild_sides.py')).read()
exec(src[:src.index('place = {}')])
LAYER = os.environ['LAYER']; ROUNDS_F = int(os.environ.get('FROUNDS', '1')); TLIM = float(os.environ.get('TLIM', '3600'))
fixed = [np.array(w, float) for w in np.load(LAYER, allow_pickle=True)]
N = 5 if TARGET == 'jsides' else 3
axis = apex - base.mean(0); axis /= np.linalg.norm(axis); c1 = base.mean(0)
def rot(k):
    an = 2 * np.pi * k / N; Kx = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(an) * Kx + (1 - np.cos(an)) * Kx @ Kx
Rk = [rot(k) for k in range(N)]
turn = lambda W, k: c1 + (W - c1) @ Rk[k].T
fixedE = [hull(W)[0] for W in fixed]; fixedBB = [(W.min(0), W.max(0)) for W in fixed]
vleft = TVOL - sum(hull(W)[1] for W in fixed)
print(f'outer layer: {len(fixed)} pieces; volume left to fill {vleft:.6f} ({vleft / TVOL:.1%} of the ring)', flush=True)
def clear_of_fixed(W):
    lo, hi = W.min(0), W.max(0)
    for (a, b), E, F in zip(fixedBB, fixedE, fixed):
        if np.any(hi < a + 1e-7) or np.any(lo > b - 1e-7): continue
        if any(np.all(W @ e[:3] + e[3] >= -1e-7) for e in E): continue
        if overlap(W, F): return False
    return True
P = np.unique(np.round(np.vstack([TV, HV] + fixed), 6), axis=0)
NB, DB = TE[:, :3], TE[:, 3]; NH, DH = HE[:, :3], HE[:, 3]
place = {}
for rnd in range(ROUNDS_F):
    new = []
    for si, (nm, V, vol) in enumerate(shapes):
        if vol > vleft + 1e-9: continue
        smax = (V @ NB.T).max(0); hmin = (V @ NH.T).min(0)
        T = (P[:, None, :] - V[None, :, :]).reshape(-1, 3)
        T = T[np.all(T @ NB.T + smax + DB <= 5e-6, axis=1)]
        for t in T:
            key = (si, tuple(np.round(t, 5)))
            if key in place: continue
            W = V + t
            if not (np.any((W @ NH.T).min(0) + DH >= -5e-6) or not overlap(W, HV)): continue
            if not clear_of_fixed(W): continue
            place[key] = W; new.append(W)
    if new:
        P = np.unique(np.round(np.vstack([P] + new), 6), axis=0)
    print(f'round {rnd}: {len(place)} placements, {len(P)} points', flush=True)
# orbits under the ring's turns
canon = lambda W: tuple(sorted(tuple(np.round(v, 4)) for v in W))
bykey = {canon(W): k for k, W in place.items()}
orbits, seen = [], set()
for k, W in place.items():
    if k in seen: continue
    mem = []
    for j in range(N):
        kk = bykey.get(canon(turn(W, j)))
        if kk is None: mem = None; break
        mem.append(kk)
    if mem is None: continue
    mem = list(dict.fromkeys(mem)); seen.update(mem); orbits.append(mem)
print(f'{len(orbits)} symmetric orbits of placements', flush=True)
rng = np.random.default_rng(5); lo, hi = TV.min(0), TV.max(0)
S = rng.uniform(lo, hi, (600000, 3)); S = S[inside(S, -1e-9) & ~in_hole(S, 1e-9)]
for E in fixedE: S = S[~np.all(S @ E[:, :3].T + E[:, 3] <= 1e-9, axis=1)]
S = S[:30000]; print('sample points', len(S), flush=True)
M = lil_matrix((len(S), len(orbits)), dtype=np.int8); vols = np.zeros(len(orbits))
for c, mem in enumerate(orbits):
    for k in mem:
        W = place[k]; E, v = hull(W); vols[c] += v
        hit = np.where(np.all(S @ E[:, :3].T + E[:, 3] <= -1e-9, axis=1))[0]
        for h in hit: M[h, c] = M[h, c] + 1
M = csr_matrix(M)
uncov = np.where(np.asarray(M.sum(1)).ravel() == 0)[0]
if len(uncov):
    U = S[uncov]; r = np.linalg.norm((U - c1) - np.outer((U - c1) @ axis, axis), axis=1); z = (U - c1) @ axis
    print(f'{len(uncov)} of {len(S)} sample points no placement can cover; their distance from the axis {r.min():.3f}-{r.max():.3f}, height {z.min():.3f}-{z.max():.3f} (band floor {-(np.linalg.norm(apex - c1)) / PHI:.3f}, top 0)', flush=True)
t0 = time.time()
res = milp(c=np.ones(len(orbits)), constraints=[LinearConstraint(M, 1, 1), LinearConstraint(vols[None, :], vleft - 1e-6, vleft + 1e-6)],
           integrality=np.ones(len(orbits)), bounds=Bounds(0, 1), options={'time_limit': TLIM})
print('MILP:', res.status, res.message, f'{time.time() - t0:.0f}s', flush=True)
if res.x is None: sys.exit()
chosen = [k for c in np.where(res.x > .5)[0] for k in orbits[c]]
Wc = [place[k] for k in chosen]
allW = fixed + Wc
bad = sum(overlap(allW[i], allW[j]) for i in range(len(allW)) for j in range(i)) + sum(overlap(w, HV) for w in allW)
tot = sum(hull(W)[1] for W in allW)
from collections import Counter
print('filling pieces:', dict(Counter(shapes[k[0]][0] for k in chosen)))
print(f'ring volume {TVOL:.12f}; pieces {tot:.12f}; overlapping pairs {bad}', flush=True)
np.save(f'ring-{TARGET}-{os.path.basename(LAYER)}', np.array(allW, dtype=object), allow_pickle=True)
