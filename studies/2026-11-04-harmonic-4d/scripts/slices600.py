#!/usr/bin/env python3
"""Harmonic fingerprint (3D, #94) of the slices of the 600-cell (White Queen) perpendicular to a corner axis and to a cell axis.
Slice at height h: the points where edges of the 600-cell cross the hyperplane x·n = h (plus corners lying on it); fingerprint = Q4, Q6, Q8 of
their directions from the slice centre. Reports zeros along h. dicto-big-brother."""
import itertools, math, json, os
import numpy as np
phi = (1 + 5**.5)/2
def even_perms(v):
    out = set()
    for p in itertools.permutations(range(4)):
        if np.linalg.det(np.eye(4)[list(p)]) > 0:
            for s in itertools.product((1, -1), repeat=4): out.add(tuple(s[i]*v[p[i]] for i in range(4)))
    return out
V = set(itertools.product((.5, -.5), repeat=4)) | {tuple(s*e) for e in np.eye(4) for s in (1, -1)} | even_perms((phi/2, .5, 1/(2*phi), 0))
V = np.unique(np.round(np.array(sorted(V), float), 12), axis=0); assert len(V) == 120
D = np.linalg.norm(V[:, None] - V[None], axis=2); E = [(i, j) for i in range(120) for j in range(i+1, 120) if abs(D[i, j] - 1/phi) < 1e-9]; assert len(E) == 720
from scipy.special import sph_harm_y
def Q(P, l):
    u = P/np.linalg.norm(P, axis=1)[:, None]; th = np.arccos(np.clip(u[:, 2], -1, 1)); ph = np.arctan2(u[:, 1], u[:, 0])
    q = np.array([sph_harm_y(l, m, th, ph).mean() for m in range(-l, l+1)]); return math.sqrt(4*math.pi/(2*l+1)*np.sum(np.abs(q)**2))
def frame(n):
    n = n/np.linalg.norm(n); B = [n]
    for e in np.eye(4):
        v = e - sum((e @ b)*b for b in B)
        if np.linalg.norm(v) > 1e-9: B.append(v/np.linalg.norm(v))
    return np.array(B[1:4])
def slice_pts(n, h):
    n = n/np.linalg.norm(n); x = V @ n; pts = [V[i] for i in range(120) if abs(x[i] - h) < 1e-12]
    for i, j in E:
        if (x[i] - h)*(x[j] - h) < -1e-15:
            t = (h - x[i])/(x[j] - x[i]); pts.append(V[i] + t*(V[j] - V[i]))
    if len(pts) < 4: return None
    P = np.array(pts) @ frame(n).T; P = P - P.mean(0)
    return P
axes = {'corner-first': V[0], 'cell-first': None}
# a cell: 4 mutually adjacent corners; its centre
nb = [set(j for j in range(120) if abs(D[i, j] - 1/phi) < 1e-9) for i in range(120)]
for a in nb[0]:
    for b in nb[0] & nb[a]:
        c_ = (nb[0] & nb[a] & nb[b])
        if c_: cell = (0, a, b, min(c_)); break
    else: continue
    break
axes['cell-first'] = V[list(cell)].mean(0)
res = {}
for name, n in axes.items():
    nn = n/np.linalg.norm(n); hs = np.linspace(-(V @ nn).max() + 1e-3, (V @ nn).max() - 1e-3, 1201)
    rows = []
    for h in hs:
        P = slice_pts(nn, h)
        if P is None or np.min(np.linalg.norm(P, axis=1)) < 1e-9: continue
        rows.append((h, len(P), Q(P, 4), Q(P, 6), Q(P, 8)))
    rows = np.array(rows); out = {}
    for k, l in ((2, 4), (3, 6), (4, 8)):
        q = rows[:, k]; z = [(round(rows[i, 0], 5), int(rows[i, 1]), round(q[i], 5)) for i in range(1, len(q)-1) if q[i] <= q[i-1] and q[i] <= q[i+1] and q[i] < 0.01]
        out[f'Q{l}_zeros'] = z
    out['Q4_always_zero'] = bool(np.all(rows[:, 2] < 1e-9))
    res[name] = out; print(name, out, flush=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'slices600.json'), 'w'), indent=1, default=str)
