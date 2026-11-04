#!/usr/bin/env python3
"""Halves census (DICTO 4 Nov 2026: "half pieces are a blind spot in our concordance"). For each convex solid and each rotation axis through its
centre (axes from its symmetry: directions of corners, face centres and edge midpoints; order n found numerically), cut by the plane through the
centre across the axis. If the two halves are congruent and the cut face is an n-gon with n-fold turn, rejoin the halves turned by π/n (gyro <-> ortho):
report the section, whether the new solid is convex, whether it is new (not congruent to the original), its Dehn status. Classical names: ortho/gyro.
Calibration: cuboctahedron (3-fold) -> anticuboctahedron J27 (convex); RD (3-fold) -> TRD (convex); TO (3-fold) -> non-convex (found 4 Nov)."""
import sys, json, math, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
sys.argv = [sys.argv[0], 'x', '8', '300']; exec(open('scripts/dehn.py').read().split("if __name__")[0])
phi = (1 + 5**.5)/2
def perms(v, even=False):
    out = set()
    for p in itertools.permutations(range(3)):
        if even and p not in [(0,1,2),(1,2,0),(2,0,1)]: continue
        for s in itertools.product((1, -1), repeat=3): out.add(tuple(s[i]*v[p[i]] for i in range(3)))
    return list(out)
SOL = {
 'cube': perms((1,1,1)), 'octahedron': perms((1,0,0)), 'tetrahedron': [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)],
 'icosahedron': perms((0,1,phi), True), 'dodecahedron': perms((1,1,1)) + perms((0,1/phi,phi), True),
 'cuboctahedron': perms((1,1,0)), 'truncated octahedron': perms((0,1,2)), 'rhombic dodecahedron': perms((1,0,0)) and perms((2,0,0)) + perms((1,1,1)),
 'rhombicuboctahedron': perms((1,1,1+2**.5)), 'icosidodecahedron': perms((phi,0,0)) + perms((.5,phi/2,phi**2/2), True),
 'truncated cube': perms((2**.5-1,1,1)), 'truncated tetrahedron': [p for p in perms((1,1,3)) if (p[0]*p[1]*p[2]) > 0],
 'hexagonal prism': [(math.cos(k*math.pi/3), math.sin(k*math.pi/3), z) for k in range(6) for z in (-.5, .5)],
}
try:
    d = json.load(open('data/og-family-solids.json'))
    for nm in d['order']: SOL[nm] = d['solids'][nm]['v']
except Exception as e: print('OG data', e)
def frame(a):
    a = a/np.linalg.norm(a); u = np.cross(a, [1, 0, 0] if abs(a[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); return np.array([u, np.cross(a, u), a])
def sig(P): D = np.linalg.norm(P[:, None] - P[None], axis=2); return tuple(sorted(np.round(D.ravel(), 5)))
def rz(t): return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
out = []
import os
ONLY = os.environ.get('ONLY')
for name, V in SOL.items():
    if ONLY and ONLY not in name: continue
    P = np.unique(np.round(np.array(V, float), 10), axis=0); P = P - P[ConvexHull(P).vertices].mean(0); h = ConvexHull(P); P = P[h.vertices]; h = ConvexHull(P)
    cand = [p for p in P] + [P[s].mean(0) for s in h.simplices] + [(p + q)/2 for p, q in itertools.combinations(P, 2) if abs(np.linalg.norm(p - q) - min(np.linalg.norm(x - y) for x, y in itertools.combinations(P, 2))) < 1e-6]
    axes = []
    for a in cand:
        if np.linalg.norm(a) < 1e-9: continue
        a = a/np.linalg.norm(a)
        if any(abs(abs(a @ b) - 1) < 1e-7 for b in axes): continue
        axes.append(a)
    seen = set()
    for a in axes:
        F = frame(a); Q = P @ F.T
        n = max([k for k in (2, 3, 4, 5, 6) if all(np.min(np.linalg.norm(Q - p, axis=1)) < 1e-4 for p in Q @ rz(2*math.pi/k).T)], default=1)
        if n < 2: continue
        hq = ConvexHull(Q)
        def half(top):
            Hs = np.vstack([hq.equations, [0, 0, -1 if top else 1, 0]]); x = HalfspaceIntersection(Hs, np.array([0, 0, 1e-3 if top else -1e-3])).intersections
            return np.unique(np.round(x, 9), axis=0)
        try: T, B = half(True), half(False)
        except Exception: continue
        if not (len(T) == len(B) and all(np.min(np.linalg.norm(B - p, axis=1)) < 1e-4 for p in -T)): continue
        sec = T[np.abs(T[:, 2]) < 1e-9]
        key = (n, len(sec), sig(T)[:40])
        if key in seen: continue
        seen.add(key)
        U = np.unique(np.round(np.vstack([T, B @ rz(math.pi/n).T]), 6), axis=0); hu = ConvexHull(U); conv = abs(hu.volume - hq.volume) < 1e-6*hq.volume
        new = sig(U[hu.vertices]) != sig(Q) if conv else True
        rec = {'solid': name, 'axis_order': n, 'section_corners': int(len(sec)), 'turn_deg': round(180/n, 3), 'convex': bool(conv), 'new_solid': bool(new)}
        if conv and new:
            X, Fc = hull_faces(U[hu.vertices]); dd = dehn(X, Fc); fs = {}
            for eq, sm in zip(hu.equations, hu.simplices): fs.setdefault(tuple(np.round(eq, 6)), set()).update(sm)
            rec.update(corners=int(len(hu.vertices)), faces=sorted(len(x) for x in fs.values()), dehn_zero=dd['dehn_zero'])
        out.append(rec); print(json.dumps(rec), flush=True)
json.dump(out, open('data/halves.json', 'w'), indent=1)
