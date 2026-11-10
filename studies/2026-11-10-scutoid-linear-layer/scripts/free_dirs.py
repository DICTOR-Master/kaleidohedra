"""Scutoid L, step 3 (DICTO 10 Nov: "scutoids?!"): can the double-row pairing (hexagons again at the top) keep FLAT side faces if the
hexagons may have any edge directions? Unknowns: bottom corners P and middle corners Q on a periodic 4 x 4 patch. Conditions:
paired (shrinking) edges collapse in Q; every other edge of Q parallel to its edge in P (flat trapezoid side faces); bottom cells convex
hexagons, middle cells convex pentagons; no edge shorter than a floor. Least squares from many random starts; a start succeeds when all
conditions hold to 1e-9 with the floors met. Usage: python free_dirs.py [starts]"""
import itertools, sys, numpy as np
from scipy.optimize import least_squares
NX, NY = 4, 4; s3 = 3 ** .5
W, Hh = NX, NY * s3 / 2
def centre(i, j): return np.array([i + 0.5 * (j % 2), j * s3 / 2])
ang = np.radians([90, 30, -30, -90, -150, 150])
corner = lambda c, k: c + np.array([np.cos(ang[k]), np.sin(ang[k])]) / s3
def key(p): q = np.array([p[0] % W, p[1] % Hh]); return tuple(np.round(q, 6) % np.round(np.array([W, Hh]), 6))
V = {}; cells = []
for i, j in itertools.product(range(NX), range(NY)):
    c = centre(i, j); ids = [V.setdefault(key(corner(c, k)), len(V)) for k in range(6)]; cells.append(((i, j), ids, [corner(c, k) for k in range(6)]))
nV = len(V)
# edges with their wrap offset (the vector from a's regular position to b's, unwrapped)
edges = {}
P0 = np.zeros((nV, 2))
for (ij, ids, pts) in cells:
    for k in range(6): P0[ids[k]] = np.array([pts[k][0] % W, pts[k][1] % Hh])
for (ij, ids, pts) in cells:
    for k in range(6):
        a, b = ids[k], ids[(k + 1) % 6]; d = pts[(k + 1) % 6] - pts[k]
        off = d - (P0[b] - P0[a])                        # lattice offset (multiple of the periods)
        edges.setdefault(frozenset((a, b)), (a, b, off))
E = list(edges.values())
def right_edge(i, j):
    ids = cells[i * NY + j][1]; return frozenset((ids[1], ids[2]))
coll = {right_edge(i, j) for i, j in itertools.product(range(NX), range(NY)) if (i + (j // 2) % 2) % 2 == 0}
assert sum(len(set(e)) for e in coll) == 2 * len(coll)
cellcyc = []                                             # per cell: list of (a, b, off) around it
for (ij, ids, pts) in cells:
    cyc = []
    for k in range(6):
        a, b = ids[k], ids[(k + 1) % 6]; d = pts[(k + 1) % 6] - pts[k]; cyc.append((a, b, d - (P0[b] - P0[a])))
    cellcyc.append(cyc)
FLOOR_P, FLOOR_Q = 0.25, 0.12
def vec(X, a, b, off): return X[b] - X[a] + off
def res(z):
    P = z[:2 * nV].reshape(-1, 2); Q = z[2 * nV:].reshape(-1, 2); r = []
    for (a, b, off) in E:
        dp, dq = vec(P, a, b, off), vec(Q, a, b, off)
        if frozenset((a, b)) in coll: r += list(10 * dq)
        else:
            r.append(10 * (dp[0] * dq[1] - dp[1] * dq[0]))
            r.append(5 * max(0, FLOOR_Q - np.linalg.norm(dq))); r.append(5 * max(0, -(dp @ dq)))      # same sense, not too short
        r.append(5 * max(0, FLOOR_P - np.linalg.norm(dp)))
    for cyc in cellcyc:                                  # convex (counterclockwise turns) for P; for Q skipping the collapsed edge
        for X, skip in ((P, False), (Q, True)):
            es = [vec(X, a, b, off) for (a, b, off) in cyc if not (skip and frozenset((a, b)) in coll)]
            for u, w in zip(es, es[1:] + es[:1]): r.append(5 * max(0, -(u[0] * w[1] - u[1] * w[0]) + 1e-3))
    r += list(P[0] - P0[0]) + list(Q[0] - P0[0])           # fix the translations
    return np.array(r)
starts = int(sys.argv[1]) if len(sys.argv) > 1 else 40
rng = np.random.default_rng(3); best = None
for t in range(starts):
    z0 = np.concatenate([(P0 + rng.normal(0, 0.12, P0.shape)).ravel(), (P0 + rng.normal(0, 0.12, P0.shape)).ravel()])
    sol = least_squares(res, z0, xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=1200)
    m = np.abs(sol.fun).max(); print(f'start {t + 1}: max violation {m:.3e}', flush=True)
    if best is None or m < best[0]: best = (m, sol.x)
    if m < 1e-9: break
print(f'starts tried {t + 1}; best max violation {best[0]:.3e}')
if best[0] < 1e-9:
    P = best[1][:2 * nV].reshape(-1, 2); Q = best[1][2 * nV:].reshape(-1, 2)
    lp = min(np.linalg.norm(vec(P, a, b, off)) for a, b, off in E); lq = min(np.linalg.norm(vec(Q, a, b, off)) for a, b, off in E if frozenset((a, b)) not in coll)
    print(f'FOUND: flat side faces with the double-row pairing; shortest bottom edge {lp:.4f}, shortest kept middle edge {lq:.4f}')
    np.save('free_dirs_solution.npy', best[1])
print('FINAL ok' if best is not None else 'FINAL FAIL')
