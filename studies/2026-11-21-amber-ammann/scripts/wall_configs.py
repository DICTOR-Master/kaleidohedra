"""Wall configurations (24 Nov 2026): is "across every prolate-oblate wall the outer patterns differ" true for every tiling, not only
for the 402-cell patch?  Exact in Q(sqrt5).

A HALF-WALL is (A, l, s): a cell spanned by the triple A of the 20 (translation classes of rhombohedra with edges e_0..e_5), and one of
its 6 faces: the face spanned by the two vectors of A other than e_l, on the side s (0: -e_l/2, 1: +e_l/2 from the cell centre).
A WALL CONFIGURATION is an unordered pair of half-walls on the same face plane {i,j} (the same face, after translation) with the two
cells on opposite sides of it.  Two cells sharing a face in a face-to-face tiling by translates of the 20 cells form exactly one wall
configuration, and the configuration fixes both cells relative to the face (centre = face centre - (2s-1) e_l / 2).

1. Enumerate every wall configuration from geometry; count the prolate-oblate ones.
2. Read the patch (data/patch.json); map each of its 998 walls to its configuration; check every prolate-oblate one occurs.
3. For the setting SOLID SCALE SEED (as facematch_exact.py, whose pattern code is reused unchanged): compare the outer patterns of the
   two sides of every configuration directly, relative to the face centre (not through the patch).
4. Full isometry groups: the 8 vertices of each cell, all distance-preserving permutations counted exactly (= order of the symmetry group);
   all 15 face rhombi congruent (|e_i . e_j| the same).
Usage: python wall_configs.py SOLID SCALE SEED.  Last line FINAL ok only if every check holds."""
import os, sys, itertools, json, runpy
from collections import Counter
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
solid, scale, seed = sys.argv[1], sys.argv[2], sys.argv[3]
fm = runpy.run_path(os.path.join(HERE, "facematch_exact.py"), run_name="facematch_exact")   # prints its own patch line
from ammann_cell import Q, dot, cross, vsub, vadd, vsc
from tiling import E, TRIPLES, tvol
def key(v): return tuple(x.key() for x in v)
def absq(x): return x if x.sign() >= 0 else -x
ok = True
vP = max((absq(tvol(A)) for A in TRIPLES), key=float)   # float only to pick the larger of the two exact volumes
kind = {A: ("P" if (absq(tvol(A)) - vP).sign() == 0 else "O") for A in TRIPLES}
# 4. face rhombi and symmetry groups
dots = {absq(dot(E[i], E[j])).key() for i, j in itertools.combinations(range(6), 2)}
print(f"|e_i . e_j| over the 15 pairs: {len(dots)} value(s) -> all faces congruent golden rhombi: {len(dots) == 1}")
ok &= len(dots) == 1
for A in (next(A for A in TRIPLES if kind[A] == "P"), next(A for A in TRIPLES if kind[A] == "O")):
    V = [vadd(vadd(vsc(a, E[A[0]]), vsc(b, E[A[1]])), vsc(c, E[A[2]])) for a, b, c in itertools.product((0, 1), repeat=3)]
    D = [[dot(vsub(V[p], V[q]), vsub(V[p], V[q])).key() for q in range(8)] for p in range(8)]
    n = sum(1 for pm in itertools.permutations(range(8)) if all(D[pm[p]][pm[q]] == D[p][q] for p in range(8) for q in range(p + 1, 8)))
    print(f"{kind[A]} cell {A}: distance-preserving vertex permutations = {n} (full symmetry group order; D3d = 12)")
    ok &= n == 12
# 1. enumerate
def half_sigma(A, l, s, i, j):
    n = cross(E[i], E[j]); d = dot(n, E[l]).sign()          # cell centre - face centre = -(2s-1) e_l / 2
    return -(2*s - 1)*d
halves = {}   # pair -> list of (A, l, s, sigma)
for A in TRIPLES:
    for l in A:
        i, j = [a for a in A if a != l]
        for s in (0, 1): halves.setdefault((i, j), []).append((A, l, s, half_sigma(A, l, s, i, j)))
configs = set()
for pr, H in halves.items():
    for h1, h2 in itertools.combinations_with_replacement(H, 2):
        if h1[3] == -h2[3]: configs.add((pr, frozenset((h1[:3], h2[:3]))) if h1 != h2 else None)
configs.discard(None)
def ckind(c): return "".join(sorted(kind[h[0]] for h in c[1]))
byk = Counter(ckind(c) for c in configs)
hk = Counter((pr, h[3], kind[h[0]]) for pr, H in halves.items() for h in H)
print(f"half-walls: {sum(len(H) for H in halves.values())} (20 cells x 6 faces); on each of the 15 face planes, each side, each kind: "
      f"{sorted(set(hk.values()))} (2 prolate and 2 oblate placements)")
ok &= set(hk.values()) == {2} and len(hk) == 60
print(f"wall configurations from geometry: {dict(sorted(byk.items()))}; total {len(configs)}")
ok &= byk["OP"] == 120
# 2. patch
P = fm["patch"]; tiles = P["tiles"]; seen = Counter(); wrong = 0
for t1, t2, pts in P["shared"]:
    pts6 = [tuple(p) for p in pts]; hs = []
    for ti in (t1, t2):
        t = tiles[ti]; A = tuple(t["A"]); n = t["n"]
        for l in A:
            if all(p[l] == n[l] for p in pts6): s = 0; break
            if all(p[l] == n[l] + 1 for p in pts6): s = 1; break
        hs.append((A, l, s))
    pr = tuple(sorted(set(hs[0][0]) - {hs[0][1]}))
    c = (pr, frozenset(hs))
    if c not in configs: wrong += 1
    seen[c] += 1
po_seen = {c for c in seen if ckind(c) == "OP"}
print(f"patch: {sum(seen.values())} walls, {wrong} not in the list; distinct configurations by kind: "
      f"{dict(sorted(Counter(ckind(c) for c in seen).items()))}; prolate-oblate configurations occurring: {len(po_seen)}/120")
ok &= wrong == 0 and len(po_seen) == 120
same = [c for c in configs if len({h[0] for h in c[1]}) == 1]
print(f"configurations with two translates of one cell stacked across the face: {len(same)} "
      f"({dict(Counter(ckind(c) for c in same))}); in the patch: {sum(1 for c in seen if c in same)}")
# 3. compare patterns per configuration, relative to the face centre
def rel(A, l, s):
    fc = vsc(Fr(1, 2) if s else Fr(-1, 2), E[l])
    return frozenset(frozenset(key(vsub(p, fc)) for p in Pg) for Pg in fm["pat"](list(A), l, s))
res = Counter()
for c in configs:
    h1, h2 = tuple(c[1]); res[(ckind(c), rel(*h1) == rel(*h2))] += 1
print(f"{solid} {scale} {seed}: per configuration, outer patterns agree from both sides: " +
      ", ".join(f"{k} {res[(k, True)]}/{res[(k, True)] + res[(k, False)]}" for k in ("OO", "OP", "PP")))
ok &= res[("OP", True)] == 0 and res[("OP", False)] == 120
print("FINAL ok" if ok else "FINAL FAILED")
