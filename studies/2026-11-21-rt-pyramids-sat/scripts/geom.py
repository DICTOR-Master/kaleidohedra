"""Exact geometry in Z[phi] (numbers a + b*phi, a, b integers; phi = (1+sqrt5)/2) for the SAT tiling search.
Pieces are given in module coordinates n in Z^k; real 3D position = sum n_i E_i with E_i in Z[phi]^3.
Kinds: C6 (cube centre pyramids), RD (rhombic dodecahedron centre pyramids), TET (regular tetrahedron),
GR (acute golden rhombohedron, icosahedral module: positive control for the 6D machinery), RT (rhombic triacontahedron centre pyramids)."""
import itertools, math
import numpy as np
from scipy.spatial import ConvexHull
PHI = (1 + 5**.5)/2
# ---------- Z[phi] arithmetic on int64 arrays with a trailing axis of length 2 ----------
def zmul(x, y): return np.stack([x[..., 0]*y[..., 0] + x[..., 1]*y[..., 1], x[..., 0]*y[..., 1] + x[..., 1]*y[..., 0] + x[..., 1]*y[..., 1]], -1)
def zdot(u, d): return zmul(u, d).sum(-2)            # over the coordinate axis (second last)
def zcross(a, b):
    return np.stack([zmul(a[..., 1, :], b[..., 2, :]) - zmul(a[..., 2, :], b[..., 1, :]),
                     zmul(a[..., 2, :], b[..., 0, :]) - zmul(a[..., 0, :], b[..., 2, :]),
                     zmul(a[..., 0, :], b[..., 1, :]) - zmul(a[..., 1, :], b[..., 0, :])], -2)
def zsign(x):
    p = 2*x[..., 0] + x[..., 1]; q = x[..., 1]          # a + b phi = (p + q sqrt5)/2
    return np.where(p*p > 5*q*q, np.sign(p), np.sign(q))
def zf(x): return x[..., 0] + x[..., 1]*PHI
def zdet3(a, b, c): return zdot(zcross(a, b), c)
# ---------- kinds ----------
def ico_basis():
    z = {0: (0, 0), 1: (1, 0), -1: (-1, 0), 'p': (0, 1)}
    rows = [(0, 1, 'p'), (0, -1, 'p'), (1, 'p', 0), (-1, 'p', 0), ('p', 0, 1), ('p', 0, -1)]
    return np.array([[z[c] for c in r] for r in rows], dtype=np.int64)          # (6, 3, 2)
