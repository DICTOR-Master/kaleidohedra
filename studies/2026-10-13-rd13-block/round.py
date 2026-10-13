# RD 13 block made rounder (DICTO 2026-10-13): the 13-RD cluster tiles space by an index-13 sublattice of FCC. Every corner of the
# honeycomb moves by a displacement that depends only on its class modulo the block lattice, so the blocks still tile exactly.
# Faces stay flat (each rhombus's 4 corners coplanar), every cell stays convex with a margin, and the block's outside surface is
# made as small as possible (its volume is fixed by the lattice, so least surface = roundest). Coordinates: FCC = integer points
# with even sum (neighbours sqrt2 apart); RD volume 2.
import itertools, json, sys, numpy as np
from scipy.optimize import minimize
W = (1, 3, 9)                                   # the block lattice: x in FCC with W.x = 0 mod 13 (one hand)
B = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]]).T
NB = [np.array(v) for v in itertools.product([-1, 0, 1], repeat=3) if sorted(map(abs, v)) == [0, 1, 1]]
C = [np.zeros(3, int)] + NB
# block lattice basis (3 short vectors)
Lv = sorted([B @ np.array(x) for x in itertools.product(range(-4, 5), repeat=3) if any(x) and np.dot(W, np.linalg.solve(B, B @ np.array(x))).round() % 13 == 0], key=lambda p: p @ p)
Lb = [Lv[0]]
for v in Lv:
    if len(Lb) == 3: break
    if abs(np.linalg.det(np.array(Lb + [v]))) > 1e-9 if len(Lb) == 2 else np.linalg.matrix_rank(np.array(Lb + [v])) == len(Lb) + 1: Lb.append(v)
L = np.array(Lb, float).T
assert abs(abs(np.linalg.det(L)) - 26) < 1e-6, np.linalg.det(L)   # 13 cells of volume 2
Li = np.linalg.inv(L)
def key(x):                                     # a corner's class modulo the block lattice (corners are half-integer points and
    g = np.round(Li @ np.asarray(x, float) * 52).astype(int)   # det L = 26, so their lattice coordinates are multiples of 1/52)
    return tuple(g % 52)
def face(p, n):                                 # the rhombus between cell p and its neighbour p + n
    i, j = [k for k in range(3) if n[k]]; k = 3 - i - j
    ei, ej, ek = np.eye(3)[i], np.eye(3)[j], np.eye(3)[k]
    oa, ob = p + n[i] * ei, p + n[j] * ej
    t1, t2 = p + (n[i] * ei + n[j] * ej + ek) / 2, p + (n[i] * ei + n[j] * ej - ek) / 2
    return [oa, t1, ob, t2]
orbits = {}
def var(x):
    k = key(x)
    if k not in orbits: orbits[k] = len(orbits)
    return orbits[k]
cells = []                                      # per cell: its faces as [(orbit, base position)]
for p in C:
    cells.append([[(var(v), v) for v in face(p.astype(float), n)] for n in NB])
inblock = {tuple(p) for p in C}
outer = [(ci, fi) for ci, p in enumerate(C) for fi, n in enumerate(NB) if tuple(p + n) not in inblock]
print('corner classes', len(orbits), 'outer faces', len(outer))
N = len(orbits)
def pos(d, o, base): return base + d[3 * o:3 * o + 3]
def quad_area(P): return 0.5 * (np.linalg.norm(np.cross(P[1] - P[0], P[2] - P[0])) + np.linalg.norm(np.cross(P[2] - P[0], P[3] - P[0])))
def area(d): return sum(quad_area([pos(d, o, b) for o, b in cells[ci][fi]]) for ci, fi in outer)
faceset = {}
for ci in range(13):
    for fi in range(12):
        key4 = tuple(sorted(o for o, _ in cells[ci][fi]))
        faceset.setdefault(key4, (ci, fi))
def planar(d):
    out = []
    for ci, fi in faceset.values():
        P = [pos(d, o, b) for o, b in cells[ci][fi]]
        out.append(np.linalg.det(np.array([P[1] - P[0], P[2] - P[0], P[3] - P[0]])))
    return np.array(out)
MARGIN = float(sys.argv[1]) if len(sys.argv) > 1 else 0.08
def convex(d):                                  # every other corner of a cell at least MARGIN inside each face's plane
    out = []
    for ci in range(13):
        verts = {o: b for f in cells[ci] for o, b in f}
        V = {o: pos(d, o, b) for o, b in verts.items()}
        cen = np.mean(list(V.values()), axis=0)
        for f in cells[ci]:
            P = [V[o] for o, _ in f]
            n = np.cross(P[2] - P[0], P[1] - P[3]); n /= np.linalg.norm(n)
            if n @ (np.mean(P, axis=0) - cen) < 0: n = -n
            for o, x in V.items():
                if o in [q for q, _ in f]: continue
                out.append(n @ (P[0] - x) - MARGIN)
    return np.array(out)
def cellvol(d, ci):
    verts = {o: pos(d, o, b) for f in cells[ci] for o, b in f}
    cen = np.mean(list(verts.values()), axis=0); vol = 0
    for f in cells[ci]:
        P = [verts[o] for o, _ in f]; m = np.mean(P, axis=0)
        for a, b in [(0, 1), (1, 2), (2, 3), (3, 0)]:
            vol += abs(np.linalg.det(np.array([P[a] - cen, P[b] - cen, m - cen]))) / 6
    return vol
