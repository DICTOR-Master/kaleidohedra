# DICTO 2026-10-17: "can they be as compacted as possible", "both together": the tightest bundle AND the chunkiest cells. Parameters: the
# scutoid layer A -> B with B = s·(dP, dH, k·dH) (k past the flip (5-φ)/3), then the smallest truncated octahedron T around B (t just above
# max(B's x-reach / 2, B's diagonal-hexagon distance / 3)). Score = the least chunky cell of the whole bundle (layer + closing layer):
# chunkiness of a cell = its thinnest / its widest extent along its own principal axes. Float search; the best point is then pinned to
# golden numbers and checked exactly by scutoid_close.py's method. -> data/scutoid-compact.txt
import itertools, numpy as np, json
from scipy.spatial import HalfspaceIntersection, ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(p): return [p, [p[1], p[2], p[0]], [p[2], p[0], p[1]]]
ICO = np.array([c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1, s2 * phi])], float)
DOD = np.array([[a, b, c] for a in (1, -1) for b in (1, -1) for c in (1, -1)] + [c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1 * phi, s2 / phi])], float)
diag = np.array([abs(abs(v[0]) - abs(v[1])) < 1e-9 and abs(abs(v[1]) - abs(v[2])) < 1e-9 for v in DOD])
N = np.vstack([ICO, DOD[diag], DOD[~diag]]); G = ['P'] * 12 + ['Hd'] * 8 + ['Ho'] * 12
SQ = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
TI = []
for b in ([0, 1, 3 * phi], [1, 2 + phi, 2 * phi], [phi, 2, phi ** 3]):
    for c in cyc(b):
        for s in itertools.product((1, -1), repeat=3): TI.append([c[k] * s[k] for k in range(3)])
TI = np.unique(np.round(TI, 9), axis=0)
dA = (TI @ N.T).max(0)
def corners(Nn, d):
    return np.unique(np.round(HalfspaceIntersection(np.c_[Nn, -d], np.zeros(3)).intersections, 9), axis=0)
def cells(Nn, d0, d1):
    D = d1 - d0; out = []
    for i in range(len(Nn)):
        r = D / D[i]; hs = np.vstack([np.r_[Nn[i], -d1[i]], np.r_[-Nn[i], d0[i]], np.c_[Nn - r[:, None] * Nn[i], -(d0 - r * d0[i])][np.arange(len(Nn)) != i]])
        nf = Nn[i] / (Nn[i] @ Nn[i]); x0 = None
        for tt in np.linspace(0.05, 0.95, 19):
            for off in [np.zeros(3)] + list(np.eye(3) * 0.04) + list(-np.eye(3) * 0.04):
                x = nf * (d0[i] + tt * D[i]) + off
                if (hs[:, :3] @ x + hs[:, 3] < -1e-9).all(): x0 = x; break
            if x0 is not None: break
        if x0 is None: out.append(None); continue
        try: V = np.unique(np.round(HalfspaceIntersection(hs, x0).intersections, 9), axis=0)
        except Exception: out.append(None); continue
        out.append(V)
    return out
def chunk(V):
    X = V - V.mean(0); ev = np.linalg.svd(X, compute_uv=False); return ev[-1] / ev[0]
def bundle(s, k, tf=1.002):
    dB = s * np.array([dA[i] * (k if G[i] == 'Ho' else 1) for i in range(32)])
    if not (dB > dA).all(): return None
    VB = corners(N, dB); hx = (VB @ SQ.T).max(); hd = max(dB[i] for i in range(32) if G[i] == 'Hd')
    t = max(hx / 2, hd / 3) * tf
    TO = np.array([[sg[0] * p[0], sg[1] * p[1], sg[2] * p[2]] for p in itertools.permutations([0, t, 2 * t]) for sg in itertools.product((1, -1), repeat=3)])
    Cl = cells(N, dA, dB)
    NN = np.vstack([N, SQ]); d0 = np.r_[dB, (VB @ SQ.T).max(0)]; d1 = np.r_[(TO @ N.T).max(0), np.full(6, 2 * t)]
    if not (d1 > d0 + 1e-9).all(): return None
    Cc = cells(NN, d0, d1)
    allc = [c for c in Cl + Cc if c is not None and len(c) >= 4]
    sc = [c for c in Cl if c is not None]
    per = {}
    for g, c in zip(G + G + ['Sq'] * 6, Cl + Cc):
        if c is not None and len(c) >= 4: per[g] = min(per.get(g, 1), chunk(c))
    return dict(s=s, k=k, t=t, worst=min(chunk(c) for c in allc), worst_layer=min(chunk(c) for c in sc), cells=len(allc), tf=tf, per={g: round(v, 3) for g, v in per.items()},
                volT=32 * t ** 3, volA=ConvexHull(TI).volume)
flip = (5 - phi) / 3
res = []
for s in []:
    for k in np.linspace(flip * 1.01, 1.6, 6):
      for tf in (1.05, 1.12, 1.2, 1.3, 1.45, 1.6):
        try: b = bundle(s, k, tf)
        except Exception: b = None
        if b: res.append(b)
res.sort(key=lambda b: -b['worst'])
out = ['DICTO · dictospheres.com', 'Compact and chunky scutoid bundles (float search): s = B/A growth, k = paired-hexagon push (flip at (5-φ)/3 = %.6f)' % flip,
       'score = the least chunky cell of the bundle (thinnest/widest principal extent); T the smallest truncated octahedron around B']
