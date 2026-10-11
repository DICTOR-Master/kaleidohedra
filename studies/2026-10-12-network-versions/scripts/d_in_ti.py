# Network version (2026-10-12): ID core -> dodecahedron -> fullerene cage (one golden step) -> triacontahedron. The missing step:
# the gap between a dodecahedron (edge 1) and the cage that wraps it (edge 1/phi, the dodecahedron's 20 corners on the cage's 20
# hexagon centres). Try the natural pieces: over each cage pentagon, the solid between it and the dodecahedron face below; over
# each cage hexagon, the solid between it and the dodecahedron corner on it; along each cage edge, what is left. Volumes checked.
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
def faces(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
D = ref['D']; T0 = ref['TI']
FT0 = faces(T0); hexn = [f for f in FT0 if np.sum(np.abs(T0 @ f[:3] + f[3]) < 1e-9) == 6]
s = 1 / PHI; TI = T0 * s; FT = faces(TI)
on_hex = all(np.min([abs(d @ f[:3] + f[3]) for f in FT]) < 1e-9 for d in D)
inside = np.all(D @ FT[:, :3].T + FT[:, 3] <= 1e-9)
vT, vD = ConvexHull(TI).volume, ConvexHull(D).volume
print(f'cage edge {s:.6f}, dodecahedron edge 1: corners on cage faces {on_hex}, dodecahedron inside {inside}; gap {vT - vD:.6f} '
      f'({(vT - vD) / vT:.1%} of the cage)')
FD = faces(D); pieces = {}
for f in FT:
    on = TI[np.abs(TI @ f[:3] + f[3]) < 1e-9]; n = f[:3] / np.linalg.norm(f[:3])
    if len(on) == 5:
        g = FD[np.argmax(FD[:, :3] @ n)]; low = D[np.abs(D @ g[:3] + g[3]) < 1e-9]
        P = np.vstack([on, low]); pieces.setdefault('over pentagons (to a dodecahedron face)', []).append(P)
    else:
        c = D[np.argmax(D @ n)]; P = np.vstack([on, c])
        pieces.setdefault('over hexagons (to a dodecahedron corner)', []).append(P)
tot = 0
for k, L in pieces.items():
    vs = [ConvexHull(P).volume for P in L]; tot += sum(vs)
    print(f'  {len(L)} x {k}: volume each {vs[0]:.6f}, corners {len(np.unique(np.round(L[0], 6), axis=0))}')
print(f'pieces so far {tot:.6f} of gap {vT - vD:.6f}; left {vT - vD - tot:.6f}')
ED = [(a, b) for a, b in itertools.combinations(range(20), 2) if abs(np.linalg.norm(D[a] - D[b]) - 1) < 1e-9]
ET = [(a, b) for a, b in itertools.combinations(range(60), 2) if abs(np.linalg.norm(TI[a] - TI[b]) - s) < 1e-9]
hexf = [f for f in FT if np.sum(np.abs(TI @ f[:3] + f[3]) < 1e-9) == 6]
wed = []
for a, b in ED:
    ha = [f for f in hexf if abs(D[a] @ f[:3] + f[3]) < 1e-9][0]; hb = [f for f in hexf if abs(D[b] @ f[:3] + f[3]) < 1e-9][0]
    shared = [(p, q) for p, q in ET if all(abs(TI[x] @ h[:3] + h[3]) < 1e-9 for x in (p, q) for h in (ha, hb))]
    if shared: p, q = shared[0]; wed.append(np.vstack([D[a], D[b], TI[p], TI[q]]))
vw = [ConvexHull(w).volume for w in wed]
ed = sorted(np.round([np.linalg.norm(wed[0][i] - wed[0][j]) for i, j in itertools.combinations(range(4), 2)], 6))
print(f'{len(wed)} edge wedges (dodecahedron edge + the cage edge between its two hexagons): volume each {vw[0]:.6f}, edges {ed}; '
      f'total pieces {tot + sum(vw):.6f} vs gap {vT - vD:.6f}')
P = pieces['over pentagons (to a dodecahedron face)'][0]; H = ConvexHull(P)
F = []
for e in H.equations:
    if not any(np.linalg.norm(e - q) < 1e-7 for q in F): F.append(e)
kinds = sorted(int(np.sum(np.abs(P @ e[:3] + e[3]) < 1e-9)) for e in F)
top, bot = P[:5], P[5:]
nrm = np.cross(top[1] - top[0], top[2] - top[0]); nrm /= np.linalg.norm(nrm)
ang = lambda Q: sorted(np.degrees(np.arctan2(*(np.c_[(Q - Q.mean(0)) @ np.cross(nrm, Q[0] - Q.mean(0)) / np.linalg.norm(Q[0] - Q.mean(0)), (Q - Q.mean(0)) @ (Q[0] - Q.mean(0)) / np.linalg.norm(Q[0] - Q.mean(0))].T))) % 72)
twist = (np.degrees(np.arctan2(np.cross(top[0] - top.mean(0), bot[np.argmin(np.linalg.norm(bot - bot.mean(0) - (top[0] - top.mean(0)) / np.linalg.norm(top[0] - top.mean(0)) * np.linalg.norm(bot[0] - bot.mean(0)), axis=1))] - bot.mean(0)) @ nrm, (top[0] - top.mean(0)) @ (bot[np.argmin(np.linalg.norm(bot - bot.mean(0) - (top[0] - top.mean(0)) / np.linalg.norm(top[0] - top.mean(0)) * np.linalg.norm(bot[0] - bot.mean(0)), axis=1))] - bot.mean(0)))))
print(f'pentagonal piece: {len(F)} faces with corner counts {kinds}; height {abs((top.mean(0) - bot.mean(0)) @ nrm):.6f}; '
      f'top pentagon edge {np.linalg.norm(top[0] - top[1]):.6f}? bottom edge from the dodecahedron face')
