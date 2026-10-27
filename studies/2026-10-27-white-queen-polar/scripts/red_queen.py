"""Red Queen 120-cell (placeholder name), stages 1-2: the exact 120-cell as the polar of the #63 source model, its checks,
its dodecahedron layers round one cell in perspective (one kind per layer?), and the core. Exact in Q(sqrt5) (Fractions).
usage: red_queen.py <600cell-source.json> <out.json>"""
import json, sys, math
from fractions import Fraction as Fr
from collections import Counter, defaultdict
from itertools import combinations

class Q:
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return Q(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Q(s.a - o.a, s.b - o.b)
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return Q(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * o.inv()
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __float__(s): return float(s.a) + float(s.b) * math.sqrt(5)
    def __repr__(s): return f"{s.a}" + (f"{'+' if s.b >= 0 else ''}{s.b}r5" if s.b else "")
Z = Q(0)
def dot(x, y): return sum((a * b for a, b in zip(x, y)), Z)
def sub(x, y): return tuple(a - b for a, b in zip(x, y))
def sc(k, x): return tuple(k * a for a in x)
def sq(x): return dot(x, x)

S = json.load(open(sys.argv[1]))
V = [tuple(Q(Fr(c[0]), Fr(c[1])) for c in v) for v in S["vertices_exact"]]
cells, tris, edges = S["cells"], S["triangles"], S["edges"]
out, ok = {}, []
def check(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)

# ---- stage 1: the 120-cell ----
R = [sc(Q(Fr(1, 4)), tuple(sum((V[i][k] for i in c), Z) for k in range(4))) for c in cells]   # corners = cell centres
cells_of_v = defaultdict(list); [cells_of_v[i].append(ci) for ci, c in enumerate(cells) for i in c]
key = lambda s: frozenset(s)
cell_by = defaultdict(list)
for ci, c in enumerate(cells):
    for t in combinations(sorted(c), 3): cell_by[key(t)].append(ci)
Redges = [tuple(cell_by[key(t)]) for t in tris]
check("1200 edges, each between two corners", len(Redges) == 1200 and all(len(e) == 2 for e in Redges))
L2 = {sq(sub(R[a], R[b])) for a, b in Redges}
check("all edges one length", len(L2) == 1)
out["corner_radius2"] = repr(sq(R[0])); out["edge2"] = repr(next(iter(L2)))
check("600 corners all at one radius", len({sq(p) for p in R}) == 1 and len(R) == 600)
adj = defaultdict(set); [(adj[a].add(b), adj[b].add(a)) for a, b in Redges]
check("every corner has 4 edges (vertex figure a tetrahedron)", all(len(adj[i]) == 4 for i in range(600)))
# pentagons: the 5 cells round each 600-cell edge
pents = []
for a, b in edges:
    ring = [ci for ci in cells_of_v[a] if b in cells[ci]]
    pents.append(ring)
check("720 pentagons of 5 corners", len(pents) == 720 and all(len(p) == 5 for p in pents))
def regular_pentagon(p):
    es = [(x, y) for x, y in combinations(p, 2) if y in adj[x]]
    if len(es) != 5: return False
    d2 = {sq(sub(R[x], R[y])) for x, y in combinations(p, 2)}
    return len(d2) == 2   # 5 sides + 5 diagonals
check("every pentagon regular (5 sides equal, 5 diagonals equal)", all(regular_pentagon(p) for p in pents))
# cells: the 20 cells round each 600-cell vertex
Rcells = [cells_of_v[i] for i in range(120)]
def regular_dodecahedron(c):
    cs = set(c)
    es = [(x, y) for x, y in combinations(c, 2) if y in adj[x]]
    deg = Counter(); [(deg.update([x, y])) for x, y in es]
    cen = sc(Q(Fr(1, 20)), tuple(sum((R[x][k] for x in c), Z) for k in range(4)))
    return len(c) == 20 and len(es) == 30 and all(deg[x] == 3 for x in c) and len({sq(sub(R[x], cen)) for x in c}) == 1 \
        and len({sq(sub(R[x], R[y])) for x, y in es}) == 1
check("120 cells, each a regular dodecahedron (20 corners, 30 equal edges, 3 per corner, on one sphere)", len(Rcells) == 120 and all(regular_dodecahedron(c) for c in Rcells))
check("each pentagon in exactly 2 cells", all(sum(1 for c in Rcells if set(p) <= set(c)) == 2 for p in pents))

# ---- stage 2: layers round one cell ----
d = V[0]                                    # axis: the White Queen's vertex 0 = centre direction of Red Queen cell 0
hc = [dot(V[i], d) for i in range(120)]    # cell heights (by their centre direction)
lay = sorted(set(hc), key=float, reverse=True)
out["cell_layers"] = [hc.count(h) for h in lay]
check("120 dodecahedra in 9 layers 1,12,20,12,30,12,20,12,1", out["cell_layers"] == [1, 12, 20, 12, 30, 12, 20, 12, 1])
hv = [dot(p, d) for p in R]
vl = sorted(set(hv), key=float, reverse=True)
out["corner_layers"] = [hv.count(h) for h in vl]
check("600 corners in 15 layers = the Cleo shells", out["corner_layers"] == [20, 20, 30, 60, 60, 60, 20, 60, 20, 60, 60, 60, 30, 20, 20])
# perspective from just beyond the opposite cell: eye on the axis, past the opposite cell's hyperplane
hmin = vl[-1]; he = hmin * Q(Fr(21, 20)); dd = sq(d)
def proj(p):
    h = dot(p, d); perp = sub(p, sc(h / dd, d))
    return sc(Q(1) / (h - he), perp)
P = [proj(p) for p in R]
kinds = []
for h in lay:
    keys = set()
    for ci in [i for i in range(120) if hc[i] == h]:
        c = Rcells[ci]
        keys.add(tuple(sorted((sq(sub(P[x], P[y])) for x, y in combinations(c, 2)), key=lambda q: (float(q), q.a, q.b))))
    kinds.append(len(keys))
out["kinds_per_cell_layer"] = kinds
print("kinds per dodecahedron layer:", kinds)
# the core: the central cell in perspective is a regular dodecahedron centred on the axis point (the image of the centre)
c0 = Rcells[0]; cen = sc(Q(Fr(1, 20)), tuple(sum((P[x][k] for x in c0), Z) for k in range(4)))
check("core projects to a regular dodecahedron centred on the axis", all(x == Z for x in cen) and len({sq(P[x]) for x in c0}) == 1
      and len({sq(sub(P[x], P[y])) for x, y in combinations(c0, 2) if y in adj[x]}) == 1)
check("the core's 20 corners are the centres of the 20 Cleo-Icos cells round White Queen vertex 0", set(c0) == set(cells_of_v[0]))
# the polar dictionary of the core: 12 pentagons of the core <-> the 12 neighbours of vertex 0
nb = {j for a, b in edges for j in (a, b) if 0 in (a, b)} - {0}
core_pents = [p for p, (a, b) in zip(pents, edges) if 0 in (a, b)]
check("core's 12 pentagons = the 12 White Queen edges at vertex 0 (the icosahedron's 12 corners)", len(nb) == 12 and len(core_pents) == 12 and all(set(p) <= set(c0) for p in core_pents))
out["checks"] = {n: v for n, v in ok}
out["eye_height_over_opposite"] = "21/20"
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(sum(v for _, v in ok), "of", len(ok), "checks passed")
