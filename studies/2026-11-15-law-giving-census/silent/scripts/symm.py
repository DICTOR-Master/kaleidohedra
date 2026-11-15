"""Symmetry checks (floats, used only to EXPLAIN over-determined points, never to claim a zero):
orbit size of a seed, the full orthogonal symmetry group order of a corner set (3D), sub-orbits under the index-2 subgroups of G
(kernels of sign characters) and their symmetry orders, and for 4D a list of candidate extra isometries (normalising G)."""
import itertools
import numpy as np

def frame(H):
    """orthonormal basis of span(W) (intrinsic coordinates), ambient -> intrinsic matrix"""
    Q, _ = np.linalg.qr(H.Wf.T)
    return Q[:, :H.r]

def orbit(H, c, eps=None):
    """float orbit of v = sum c_j w_j by reflections; with eps (sign per node) also returns the sub-orbit of ker(eps)"""
    v = np.asarray(c, float) @ H.Wf; v = v/np.linalg.norm(v)
    R = H.Rf
    def key(p): return tuple(np.round(p, 8) + 0.0)
    if eps is None:
        seen = {key(v): v}; fr = [v]
        while fr:
            nf = []
            for p in fr:
                for a in R:
                    q = p - 2*np.dot(p, a)*a; k = key(q)
                    if k not in seen: seen[k] = q; nf.append(q)
            fr = nf
        return np.array(list(seen.values()))
    seen = {(key(v), 1): v}; fr = [(v, 1)]
    while fr:
        nf = []
        for p, sg in fr:
            for a, e in zip(R, eps):
                q = p - 2*np.dot(p, a)*a; s2 = sg*e; k = (key(q), s2)
                if k not in seen: seen[k] = q; nf.append((q, s2))
        fr = nf
    sub = {k[0]: q for k, q in seen.items() if k[1] == 1}
    return np.array(list(sub.values()))

def orbit_size(H, c): return int(len(orbit(H, c)))

def sym_order(P, tol=1e-6):
    """order of the group of orthogonal maps permuting the finite set P (rows, intrinsic coords, common norm)"""
    m, d = P.shape
    keys = {tuple(np.round(p, 5) + 0.0) for p in P}
    def inset(Q): return all(tuple(np.round(q, 5) + 0.0) in keys for q in Q)
    # basis: greedy, nearest points first
    b = [0]; order = np.argsort(-P @ P[0])
    for j in order:
        if len(b) == d: break
        M = P[b + [j]]
        if np.linalg.matrix_rank(M, tol=1e-6) == len(b) + 1: b.append(int(j))
    if len(b) < d: return None
    B = P[b]; Gb = B @ B.T; Binv = np.linalg.inv(B)
    G = P @ P.T; count = 0
    def rec(chosen):
        nonlocal count
        i = len(chosen)
        if i == d:
            Qm = P[chosen]; L = Binv @ Qm   # row-vector convention: p -> p L
            if inset(P @ L): count += 1
            return
        for q in range(m):
            if abs(G[q, q] - Gb[i, i]) > tol: continue
            if all(abs(G[q, chosen[j]] - Gb[i, j]) < tol for j in range(i)): rec(chosen + [q])
    rec([]); return count

def sign_characters(H):
    """nontrivial homomorphisms W -> {+-1}: nodes joined by an odd-label edge share a sign"""
    import math
    r = H.r; out = []
    for eps in itertools.product((1, -1), repeat=r):
        if all(e == 1 for e in eps): continue
        ok = True
        for i in range(r):
            for j in range(i + 1, r):
                cth = -float(H.G[i][j])
                if cth > 1e-12:
                    m = round(math.pi/math.acos(min(1, cth)))
                    if m % 2 == 1 and eps[i] != eps[j]: ok = False
        if ok: out.append(eps)
    return out

def extra_isometries(H):
    """float ambient matrices of isometries normalising G that are not (necessarily) in G: -I, diagram automorphisms L_sigma,
    and the reflections that enlarge B4 -> F4, D4 -> B4"""
    n = H.Rf.shape[1]; out = {'-I': -np.eye(n)}
    A = H.Rf.T   # columns alpha_i
    if n > H.r:   # complete with the orthogonal complement (fixed)
        Q, _ = np.linalg.qr(np.hstack([A, np.ones((n, 1))])); comp = Q[:, H.r:]
    for s in H.aut:
        As = H.Rf[list(s)].T
        if n > H.r:
            M = np.hstack([A, comp]); Ms = np.hstack([As, comp])
        else: M, Ms = A, As
        out[f'L{tuple(s)}'] = Ms @ np.linalg.inv(M)
    def refl(u):
        u = np.asarray(u, float); u = u/np.linalg.norm(u); return np.eye(len(u)) - 2*np.outer(u, u)
    if H.name == 'B4': out['refl (1,1,1,1)/2 (F4)'] = refl([1, 1, 1, 1])
    if H.name == 'D4': out['refl e4 (B4)'] = refl([0, 0, 0, 1]); out['refl (1,1,1,1)/2 (F4)'] = refl([1, 1, 1, 1])
    if H.name == 'A3': out['refl e1 (B3)'] = refl([1, 0, 0])
    return out

def explain(H, c):
    """symmetry information for an over-determined point"""
    F = frame(H); P = orbit(H, c); info = {'orbit_size': len(P)}
    keys = {tuple(np.round(p, 6) + 0.0) for p in P}
    ext = []
    for nm, M in extra_isometries(H).items():
        Q = P @ M.T
        if all(tuple(np.round(q, 6) + 0.0) in keys for q in Q): ext.append(nm)
    info['extra_isometries_preserving'] = ext
    if H.r == 3:
        so = sym_order(P @ F); info['full_symmetry_order'] = so; info['G_order'] = H.order
        subs = []
        for eps in sign_characters(H):
            S = orbit(H, c, eps)
            if len(S) == len(P): continue
            o = sym_order(S @ F)
            subs.append({'character': list(eps), 'suborbit_size': len(S), 'suborbit_symmetry_order': o, 'subgroup_order': H.order//2,
                         'hidden': bool(o and o > H.order//2)})
        info['suborbits'] = subs
        info['explained'] = bool((so and so > H.order) or any(s['hidden'] for s in subs))
    else:
        subs = []
        info['explained'] = bool(ext)
    return info
