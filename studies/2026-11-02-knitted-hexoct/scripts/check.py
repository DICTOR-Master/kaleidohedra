# Knitted HexOct (DICTO's idea, 2026-11-02): exact checks of the link geometry and of the test pieces.
# Run on dicto-big-brother with ~/geom/bin/python, in a folder that also holds tiles.py, engine.py, stackings.py
# (studies/2026-10-29-endless-stack-cell/scripts). Node spacing a = 1, sheet spacing d = sqrt(2/3).
import itertools, random, sympy as sp
from fractions import Fraction as Fr
r3, d = sp.sqrt(3), sp.sqrt(sp.Rational(2, 3))
e1, e2 = sp.Matrix([1, 0]), sp.Matrix([sp.Rational(1, 2), r3 / 2])
POS = {'A': 0 * e1, 'B': (e1 + e2) / 3, 'C': 2 * (e1 + e2) / 3}
def node(L, i, j, z): return sp.Matrix([*(POS[L] + i * e1 + j * e2), z * d])
def up_links(lo, hi):
    """offsets (i,j) of the 3 nodes of sheet hi touched by node (0,0) of sheet lo: hi-nodes at horizontal distance 1/sqrt(3)."""
    out = []
    for i, j in itertools.product(range(-2, 3), repeat=2):
        v = POS[hi] + i * e1 + j * e2 - POS[lo]
        if sp.simplify(v.dot(v) - sp.Rational(1, 3)) == 0: out.append((i, j, sp.simplify(v)))
    return out
print("1. links, a = 1, d = sqrt(2/3)")
for lo, hi in [('A', 'B'), ('B', 'C'), ('B', 'A'), ('A', 'C')]:
    L = up_links(lo, hi); assert len(L) == 3
    for i, j, v in L:
        w = sp.Matrix([v[0], v[1], d]); ln = sp.sqrt(sp.simplify(w.dot(w)))
        ang = sp.deg(sp.atan2(d, sp.sqrt(v.dot(v))))
        print(f"  {lo}(i,j) -> {hi}(i{i:+d},j{j:+d}):", end=" ")
        print(f"horizontal offset ({sp.nsimplify(v[0])}, {sp.nsimplify(v[1])}), length {sp.simplify(ln)}, tilt above sheet {float(ang):.4f} deg")
        assert sp.simplify(ln - 1) == 0
# c and h at sheet B: down-links B->A (as vectors from B) and up-links B->C (c) or B->A (h)
down = [sp.Matrix([-v[0], -v[1], -d]) for _, _, v in up_links('A', 'B')]
for kind, hi in [('c', 'C'), ('h', 'A')]:
    ups = [sp.Matrix([v[0], v[1], d]) for _, _, v in up_links('B', hi)]
    straight = sum(any(sp.simplify(u + w).norm() == 0 for w in down) for u in ups)
    mirror = sum(any(sp.simplify(sp.Matrix([u[0] - w[0], u[1] - w[1], u[2] + w[2]])).norm() == 0 for w in down) for u in ups)
    print(f"  sheet B {kind} (A-B-{hi}): up-links collinear with a down-link: {straight}/3; mirror images of a down-link in the sheet: {mirror}/3")
# 2. self-centring: shifting sheet B sideways by t lowers the sheet spacing allowed by three taut links of length 1
random.seed(1); worst = 0
for _ in range(20000):
    t = (random.uniform(-.3, .3), random.uniform(-.3, .3)); m = 0
    for _, _, v in up_links('A', 'B'):
        h2 = (float(v[0]) + t[0]) ** 2 + (float(v[1]) + t[1]) ** 2; m = max(m, h2)
    zmax = (1 - m) ** .5 if m < 1 else 0; worst = max(worst, zmax - float(d))
print(f"2. self-centring: 20000 random sideways shifts |t|<=0.42, largest (allowed spacing - sqrt(2/3)) = {worst:.3e} (<= 0: spacing is greatest only at t = 0)")
# 3. test pieces: 3 sheets, 3 x 3 nodes each (rhombic patch i, j = 0..2), links between neighbouring sheets inside the patches
def piece(word):
    nodes = {(k, i, j) for k in range(3) for i in range(3) for j in range(3)}; links = []
    for k in range(2):
        for i, j in itertools.product(range(3), repeat=2):
            for di, dj, _ in up_links(word[k], word[k + 1]):
                if (k + 1, i + di, j + dj) in nodes: links.append(((k, i, j), (k + 1, i + di, j + dj)))
    deg = {n: 0 for n in nodes}
    for a, b in links: deg[a] += 1; deg[b] += 1
    return nodes, links, deg
for word in ['ABC', 'ABA']:
    n, l, deg = piece(word)
    per = [sum(1 for a, b in l if a[0] == k) for k in range(2)]
    full = sum(1 for (k, i, j), g in deg.items() if k == 1 and g == 6)
    print(f"3. test piece {word}: nodes {len(n)}, links {len(l)} (gap 1: {per[0]}, gap 2: {per[1]}), middle-sheet nodes with all 6 links: {full}")
    for k in range(3):
        print("   sheet", k, word[k], "links per node:", [[deg[(k, i, j)] for i in range(3)] for j in range(3)])
# 4. HexOct at the ring-build weight lambda = -1/8: the tile pieces are the cells enclosed by sheets and links
from tiles import tile, POS as TP
def dist2(p, q):  # tile coordinates: (u, v) on the triangular lattice of spacing 1, z in layer units (sheet spacing sqrt(2/3))
    du, dv, dz = p[0] - q[0], p[1] - q[1], p[2] - q[2]; return du * du + du * dv + dv * dv + Fr(2, 3) * dz * dz
def is_node(word, L, p):
    if p[2] not in (-1, 0, 1): return False
    w = word[(L + int(p[2])) % len(word)]; u = p[0] - (TP[w][0] - TP[word[L]][0]); v = p[1] - (TP[w][1] - TP[word[L]][1])
    return u.denominator == 1 and v.denominator == 1
for word, L in [('ABC', 1), ('AB', 1), ('ABCB', 1), ('ABCB', 2), ('ABCACB', 3)]:
    pieces, tz = tile(word, L, Fr(-1, 8)); res = []
    for k, up, s, P, J in pieces:
        nodes = [p for p in P if is_node(word, L, p)]; other = [p for p in P if not is_node(word, L, p)]
        if k == 'tet':
            ok = len(P) == 4 and len(nodes) == 4 and all(dist2(a, b) == 1 for a, b in itertools.combinations(P, 2))
            res.append(f"tet {'OK' if ok else 'FAIL'} (4 nodes, all 6 edges = a)")
        else:
            def is_mid(m):  # m = midpoint of a link from a node a of sheet L (z = 0) to a node 2m - a of sheet L +- 1
                for du, dv in itertools.product(range(-2, 3), repeat=2):
                    a_ = (Fr(int(m[0]) + du), Fr(int(m[1]) + dv), Fr(0)); b_ = tuple(2 * m[r] - a_[r] for r in range(3))
                    if is_node(word, L, b_) and dist2(a_, b_) == 1: return True
                return False
            mids = all(is_mid(m) for m in other)
            ok = len(nodes) == 3 and len(other) == 6 and mids and all(dist2(a, b) == 1 for a, b in itertools.combinations(nodes, 2))
            res.append(f"oct-{'top' if up else 'bottom'} half {'OK' if ok else 'FAIL'} (3 nodes + 6 link midpoints)")
    print(f"4. lambda=-1/8, layer {L} of {word} ({'c' if word[L-1] != word[(L+1) % len(word)] else 'h'}):", "; ".join(res))
