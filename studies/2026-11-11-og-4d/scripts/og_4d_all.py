# og_4d_all.py, 12 Nov 2026: the OG (102 corners, 80 faces: 20 hexagons + 60 four-sided) against ALL 15 uniform H4 polytopes
# (DICTO 11 Nov: "so is it possible that the OG is the same form as a 4D polytope"; the 11 Nov pilot og_4d_slices.py did 4 of them and
# its face/corner count was faulty: neighbour-chain merging of hull triangles and collinear points counted as corners).
# Polytopes: Wythoff construction. Flag of the 600-cell (vertex, edge midpoint, triangle centre, cell centre) gives the four chamber
# corners f0..f3; mirror normal n_i is orthogonal to the other three; ring set S -> point p with p.n_i = 1 (i in S), 0 otherwise;
# vertices = orbit of p under the reflections in the 60 root pairs (the 120 vertices of the 600-cell are the H4 roots).
# Axis: w = a 600-cell vertex (the only axis whose stabiliser is the icosahedral group H3). Per polytope: every slice w.x = h at each
# vertex height and each midpoint between consecutive heights, and the shadow on w-perp.
# Counting (fixed): faces = distinct hull planes (global grouping); a point is a CORNER iff the planes through it have normals of rank 3;
# sides of a face = corners on its plane.
# Controls: vertex counts of the 15 (120, 600, 720, 1200, 1440, 2400, 2400, 3600, 3600, 3600, 7200, 7200, 7200, 7200, 14400 as a
# multiset); mirror normals are roots; equal edge lengths; describe() on an icosidodecahedron given with extra edge midpoints and
# face centres must give 30 corners, 32 faces {3: 20, 5: 12}.
# usage: python -u og_4d_all.py <out.json>
import sys, json, itertools, numpy as np
from collections import Counter
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
ROOTS = []
for v in V600:
    if not any(np.allclose(v, -r) for r in ROOTS): ROOTS.append(v)
ROOTS = np.array(ROOTS); assert len(ROOTS) == 60

def describe(Q):
    Q = np.unique(np.round(np.asarray(Q, float), 9), axis=0)
    if len(Q) < 4: return None
    h = ConvexHull(Q); scale = np.abs(Q).max()
    E = h.equations / np.array([1, 1, 1, max(1, scale)])       # group hull triangles into planes by distance, not by rounding
    keep = []
    for eq in E:
        if not any(np.abs(eq - q).max() < 1e-6 for q in keep): keep.append(eq)
    P = np.array(keep) * np.array([1, 1, 1, max(1, scale)]); N, D = P[:, :3], P[:, 3]
    on = np.abs(Q @ N.T + D) < 1e-7 * max(1, scale)          # point x plane incidence
    corner = np.array([np.linalg.matrix_rank(N[on[i]], tol=1e-6) == 3 if on[i].sum() >= 3 else False for i in range(len(Q))])
    sides = [int((on[:, f] & corner).sum()) for f in range(len(P))]
    return dict(corners=int(corner.sum()), faces=len(P), types={str(k): v for k, v in sorted(Counter(sides).items())})

# control: icosidodecahedron with junk points (edge midpoints, face centres) must still read 30 / 32 / {3:20, 5:12}
ico = np.array([p for s1 in (1, -1) for s2 in (1, -1) for p in ([0, s1, s2 * phi], [s1, s2 * phi, 0], [s2 * phi, 0, s1])], float)
ie = [(a, b) for a in range(12) for b in range(a + 1, 12) if abs(np.linalg.norm(ico[a] - ico[b]) - 2) < 1e-9]; assert len(ie) == 30
ID = np.array([(ico[a] + ico[b]) / 2 for a, b in ie])
idd = [(a, b) for a in range(30) for b in range(a + 1, 30) if abs(np.linalg.norm(ID[a] - ID[b]) - np.min([np.linalg.norm(ID[0] - ID[j]) for j in range(1, 30)])) < 1e-9]
junk = [(ID[a] + ID[b]) / 2 for a, b in idd] + [ID[a] * 0.5 for a in range(30)]
c = describe(np.vstack([ID, junk])); assert c == dict(corners=30, faces=32, types={'3': 20, '5': 12}), c
print('control describe(icosidodecahedron + junk points):', c, flush=True)

# flag of the 600-cell and the chamber
def nbrs(i): return [j for j in range(120) if abs(np.linalg.norm(V600[i] - V600[j]) - 1 / phi) < 1e-9]
v0 = 0; n0 = nbrs(v0); v1 = n0[0]; v2 = [j for j in n0 if j in nbrs(v1)][0]; v3 = [j for j in n0 if j in nbrs(v1) and j in nbrs(v2)][0]
F = np.array([V600[v0], (V600[v0] + V600[v1]) / 2, (V600[v0] + V600[v1] + V600[v2]) / 3, (V600[v0] + V600[v1] + V600[v2] + V600[v3]) / 4])
Nm = []
for i in range(4):
    A = np.delete(F, i, axis=0); n = np.linalg.svd(A)[2][-1]; n = n / np.linalg.norm(n)
    if n @ F[i] < 0: n = -n
    assert any(np.allclose(n, r) or np.allclose(n, -r) for r in ROOTS), 'mirror normal not a root'
    Nm.append(n)
Nm = np.array(Nm); print('control: the four chamber mirrors are H4 roots', flush=True)

