# Group 2, a logical rule to test (2026-10-30): POLAR SPIKES. Instead of t x the foot of each face's perpendicular, put each spike's tip at
# the face's polar point in a sphere of radius rho (rho^2 = t R^2, R the circumradius): tip = rho^2 n / c for the face plane n.x = c.
# Then the tips of the faces round any corner v all lie in the plane v.x = rho^2 (the polar plane of v), so the hull of the tips is the
# polar solid, each of its facets sits over one corner, and the layer between the star and the halo should split into one pyramid over
# each corner (its base the polygon of the tips round it) and one tetrahedron over each edge. Tested here on group 2 (and on group 1 for
# comparison): star inside halo, layer volume, overlaps. t = phi and 2.
import json, os, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from star_core import faces_info, polyvol, vol, load, pl, overlaps
phi = (1 + 5 ** .5) / 2
DS, SC = sys.argv[1:3]; out = []
for r in json.load(open(SC)):
    if not r.get('pyramids_add_up') or not r.get('convex', True): continue
    d, V, F = load(r['file']); V = V - V.mean(0); FI = faces_info(V, F); R2 = float((np.linalg.norm(V, axis=1) ** 2).max())
    row = dict(D=r['D'], name=r['name'], group=r['verdict'])
    for tn, t in (('phi', phi), ('2', 2.0)):
        rho2 = t * R2; tips = np.array([rho2 * n / c for _, n, c in FI]); VS = polyvol(V, F)
        spikes = [np.vstack([V[f], tp]) for (f, _, _), tp in zip(FI, tips)]; star = VS + sum(map(vol, spikes)); VH = vol(tips)
        hp = pl(tips); ins = lambda Q: bool(np.all(Q @ hp[:, :3].T + hp[:, 3] <= 1e-8))
        fa = {v: [i for i, (f, _, _) in enumerate(FI) if v in f] for v in range(len(V))}
        E = sorted({tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f, _, _ in FI for i in range(len(f))})
        L1 = [np.vstack([V[v]] + [tips[i] for i in fa[v]]) for v in range(len(V))] + [np.vstack([V[a], V[b]] + [tips[i] for i in fa[a] if i in fa[b]]) for a, b in E]
        cop = all(np.ptp(tips[fa[v]] @ V[v]) < 1e-7 * rho2 for v in range(len(V)))
        row[tn] = dict(tips_round_each_corner_coplanar=bool(cop), star_inside_halo=all(ins(Q) for Q in spikes) and ins(V),
                       layer_over_needed=sum(map(vol, L1)) / (VH - star), star_over_solid=star / VS, halo_over_solid=VH / VS,
                       pieces=1 + len(spikes) + len(L1), overlaps=overlaps([V] + spikes + L1, limit=3) if len(L1) < 1200 else None)
    out.append(row); print(row['D'], row['name'][:28], '|', row['group'][:28], '| phi', round(row['phi']['layer_over_needed'], 9), row['phi']['overlaps'], '| 2', round(row['2']['layer_over_needed'], 9), row['2']['overlaps'], flush=True)
json.dump(out, open('data/polar-spikes.json', 'w'), indent=1, default=float)
