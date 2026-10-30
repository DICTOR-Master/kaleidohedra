# Group 2 diagnosis (DICTO 10-30: "think of a logical approach for group 2"): shapes whose star lies inside its halo but whose layer is not
# filled by corner pieces + edge tetrahedra. For each: corner degrees; the layer sum vs the volume needed (gap or overlap?); and every
# halo facet classified by the faces whose tips span it: all round one corner (corner facet), the two faces of one edge + ... (edge facet),
# or tips of faces with no common corner (window facet), and whether its tips are coplanar with more tips than 3. t = phi.
import json, os, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from star_core import faces_info, polyvol, vol, load
phi = (1 + 5 ** .5) / 2
DS, SC = sys.argv[1:3]
out = []
for r in json.load(open(SC)):
    if r.get('verdict') != 'star inside halo, layer does not fill': continue
    d, V, F = load(r['file']); V = V - V.mean(0); FI = faces_info(V, F); t = phi
    tips = np.array([t * c * n for _, n, c in FI]); VS = polyvol(V, F)
    star = VS + sum(vol(np.vstack([V[f], tp])) for (f, _, _), tp in zip(FI, tips)); VH = vol(tips)
    fa = {v: [i for i, (f, _, _) in enumerate(FI) if v in f] for v in range(len(V))}
    E = sorted({tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f, _, _ in FI for i in range(len(f))})
    L1 = [np.vstack([V[v]] + [tips[i] for i in fa[v]]) for v in range(len(V))] + [np.vstack([V[a], V[b]] + [tips[i] for i in fa[a] if i in fa[b]]) for a, b in E]
    s1 = sum(map(vol, L1))
    hq = ConvexHull(tips); fac = {}
    for eq in hq.equations: fac.setdefault(tuple(np.round(eq, 7)), [i for i, p in enumerate(tips) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    kinds = {'corner': 0, 'edge': 0, 'window': 0}; sizes = {}
    for ids in fac.values():
        sizes[len(ids)] = sizes.get(len(ids), 0) + 1
        common = set(FI[ids[0]][0])
        for i in ids[1:]: common &= set(FI[i][0])
        if common: kinds['corner'] += 1; continue
        pairs = sum(1 for a, b in itertools.combinations(ids, 2) if len(set(FI[a][0]) & set(FI[b][0])) >= 2)
        kinds['edge' if pairs else 'window'] += 1
    deg = {}
    for v in fa: deg[len(fa[v])] = deg.get(len(fa[v]), 0) + 1
    res = dict(D=r['D'], name=r['name'], corner_degrees=dict(sorted(deg.items())), layer_sum_over_needed=s1 / (VH - star),
               halo_facets=len(fac), facet_tip_counts=dict(sorted(sizes.items())), facet_kinds=kinds)
    out.append(res); print(json.dumps(res), flush=True)
json.dump(out, open('data/group2-diag.json', 'w'), indent=1)
