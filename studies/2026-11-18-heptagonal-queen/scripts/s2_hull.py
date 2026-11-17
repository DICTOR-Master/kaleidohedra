#!/usr/bin/env python3
"""Heptagonal Queen, part 2: hulls, face lattices, exact facet certificates, walls (18 Nov 2026).
Hull by qhull (floats) -> facets as vertex sets; every facet orbit representative is then certified exactly over the field
(normal from an exact rational null space; all points checked on one side). Face lattice by orbit representatives under
the exact symmetry group from part 1 (faces of a face F = maximal F n G over facets G). Euler's relation is checked.
Walls (method of the 600-cell walls study): the central hyperplane through each ridge (codimension-2 face) is a 'plate';
we test whether it is a mirror of the symmetry group and whether it is perpendicular to a corner.
Golden control: solid A in R^5 must have all 30 plates perpendicular to 600-cell corners (H4 mirrors), 10 of them S5 mirrors;
the ordinary orbit (phi^2,phi^2,phi^2,3/2,0) only 10 of 30.
Usage: s2_hull.py outdir"""
import sys, json, time, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hlib import *
import sympy as sp
from scipy.spatial import ConvexHull
OUTD = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}

def fl(K, X): return K.f(X)

def hull_facets(K, X):
    d = X.shape[1]; Xf = fl(K, X)
    Q, _ = np.linalg.qr((np.eye(d)[:d-1] - 1/d).T); Bs = Q[:, :d-1]
    Y = Xf @ Bs; H = ConvexHull(Y, qhull_options='Qt')
    eq = H.equations / np.linalg.norm(H.equations[:, :-1], axis=1)[:, None]
    seen = {}; facets = []; eqs = []
    for e in eq:
        k = tuple(np.round(e, 7))
        if k in seen: continue
        seen[k] = 1
        F = np.nonzero(np.abs(Y @ e[:-1] + e[-1]) < 1e-7)[0]
        facets.append(tuple(F.tolist())); eqs.append(np.concatenate([Bs @ e[:-1], [e[-1]]]))
    return facets, np.array(eqs)

def exact_normal(K, W, extra_ones=True):
    """n in K^d (as (d, n) ints) with <n, w> = 0 for every row w of W (and <n, 1> = 0); returns (n, nullity over Q)"""
    d, nn = W.shape[1], K.n
    rows = []
    Ws = list(W) + ([np.tile(K.el(1), (d, 1))] if extra_ones else [])
    for w in Ws:
        for k in range(nn):
            row = np.zeros((d, nn), dtype=object)
            for dd in range(d):
                for i in range(nn): row[dd, i] = int(sum(w[dd, j]*K.M[i, j, k] for j in range(nn)))
            rows.append(row.reshape(-1))
    Mx = sp.Matrix(rows); ns = Mx.nullspace()
    v = ns[0]; den = sp.ilcm(*[sp.fraction(c)[1] for c in v]); v = [int(c*den) for c in v]
    g = np.gcd.reduce([abs(c) for c in v if c]) if any(v) else 1
    return np.array(v, dtype=np.int64).reshape(d, nn)//g, len(ns)

def certify_facet(K, X, F):
    V = X[list(F)]; n, nul = exact_normal(K, V[1:] - V[0])
    vals = K.ip(X, np.broadcast_to(n, X.shape)); c = vals[F[0]]; diff = vals - c
    zero = np.all(diff == 0, axis=1); df = K.f(diff)
    ok = nul == K.n and set(np.nonzero(zero)[0].tolist()) == set(F) and (np.all(df[~zero] < -1e-9) or np.all(df[~zero] > 1e-9))
    return ok, n

def canon(perms, F):
    im = np.sort(perms[:, list(F)], axis=1); i = np.lexsort(im.T[::-1])[0]; m = im[i]
    return tuple(m.tolist()), int(np.all(im == m, axis=1).sum())

