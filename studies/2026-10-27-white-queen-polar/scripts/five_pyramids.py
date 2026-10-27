"""Red Queen paper, main theorem check (DICTO 2026-10-28): Aristotle's five pyramids as the cores of the regular 4D solids, exact.
Vertex cores (simplex cells, 5-, 16-, 600-cell): seen from just beyond the far side along a vertex, the cells at that vertex cast pyramids
with apex at the centre over the faces of a regular solid. Cell cores (all six): seen along a cell's centre, the sides of the 4D pyramid
from the solid's centre over that cell cast the face pyramids of the cell's regular shadow. Star core: the small stellated 120-cell
{5/2,5,3} (on the 600-cell's corners): the 12 spikes at a corner. Each shadow pyramid is compared with Aristotle's face pyramid of the
same solid by circumradius^2 / edge^2 (exact), and with the true 4D piece. usage: five_pyramids.py <600cell-source.json> <out.json>"""
import json, sys, math
from fractions import Fraction as Fr
from itertools import combinations, product, permutations
from collections import defaultdict

class Q:
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return Q(s.a / n, -s.b / n)
    def __truediv__(s, o): o = o if isinstance(o, Q) else Q(o); return s * o.inv()
    def __eq__(s, o): o = o if isinstance(o, Q) else Q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __float__(s): return float(s.a) + float(s.b) * math.sqrt(5)
    def __repr__(s): return f"{s.a}" + (f"{'+' if s.b >= 0 else ''}{s.b}r5" if s.b else "")
Z = Q(0)
def dot(x, y): return sum((a * b for a, b in zip(x, y)), Z)
def sub(x, y): return tuple(a - b for a, b in zip(x, y))
def add(x, y): return tuple(a + b for a, b in zip(x, y))
def sc(k, x): return tuple(k * a for a in x)
def sq(x): return dot(x, x)
def mean(P): return sc(Q(Fr(1, len(P))), tuple(sum((p[k] for p in P), Z) for k in range(len(P[0]))))
PHI = Q(Fr(1, 2), Fr(1, 2))
ARIST = {4: ('tetrahedron', Q(Fr(3, 8))), 6: ('octahedron', Q(Fr(1, 2))), 8: ('cube', Q(Fr(3, 4))),
         12: ('icosahedron', Q(Fr(5, 8), Fr(1, 8))), 20: ('dodecahedron', Q(Fr(9, 8), Fr(3, 8)))}   # R^2/a^2 of the Platonic solids

def proj(p, d, he):
    h = dot(p, d); perp = sub(p, sc(h / sq(d), d)); return sc(Q(1) / (h - he), perp)
def eye(V, d): return min((dot(v, d) for v in V), key=float) * Q(Fr(21, 20))
def platonic(P):
    """P: points round 0. Regular Platonic solid centred at 0? returns (name, R2/a2, faces) or None."""
    if any(c != Z for c in mean(P)) or len({sq(p) for p in P}) != 1: return None
    d2 = sorted({sq(sub(p, q)) for p, q in combinations(P, 2)}, key=float); a2 = d2[0]
    E = [(i, j) for i, j in combinations(range(len(P)), 2) if sq(sub(P[i], P[j])) == a2]
    F = 2 - len(P) + len(E)
    if len(P) not in ARIST: return None
    name, r = ARIST[len(P)]
    return dict(solid=name, R2_over_a2=sq(P[0]) / a2, aristotle=r, matches=(sq(P[0]) / a2 == r), faces=F, edges=len(E))

def vertex_core(V, cells, name):
    v0 = V[0]; he = eye(V, v0); at = [c for c in cells if 0 in c]
    nb = sorted({i for c in at for i in c} - {0}); P = [proj(V[i], v0, he) for i in nb]
    pl = platonic(P)
    ok = pl is not None and pl['matches'] and pl['faces'] == len(at) and proj(v0, v0, he) == tuple(Z for _ in v0)
    true = sq(sub(V[at[0][0]], V[at[0][1]])) and Q(1)   # the 4D cells are regular tetrahedra: apex edge = base edge
    return dict(polytope=name, core='vertex', cells_at_vertex=len(at), shadow=pl, ok=ok, true_apex2_over_base2='1 (regular tetrahedron)')

def cell_core(V, cells, name):
    C = cells[0]; c = mean([V[i] for i in C]); he = eye(V, c)
    P = [proj(V[i], c, he) for i in C]; pl = platonic(P)
    ok = pl is not None and pl['matches'] and proj(tuple(Z for _ in c), c, he) == tuple(Z for _ in c)
    a2 = min((sq(sub(V[i], V[j])) for i, j in combinations(C, 2)), key=float)
    return dict(polytope=name, core='cell', cell_corners=len(C), shadow=pl, ok=ok, true_apex2_over_base2=sq(V[C[0]]) / a2)

