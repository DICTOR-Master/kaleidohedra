# DICTO · dictospheres.com — exact geometry of the six regular 4-polytopes and of the 600-cell with 120 caps, for the
# paper "The Dehn–Hadwiger invariant in four dimensions". Every number is held exactly as p + q√5 with p, q rational (Q5);
# no floating point is used in any check. Facets are found from the facet normals (the polar vertex sets), ridges as the
# vertex sets shared by two facets in at least 3 corners, and dihedral angles from the normals: cos = −n₁·n₂ / |n|².
# The 600-cell is the binary icosahedral group 2I of unit quaternions (circumradius 1, edge 1/φ); the caps are the
# regular 5-cells on the facets of one orbit of left multiplication (study 2026-11-20-600cell-5cell-zero).
# Usage: import exact4d (used by audit.py and fig_scenes.py); python3 exact4d.py prints the checks.
from fractions import Fraction as Fr
from itertools import combinations, permutations, product


class Q5:
    """a + b√5, a and b rational."""
    __slots__ = ('a', 'b')

    def __init__(self, a=0, b=0): self.a = Fr(a); self.b = Fr(b)
    def __add__(s, o): o = q(o); return Q5(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = q(o); return Q5(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return q(o) - s
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): o = q(o); return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def conj(s): return Q5(s.a, -s.b)
    def norm(s): return s.a * s.a - 5 * s.b * s.b
    def __truediv__(s, o): o = q(o); n = o.norm(); assert n != 0; t = s * o.conj(); return Q5(t.a / n, t.b / n)
    def __rtruediv__(s, o): return q(o) / s
    def __eq__(s, o): o = q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __float__(s): return float(s.a) + float(s.b) * 5 ** 0.5

    def sign(s):
        """exact sign of a + b√5."""
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        # opposite signs: compare a² with 5b²
        d = a * a - 5 * b * b
        return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)

    def __lt__(s, o): return (s - q(o)).sign() < 0
    def __gt__(s, o): return (s - q(o)).sign() > 0
    def __repr__(s): return f'({s.a}+{s.b}√5)'


def q(x): return x if isinstance(x, Q5) else Q5(x)


R5 = Q5(0, 1)                      # √5
PHI = Q5(Fr(1, 2), Fr(1, 2))       # φ
H = Fr(1, 2)


def dot(u, v): return sum((x * y for x, y in zip(u, v)), Q5())
def sub(u, v): return tuple(x - y for x, y in zip(u, v))
def add(u, v): return tuple(x + y for x, y in zip(u, v))
def scal(c, u): return tuple(c * x for x in u)
def vq(*xs): return tuple(q(x) for x in xs)


def qmul(x, y):
    """quaternion product, (w, i, j, k)."""
    a1, b1, c1, d1 = x; a2, b2, c2, d2 = y
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def signs(v):
    out = set()
    for s in product((1, -1), repeat=len(v)): out.add(tuple(si * x for si, x in zip(s, v)))
    return out


def even_perms(v):
    out = set()
    for p in permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0: out.add(tuple(v[p[i]] for i in range(4)))
    return out


def all_perms(v): return set(tuple(v[p[i]] for i in range(4)) for p in permutations(range(4)))


def verts600():
    """the 120 unit quaternions of 2I (circumradius 1, edge 1/φ)."""
    S = set()
    for p in all_perms((1, 0, 0, 0)): S |= signs(p)
    S |= signs((H, H, H, H))
    for s in signs((PHI / 2, Q5(H), 1 / (2 * PHI), Q5(0))): S |= even_perms(s)
    S = [vq(*v) for v in S]; uniq = {}
    for v in S: uniq[v] = 1
    return sorted(uniq, key=lambda v: tuple(float(x) for x in v))


class Polytope:
    """vertices V, facet normals N (facet = vertices maximising n·x), all normals of one length."""

    def __init__(self, name, V, N):
        self.name, self.V, self.N = name, [vq(*v) for v in V], [vq(*n) for n in N]
        nn = {dot(n, n) for n in self.N}; assert len(nn) == 1, name; self.nn = nn.pop()
        r2 = {dot(v, v) for v in self.V}; assert len(r2) == 1, name + ': vertices not on one sphere'; self.R2 = r2.pop()
        self.cells = []
        for n in self.N:
            vals = [dot(n, v) for v in self.V]; m = vals[0]
            for x in vals: m = x if x > m else m
            assert m.sign() > 0
            self.cells.append(frozenset(i for i, x in enumerate(vals) if x == m))
        d2 = {}
        for i, j in combinations(range(len(self.V)), 2): d2.setdefault(dot(sub(self.V[i], self.V[j]), sub(self.V[i], self.V[j])), []).append((i, j))
        self.a2 = min(d2, key=float); self.E = d2[self.a2]
        # ridges: vertex sets shared by two facets in >= 3 corners; dihedral cos from the two normals
        self.ridges, cosv = {}, set()
        inc = {}
        for k, c in enumerate(self.cells):
            for v in c: inc.setdefault(v, []).append(k)
        for k, c in enumerate(self.cells):
            nb = set(l for v in c for l in inc[v] if l > k)
            for l in nb:
                s = c & self.cells[l]
                if len(s) >= 3:
                    self.ridges[frozenset(s)] = (k, l); cosv.add(-dot(self.N[k], self.N[l]) / self.nn)
        assert len(cosv) == 1, name + ': more than one dihedral angle'; self.cos = cosv.pop()
        # every ridge in exactly two facets (no third facet contains it)
        for s, (k, l) in self.ridges.items(): assert sum(1 for c in self.cells if s <= c) == 2

    def counts(self): return len(self.V), len(self.E), len(self.ridges), len(self.cells)