def orbit(p):
    # 12 Nov fix (pilot FAIL, controls caught it): float drift made near-duplicate orbit points; reflect from SNAPPED points, then merge
    key = lambda x: tuple(np.round(x, 6)); seen = {key(p): p}; todo = [p]
    while todo:
        x = todo.pop(); Y = x[None, :] - 2 * (ROOTS @ x)[:, None] * ROOTS
        for y in Y:
            k = key(y)
            if k not in seen: seen[k] = y; todo.append(y)
    Q = np.array(list(seen.values())); t = cKDTree(Q); grp = {}
    for i, j in sorted(t.query_pairs(1e-5)): grp.setdefault(j, i)
    keep = [i for i in range(len(Q)) if i not in grp]
    return Q[keep]

NAMES = {(0,): '600-cell', (3,): '120-cell', (1,): 'rectified 600-cell', (2,): 'rectified 120-cell', (0, 1): 'truncated 600-cell',
         (2, 3): 'truncated 120-cell', (0, 2): 'cantellated 600-cell', (1, 3): 'cantellated 120-cell', (0, 3): 'runcinated 120-cell',
         (1, 2): 'bitruncated 120-cell', (0, 1, 2): 'cantitruncated 600-cell', (1, 2, 3): 'cantitruncated 120-cell',
         (0, 1, 3): 'runcitruncated 600-cell', (0, 2, 3): 'runcitruncated 120-cell', (0, 1, 2, 3): 'omnitruncated 120-cell'}
w = V600[v0] / np.linalg.norm(V600[v0])
B = np.linalg.svd(w[None, :])[2][1:]          # orthonormal basis of w-perp (3 x 4)
out = []; counts = []; ok = True
for k, ring in enumerate(sorted(NAMES, key=lambda r: (len(r), r))):
    rhs = np.array([1.0 if i in ring else 0.0 for i in range(4)]); p = np.linalg.solve(Nm, rhs)
    P = orbit(p); counts.append(len(P))
    t = cKDTree(P); dmin = t.query(P, k=2)[0][:, 1].min(); Ed = np.array(sorted(t.query_pairs(dmin * (1 + 1e-6))))
    el = np.linalg.norm(P[Ed[:, 0]] - P[Ed[:, 1]], axis=1); assert np.ptp(el) < 1e-9
    ht = P @ w; hs = np.unique(np.round(ht, 9)); levels = sorted(list(hs) + list((hs[:-1] + hs[1:]) / 2))
    nsl = 0
    for hgt in levels:
        s = ht - hgt; pts = list(P[np.abs(s) < 1e-9] @ B.T)
        a, b = Ed[:, 0], Ed[:, 1]; cr = (s[a] * s[b] < 0) & (np.abs(s[a]) > 1e-9) & (np.abs(s[b]) > 1e-9)
        tt = s[a[cr]] / (s[a[cr]] - s[b[cr]]); X = P[a[cr]] + tt[:, None] * (P[b[cr]] - P[a[cr]]); pts += list(X @ B.T)
        if len(pts) < 4: continue
        try: d = describe(pts)
        except Exception: continue          # flat slice (the end caps): no 3D hull
        if d is None: continue
        d.update(polytope=NAMES[ring], kind='slice', height=float(hgt)); out.append(d); nsl += 1
    sh = describe(P @ B.T); sh.update(polytope=NAMES[ring], kind='shadow'); out.append(sh)
    print(f'{NAMES[ring]}: {len(P)} vertices, {len(Ed)} edges, {nsl} slices | shadow {sh["corners"]} corners, {sh["faces"]} faces {sh["types"]}', flush=True)
    for d in out:
        if d['polytope'] == NAMES[ring] and (d['corners'] == 102 or d['faces'] == 80):
            print(f'    NEAR {d["kind"]} h={d.get("height")}: {d["corners"]} corners, {d["faces"]} faces {d["types"]}', flush=True)
    print(f'PROGRESS {(k + 1) / 15:.2f} polytopes', flush=True)
VC = {'600-cell': 120, '120-cell': 600, 'rectified 600-cell': 720, 'rectified 120-cell': 1200, 'truncated 600-cell': 1440,
      'truncated 120-cell': 2400, 'cantellated 600-cell': 3600, 'cantellated 120-cell': 3600, 'runcinated 120-cell': 2400,
      'bitruncated 120-cell': 3600, 'cantitruncated 600-cell': 7200, 'cantitruncated 120-cell': 7200, 'runcitruncated 600-cell': 7200,
      'runcitruncated 120-cell': 7200, 'omnitruncated 120-cell': 14400}
byname = dict(zip([NAMES[r] for r in sorted(NAMES, key=lambda r: (len(r), r))], counts))
bad = {n: (byname[n], VC[n]) for n in VC if byname[n] != VC[n]}; print('control vertex count per name:', 'OK' if not bad else bad, flush=True); ok &= not bad
want = sorted([120, 600, 720, 1200, 1440, 2400, 2400, 3600, 3600, 3600, 7200, 7200, 7200, 7200, 14400])
print('control vertex counts:', sorted(counts), 'OK' if sorted(counts) == want else 'MISMATCH', flush=True); ok &= sorted(counts) == want
json.dump(out, open(sys.argv[1], 'w'), indent=1)
match = [o for o in out if o['corners'] == 102 and o['faces'] == 80 and o['types'].get('6') == 20 and o['types'].get('4') == 60]
print('OG signature (102 corners, 80 faces = 20 hexagons + 60 four-sided):', [(o['polytope'], o['kind'], o.get('height')) for o in match] or 'NONE')
print('FINAL ok' if ok else 'FINAL FAIL')
