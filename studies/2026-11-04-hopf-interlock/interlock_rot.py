#!/usr/bin/env python3
"""Rotational interlocking check (DICTO 4 Nov: "run the rotation check on the admiral slab"). Infinitesimal rigid motion (v, ω) of one body, neighbours fixed:
non-penetration at every corner of every contact polygon q: (v + ω × (q − c))·n <= 0 (n outward normal of the body's face). Contact polygons = exact clipping of the two
touching faces in their common plane (Sutherland–Hodgman). LOCKED iff the only solution is (v, ω) = 0, tested by LP with each of the 12 unit directions ±e_i in R^6 as d·(v,ω) = 1.
Reuses faces(), touching() and the case builders of interlock_pieces.py."""
import os, sys, math, json, itertools
import numpy as np
from scipy.optimize import linprog
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interlock_pieces.py')).read()
g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interlock_pieces.py')}
exec(src.split("R = {}")[0], g)
faces, touching = g['faces'], g['touching']
def clip(Fa, Fb, n):
    """intersection polygon of convex polygons Fa, Fb lying in one plane with normal n (both oriented CCW about n for Fa; Fb reversed)"""
    poly = [p for p in Fa]; Fb = Fb[::-1]          # Fb is CCW about -n; reverse to CCW about n
    for i in range(len(Fb)):
        a, b = Fb[i], Fb[(i+1) % len(Fb)]; out = []
        inside = lambda p: np.cross(b - a, p - a) @ n >= -1e-12
        for j in range(len(poly)):
            p, q = poly[j], poly[(j+1) % len(poly)]
            if inside(q):
                if not inside(p): out.append(inter(p, q, a, b, n))
                out.append(q)
            elif inside(p): out.append(inter(p, q, a, b, n))
        poly = out
        if not poly: break
    return poly
def inter(p, q, a, b, n):
    d1 = np.cross(b - a, p - a) @ n; d2 = np.cross(b - a, q - a) @ n; t = d1/(d1 - d2); return p + t*(q - p)
def rot_locked(bodies, i, near):
    c = np.mean(np.vstack(bodies[i]), 0); rows = []
    for part in bodies[i]:
        for fa in faces(np.array(part, float)):
            for j in near:
                for pj in bodies[j]:
                    for fb in faces(np.array(pj, float)):
                        if touching(fa, fb):
                            for q in clip(fa[2], fb[2], fa[0]):
                                r = q - c; rows.append(np.r_[fa[0], np.cross(r, fa[0])])   # (v + ω×r)·n = v·n + ω·(r×n)
    if not rows: return 'free (no contacts)'
    A = np.array(rows)
    for d in np.vstack([np.eye(6), -np.eye(6)]):
        r = linprog(np.zeros(6), A_ub=A, b_ub=np.zeros(len(A)) + 1e-12, A_eq=[d], b_eq=[1], bounds=[(-1, 1)]*6, method='highs')
        if r.status == 0: return 'free'
    return 'locked'
def run(name, bodies, ids, kinds):
    cent = np.array([np.mean(np.vstack(b), 0) for b in bodies]); rad = np.array([np.max(np.linalg.norm(np.vstack(b) - cent[k], axis=1)) for k, b in enumerate(bodies)])
    tally = {}
    for i in ids:
        near = [j for j in range(len(bodies)) if j != i and np.linalg.norm(cent[j] - cent[i]) < rad[i] + rad[j] + 1e-6]
        r = rot_locked(bodies, i, near); tally.setdefault(kinds[i], {}).setdefault(r, 0); tally[kinds[i]][r] += 1
    print(f'{name} (translations + rotations): {tally}', flush=True); return tally
# calibration: Dyskin tetrahedra
h = 1/math.sqrt(2)
def tet(x, y, turn):
    V = np.array([(1, 0, h), (-1, 0, h), (0, 1, -h), (0, -1, -h)], float)/2
    if turn: V = V[:, [1, 0, 2]]
    return V + [x, y, 0]
bodies = []; kinds = []
for a in range(-4, 5):
    for b in range(-4, 5): bodies.append([tet(0.5*a, 0.5*b, (a + b) % 2)]); kinds.append('T')
cent = [np.mean(b[0], 0) for b in bodies]; ids = [i for i, cc in enumerate(cent) if np.linalg.norm(cc[:2]) < 1.2]
R = {'dyskin': run('calibration, Dyskin tetrahedra', bodies, ids, kinds)}
# Admiral slab: rebuild bodies exactly as in interlock_pieces.py
P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admiral-network-pieces.json'))); bodies = []; kinds = []
for p in P:
    V = np.unique(np.round(np.array([cc for f in p['faces'] for cc in f], float), 9), axis=0)
    if p['kind'] == 'A':
        eqf = [np.array(f, float) for f in p['faces'] if len(f) == 3 and all(abs(np.linalg.norm(np.array(f[k]) - np.array(f[(k+1) % 3])) - 1) < 1e-6 for k in range(3))]
        A1 = {tuple(np.round(v, 9)) for v in eqf[0]}; A2 = {tuple(np.round(v, 9)) for v in eqf[1]}
        e = [np.array(v) for v in A1 & A2]; v1 = [np.array(v) for v in A1 - A2][0]; v2 = [np.array(v) for v in A2 - A1][0]
        apex = [v for v in V if not any(np.allclose(v, q) for q in e + [v1, v2])][0]
        bodies.append([np.array([apex, e[0], e[1], v1]), np.array([apex, e[0], e[1], v2])]); kinds.append('Admiral Cap')
    else:
        bodies.append([V]); kinds.append({'I': 'icosahedron', 'Q′': 'tetrahedron face pyramid'}.get(p['kind'], p['kind']))
cent = np.array([np.mean(np.vstack(b), 0) for b in bodies]); c0 = cent.mean(0)
ids = [i for i, cc in enumerate(cent) if np.linalg.norm((cc - c0)[:2]) < 1.8]
R['admiral'] = run('#47 Admiral slab', bodies, ids, kinds)
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interlock-rot.json'), 'w'), indent=1)
