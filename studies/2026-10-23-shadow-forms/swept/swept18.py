# Counter-rotated swept dodecahedra (DICTO 10-24: "minute rotations or counter rotations to align gaps better"). Two families per cell:
# K1 = R(+theta) K on a lattice L, K2 = R(-theta) K on L + t. No overlaps iff every lattice vector avoids int(K1-K1) and int(K2-K2)
# and every v + t avoids int(K1-K2). Scaling L and t together, the best scale makes the smallest gauge 1, so
# density = 2 vol(K) * (min gauge)^3 / |det L|. Axes: z (K's 2-fold axis), the sweep direction, and the axis across both.
import numpy as np, itertools, json
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
from multiprocessing import Pool
phi = (1 + 5**.5) / 2
D = np.array([(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]) * phi / 2
D = np.vstack([D] + [np.array([[0, a*.5, b*phi**2/2], [a*.5, b*phi**2/2, 0], [b*phi**2/2, 0, a*.5]]) for a in (1, -1) for b in (1, -1)])
s = np.array([phi, phi, 0.]); KV = np.vstack([D, D + s]); KV = KV - KV.mean(0); KV = KV[ConvexHull(KV).vertices]; VK = ConvexHull(KV).volume
AX = {'z': np.array([0, 0, 1.]), 'sweep': s / np.linalg.norm(s), 'across': np.cross(s, [0, 0, 1]) / np.linalg.norm(np.cross(s, [0, 0, 1]))}
def rot(u, a):
    K = np.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]]); return np.eye(3) + np.sin(a)*K + (1 - np.cos(a))*K @ K
def gauge_eq(P):
    E = ConvexHull(P).equations; return E[:, :3], -E[:, 3]
C = np.array([c for c in itertools.product(range(-2, 3), repeat=3)], float); Cnz = C[np.any(C != 0, 1)]
def lll(B, delta=.75):
    B = [np.array(b, float) for b in B]; k = 1
    def gs(B):
        O = []
        for b in B: O.append(b - sum((b @ o) / (o @ o) * o for o in O))
        return O
    while k < 3:
        O = gs(B)
        for j in range(k-1, -1, -1):
            q = round((B[k] @ O[j]) / (O[j] @ O[j]))
            if q: B[k] = B[k] - q * B[j]; O = gs(B)
        if O[k] @ O[k] >= (delta - ((B[k] @ O[k-1]) / (O[k-1] @ O[k-1]))**2) * (O[k-1] @ O[k-1]): k += 1
        else: B[k], B[k-1] = B[k-1], B[k]; k = max(k-1, 1)
    return np.array(B)
def setup(axis, deg):
    R1, R2 = rot(AX[axis], np.radians(deg)), rot(AX[axis], -np.radians(deg))
    K1, K2 = KV @ R1.T, KV @ R2.T
    g11 = gauge_eq(np.vstack([K1 - a for a in K1])); g22 = gauge_eq(np.vstack([K2 - a for a in K2])); g12 = gauge_eq(np.vstack([K1 - b for b in K2]))
    return g11, g22, g12
def dens(p, G):
    M = p[:9].reshape(3, 3); t = p[9:]; d = abs(np.linalg.det(M))
    if d < 1e-6 * max(1, np.abs(M).max())**3: return 0
    R = lll(M); V = Cnz @ R; W = C @ R
    t = t - np.round(np.linalg.solve(R.T, t)) @ R          # reduce t into the cell
    gm = min(((V @ G[0][0].T) / G[0][1]).max(1).min(), ((V @ G[1][0].T) / G[1][1]).max(1).min(), (((W + t) @ G[2][0].T) / G[2][1]).max(1).min())
    r = 2 * VK * gm**3 / d
    return r if r <= 1 else 0
def run(job):
    axis, deg, seed = job; G = setup(axis, deg); rs = np.random.default_rng(seed); best = (0, None)
    for _ in range(14):
        p0 = np.concatenate([rs.normal(size=9) * 2, rs.normal(size=3)])
        f = lambda p: -dens(p, G)
        r = minimize(f, p0, method='Nelder-Mead', options={'maxiter': 9000, 'xatol': 1e-9, 'fatol': 1e-12, 'adaptive': True})
        r = minimize(f, r.x, method='Powell', options={'maxiter': 20000, 'xtol': 1e-9, 'ftol': 1e-13})
        if -r.fun > best[0]: best = (-r.fun, r.x)
    return axis, deg, best[0], best[1].tolist()
if __name__ == '__main__':
    jobs = [(a, d, sd) for a in AX for d in range(0, 13) for sd in (1, 2)]
    with Pool(23) as pool: res = pool.map(run, jobs)
    out = {}
    for a in AX:
        row = []
        for d in range(0, 13):
            b = max((r for r in res if r[0] == a and r[1] == d), key=lambda r: r[2]); row.append((d, b[2])); out[f'{a}:{d}'] = {'density': b[2], 'params': b[3]}
        print(f'{a:7s} ' + '  '.join(f'{d}°:{v*100:.2f}' for d, v in row))
    json.dump(out, open('swept-counter.json', 'w'))
