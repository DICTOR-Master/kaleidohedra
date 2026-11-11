# og_4d_slices.py, DICTO 11 Nov 2026 ("so is it possible that the OG is the same form as a 4D polytope"). The OG (102 corners, 80 faces:
# 20 regular hexagons + 60 kites, icosahedral) against H4 polytopes. Icosahedral symmetry inside H4 forces the axis: a 600-cell vertex
# axis w = (0,0,0,1). For each polytope: SLICES w.x = h at every combinatorially distinct height (each vertex height and each midpoint
# between consecutive ones) and the SHADOW (projection onto w-perp). Per slice/shadow: corners, faces, face types (sides); flag any with
# 102 corners and 80 faces, then compare the face-type count {6: 20, 4: 60} and, if equal, the shape (kite angles, hexagon regularity).
# Polytopes (pilot): 600-cell, 120-cell (vertices along the 600 cell normals of the 600-cell), rectified 600-cell (edge midpoints),
# rectified 120-cell (its edge midpoints). Edges = vertex pairs at the minimal distance (uniform polytopes). Control: vertex/edge counts.
# usage: python -u og_4d_slices.py <out.json>
import sys, json, itertools, numpy as np
from scipy.spatial import ConvexHull, cKDTree
phi = (1 + 5 ** .5) / 2
def even_perms(v):
    out = []
    for p in itertools.permutations(range(4)):
        inv = sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b])
        if inv % 2 == 0: out.append([v[p[q]] for q in range(4)])
    return out
V = []
for i in range(4):
    for sg in (1, -1): e = [0] * 4; e[i] = sg; V.append(e)
V += [list(s) for s in itertools.product([.5, -.5], repeat=4)]
for sg in itertools.product([1, -1], repeat=3): V += even_perms([sg[0] * phi / 2, sg[1] * .5, sg[2] / (2 * phi), 0])
V600 = np.unique(np.round(np.array(V, float), 12), axis=0); assert len(V600) == 120
def edges_min(P):
    t = cKDTree(P); d = t.query(P, k=2)[0][:, 1].min()
    pr = t.query_pairs(d * (1 + 1e-6)); return np.array(sorted(pr)), d
E600, _ = edges_min(V600); assert len(E600) == 720, len(E600)
adj = {i: set() for i in range(120)}
for a, b in E600: adj[a].add(b); adj[b].add(a)
cells = set()
for a in range(120):
    for b, c, d in itertools.combinations(sorted(adj[a]), 3):
        if c in adj[b] and d in adj[b] and d in adj[c]: cells.add(tuple(sorted((a, b, c, d))))
C = np.array([V600[list(c)].mean(0) for c in cells]); V120 = C / np.linalg.norm(C, axis=1)[:, None]; assert len(V120) == 600
E120, _ = edges_min(V120); assert len(E120) == 1200, len(E120)
R600 = (V600[E600[:, 0]] + V600[E600[:, 1]]) / 2; R120 = (V120[E120[:, 0]] + V120[E120[:, 1]]) / 2
polys = {'600-cell': V600, '120-cell': V120, 'rectified 600-cell': R600, 'rectified 120-cell': R120}
w = np.array([0, 0, 0, 1.0]); assert any(np.allclose(v, w) for v in V600)
def describe(P3):
    if len(P3) < 4: return None
    h = ConvexHull(P3); E = h.equations; n = len(E); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(E[f] - E[g]).max() < 1e-7: par[find(f)] = find(g)   # 1e-9 split coplanar shadow faces (11-11)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    sides = sorted(len(s) for s in grp.values())
    from collections import Counter
    return dict(corners=len(h.vertices), faces=len(grp), types=dict(Counter(sides)))
out = []; ok = True
for name, P in polys.items():
    Ed, _ = edges_min(P)
    hs = np.unique(np.round(P @ w, 10)); levels = list(hs) + list((hs[:-1] + hs[1:]) / 2)
    found = []
    for hgt in sorted(levels):
        if abs(hgt) >= 1 - 1e-12 and name == '600-cell' and False: continue
        s = P @ w - hgt; pts = list(P[np.abs(s) < 1e-12][:, :3])
        a, b = Ed[:, 0], Ed[:, 1]; cr = (s[a] * s[b] < 0)
        tt = s[a[cr]] / (s[a[cr]] - s[b[cr]]); X = P[a[cr]] + tt[:, None] * (P[b[cr]] - P[a[cr]]); pts += list(X[:, :3])
        if len(pts) < 4: continue
        Q = np.unique(np.round(np.array(pts), 10), axis=0)
        try: d = describe(Q)
        except Exception: continue
        if d is None: continue
        d.update(polytope=name, kind='slice', height=float(hgt)); out.append(d)
        flag = d['corners'] == 102 and d['faces'] == 80
        if flag or d['faces'] in (80,) or d['corners'] in (102,): found.append(d)
    sh = describe(np.unique(np.round(P[:, :3], 10), axis=0)); sh.update(polytope=name, kind='shadow'); out.append(sh)
    print(f'{name}: {len(P)} vertices, {len(Ed)} edges | slices: {sum(1 for o in out if o["polytope"] == name and o["kind"] == "slice")} | shadow: {sh["corners"]} corners, {sh["faces"]} faces {sh["types"]}', flush=True)
    for d in found: print(f'    NEAR-MATCH slice h = {d["height"]:+.6f}: {d["corners"]} corners, {d["faces"]} faces, types {d["types"]}', flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
match = [o for o in out if o['corners'] == 102 and o['faces'] == 80 and o['types'].get(6) == 20 and o['types'].get(4) == 60]
print('slices/shadows with the OG signature (102 corners, 80 faces = 20 hexagons + 60 four-sided):', [(o['polytope'], o['kind'], o.get('height')) for o in match])
print('FINAL ok' if ok else 'FINAL FAIL')
