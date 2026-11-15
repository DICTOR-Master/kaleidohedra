#!/usr/bin/env python3
"""Gorinto cells: exact geometry of the Platonic gorinto (five Platonic solids in one circumsphere, stacked face down on one axis)
and the separating-axis machinery used for every arrangement (columns, lattice fields, rings, the 3D mandala web).

Exact layer: sympy coordinates (nested radicals in Q(sqrt2, sqrt3, sqrt5, ...)).
Float layer: numpy float64 copies for searches; mpmath 50-digit copies for certification.

Overlap test (as in the EKP network): two convex pieces A and B + x overlap in their interiors iff x lies in the interior of the
Minkowski difference D = A - B. Every facet normal of D is a face normal of A, a face normal of B, or a cross product of an edge
direction of A with one of B, so D = {x : n.x <= h_D(n) for every candidate n}, h_D(n) = max_A n.a - min_B n.b. For a line
x(t) = p + t d the forbidden parameters (interior overlap) form one open interval, read off the candidate inequalities.
"""
import itertools, math
import numpy as np
import sympy as sp
from scipy.spatial import ConvexHull

S2, S3, S5 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)
PHI = (1 + S5) / 2
ORDER = ['earth', 'water', 'fire', 'wind', 'void']          # bottom to top (gorinto order)
SOLID = {'earth': 'cube', 'water': 'icosahedron', 'fire': 'tetrahedron', 'wind': 'octahedron', 'void': 'dodecahedron'}
KANJI = {'earth': '地', 'water': '水', 'fire': '火', 'wind': '風', 'void': '空'}
SEED = {'earth': 'a', 'water': 'va', 'fire': 'ra', 'wind': 'ha', 'void': 'kha'}