def tri_area2(P, Q, R):
    """squared area of a triangle, exact."""
    u, v = sub(Q, P), sub(R, P); return (dot(u, u) * dot(v, v) - dot(u, v) * dot(u, v)) / 4


def six():
    """the six regular 4-polytopes, D·I·C·T·O order of their cells' solids, then the 24-cell."""
    P = {}
    V600 = verts600()
    # 600-cell: normals = facet centroids (sums of the 4 corners of each tetrahedron); found from the edge graph
    Vs = V600; adj = {i: set() for i in range(len(Vs))}
    d = {}
    for i, j in combinations(range(len(Vs)), 2): d[(i, j)] = dot(Vs[i], Vs[j])
    top = max(set(d.values()) - {Q5(1)}, key=float)            # nearest neighbours: inner product φ/2
    assert top == PHI / 2
    for (i, j), x in d.items():
        if x == top: adj[i].add(j); adj[j].add(i)
    tets = set()
    for i in adj:
        for j, k, l in combinations(sorted(adj[i]), 3):
            if k in adj[j] and l in adj[j] and l in adj[k]: tets.add(frozenset((i, j, k, l)))
    cent = [tuple(sum((Vs[i][c] for i in t), Q5()) for c in range(4)) for t in sorted(tets, key=sorted)]
    P['600-cell'] = Polytope('600-cell', Vs, cent)
    P['120-cell'] = Polytope('120-cell', cent, Vs)
    P['tesseract'] = Polytope('tesseract', list(signs((1, 1, 1, 1))), [v for p in all_perms((1, 0, 0, 0)) for v in signs(p)])
    P['16-cell'] = Polytope('16-cell', [v for p in all_perms((1, 0, 0, 0)) for v in signs(p)], list(signs((1, 1, 1, 1))))
    V24 = [v for p in all_perms((1, 1, 0, 0)) for v in signs(p)]
    N24 = [scal(2, v) for p in all_perms((1, 0, 0, 0)) for v in signs(p)] + list(signs((1, 1, 1, 1)))
    P['24-cell'] = Polytope('24-cell', V24, N24)
    s = R5 / 5                                                       # 1/√5
    V5 = [vq(1, 1, 1, -s), vq(1, -1, -1, -s), vq(-1, 1, -1, -s), vq(-1, -1, 1, -s), vq(0, 0, 0, 4 * s)]
    P['5-cell'] = Polytope('5-cell', V5, [scal(-1, v) for v in V5])
    return P


ORDER = ['120-cell', '600-cell', 'tesseract', '5-cell', '16-cell', '24-cell']


def caps(P600):
    """the 5 orbits of the 600 facets under left multiplication by 2I, and the cap tips of each orbit."""
    V = P600.V; idx = {v: i for i, v in enumerate(V)}; cells = P600.cells
    cid = {c: k for k, c in enumerate(cells)}; seen, orbits = set(), []
    for k, c in enumerate(cells):
        if k in seen: continue
        orb = []
        for g in V:
            img = frozenset(idx[qmul(g, V[i])] for i in c)
            orb.append(cid[img])
        orb = sorted(set(orb)); seen |= set(orb); orbits.append(orb)
    return orbits


def tip(P600, k):
    """apex of the regular 5-cell on facet k: (4/φ²) × centroid = (1/φ²) × (sum of the 4 corners)."""
    c = P600.cells[k]; s = tuple(sum((P600.V[i][j] for i in c), Q5()) for j in range(4))
    return scal(1 / (PHI * PHI), s)


def cap_checks(P600, orb):
    """exact facts of one orbit: no shared triangle, every edge once, every corner 4 times, tips regular at radius √2."""
    cells = [P600.cells[k] for k in orb]; out = {}
    tri = {}
    for c in cells:
        for t in combinations(sorted(c), 3): tri[frozenset(t)] = tri.get(frozenset(t), 0) + 1
    out['no_shared_triangle'] = max(tri.values()) == 1 and len(tri) == 4 * len(cells)
    ec = {}
    for c in cells:
        for e in combinations(sorted(c), 2): ec[e] = ec.get(e, 0) + 1
    out['edges_once'] = len(ec) == len(P600.E) and set(ec.values()) == {1} and set(ec) == set(P600.E)
    vc = {}
    for c in cells:
        for v in c: vc[v] = vc.get(v, 0) + 1
    out['corner_in_4'] = set(vc.values()) == {4} and len(vc) == 120
    T = [tip(P600, k) for k in orb]
    out['tip_r2'] = {dot(t, t) for t in T} == {Q5(2)}
    out['cap_regular'] = all(dot(sub(t, P600.V[i]), sub(t, P600.V[i])) == P600.a2 for t, k in zip(T, orb) for i in P600.cells[k])
    # tips = P · t0 (right multiplication by the fixed quaternion t0): an isometric copy of √2 × the 600-cell
    t0 = T[0]; out['tips_are_P_t0'] = set(T) == {qmul(v, t0) for v in P600.V}
    return out, T


if __name__ == '__main__':
    P = six()
    for nm in ORDER:
        p = P[nm]; print(nm, p.counts(), 'cos', p.cos, 'edge²/R²', p.a2 / p.R2)
    orbs = caps(P['600-cell']); print('orbits', [len(o) for o in orbs])
    for o in orbs: print(cap_checks(P['600-cell'], o)[0])
