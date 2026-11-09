# s2b_kis_check.py -- the edge-tangent kis roots of s2 (every edge of the kis at the midsphere distance rho_1): is the polar of the
# kis in the midsphere uniform (all its edges equal)? Is the apex on a corner (degenerate)? Floats (1e-9). Study 2026-11-09-regular-stars-census.
# Polar: each kis triangle (apex t.c_f, a, b) -> its pole; kis edge ab (between faces f, g) -> polar edge (pole(f,ab), pole(g,ab));
# kis edge (apex_f, a) -> polar edge between the poles of the two triangles of f at a.
# Usage: ~/geom/bin/python -u s2b_kis_check.py <flags.json> <s2_census3d.json> <out json>
import sys, json, itertools
import numpy as np, sympy as sp
from regstar import *
FL, CEN, OUT = sys.argv[1:4]
flags = {r['symbol']: r for r in json.load(open(FL)) if r['d'] == 3}
cen = json.load(open(CEN)); out = []; ok = True
def orbit(gens, x):
    seen = [x]; fr = [x]
    while fr:
        nx = []
        for y in fr:
            for M in gens:
                z = M @ y
                if not any(np.abs(z - s).max() < 1e-9 for s in seen): seen.append(z); nx.append(z)
        fr = nx
    return seen
for rec in cen:
    row = flags[rec['symbol']]; ms = [vp(m) for m in row['mirrors']]; q = [flv(vp(x)) for x in row['q']]
    Ms = [refl_mat(m) for m in ms]
    poly = [q[0]]
    while True:
        nxt = Ms[1] @ (Ms[0] @ poly[-1])
        if np.abs(nxt - poly[0]).max() < 1e-9: break
        poly.append(nxt)
    # all faces: images of (centre, polygon) under the group
    G = group_float(Ms); faces = []
    for g in G:
        c = g @ q[2]
        if not any(np.abs(c - f[0]).max() < 1e-9 for f in faces): faces.append((c, [g @ p for p in poly]))
    V = orbit(Ms, q[0]); R = np.linalg.norm(q[0]); rho1 = np.linalg.norm(q[1])
    for e in rec['star_line_events']:
        if not e['kind'].startswith('metric'): continue
        t = e['t_f']; tris = []
        for c, P in faces:
            A = t * c
            for i in range(len(P)): tris.append((A, P[i], P[(i + 1) % len(P)], c))
        def pole(T):
            A, a, b, _ = T; n = np.cross(a - A, b - A); d = n @ a; return n / d * rho1 ** 2
        # kis edges: distances from 0 (tangency check) and polar edge lengths
        dist = []; lens = []
        for T in tris:
            A, a, b, c = T
            for X, Y in ((A, a), (a, b)):
                u = Y - X; dist.append(np.linalg.norm(np.cross(X, u)) / np.linalg.norm(u))
        poles = [pole(T) for T in tris]
        for (i, T), (j, U) in itertools.combinations(enumerate(tris), 2):
            sh = [p for p in (T[1], T[2]) if any(np.abs(p - r).max() < 1e-9 for r in (U[1], U[2]))]
            if len(sh) == 2 or (len(sh) == 1 and np.abs(T[0] - U[0]).max() < 1e-9):
                lens.append(np.linalg.norm(poles[i] - poles[j]))
        apex_on_corner = any(np.abs(t * faces[0][0] - v).max() < 1e-9 for v in V)
        tangent = bool(np.ptp(dist) < 1e-9 * R and abs(dist[0] - rho1) < 1e-9 * R)
        uniform = bool(np.ptp(lens) < 1e-9 * max(lens))
        rr = dict(symbol=rec['symbol'], name=rec['name'], t=e['t'], t_f=t, edges_tangent=tangent, polar_edges_equal=uniform,
                  apex_on_corner=bool(apex_on_corner), polar_edge_lengths=[float(min(lens)), float(max(lens))], n_polar_edges=len(lens))
        ok &= tangent
        print(rr, flush=True); out.append(rr)
json.dump(out, open(OUT, 'w'), indent=1)
print('FINAL ok' if ok else 'FINAL FAIL: an edge-tangent root is not tangent')
