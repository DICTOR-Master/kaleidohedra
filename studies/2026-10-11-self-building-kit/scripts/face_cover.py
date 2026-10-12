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
def run_face(e, label):
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
    if not keys: print(f'  {label}: no piece can touch this face at all'); return
    rng = np.random.default_rng(3); lo, hi = to2(corners).min(0), to2(corners).max(0)
    S = rng.uniform(lo, hi, (60000, 2)); S = S[in2(S, -1e-9)][:6000]
    from scipy.spatial import ConvexHull
    M = np.zeros((len(S), len(keys)), dtype=np.int8)
    for k, key in enumerate(keys):
        F2 = to2(cand[key][1]); H = ConvexHull(F2)
        M[:, k] = np.all(S @ H.equations[:, :2].T + H.equations[:, 2] < -1e-9, axis=1)
    cons = [LinearConstraint(M, 1, 1)]; sols = []
    for it in range(MAXSOL):
        res = milp(c=np.ones(len(keys)), constraints=cons, integrality=np.ones(len(keys)), bounds=Bounds(0, 1), options={'time_limit': 300})
        if res.x is None: break
        ch = [keys[i] for i in np.where(res.x > .5)[0]]
        W = [cand[k][0] for k in ch]
        pairs = [(a, b) for a in range(len(W)) for b in range(a) if overlap(W[a], W[b])]
        names = sorted(shapes[k[0]][0] for k in ch)
        if not pairs:
            sols.append((names, 0)); print(f'  {label} COLLISION-FREE cover: {names}', flush=True)
            np.save(f'face-cover-{TARGET}-{label.replace(" ", "")}-{len(sols)}.npy', np.array([cand[k][0] for k in ch], dtype=object), allow_pickle=True)
            v = np.zeros(len(keys)); v[[keys.index(k) for k in ch]] = 1
            cons.append(LinearConstraint(v[None, :], -np.inf, len(ch) - 1)); continue
        # lazy cuts: the colliding pairs may not both be used
        for a, b in pairs:
            v = np.zeros(len(keys)); v[keys.index(ch[a])] = 1; v[keys.index(ch[b])] = 1
            cons.append(LinearConstraint(v[None, :], -np.inf, 1))
        if it % 10 == 0: print(f'  {label} try {it + 1}: {len(pairs)} colliding pair(s) forbidden', flush=True)
    print(f'  {label}: {len(sols)} collision-free cover(s) after {it + 1} solves' + ('' if res.x is not None else ' (no more covers exist: proved)'))
kinds = {}
for e in faces:
    on = TV[np.abs(TV @ e[:3] + e[3]) < 1e-6]
    sig = tuple(sorted(np.round([np.linalg.norm(a - b) for a, b in itertools.combinations(on, 2)], 4)))
    kinds.setdefault(sig, e)
for i, (sig, e) in enumerate(kinds.items()): run_face(e, f'face type {i}')
