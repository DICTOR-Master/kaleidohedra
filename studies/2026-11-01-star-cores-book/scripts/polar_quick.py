# Star Cores book: the polar-spike halo of D106-D109 (Chapter 2, Main theorem) without the pairwise overlap test of polar_spikes.py:
# halo volume over the solid at rho^2 = phi R^2 and 2 R^2, and the layer volume (corner pyramids + edge tetrahedra) against halo - star.
# Usage: polar_quick.py <dataset-v7 dir> <star-cores scripts dir> <out json>
import sys, os, json, numpy as np
DS, SCR, OUT = sys.argv[1:4]; sys.argv = [sys.argv[0], DS, '/tmp']; sys.path.insert(0, SCR)
from star_core import faces_info, polyvol, vol, load
phi = (1 + 5 ** .5) / 2; res = []
for D, fn in (('D106', 'dicto-cube-pearl'), ('D107', 'dicto-golden-clasp'), ('D108', 'dicto-hamlet'), ('D109', 'dicto-ophelia')):
    d, V, F = load('solids/' + fn + '.json'); V = V - V.mean(0); FI = faces_info(V, F); R2 = float((np.linalg.norm(V, axis=1) ** 2).max()); row = dict(D=D, name=d['name'])
    for key, t in (('phi', phi), ('2', 2.0)):
        rho2 = t * R2; tips = np.array([rho2 * n / c for _, n, c in FI])
        fa = {v: [i for i, (f, _, _) in enumerate(FI) if v in f] for v in range(len(V))}
        E = sorted({tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f, _, _ in FI for i in range(len(f))})
        corner = [np.vstack([V[v]] + [tips[i] for i in fa[v]]) for v in range(len(V))]
        edge = [np.vstack([V[a], V[b]] + [tips[i] for i in fa[a] if i in fa[b]]) for a, b in E]
        VS = polyvol(V, F); VH = vol(tips); star = VS + sum(vol(np.vstack([V[f], tp])) for (f, _, _), tp in zip(FI, tips)); lay = sum(map(vol, corner + edge))
        row[key] = dict(halo_over_solid=VH / VS, star_over_solid=star / VS, pieces=len(corner) + len(edge), layer_over_needed=lay / (VH - star))
    res.append(row); print(json.dumps(row), flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
