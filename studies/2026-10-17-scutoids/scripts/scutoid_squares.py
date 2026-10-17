# DICTO 2026-10-17: "try the squares in the layer design first". The 6 square planes (coordinate axes) join the scutoid layer itself:
#   layer A -> B over 38 planes: the 32 cage planes and the 6 squares (in A the squares only touch the truncated icosahedron, along its
#   axis edges; they move out with the layer), and B is chosen so that its 8 diagonal hexagons and 6 squares ARE the faces of a truncated
#   octahedron T (Hd at 3t, squares at 2t): B = T with its 24 corners cut by the pentagon and paired-hexagon planes;
#   closing layer B -> T: only those 24 corner cells, tapering to T's corners (the Hd and square planes stay fixed: no slab cells).
# Parameters: s (T and the Hd/square planes grow with s), p (pentagon planes, as a share of the way to T's corner support), k (paired-hexagon
# push). Score: the least chunky cell (thinnest / widest principal extent) of the whole bundle; core share = TI volume / T volume. Float.
import itertools, numpy as np, json
from scipy.spatial import HalfspaceIntersection, ConvexHull
exec(open('scripts/scutoid_compact.py').read().split("def bundle(")[0])
def sweep_cells(Nn, d0, d1, groups, skip=()):
    D = d1 - d0; res = []
    for i in range(len(Nn)):
        if i in skip or D[i] <= 1e-12: continue
        r = D / D[i]; hs = np.vstack([np.r_[Nn[i], -d1[i]], np.r_[-Nn[i], d0[i]], np.c_[Nn - r[:, None] * Nn[i], -(d0 - r * d0[i])][np.arange(len(Nn)) != i]])
        nf = Nn[i] / (Nn[i] @ Nn[i]); x0 = None
        for tt in np.linspace(0.03, 0.97, 33):
            for off in [np.zeros(3)] + list(np.eye(3) * 0.03) + list(-np.eye(3) * 0.03):
                x = nf * (d0[i] + tt * D[i]) + off
                if (hs[:, :3] @ x + hs[:, 3] < -1e-9).all(): x0 = x; break
            if x0 is not None: break
        if x0 is None: res.append((groups[i], None)); continue
        try: V = np.unique(np.round(HalfspaceIntersection(hs, x0).intersections, 9), axis=0)
        except Exception: res.append((groups[i], None)); continue
        res.append((groups[i], V))
    return res
NN = np.vstack([N, SQ]); GG = G + ['Sq'] * 6
flip = (5 - phi) / 3
dA38 = np.r_[dA, (TI @ SQ.T).max(0)]
def bundle_sq(s, p, k):
    t = s * max(dA[i] for i in range(32) if G[i] == 'Hd') / 3
    TO = np.array([[sg[0] * q[0], sg[1] * q[1], sg[2] * q[2]] for q in itertools.permutations([0, t, 2 * t]) for sg in itertools.product((1, -1), repeat=3)])
    supT = (TO @ N.T).max(0)
    dB = np.r_[[3 * t if g == 'Hd' else 0 for g in G], np.full(6, 2 * t)].astype(float)
    for i, g in enumerate(G):
        if g == 'P': dB[i] = dA[i] + p * (supT[i] - dA[i])
        if g == 'Ho': dB[i] = min(dA[i] * k * s, supT[i] - 1e-6)
    if not (dB > dA38 + 1e-9).all(): return None
    L = sweep_cells(NN, dA38, dB, GG)
    d1c = dB.copy()
    for i, g in enumerate(G):
        if g in ('P', 'Ho'): d1c[i] = supT[i]
    C = sweep_cells(NN, dB, d1c, GG, skip=[i for i, g in enumerate(GG) if g in ('Hd', 'Sq')])
    per = {}; scut = 0
    for tag, lst in (('layer', L), ('close', C)):
        for g, V in lst:
            if V is None or len(V) < 4: continue
            per[f'{tag} {g}'] = min(per.get(f'{tag} {g}', 1), chunk(V))
    vB = ConvexHull(corners(NN, dB)).volume
    return dict(s=s, p=p, k=k, t=t, worst=min(per.values()) if per else 0, per={a: round(b, 3) for a, b in per.items()}, core=ConvexHull(TI).volume / (32 * t ** 3), B_in_T=vB / (32 * t ** 3))
R = []
for s_ in np.linspace(1.0, 1.8, 17):
    for p_ in (0.2, 0.35, 0.5, 0.65, 0.8):
        for k_ in np.linspace(flip * 1.01, 1.6, 6):
            try: b = bundle_sq(s_, p_, k_)
            except Exception: b = None
            if b and b['worst'] > 0: R.append(b)
R.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Squares in the layer: core TI, scutoid layer over 38 planes to B = T minus 24 corners, closing corner cells (float)']
for b in R[:6]: out.append(f"  s {b['s']:.3f} p {b['p']:.2f} k {b['k']:.3f}: worst cell {b['worst']:.3f}, core share {b['core']:.3f}; by kind {b['per']}")
out.append('  trade-off: best worst-cell for each core share band')
for lo, hi in ((0.30, 1), (0.2, 0.3), (0.12, 0.2), (0.06, 0.12)):
    band = [b for b in R if lo <= b['core'] < hi]
    if band: bb = max(band, key=lambda b: b['worst']); out.append(f"    core share {lo:.2f}-{hi:.2f}: worst cell {bb['worst']:.3f} (s {bb['s']:.3f}, p {bb['p']:.2f}, k {bb['k']:.3f}); kinds {bb['per']}")
print('\n'.join(out)); open('data/scutoid-squares.txt', 'w').write('\n'.join(out) + '\n'); json.dump(R[:30], open('data/scutoid-squares.json', 'w'))
