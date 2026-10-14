# Polar Dharma step 5 (2026-10-16, DICTO's question): can a Kepler-Poinsot solid sit in the original's big gap, between the
# triacontahedron (RT) and the outer dodecahedron D(phi^3)? Star solids as filled bodies (points of nonzero winding number), all
# star-shaped from the centre. For each: the scale range [lo, hi] with RT inside the star and the star inside D(phi^3).
import json, itertools, numpy as np
CL = json.load(open('data/reversed-chain.json')); C = {n: np.array(V, float) for n, V in CL}
RT, DO, IC = C['rhombic triacontahedron'], C['dodecahedron (phi^3)'], C['icosahedron']
phi = (1 + 5 ** .5) / 2
Vi = IC / np.linalg.norm(IC[0])                              # unit icosahedron on the chain's 5-fold axes
Vd = DO / np.linalg.norm(DO[0])                              # unit dodecahedron on the 3-fold axes
def ring(V, idx, n):
    Q = V[idx]; c = Q.mean(0); a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
    return [idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))]
def stars():
    a = min(np.linalg.norm(Vi[0] - w) for w in Vi[1:])
    GD, SSD, GI, GSD = [], [], [], []
    for v in Vi:
        nb = [i for i in range(12) if abs(np.linalg.norm(Vi[i] - v) - a) < 1e-6]; r = ring(Vi, nb, v)
        GD.append(Vi[r]); SSD.append(Vi[[r[0], r[2], r[4], r[1], r[3]]])
    seen = []
    for t in itertools.combinations(range(12), 3):
        if all(abs(np.linalg.norm(Vi[i] - Vi[j]) - phi * a) < 1e-6 for i, j in itertools.combinations(t, 2)):
            n = np.cross(Vi[t[1]] - Vi[t[0]], Vi[t[2]] - Vi[t[0]]); n /= np.linalg.norm(n); n = n if n @ Vi[t[0]] > 0 else -n
            GI.append(Vi[ring(Vi, list(t), n)])
    for u in Vi:
        h = Vd @ u; lev = sorted(set(np.round(h, 6)))
        idx = [i for i in range(20) if abs(h[i] - lev[2]) < 1e-5]; r = ring(Vd, idx, u)   # the near-equator level on u's side
        GSD.append(Vd[[r[0], r[2], r[4], r[1], r[3]]])
    return {'great dodecahedron': (GD, Vi), 'small stellated dodecahedron': (SSD, Vi), 'great icosahedron': (GI, Vi), 'great stellated dodecahedron': (GSD, Vd)}
def orient(F):   # every face facing away from the centre
    out = []
    for P in F:
        c = P.mean(0); n = sum(np.cross(P[i] - c, P[(i + 1) % len(P)] - c) for i in range(len(P)))
        out.append(P if n @ c > 0 else P[::-1])
    return out
def wind(F, x):  # generalized winding number, faces fanned from their centres
    w = 0.0
    for P in F:
        c = P.mean(0)
        for i in range(len(P)):
            A, B, Cc = P[i] - x, P[(i + 1) % len(P)] - x, c - x
            la, lb, lc = map(np.linalg.norm, (A, B, Cc))
            w += 2 * np.arctan2(np.dot(A, np.cross(B, Cc)), la * lb * lc + np.dot(A, B) * lc + np.dot(B, Cc) * la + np.dot(Cc, A) * lb)
    return w / (4 * np.pi)
def radial(F, u, R):  # distance to the body's surface along u (star-shaped), by bisection on the winding number
    lo, hi = 0.0, R * 1.0001
    for _ in range(40):
        m = (lo + hi) / 2; lo, hi = (m, hi) if abs(wind(F, u * m)) > 0.5 else (lo, m)
    return lo
def hull_radial(V, u):
    from scipy.spatial import ConvexHull
    e = ConvexHull(V).equations; nu = e[:, :3] @ u; m = nu > 1e-12; return np.min(-e[m, 3] / nu[m])
g = np.pi * (3 - 5 ** .5); N = 600
U = [np.array([np.cos(g * i) * np.sqrt(1 - z * z), np.sin(g * i) * np.sqrt(1 - z * z), z]) for i, z in enumerate(np.linspace(1 - 1 / N, -1 + 1 / N, N))]
U += [v / np.linalg.norm(v) for v in np.vstack([RT, Vi, Vd])]   # the triacontahedron's corners and both axis sets
lines = []
for name, (F, V) in stars().items():
    F = orient(F); dens = wind(F, np.zeros(3) + 1e-9)
    lo = max(hull_radial(RT, u) / radial(F, u, 1.0) for u in U)      # RT inside the star once scaled by lo
    hi = min(hull_radial(DO, v / np.linalg.norm(v)) / np.linalg.norm(v) for v in V)   # star corners inside D(phi^3)
    lines.append(f'{name}: {len(F)} faces, density at the centre {dens:.3f}; fits between RT and D(phi^3) for corner radius '
                 f'{lo:.6f} .. {hi:.6f} ' + ('YES' if lo <= hi + 1e-9 else 'NO'))
    print(lines[-1], flush=True)
open('data/polar-stars.txt', 'w').write('\n'.join(lines) + '\n')
