#!/usr/bin/env python3
"""Shared tools for the echo-shapes study (15 Nov 2026).

Exact arithmetic: Q5 = numbers a + b*phi with a, b rational (Fractions); signs are decided exactly.
Tones: T_k(X) = (1/N^2) sum_{x,y in X} P_k(cos angle(x, y)) (Legendre P_k on S^2), the census's definition (studies/2026-11-15-law-giving-census).
  Computed at 60 digits (mpmath); a tone is called zero only if |T_k| < 1e-40, and zeros that the symmetry does not force are re-checked
  exactly (even k: P_k is a polynomial in c^2, and c^2 is exact in Q5 for point sets with coordinates in Q5).
Forced silences: degree k is silent for every point set with symmetry group G when G has no invariant harmonic of degree k
  (Molien count by the character formula: dim = (1/|G|) sum_g det(g)^k chi_k(rot(g)), chi_k(theta) = sin((2k+1)theta/2)/sin(theta/2)).
Dehn invariant: sum over edges of length (x) dihedral angle in R (x) R/(Q pi). Lengths are reduced to a Q-basis by PSLQ and each basis
  coefficient (an angle combination) is tested for being a rational multiple of pi by PSLQ (80 digits, coefficients <= 10^6).
  As in the census for H3, completeness of the PSLQ relations is not proved; 'nonzero' means no relation was found.
Translation tiling (convex): a convex polytope tiles R^3 by translations iff it is a parallelohedron, iff it is centrally symmetric,
  every face is centrally symmetric and every belt has 4 or 6 faces (Minkowski 1897, Venkov 1954, McMullen 1980). Checked on the hull."""
import itertools, math
from fractions import Fraction as Fr
import mpmath as mp
import numpy as np

mp.mp.dps = 60

