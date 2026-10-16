# Render data for the P4 figures (Fable review 2, 2026-10-16): every interlock piece of both settings with cleaned float corners
# (duplicates and edge-only points dropped, as in interlock_kinds.py), whole faces merged by plane, its original layer o and its kind k
# (rank by exact volume, largest first, matching Tables 1-2), plus candidate oblique bearings (a two-fold axis projected as up) and the
# five-fold axis nearest each bearing for the cake-slice wedge. -> data/p4-render-<setting>.json
import json, sys, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, '../_lib'); import geomcheck as gc
C = {n: np.array(V) for n, V in json.load(open('data/orig-chain.json'))}
ax = gc.icosa_axes(C['icosahedron']); A5, A3, A2 = (np.array(ax[k]) for k in '532')
def clean(P):
    U = []
    for x in P:
        if all(np.linalg.norm(x - y) > 1e-6 for y in U): U.append(x)
    P = np.array(U); h = ConvexHull(P); keep = []
    for i in range(len(P)):
        ns = [e[:3] for e in h.equations if abs(P[i] @ e[:3] + e[3]) < 1e-7]
        if np.linalg.matrix_rank(np.array(ns), tol=1e-6) == 3: keep.append(i)
    return P[keep]
def faces(V):
    h = ConvexHull(V); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    F = []
    for e in pl:
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]; Q = V[idx]; c = Q.mean(0)
        a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return F
a5 = A5[0]; a3 = max(A3, key=lambda v: v @ a5); a2 = max(A2, key=lambda v: v @ (a5 + a3))
nrm = lambda v: v / np.linalg.norm(v)
B = {'A': nrm(0.8 * a3 + 0.5 * a5), 'B': nrm(a5 + 0.45 * a3), 'C': nrm(a2 + 0.35 * a3 + 0.15 * a5)}
views = {}
for k, d in B.items():
    u = min(A2, key=lambda v: abs(v @ d)); u = nrm(u - (u @ d) * d)
    if u @ np.array([0, 0, 1.0]) < 0 and abs(u[2]) > 1e-9: u = -u
    w5 = max(A5, key=lambda v: v @ d); e = nrm(d - (d @ w5) * w5)
    views[k] = {'dir': d.tolist(), 'up': u.tolist(), 'wedge_axis': w5.tolist(), 'wedge_ref': e.tolist()}
radii = {n: float(np.linalg.norm(V, axis=1).max()) for n, V in C.items()}
for s in ('ends', 'middle'):
    J = json.load(open(f'data/interlock-{s}.json')); vols = sorted({round(q['vol'], 7) for q in J['pieces']}, reverse=True); P = []
    for q in J['pieces']:
        V = clean(np.array(q['v'])); P.append({'v': np.round(V, 6).tolist(), 'f': faces(V), 'o': q['o'][0], 'k': vols.index(round(q['vol'], 7)) + 1})
    json.dump({'pieces': P, 'views': views, 'radii': radii, 'layers': J['orig_layers']}, open(f'data/p4-render-{s}.json', 'w'))
    print(s, len(P), 'pieces,', len(vols), 'kinds')