def std_vertices(name):
    if name == 'cube':
        return [sp.Matrix(v) for v in itertools.product((1, -1), repeat=3)]
    if name == 'tetrahedron':
        return [sp.Matrix(v) for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
    if name == 'octahedron':
        return [sp.Matrix(v) for k in range(3) for s in (1, -1) for v in [tuple(s if i == k else 0 for i in range(3))]]
    if name == 'icosahedron':
        out = []
        for a, b in itertools.product((1, -1), repeat=2):
            p = (0, a, b * PHI)
            for r in range(3): out.append(sp.Matrix(p[-r:] + p[:-r]) if r else sp.Matrix(p))
        return out
    if name == 'dodecahedron':
        out = [sp.Matrix(v) for v in itertools.product((1, -1), repeat=3)]
        for a, b in itertools.product((1, -1), repeat=2):
            p = (0, a / PHI, b * PHI)
            for r in range(3): out.append(sp.Matrix(p[-r:] + p[:-r]) if r else sp.Matrix(p))
        return out
    raise ValueError(name)


def faces_of(P):
    """faces of a convex polytope (float vertices), as cyclic index lists with outward normals (coplanar triangles merged)."""
    P = np.asarray(P, float); h = ConvexHull(P); planes = []
    for eq in h.equations:
        if not any(np.allclose(eq, q, atol=1e-7) for q in planes): planes.append(eq)
    faces = []
    for eq in planes:
        idx = [i for i in range(len(P)) if abs(P[i] @ eq[:3] + eq[3]) < 1e-7]
        c0 = P[idx].mean(0); n = eq[:3]; u = P[idx[0]] - c0; u /= np.linalg.norm(u); v = np.cross(n, u)
        idx.sort(key=lambda i: math.atan2((P[i] - c0) @ v, (P[i] - c0) @ u))
        faces.append(idx)
    return faces


def simp(e):
    e = sp.nsimplify(e) if e.is_number and e.is_rational else e
    return sp.radsimp(sp.sqrtdenest(sp.simplify(e)))


def face_down(name, align=0):
    """the solid of circumradius 1 resting on a face: that face horizontal at the bottom, its centre on the z-axis, the solid's centre
    on the z-axis; one bottom-face corner at azimuth `align` (degrees, from +x). Returns exact vertex list with bottom at z = 0."""
    V = std_vertices(name)
    Pf = np.array([[float(x) for x in v] for v in V])
    F = faces_of(Pf)
    # choose the face whose outward normal is closest to (-1, -2, -3) direction (any face works: all are equivalent by symmetry)
    tgt = np.array([-0.31, -0.52, -0.79])
    def fn(f): c = Pf[f].mean(0); return c / np.linalg.norm(c)
    f = max(F, key=lambda f: fn(f) @ tgt)
    fc = sum((V[i] for i in f), sp.zeros(3, 1)) / len(f)
    ez = -fc / sp.sqrt(fc.dot(fc))                      # down is the face direction
    w = V[f[0]] - fc
    ex = w / sp.sqrt(w.dot(w))
    ey = ez.cross(ex)
    R = sp.sqrt(V[0].dot(V[0]))
    a = sp.rad(align); ca, sa = sp.cos(a), sp.sin(a)
    out = []
    for v in V:
        x, y, z = v.dot(ex) / R, v.dot(ey) / R, v.dot(ez) / R
        X, Y = ca * x - sa * y, sa * x + ca * y
        out.append([X, Y, z])
    z0 = min(out, key=lambda p: float(p[2]))[2]
    out = [[simp(p[0]), simp(p[1]), simp(p[2] - z0)] for p in out]
    return out


def cube_face_down():
    s = 1 / S3
    return [[x * s, y * s, (z + 1) * s] for x, y, z in itertools.product((1, -1), repeat=3)]


def platonic_gorinto():
    """the Platonic gorinto: earth cube, water icosahedron, fire tetrahedron (apex up), wind octahedron, void dodecahedron; all of
    circumradius 1 (the five in one sphere, as Euclid XIII.18 compares them), centres on the z-axis, each resting on the one below.
    Alignment: icosahedron bottom corner at azimuth 0; tetrahedron base aligned with the icosahedron's top face (60 deg); octahedron
    bottom face aligned with the tetrahedron base (60 deg); dodecahedron bottom corner over an octahedron top corner (0 deg).
    Every piece is symmetric in the plane y = 0, so the whole cell is."""
    parts = [('earth', cube_face_down())]
    parts.append(('water', face_down('icosahedron', 0)))
    parts.append(('fire', face_down('tetrahedron', 60)))
    parts.append(('wind', face_down('octahedron', 60)))
    parts.append(('void', face_down('dodecahedron', 0)))
    z = sp.Integer(0); out = []
    for el, V in parts:
        hz = max(V, key=lambda p: float(p[2]))[2]
        V = [[p[0], p[1], simp(p[2] + z)] for p in V]
        out.append(dict(element=el, solid=SOLID[el], V=V, bottom=z, top=simp(z + hz), height=hz))
        z = simp(z + hz)
    return out, z


def exact_volume(solid):
    if solid == 'cube': a = 2 / S3; return a ** 3
    if solid == 'tetrahedron': a = sp.sqrt(sp.Rational(8, 3)); return a ** 3 / (6 * S2)
    if solid == 'octahedron': a = S2; return S2 / 3 * a ** 3
    if solid == 'icosahedron': a = 4 / sp.sqrt(10 + 2 * S5); return sp.Rational(5, 12) * (3 + S5) * a ** 3
    if solid == 'dodecahedron': a = 4 / (S3 * (1 + S5)); return (15 + 7 * S5) / 4 * a ** 3


# ---------------------------------------------------------------- float machinery
class Piece:
    def __init__(self, element, V, exact=None):
        self.element = element; self.V = np.asarray(V, float); self.exact = exact
        self.faces = faces_of(self.V)
        c = self.V.mean(0)
        self.normals = []
        for f in self.faces:
            n = np.cross(self.V[f[1]] - self.V[f[0]], self.V[f[2]] - self.V[f[0]]); n /= np.linalg.norm(n)
            if (self.V[f].mean(0) - c) @ n < 0: n = -n
            self.normals.append(n)
        self.normals = np.array(self.normals)
        E = set()
        for f in self.faces:
            for a, b in zip(f, f[1:] + f[:1]): E.add((min(a, b), max(a, b)))
        self.edges = sorted(E)
        dirs = []
        for a, b in self.edges:
            d = self.V[b] - self.V[a]; d /= np.linalg.norm(d)
            if not any(abs(abs(d @ e) - 1) < 1e-9 for e in dirs): dirs.append(d)
        self.dirs = np.array(dirs)

    def transformed(self, M, t=(0, 0, 0), exactM=None, exactt=None):
        ex = None
        if self.exact is not None and exactM is not None:
            ex = [list(exactM * sp.Matrix(p) + sp.Matrix(exactt)) for p in self.exact]
        return Piece(self.element, self.V @ np.asarray(M, float).T + np.asarray(t, float), ex)


def pair_normals(A, B):
    """candidate normals for D = A - B with labels (for exact reconstruction): ('fA', i), ('fB', j), ('e', i, j)."""
    N, L = [], []
    for i, n in enumerate(A.normals): N.append(n); L.append(('fA', i))
    for j, n in enumerate(B.normals): N.append(n); L.append(('fB', j))
    for i, a in enumerate(A.dirs):
        for j, b in enumerate(B.dirs):
            c = np.cross(a, b); nc = np.linalg.norm(c)
            if nc < 1e-9: continue
            N.append(c / nc); L.append(('e', i, j))
    N = np.array(N); N = np.vstack([N, -N]); L = L + [('-',) + l for l in L]
    h = (A.V @ N.T).max(0) - (B.V @ N.T).min(0)
    return N, h, L


class PairTable:
    """D = A - B for every pair of pieces of two gorinto cells (given orientations), cached."""
    def __init__(self, cellA, cellB):
        self.cells = (cellA, cellB)
        self.data = {}
        for i, A in enumerate(cellA):
            for j, B in enumerate(cellB):
                self.data[(i, j)] = pair_normals(A, B)

    def forbidden(self, P, Dd, eps=1e-12):
        """for lines x = P[k] + t Dd[k] (arrays M x 3), the open forbidden t-intervals for all piece pairs.
        Returns list of (lo, hi, k, i, j)."""
        out = []
        for (i, j), (N, h, L) in self.data.items():
            NP = P @ N.T; ND = Dd @ N.T; R = h[None, :] - NP
            with np.errstate(divide='ignore', invalid='ignore'):
                q = R / ND
            pos = ND > eps; neg = ND < -eps; zer = ~(pos | neg)
            hi = np.where(pos, q, np.inf).min(1); lo = np.where(neg, q, -np.inf).max(1)
            bad = (zer & (R <= eps)).any(1)
            ok = (lo < hi) & ~bad
            for k in np.nonzero(ok)[0]: out.append((lo[k], hi[k], int(k), i, j))
        return out


def min_feasible(intervals, t0=1e-9):
    """smallest t >= t0 outside every open interval."""
    t = t0; iv = sorted(intervals, key=lambda x: x[0]); changed = True
    while changed:
        changed = False
        for lo, hi, *rest in iv:
            if lo < t < hi - 1e-13:
                t = hi; changed = True
    return t


def binding(intervals, t, tol=1e-9):
    """intervals whose upper end is t (the contacts that stop t from being smaller)."""
    return [x for x in intervals if abs(x[1] - t) < tol]


def gap_at(PT, i, j, x):
    """max over candidate normals of n.x - h(n): > 0 separated, = 0 touching, < 0 overlapping; with the normal index."""
    N, h, L = PT.data[(i, j)]
    g = N @ x - h; k = int(np.argmax(g)); return g[k], k


def contact_kind(A, B, n, x, tol=1e-7):
    """contact between A and B + x across normal n: counts of A corners on the support plane and of B corners."""
    sa = A.V @ n; sb = (B.V + x) @ n
    ka = int((sa > sa.max() - tol).sum()); kb = int((sb < sb.min() + tol).sum())
    nm = {1: 'corner', 2: 'edge'}
    return f"{nm.get(ka, 'face')}-{nm.get(kb, 'face')}"


def cell_pieces(parts, zshift):
    """float Pieces of the Platonic gorinto with the axis midpoint at the origin (z shifted by -zshift)."""
    out = []
    for p in parts:
        V = np.array([[float(c) for c in v] for v in p['V']]); V[:, 2] -= float(zshift)
        ex = [[c[0], c[1], c[2] - zshift] for c in p['V']]
        out.append(Piece(p['element'], V, ex))
    return out


def rotz(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def rotz_exact(a):
    c, s = sp.cos(a), sp.sin(a); return sp.Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])


INVERT = np.diag([1.0, -1.0, -1.0])      # half turn about the x-axis through the axis midpoint (up -> down)
INVERT_EXACT = sp.diag(1, -1, -1)
