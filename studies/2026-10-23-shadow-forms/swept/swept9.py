# Swept dodecahedra: symmetric (monoclinic) lattice search (DICTO 10-24). K = D + [0, s], s = (phi, phi, 0); its symmetry is C2h
# (inversion, mirror z -> -z, half-turn about z). Lattice packings of K avoid the interior of the difference body DK = 2D + [-s, s].
# For a lattice shape M the best scale makes min over nonzero v of gauge_DK(v) equal 1, so density(M) = vol(K) * min_v g(v)^3 / |det M|.
# Families: general (9 numbers, sanity check vs swept5's 0.77767), monoclinic P (a, b in the xy plane, c along z) and monoclinic C
# (third vector c + (a + b)/2 or + a/2 or + b/2). Multi-start Nelder-Mead; best results re-checked with a wider vector range.
import numpy as np, itertools, json, sys
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
from multiprocessing import Pool
phi = (1 + 5**.5) / 2
D = np.array([(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]) * phi / 2
D = np.vstack([D] + [np.array([[0, a*.5, b*phi**2/2], [a*.5, b*phi**2/2, 0], [b*phi**2/2, 0, a*.5]]) for a in (1, -1) for b in (1, -1)])
s = np.array([phi, phi, 0.])
VK = ConvexHull(np.vstack([D, D + s])).volume
DK = np.vstack([2*D - s, 2*D + s]); E = ConvexHull(DK).equations
N, H = E[:, :3], -E[:, 3]                      # n.x <= h, h > 0
def coeffs(r): return np.array([c for c in itertools.product(range(-r, r+1), repeat=3) if any(c)], float)
C2, C4 = coeffs(2), coeffs(4)
def lll(B, delta=.75):
    B = [np.array(b, float) for b in B]; k = 1
    def gs(B):
        O = []
        for b in B:
            v = b - sum((b @ o) / (o @ o) * o for o in O); O.append(v)
        return O
    while k < 3:
        O = gs(B)
        for j in range(k-1, -1, -1):
            q = round((B[k] @ O[j]) / (O[j] @ O[j]))
            if q: B[k] = B[k] - q * B[j]; O = gs(B)
        if O[k] @ O[k] >= (delta - ((B[k] @ O[k-1]) / (O[k-1] @ O[k-1]))**2) * (O[k-1] @ O[k-1]): k += 1
        else: B[k], B[k-1] = B[k-1], B[k]; k = max(k-1, 1)
    return np.array(B)
def dens(M, C=C2):
    d = abs(np.linalg.det(M))
    if d < 1e-6 * max(1, np.abs(M).max())**3: return 0
    R = lll(M); g = ((C @ R) @ N.T / H).max(1).min()
    r = VK * g**3 / d
    return r if r <= 1 else 0
def build(fam, p):
    if fam == 'general': return p.reshape(3, 3)
    a = np.array([p[0], p[1], 0]); b = np.array([p[2], p[3], 0]); c = np.array([0, 0, 1.])
    if fam == 'P': return np.array([a, b, c])
    sh = {'C_ab': (a + b)/2, 'C_a': a/2, 'C_b': b/2}[fam]
    return np.array([a, b, c + sh])
def run(args):
    fam, seed = args; rs = np.random.default_rng(seed); best = (0, None)
    k = 9 if fam == 'general' else 4
    for _ in range(40):
        p0 = rs.normal(size=k) * 2
        f = lambda p: -dens(build(fam, p))
        r = minimize(f, p0, method='Nelder-Mead', options={'maxiter': 4000, 'xatol': 1e-9, 'fatol': 1e-12})
        r = minimize(f, r.x, method='Nelder-Mead', options={'maxiter': 4000, 'xatol': 1e-10, 'fatol': 1e-13})
        if -r.fun > best[0]: best = (-r.fun, r.x)
    return fam, seed, best[0], best[1].tolist()
if __name__ == '__main__':
    fams = ['general', 'P', 'C_ab', 'C_a', 'C_b']
    jobs = [(f, s) for f in fams for s in range(8 if f != 'general' else 16)]
    with Pool(22) as pool: res = pool.map(run, jobs)
    out = {}
    for fam in fams:
        r = max((x for x in res if x[0] == fam), key=lambda x: x[2])
        M = build(fam, np.array(r[3])); d4 = dens(M, C4)
        M = lll(M); g = ((C4 @ M) @ N.T / H).max(1); M = M * (1 / g.min())   # scale so the packing just touches
        out[fam] = {'density': d4, 'basis': M.tolist(), 'det': abs(np.linalg.det(M))}
        print(f'{fam:8s} best density {d4:.6f} (seeds agree: {sorted(round(x[2], 5) for x in res if x[0] == fam)[-3:]})')
    json.dump(out, open('swept-symmetric.json', 'w'), indent=1)
