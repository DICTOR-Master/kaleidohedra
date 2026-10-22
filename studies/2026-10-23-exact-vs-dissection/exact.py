# Exact geometry for the exact-vs-dissection study (DICTO, 2026-10-23) · DICTO · dictospheres.com
# Numbers live in one quadratic field Q(sqrt d) at a time: a + b*sqrt(d), a and b rational (fractions.Fraction).
# Every test below is exact (no floating point decides anything); floats are only printed or used to size a search box.
from fractions import Fraction as Fr
from functools import cmp_to_key
import itertools, math, re


class QF:
    """a + b*sqrt(d) with a, b rational. d = None for a plain rational (b = 0)."""
    __slots__ = ('a', 'b', 'd')

    def __init__(self, a=0, b=0, d=None):
        self.a = Fr(a); self.b = Fr(b)
        self.d = d if self.b != 0 else None
        if self.b != 0 and d is None:
            raise ValueError('irrational part needs d')

    @staticmethod
    def _d(x, y):
        if x.d is None: return y.d
        if y.d is None or y.d == x.d: return x.d
        raise ValueError(f'mixed fields sqrt({x.d}) and sqrt({y.d})')

    def __add__(s, o):
        o = q(o); return QF(s.a + o.a, s.b + o.b, QF._d(s, o))
    __radd__ = __add__

    def __neg__(s): return QF(-s.a, -s.b, s.d)

    def __sub__(s, o): return s + (-q(o))

    def __rsub__(s, o): return q(o) - s

    def __mul__(s, o):
        o = q(o); d = QF._d(s, o)
        return QF(s.a * o.a + (s.b * o.b * d if d else 0), s.a * o.b + s.b * o.a, d)
    __rmul__ = __mul__

    def conj(s): return QF(s.a, -s.b, s.d)

    def norm(s): return s.a * s.a - (s.b * s.b * s.d if s.d else 0)

    def __truediv__(s, o):
        o = q(o); n = o.norm()
        if n == 0: raise ZeroDivisionError
        r = s * o.conj(); return QF(r.a / n, r.b / n, r.d)

    def __rtruediv__(s, o): return q(o) / s

    def __eq__(s, o):
        o = q(o); return s.a == o.a and s.b == o.b and (s.b == 0 or s.d == o.d)

    def __hash__(s): return hash((s.a, s.b))

    def sign(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        big = a * a > b * b * s.d       # |a| vs |b| sqrt d (never equal: d is not a square)
        return (1 if a > 0 else -1) if big else (1 if b > 0 else -1)

    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0

    def __float__(s): return float(s.a) + (float(s.b) * math.sqrt(s.d) if s.d else 0.0)

    def is_int(s): return s.b == 0 and s.a.denominator == 1

    def __repr__(s): return to_str(s)


def q(x):
    if isinstance(x, QF): return x
    return QF(x)


def surd(d, b=1, a=0): return QF(a, b, d)


R2, R3, R5 = surd(2), surd(3), surd(5)
PHI = (1 + R5) / 2

_RX = re.compile(r'^(-?\d+(?:/\d+)?)([+-])(\d+(?:/\d+)?)\*sqrt\((\d+)\)$')


def to_str(x):
    x = q(x)
    if x.b == 0: return str(x.a)
    return f"{x.a}{'+' if x.b > 0 else '-'}{abs(x.b)}*sqrt({x.d})"


def parse(s):
    s = s.replace(' ', '')
    m = _RX.match(s)
    if m:
        a, sg, b, d = m.groups(); b = Fr(b) * (1 if sg == '+' else -1)
        return QF(Fr(a), b, int(d))
    return QF(Fr(s))


# ---- vectors and matrices (tuples of QF; matrices as lists of rows) ----
def V(*xs): return tuple(q(x) for x in xs)
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def sc(u, k): return tuple(a * k for a in u)
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def det3(a, b, c): return dot(a, cross(b, c))
def iszero(u): return all(x == 0 for x in u)
def vsum(vs):
    s = (q(0), q(0), q(0))
    for v in vs: s = add(s, v)
    return s
def fl(u): return [float(x) for x in u]
def vstr(u): return [to_str(x) for x in u]
def vparse(u): return tuple(parse(x) for x in u)
def matvec(M, v): return tuple(dot(r, v) for r in M)
def transpose(M): return [tuple(M[j][i] for j in range(3)) for i in range(3)]
def matmul(A, B): return [tuple(dot(A[i], tuple(B[k][j] for k in range(3))) for j in range(3)) for i in range(3)]
def cols(vs): return [tuple(v[i] for v in vs) for i in range(3)]  # matrix whose columns are vs
def mdet(M): return det3(*M)


def minv(M):
    d = mdet(M)
    c = lambda r1, c1, r2, c2: M[r1][c1] * M[r2][c2] - M[r1][c2] * M[r2][c1]
    adj = [(c(1, 1, 2, 2), -c(0, 1, 2, 2), c(0, 1, 1, 2)),
           (-c(1, 0, 2, 2), c(0, 0, 2, 2), -c(0, 0, 1, 2)),
           (c(1, 0, 2, 1), -c(0, 0, 2, 1), c(0, 0, 1, 1))]
    return [tuple(x / d for x in r) for r in adj]


def solve_coords(basis, v):
    """Coordinates of v in the basis (three vectors)."""
    return matvec(minv(cols(basis)), v)


# ---- convex hull (exact, brute force; fine for up to ~40 points) ----
def _canon(n):
    """Oriented key: n scaled so its first nonzero entry is +1 or -1 (positive multiples share a key)."""
    for x in n:
        if x != 0: return tuple(y / abs_q(x) for y in n)


def _line(n):
    """Unoriented key: n scaled so its first nonzero entry is 1 (n and -n share a key)."""
    for x in n:
        if x != 0: return tuple(y / x for y in n)


def hull(points):
    """Exact convex hull of a point set in general 3D position. Returns (verts, faces) with faces as CCW (outward) index
    lists of the true corners only (points inside faces or on edges are dropped)."""
    P = list(dict.fromkeys(points))
    planes = {}
    for i, j, k in itertools.combinations(range(len(P)), 3):
        n = cross(sub(P[j], P[i]), sub(P[k], P[i]))
        if iszero(n): continue
        h = dot(n, P[i]); s = [(dot(n, p) - h).sign() for p in P]
        if all(x <= 0 for x in s): pass
        elif all(x >= 0 for x in s): n = tuple(-x for x in n); h = -h
        else: continue
        planes[_canon(n)] = (n, h)
    faces = []
    for key, (n, h) in planes.items():
        on = [p for p in P if dot(n, p) == h]
        faces.append(_order(on, n))
    corners = sorted({p for f in faces for p in f}, key=lambda p: tuple(float(x) for x in p))
    idx = {p: i for i, p in enumerate(corners)}
    return corners, [[idx[p] for p in f] for f in faces]


def _order(pts, n):
    """Order coplanar points CCW about normal n and keep only the true corners."""
    c = sc(vsum(pts), Fr(1, len(pts)))
    r = sub(pts[0], c)
    def grp(p):
        x = sub(p, c); s = dot(n, cross(r, x)).sign()
        if s > 0: return 1
        if s < 0: return 3
        return 0 if dot(r, x).sign() > 0 else 2
    def cmp(p1, p2):
        g1, g2 = grp(p1), grp(p2)
        if g1 != g2: return g1 - g2
        if g1 in (0, 2): return 0
        return -dot(n, cross(sub(p1, c), sub(p2, c))).sign()
    ring = sorted(pts, key=cmp_to_key(cmp))
    out = []
    m = len(ring)
    for i in range(m):          # drop points lying on a polygon edge (collinear with neighbours)
        a, b, cc = ring[i - 1], ring[i], ring[(i + 1) % m]
        if not iszero(cross(sub(b, a), sub(cc, b))): out.append(b)
    return out


# ---- zonotopes ----
def zonotope(gens):
    """The zonotope sum of segments [-g/2, g/2], exactly: (verts, faces CCW outward, info). Generators must be
    pairwise non-parallel. info['zones'] lists, for each face plane, the generator indices lying in it."""
    gens = list(gens)
    for i, j in itertools.combinations(range(len(gens)), 2):
        if iszero(cross(gens[i], gens[j])): raise ValueError(f'generators {i} and {j} are parallel')
    planes = {}
    for i, j in itertools.combinations(range(len(gens)), 2):
        n = cross(gens[i], gens[j]); key = _line(n)
        if key not in planes: planes[key] = (n, sorted(k for k in range(len(gens)) if dot(n, gens[k]) == 0))
    pts, faces, zones = [], [], []
    for n, Z in planes.values():
        for sg in (1, -1):
            N = sc(n, sg)
            c = sc(vsum(sc(gens[k], dot(N, gens[k]).sign()) for k in range(len(gens)) if k not in Z), Fr(1, 2))
            e = gens[Z[0]]; f = cross(N, e)
            ds = []
            for k in Z:
                d = gens[k]; t = dot(f, d).sign()
                if t < 0 or (t == 0 and dot(e, d).sign() < 0): d = sc(d, -1)
                ds.append(d)
            ds.sort(key=cmp_to_key(lambda a, b: -dot(N, cross(a, b)).sign()))
            p = sub(c, sc(vsum(ds), Fr(1, 2))); ring = [p]
            for d in ds[:-1]: p = add(p, d); ring.append(p)
            p = add(p, ds[-1]); ring.append(p)
            for d in ds[:-1]: p = sub(p, d); ring.append(p)
            faces.append(ring); zones.append(Z)
    corners = sorted({p for f in faces for p in f}, key=lambda p: tuple(float(x) for x in p))
    idx = {p: i for i, p in enumerate(corners)}
    return corners, [[idx[p] for p in f] for f in faces], {'zones': zones}


def zonotope_volume(gens):
    return sum((abs_q(det3(*t)) for t in itertools.combinations(gens, 3)), q(0))


def abs_q(x): return x if x.sign() >= 0 else -x


def dependency(h):
    """For four vectors in general position: the coefficients mu with sum mu_i h_i = 0, normalised mu_4 = 1."""
    # mu_1 h1 + mu_2 h2 + mu_3 h3 = -h4
    m = solve_coords(h[:3], sc(h[3], -1))
    return list(m) + [q(1)]


def positive_signs(h):
    """Signs eps_i with sum mu_i eps_i h_i = 0 for some mu_i > 0 (the RD-type sign choice), and those mu."""
    mu = dependency(h)
    eps = [x.sign() for x in mu]
    return [sc(v, e) for v, e in zip(h, eps)], [abs_q(x) for x in mu]


def circumcentre(P):
    A = [sc(sub(P[i], P[0]), 2) for i in (1, 2, 3)]
    b = [dot(P[i], P[i]) - dot(P[0], P[0]) for i in (1, 2, 3)]
    return matvec(minv(A), tuple(b))


# ---- checks on a polyhedron given as (verts, faces) ----
def face_normal(V_, f):
    a, b, c = V_[f[0]], V_[f[1]], V_[f[2]]
    return cross(sub(b, a), sub(c, b))


def checks(V_, F_):
    """Exact checks: closed (every edge in exactly two faces, opposite directions), planar faces, strictly convex
    CCW-outward faces, convex solid, Euler. Returns dict of results and the f-vector; raises nothing."""
    res = {}
    de = {}
    for fi, f in enumerate(F_):
        for i in range(len(f)): de.setdefault((f[i], f[(i + 1) % len(f)]), []).append(fi)
    res['closed'] = all(len(v) == 1 for v in de.values()) and all((b, a) in de for (a, b) in de)
    edges = {frozenset(e) for e in de}
    planar = True; outward = True; convex = True
    cen = sc(vsum(V_), Fr(1, len(V_)))
    for f in F_:
        n = face_normal(V_, f); h = dot(n, V_[f[0]])
        if any(dot(n, V_[i]) != h for i in f): planar = False
        for i in range(len(f)):
            a, b, c = V_[f[i - 1]], V_[f[i]], V_[f[(i + 1) % len(f)]]
            if dot(cross(sub(b, a), sub(c, b)), n).sign() <= 0: outward = False
        if (dot(n, V_[f[0]]) - dot(n, cen)).sign() <= 0: outward = False
        if any((dot(n, V_[i]) - h).sign() >= 0 for i in range(len(V_)) if i not in f): convex = False
    res['planar'] = planar; res['outward_wound'] = outward; res['convex'] = convex
    res['used_all_vertices'] = sorted({i for f in F_ for i in f}) == list(range(len(V_)))
    fv = (len(V_), len(edges), len(F_)); res['euler'] = fv[0] - fv[1] + fv[2] == 2
    return res, fv


def volume(V_, F_):
    v = q(0)
    for f in F_:
        for m in range(1, len(f) - 1): v = v + det3(V_[f[0]], V_[f[m]], V_[f[m + 1]])
    return v / 6


def edge_lengths2(V_, F_):
    return sorted({dot(sub(V_[f[i]], V_[f[(i + 1) % len(f)]]), sub(V_[f[i]], V_[f[(i + 1) % len(f)]])) for f in F_ for i in range(len(f))}, key=float)


def corner_cos2(a, b):
    """cos^2 of the angle between a and b, and the sign of cos."""
    d = dot(a, b); return d * d / (dot(a, a) * dot(b, b)), d.sign()


SPECIAL = {Fr(1, 4): 60, Fr(1, 2): 45, Fr(0): 90, Fr(1, 9): 70.5288, Fr(1, 5): 63.4349}  # cos^2 values (rational ones)


def face_kind(V_, f):
    """Name a face exactly: square, rhombus <acute angle>, regular hexagon, hexagon <corners>, parallelogram ..."""
    P = [V_[i] for i in f]; n = len(P)
    L = [dot(sub(P[(i + 1) % n], P[i]), sub(P[(i + 1) % n], P[i])) for i in range(n)]
    eq = all(x == L[0] for x in L)
    angs = []
    for i in range(n):
        a = sub(P[i - 1], P[i]); b = sub(P[(i + 1) % n], P[i])
        c2, s = corner_cos2(a, b)
        ang = math.degrees(math.acos(max(-1, min(1, (1 if s >= 0 else -1) * math.sqrt(float(c2))))))
        angs.append((c2, s, ang))
    if n == 4:
        acute = min(a[2] for a in angs)
        if all(a[0] == 0 for a in angs): return 'square' if eq else 'rectangle'
        if eq:
            c2 = [a for a in angs if a[1] > 0][0][0]
            if c2 == Fr(1, 4): return 'rhombus 60'
            if c2 == Fr(1, 5): return 'golden rhombus'      # cos^2 = 1/5: diagonals in the golden ratio
            if c2 == Fr(1, 9): return 'rhombus 70.53'
            return f'rhombus {acute:.2f}'
        return f'parallelogram {acute:.2f}'
    if n == 6:
        if eq and all(a[0] == Fr(1, 4) and a[1] < 0 for a in angs): return 'regular hexagon'
        cs = sorted({round(a[2], 2) for a in angs}, reverse=True)
        return ('equilateral ' if eq else '') + 'hexagon ' + '/'.join(f'{a:g}' for a in sorted([round(x[2], 2) for x in angs[:3]], reverse=True))
    return f'{n}-gon'


def face_census(V_, F_):
    out = {}
    for f in F_:
        k = face_kind(V_, f); out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


# ---- symmetry (exact point group of a vertex set centred at the origin) ----
def symmetry(V_):
    Vs = set(V_)
    norms = [dot(v, v) for v in V_]
    # three independent vertices
    base = None
    for a, b, c in itertools.combinations(range(len(V_)), 3):
        if det3(V_[a], V_[b], V_[c]) != 0: base = (a, b, c); break
    a, b, c = base
    Binv = minv(cols([V_[a], V_[b], V_[c]]))
    G = []
    cand = lambda i: [j for j in range(len(V_)) if norms[j] == norms[i]]
    for ja in cand(a):
        for jb in cand(b):
            if dot(V_[ja], V_[jb]) != dot(V_[a], V_[b]): continue
            for jc in cand(c):
                if dot(V_[ja], V_[jc]) != dot(V_[a], V_[c]) or dot(V_[jb], V_[jc]) != dot(V_[b], V_[c]): continue
                M = matmul(cols([V_[ja], V_[jb], V_[jc]]), Binv)
                MtM = matmul(transpose(M), M)
                if any(MtM[i][j] != (1 if i == j else 0) for i in range(3) for j in range(3)): continue
                if all(matvec(M, v) in Vs for v in V_): G.append(M)
    return G


def group_name(G):
    n = len(G)
    dets = [mdet(M) for M in G]; rot = [M for M, d in zip(G, dets) if d == 1]
    inv = any(all(M[i][j] == (-1 if i == j else 0) for i in range(3) for j in range(3)) for M in G)
    tr = lambda M: M[0][0] + M[1][1] + M[2][2]
    # rotation by angle t has trace 1 + 2 cos t: 4-fold trace 1, 3-fold trace 0, 2-fold trace -1
    c4 = sum(1 for M in rot if tr(M) == 1); c3 = sum(1 for M in rot if tr(M) == 0); c2 = sum(1 for M in rot if tr(M) == -1)
    name = {(48, True): 'Oh', (16, True): 'D4h', (12, True): 'D3d', (8, True): 'D2h', (4, True): 'C2h', (2, True): 'Ci',
            (24, True): 'D6h' if c3 == 2 and c4 == 0 else 'Th', (1, False): 'C1'}.get((n, inv), f'order {n}')
    if (n, inv) == (16, True) and c4 != 2: name = f'order 16 (4-fold elements {c4})'
    if (n, inv) == (12, True) and c3 != 2: name = f'order 12 (3-fold elements {c3})'
    return {'name': name, 'order': n, 'rotations': len(rot), 'inversion': inv, 'fourfold_elements': c4, 'threefold_elements': c3, 'twofold_rotations': c2}


# ---- congruence by corner matching (exact) ----
def congruent(P, Q):
    """A bijection of corners keeping every pairwise distance exactly (then an isometry carries one set onto the other).
    Returns the bijection as a list or None. Summary fingerprints are only used to prune."""
    if len(P) != len(Q): return None
    n = len(P)
    D = lambda S: [[dot(sub(a, b), sub(a, b)) for b in S] for a in S]
    DP, DQ = D(P), D(Q)
    sig = lambda row: tuple(sorted(row, key=float))
    sP = [sig(r) for r in DP]; sQ = [sig(r) for r in DQ]
    if sorted(sP, key=lambda t: [float(x) for x in t]) != sorted(sQ, key=lambda t: [float(x) for x in t]): return None
    order = sorted(range(n), key=lambda i: sum(1 for j in range(n) if sQ[j] == sP[i]))
    m = {}; used = set()

    def bt(k):
        if k == n: return True
        i = order[k]
        for j in range(n):
            if j in used or sQ[j] != sP[i]: continue
            if all(DP[i][i2] == DQ[j][m[i2]] for i2 in m):
                m[i] = j; used.add(j)
                if bt(k + 1): return True
                del m[i]; used.discard(j)
        return False
    return [m[i] for i in range(n)] if bt(0) else None


# ---- tiling by translation: exact proof ----
def facets(V_, F_):
    out = []
    for f in F_:
        n = face_normal(V_, f); out.append((n, dot(n, V_[f[0]]), f))
    return out


def tiling(V_, F_, basis):
    """P centred at the origin, centrally symmetric. Proves that the translates P + L Z^3 tile space:
    (1) vol P = |det L|; (2) packing: no nonzero lattice vector lies inside 2P = P - P (exact facet test);
    (3) face-to-face: each facet's neighbour translation 2 x (facet centre) is a lattice vector, and touches along it."""
    res = {}
    vol = volume(V_, F_); dL = mdet(cols(basis)); res['volume'] = to_str(vol); res['det_L'] = to_str(abs_q(dL))
    res['volume_equals_det'] = vol == abs_q(dL)
    res['centrally_symmetric'] = set(V_) == {sc(v, -1) for v in V_}
    FS = facets(V_, F_)
    Linv = minv(cols(basis))
    R = max(max(abs(float(x)) for x in matvec(Linv, v)) for v in V_)
    N = int(math.floor(2 * R + 1e-9)) + 1
    inside = []
    for m in itertools.product(range(-N, N + 1), repeat=3):
        if m == (0, 0, 0): continue
        t = vsum(sc(b, k) for b, k in zip(basis, m))
        if all((dot(n, t) - 2 * h).sign() < 0 for n, h, _ in FS): inside.append(m)
    res['search_box'] = N; res['lattice_points_in_open_2P'] = len(inside); res['packing'] = not inside
    ok = True; neigh = set()
    for n, h, f in FS:
        t = sc(vsum(V_[i] for i in f), Fr(2, len(f)))
        c = matvec(Linv, t)
        if not all(x.is_int() for x in c) or dot(n, t) != 2 * h: ok = False
        neigh.add(t)
    res['face_neighbours_are_lattice_vectors'] = ok
    res['face_neighbours'] = len(neigh)
    res['tiles'] = res['volume_equals_det'] and res['packing'] and ok and res['centrally_symmetric']
    return res


# ---- dissections: pieces interior-disjoint inside a convex hull, volumes adding up ----
def polytope_edges(V_, F_):
    return {frozenset((f[i], f[(i + 1) % len(f)])) for f in F_ for i in range(len(f))}


def separated(A, B):
    """Exact separating-axis test for convex polytopes (verts, faces): True when their interiors are disjoint."""
    (VA, FA), (VB, FB) = A, B
    axes = [face_normal(VA, f) for f in FA] + [face_normal(VB, f) for f in FB]
    ea = [sub(VA[min(e)], VA[max(e)]) for e in map(tuple, polytope_edges(VA, FA))]
    eb = [sub(VB[min(e)], VB[max(e)]) for e in map(tuple, polytope_edges(VB, FB))]
    for a in ea:
        for b in eb:
            c = cross(a, b)
            if not iszero(c): axes.append(c)
    for n in axes:
        pa = [dot(n, v) for v in VA]; pb = [dot(n, v) for v in VB]
        if max(pa) <= min(pb) or max(pb) <= min(pa): return True
    return False


def _qmax(xs):
    m = xs[0]
    for x in xs[1:]:
        if x > m: m = x
    return m


def dissection(whole_points, pieces_points):
    """whole = hull(whole_points); pieces = hulls. Checks: each piece inside the whole, pieces pairwise interior-disjoint,
    volumes add up exactly. Then the pieces glued together ARE the whole."""
    W = hull(whole_points); vw = volume(*W)
    Ps = [hull(p) for p in pieces_points]
    FS = facets(*W)
    inside = all(all((dot(n, v) - h).sign() <= 0 for n, h, _ in FS) for P in Ps for v in P[0])
    disjoint = all(separated(Ps[i], Ps[j]) for i, j in itertools.combinations(range(len(Ps)), 2))
    vols = [volume(*P) for P in Ps]
    total = vsum_scalar(vols)
    return {'pieces_inside_whole': inside, 'pieces_interior_disjoint': disjoint, 'piece_volumes': [to_str(v) for v in vols],
            'sum_of_pieces': to_str(total), 'whole_volume': to_str(vw), 'volumes_add_up': total == vw,
            'glued_pieces_are_the_whole': inside and disjoint and total == vw}, W, Ps


def vsum_scalar(xs):
    s = q(0)
    for x in xs: s = s + x
    return s
