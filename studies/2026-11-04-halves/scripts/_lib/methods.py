# Shared research methods (DICTO 2026-11-04: code-sharing map for the Concordance). One copy of each core method, each with a calibration
# in test_methods.py that must pass before a study uses it. Use:  sys.path.insert(0, os.path.expanduser('~/k-research/studies/_lib')); import methods as M
# Methods: point sets (perms, even_perms, cyclic), polar sweep sections (sweep_cube_octa, halfspace_poly), harmonic fingerprint in 3D and 4D
# (Q3d, W6, Q4d), separating-axis overlap of convex pieces (overlap), rotations/reflections about a line (rot_line, refl_perp, refl_plane),
# forced-sector candidates (sector_candidates; uses the true wedge middle from the two face normals — the 4 Nov bug fix), check ledger (Ledger).
import itertools, math
import numpy as np

PHI = (1 + 5 ** .5) / 2

# ---- point sets
def perms(v, signs=True):
    out = set()
    for p in itertools.permutations(v):
        for s in (itertools.product((1, -1), repeat=len(v)) if signs else [(1,) * len(v)]):
            out.add(tuple(a * b for a, b in zip(p, s)))
    return np.array(sorted(out), float)

def cyclic(v):
    """cyclic permutations of a 3-vector with all sign changes"""
    out = set()
    for k in range(3):
        p = v[k:] + v[:k]
        for s in itertools.product((1, -1), repeat=3): out.add(tuple(a * b for a, b in zip(p, s)))
    return np.array(sorted(out), float)

def even_perms(v):
    out = set()
    n = len(v)
    for p in itertools.permutations(range(n)):
        if np.linalg.det(np.eye(n)[list(p)]) > 0:
            for s in itertools.product((1, -1), repeat=n): out.add(tuple(s[i] * v[p[i]] for i in range(n)))
    return np.array(sorted(out), float)

# ---- polytopes from half-spaces; the cube–octahedron sweep
def halfspace_poly(planes, inner):
    """planes: list of (normal, offset) meaning n·x <= d; inner: a point inside. Returns the corner array."""
    from scipy.spatial import HalfspaceIntersection
    H = np.array([[*n, -d] for n, d in planes], float)
    return np.unique(np.round(HalfspaceIntersection(H, np.asarray(inner, float)).intersections, 11), axis=0)

def sweep_cube_octa(mu):
    """corners of S(mu) = C ∩ mu C*, C = [-1,1]^3, 1 <= mu <= 3 (#90, #91)"""
    return perms((1, mu - 1, 0)) if mu <= 2 else perms((1, 1, mu - 2))

# ---- harmonic fingerprint (#94)
def Q3d(P, l, centre=None):
    from scipy.special import sph_harm_y
    P = np.asarray(P, float); P = P - (P.mean(0) if centre is None else np.asarray(centre))
    u = P / np.linalg.norm(P, axis=1)[:, None]; th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0])
    q = np.array([sph_harm_y(l, m, th, ph).mean() for m in range(-l, l + 1)])
    return math.sqrt(4 * math.pi / (2 * l + 1) * float(np.sum(np.abs(q) ** 2)))

_W3J = {}
def W6(P, centre=None):
    from scipy.special import sph_harm_y
    from sympy.physics.wigner import wigner_3j
    P = np.asarray(P, float); P = P - (P.mean(0) if centre is None else np.asarray(centre))
    u = P / np.linalg.norm(P, axis=1)[:, None]; th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0])
    q = np.array([sph_harm_y(6, m, th, ph).mean() for m in range(-6, 7)]); s = float(np.sum(np.abs(q) ** 2))
    if 6 not in _W3J: _W3J[6] = [(a, b, -a - b, float(wigner_3j(6, 6, 6, a, b, -a - b))) for a in range(-6, 7) for b in range(-6, 7) if abs(a + b) <= 6]
    return float(np.real(sum(c * q[a + 6] * q[b + 6] * q[d + 6] for a, b, d, c in _W3J[6]))) / s ** 1.5

