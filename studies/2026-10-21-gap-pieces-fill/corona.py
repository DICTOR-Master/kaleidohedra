# DICTO 2026-10-21 ("run it alongside beat 12"): the building test for the gap pieces. Can a piece (or a set) be surrounded completely
# by copies, face to face? A first corona: a seed with copies round it so that all space near the seed is filled with no overlaps.
# If no corona exists, the set cannot fill space face to face. Search: depth-first; at each step take the uncovered point nearest
# the seed (sample points within DELTA of the seed's surface), try every copy that meets an exposed face near that point face to
# face (congruent faces, opposite orientation, every turn), and keep it if it overlaps nothing (linear programme on the two convex
# pieces). Limits, stated in the log: face-to-face only; the branching uses the 3 exposed faces nearest the gap point, so "no corona
# found" is strong evidence, not a proof. Proper turns only: B1-B5 each have a mirror plane, so their mirror images are turned copies.
# usage: python3 corona.py B1 [B2 ...]   (a set: every piece of the set may be used; the seed is the first)
import os, sys, json, itertools, time
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, '..')
def load(name):
    d = json.load(open(os.path.join(S, f'2026-10-12-bodhi-pieces/data/bodhi-{name}-unit.json'))); V = np.array(d['vertices'], float)
    V = V - V.mean(0); H = ConvexHull(V); F = []
    for eq in H.equations:
        if not any(np.allclose(eq, g, atol=1e-7) for g, _ in F):
            ids = [i for i in range(len(V)) if abs(V[i] @ eq[:3] + eq[3]) < 1e-7]; c = V[ids].mean(0); n = eq[:3]
            u = V[ids[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
            ids.sort(key=lambda i: np.arctan2((V[i] - c) @ w, (V[i] - c) @ u)); F.append((eq, ids))    # counter-clockwise seen from outside
    return {'name': name, 'V': V, 'F': F}
def kabsch(P, Q):
    pc, qc = P.mean(0), Q.mean(0); U, s, Wt = np.linalg.svd((P - pc).T @ (Q - qc)); Dm = np.diag([1, 1, np.sign(np.linalg.det(Wt.T @ U.T))])
    R = Wt.T @ Dm @ U.T; return R, qc - R @ pc
class Placed:
    def __init__(self, T, R, t):
        self.T = T; self.V = T['V'] @ R.T + t; self.c = self.V.mean(0)
        self.F = [((R @ eq[:3]), -(eq[3]) + (R @ eq[:3]) @ t, ids) for eq, ids in T['F']]       # (n, d, ids): n.x <= d inside
        self.A = np.array([n for n, d, _ in self.F]); self.b = np.array([d for n, d, _ in self.F])
def overlap(P, Q):
    A = np.vstack([P.A, Q.A]); b = np.concatenate([P.b, Q.b]); c = np.zeros(4); c[3] = -1
    r = linprog(c, A_ub=np.hstack([A, np.ones((len(A), 1))]), b_ub=b, bounds=[(None, None)] * 3 + [(0, 1)], method='highs')
    return r.status == 0 and -r.fun > 1e-6
def candidates(face_pts, n_out, types):
    out = []
    for T in types:
        for eq, ids in T['F']:
            if len(ids) != len(face_pts): continue
            k = len(ids)
            for sh in range(k):
                order = [ids[(sh - j) % k] for j in range(k)]            # reversed orientation: faces meet back to back
                R, t = kabsch(T['V'][order], face_pts)
                if np.abs(T['V'][order] @ R.T + t - face_pts).max() > 1e-6: continue
                P = Placed(T, R, t)
                if (P.c - face_pts.mean(0)) @ n_out > 0: out.append(P)
    return out
def inside_any(X, pieces, tol=1e-7):
    m = np.zeros(len(X), bool)
    for P in pieces: m |= np.all(X @ P.A.T <= P.b + tol, axis=1)
    return m
def run(names, max_pieces=80, time_limit=3000):
    types = [load(n) for n in names]; seed = Placed(types[0], np.eye(3), np.zeros(3))
    E = min(np.linalg.norm(seed.V[a] - seed.V[b]) for a, b in itertools.combinations(range(len(seed.V)), 2)); DELTA = 0.12 * E
    rng = np.random.default_rng(1); R0 = np.linalg.norm(seed.V, axis=1).max() + DELTA
    X = rng.uniform(-R0, R0, (60000, 3)); g = np.max(X @ seed.A.T - seed.b, axis=1); X = X[(g > 1e-9) & (g < DELTA)]   # shell points
    X = X[np.argsort(g[(g > 1e-9) & (g < DELTA)])]
    t0 = time.time(); stats = {'nodes': 0, 'best': 0}
    def exposed(pieces):
        out = []
        for i, P in enumerate(pieces):
            for n, d, ids in P.F:
                C = P.V[ids].mean(0)
                if not any(Q is not P and np.allclose(sorted(map(tuple, np.round(Q.V[q], 6))), sorted(map(tuple, np.round(P.V[ids], 6)))) for Q in pieces for _, _, q in Q.F if len(q) == len(ids)):
                    out.append((P.V[ids], n, C))
        return out
    def dfs(pieces):
        stats['nodes'] += 1; covered = inside_any(X, pieces)
        stats['best'] = max(stats['best'], covered.mean())
        if covered.all(): return pieces
        if len(pieces) >= max_pieces or time.time() - t0 > time_limit: return None
        p = X[~covered][0]; ex = exposed(pieces)
        ex.sort(key=lambda f: np.linalg.norm(f[2] - p) + 10 * max(0, -((p - f[2]) @ f[1])))
        tried = 0
        for pts, n, C in ex[:3]:
            for P in candidates(pts, n, types):
                if not np.all(P.A @ p <= P.b + 1e-7) and tried > 0: pass
                if any(overlap(P, Q) for Q in pieces): continue
                tried += 1; r = dfs(pieces + [P])
                if r: return r
                if time.time() - t0 > time_limit: return None
        return None
    res = dfs([seed])
    return res, stats, time.time() - t0, len(X)
if __name__ == '__main__':
    names = sys.argv[1:] or ['B1']; res, st, dt, nx = run(names)
    msg = f"{' + '.join(names)}: " + (f"FIRST CORONA FOUND with {len(res) - 1} copies round the seed" if res else
          f"no first corona found (face to face, 3 nearest faces branched); best shell cover {st['best'] * 100:.1f}%") + f"; {st['nodes']} search nodes, {dt:.0f} s, {nx} shell points"
    print(msg, flush=True)
    if res: json.dump([{'type': P.T['name'], 'V': P.V.round(6).tolist()} for P in res], open(os.path.join(HERE, f"corona-{'-'.join(names)}.json"), 'w'))
