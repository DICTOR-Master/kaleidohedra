# Star Cores book: the overlap test of polar_spikes.py (#79) for Ophelia's polar layer, which polar_spikes.py skips (1722 pieces >= 1200).
# The pieces are those of polar_spikes.py: the solid, the 440 spikes, 642 corner pyramids and 1080 edge tetrahedra; pairs split in chunks.
# Usage: ovl_ophelia.py <dataset-v7 dir> <star-cores scripts dir> <phi|2> <chunk k> <chunks K> <out json>
import sys, os, json, itertools, numpy as np
DS, SCR, T, K, KK, OUT = sys.argv[1:7]; k, KK = int(K), int(KK); sys.argv = [sys.argv[0], DS, '/tmp']; sys.path.insert(0, SCR)
from star_core import faces_info, polyvol, vol, load, axes
phi = (1 + 5 ** .5) / 2; t = phi if T == 'phi' else 2.0
d, V, F = load('solids/dicto-ophelia.json'); V = V - V.mean(0); FI = faces_info(V, F); R2 = float((np.linalg.norm(V, axis=1) ** 2).max())
rho2 = t * R2; tips = np.array([rho2 * n / c for _, n, c in FI])
fa = {v: [i for i, (f, _, _) in enumerate(FI) if v in f] for v in range(len(V))}
E = sorted({tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f, _, _ in FI for i in range(len(f))})
spikes = [np.vstack([V[f], tp]) for (f, _, _), tp in zip(FI, tips)]
corner = [np.vstack([V[v]] + [tips[i] for i in fa[v]]) for v in range(len(V))]
edge = [np.vstack([V[a], V[b]] + [tips[i] for i in fa[a] if i in fa[b]]) for a, b in E]
pieces = [Q for Q in [V] + spikes + corner + edge if vol(Q) > 1e-12]
AX = [axes(Q) for Q in pieces]; C = [Q.mean(0) for Q in pieces]; R = [np.linalg.norm(Q - Q.mean(0), axis=1).max() for Q in pieces]
bad = []; tested = 0
for i in range(len(pieces)):
    if i % KK != k: continue
    for j in range(i + 1, len(pieces)):
        if np.linalg.norm(C[i] - C[j]) > R[i] + R[j] + 1e-9: continue
        tested += 1; sepd = False
        for ax in AX[i][0] + AX[j][0] + [np.cross(u, v) for u in AX[i][1] for v in AX[j][1]]:
            nn = np.linalg.norm(ax)
            if nn < 1e-12: continue
            pa, pb = pieces[i] @ (ax / nn), pieces[j] @ (ax / nn)
            if pa.max() <= pb.min() + 1e-7 or pb.max() <= pa.min() + 1e-7: sepd = True; break
        if not sepd: bad.append([i, j])
json.dump(dict(t=T, chunk=k, chunks=KK, pieces=len(pieces), pairs_tested=tested, overlaps=bad), open(OUT, 'w')); print(T, k, len(pieces), tested, len(bad))
