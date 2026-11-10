"""Scutoid L, step 2 (DICTO 10 Nov: scutoids not to be left waiting). On a periodic hexagonal tiling (torus NX x NY cells) find a
pairing of cells into neighbouring pairs (the shared edge of each pair shrinks to a point going up) such that
 (1) every cell is in exactly one pair (so every cell becomes a pentagon at the middle level),
 (2) no two shrinking edges share a corner (each shrunk point has exactly four cells),
 (3) every cell is the top or bottom TIP of exactly one shrinking edge (so after the points reopen across, every cell is a hexagon again).
Exact search by SAT (pysat). Known answer used as a control: the brick pairing satisfies (1)-(2) but not (3) (it gives 5s and 7s).
Usage: python pairing_search.py NX NY"""
import sys, itertools
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
NX, NY = int(sys.argv[1]), int(sys.argv[2])
cells = [(i, j) for j in range(NY) for i in range(NX)]; cid = {c: n for n, c in enumerate(cells)}
def nbrs(i, j):   # offset rows (odd rows shifted right): six neighbours on the torus, in corner order
    if j % 2 == 0: d = [(1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
    else: d = [(1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1)]
    return [((i + a) % NX, (j + b) % NY) for a, b in d]
# edges = unordered neighbour pairs; corners = triples of mutually adjacent cells (each corner of the tiling is shared by 3 cells)
E = sorted({frozenset((cid[c], cid[n])) for c in cells for n in nbrs(*c)}, key=sorted)
eid = {e: k + 1 for k, e in enumerate(E)}
corners = set()
for c in cells:
    N = nbrs(*c)
    for k in range(6):
        corners.add(frozenset((cid[c], cid[N[k]], cid[N[(k + 1) % 6]])))
# an edge {a, b} has two corners: {a, b, x} and {a, b, y}; x and y are its two TIP cells
tips = {}
for e in E:
    a, b = sorted(e); xs = [next(iter(t - e)) for t in corners if e <= t]
    assert len(xs) == 2, (e, xs); tips[e] = xs
assert len(E) == 3 * len(cells) and len(corners) == 2 * len(cells)
S = Cadical153(); top = len(E)
def card(lits, k):
    global top
    cnf = CardEnc.equals(lits=lits, bound=k, top_id=top, encoding=EncType.seqcounter); top = max(top, cnf.nv)
    for cl in cnf.clauses: S.add_clause(cl)
for n in range(len(cells)): card([eid[e] for e in E if n in e], 1)                      # (1)
for t in corners:                                                                         # (2): at most one shrinking edge per corner
    es = [eid[frozenset(p)] for p in itertools.combinations(t, 2)]
    for x, y in itertools.combinations(es, 2): S.add_clause([-x, -y])
for n in range(len(cells)): card([eid[e] for e in E if n in tips[e]], 1)                 # (3)
ok = S.solve()
print(f'torus {NX} x {NY}: ' + ('a pairing with hexagons everywhere at the top EXISTS' if ok else 'NO such pairing'))
if ok:
    pairs = [sorted(cells[x] for x in e) for e in E if eid[e] in set(l for l in S.get_model() if l > 0)]
    print('pairs:', pairs)
# control: the brick pairing must pass (1)-(2) and fail (3)
brick = [frozenset((cid[(i, j)], cid[((i + 1) % NX, j)])) for j in range(NY) for i in range(NX) if (i + j) % 2 == 0]
c1 = all(sum(n in e for e in brick) == 1 for n in range(len(cells)))
c3 = all(sum(n in tips[e] for e in brick) == 1 for n in range(len(cells)))
print(f'control (brick pairing): every cell paired {c1}; hexagons at the top {c3} (expected True, False)')
print('FINAL ok' if (c1 and not c3) else 'FINAL FAIL: control did not behave as known')
