#!/usr/bin/env python3
"""Resonus, Vacuus and their overlap for the six regular 4-polytopes and the 4D permutohedron, exactly in Q(sqrt5).

Resonus (DICTO, 24 Nov): one hyperplane through the centre O parallel to each facet (parallel facets share one).
Vacuus (#110 Section 2): one hyperplane through O and each ridge (two-face), its plate.
Mirrors: hyperplanes whose reflection maps the corner set to itself (found by exact reflection, independent of facets).

No floating point is used for any decision. Method:
  corners exact -> mirrors by exact reflection test (candidates b - w for b in a spanning set of corners)
  -> facets through one corner v0 from triples of its nearest corners, kept only if exactly supporting
  -> all facets as the orbit under the mirror reflections (each polytope here is corner-transitive under them)
  -> ridges = pairs of facets meeting in an affine plane; edges = polygon sides of the ridges (exact side test)
  -> checks: f-vector equals the known one, Euler f0 - f1 + f2 - f3 = 0, every ridge in exactly two facets.
Each facet is written a.x <= 1 (a = corner of the polar). Resonus normal = a (Theorem 1a of the resonus study);
Vacuus normal computed twice: a_F - a_G (Theorem 1b / pencil lemma) and the exact null vector of the ridge's corners.
"""
import sys, json, itertools, time, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qsqrt5 import K, R5, PHI, IPHI, ZERO, ONE, dot, sub, scal, vkey, linekey, nullspace, rank

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")
T0 = time.time()
FAILS = []
def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond: FAILS.append(msg)

def k(x): return K(Fr(x))
def signs(v):
    nz = [i for i, x in enumerate(v) if x]
    for s in itertools.product([1, -1], repeat=len(nz)):
        w = list(v)
        for i, e in zip(nz, s): w[i] = w[i] * e
        yield tuple(w)
def perms(v, even=False, odd=False):
    out = set()
    for p in itertools.permutations(range(len(v))):
        if even or odd:
            inv = sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])
            if inv % 2 != (1 if odd else 0): continue
        out.add(tuple(v[i] for i in p))
    return out
def dedup(vs):
    d = {}
    for v in vs: d[vkey(v)] = v
    return list(d.values())
def allsp(v, even=False, odd=False):
    return dedup([w for p in perms(v, even, odd) for w in signs(p)])

# ---------------------------------------------------------------- polytopes
def five_cell():
    return [tuple(k(5 if j == i else 0) - 1 for j in range(5)) for i in range(5)]
def tesseract(): return allsp((ONE, ONE, ONE, ONE))
def sixteen(): return allsp((ONE, ZERO, ZERO, ZERO))
def twentyfour(): return allsp((ONE, ONE, ZERO, ZERO))
def six_hundred(odd=False):
    h = K(Fr(1, 2))
    return dedup(allsp((ONE, ZERO, ZERO, ZERO)) + allsp((h, h, h, h)) + allsp((PHI * h, h, IPHI * h, ZERO), even=not odd, odd=odd))
def one_twenty():
    p, ip, p2, ip2 = PHI, IPHI, PHI * PHI, IPHI * IPHI
    two = k(2)
    V = (allsp((ZERO, ZERO, two, two)) + allsp((ONE, ONE, ONE, R5)) + allsp((ip2, p, p, p)) + allsp((ip, ip, ip, p2))
         + allsp((ZERO, ip2, ONE, p2), even=True) + allsp((ZERO, ip, p, R5), even=True) + allsp((ip, ONE, p, two), even=True))
    return dedup(V)
def permutohedron():
    return [tuple(k(x) - 3 for x in p) for p in itertools.permutations(range(1, 6))]
def six_hundred_110():
    """#110's frame: the 600-cell in the sum-zero space of R^5 as five S5-orbits A, -A, B, -B, C3 (Section 2)."""
    p2 = PHI * PHI
    def centred(orbit):
        orbit = list(orbit); m = sum((x for x in orbit[0]), ZERO) / 5
        return [tuple(x - m for x in v) for v in orbit]
    A = centred(perms((p2, p2, p2, PHI, ZERO)))
    B = centred(perms((p2, p2, ONE, ONE, ZERO)))
    C3 = [tuple(PHI * (k(1) if t == i else k(-1) if t == j else ZERO) for t in range(5))
          for i in range(5) for j in range(5) if i != j]
    neg = lambda S: [tuple(-x for x in v) for v in S]
    return dedup(A + neg(A) + B + neg(B) + C3), {"A": A, "B": B, "C3": C3}