# ---------- Q(sqrt5) as a + b*phi ----------
class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = q5(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = q5(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return q5(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = q5(o); return Q5(s.a*o.a + s.b*o.b, s.a*o.b + s.b*o.a + s.b*o.b)   # phi^2 = phi + 1
    __rmul__ = __mul__
    def conj(s): return Q5(s.a + s.b, -s.b)            # phi -> 1 - phi
    def norm(s): return s.a*s.a + s.a*s.b - s.b*s.b      # (a + b phi)(a + b phi')
    def inv(s): n = s.norm(); c = s.conj(); return Q5(c.a/n, c.b/n)
    def __truediv__(s, o): return s*q5(o).inv()
    def __rtruediv__(s, o): return q5(o)*s.inv()
    def iszero(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): o = q5(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        # sign of a + b phi = a + b/2 + (b/2) sqrt5
        x, y = s.a + s.b/2, s.b/2
        if y == 0: return (x > 0) - (x < 0)
        if x == 0: return (y > 0) - (y < 0)
        if (x > 0) == (y > 0): return 1 if x > 0 else -1
        d = x*x - 5*y*y          # compare |x| with |y| sqrt5
        return (1 if x > 0 else -1) if d > 0 else (1 if y > 0 else -1)
    def __lt__(s, o): return (s - o).sign() < 0
    def mpf(s): return mp.mpf(s.a.numerator)/s.a.denominator + mp.mpf(s.b.numerator)/s.b.denominator*mp.phi
    def __float__(s): return float(s.a) + float(s.b)*(1 + 5**0.5)/2
    def key(s): return (s.a, s.b)
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f'({s.a}{"+" if s.b >= 0 else "-"}{abs(s.b)}phi)'

def q5(x): return x if isinstance(x, Q5) else Q5(x, 0)
PHI = Q5(0, 1); IPHI = Q5(-1, 1)          # 1/phi = phi - 1
SQ5 = Q5(-1, 2)                          # sqrt5 = 2 phi - 1

def dot(u, v): return sum((x*y for x, y in zip(u, v)), Q5())
def vadd(u, v): return tuple(x + y for x, y in zip(u, v))
def vsub(u, v): return tuple(x - y for x, y in zip(u, v))
def vscale(c, u): return tuple(c*x for x in u)
def vkey(u): return tuple(x.key() for x in u)
def to_mp(u): return [x.mpf() for x in u]
def to_np(u): return np.array([float(x) for x in u])

def perms_even(t):
    out = []
    for p in itertools.permutations(range(len(t))):
        inv = sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])
        if inv % 2 == 0: out.append(tuple(t[i] for i in p))
    return out
def signs(t):
    idx = [i for i, x in enumerate(t) if not q5(x).iszero()]
    out = []
    for s in itertools.product((1, -1), repeat=len(idx)):
        u = list(t)
        for i, sg in zip(idx, s): u[i] = q5(u[i])*sg
        out.append(tuple(q5(x) for x in u))
    return out
def uniq(pts):
    seen = {};
    for p in pts: seen.setdefault(vkey(p), p)
    return list(seen.values())

# ---------- groups (as conjugacy data: list of (count, theta, det)) and Molien counts ----------
TAU = 2*math.pi
ROT = {
 'I': [(1, 0, 1), (15, math.pi, 1), (20, TAU/3, 1), (12, TAU/5, 1), (12, 2*TAU/5, 1)],
 'O': [(1, 0, 1), (8, TAU/3, 1), (3, math.pi, 1), (6, TAU/4, 1), (6, math.pi, 1)],
 'T': [(1, 0, 1), (8, TAU/3, 1), (3, math.pi, 1)],
}
def with_inversion(cl): return cl + [(c, th, -1) for c, th, d in cl]
GROUPS = {'I': ROT['I'], 'Ih': with_inversion(ROT['I']), 'O': ROT['O'], 'Oh': with_inversion(ROT['O']), 'T': ROT['T'],
          'Th': with_inversion(ROT['T']),
          # T_d: T plus -(the 6 half-turns about 2-fold edge axes) [mirrors] and -(the 6 quarter-turns) [S4]
          'Td': ROT['T'] + [(6, math.pi, -1), (6, TAU/4, -1)]}
def chi(k, th):
    if abs(th) < 1e-12: return 2*k + 1
    return math.sin((2*k + 1)*th/2)/math.sin(th/2)
def molien(gname, k):
    cl = GROUPS[gname]; n = sum(c for c, _, _ in cl)
    v = sum(c*(d**k)*chi(k, th) for c, th, d in cl)/n
    r = round(v); assert abs(v - r) < 1e-9, (gname, k, v); return r
def forced_silent(gname, kmax=30): return [k for k in range(1, kmax + 1) if molien(gname, k) == 0]

# ---------- tones ----------
def legendre_all(x, kmax):
    P = [mp.mpf(1), x]
    for k in range(1, kmax): P.append(((2*k + 1)*x*P[k] - k*P[k - 1])/(k + 1))
    return P[:kmax + 1]

def tones(points, kmax=30, weights=None):
    """points: list of exact tuples (Q5 entries) or mp vectors in R^d (any d; directions taken). Returns list T[0..kmax] (mp)."""
    V = [to_mp(p) if isinstance(p[0], Q5) else [mp.mpf(x) for x in p] for p in points]
    U = []
    for v in V:
        r = mp.sqrt(sum(x*x for x in v)); U.append([x/r for x in v])
    w = weights or [1]*len(U); W = sum(w)
    groups = {}
    for i in range(len(U)):
        for j in range(i, len(U)):
            c = sum(a*b for a, b in zip(U[i], U[j]))
            if c > 1: c = mp.mpf(1)
            if c < -1: c = mp.mpf(-1)
            key = mp.nstr(c, 40)
            m = w[i]*w[j]*(1 if i == j else 2)
            g = groups.get(key)
            if g is None: groups[key] = [c, m]
            else: g[1] += m
    T = [mp.mpf(0)]*(kmax + 1)
    for c, m in groups.values():
        P = legendre_all(c, kmax)
        for k in range(kmax + 1): T[k] += m*P[k]
    return [t/(W*W) for t in T]

def tones_exact_even(points, k, ip=None):
    """exact T_k * N^2 for even k on points with Q5 coordinates (or with an exact inner product ip(x, y) -> Q5)"""
    ip = ip or dot
    leg = legendre_coeffs(k)       # P_k(c) = sum_j a_j c^(2j)  (even k)
    tot = Q5(); n2 = [ip(p, p) for p in points]
    cnt = {}
    for i in range(len(points)):
        for j in range(i, len(points)):
            x = ip(points[i], points[j]); c2 = x*x/(n2[i]*n2[j]); key = c2.key()
            cnt[key] = cnt.get(key, 0) + (1 if i == j else 2)
    for key, m in cnt.items():
        c2 = Q5(*key); s = Q5(); pw = Q5(1)
        for a in leg: s = s + pw*Q5(a); pw = pw*c2
        tot = tot + s*m
    return tot

def legendre_coeffs(k):
    """coefficients a_j with P_k(x) = sum_j a_j x^(k - 2j)... returned as polynomial in x^2 for even k (ascending powers of x^2)"""
    assert k % 2 == 0
    # explicit: P_k(x) = 2^-k sum_m (-1)^m C(k,m) C(2k-2m,k) x^(k-2m)
    co = {}
    for m in range(k//2 + 1):
        co[k - 2*m] = Fr((-1)**m * math.comb(k, m) * math.comb(2*k - 2*m, k), 2**k)
    return [co.get(2*j, Fr(0)) for j in range(k//2 + 1)]

def tone_report(T, gname, tol=mp.mpf(10)**-40):
    forced = set(forced_silent(gname, len(T) - 1))
    zeros = [k for k in range(1, len(T)) if abs(T[k]) < tol]
    return {'forced_silent': sorted(forced), 'zero': zeros,
            'unforced_zero': [k for k in zeros if k not in forced],
            'forced_but_nonzero': [k for k in forced if k not in zeros],
            'first_tones': {k: float(T[k]) for k in range(1, len(T)) if k not in zeros and k <= 20}}

# ---------- 3D convex hull with merged faces ----------
def hull3(P, tol=1e-9):
    """P: (n,3) float array -> dict with vertices (indices), faces (ordered index cycles), normals, offsets"""
    from scipy.spatial import ConvexHull
    P = np.asarray(P, float); H = ConvexHull(P)
    planes = []
    for eq in H.equations:
        n, d = eq[:3], eq[3]
        for pl in planes:
            if np.linalg.norm(pl[0] - n) < 1e-7 and abs(pl[1] - d) < 1e-7: break
        else: planes.append((n, d))
    faces = []
    for n, d in planes:
        idx = [i for i in range(len(P)) if abs(P[i] @ n + d) < 1e-7*max(1, np.abs(P).max())]
        c = P[idx].mean(0); u = P[idx[0]] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        ang = [math.atan2((P[i] - c) @ v, (P[i] - c) @ u) for i in idx]
        cyc = [i for _, i in sorted(zip(ang, idx))]
        # drop points in the relative interior of an edge (collinear)
        keep = []
        for t in range(len(cyc)):
            a, b, cc = P[cyc[t - 1]], P[cyc[t]], P[cyc[(t + 1) % len(cyc)]]
            if np.linalg.norm(np.cross(b - a, cc - b)) > 1e-9*max(1, np.abs(P).max()): keep.append(cyc[t])
        faces.append(keep)
    verts = sorted({i for f in faces for i in f})
    return {'P': P, 'faces': faces, 'normals': [n for n, d in planes], 'offsets': [-d for n, d in planes], 'verts': verts}

def fvec(H):
    E = set()
    for f in H['faces']:
        for t in range(len(f)): E.add(frozenset((f[t - 1], f[t])))
    return len(H['verts']), len(E), len(H['faces'])

def face_census(H):
    from collections import Counter
    return dict(sorted(Counter(len(f) for f in H['faces']).items()))

NAMES = {  # (V, E, F, face census) -> name
 (4, 6, 4, ((3, 4),)): 'tetrahedron', (8, 12, 6, ((4, 6),)): 'cube or parallelepiped', (6, 12, 8, ((3, 8),)): 'octahedron',
 (20, 30, 12, ((5, 12),)): 'dodecahedron', (12, 30, 20, ((3, 20),)): 'icosahedron',
 (30, 60, 32, ((3, 20), (5, 12))): 'icosidodecahedron', (12, 24, 14, ((3, 8), (4, 6))): 'cuboctahedron',
 (60, 90, 32, ((5, 12), (6, 20))): 'truncated icosahedron', (60, 90, 32, ((3, 20), (10, 12))): 'truncated dodecahedron',
 (60, 120, 62, ((3, 20), (4, 30), (5, 12))): 'rhombicosidodecahedron', (24, 36, 14, ((4, 6), (6, 8))): 'truncated octahedron',
 (24, 36, 14, ((3, 8), (8, 6))): 'truncated cube', (24, 48, 26, ((3, 8), (4, 18))): 'rhombicuboctahedron',
 (12, 18, 8, ((3, 4), (6, 4))): 'truncated tetrahedron', (14, 24, 12, ((4, 12),)): 'rhombic dodecahedron',
 (32, 60, 30, ((4, 30),)): 'rhombic triacontahedron', (120, 180, 62, ((4, 30), (6, 20), (10, 12))): 'truncated icosidodecahedron',
 (48, 72, 26, ((4, 12), (6, 8), (8, 6))): 'truncated cuboctahedron', (8, 12, 6, ((4, 6),)): 'cube or parallelepiped',
 (62, 120, 60, ((4, 60),)): 'deltoidal or rhombic hexecontahedron (60 quadrilaterals)', (26, 48, 24, ((4, 24),)): 'deltoidal icositetrahedron (24 quadrilaterals)',
 (32, 90, 60, ((3, 60),)): 'pentakis dodecahedron or triakis icosahedron (60 triangles)',
 (92, 180, 90, ((4, 90),)): 'rhombic enneacontahedron', (22, 40, 20, ((4, 20),)): 'rhombic icosahedron',
 (32, 48, 18, ((4, 6), (6, 12))): 'chamfered cube type (6 squares, 12 hexagons)', (80, 120, 42, ((5, 12), (6, 30))): 'Goldberg GP(2,0) type (12 pentagons, 30 hexagons)',
 (42, 120, 80, ((3, 80),)): 'geodesic (2,0) type (80 triangles)', (5, 8, 5, ((3, 4), (4, 1))): 'square pyramid', (6, 9, 5, ((3, 2), (4, 3))): 'triangular prism',
}
def name_of(H):
    V, E, F = fvec(H); fc = tuple(face_census(H).items())
    return NAMES.get((V, E, F, fc), f'V{V} E{E} F{F} faces{dict(fc)}')

# ---------- Dehn invariant ----------
def dehn(Pmp, H, maxcoeff=10**6):
    """Pmp: list of mp 3-vectors (exact-derived), H: hull3 on the float copy. Returns dict(zero: bool, classes, basis_size, residual info)."""
    mp.mp.dps = 80
    P = [[mp.mpf(x) for x in p] for p in Pmp]
    def sub(a, b): return [x - y for x, y in zip(a, b)]
    def cross(a, b): return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]
    def dt(a, b): return sum(x*y for x, y in zip(a, b))
    def nrm(a): return mp.sqrt(dt(a, a))
    c = [sum(p[i] for p in P)/len(P) for i in range(3)]
    fn = []
    for f in H['faces']:
        n = [mp.mpf(0)]*3
        for t in range(len(f)):     # Newell normal, exact-derived
            a, b = P[f[t]], P[f[(t + 1) % len(f)]]
            n = [n[0] + (a[1] - b[1])*(a[2] + b[2]), n[1] + (a[2] - b[2])*(a[0] + b[0]), n[2] + (a[0] - b[0])*(a[1] + b[1])]
        m = nrm(n); n = [x/m for x in n]
        if dt(n, sub(P[f[0]], c)) < 0: n = [-x for x in n]
        fn.append(n)
    edges = {}
    for fi, f in enumerate(H['faces']):
        for t in range(len(f)): edges.setdefault(frozenset((f[t - 1], f[t])), []).append(fi)
    cls = {}
    for e, fs in edges.items():
        assert len(fs) == 2
        i, j = tuple(e); L = nrm(sub(P[i], P[j]))
        th = mp.pi - mp.acos(max(-1, min(1, dt(fn[fs[0]], fn[fs[1]]))))
        key = (mp.nstr(L, 30), mp.nstr(th, 30))
        if key in cls: cls[key][2] += 1
        else: cls[key] = [L, th, 1]
    C = list(cls.values())
    # Q-basis of lengths
    basis = []; coords = []
    for L, th, m in C:
        rel = mp.pslq([L] + basis, maxcoeff=maxcoeff, maxsteps=10**6) if basis else None
        if rel is not None and rel[0] != 0:
            coords.append([Fr(-r, rel[0]) for r in rel[1:]])
        else:
            basis.append(L); coords.append(None)
    nb = len(basis); full = []; j = 0
    for co in coords:
        if co is None: v = [Fr(0)]*nb; v[j] = Fr(1); j += 1
        else: v = list(co) + [Fr(0)]*(nb - len(co))
        full.append(v)
    # rebuild coordinates for entries found before later basis members were added: recompute properly
    full = []
    for L, th, m in C:
        rel = mp.pslq([L] + basis, maxcoeff=maxcoeff, maxsteps=10**6)
        full.append([Fr(-r, rel[0]) for r in rel[1:]])
    comps = []
    for jj in range(nb):
        Th = sum((mp.mpf(v[jj].numerator)/v[jj].denominator*m*th for (L, th, m), v in zip(C, full)), mp.mpf(0))
        rel = mp.pslq([Th, mp.pi], maxcoeff=10**8, maxsteps=10**6)
        comps.append({'theta_sum': mp.nstr(Th, 20), 'rational_pi': rel is not None and rel[0] != 0,
                      'ratio': (None if rel is None or rel[0] == 0 else f'{-rel[1]}/{rel[0]}')})
    mp.mp.dps = 60
    return {'zero': all(cp['rational_pi'] for cp in comps), 'edge_classes': len(C), 'length_basis': nb, 'components': comps}

# ---------- translation tiling test for convex polytopes (Venkov-McMullen) ----------
def parallelohedron(H, tol=1e-7):
    P = H['P']; c = P[H['verts']].mean(0); Q = P[H['verts']] - c
    S = {tuple(np.round(q, 6)) for q in Q}
    cs = all(tuple(np.round(-q, 6)) in S for q in Q)
    fcs = True
    for f in H['faces']:
        F = P[f]; fc = F.mean(0); Ff = {tuple(np.round(x - fc, 6)) for x in F}
        if not all(tuple(np.round(-(x - fc), 6)) in Ff for x in F): fcs = False; break
    # belts: for each edge direction, the faces containing an edge parallel to it
    dirs = []
    for f in H['faces']:
        for t in range(len(f)):
            d = P[f[t]] - P[f[t - 1]]; d = d/np.linalg.norm(d)
            if d[np.argmax(np.abs(d))] < 0: d = -d
            if not any(np.linalg.norm(d - e) < 1e-6 for e in dirs): dirs.append(d)
    belts = []
    for d in dirs:
        n = 0
        for f in H['faces']:
            if any(np.linalg.norm(np.cross(P[f[t]] - P[f[t - 1]], d)) < 1e-6*np.linalg.norm(P[f[t]] - P[f[t - 1]]) for t in range(len(f))): n += 1
        belts.append(n)
    ok = cs and fcs and len(H['faces']) <= 14 and all(b in (4, 6) for b in belts)
    return {'tiles_by_translation': bool(ok), 'centrally_symmetric': bool(cs), 'faces_centrally_symmetric': bool(fcs),
            'belt_sizes': sorted(set(belts))}

# ---------- 3D symmetry group order of a weighted point set ----------
def sym_group(X, w=None, tol=1e-6):
    """X: (n,3) floats. Returns (order, has_inversion, n_improper) of the group of orthogonal maps preserving the weighted set."""
    from scipy.spatial import cKDTree
    X = np.asarray(X, float); n = len(X); w = np.ones(n) if w is None else np.asarray(w, float)
    r = np.round(np.linalg.norm(X, axis=1), 6)
    tree = cKDTree(X)
    # choose three independent points from the smallest nonzero shell(s)
    order = sorted(range(n), key=lambda i: (r[i] == 0, sum(r == r[i]), r[i]))
    base = []
    for i in order:
        if r[i] == 0: continue
        cand = base + [i]
        if np.linalg.matrix_rank(X[cand], tol=1e-8) == len(cand): base = cand
        if len(base) == 3: break
    B = X[base]; Binv = np.linalg.inv(B)
    G = np.array([[X[a] @ X[b] for b in base] for a in base])
    pools = [[j for j in range(n) if abs(r[j] - r[i]) < 1e-6 and abs(w[j] - w[i]) < 1e-9] for i in base]
    found = []
    for j0 in pools[0]:
        for j1 in pools[1]:
            if abs(X[j0] @ X[j1] - G[0, 1]) > tol: continue
            for j2 in pools[2]:
                if abs(X[j0] @ X[j2] - G[0, 2]) > tol or abs(X[j1] @ X[j2] - G[1, 2]) > tol: continue
                M = Binv @ X[[j0, j1, j2]]           # rows: x -> x @ M maps base rows to targets
                if np.abs(M @ M.T - np.eye(3)).max() > 1e-6: continue
                Y = X @ M; d, idx = tree.query(Y)
                if d.max() < 1e-6 and np.allclose(w[idx], w): found.append(M)
    inv = any(np.allclose(M, -np.eye(3), atol=1e-6) for M in found)
    nimp = sum(1 for M in found if np.linalg.det(M) < 0)
    return len(found), inv, nimp

def group_name(order, inv, nimp):
    if order == 120: return 'Ih'
    if order == 60: return 'I'
    if order == 48: return 'Oh'
    if order == 24: return ('Th' if inv else ('Td' if nimp else 'O'))
    if order == 12: return 'T'
    return f'order{order}{"+inv" if inv else ""}'
