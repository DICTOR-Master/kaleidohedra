#!/usr/bin/env python3
"""Interlocking of DICTO's pieces (DICTO 4 Nov: "test the pyramids and admiral caps for interlocking"). Translational kinematic test (Dyskin et al. 2003 sense, rotations not yet):
a body is LOCKED if no velocity v != 0 satisfies v·n <= 0 for every outward normal n of its faces that touch a neighbour (area contact); the layer's outer ring is held fixed.
Bodies are unions of convex parts (a cap = its two tetrahedra). Cases: calibration (Dyskin tetrahedra), octet slab cut into centre pyramids, a cube layer cut into C6
pyramids, the #47 Admiral slab (engine data: icosahedra, caps, tetrahedron face pyramids)."""
import itertools, math, json, os, sys
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
EPS = 1e-7
def faces(P):
    h = ConvexHull(P); out = {}
    for s, eq in zip(h.simplices, h.equations):
        k = tuple(np.round(eq, 6))
        if k not in out: out[k] = [eq[:3], -eq[3], set()]
        out[k][2].update(s.tolist())
    res = []
    for n, d, idx in out.values():
        F = P[sorted(idx)]; c = F.mean(0); u = F[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        F = F[np.argsort([math.atan2((p - c) @ w, (p - c) @ u) for p in F])]; res.append((n, d, F))
    return res
def inside_poly(p, F, n):
    for i in range(len(F)):
        a, b = F[i], F[(i+1) % len(F)]
        if np.cross(b - a, p - a) @ n < -1e-9: return False
    return True
def touching(fa, fb):
    """face fa of one part and fb of another: opposite normals, same plane, polygons overlap with area"""
    na, da, Fa = fa; nb, db, Fb = fb
    if np.linalg.norm(na + nb) > 1e-6 or abs(da + db) > 1e-6: return False
    c = Fa.mean(0); pts = [c] + [c + 0.9*(v - c) for v in Fa] + [Fb.mean(0)]
    return any(inside_poly(p, Fb, nb) and inside_poly(p, Fa, na) for p in pts)
def locked_report(bodies, test_ids):
    """bodies: list of lists of convex vertex arrays"""
    F = [[faces(np.array(p, float)) for p in body] for body in bodies]
    cent = np.array([np.mean(np.vstack(b), 0) for b in bodies]); rad = np.array([np.max(np.linalg.norm(np.vstack(b) - cent[i], axis=1)) for i, b in enumerate(bodies)])
    out = []
    for i in test_ids:
        cons = []
        near = [j for j in range(len(bodies)) if j != i and np.linalg.norm(cent[j] - cent[i]) < rad[i] + rad[j] + 1e-6]
        for fa in [f for part in F[i] for f in part]:
            if any(touching(fa, fb) for j in near for part in F[j] for fb in part): cons.append(fa[0])
        if not cons: out.append('free (no contacts)'); continue
        A = np.array(cons); free = None
        for d in np.vstack([np.eye(3), -np.eye(3)]):
            r = linprog(np.zeros(3), A_ub=A, b_ub=np.zeros(len(A)), A_eq=[d], b_eq=[1], bounds=[(-1, 1)]*3, method='highs')
            if r.status == 0: free = r.x; break
        out.append('locked' if free is None else 'free')
    return out
def summary(name, bodies, test_ids, kinds):
    rep = locked_report(bodies, test_ids); tally = {}
    for i, r in zip(test_ids, rep): tally.setdefault(kinds[i], {}).setdefault(r, 0); tally[kinds[i]][r] += 1
    print(f'{name}: {tally}', flush=True); return tally
R = {}
# 1. calibration: Dyskin tetrahedra, square midsections in a checkerboard, neighbours turned 90 deg
h = 1/math.sqrt(2)
def tet(x, y, turn):
    V = np.array([(1, 0, h), (-1, 0, h), (0, 1, -h), (0, -1, -h)], float)/2
    if turn: V = V[:, [1, 0, 2]]
    return V + [x, y, 0]
bodies = []; kinds = []
for a in range(-4, 5):
    for b in range(-4, 5):
        bodies.append([tet(0.5*a, 0.5*b, (a + b) % 2)]); kinds.append('T')   # midsection squares of side 1/2 tile the plane
cent = [np.mean(b[0], 0) for b in bodies]; ids = [i for i, c in enumerate(cent) if np.linalg.norm(c[:2]) < 1.2]
R['dyskin_tetrahedra'] = summary('calibration, Dyskin tetrahedron layer', bodies, ids, kinds)
# 2. octet slab (two layer planes A, B) cut into centre pyramids
H = math.sqrt(2/3); POS = {'A': (0, 0), 'B': (.5, math.sqrt(3)/6)}
pts = np.array([np.array([POS[L][0] + a + b/2, POS[L][1] + b*math.sqrt(3)/2, z*H]) for z, L in enumerate('AB') for a in range(-5, 6) for b in range(-5, 6)])
n = len(pts); nbm = np.abs(np.linalg.norm(pts[:, None] - pts[None], axis=2) - 1) < 1e-9
adj = [np.where(nbm[i])[0].tolist() for i in range(n)]
tets = {tuple(sorted(q)) for i in range(n) for q in itertools.combinations([i] + adj[i], 4) if all(nbm[a, b] for a, b in itertools.combinations(q, 2))}
octs = set()
for i in range(n):
    for q in itertools.combinations(adj[i], 4):
        if sum(nbm[a, b] for a, b in itertools.combinations(q, 2)) != 4: continue
        for o in set.intersection(*[set(adj[x]) for x in q]) - {i}:
            if not nbm[i, o]: octs.add(tuple(sorted((i, o) + q)))
def pyramids(V):
    c = V.mean(0); return [np.vstack([c, F]) for n_, d_, F in faces(V)]
bodies = []; kinds = []
for t in tets:
    for p in pyramids(pts[list(t)]): bodies.append([p]); kinds.append('T pyramid')
for o in octs:
    for p in pyramids(pts[list(o)]): bodies.append([p]); kinds.append('O pyramid')
cent = [np.mean(b[0], 0) for b in bodies]; ids = [i for i, c in enumerate(cent) if np.linalg.norm(c[:2]) < 1.3]
R['octet_slab_pyramids'] = summary('octet slab cut into centre pyramids', bodies, ids, kinds)
# 3. one layer of unit cubes cut into their six C6 pyramids
bodies = []; kinds = []
for a in range(-3, 4):
    for b in range(-3, 4):
        C = np.array(list(itertools.product((0, 1), repeat=3)), float) + [a, b, 0]
        for p in pyramids(C): bodies.append([p]); kinds.append('C6 (base %s)' % ('on layer plane' if abs(abs(np.mean(p[1:], 0)[2] - 0.5) - 0.5) < 1e-9 else 'inside'))
cent = [np.mean(b[0], 0) for b in bodies]; ids = [i for i, c in enumerate(cent) if np.linalg.norm(c[:2]) < 1.6]
R['cube_layer_pyramids'] = summary('cube layer cut into C6 pyramids', bodies, ids, kinds)
# 4. the #47 Admiral slab from the engine (icosahedra, Admiral caps as rigid pairs of tetrahedra, tetrahedron face pyramids)
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admiral-network-pieces.json')
if os.path.exists(src):
    P = json.load(open(src)); bodies = []; kinds = []
    for p in P:
        V = np.unique(np.round(np.array([c for f in p['faces'] for c in f], float), 9), axis=0)
        if p['kind'] == 'A':
            eqf = [np.array(f, float) for f in p['faces'] if len(f) == 3 and all(abs(np.linalg.norm(np.array(f[k]) - np.array(f[(k+1) % 3])) - 1) < 1e-6 for k in range(3))]
            assert len(eqf) == 2, 'cap equilateral faces'
            A1 = {tuple(np.round(v, 9)) for v in eqf[0]}; A2 = {tuple(np.round(v, 9)) for v in eqf[1]}
            e = [np.array(v) for v in A1 & A2]; v1 = [np.array(v) for v in A1 - A2][0]; v2 = [np.array(v) for v in A2 - A1][0]
            apex = [v for v in V if not any(np.allclose(v, q) for q in e + [v1, v2])][0]
            best = [np.array([apex, e[0], e[1], v1]), np.array([apex, e[0], e[1], v2])]
            bodies.append(best); kinds.append('Admiral Cap')
        else:
            bodies.append([V]); kinds.append({'I': 'icosahedron', 'Q′': 'tetrahedron face pyramid'}.get(p['kind'], p['kind']))
    cent = np.array([np.mean(np.vstack(b), 0) for b in bodies]); c0 = cent.mean(0)
    ids = [i for i, c in enumerate(cent) if np.linalg.norm((c - c0)[:2]) < 1.8]
    R['admiral_slab'] = summary('#47 Admiral slab (engine)', bodies, ids, kinds)
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interlock-pieces.json'), 'w'), indent=1)
