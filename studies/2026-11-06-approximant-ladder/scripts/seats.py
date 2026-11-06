"""Cluster seats by harmonics (DICTO 11-06: "then put nests in the clusters, harmonics?"). Full rhombic triacontahedra do not occur at the
approximants' star points (1-5 prolate round each), so the seats are chosen by the harmonic fingerprint of each point's neighbourhood
(bond directions to all points within radius rc): Q4 (cubic tone, 0 for a perfect icosahedral surrounding) and Q6 (icosahedral tone,
0.6633 for a perfect icosahedron) - Steinhardt's bond-order parameters, as in the harmonic-fingerprint study. Per periodic cell: the
points ranked by icosahedral-ness (low Q4, high Q6), the best seats and their spacing. Usage: seats.py qn qd R [rc]"""
import itertools, sys, numpy as np
from scipy.special import sph_harm_y
rc = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
exec(open('cutproject.py').read().split('print("FINAL ok")')[0].replace('print(', '(lambda *a, **k: None)('))
from scipy.spatial import cKDTree
T = cKDTree(X)
def Q(l, vecs):
    th = np.arccos(np.clip(vecs[:, 2] / np.linalg.norm(vecs, axis=1), -1, 1)); ph = np.arctan2(vecs[:, 1], vecs[:, 0])
    q = np.array([sph_harm_y(l, m, th, ph).mean() for m in range(-l, l + 1)])
    return np.sqrt(4 * np.pi / (2 * l + 1) * np.sum(np.abs(q) ** 2))
fr = X @ Binv.T; inc = np.all((fr >= -1e-9) & (fr < 1 - 1e-9), axis=1)
rows = []
for i in np.where(inc)[0]:
    nb = [j for j in T.query_ball_point(X[i], rc) if j != i]
    if len(nb) < 6: continue
    vecs = X[nb] - X[i]; rows.append((i, len(nb), Q(4, vecs), Q(6, vecs)))
rows.sort(key=lambda r: (r[2] - r[3]))
print(f"rung {qn}/{qd}: {inc.sum()} points per cell, rc = {rc}; ideal icosahedron Q4 0, Q6 0.6633")
for i, n, q4, q6 in rows[:10]: print(f"  point {tuple(np.round(X[i], 3))}: {n} neighbours, Q4 {q4:.4f}, Q6 {q6:.4f}")
good = [r for r in rows if r[2] < 0.05 and r[3] > 0.55]
print(f"icosahedral seats (Q4 < 0.05, Q6 > 0.55): {len(good)} per cell")
if len(good) > 1:
    P = X[[r[0] for r in good]]
    # nearest seat distance (periodic: include images)
    imgs = np.array([P + B.T @ np.array(s) for s in itertools.product((-1, 0, 1), repeat=3)]).reshape(-1, 3)
    d = min(np.sort(np.linalg.norm(imgs - p, axis=1))[1] for p in P); print(f"nearest seats {d:.4f} apart")
print("FINAL ok")