for b in res[:10]: out.append(f"  s {b['s']:.3f}  k {b['k']:.3f}  T ×{b['tf']:.2f} of tightest  worst cell {b['worst']:.3f}  core share {b['volA'] / b['volT']:.3f}  by kind {b['per']}")
# the trade-off: for each T looseness, the best worst-cell
out.append('  trade-off (T looseness: best worst-cell, its core share):')
for tf in sorted({b['tf'] for b in res}):
    bb = max((b for b in res if b['tf'] == tf), key=lambda b: b['worst']); out.append(f"    ×{tf:.2f}: {bb['worst']:.3f} (s {bb['s']:.3f}, k {bb['k']:.3f}, core share {bb['volA'] / bb['volT']:.3f}, by kind {bb['per']})")
out.append(f"  (the exact bundle of scutoid_close.py: s = φ, k = 2/φ, t = 9/2)")
open('data/scutoid-compact.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out[-8:])); _ = (lambda: None)  # main search kept
#.write('\n'.join(out) + '\n'); json.dump(res[:20], open('data/scutoid-compact.json', 'w'))

# ---- variant (2026-10-17): B's 8 diagonal hexagons ARE T's hexagons (shared faces, no slab cells between them): t = B's Hd distance / 3,
# needing B's x-reach <= 2t; the Hd planes stay fixed in the closing sweep (Δ = 0 is allowed for j != i: a fixed wall)
def bundle_shared(s, k):
    dB = s * np.array([dA[i] * (k if G[i] == 'Ho' else 1) for i in range(32)])
    if not (dB > dA).all(): return None
    VB = corners(N, dB); hx = (VB @ SQ.T).max(); hd = max(dB[i] for i in range(32) if G[i] == 'Hd'); t = hd / 3
    if hx >= 2 * t - 1e-9: return None
    TO = np.array([[sg[0] * p[0], sg[1] * p[1], sg[2] * p[2]] for p in itertools.permutations([0, t, 2 * t]) for sg in itertools.product((1, -1), repeat=3)])
    Cl = cells(N, dA, dB)
    NN = np.vstack([N, SQ]); d0 = np.r_[dB, (VB @ SQ.T).max(0)]; d1 = np.r_[(TO @ N.T).max(0), np.full(6, 2 * t)]
    hdmask = np.array([g == 'Hd' for g in G] + [False] * 6); d1[hdmask] = d0[hdmask]
    if not (d1[~hdmask] > d0[~hdmask] + 1e-9).all(): return None
    D = d1 - d0; Cc = []
    for i in range(len(NN)):
        if hdmask[i]: continue
        r = D / D[i]; hs = np.vstack([np.r_[NN[i], -d1[i]], np.r_[-NN[i], d0[i]], np.c_[NN - r[:, None] * NN[i], -(d0 - r * d0[i])][np.arange(len(NN)) != i]])
        nf = NN[i] / (NN[i] @ NN[i]); x0 = None
        for tt in np.linspace(0.05, 0.95, 19):
            for off in [np.zeros(3)] + list(np.eye(3) * 0.04) + list(-np.eye(3) * 0.04):
                x = nf * (d0[i] + tt * D[i]) + off
                if (hs[:, :3] @ x + hs[:, 3] < -1e-9).all(): x0 = x; break
            if x0 is not None: break
        Cc.append((G + ['Sq'] * 6)[i] if x0 is None else ((G + ['Sq'] * 6)[i], np.unique(np.round(HalfspaceIntersection(hs, x0).intersections, 9), axis=0)))
    per = {}
    for g, c in zip(G, Cl):
        if c is not None: per['layer ' + g] = min(per.get('layer ' + g, 1), chunk(c))
    for e in Cc:
        if isinstance(e, tuple): per['close ' + e[0]] = min(per.get('close ' + e[0], 1), chunk(e[1]))
    return dict(s=s, k=k, t=t, worst=min(per.values()), per={a: round(b, 3) for a, b in per.items()}, core=ConvexHull(TI).volume / (32 * t ** 3))
R2 = []
for s_ in np.linspace(1.05, 2.4, 28):
    for k_ in np.linspace(flip * 1.005, 1.7, 16):
        try: b = bundle_shared(s_, k_)
        except Exception: b = None
        if b: R2.append(b)
R2.sort(key=lambda b: -b['worst'])
out2 = ['', "Variant: B's 8 diagonal hexagons shared with T (no slab cells):"]
for b in R2[:6]: out2.append(f"  s {b['s']:.3f}  k {b['k']:.3f}  t {b['t']:.3f}  worst cell {b['worst']:.3f}  core share {b['core']:.3f}  by kind {b['per']}")
best_core = sorted([b for b in R2 if b['worst'] >= 0.3], key=lambda b: -b['core'])[:3]
out2.append('  most compact with every cell at least 0.30 chunky:')
for b in best_core: out2.append(f"  s {b['s']:.3f}  k {b['k']:.3f}  t {b['t']:.3f}  worst cell {b['worst']:.3f}  core share {b['core']:.3f}")
print('\n'.join(out2)); open('data/scutoid-compact.txt', 'a').write('\n'.join(out2) + '\n')