def Q4d(P, l):  # NOTE: returns sqrt of a mean; rounding noise ~1e-5 at true zeros, so test silence with Q < 1e-4
    """4D fingerprint: corner directions on S^3, zonal harmonic = Chebyshev U_l"""
    P = np.asarray(P, float); u = P / np.linalg.norm(P, axis=1)[:, None]; t = np.clip(u @ u.T, -1, 1)
    th = np.arccos(t); s = np.sin(th)
    U = np.where(np.abs(s) > 1e-12, np.sin((l + 1) * th) / np.where(np.abs(s) > 1e-12, s, 1), np.where(t > 0, l + 1, (-1) ** l * (l + 1)))
    return math.sqrt(max(float(U.mean()) / (l + 1), 0.0))

# ---- convex pieces
def _hull(t):
    from scipy.spatial import ConvexHull
    h = ConvexHull(t); return h, [eq[:3] for eq in h.equations], [t[j] - t[i] for s in h.simplices for i, j in itertools.combinations(s, 2)]

def overlap(a, b, eps=1e-9):
    """depth of interior overlap of two convex pieces (0.0 if they only touch or are apart); separating-axis test"""
    _, aa, ea = _hull(a); _, ab, eb = _hull(b); cand = aa + ab
    for x in ea:
        for y in eb:
            c = np.cross(x, y); n = np.linalg.norm(c)
            if n > 1e-12: cand.append(c / n)
    best = 1e9
    for n in cand:
        pa, pb = a @ n, b @ n; d = min(pa.max() - pb.min(), pb.max() - pa.min())
        if d <= eps: return 0.0
        best = min(best, d)
    return best

def rot_line(P, X, Y, ang):
    k = (Y - X) / np.linalg.norm(Y - X); c, s = math.cos(ang), math.sin(ang)
    return np.array([X + (p - X) * c + np.cross(k, p - X) * s + k * (k @ (p - X)) * (1 - c) for p in P])

def refl_perp(P, X, Y):
    m = (X + Y) / 2; k = (Y - X) / np.linalg.norm(Y - X); return np.array([p - 2 * ((p - m) @ k) * k for p in P])

def refl_plane(P, X, n):
    n = n / np.linalg.norm(n); return np.array([p - 2 * ((p - X) @ n) * n for p in P])

def sector_candidates(t, i, j, dih):
    """pieces congruent to t that have segment t[i]t[j] as the same kind of edge and fill the k-th other sector (k = 1..m-1, m = 2π/dih);
    four variants per sector (identity, swap ends, swap faces, both). The sector middle comes from t's two face normals at the edge."""
    X, Y = t[i], t[j]; m = int(round(2 * math.pi / dih)); axis = (Y - X) / np.linalg.norm(Y - X)
    h, _, _ = _hull(t); ns = []
    for sm, eq in zip(h.simplices, h.equations):
        if i in sm and j in sm and not any(np.allclose(eq[:3], q) for q in ns): ns.append(eq[:3])
    r0 = -(ns[0] + ns[1]); r0 = r0 - axis * (r0 @ axis); r0 /= np.linalg.norm(r0)
    out = []
    for k in range(1, m):
        base = rot_line(t, X, Y, k * dih)
        mid = rot_line(np.array([X + r0]), X, Y, k * dih)[0] - X; npl = np.cross(axis, mid)
        vs = [base, refl_perp(base, X, Y), refl_plane(base, X, npl), refl_perp(refl_plane(base, X, npl), X, Y)]
        uniq = []
        for v in vs:
            if not any(same_piece(v, q) for q in uniq): uniq.append(v)
        out.append(uniq)
    return out

def same_piece(a, b, tol=1e-7):
    return len(a) == len(b) and np.allclose(a[0], b[0], atol=tol) and all(np.min(np.linalg.norm(b - p, axis=1)) < tol for p in a)

# ---- check ledger
class Ledger:
    def __init__(self): self.rows = []
    def check(self, name, ok, detail=''):
        self.rows.append((name, bool(ok), str(detail))); print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail != '' else ''))
        return ok
    def summary(self):
        p = sum(r[1] for r in self.rows); f = len(self.rows) - p; print(f'{p} PASS {f} FAIL'); return f == 0