def int_basis(): return np.array([[[1 if i == j else 0, 0] for j in range(3)] for i in range(3)], dtype=np.int64)
def to3(n, E): return np.einsum('...i,icd->...cd', np.asarray(n, dtype=np.int64), E)
def kind_data(kind):
    """returns E (k,3,2) and templates: list of integer arrays (m, k); row 0 is the reference point (apex), placed at the class point"""
    if kind == 'C6':
        E = int_basis(); T = []
        for a in range(3):
            for s in (1, -1):
                vs = [v for v in itertools.product((1, -1), repeat=3) if v[a] == s]; T.append(np.array([(0, 0, 0)] + vs))
        return E, T
    if kind == 'RD':
        E = int_basis(); T = []
        for a, b in itertools.combinations(range(3), 2):
            c = 3 - a - b
            for s1, s2 in itertools.product((1, -1), repeat=2):
                v1 = [0, 0, 0]; v1[a] = 2*s1; v2 = [0, 0, 0]; v2[b] = 2*s2
                w = [[0, 0, 0], [0, 0, 0]]
                for t, sc in enumerate((1, -1)): w[t][a] = s1; w[t][b] = s2; w[t][c] = sc
                T.append(np.array([(0, 0, 0), v1, w[0], v2, w[1]]))
        return E, T
    if kind == 'TET':
        E = int_basis(); t = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)])
        return E, [np.vstack([[0, 0, 0], t]), np.vstack([[0, 0, 0], -t])]   # row 0 = centroid (reference, not a vertex)
    E = ico_basis()
    if kind == 'RT':
        T = []; Ef = zf(E)
        for i, j in itertools.combinations(range(6), 2):
            nrm = np.cross(Ef[i], Ef[j])
            for s in (1, -1):
                eps = [int(np.sign(s*(nrm @ Ef[l]))) if l not in (i, j) else 0 for l in range(6)]
                quad = []
                for a, b in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
                    v = list(eps); v[i] = a; v[j] = b; quad.append(v)
                T.append(np.array([[0]*6] + quad))
        return E, T
    if kind == 'GR':
        # acute golden rhombohedron spanned by 2e_0, 2e_2, 2e_4 (pairwise angles arccos(1/sqrt5) after sign choice) and its images under the icosahedral group
        G = ico_group_signed_perms(E); base = acute_triple(E)
        verts0 = np.array([[2*sum(s[t]*(1 if l == base[t][0] else 0)*base[t][1] for t in range(3)) for l in range(6)] for s in itertools.product((0, 1), repeat=3)])
        seen = {}; T = []
        for (perm, sg) in G:
            v = np.zeros_like(verts0)
            for l in range(6): v[:, perm[l]] = sg[l]*verts0[:, l]
            key = tuple(sorted(map(tuple, v - v.min(0))))  # translation class: compare after shift
            k2 = tuple(sorted(map(tuple, v - v[np.lexsort(v.T[::-1])][0])))
            if k2 in seen: continue
            seen[k2] = 1; v = v - v[np.lexsort(v.T[::-1])][0]  # reference = lexicographically smallest vertex at 0
            order = np.lexsort(v.T[::-1]); T.append(v[order])
        return E, T
    raise ValueError(kind)
def ico_group_signed_perms(E):
    """the 120 elements of the icosahedral group I_h as signed permutations of the six 5-fold vectors"""
    Ef = zf(E); gens = []
    c5 = math.cos(2*math.pi/5); s5 = math.sin(2*math.pi/5); ax = Ef[0]/np.linalg.norm(Ef[0])
    K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]]); R5 = np.eye(3) + s5*K + (1 - c5)*K@K
    R2 = np.diag([1., -1, -1]); M = np.diag([-1., 1, 1]); P3 = np.array([[0., 1, 0], [0, 0, 1], [1, 0, 0]])
    def sp(R):
        perm, sg = [0]*6, [0]*6
        for l in range(6):
            w = R @ Ef[l]
            for m in range(6):
                if np.allclose(w, Ef[m]): perm[l], sg[l] = m, 1
                elif np.allclose(w, -Ef[m]): perm[l], sg[l] = m, -1
        assert all(sg); return tuple(perm), tuple(sg)
    mats = [np.eye(3)]; frontier = [np.eye(3)]
    while frontier:
        nf = []
        for A in frontier:
            for g in (R5, R2, M, P3):
                B = g @ A
                if not any(np.allclose(B, C) for C in mats): mats.append(B); nf.append(B)
        frontier = nf
    assert len(mats) == 120, len(mats)
    return [sp(R) for R in mats]
def acute_triple(E):
    Ef = zf(E)
    for sb, sc in itertools.product((1, -1), repeat=2):
        a, b, c = Ef[0], sb*Ef[2], sc*Ef[4]
        if a @ b > 0 and a @ c > 0 and b @ c > 0: return [(0, 1), (2, sb), (4, sc)]
    raise RuntimeError
