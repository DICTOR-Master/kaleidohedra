"""Exact follow-up (22 Nov 2026): two patch facts used in #118, now exact (they were floating-point checks before).
 1. Mirror relation on shared walls: for each of the 998 shared walls, is the second cell the mirror image of the first in the wall
    plane (all 8 corners and the centre), exactly in Q(sqrt5)?  Expect: every prolate-prolate and oblate-oblate wall yes, every
    prolate-oblate wall no.
 2. Cells round the interior edges: integer combinatorics on the lattice points of the patch (as tiling.py: an edge is interior when
    every face through it is shared by two tiles); the number of tiles round each interior edge, and the number of odd edges.
Last line PATCH EXACT OK when the counts are as stated in #118 (380 mirror, 618 not; 814 interior edges, 552 odd)."""
import itertools, json, os
from collections import Counter
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
from tiling import E
from ammann_cell import Q, dot, cross, vsub, vsc
P = json.load(open(os.path.join(HERE, "../data/patch.json"))); T = P["tiles"]
def P3(v6): return [sum((E[i][r]*v6[i] for i in range(6)), Q(0)) for r in range(3)]
def key(v): return tuple(x.key() for x in v)
def corners6(t):
    out = []
    for bits in itertools.product((0, 1), repeat=3):
        v = list(t["n"])
        for q in range(3): v[t["A"][q]] += bits[q]
        out.append(v)
    return out
def centre6(t): return [Fr(t["n"][i]) + (Fr(1, 2) if i in t["A"] else 0) for i in range(6)]
mc = Counter()
for a, b, pts in P["shared"]:
    X = [P3(p) for p in pts]; n = cross(vsub(X[1], X[0]), vsub(X[3], X[0])); nn = dot(n, n)
    def R(x): return vsub(x, vsc(2*dot(vsub(x, X[0]), n)/nn, n))
    A = {key(R(P3(c))) for c in corners6(T[a])}; B = {key(P3(c)) for c in corners6(T[b])}
    mir = A == B and key(R(P3(centre6(T[a])))) == key(P3(centre6(T[b])))
    mc[("".join(sorted(T[a]["kind"] + T[b]["kind"])), mir)] += 1
print("mirror relation on shared walls (exact):", dict(mc))
# integer combinatorics of edges
faces = Counter(); edges = {}
for ti, t in enumerate(T):
    n, A = t["n"], t["A"]
    for k in range(3):
        i, j = [A[q] for q in range(3) if q != k]; l = A[k]
        for side in (0, 1):
            base = list(n); base[l] += side; pts = []
            for x, y in ((0, 0), (1, 0), (1, 1), (0, 1)):
                v = list(base); v[i] += x; v[j] += y; pts.append(tuple(v))
            faces[frozenset(pts)] += 1
        o1, o2 = [A[q] for q in range(3) if q != k]
        for x, y in ((0, 0), (1, 0), (0, 1), (1, 1)):
            v = list(n); v[o1] += x; v[o2] += y; w = list(v); w[l] += 1
            edges.setdefault(frozenset((tuple(v), tuple(w))), set()).add(ti)
fac_by_edge = {}
for f in faces:
    p = list(f)
    for u, v in itertools.combinations(p, 2):
        if sum(abs(x - y) for x, y in zip(u, v)) == 1: fac_by_edge.setdefault(frozenset((u, v)), []).append(f)
interior = [e for e in edges if all(faces[f] == 2 for f in fac_by_edge[e])]
deg = Counter(len(edges[e]) for e in interior)
odd = sum(c for d, c in deg.items() if d % 2)
print(f"faces {len(faces)}: shared {sum(1 for c in faces.values() if c == 2)}, boundary {sum(1 for c in faces.values() if c == 1)}")
print(f"interior edges {len(interior)} by number of cells round them (exact, integer): {dict(sorted(deg.items()))}; odd: {odd}")
ok = mc == Counter({("OP", False): 618, ("PP", True): 319, ("OO", True): 61}) and len(interior) == 814 and odd == 552
print("PATCH EXACT OK" if ok else "PATCH EXACT FAILED")