# ---------------------------------------------------------------- analysis
def reflect(x, r, rr): c = 2 * dot(x, r) / rr; return tuple(a - c * b for a, b in zip(x, r))

def mirrors_of(V):
    keys = {vkey(v) for v in V}
    basis = []
    for v in V:
        if rank(basis + [v], len(v)) > len(basis):
            basis.append(v)
        if len(basis) == 4: break
    lines = {}
    for b in basis:
        for w in V:
            if vkey(w) == vkey(b): continue
            r = sub(b, w); lk = linekey(r)
            if lk in lines: continue
            rr = dot(r, r)
            if all(vkey(reflect(x, r, rr)) in keys for x in V): lines[lk] = r
    return lines

def analyze(name, V, perp, known_f):
    print(f"== {name}: {len(V)} corners"); n = len(V[0])
    check(all(not sum((v[i] for v in V), ZERO) for i in range(n)), "corner centroid is O")
    r2 = {dot(v, v).key() for v in V}; check(len(r2) == 1, "all corners on one sphere")
    mir = mirrors_of(V)
    print(f"  mirrors (exact reflection symmetries): {len(mir)}")
    v0 = V[0]
    d2 = sorted({dot(sub(v, v0), sub(v, v0)) for v in V if vkey(v) != vkey(v0)}, key=lambda x: x)
    mind = d2[0]
    nb = [v for v in V if vkey(v) != vkey(v0) and dot(sub(v, v0), sub(v, v0)) == mind]
    facets = {}
    for a_, b_, c_ in itertools.combinations(nb, 3):
        ns = nullspace([sub(a_, v0), sub(b_, v0), sub(c_, v0)] + perp, n)
        if len(ns) != 1: continue
        h = dot(ns[0], v0)
        if not h: continue
        a = scal(h.inv(), ns[0])
        if all(dot(a, v) <= ONE for v in V): facets[vkey(a)] = a
    front = list(facets.values()); refl = [(r, dot(r, r)) for r in mir.values()]
    while front:
        nf = []
        for a in front:
            for r, rr in refl:
                b = reflect(a, r, rr); kb = vkey(b)
                if kb not in facets: facets[kb] = b; nf.append(b)
        front = nf
    F = list(facets.values())
    check(all(all(dot(a, v) <= ONE for v in V) for a in F), f"all {len(F)} facets exactly supporting (a.x <= 1 on every corner)")
    fv = [frozenset(i for i, v in enumerate(V) if dot(a, v) == ONE) for a in F]
    check(all(rank([sub(V[i], V[min(s)]) for i in s], n) == 3 for s in fv), "every facet is 3-dimensional")
    byv = {}
    for fi, s in enumerate(fv):
        for i in s: byv.setdefault(i, []).append(fi)
    ridges = {}
    for i, fl in byv.items():
        for f, g in itertools.combinations(fl, 2):
            s = fv[f] & fv[g]
            if len(s) < 3 or min(s) != i: continue
            if rank([sub(V[j], V[i]) for j in s], n) == 2: ridges.setdefault(s, set()).update((f, g))
    check(all(len(x) == 2 for x in ridges.values()), "every ridge lies in exactly two facets")
    edges = set()
    for s in ridges:
        P = sorted(s)
        for p, q in itertools.combinations(P, 2):
            s_ = next(t for t in P if t != p and t != q)
            u = sub(V[q], V[p]); uu = dot(u, u); us = dot(u, sub(V[s_], V[p]))
            if all((uu * dot(sub(V[t], V[p]), sub(V[s_], V[p])) - dot(u, sub(V[t], V[p])) * us).sign() > 0
                   for t in P if t != p and t != q):
                edges.add((p, q))
    f = (len(V), len(edges), len(ridges), len(F))
    print(f"  f-vector {f}")
    check(f == known_f, f"f-vector equals the known {known_f}")
    check(f[0] - f[1] + f[2] - f[3] == 0, "Euler f0 - f1 + f2 - f3 = 0")
    check(all(dot(sub(V[p], V[q]), sub(V[p], V[q])) == mind for p, q in edges), "edges are exactly the nearest pairs used for v0")
    # Resonus
    res = {}
    for fi, a in enumerate(F): res.setdefault(linekey(a), []).append(fi)
    rper = sorted({len(x) for x in res.values()})
    print(f"  Resonus: {len(res)} hyperplanes, facets per hyperplane {rper}")
    # Vacuus, two independent normals
    vac = {}; agree = True
    for s, fg in ridges.items():
        f_, g_ = sorted(fg)
        n1 = sub(F[f_], F[g_])
        P = sorted(s); rows = []
        for j in P:
            if rank(rows + [V[j]], n) > len(rows): rows.append(V[j])
            if len(rows) == 3: break
        ns = nullspace(rows + perp, n)
        if len(ns) != 1 or linekey(ns[0]) != linekey(n1): agree = False
        vac.setdefault(linekey(n1), []).append(s)
    check(agree, "Vacuus: normal a_F - a_G equals the null vector of the ridge's corners, for every ridge")
    vper = sorted({len(x) for x in vac.values()})
    print(f"  Vacuus: {len(vac)} plates, ridges per plate {vper}")
    R, Va, M = set(res), set(vac), set(mir)
    out = dict(name=name, f=f, mirrors=len(M), resonus=len(R), resonus_facets_per=rper, vacuus=len(Va), vacuus_ridges_per=vper,
               resonus_and_vacuus=len(R & Va), resonus_on_mirrors=len(R & M), vacuus_on_mirrors=len(Va & M),
               resonus_equals_vacuus=R == Va, resonus_equals_mirrors=R == M, vacuus_equals_mirrors=Va == M)
    print("  " + ", ".join(f"{a}={out[a]}" for a in ["resonus_and_vacuus", "resonus_on_mirrors", "vacuus_on_mirrors",
                                                       "resonus_equals_vacuus", "resonus_equals_mirrors", "vacuus_equals_mirrors"]))
    print(f"PROGRESS {name} done {time.time() - T0:.0f}s")
    return out, dict(V=V, F=F, R=R, Va=Va, M=M, mir=mir, res=res)