EQUAL = len(sys.argv) > 2 and sys.argv[2] == 'equal'
# 'rdcentre' (DICTO 2026-10-13: "it looks more like an RD than the others"): the centre stays an exact rhombic dodecahedron, its 14
# corners at m + s * (its plain corners), with the size s and the middle m free (4 extra unknowns after the displacements).
RDC = len(sys.argv) > 2 and sys.argv[2] == 'rdcentre'
centre_corners = {o: np.array(b, float) for f in cells[0] for o, b in f}
free = [o for o in range(N) if o not in centre_corners]
# The centre's corners are not unknowns: they follow from its size s and middle m (so nothing is stated twice); x = the other corner
# classes' displacements, then s and m.
def expand(x):
    d = np.zeros(3 * N)
    for i, o in enumerate(free): d[3 * o:3 * o + 3] = x[3 * i:3 * i + 3]
    s_, m = x[3 * len(free)], x[3 * len(free) + 1:3 * len(free) + 4]
    for o, b in centre_corners.items(): d[3 * o:3 * o + 3] = (s_ - 1) * b + m
    return d
def rd_centre(x): return np.zeros(1)
d0 = np.zeros(3 * N)
a0 = area(d0); V = 26.0
iq = lambda a: 36 * np.pi * V ** 2 / a ** 3
print('start: outer area %.4f  roundness (36 pi V^2/S^3) %.4f' % (a0, iq(a0)))
D = expand if RDC else (lambda x: x)
# the centre's own faces are flat by construction in rdcentre mode, so their flatness is not asked again
centre_faces = {tuple(sorted(o for o, _ in f)) for f in cells[0]}
planar_keep = [k for k in faceset if not (RDC and k in centre_faces)]
def planar_used(d):
    out = []
    for k in planar_keep:
        ci, fi = faceset[k]; P = [pos(d, o, b) for o, b in cells[ci][fi]]
        out.append(np.linalg.det(np.array([P[1] - P[0], P[2] - P[0], P[3] - P[0]])))
    return np.array(out)
cons = [{'type': 'eq', 'fun': lambda x: planar_used(D(x))}, {'type': 'ineq', 'fun': lambda x: convex(D(x))}]
if EQUAL: cons.append({'type': 'eq', 'fun': lambda d: np.array([cellvol(D(d), ci) - 2 for ci in range(13)])})
# The RD block is a balance point: start from small random nudges, keep the best that meets every constraint.
best = None
# More and wider starts on request (robustness check): NSEEDS, NOISE, SEED0 in the environment.
import os
NSEEDS, NOISE, SEED0 = int(os.environ.get('NSEEDS', 5)), float(os.environ.get('NOISE', 0.03)), int(os.environ.get('SEED0', 0))
for seed in range(SEED0, SEED0 + NSEEDS):
    start = np.random.default_rng(seed).normal(0, NOISE, 3 * (len(free) if RDC else N))
    if RDC: start = np.concatenate([start, [1.0, 0, 0, 0]])
    res = minimize(lambda x: area(D(x)), start, method='SLSQP', constraints=cons, options={'maxiter': 1500, 'ftol': 1e-10})
    x = D(res.x)
    ok = np.abs(planar(x)).max() < 1e-8 and convex(x).min() > -1e-8 and (not EQUAL or max(abs(cellvol(x, ci) - 2) for ci in range(13)) < 1e-6) and (not RDC or np.abs(rd_centre(res.x)).max() < 1e-7)
    print('seed', seed, res.message, 'area %.4f' % area(x), ('centre scale %.4f' % res.x[3 * len(free)]) if RDC else '', 'ok' if ok else 'FAILS constraints', flush=True)
    if ok and (best is None or area(D(res.x)) < area(D(best.x))): best = res
res = best or res
d = D(res.x)
print(res.message, 'iterations', res.nit)
print('end:   outer area %.4f  roundness %.4f  | max non-flatness %.2e  min convexity margin %.4f' % (area(d), iq(area(d)), np.abs(planar(d)).max(), convex(d).min() + MARGIN))
vols = [cellvol(d, ci) for ci in range(13)]
for ci in []:
    verts = {o: pos(d, o, b) for f in cells[ci] for o, b in f}
    cen = np.mean(list(verts.values()), axis=0); vol = 0
    for f in cells[ci]:
        P = [verts[o] for o, _ in f]
        for a, b in [(0, 1), (1, 2), (2, 3), (3, 0)]:
            vol += abs(np.linalg.det(np.array([P[a] - cen, P[b] - cen, np.mean(P, axis=0) - cen]))) / 6
    vols.append(vol)
print('cell volumes', [round(float(v), 4) for v in vols], 'sum %.6f' % sum(vols))
json.dump({'W': W, 'L': L.T.tolist(), 'margin': MARGIN, 'cells': [[[ (np.array(b) + d[3*o:3*o+3]).tolist() for o, b in f] for f in cells[ci]] for ci in range(13)],
           'centres': [p.tolist() for p in C], 'area0': a0, 'area': area(d), 'volumes': vols}, open(os.environ.get('OUT') or f'rd13-round-m{MARGIN}{"-equal" if EQUAL else "-rdcentre" if RDC else ""}.json', 'w'))
