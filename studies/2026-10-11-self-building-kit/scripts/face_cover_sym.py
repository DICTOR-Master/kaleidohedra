# Outside-in, all tilings (2026-10-11): tile one sloping face of the side ring directly with faces of kit pieces that sit inside the
# ring in the kit's own (Lotus-frame) turns, at sizes phi^-1 .. phi^-K. Every exact cover of the face is listed (no-good cuts), and
# each is checked for 3D overlaps between the pieces behind it. None found = this face cannot be the outside of kit pieces.
import sys, os, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'selfbuild_sides.py')).read()
exec(src[:src.index('place = {}')])
MAXSOL = int(os.environ.get('MAXSOL', '400')); RND = int(os.environ.get('RND', '3'))
axis = (apex - base.mean(0)); axis /= np.linalg.norm(axis)
faces = [e for e in np.unique(np.round(TE, 9), axis=0) if abs(abs(e[:3] @ axis) - 1) > 1e-6]
def prep_face(e, label):
    n, d0 = e[:3], e[3]
    corners = TV[np.abs(TV @ n + d0) < 1e-6]
    c = corners.mean(0); ex = corners[0] - c; ex /= np.linalg.norm(ex); ey = np.cross(n, ex)
    to2 = lambda P: np.c_[(P - c) @ ex, (P - c) @ ey]
    C2 = to2(corners); ang = np.arctan2(C2[:, 1] - C2[:, 1].mean(), C2[:, 0] - C2[:, 0].mean()); C2 = C2[np.argsort(ang)]
    edges2 = []
    for i in range(len(C2)):
        a, b = C2[i], C2[(i + 1) % len(C2)]; m = np.array([b[1] - a[1], a[0] - b[0]]); m /= np.linalg.norm(m)
        if m @ (C2.mean(0) - a) > 0: m = -m
        edges2.append((m, -m @ a))
    in2 = lambda X, tol=1e-6: np.all(np.stack([X @ m + dd for m, dd in edges2], -1) <= tol, -1)
    P = corners.copy(); cand = {}
    for r in range(RND):
        new = []
        for si, (nm, V, vol) in enumerate(shapes):
            for p in P:
                for j in range(len(V)):
                    W = V + (p - V[j]); dist = W @ n + d0
                    if dist.max() > 1e-6: continue
                    onp = W[np.abs(dist) < 1e-6]
                    if len(onp) < 3 or not in2(to2(onp)).all(): continue
                    key = (si, tuple(np.round(p - V[j], 6)))
                    if key in cand: continue
                    if not inside(W, 1e-6).all() or not clear_of_hole(W): continue
                    cand[key] = (W, onp); new.append(onp)
        if new: P = np.unique(np.round(np.vstack([P] + new), 7), axis=0)
        print(f'  {label} round {r}: {len(cand)} pieces with a face on it, {len(P)} points', flush=True)
    keys = list(cand)
    if not keys: print(f'  {label}: no piece can touch this face at all'); return [], {}, None
    rng = np.random.default_rng(3); lo, hi = to2(corners).min(0), to2(corners).max(0)
    S = rng.uniform(lo, hi, (60000, 2)); S = S[in2(S, -1e-9)][:6000]
    from scipy.spatial import ConvexHull
    M = np.zeros((len(S), len(keys)), dtype=np.int8)
    for k, key in enumerate(keys):
        F2 = to2(cand[key][1]); H = ConvexHull(F2)
        M[:, k] = np.all(S @ H.equations[:, :2].T + H.equations[:, 2] < -1e-9, axis=1)
    return keys, cand, M

kinds = {}
for e in faces:
    on = TV[np.abs(TV @ e[:3] + e[3]) < 1e-6]
    sig = tuple(sorted(np.round([np.linalg.norm(a - b) for a, b in itertools.combinations(on, 2)], 4)))
    kinds.setdefault(sig, e)
N = 5 if TARGET == 'jsides' else 3
c1 = base.mean(0)
def rot(k):
    an = 2 * np.pi * k / N; Kx = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(an) * Kx + (1 - np.cos(an)) * Kx @ Kx
Rk = [rot(k) for k in range(N)]
turn = lambda W, k: c1 + (W - c1) @ Rk[k].T
for k in range(N):
    Y = turn(TV, k); assert all(np.min(np.linalg.norm(TV - y, axis=1)) < 1e-6 for y in Y)
prep = [prep_face(e, f'face type {i}') for i, (sig, e) in enumerate(kinds.items())]
if any(p[2] is None for p in prep): print('a face type has no candidates: stop'); sys.exit()
allkeys = [(t, k) for t, p in enumerate(prep) for k in p[0]]; idx = {kk: i for i, kk in enumerate(allkeys)}
W_of = lambda tk: prep[tk[0]][1][tk[1]][0]
from scipy.sparse import block_diag, csr_matrix
Mbig = block_diag([csr_matrix(p[2]) for p in prep]).tocsr()
cons = [LinearConstraint(Mbig, 1, 1)]; nvar = len(allkeys); found = 0
for it in range(MAXSOL):
    res = milp(c=np.ones(nvar), constraints=cons, integrality=np.ones(nvar), bounds=Bounds(0, 1), options={'time_limit': 600})
    if res.x is None: print(f'NO symmetric collision-free outer layer exists (proved for these candidates) after {it} solves'); break
    ch = [allkeys[i] for i in np.where(res.x > .5)[0]]
    cuts = []
    for a_, b_ in itertools.combinations_with_replacement(range(len(ch)), 2):
        for k in range(N):
            if a_ == b_ and k == 0: continue
            if k == 0 and overlap(W_of(ch[a_]), W_of(ch[b_])): cuts.append((a_, b_))
            elif k and overlap(W_of(ch[a_]), turn(W_of(ch[b_]), k)): cuts.append((a_, b_))
    if not cuts:
        names = sorted(shapes[k[0]][0] for _, k in ch)
        found += 1; print(f'SYMMETRIC OUTER LAYER {found}: per face set {names}', flush=True)
        L = [turn(W_of(c), k) for k in range(N) for c in ch]
        np.save(f'outer-layer-{TARGET}-{found}.npy', np.array(L, dtype=object), allow_pickle=True)
        vf = sum(hull(W)[1] for W in L); print(f'   {len(L)} pieces, volume {vf:.6f} of ring {TVOL:.6f} ({vf / TVOL:.1%}); left inside {TVOL - vf:.6f}', flush=True)
        v = np.zeros(nvar); v[[idx[c] for c in ch]] = 1; cons.append(LinearConstraint(v[None, :], -np.inf, len(ch) - 1))
        if found >= 5: break
        continue
    for a_, b_ in set(cuts):
        v = np.zeros(nvar); v[idx[ch[a_]]] += 1; v[idx[ch[b_]]] += 1
        cons.append(LinearConstraint(v[None, :], -np.inf, 1))
    if it % 20 == 0: print(f'  try {it + 1}: {len(set(cuts))} clashing pair(s) forbidden', flush=True)
