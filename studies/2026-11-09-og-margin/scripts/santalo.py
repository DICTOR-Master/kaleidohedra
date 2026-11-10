# santalo.py (from float_family.py), DICTO 10 Nov 2026: 'start the Santaló volume test for #43'. Adds per k the volume product
# vol(D_k) vol(D_k°) / (4π/3)² (Blaschke–Santaló: ≤ 1, = 1 only for the ball; centre = origin by icosahedral symmetry) and its change.
# Original header: DICTO #43 Conjecture 1 (the OG's margin), study 2026-11-09: float exploration of the OG's downward family far beyond k = 8.
# D_0 = OG (exact, from the five-fold-octet tools, then float), D_k = P(D_{k-1}) = hull of the foot points of D_{k-1}'s face planes.
# t_min(D_k) = max over corners v of D_k and faces (m, d) of D_{k+1} of m.v/d (D_k inside t.D_{k+1}).
# Records per k: corners, faces, R, r, H, t_min, (R/r)^2, the argmax, and the normalised radial profile (for shape convergence).
# Sanity: t_min for k = 0..8 must match Table 7 of #43 to 1e-9; corner/face counts must match the exact counts (k <= 11).
# usage: python -u float_family.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, time
import numpy as np
from scipy.spatial import ConvexHull
OUT = os.path.abspath(sys.argv[3])                      # resolved before the chdir below
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])   # OG (exact), G (60 exact rotations)
KMAX = int(sys.argv[2])
OGf = np.array([[x.f() for x in v] for v in OG]); Gf = np.array([[[x.f() for x in row] for row in M] for M in G])

def faces(V, tol=1e-9):
    """distinct face planes of hull(V): unit normals m, distances d, and the hull's corners. Coplanar hull triangles are merged
    by joining neighbouring triangles whose planes agree within tol (union-find over hull adjacency; memory O(n))."""
    h = ConvexHull(V); E = h.equations; n = len(E); par = np.arange(n)
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if g > f and np.abs(E[f] - E[g]).max() < tol: par[find(f)] = find(g)
    roots = np.array([find(i) for i in range(n)]); u, inv = np.unique(roots, return_inverse=True)
    M = np.zeros((len(u), 3)); Dd = np.zeros(len(u)); cnt = np.bincount(inv)
    np.add.at(M, inv, E[:, :3]); np.add.at(Dd, inv, -E[:, 3]); M /= np.linalg.norm(M, axis=1)[:, None]; Dd /= cnt
    return M, Dd, np.unique(h.vertices)

def cover_radius(M):
    """covering radius (rad) of the unit normal set M: arccos of the smallest facet distance of hull(M)."""
    return float(np.arccos((-ConvexHull(M).equations[:, 3]).min()))

def symmetrise(W):
    """orbit closure under the 60 rotations, then merge points closer than 1e-9 (kills float drift of the symmetry)."""
    X = np.vstack([W @ g.T for g in Gf]); X = X[np.lexsort(X.T[::-1])]
    from scipy.spatial import cKDTree
    t = cKDTree(X); groups = {}
    for i, js in enumerate(t.query_ball_point(X, 1e-8)):
        groups.setdefault(min(js), []).append(i)
    return np.array([X[g].mean(0) for g in groups.values()])

def sym_err(V):
    from scipy.spatial import cKDTree
    t = cKDTree(V); return max(t.query(V @ g.T)[0].max() for g in Gf)

TABLE7 = [1.133581, 1.117382, 1.103147, 1.145898, 1.042441, 1.086902, 1.025657, 1.059516, 1.138077]
EXACT_COUNTS = {0: (102, 80), 1: (80, 132), 2: (132, 140), 3: (140, 162), 4: (162, 200), 5: (200, 252), 6: (192, 320), 7: (260, 402),
                8: (312, 500), 9: (500, 732)}
TARGET = 3 / ((1 + 5 ** .5) / 2) ** 2
res = {'mark': 'DICTO #43 Conjecture 1, float downward family, 2026-11-09 · DICTO · dictospheres.com', 'k': []}
V = OGf; FF = faces(V); t0 = time.time(); ok_all = True
for k in range(KMAX + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None])                             # foot points = listed points of D_{k+1}
    FN = faces(W); M2, D2, cor2 = FN
    Vc = V[cor]
    t, i, j = -1.0, 0, 0                                          # chunked max of m.v/d (memory)
    for c0 in range(0, len(Vc), 1000):
        blk = Vc[c0:c0 + 1000] @ M2.T / D2[None, :]; a, b = np.unravel_index(np.argmax(blk), blk.shape)
        if blk[a, b] > t: t, i, j = float(blk[a, b]), c0 + a, b
    R = np.linalg.norm(Vc, axis=1).max(); r = Dd.min(); H = Dd.max()
    sym = sym_err(Vc)
    row = {'k': k, 'listed': len(V), 'corners': len(cor), 'faces': len(M), 't_min': float(t), 'R': float(R), 'r': float(r), 'H': float(H),
           'R_over_r_sq': float((R / r) ** 2), 'argmax_corner_radius': float(np.linalg.norm(Vc[i])), 'argmax_face_dist': float(D2[j]),
           'sym_err': float(sym), 'theta': cover_radius(M), 'n_corner_radii': len(set(np.round(np.linalg.norm(Vc, axis=1) / R, 7).tolist())),
           'R_over_r_next': float(R / D2.min()),
           'vol': float(ConvexHull(Vc).volume), 'vol_polar': float(ConvexHull(M / Dd[:, None]).volume)}
    row['santalo'] = row['vol'] * row['vol_polar'] / (4 * np.pi / 3) ** 2
    res['k'].append(row)
    flag = ''
    if k < len(TABLE7):
        good = abs(t - TABLE7[k]) < 2e-6; ok_all &= good; flag += ' T7 ' + ('ok' if good else 'MISMATCH')
    if k in EXACT_COUNTS:
        good = (len(cor), len(M)) == EXACT_COUNTS[k]; ok_all &= good; flag += ' counts ' + ('ok' if good else f'MISMATCH {EXACT_COUNTS[k]}')
    print(f'k {k:3d}: {len(cor):5d} corners ({len(V)} listed) {len(M):5d} faces  t_min {t:.9f} {"<=" if t <= TARGET + 1e-12 else "> "} 3/phi^2   '
          f'(R/r)^2 {(R/r)**2:.6f}  R {R:.6f} r/R {r/R:.6f} H/R {H/R:.6f}  theta {np.degrees(row["theta"]):.4f} deg  R/r_next {row["R_over_r_next"]:.6f}  r {r:.6f} '
          f'sym {sym:.1e}{flag}  SANTALO {row["santalo"]:.10f} ({time.time()-t0:.0f}s)', flush=True)
    V, FF = W, FN
    json.dump(res, open(OUT, 'w'))
mx = max(res['k'], key=lambda r: r['t_min'])
print(f'max t_min over k = 0..{KMAX}: {mx["t_min"]:.9f} at k = {mx["k"]}; 3/phi^2 = {TARGET:.9f}')
print('FINAL ok' if ok_all else 'FINAL FAIL: sanity mismatch with Table 7 or exact counts')

sp = [r['santalo'] for r in res['k']]
dec = [k for k in range(1, len(sp)) if sp[k] < sp[k - 1] - 1e-12]
print('volume product per k:', ' '.join(f'{x:.8f}' for x in sp))
print('steps where the product FALLS:', dec if dec else 'none (rises at every step)')
print('FINAL ok' if all(0 < x <= 1 + 1e-9 for x in sp) else 'FINAL FAIL: product outside (0, 1]: volume error')