S = [(ONE,) * 5]
SMOKE = 'smoke' in sys.argv
results = {}; data = {}
for name, V, perp, f in [
        ("5-cell", five_cell(), S, (5, 10, 10, 5)),
        ("tesseract", tesseract(), [], (16, 32, 24, 8)),
        ("16-cell", sixteen(), [], (8, 24, 32, 16)),
        ("24-cell", twentyfour(), [], (24, 96, 96, 24)),
        ("600-cell", six_hundred(), [], (120, 720, 1200, 600)),
        ("120-cell", one_twenty(), [], (600, 1200, 720, 120)),
        ("4D permutohedron", permutohedron(), S, (120, 240, 150, 30))]:
    if SMOKE and name in ("600-cell", "120-cell"): continue
    results[name], data[name] = analyze(name, V, perp, f)

if SMOKE: sys.exit(0)
print("== theorem checks")
P6, P1 = data["600-cell"], data["120-cell"]
# 600-cell corners are the H4 roots: each reflection in a corner maps the corner set to itself
keys6 = {vkey(v) for v in P6["V"]}
check(all(all(vkey(reflect(x, v, dot(v, v))) in keys6 for x in P6["V"]) for v in P6["V"]),
      "reflection in every 600-cell corner maps the 120 corners to themselves (corners = H4 roots)")
check({linekey(v) for v in P6["V"]} == P6["M"], "the 600-cell's 60 mirrors are exactly the 60 corner lines")
# Theorem 1a independently: 120-cell facet normals are the polar's corners; polar of 120-cell is a 600-cell
check(P1["R"] == P1["M"], "Resonus(120-cell) = its 60 mirrors (normals found from its own facets)")
# frame match: the standard 120-cell (radius sqrt 8) is polar to the 600-cell built with ODD permutations
print("  (the standard 120-cell and the even-permutation 600-cell are in mirror-image frames: shared mirrors",
      len(P1["M"] & P6["M"]), "of 60)")
