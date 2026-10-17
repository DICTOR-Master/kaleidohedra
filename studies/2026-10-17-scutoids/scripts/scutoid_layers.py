# DICTO 2026-10-17, route B: golden scutoid layers. "Can they not alternate, switching top and bottom to adjust symmetry? Pentagons and
# hexagons changing places." "Maybe as a group that forms a space-filling shape." (float first; exact check to follow)
# Planes: the truncated icosahedron's 32 face directions (12 five-fold P, 20 three-fold H). Under the 24 symmetries the OCD shares with the
# bcc packing (Th) the 20 split into 8 on the cube diagonals (Hd) and 12 others (Ho, in pairs across the coordinate axes). A cage is the
# intersection of the 32 half-spaces n·x <= d with one distance per group (dP, dHd, dHo).
#   cage A: the truncated icosahedron; cage B: Ho pushed out past the flip, so the 6 Ho|Ho edges on the coordinate axes vanish and P|P edges
#   appear: pentagons become hexagons, the paired hexagons pentagons (DICTO's swap).
# Cells of a layer: every plane slides linearly from the inner cage's distance to the outer's; a point belongs to the face that sweeps through
# it. Cell i = layer ∩ { (n_j − (Δ_j/Δ_i) n_i)·x ≤ d0_j − (Δ_j/Δ_i) d0_i  for all j } : convex, flat walls, the cells tile the layer, and a
# wall changes neighbours where the faces flip: the scutoid's Y.
import json, itertools, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(p): return [p, [p[1], p[2], p[0]], [p[2], p[0], p[1]]]
P5 = np.array([c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1, s2 * phi])], float)                 # icosahedron corners: 5-fold
D3 = np.array([[a, b, c] for a in (1, -1) for b in (1, -1) for c in (1, -1)] + [c for s1 in (1, -1) for s2 in (1, -1) for c in cyc([0, s1 * phi, s2 / phi])], float)
P5 /= np.linalg.norm(P5, axis=1)[:, None]; D3 /= np.linalg.norm(D3, axis=1)[:, None]
diag = np.array([abs(abs(v[0]) - abs(v[1])) < 1e-9 and abs(abs(v[1]) - abs(v[2])) < 1e-9 for v in D3])
N = np.vstack([P5, D3[diag], D3[~diag]]); GROUP = ['P'] * 12 + ['Hd'] * 8 + ['Ho'] * 12
def cage(dist):
    d = np.array([dist[g] for g in GROUP]); hs = np.c_[N, -d]
    V = HalfspaceIntersection(hs, np.zeros(3)).intersections; V = np.unique(np.round(V, 10), axis=0)
    sides = [sum(1 for v in V if abs(N[i] @ v - d[i]) < 1e-8) for i in range(32)]
    return V, d, sides
def describe(name, dist):
    V, d, sides = cage(dist); s = {g: sorted({sides[i] for i in range(32) if GROUP[i] == g}) for g in ('P', 'Hd', 'Ho')}
    return f'{name}: distances {dist}; corners {len(V)}; sides by group {s}; volume {ConvexHull(V).volume:.6f}', sides
# the truncated icosahedron: pentagon and hexagon planes of the classical TI (edge 2): face distances from its corners
TIv = []
for p in itertools.permutations([0, 1, 3 * phi]):
    pass
def ti_corners():
    base = [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, phi ** 3)]
    out = set()
    for b in base:
        for perm in cyc(list(b)):
            for s in itertools.product((1, -1), repeat=3):
                out.add(tuple(round(x * y, 9) for x, y in zip(perm, s)))
    return np.array(sorted(out))
T = ti_corners(); assert len(T) == 60, len(T)
dP = (T @ P5.T).max(); dH = (T @ D3.T).max()
A = {'P': dP, 'Hd': dH, 'Ho': dH}
out = ['DICTO · dictospheres.com', 'Golden scutoid layers, route B (float)']
la, sA = describe('cage A (the truncated icosahedron)', A); out.append(la)
# the flip: push Ho out until the Ho|Ho edges vanish; B a little beyond it
lo, hi = dH, dH * 1.3
for _ in range(60):
    mid = (lo + hi) / 2; _, _, s = cage({'P': dP, 'Hd': dH, 'Ho': mid})
    if min(s[i] for i in range(32) if GROUP[i] == 'Ho') <= 5: hi = mid
    else: lo = mid
