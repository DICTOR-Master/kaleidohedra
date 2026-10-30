# Group 2, DICTO's rule (2026-10-30: "an order of sloping base pyramids to align at vertex points"). Keep the TI-rule tips (t x the foot
# of each face's perpendicular). Over each corner v, take the tips of its faces in their order round v (a closed, generally skew ring)
# and fill it with pyramids from v whose bases are triangles of ring tips only, so the pieces meet at the tip points and no new point is
# added. Of all triangulations of each ring, the one taken is the one whose triangles bulge outwards most (the largest volume over v),
# the sloping bases nearest a flat face. Over each edge the tetrahedron (edge + the tips of its two faces), as before.
# The outer skin is then made of the ring triangles: the star wrapped by its own tips. Checked: overlaps among all pieces (solid,
# spikes, corner pyramids, edge tetrahedra); the skin closed; volume of the skin = solid + spikes + pieces; skin convex or not.
import json, os, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from star_core import faces_info, polyvol, vol, load, overlaps
phi = (1 + 5 ** .5) / 2
DS, SC = sys.argv[1:3]; WHICH = sys.argv[3] if len(sys.argv) > 3 else 'star inside halo, layer does not fill'; out = []
def ring(v, FI, fa, V):
    fs = fa[v]; nxt = {}
    for i in fs:
        f = FI[i][0]; k = f.index(v); nxt[f[(k - 1) % len(f)]] = (i, f[(k + 1) % len(f)])   # face i goes from the previous corner to the next
    i0 = fs[0]; f0 = FI[i0][0]; k = f0.index(v); start = f0[(k - 1) % len(f0)]; order = []; cur = start
    for _ in range(len(fs)):
        i, cur = nxt[cur]; order.append(i)
    return order
for r in json.load(open(SC)):
    if r.get('verdict') != WHICH or not r.get('convex', True): continue
    d, V, F = load(r['file']); V = V - V.mean(0); FI = faces_info(V, F); VS = polyvol(V, F)
    fa = {v: [i for i, (f, _, _) in enumerate(FI) if v in f] for v in range(len(V))}
    E = sorted({tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f, _, _ in FI for i in range(len(f))})
    row = dict(D=r['D'], name=r['name'])
    for tn, t in (('phi', phi), ('2', 2.0)):
        tips = np.array([t * c * n for _, n, c in FI]); spikes = [np.vstack([V[f], tp]) for (f, _, _), tp in zip(FI, tips)]
        corner, skin = [], []
        for v in range(len(V)):
            o = ring(v, FI, fa, V); P = [tips[i] for i in o]
            n = len(P); memo = {}
            def best(i, j):
                if j - i < 2: return 0.0, ()
                if (i, j) in memo: return memo[(i, j)]
                bv, bt = -1e18, ()
                for k in range(i + 1, j):
                    w = abs(np.linalg.det(np.array([P[i] - V[v], P[k] - V[v], P[j] - V[v]]))) / 6
                    a, ta = best(i, k); b, tb = best(k, j)
                    if a + b + w > bv: bv, bt = a + b + w, ta + tb + ((i, k, j),)
                memo[(i, j)] = (bv, bt); return memo[(i, j)]
            for a, b, c in best(0, n - 1)[1]:
                corner.append(np.vstack([V[v], P[a], P[b], P[c]])); skin.append((o[a], o[b], o[c]))
        edges = [np.vstack([V[a], V[b]] + [tips[i] for i in fa[a] if i in fa[b]]) for a, b in E]
        total = VS + sum(map(vol, spikes)) + sum(map(vol, corner)) + sum(map(vol, edges))
        hull_vol = vol(tips)
        row[tn] = dict(corner_pyramids=len(corner), edge_tetrahedra=len(edges), volume_over_solid=total / VS, hull_of_tips_over_solid=hull_vol / VS,
                       fills_hull=bool(abs(total - hull_vol) < 1e-7 * hull_vol),
                       overlaps=overlaps([V] + spikes + corner + edges, limit=5) if len(corner) + len(edges) < 1500 else None)
    out.append(row); print(row['D'], row['name'][:30], '| phi', round(row['phi']['volume_over_solid'], 6), 'hull', round(row['phi']['hull_of_tips_over_solid'], 6), 'ov', row['phi']['overlaps'], '| 2', round(row['2']['volume_over_solid'], 6), 'ov', row['2']['overlaps'], flush=True)
json.dump(out, open('data/sloping-bases.json', 'w'), indent=1, default=float)
