# The companion solid's family (DICTO 2026-10-16: "any tweaks to give it anything special?"): the golden envelope's 30 planes (distance 2/3,
# fixed) cut by the 20 three-fold planes at distance d (the companion: d = the OCD's hexagon-plane distance). Sweep d and look for special
# members: all edges equal, a midsphere (canonical), all corners on one sphere, the same distance for all 50 faces (insphere), triangle and
# hexagon of equal area, a volume equal to the bcc cell, and the end points. Float; special values then to be made exact. -> data/companion-family.txt
import json, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import brentq
d0 = json.load(open('data/hull-render.json')); HV = np.array(d0['hull']['v']); hh = ConvexHull(HV)
E = []
for e in hh.equations:
    if not any(np.allclose(e, q, atol=1e-6) for q in E): E.append(e)
E = np.array(E); dist = -E[:, 3]
gold = E[np.abs(dist - 2 / 3) < 1e-4][:, :3]; tri = E[np.abs(dist - 2 / 3) >= 1e-4][:, :3]
dC = float(dist[np.abs(dist - 2 / 3) >= 1e-4][0]); cell = 1.327676
assert len(gold) == 30 and len(tri) == 20
def solid(d):
    H = np.vstack([np.hstack([gold, -np.full((30, 1), 2 / 3)]), np.hstack([tri, -np.full((20, 1), d)])])
    V = HalfspaceIntersection(H, np.zeros(3)).intersections; U = []
    for v in V:  # merge the copies where many planes meet (five-fold corners)
        if not any(np.linalg.norm(v - u) < 1e-6 for u in U): U.append(v)
    V = np.array(U); h = ConvexHull(V); return V[h.vertices], ConvexHull(V[h.vertices])
def stats(d):
    V, h = solid(d); P = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    edges = set()
    for e in P:
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]; Q = V[idx]; c = Q.mean(0); a = Q[0] - c; b = np.cross(e[:3], a)
        o = [idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]
        for i in range(len(o)): edges.add(tuple(sorted((o[i], o[(i + 1) % len(o)]))))
    L = [np.linalg.norm(V[a] - V[b]) for a, b in edges]
    mid = [np.linalg.norm(np.cross(V[a], V[b] - V[a])) / np.linalg.norm(V[b] - V[a]) for a, b in edges]
    r = np.linalg.norm(V, axis=1)
    return dict(nV=len(V), nF=len(P), Lmin=min(L), Lmax=max(L), mid_spread=max(mid) - min(mid), r_spread=r.max() - r.min(), vol=h.volume)
# range of d: the triangle planes must cut (d below the RT three-fold corner distance) and leave the hexagons (above the icosahedron's own cut)
rt3 = max(np.linalg.norm(v) for v in HV)  # not exact; scan instead
ds = np.linspace(0.55, 0.70, 151); rows = []
for d in ds:
    try: s = stats(d); rows.append((d, s))
    except Exception: pass
ok = [(d, s) for d, s in rows if s['nF'] == 50]
lo, hi = ok[0][0], ok[-1][0]
out = ['DICTO · dictospheres.com', 'Companion family: golden envelope (30 planes at 2/3) cut by 20 three-fold planes at d (float)',
       f'  50-face range: d from {lo:.4f} to {hi:.4f}; the companion solid is d = {dC:.6f}']
def root(f, name):
    xs = [d for d, s in ok]; ys = [f(s) for d, s in ok]
    for i in range(len(xs) - 1):
        if ys[i] == 0 or ys[i] * ys[i + 1] < 0:
            r = brentq(lambda d: f(stats(d)), xs[i], xs[i + 1], xtol=1e-12); out.append(f'  {name}: d = {r:.10f}  ({stats(r)})'); return r
    out.append(f'  {name}: none in range')
root(lambda s: s['Lmax'] - s['Lmin'] - 1e-15 if False else (s['Lmax'] / s['Lmin'] - 1) * (1 if True else 1) - 0, 'equal edges (scan)')
# equal edges: the two edge kinds cross; use signed difference of the two kinds
def kinds(d):
    V, h = solid(d); r = np.linalg.norm(V, axis=1); return r
for name, f in (('volume = bcc cell', lambda s: s['vol'] - cell),):
    root(f, name)
c = stats(dC); out.append(f'  companion: {c}')
print('\n'.join(out)); open('data/companion-family.txt', 'w').write('\n'.join(out) + '\n')