def lattice(K, X, perms, facets):
    N = len(X); D = np.linalg.matrix_rank(fl(K, X))  # dimension of the polytope
    Inc = np.zeros((len(facets), N), bool)
    for i, F in enumerate(facets): Inc[i, list(F)] = True
    G = len(perms); reps = {D - 1: {}}
    for F in facets:
        k, st = canon(perms, F)
        if k not in reps[D - 1]: reps[D - 1][k] = st
    for dim in range(D - 1, 0, -1):
        reps[dim - 1] = {}
        for F in reps[dim]:
            cnt = Inc[:, list(F)].sum(1); Fs = set(F)
            cands = {tuple(sorted(Fs & set(np.nonzero(Inc[j])[0].tolist()))) for j in np.nonzero((cnt >= dim) & (cnt < len(F)))[0]}
            cands = [set(c) for c in cands]
            maxi = [c for c in cands if not any(c < e for e in cands)]
            for c in maxi:
                k, st = canon(perms, tuple(sorted(c)))
                if k not in reps[dim - 1]: reps[dim - 1][k] = st
    fvec = [sum(G//st for st in reps[k].values()) for k in range(D)]
    return D, fvec, reps

def ridge_walls(K, X, perms, reps, D, corners):
    """for each ridge orbit: is its central plate an S_d mirror (x_i = x_j on all its corners)? perpendicular to a corner?"""
    G = len(perms); res = []
    for F, st in reps[D - 2].items():
        V = X[list(F)]; d = X.shape[1]
        mirror = any(np.all(V[:, i] == V[:, j]) for i in range(d) for j in range(i + 1, d))
        n, nul = exact_normal(K, V)
        cr = K.mul(corners[:, :, None], n[None, None]) - K.mul(corners[:, None, :], n[None, :, None])
        perp_corner = bool(np.any(np.all(cr == 0, axis=(1, 2, 3))))
        res.append(dict(n_corners=len(F), count=G//st, s_mirror=bool(mirror), perp_to_corner=perp_corner, nullity=nul))
    return res

# ---------------- golden control ----------------
K = GOLD; z, one, ph, ph2 = K.el(0), K.el(1), K.el(0, 1), K.el(1, 1)
A = centre(canon_orbit([z, ph, ph2, ph2, ph2], K)); B = centre(canon_orbit([z, one, one, ph2, ph2], K))
R = centre(canon_orbit([ph, z, z, z, -ph], K)); P600 = uniq_pts(np.concatenate([A, -A, B, -B, R]))
_, pA = isometry_group(K, A); pA = np.array(pA)
fA, _ = hull_facets(K, A); DA, fvA, rA = lattice(K, A, pA, fA)
C(fvA == [20, 40, 30, 10], f'control: golden truncated 5-cell A f-vector {fvA} (queens-construct: 20/40/30/10)')
wA = ridge_walls(K, A, pA, rA, DA, P600)
C(sum(w['count'] for w in wA if w['perp_to_corner']) == 30 and sum(w['count'] for w in wA if w['s_mirror']) == 10,
  f'control: all 30 plates of A perpendicular to a 600-cell corner (H4 mirrors), 10 of them S5 mirrors {wA}')
T = K.el(3)
Ob = centre(canon_orbit([z, T, 2*ph2, 2*ph2, 2*ph2], K)); _, pO = isometry_group(K, Ob); pO = np.array(pO)
fO, _ = hull_facets(K, Ob); DO, fvO, rO = lattice(K, Ob, pO, fO); wO = ridge_walls(K, Ob, pO, rO, DO, P600)
C(sum(w['count'] for w in wO if w['perp_to_corner']) == 10, f'control: ordinary orbit (phi^2 x3, 3/2, 0) has only 10 of {sum(w["count"] for w in wO)} plates on H4 mirrors')
out['gold'] = dict(A_fvec=fvA, A_walls=wA, ordinary_walls=wO)

# ---------------- heptagonal ----------------
K = HEPT; z = K.el(0); one = K.el(1); rho = K.el(0, 1); sig = K.el(-1, 0, 1)
rho2, sig2, rs = K.mul(rho, rho), K.mul(sig, sig), K.mul(rho, sig)
Ah = centre(canon_orbit([z, rho, rs, sig2, sig2, sig2, sig2], K)); Bh = centre(canon_orbit([z, one, one, rho2, rho2, sig2, sig2], K))
Qh = np.concatenate([Ah, -Ah, Bh, -Bh])
for name, X in [('A_h', Ah), ('B_h', Bh), ('Q_h', Qh)]:
    t1 = time.time()
    o, perms = isometry_group(K, X); perms = np.array(perms)
    facets, eqs = hull_facets(K, X)
    D, fv, reps = lattice(K, X, perms, facets)
    eul = sum((-1)**k*f for k, f in enumerate(fv))
    C(D == 6 and fv[0] == len(X) and fv[-1] == len(facets) and eul == 0, f'{name}: f-vector {fv} (Euler sum 0: {eul == 0}; facets from qhull {len(facets)}) ({time.time() - t1:.1f} s)')
    ftypes = []; allok = True
    for F, st in sorted(reps[D - 1].items(), key=lambda kv: -len(kv[0])):
        ok, n = certify_facet(K, X, F); allok &= ok
        nA = sum(1 for i in F if i < 420) if name == 'Q_h' else None
        sub = sum(1 for G_, s2 in reps[D - 2].items() if set(G_) <= set(F))
        cr = K.mul(Qh[:, :, None], n[None, None]) - K.mul(Qh[:, None, :], n[None, :, None])
        perp = int(np.nonzero(np.all(cr == 0, axis=(1, 2, 3)))[0][0]) if np.any(np.all(cr == 0, axis=(1, 2, 3))) else None
        mirror_normal = bool(sum(1 for c in n if np.any(c != 0)) == 2)
        ftypes.append(dict(corners=len(F), count=int(o//st), from_A_h_or_minus_A_h=nA, normal=n.tolist(), normal_float=np.round(K.f(n)/np.linalg.norm(K.f(n)), 6).tolist(),
                           normal_parallel_to_corner_of_Q_h=(None if perp is None else ('A_h' if perp < 420 else 'B_h') + ('+' if (perp % 420 < 210 if perp < 420 else (perp - 420) < 630) else '-')),
                           normal_is_root=mirror_normal))
    C(allok, f'{name}: every facet orbit representative certified exactly in Q(rho) ({len(ftypes)} facet orbits)')
    C(sum(f['count'] for f in ftypes) == fv[-1], f'{name}: facet orbit sizes sum to f5')
    walls = ridge_walls(K, X, perms, reps, D, Qh)
    nm = sum(w['count'] for w in walls if w['s_mirror']); npc = sum(w['count'] for w in walls if w['perp_to_corner']); nr = sum(w['count'] for w in walls)
    C(nr == fv[4], f'{name}: ridges {nr}: on S7 mirrors {nm}, plate perpendicular to a corner of Q_h {npc}, on neither {sum(w["count"] for w in walls if not (w["s_mirror"] or w["perp_to_corner"]))}')
    out[name] = dict(n=len(X), G=int(o), fvec=fv, facet_orbits=ftypes, ridge_orbits=walls, face_orbit_reps={int(k): len(v) for k, v in reps.items()})
    np.save(f'{OUTD}/{name}_facet_eqs.npy', eqs)
    for f in ftypes: print('   facet', {k: f[k] for k in ('corners', 'count', 'from_A_h_or_minus_A_h', 'normal_float', 'normal_parallel_to_corner_of_Q_h', 'normal_is_root')})
json.dump(out, open(f'{OUTD}/s2_hull.json', 'w'), indent=1, default=str)
C.final(); print(f'time {time.time() - t0:.1f} s')
