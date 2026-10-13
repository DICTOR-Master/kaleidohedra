# Cuboctahedral cages, parallel and turned (DICTO, 2026-10-14): unit cuboctahedra placed on the 12 vertex, 6 square or 8 triangle
# axes of a central one, either parallel or turned about their own axis (90°, 45°, 60°), slid in until first contact with each
# other. Reports contact type, the largest centred cuboctahedron that fits, fill of the hull, and any hull faces that are
# flat-ended triangles (with their r). DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
P0 = np.unique(np.array([p for sg in itertools.product((1, -1), repeat=2) for p in set(itertools.permutations((sg[0], sg[1], 0)))], float), axis=0) / math.sqrt(2)
H0 = ConvexHull(P0)
def rot(axis, ang):
    a = axis / np.linalg.norm(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K
def faces_edges(P):
    h = ConvexHull(P); N = np.unique(np.round(h.equations[:, :3], 9), axis=0)
    E = {tuple(np.round((P[b] - P[a]) / np.linalg.norm(P[b] - P[a]), 9)) for s in h.simplices for a, b in itertools.combinations(s, 2)}
    return N, [np.array(e) for e in E]
def overlap(A, B, eps=1e-9):
    NA, EA = faces_edges(A); NB, EB = faces_edges(B); ax = list(NA) + list(NB)
    for e1 in EA:
        for e2 in EB:
            n = np.cross(e1, e2)
            if np.linalg.norm(n) > 1e-9: ax.append(n / np.linalg.norm(n))
    for n in ax:
        a, b = A @ n, B @ n
        if a.max() <= b.min() + eps or b.max() <= a.min() + eps: return False
    return True
def contact(A, B, tol=1e-6):
    sv = sum(np.min(np.linalg.norm(B[None] - A[:, None], axis=2), axis=1) < tol); return int(sv)
AX = {'vertex': np.unique(np.round(P0 / np.linalg.norm(P0, axis=1)[:, None], 9), axis=0),
      'square': np.vstack([np.eye(3), -np.eye(3)]),
      'triangle': np.array(list(itertools.product((1, -1), repeat=3)), float) / math.sqrt(3)}
TURN = {'vertex': math.pi / 2, 'square': math.pi / 4, 'triangle': math.pi / 3}
res = []
for name, U in AX.items():
    for turned in (False, True):
        R = rot(np.ones(3), 0)
        outs = lambda t: [(P0 @ (rot(u, TURN[name]) if turned else np.eye(3)).T) + u * t for u in U]
        # nearest-neighbour pairs among the axes
        G = U @ U.T; np.fill_diagonal(G, -2); cmax = G.max()
        pairs = [(i, j) for i, j in itertools.combinations(range(len(U)), 2) if abs(G[i, j] - cmax) < 1e-9]
        ok = lambda t: not any(overlap(O[i], O[j]) for O in [outs(t)] for i, j in pairs)
        lo, hi = 0.2, 4.0
        if not ok(hi): res.append(dict(axes=name, turned=turned, note='overlap even far out')); continue
        for _ in range(50):
            mid = (lo + hi) / 2
            (hi := mid) if ok(mid) else (lo := mid)
        t = hi; O = outs(t)
        cont = sorted({contact(O[i], O[j]) for i, j in pairs})
        # biggest centred cuboctahedron (parallel to the original) that fits
        lo2, hi2 = 0.0, 3.0
        for _ in range(50):
            m = (lo2 + hi2) / 2
            (lo2 := m) if not any(overlap(P0 * m, o) for o in O) else (hi2 := m)
        c = lo2
        allv = np.vstack(O + [P0 * c]); H = ConvexHull(allv)
        fill = (len(O) * H0.volume + H0.volume * c ** 3) / H.volume
        eq = np.unique(np.round(H.equations, 6), axis=0); hexes = []
        for e in eq:
            on = np.unique(np.round(allv[np.abs(allv @ e[:3] + e[3]) < 1e-6], 9), axis=0)
            if len(on) == 6:
                cc = on.mean(0); a = on[0] - cc; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
                Q = on[np.argsort(np.arctan2((on - cc) @ b, (on - cc) @ a))]
                L = [np.linalg.norm(Q[i] - Q[(i + 1) % 6]) for i in range(6)]
                ang = [math.degrees(math.acos(np.clip((Q[i - 1] - Q[i]) @ (Q[(i + 1) % 6] - Q[i]) / np.linalg.norm(Q[i - 1] - Q[i]) / np.linalg.norm(Q[(i + 1) % 6] - Q[i]), -1, 1))) for i in range(6)]
                if max(abs(x - 120) for x in ang) < 1e-4: hexes.append(round(min(L) / max(L), 6))
        res.append(dict(axes=name, n=len(U), turned=turned, contactDistance=round(t, 6), sharedCornersPerPair=cont,
                        centreScale=round(c, 6), fill=round(fill, 6), hullFaces=len(eq), flatEndedHullFaces=sorted(set(hexes))))
json.dump(dict(credit='DICTO · dictospheres.com', cuboMember_r=(3 ** .5 - 1) / 2, cages=res), open(os.path.join(ROOT, 'cubo-cages.json'), 'w'), indent=1)
for r in res: print(r)
