"""Hollow-straw layer, built (27 Nov 2026; DICTO's idea, flat-walled version). With Claude (Anthropic).
From c116_straw_lp.py (floating pairing, offsets d_t, exact-checked): core = {x : n_t . x <= c_t - d_t for all Minana faces t}
(every core face parallel to its Minana face), shell = Minana minus core. Straw t (core face sigma^-1(t) -> Minana face t) is
  { x : 0 <= D_t(x) <= d_t,  D_t(x)/d_t <= D_s(x)/d_s for every s,  D_s(x) >= 0 for every s },  D_t(x) = c_t - n_t . x,
an intersection of half-spaces, so CONVEX, with flat walls D_t/d_t = D_s/d_s. Checks (floats, 1e-9): volumes add up to the shell;
each piece meets the core exactly in its core face and Minana exactly in its face (side counts = C116's and Minana's under the
pairing); Y vertices (corners inside the shell where four straws meet) counted. Output data/cells/stand/hollow_straw_float.json in
the render format of the amber cells."""
import os, sys, json
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
Dm = A.build("aequus-377")
N = np.array([[float(x) for x in u] for u, c in Dm["planes"]]); C = np.array([float(c) for u, c in Dm["planes"]])
S = json.load(open(os.path.join(HERE, '../data/c116/straw_lp_onefloor_float.json')))
d = np.array([float(eval(x)) if '/' not in x else float(int(x.split('/')[0]) / int(x.split('/')[1])) for x in S['offsets']])
P = json.load(open(os.path.join(HERE, '../data/c116/onefloor_float.json'))); sig = {int(k): int(v) for k, v in P['pairing'].items()}
inv = {v: k for k, v in sig.items()}
faces = json.load(open(os.path.join(HERE, '../data/c116/pairing.json')))['faces']
mverts = [vs for vs, kk in Dm["faces"]]
T = len(N)
def hs(rows):  # rows: (a, b) meaning a . x <= b  ->  scipy format [a, -b]
    return np.array([np.r_[a, -b] for a, b in rows])
def solid(rows):
    H = HalfspaceIntersection(hs(rows), interior_point(rows)); return H.intersections
from scipy.optimize import linprog
def interior_point(rows):
    A_ = np.array([np.r_[a, np.linalg.norm(a)] for a, b in rows]); b_ = np.array([b for a, b in rows])
    r = linprog(np.r_[0, 0, 0, -1], A_ub=A_, b_ub=b_, bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    assert r.status == 0 and r.x[3] > 1e-9, 'empty piece'
    return r.x[:3]
def volume(V): return ConvexHull(V).volume
def outward_idx(V):
    h = ConvexHull(V); c = V.mean(0); out = []
    for s in h.simplices:
        a, b, e = V[s]
        out.append([int(i) for i in (s if np.cross(b - a, e - a) @ (a - c) > 0 else s[::-1])])
    return out
def outward(V): return [[V[i].tolist() for i in s] for s in outward_idx(V)]
core_rows = [(N[t], C[t] - d[t]) for t in range(T)]
mrows = [(N[t], C[t]) for t in range(T)]
Vcore = solid(core_rows); Vmin = solid(mrows); shell = volume(Vmin) - volume(Vcore)
pieces = []; tot = 0.0; bad = []
for t in range(T):
    rows = [(N[s], C[s]) for s in range(T)]                                  # D_s >= 0
    rows.append((-N[t], -(C[t] - d[t])))                                      # D_t <= d_t  i.e. n_t.x >= c_t - d_t
    for s in range(T):
        if s != t: rows.append((-N[t] / d[t] + N[s] / d[s], C[s] / d[s] - C[t] / d[t]))   # D_t/d_t <= D_s/d_s
    V = solid(rows); vol = volume(V); tot += vol
    on_core = [v for v in V if abs(N[t] @ v - (C[t] - d[t])) < 1e-9]; on_min = [v for v in V if abs(N[t] @ v - C[t]) < 1e-9]
    k = inv[t]; si, so = len(on_core), len(on_min)
    if si != len(faces[k]) or so != len(mverts[t]): bad.append((t, si, len(faces[k]), so, len(mverts[t])))
    pieces.append(dict(F=t, core_face=k, sides_in=si, sides_out=so, vol=vol, V=V.tolist(), tris=outward(V)))
print(f'pieces {len(pieces)}; volumes sum {tot:.12f}, shell {shell:.12f}, difference {abs(tot - shell):.2e}', flush=True)
print('pieces whose ends do not match the faces (t, in, expected, out, expected):', bad[:10], flush=True)
# Y vertices: piece corners strictly inside the shell (not on core or Minana) shared by four or more pieces
allc = {}
for p in pieces:
    for v in p['V']:
        key = tuple(np.round(v, 7)); allc.setdefault(key, set()).add(p['F'])
def inside(v):
    v = np.array(v); return all(N[t] @ v < C[t] - 1e-7 for t in range(T)) and any(N[t] @ v > C[t] - d[t] + 1e-7 for t in range(T))
Y = [k for k, s in allc.items() if len(s) >= 4 and inside(k)]
print('Y vertices (inner corners where four straws meet):', len(Y), '; expected 18 (one per swap)', flush=True)
from collections import Counter
print('changes (core sides -> Minana sides):', sorted(Counter((p['sides_in'], p['sides_out']) for p in pieces).items()), flush=True)
hc = ConvexHull(Vcore)
out = dict(s=1.0, pieces=[{k: v for k, v in p.items() if k not in ('V', 'tris')} for p in pieces],
           geom=[dict(F=p['F'], tris=p['tris']) for p in pieces], solid_V=Vcore.tolist(), solid_faces=outward_idx(Vcore),
           n_Y=len(Y), shell_volume=shell)
json.dump(out, open(os.path.join(HERE, '../data/cells/stand/hollow_straw_float.json'), 'w'))
ok = abs(tot - shell) < 1e-9 * shell and not bad and len(Y) == 18
print('FINAL ok' if ok else 'FINAL FAIL')