o6b, P6b = analyze("600-cell, odd permutations (polar frame of the standard 120-cell)", six_hundred(odd=True), [], (120, 720, 1200, 600))
check(P1["M"] == P6b["M"] == {linekey(v) for v in P6b["V"]}, "the standard 120-cell's 60 mirrors = the corner lines of the odd-permutation 600-cell")
check(P6b["R"] == {linekey(v) for v in P1["V"]}, "Resonus(600-cell) normals = the 300 corner lines of the standard 120-cell (its polar), found from facets")
check(P1["R"] == {linekey(v) for v in P6b["V"]}, "Resonus(120-cell) normals = the 120 corners (60 lines) of the 600-cell, found from facets")
check(not (P6["R"] & P6["M"]), "no Resonus hyperplane of the 600-cell is a mirror")
# 25 inscribed 24-cells of the 600-cell and their Resonus (#110's second description of the cross walls)
h = K(Fr(1, 2))
std24 = frozenset(vkey(v) for v in allsp((ONE, ZERO, ZERO, ZERO)) + allsp((h, h, h, h)))
check(std24 <= keys6, "the 24 Hurwitz units are corners of the 600-cell")
cells24 = {std24}; front = [std24]; byk = {vkey(v): v for v in P6["V"]}
refl6 = [(r, dot(r, r)) for r in P6["mir"].values()]
while front:
    nf = []
    for c in front:
        for r, rr in refl6:
            d = frozenset(vkey(reflect(byk[x], r, rr)) for x in c)
            if d not in cells24: cells24.add(d); nf.append(d)
    front = nf
check(len(cells24) == 25, f"the 600-cell holds exactly {len(cells24)} inscribed 24-cells in the orbit (Schoute; Denney et al.)")
sections = {}
for c in cells24:
    Vc = [byk[x] for x in c]
    # facets of a 24-cell: its polar corners; computed exactly from the corners as for the 24-cell above
    o, _ = analyze("inscribed 24-cell", Vc, [], (24, 96, 96, 24))
    for lk in _["R"]: sections.setdefault(lk, 0); sections[lk] += 1
check(len(sections) == 300 and set(sections.values()) == {1}, "the 25 x 12 middle walls of the 24-cells are 300 distinct hyperplanes")
check(set(sections) == P6["R"], "they are exactly the Resonus of the 600-cell (#110's cross walls)")
# #110's own frame (sum-zero R^5, five S5 orbits)
V110, orb = six_hundred_110()
o110, D110 = analyze("600-cell in #110's frame", V110, S, (120, 720, 1200, 600))
results["600-cell (#110 frame)"] = o110
fc = data["5-cell"]
check(fc["R"] <= D110["R"], "the 5-cell's 5 Resonus hyperplanes (coordinate k = mean) are cross walls of #110's 600-cell")
check(fc["Va"] <= D110["M"], "the 5-cell's 10 Vacuus plates (x_i = x_j) are mirrors of #110's 600-cell")
check(fc["Va"] == fc["M"], "the 5-cell's Vacuus = its 10 mirrors (A4 reflection arrangement)")
check(fc["R"] == {linekey(v) for v in fc["V"]},
      "the 5-cell's Resonus normals are its own corners e_k - mean")
pm = data["4D permutohedron"]
subsets = set()
for r in range(1, 5):
    for Ssub in itertools.combinations(range(5), r):
        w = tuple(k(5 if i in Ssub else 0) - r for i in range(5)); subsets.add(linekey(w))
check(pm["R"] == subsets, "Resonus(4D permutohedron) = restricted all-subset arrangement A'_5 (15 hyperplanes sum_S y = 0)")
check(pm["R"] <= pm["Va"], "every Resonus hyperplane of the 4D permutohedron is a Vacuus plate (15 of 65)")

json.dump(results, open(os.path.join(OUT, "resonus_4d.json"), "w"), indent=1, default=str)
print("== table")
for nme, o in results.items():
    print(f"  {nme}: mirrors {o['mirrors']}, Resonus {o['resonus']} {o['resonus_facets_per']}, Vacuus {o['vacuus']} {o['vacuus_ridges_per']}, "
          f"R&V {o['resonus_and_vacuus']}, R on mirrors {o['resonus_on_mirrors']}, V on mirrors {o['vacuus_on_mirrors']}")
print(f"time {time.time() - T0:.0f}s")
print("FINAL ok" if not FAILS else "FINAL FAIL " + "; ".join(FAILS))
sys.exit(1 if FAILS else 0)
