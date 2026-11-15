"""The five universes: 600-cell (120), 120-cell (600), 24-cell (24), snub 24-cell (96), E8 roots (240, 8D icosian model).
H4 is built from quaternions: x -> l x rbar and x -> l xbar rbar (l, r unit icosians); its elements are labelled (l, r, star)."""
import numpy as np
from hz_core import *

def h4_ambient():
    X = cell600()
    keyidx = {k: i for i, k in enumerate(keyrows(X))}
    def perm_of(Y): return np.array([keyidx[k] for k in keyrows(Y)], dtype=np.int32)
    Lp = np.array([perm_of(qmul_pts(np.broadcast_to(X[l], X.shape), X)) for l in range(120)])
    Xc = qconj_pts(X)
    Rp = np.array([perm_of(qmul_pts(X, np.broadcast_to(Xc[r], X.shape))) for r in range(120)])   # x -> x rbar
    St = perm_of(Xc)                                                                               # x -> xbar
    idn = np.arange(120)
    seen = {}; perms = []; labels = []
    for s in (0, 1):
        pre = St if s else idn
        for l in range(120):
            for r in range(120):
                p = Lp[l][Rp[r][pre]]
                kb = p.tobytes()
                if kb in seen: continue
                seen[kb] = len(perms); perms.append(p); labels.append((l, r, s))
    perms = np.array(perms, dtype=np.int32)
    assert len(perms) == 14400
    basis = span_basis(to_float(X))
    A = Ambient(perms, basis)
    sig = galois_perm(X)                      # Galois conjugation (after a fixed signed coordinate permutation) as a permutation
    return X, A, np.array(labels), Lp, Rp, St, sig

def u600(X, kmax=20):
    return Universe('600-cell', X, 4, to_float(X) / 2, kmax=kmax)

def cell120_from(X, A):
    """120-cell: one vertex per tetrahedral cell of the 600-cell, at phi^-2 * (sum of the 4 corners) (rational squared radius)."""
    a, b = ip_pairs(X, X)
    adj = (a == 0) & (b == 2)            # 4<x,y> = 2 phi  <=> <x,y> = phi/2 (edge)
    nb = [set(np.nonzero(adj[i])[0]) for i in range(120)]
    tets = set()
    for i in range(120):
        for j in nb[i]:
            for k in nb[i] & nb[j]:
                for l in nb[i] & nb[j] & nb[k]:
                    tets.add(tuple(sorted((i, j, k, l))))
    tets = sorted(tets); assert len(tets) == 600
    T = np.array(tets)
    S = X[T].sum(1)                       # (600, 4, 2): 2*sum
    # multiply by phi^-2 = 2 - phi = (2, -1)
    a_, b_ = S[..., 0], S[..., 1]; c, d = 2, -1
    Y = np.stack([a_ * c + b_ * d, a_ * d + b_ * c + b_ * d], -1)
    # lift the ambient perms to the cells
    key = lambda M: ((M[:, 0] * 120 + M[:, 1]) * 120 + M[:, 2]) * 120 + M[:, 3]
    tk = key(T); o = np.argsort(tk); tks = tk[o]
    lift = np.empty((A.n, 600), dtype=np.int32)
    for g in range(A.n):
        im = np.sort(A.P[g][T], axis=1); kk = key(im)
        pos = np.searchsorted(tks, kk); assert (tks[pos] == kk).all()
        lift[g] = o[pos]
    return Y, lift

def galois_perm(Y):
    """Double Vision: sigma (sqrt5 -> -sqrt5 on coordinates) followed by the first signed coordinate permutation tau (a rational
    orthogonal map, so <tau sigma x, tau sigma y> = sigma<x,y>) that maps the set onto itself. Any two such differ by a symmetry."""
    ki = {k: i for i, k in enumerate(keyrows(Y))}
    Z = galois_points(Y)
    def det_sp(p, sg):
        M = np.zeros((4, 4))
        for i in range(4): M[p[i], i] = sg[i]
        return round(np.linalg.det(M))
    cands = [(p, sg) for p in itertools.permutations(range(4)) for sg in itertools.product((1, -1), repeat=4)]
    # prefer quaternion automorphisms (fix the real axis, rotate the pure part): then tau*sigma is a ring automorphism of H
    cands.sort(key=lambda c: (not (c[0][0] == 0 and c[1][0] == 1 and det_sp(*c) == 1), c))
    for p, sg in cands:
        if True:
            W = Z[:, list(p), :] * np.array(sg)[None, :, None]
            ks = keyrows(W)
            if all(k in ki for k in ks):
                GALOIS_TAU[id(Y)] = (p, sg)
                return np.array([ki[k] for k in ks], dtype=np.int32)
    return None
GALOIS_TAU = {}

def e8_from(X):
    """E8 roots as icosians: the 120 units and phi^-1 times the units, with the rational form B(x,y) = a + b when <x,y> = a + b sqrt5
    (Conway-Sloane SPLAG ch. 8). Stored scale 2: B_stored = 4 B."""
    a_, b_ = X[..., 0], X[..., 1]
    Y = np.stack([b_ - a_, a_], -1)                      # phi^-1 * x  (phi - 1 = (-1, 1))
    P8 = np.concatenate([X, Y])
    def ipB(U, V):
        a, b = ip_pairs(U, V)        # <u,v> = a + b phi = (a + b/2) + (b/2) sqrt5 -> B = a + b
        return a + b, np.zeros_like(a)
    l1, l2 = (1 + 1 / 5 ** 0.5) / 2, (1 - 1 / 5 ** 0.5) / 2
    Yf = np.hstack([np.sqrt(l1) * to_float(P8) / 2, np.sqrt(l2) * to_float_conj(P8) / 2])
    return P8, ipB, Yf

def e8_reflections(P8, ipB):
    """root reflections x -> x - 2 B(x,r)/B(r,r) r as permutations of the 240 roots (exact)."""
    Bs, _ = ipB(P8, P8)                 # stored scale: B(r,r) -> 4
    assert (Bs.diagonal() == 4).all()
    vals = set(np.unique(Bs).tolist()); assert vals <= {-4, -2, 0, 2, 4}, vals
    ki = {k: i for i, k in enumerate(keyrows(P8))}
    refl = []
    for r in range(240):
        coef = Bs[:, r] // 2            # 2 B(x,r)/B(r,r) = 2*(Bs/4) = Bs/2
        Z = P8 - coef[:, None, None] * P8[r][None]
        refl.append(np.array([ki[k] for k in keyrows(Z)], dtype=np.int32))
    return np.array(refl)
