#!/usr/bin/env python3
"""Can anticuboctahedra (J27) and octahedra fill space, as cuboctahedra and octahedra do (rectified cubic)? #92 v2 Theorem 10 lead.
On a stacking, whole J27 (or CO) of the centre pyramids sit at chosen centres v; every tetrahedron must lie in exactly one solid (one centre among
its 4 corners); an octahedron at a centre is cut across the axis through that centre, so among its 6 corners at most one antipodal PAIR can be centres
(or one corner). Integer program (scipy milp) on a periodic box; reports feasibility for hcp (all J27), fcc (all CO: control, must be feasible) and others."""
import itertools, math, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
POS = {'A': (0.0, 0.0), 'B': (0.5, math.sqrt(3)/6), 'C': (1.0, math.sqrt(3)/3)}
def build(word, nx, ny):
    """periodic box: nx × ny in-plane cells, len(word) layers (word must close periodically)"""
    pts = []; H = math.sqrt(2/3)
    for z, L in enumerate(word):
        ox, oy = POS[L]
        for a in range(nx):
            for b in range(ny): pts.append((a, b, z, ox, oy))
    idx = {}
    def coord(a, b, z, ox, oy): return np.array([ox + a + b/2, oy + b*math.sqrt(3)/2, z*H])
    P = np.array([coord(*p) for p in pts]); n = len(P); Lz = len(word)*H
    A1 = np.array([nx, 0, 0.]); A2 = np.array([ny/2, ny*math.sqrt(3)/2, 0]); A3 = np.array([0, 0, Lz])
    def d(i, j):
        v = P[j] - P[i]; best = 9
        for s, t, u in itertools.product((-1, 0, 1), repeat=3): best = min(best, np.linalg.norm(v + s*A1 + t*A2 + u*A3))
        return best
    nb = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if abs(d(i, j) - 1) < 1e-6: nb[i].add(j); nb[j].add(i)
    tets = {tuple(sorted(q)) for i in range(n) for q in itertools.combinations(sorted(nb[i] | {i}), 4) if i in q and all(b in nb[a] for a, b in itertools.combinations(q, 2))}
    octs = set()
    for i in range(n):
        for q in itertools.combinations(sorted(nb[i]), 4):          # 4 neighbours of i forming a square -> octahedron i, square, opposite
            e = [b in nb[a] for a, b in itertools.combinations(q, 2)]
            if sum(e) != 4: continue
            opp = set.intersection(*[nb[x] for x in q]) - {i}
            for o in opp:
                if o not in nb[i] and all(o in nb[x] for x in q):
                    octs.add(tuple(sorted((i, o) + q)))
    # antipodal pairs in an octahedron = the 3 non-adjacent pairs
    return n, sorted(tets), sorted(octs), nb
def solve(word, nx, ny):
    n, tets, octs, nb = build(word, nx, ny)
    rows, lo, hi = [], [], []
    for t in tets:
        r = np.zeros(n); r[list(t)] = 1; rows.append(r); lo.append(1); hi.append(1)
    for o in octs:
        pairs = [(a, b) for a, b in itertools.combinations(o, 2) if b not in nb[a]]
        for (a, b), (c, d_) in itertools.combinations(pairs, 2):      # centres in two different antipodal pairs: forbidden
            for x, y in itertools.product((a, b), (c, d_)):
                r = np.zeros(n); r[[x, y]] = 1; rows.append(r); lo.append(0); hi.append(1)
    res = milp(c=np.zeros(n), constraints=LinearConstraint(np.array(rows), lo, hi), integrality=np.ones(n), bounds=Bounds(0, 1))
    ok = res.status == 0
    print(f'{word:8s} box {nx}x{ny}: points {n}, tetrahedra {len(tets)}, octahedra {len(octs)} -> feasible {ok}' + (f', centres {int(round(res.x.sum()))} = {res.x.sum()/n:.3f} of points' if ok else ''))
    return ok
for word, nx, ny in (('ABC', 4, 4), ('ABC', 2, 2), ('AB', 4, 4), ('AB', 2, 2), ('AB', 6, 6), ('ABCB', 4, 4)):
    solve(word, nx, ny)
