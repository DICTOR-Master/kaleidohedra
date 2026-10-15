# Step 14 (DICTO: "maybe a Dogstar analog" -> the densest lattice packing of the OCD, whose holes may pinch off like the Dogstar).
# Exploratory, float. Copies OCD + Lambda form a packing iff no nonzero lattice vector lies inside 2*OCD: with the OCD's 80 face
# planes n.x = d (unit n), the gauge of 2K is g(x) = max_f n_f.x / (2 d_f), and the packing condition is g(B m) >= 1 for all
# nonzero integer m. Local search (Betke-Henk style): with the touching pairs' faces fixed, the constraints are linear in the
# basis B; minimise det B by SLSQP inside a trust region, update the touching set, repeat. Many starts; verify the best widely.
import json, itertools, numpy as np, sys
from multiprocessing import Pool
from scipy.spatial import ConvexHull
from scipy.optimize import minimize
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T'])
pl = []
for e in ConvexHull(O).equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
pl = np.array(pl); n_f = pl[:, :3] / np.linalg.norm(pl[:, :3], axis=1)[:, None]; d_f = -pl[:, 3] / np.linalg.norm(pl[:, :3], axis=1)
VOL = ConvexHull(O).volume
M = np.array([m for m in itertools.product(range(-2, 3), repeat=3) if any(m)], float)
M = M[[i for i in range(len(M)) if tuple(M[i]) > tuple(-M[i])]]          # one of each +-m pair
def g(X): return np.max((X @ n_f.T) / (2 * d_f), axis=-1)
def reduce(B):   # simple pairwise (Gauss) reduction of the basis columns
    B = B.copy()
    for _ in range(20):
        ch = False
        for i, j in itertools.permutations(range(3), 2):
            k = np.round(B[:, i] @ B[:, j] / (B[:, j] @ B[:, j]))
            if k: B[:, i] -= k * B[:, j]; ch = True
        if not ch: break
    return B
def admissible_scale(B):
    return 1 / g((B @ M.T).T).min()
def local(B, iters=60):
    B = reduce(B); B *= admissible_scale(B) * (1 + 1e-9)
    for it in range(iters):
        X = (B @ M.T).T; gx = g(X); near = np.where(gx < 1.25)[0]
        fsel = np.argmax((X[near] @ n_f.T) / (2 * d_f), axis=1)
        b0 = B.ravel().copy(); delta = 0.15 * np.abs(np.linalg.det(B)) ** (1 / 3)
        cons = [{'type': 'ineq', 'fun': (lambda b, m=M[k], f=fsel[i]: n_f[f] @ (b.reshape(3, 3) @ m) / (2 * d_f[f]) - 1)} for i, k in enumerate(near)]
        cons.append({'type': 'ineq', 'fun': lambda b: delta ** 2 - np.sum((b - b0) ** 2)})
        sgn = np.sign(np.linalg.det(B))
        r = minimize(lambda b: sgn * np.linalg.det(b.reshape(3, 3)), b0, method='SLSQP', constraints=cons, options={'maxiter': 200, 'ftol': 1e-12})
        Bn = r.x.reshape(3, 3); Bn = reduce(Bn); Bn *= admissible_scale(Bn) * (1 + 1e-12)          # restore exact admissibility
        if abs(np.linalg.det(Bn)) > abs(np.linalg.det(B)) * (1 - 1e-10): break
        B = Bn
    return B
def run(seed):
    rng = np.random.default_rng(seed)
    if seed == 0: B0 = np.array([T[0] + T[1], T[0] + T[2], T[0]]).T           # our bcc packing
    elif seed < 40: B0 = np.array([T[0] + T[1], T[0] + T[2], T[0]]).T + rng.normal(0, 0.25, (3, 3))
    else: B0 = rng.normal(0, 1, (3, 3))
    try: B = local(B0)
    except Exception: return None
    return abs(np.linalg.det(B)), B.tolist()
if __name__ == '__main__':
    with Pool(4) as P: res = [r for r in P.map(run, range(int(sys.argv[1]) if len(sys.argv) > 1 else 400)) if r]
    res.sort(key=lambda r: r[0]); best = np.array(res[0][1])
    # verify widely: every lattice vector with coefficients up to 4
    W = np.array([m for m in itertools.product(range(-4, 5), repeat=3) if any(m)], float)
    gw = g((best @ W.T).T); ok = gw.min() >= 1 - 1e-9
    dens = [VOL / r[0] for r in res]
    X = (best @ W.T).T; touch = W[np.abs(gw - 1) < 1e-7]
    faces = []
    for m in touch:
        x = best @ m; v = (x @ n_f.T) / (2 * d_f); f = np.where(np.abs(v - 1) < 1e-7)[0]
        faces.append(tuple(sorted(int(np.sum(np.abs(O @ pl[k, :3] + pl[k, 3]) < 1e-7)) for k in f)))
    from collections import Counter
    out = [f'{len(res)} local searches; best density {VOL / res[0][0]:.6f} (our bcc packing 0.774332); top densities {[round(x, 6) for x in dens[:8]]}',
           f'best lattice verified over coefficients up to 4: packing {ok} (min gauge {gw.min():.9f})',
           f'touching neighbours: {len(touch)}; the faces they touch on (corner counts per contact face): {dict(Counter(faces))}']
    print('\n'.join(out)); open('data/densest.txt', 'w').write('\n'.join(out) + '\n')
    json.dump({'B': best.tolist(), 'density': VOL / res[0][0], 'all': [r[0] for r in res]}, open('data/densest.json', 'w'))
