# DICTO 2026-10-21 ("can we identify and name any for now?"): the new solids of the OG downward family, D_5 .. D_11 (beats 5-11 of
# the turned-out sequence, scaled), from the exact points in golden-long-solids.pkl: true hull corners, faces (coplanar merged),
# face kinds by side count and regularity (float on exact points; 1e-9).   usage: python3 new_solids_faces.py <five-fold-octet dir>
import sys, os, pickle, numpy as np
from collections import Counter
from scipy.spatial import ConvexHull
sys.path.insert(0, sys.argv[1]); HERE = os.path.dirname(os.path.abspath(__file__))
D = pickle.load(open(os.path.join(HERE, 'golden-long-solids.pkl'), 'rb'))
for k in range(len(D)):
    P = np.array([[x.f() for x in v] for v in D[k]]); H = ConvexHull(P); corners = sorted(set(H.vertices)); G = {}
    for s, e in zip(H.simplices, H.equations): G.setdefault(tuple(np.round(e, 8)), set()).update(s)
    kinds = Counter()
    for ids in G.values():
        Q = P[list(ids)]; c = Q.mean(0); n = c / np.linalg.norm(c); u = Q[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        Q = Q[np.argsort(np.arctan2((Q - c) @ w, (Q - c) @ u))]; L = np.linalg.norm(np.roll(Q, -1, 0) - Q, axis=1)
        kinds[(len(Q), 'regular' if np.ptp(L) < 1e-7 and np.ptp(np.linalg.norm(Q - c, axis=1)) < 1e-7 else 'equal sides' if np.ptp(L) < 1e-7 else 'irregular')] += 1
    E = sum(n for (n, _), m in kinds.items() for _ in range(m)) // 2; F = sum(kinds.values())
    print(f'D{k}: {len(corners)} corners ({len(P)} listed), {F} faces, {E} edges, Euler {len(corners) - E + F}:', dict(sorted(kinds.items())), flush=True)
