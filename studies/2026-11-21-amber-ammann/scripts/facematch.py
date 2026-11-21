"""Amber-Ammann: do the outer patterns of two neighbouring cells agree on their shared face?  (If yes, the pieces of the two cells meet
top to top, edge to edge, across that face; if not, the pieces still fill both cells, but their tops do not line up across the face.)
Exact in Q(sqrt5).  For every one of the 20 cell orientations and each of its 6 faces, the outer pattern on that face (Voronoi cells of the
seeds cut by the face, exactly as ammann_cell.py) is computed once, relative to the cell centre, in patch units (mould = the patch's
rhombohedron, edge |e|; the solid scaled by 3/s).  Each shared face of the patch is then compared from both sides after translation:
patterns are sets of polygons (collinear vertices removed), compared exactly.
Usage: python facematch.py SOLID SCALE SEED   (SCALE = S0 or S65; s from data/s0.txt)."""
import json, os, sys, itertools
from collections import Counter
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
from ammann_cell import Q, dot, cross, vsub, vadd, vsc, det3, clip, area2, IH, act
from aligned import aligned
from tiling import E, TRIPLES
def key(v): return tuple(x.key() for x in v)
def fl(v): return np.array([float(x) for x in v])
def parseQ(t):
    t = t.strip()
    if "r5" not in t: return Q(Fr(t))
    a, b = t[:-2].rsplit("+", 1) if "+" in t[1:] else ("0", t[:-2])
    return Q(Fr(a), Fr(b))
solid, scale, seed = sys.argv[1], sys.argv[2], sys.argv[3]
for line in open(os.path.join(HERE, "../data/s0.txt")):
    w = line.split()
    if w[0] == solid: S = Q(Fr(w[1]), Fr(w[2]))
if scale == "S65": S = S*Fr(6, 5)
C = aligned(solid, IH, act); V = [vsc(Q(3)/S, v) for v in C["V"]]
cent = [[sum((V[i][j] for i in f), Q(0))/len(f) for j in range(3)] for f, k in C["faces"]]
patch = json.load(open(os.path.join(HERE, "../data/patch.json")))
tiles = patch["tiles"]
def P3(v6): return [sum((E[i][r]*v6[i] for i in range(6)), Q(0)) for r in range(3)]
def mould(A):   # halfspaces of the patch rhombohedron spanned by e_a, e_b, e_c, centred at 0
    H = []
    for k in range(3):
        n = cross(E[A[(k+1) % 3]], E[A[(k+2) % 3]]); h = dot(n, E[A[k]])
        if h.sign() < 0: n = vsc(-1, n); h = -h
        H.append((n, h/2)); H.append((vsc(-1, n), h/2))
    return H
def seeds_for(A):
    if seed == "cen": return cent
    H = mould(A); out = []
    for c0 in cent:
        t = None
        for n, c in H:
            d = dot(n, c0)
            if d.sign() > 0:
                r = c/d
                if t is None or (r - t).sign() < 0: t = r
        out.append(vsc(t, c0))
    return out
def canon(P):
    P = [p for i, p in enumerate(P) if key(p) != key(P[i-1])]
    out = []
    for i, p in enumerate(P):
        a, b = P[i-1], P[(i+1) % len(P)]
        if not all(x.sign() == 0 for x in cross(vsub(p, a), vsub(b, p))): out.append(p)
    return out
def pattern(face, sd):
    """face: exact polygon (relative to the cell centre); sd: seeds. Returns list of polygons (exact)."""
    sf = np.array([fl(p) for p in sd]); sq = [dot(p, p) for p in sd]
    pf = np.array([fl(p) for p in face]); cen_f = pf.mean(0); rad = np.linalg.norm(pf - cen_f, axis=1).max()
    out = []
    for F in range(len(sd)):
        P = face
        for G in sorted(range(len(sd)), key=lambda G: np.linalg.norm(sf[G] - sf[F])):
            if G == F: continue
            a = 2*(sf[G] - sf[F]); b = sf[G] @ sf[G] - sf[F] @ sf[F]
            if a @ cen_f + np.linalg.norm(a)*rad < b - 1e-7: continue
            P = clip(P, vsc(2, vsub(sd[G], sd[F])), sq[G] - sq[F])
            if len(P) < 3: break
        if len(P) >= 3 and any(x.sign() != 0 for x in area2(P)): out.append(canon(P))
    return out
# per (triple, face given by (l, side)) pattern relative to the cell centre
cache = {}
def face_rel(A, l, side):
    """face of the rhombohedron (centred at 0) opposite... : the face spanned by the other two vectors, on side -1/2 or +1/2 of e_l"""
    i, j = [a for a in A if a != l]
    base = vsc(Fr(1, 2) if side else Fr(-1, 2), E[l])
    return [vadd(base, vadd(vsc(Fr(sa, 2), E[i]), vsc(Fr(sb, 2), E[j]))) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
def pat(A, l, side):
    k = (tuple(A), l, side)
    if k not in cache: cache[k] = pattern(face_rel(A, l, side), seeds_for(A))
    return cache[k]
match = Counter(); total = Counter()
for t1, t2, pts in patch["shared"]:
    pts6 = [tuple(p) for p in pts]
    res = []
    for ti in (t1, t2):
        t = tiles[ti]; A = t["A"]; n = t["n"]
        c = [parseQ(x) for x in t["centre_exact"]]
        # which face: the vector of A not spanned by the face, and the side
        for l in A:
            if all(p[l] == n[l] for p in pts6): side = 0; break
            if all(p[l] == n[l] + 1 for p in pts6): side = 1; break
        polys = pat(A, l, side)
        res.append(frozenset(frozenset(key(vadd(p, c)) for p in P) for P in polys))
    kinds = "".join(sorted(tiles[t1]["kind"] + tiles[t2]["kind"]))
    total[kinds] += 1
    if res[0] == res[1]: match[kinds] += 1
print(f"{solid} {scale} {seed}: shared faces whose outer patterns agree from both sides: " +
      ", ".join(f"{k} {match[k]}/{total[k]}" for k in sorted(total)) + f"; all {sum(match.values())}/{sum(total.values())}")