def cells_by_dirs(V, dirs):
    out = []
    for c in dirs:
        hs = [dot(v, c) for v in V]; m = max(hs, key=float); out.append([i for i, h in enumerate(hs) if h == m])
    return out

R = []
# 5-cell in the hyperplane x0+..+x4 = 0 of R^5
V5 = [tuple(Q(Fr(1 if j == i else 0) - Fr(1, 5)) for j in range(5)) for i in range(5)]; C5 = [list(s) for s in combinations(range(5), 4)]
# 16-cell, tesseract, 24-cell
V16 = [tuple(Q(s if j == i else 0) for j in range(4)) for i in range(4) for s in (1, -1)]
C16 = cells_by_dirs(V16, [tuple(Q(x) for x in s) for s in product((1, -1), repeat=4)])
V8 = [tuple(Q(x) for x in s) for s in product((1, -1), repeat=4)]
C8 = cells_by_dirs(V8, [tuple(Q(s if j == i else 0) for j in range(4)) for i in range(4) for s in (1, -1)])
V24 = sorted({tuple(Q(x) for x in p) for s in product((1, -1), repeat=2) for p in permutations((s[0], s[1], 0, 0))}, key=lambda v: [float(x) for x in v])
D24 = [tuple(Q(2 * s if j == i else 0) for j in range(4)) for i in range(4) for s in (1, -1)] + [tuple(Q(x) for x in s) for s in product((1, -1), repeat=4)]
C24 = cells_by_dirs(V24, D24)
S = json.load(open(sys.argv[1]))
V600 = [tuple(Q(Fr(c[0]), Fr(c[1])) for c in v) for v in S["vertices_exact"]]; C600 = S["cells"]
cells_of_v = defaultdict(list); [cells_of_v[i].append(ci) for ci, c in enumerate(C600) for i in c]
V120 = [mean([V600[i] for i in c]) for c in C600]; C120 = [cells_of_v[i] for i in range(120)]
for name, V, C, n in [('5-cell', V5, C5, 5), ('16-cell', V16, C16, 16), ('tesseract', V8, C8, 8), ('24-cell', V24, C24, 24), ('600-cell', V600, C600, 600), ('120-cell', V120, C120, 120)]:
    assert len(C) == n, (name, len(C))
    if len(C[0]) == 4: R.append(vertex_core(V, C, name))
    R.append(cell_core(V, C, name))

# star core: small stellated 120-cell {5/2,5,3}: edges = 600-cell corner pairs at distance 2 (radius), cells = the 12 neighbours of
# each corner (an icosahedron) joined as a small stellated dodecahedron; the spike at a corner v0 of a cell: apex v0 over the pentagon
# of the points v0 + (u - v0)/phi^2 on its 5 cell edges v0u.
r2 = sq(V600[0]); edge600 = min((sq(sub(V600[0], v)) for v in V600[1:]), key=float)
nbr = {i: [j for j in range(120) if j != i and sq(sub(V600[i], V600[j])) == edge600] for i in range(120)}
star_edges = {frozenset((i, j)) for i in range(120) for j in range(120) if i < j and sq(sub(V600[i], V600[j])) == r2}
cells_star = [nbr[w] for w in range(120)]
at = [c for c in cells_star if 0 in c]
spikes = []
for c in at:
    us = [u for u in c if frozenset((0, u)) in star_edges]
    spikes.append([add(V600[0], sc(Q(1) / (PHI * PHI), sub(V600[u], V600[0]))) for u in us])
base = {p for s in spikes for p in s}
v0 = V600[0]; he = eye(V600, v0)
P = [proj(p, v0, he) for p in base]; pl = platonic(P)
true = [sq(sub(spikes[0][0], v0)), min((sq(sub(p, q)) for p, q in combinations(spikes[0], 2)), key=float)]
star = dict(polytope='small stellated 120-cell {5/2,5,3}', core='star vertex', edges=len(star_edges), cells_at_vertex=len(at),
            edges_per_spike=[len(s) for s in spikes], distinct_base_points=len(base), shadow=pl,
            ok=len(star_edges) == 1200 and len(at) == 12 and all(len(s) == 5 for s in spikes) and len(base) == 20 and pl is not None and pl['matches'] and pl['faces'] == 12,
            true_apex2_over_base2=true[0] / true[1])
R.append(star)
for r in R:
    s = r['shadow']
    print(f"{'PASS' if r['ok'] else 'FAIL'} {r['polytope']:>36} {r['core']:>11} core: shadow {s['solid'] if s else None} "
          f"R2/a2 {s['R2_over_a2'] if s else None} (Aristotle {s['aristotle'] if s else None}), {s['faces'] if s else None} pyramids; "
          f"true 4D apex2/base2 {r['true_apex2_over_base2']}")
json.dump(R, open(sys.argv[2], 'w'), indent=1, default=repr)
print(sum(r['ok'] for r in R), 'of', len(R), 'checks passed')
