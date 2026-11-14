# golden.py (14 Nov 2026) - DICTO · dictospheres.com
# Exact geometry in Q(sqrt5) for the hybrid golden slab of the Platonic mixes (study 2026-11-14-platonic-hybrid).
# Frame: Euclid's cube of edge phi centred at the origin; the dodecahedron of edge 1 is that cube with six roofs, corners
# (+-phi/2)^3 and the cyclic permutations of (0, +-1/2, +-phi^2/2); the icosahedron of edge 1 is Pacioli's, corners the cyclic
# permutations of (0, +-1/2, +-phi/2), inside the octahedron |x|+|y|+|z| <= phi^2/2 (#47 Lemma 4); everything pyritohedral.
# Pieces are sets: (label, positive convex parts, negative convex parts) = union(pos) minus union(neg).
# Point tests are exact: a point is an integer vector over a fixed denominator QD, a half-space n.x <= c has n, c in Q(sqrt5)
# scaled to integers, and the sign of u + v sqrt5 is decided exactly.
from fractions import Fraction as F
import itertools
from math import gcd

class Q5:
    __slots__ = ('a', 'b')
    def __init__(s, a=0, b=0): s.a = F(a); s.b = F(b)
    def __add__(s, o): o = q(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = q(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return q(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = q(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s):
        d = s.a * s.a - 5 * s.b * s.b; assert d != 0; return Q5(s.a / d, -s.b / d)
    def __truediv__(s, o): return s * q(o).inv()
    def __rtruediv__(s, o): return q(o) * s.inv()
    def sign(s): return sgn5(s.a, s.b)
    def __eq__(s, o):
        if not isinstance(o, (Q5, int, F)): return False
        o = q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5
    def __repr__(s):
        if s.b == 0: return str(s.a)
        return f'({s.a}{"+" if s.b > 0 else "-"}{abs(s.b)}r5)'
def q(x): return x if isinstance(x, Q5) else Q5(x)
def sgn5(u, v):
    """exact sign of u + v sqrt5 (u, v rational or int)"""
    if u >= 0 and v >= 0: return 0 if (u == 0 and v == 0) else 1
    if u <= 0 and v <= 0: return -1
    d = u * u - 5 * v * v
    if u > 0: return 1 if d > 0 else (-1 if d < 0 else 0)
    return -1 if d > 0 else (1 if d < 0 else 0)

PHI = Q5(F(1, 2), F(1, 2)); HF = PHI / 2; HALF = Q5(F(1, 2)); PHI2 = PHI * PHI
def V(*c): return tuple(q(x) for x in c)
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def mul(k, u): return tuple(k * a for a in u)
def dot(u, v): return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
def iszero(u): return all(x == 0 for x in u)
def cyc(p): return [p, (p[1], p[2], p[0]), (p[2], p[0], p[1])]
def signs(p):
    out = []
    for s in itertools.product((1, -1), repeat=3):
        v = tuple(x * k for x, k in zip(p, s))
        if v not in out: out.append(v)
    return out

# ---- exact convex hull: facet planes (n.x <= c) from vertices, and vertices from half-spaces
def planes_from_vertices(Vs):
    Vs = list(dict.fromkeys(Vs)); out = []
    cen = mul(Q5(F(1, len(Vs))), tuple(sum((v[i] for v in Vs), Q5()) for i in range(3)))
    for a, b, c in itertools.combinations(range(len(Vs)), 3):
        n = cross(sub(Vs[b], Vs[a]), sub(Vs[c], Vs[a]))
        if iszero(n): continue
        o = dot(n, Vs[a])
        if dot(n, cen) > o: n = mul(Q5(-1), n); o = -o
        if all(dot(n, v) <= o for v in Vs):
            n, o = normalise(n, o)
            if (n, o) not in out: out.append((n, o))
    return out
def normalise(n, o):
    k = next(x for x in n if x != 0)
    # scale so the first non-zero component is +-1 with the sign kept (positive scaling only)
    s = 1 if k > 0 else -1; f = (Q5(s) / k)
    return tuple(f * x for x in n), f * o
def solve3(A, b):
    det = lambda M: (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                     + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    D = det(A)
    if D == 0: return None
    out = []
    for i in range(3):
        M = [list(r) for r in A]
        for r in range(3): M[r][i] = b[r]
        out.append(det(M) / D)
    return tuple(out)
def vertices_from_planes(Hs):
    out = []
    for i, j, k in itertools.combinations(range(len(Hs)), 3):
        p = solve3([Hs[i][0], Hs[j][0], Hs[k][0]], [Hs[i][1], Hs[j][1], Hs[k][1]])
        if p is None or p in out: continue
        if all(dot(n, p) <= c for n, c in Hs): out.append(p)
    return out
def volume(Vs):
    """exact volume of the convex hull of Vs: cone from the centroid over each facet, facet fanned in cyclic order"""
    Vs = list(dict.fromkeys(Vs)); P = planes_from_vertices(Vs)
    cen = mul(Q5(F(1, len(Vs))), tuple(sum((v[i] for v in Vs), Q5()) for i in range(3)))
    inc = {i: [k for k, (n, c) in enumerate(P) if dot(n, Vs[i]) == c] for i in range(len(Vs))}
    tot = Q5()
    for k, (n, c) in enumerate(P):
        fv = [i for i in inc if k in inc[i]]
        # cyclic order: neighbours share a second facet (an edge of the polytope)
        cyc_ = [fv[0]]; rest = set(fv[1:])
        while rest:
            nxt = next(j for j in rest if len(set(inc[cyc_[-1]]) & set(inc[j])) >= 2); cyc_.append(nxt); rest.remove(nxt)
        for a, b in zip(cyc_[1:-1], cyc_[2:]):
            t = dot(sub(Vs[cyc_[0]], cen), cross(sub(Vs[a], cen), sub(Vs[b], cen)))
            tot = tot + (t if t > 0 else -t)
    return tot / 6

# ---- the solids in the cell frame
CUBE = [V(*p) for p in signs((HF, HF, HF))]
RIDGE = [V(*c) for p in signs((0, HALF, PHI2 / 2)) for c in cyc(p)]           # 12 ridge ends
DOD = CUBE + RIDGE
ICO = [V(*c) for p in signs((0, HALF, HF)) for c in cyc(p)]
OCT = [V(*c) for p in [(PHI2 / 2, 0, 0), (-PHI2 / 2, 0, 0)] for c in cyc(p)]
def roof(axis, sg):
    """Euclid's roof on the cube face x_axis = sg*phi/2: the face's 4 corners and the 2 ridge ends above it"""
    return [v for v in CUBE if v[axis] == sg * HF] + [v for v in RIDGE if v[axis] == sg * PHI2 / 2]
ROOFS = {(a, s): roof(a, s) for a in range(3) for s in (1, -1)}
def rot_z90(v): return (-v[1], v[0], v[2])            # quarter turn about the vertical axis (negative control)
def admiral_caps():
    """#47's six Admiral Caps: the octahedron minus the icosahedron, one piece round each corner, each = 2 tetrahedra"""
    c0 = V(PHI2 / 2, 0, 0); pp = V(HF, 0, HALF); pm = V(HF, 0, -HALF); qp = V(HALF, HF, 0); qm = V(HALF, -HF, 0)
    base = [[c0, pp, pm, qp], [c0, pp, pm, qm]]
    maps = [lambda v: v, lambda v: (-v[0], -v[1], v[2])]     # corner +x, and corner -x by the half turn about z
    out = []
    for m in maps:
        for k in range(3):
            perm = lambda v, k=k: tuple(v[(i - k) % 3] for i in range(3))   # cyclic: x -> y -> z
            out.append([[perm(m(v)) for v in t] for t in base])
    return out
def caps8():
    """the 8 caps: dodecahedron minus octahedron, cut by the coordinate planes; each convex"""
    D = planes_from_vertices(DOD); out = []
    for s in itertools.product((1, -1), repeat=3):
        Hs = list(D) + [(tuple(Q5(-k) if i == j else Q5(0) for j in range(3)), Q5(0)) for i, k in enumerate(s)]
        Hs.append((tuple(Q5(-k) for k in s), -PHI2 / 2))
        out.append((s, vertices_from_planes(Hs)))
    return out

# ---- integer half-spaces for fast exact point tests
def lcm(a, b): return a * b // gcd(a, b)
def int_halfspaces(Vs):
    """convex hull of Vs as integer rows (na0,na1,na2,nb0,nb1,nb2,ca,cb): inside iff (ca - na.p) + (cb - nb.p) sqrt5 > 0"""
    rows = []
    for n, c in planes_cached(Vs):
        fr = [x.a for x in n] + [x.b for x in n] + [c.a, c.b]
        m = 1
        for x in fr: m = lcm(m, x.denominator)
        rows.append(tuple(int(x * m) for x in fr))
    return rows
def fbox(Vs):
    f = [[float(x) for x in v] for v in Vs]
    return tuple(min(p[i] for p in f) for i in range(3)), tuple(max(p[i] for p in f) for i in range(3))
_PCACHE = {}
def planes_cached(Vs):
    """facet planes of a translate: computed once per shape (centred at its centroid), then shifted exactly"""
    Vs = list(dict.fromkeys(Vs)); k = Q5(F(1, len(Vs)))
    cen = tuple(k * sum((v[i] for v in Vs), Q5()) for i in range(3))
    key = tuple(sorted(repr(sub(v, cen)) for v in Vs))
    if key not in _PCACHE: _PCACHE[key] = planes_from_vertices([sub(v, cen) for v in Vs])
    return [(n, c + dot(n, cen)) for n, c in _PCACHE[key]]
class Part:
    __slots__ = ('rows', 'lo', 'hi', 'verts')
    def __init__(s, Vs):
        s.verts = list(dict.fromkeys(Vs)); s.rows = int_halfspaces(s.verts); s.lo, s.hi = fbox(s.verts)
    def test(s, P, QD, fp):
        """1 inside, 0 outside, None on the boundary (exact). P integer vector, point = P/QD; fp = float point"""
        if any(fp[i] < s.lo[i] - 1e-9 or fp[i] > s.hi[i] + 1e-9 for i in range(3)): return 0
        tie = False
        for na0, na1, na2, nb0, nb1, nb2, ca, cb in s.rows:
            sg = sgn5(ca * QD - na0 * P[0] - na1 * P[1] - na2 * P[2], cb * QD - nb0 * P[0] - nb1 * P[1] - nb2 * P[2])
            if sg < 0: return 0
            if sg == 0: tie = True
        return None if tie else 1
def shift(Vs, c): return [add(v, c) for v in Vs]