# ---------- per-template polytope data ----------
class Piece:
    def __init__(self, n, E, has_ref_vertex=True):
        self.n = n                                   # module coords, row 0 = reference
        X = to3(n, E)                                # (m, 3, 2)
        self.ref_is_vertex = has_ref_vertex
        self.V = X if has_ref_vertex else X[1:]      # polytope vertices
        Vf = zf(self.V); h = ConvexHull(Vf); cen = Vf.mean(0)
        normals, offs, seenp = [], [], []
        for simp, eq in zip(h.simplices, h.equations):
            if any(np.allclose(eq, q, atol=1e-9) for q in seenp): continue
            seenp.append(eq); a, b, c = self.V[simp[0]], self.V[simp[1]], self.V[simp[2]]
            nrm = zcross(b - a, c - a)
            if zf(zdot(nrm, a)) - zf(nrm) @ cen < 0: nrm = -nrm
            normals.append(nrm); offs.append(zdot(nrm, a))
        self.N = np.array(normals); self.off = np.array(offs)   # x in P <=> N.x <= off
        fn = {}
        for k, simp in enumerate(h.simplices):
            pl = next(i for i, q in enumerate(seenp) if np.allclose(h.equations[k], q, atol=1e-9))
            for i, j in itertools.combinations(sorted(simp), 2): fn.setdefault((i, j), set()).add(pl)
        self.edges = [(i, j) for (i, j), s in fn.items() if len(s) == 2]
        self.Edir = np.array([self.V[j] - self.V[i] for i, j in self.edges])
        # exact volume via cone from the centroid-free formula: sum over facets off * area / 3 is awkward; use tetrahedra from vertex 0
        vol = 0.0; self.volf = ConvexHull(Vf).volume
        self.centroid_num = self.V.sum(0); self.m = len(self.V)   # centroid = centroid_num / m (vertex average, interior point)
def pair_axes(A, B):
    """axes for the separating-axis test of A and B (face normals and edge-edge cross products) with exact interval data"""
    cand = list(A.N) + list(B.N) + [zcross(e, f) for e in A.Edir for f in B.Edir]
    axes, dirs = [], []
    for u in cand:
        uf = zf(u); nn = np.linalg.norm(uf)
        if nn < 1e-9: continue
        uf = uf/nn
        if any(abs(abs(uf @ d) - 1) < 1e-10 for d in dirs): continue
        dirs.append(uf); axes.append(u)
    U = np.array(axes)
    pa = zdot(U[:, None], A.V[None]); pb = zdot(U[:, None], B.V[None])   # (na, m, 2)
    fa, fb = zf(pa), zf(pb)
    ia_max = pa[np.arange(len(U)), fa.argmax(1)]; ia_min = pa[np.arange(len(U)), fa.argmin(1)]
    ib_max = pb[np.arange(len(U)), fb.argmax(1)]; ib_min = pb[np.arange(len(U)), fb.argmin(1)]
    return U, ia_max - ib_min, ia_min - ib_max      # overlap(d) <=> lo < U.d < hi on every axis
def overlap_many(U, hi, lo, D, tol=1e-9):
    """D: (n, 3, 2) offsets of B relative to A (B = template B + d). Returns bool array: interiors overlap (exact decision)."""
    if len(D) == 0: return np.zeros(0, bool)
    Uf, hif, lof = zf(U), zf(hi), zf(lo)
    f = zf(D) @ Uf.T                                   # (n, na)
    marg = np.minimum(hif[None] - f, f - lof[None])
    sure_sep = (marg < -tol).any(1); sure_ov = (marg > tol).all(1)
    res = sure_ov.copy(); amb = np.where(~sure_sep & ~sure_ov)[0]
    if len(amb):
        ud = zdot(U[None, :, :, :], D[amb][:, None, :, :])       # (na_amb, axes, 2)
        ok = (zsign(hi[None] - ud) > 0) & (zsign(ud - lo[None]) > 0)
        res[amb] = ok.all(1)
    return res
def contains_many(P, Y, scale, tol=1e-9):
    """Y: (n,3,2) points times `scale` (relative to P's reference point). True if Y/scale lies in the closed polytope P (exact)."""
    if len(Y) == 0: return np.zeros(0, bool)
    f = zf(Y) @ zf(P.N).T; offf = scale*zf(P.off)
    marg = offf[None] - f
    sure_out = (marg < -tol).any(1); sure_in = (marg > tol).all(1)
    res = sure_in.copy(); amb = np.where(~sure_out & ~sure_in)[0]
    if len(amb):
        val = scale*P.off[None] - zdot(P.N[None], Y[amb][:, None])
        res[amb] = (zsign(val) >= 0).all(1)
    return res