flip = hi; out.append(f'the flip: Ho at {flip:.6f} (×{flip / dH:.6f} of the TI hexagon distance)')
for k in (1.002, 1.01, 1.03, 1.06):
    l, _ = describe(f'cage B at Ho = {k:.3f} × flip', {'P': dP, 'Hd': dH, 'Ho': flip * k}); out.append(l)
print('\n'.join(out)); json.dump(dict(dP=dP, dH=dH, flip=flip), open('data/scutoid-cages.json', 'w'))
open('data/scutoid-layers.txt', 'w').write('\n'.join(out) + '\n')
# ---- the cells of the two alternating layers (float): A -> B = φ(dP, dH, (2/φ) dH) -> A' = φ² A
dA = np.array([A[g] for g in GROUP]); dB = phi * np.array([{'P': dP, 'Hd': dH, 'Ho': 2 / phi * dH}[g] for g in GROUP]); dA2 = phi ** 2 * dA
def cells(d0, d1):
    D = d1 - d0; assert (D > 0).all(); out = []
    for i in range(32):
        hs = [np.r_[N[i], -d1[i]], np.r_[-N[i], d0[i]]]
        for j in range(32):
            if j == i: continue
            r = D[j] / D[i]; hs.append(np.r_[N[j] - r * N[i], -(d0[j] - r * d0[i])])
        hs = np.array(hs)
        # an interior point: on face i's centre line, half way through the layer
        x0 = N[i] * (d0[i] + d1[i]) / 2
        for t in np.linspace(0.3, 0.7, 9):
            x0 = N[i] * (d0[i] + t * D[i])
            if (hs[:, :3] @ x0 + hs[:, 3] < -1e-9).all(): break
        V = HalfspaceIntersection(hs, x0).intersections; V = np.unique(np.round(V, 9), axis=0)
        inner = [k for k in range(len(V)) if abs(N[i] @ V[k] - d0[i]) < 1e-7]; outer = [k for k in range(len(V)) if abs(N[i] @ V[k] - d1[i]) < 1e-7]
        free = [k for k in range(len(V)) if k not in inner and k not in outer]
        out.append(dict(i=i, group=GROUP[i], inner=len(inner), outer=len(outer), free=len(free), corners=len(V), vol=ConvexHull(V).volume, V=V.tolist()))
    return out
lines = []
for name, d0, d1 in (('layer 1: A -> B', dA, dB), ('layer 2: B -> A\' = φ² A', dB, dA2)):
    C = cells(d0, d1)
    vin = ConvexHull(HalfspaceIntersection(np.c_[N, -d0], np.zeros(3)).intersections).volume; vout = ConvexHull(HalfspaceIntersection(np.c_[N, -d1], np.zeros(3)).intersections).volume
    lines.append(f'{name}: cells sum {sum(c["vol"] for c in C):.6f} vs layer {vout - vin:.6f}')
    kinds = {}
    for c in C: kinds.setdefault((c['group'], c['inner'], c['outer'], c['free'], c['corners']), []).append(c['i'])
    for (g, a, b, f, nc), ids in sorted(kinds.items()):
        tag = 'SCUTOID' if a != b and f else ('frustum' if a == b else 'bases differ')
        lines.append(f'   {g}: {len(ids)} cells, inner base {a}-gon, outer base {b}-gon, {f} Y-corner(s), {nc} corners: {tag}')
    json.dump(C, open(f'data/cells-{name.split(":")[0].replace(" ", "")}.json', 'w'))
print('\n'.join(lines)); open('data/scutoid-layers.txt', 'a').write('\n'.join(lines) + '\n')
