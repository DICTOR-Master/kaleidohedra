# Companion-solid variants for space filling (DICTO 2026-10-16: "both, side by side", depths "which may improve space filling"). Each variant
# is a set of half-spaces n·x ≤ d drawn from the companion's planes (30 golden at 2/3, 20 three-fold at the OCD hexagon distance), with some
# planes dropped (star points grow) or pushed in (cuts), plus the bcc cell's own planes for the trimmed one. For each: corners/faces, volume,
# (a) the bcc packing of the OCD network: the largest scale s with no overlap, density s³·V / cell; (b) the densest lattice packing
# (Betke–Henk style local search, centrally symmetric bodies), density. Float. -> data/companion-variants.json, .txt
import json, itertools, sys, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import minimize
from multiprocessing import Pool
R = json.load(open('data/hull-render.json')); HV = np.array(R['hull']['v']); hh = ConvexHull(HV)
E = []
for e in hh.equations:
    if not any(np.allclose(e, q, atol=1e-6) for q in E): E.append(e)
E = np.array(E); nrm = E[:, :3]; dist = -E[:, 3]
gold = nrm[np.abs(dist - 2 / 3) < 1e-4]; tri = nrm[np.abs(dist - 2 / 3) >= 1e-4]; dT = float(dist[np.abs(dist - 2 / 3) >= 1e-4][0])
cell_planes = []
CV = np.array(json.load(open('data/adapter-render.json'))['cell']['v']); CELL = ConvexHull(CV).volume
for e in ConvexHull(CV).equations:
    if not any(np.allclose(e, q, atol=1e-6) for q in cell_planes): cell_planes.append(e)
cell_planes = np.array(cell_planes)
axis = lambda n: np.isclose(np.sort(np.abs(n)), [0, 0, 1], atol=1e-6).all()                 # cube axes (4-fold of the cell)
diag = lambda n: np.allclose(np.abs(n), 1 / np.sqrt(3), atol=1e-6)                           # cube diagonals (the 8 joints)
def body(H):
    V = HalfspaceIntersection(np.array(H), np.zeros(3)).intersections; U = []
    for v in V:
        if not any(np.linalg.norm(v - u) < 1e-6 for u in U): U.append(v)
    V = np.array(U); h = ConvexHull(V); return V[h.vertices]
def planes_of(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
def first_ring(V, n):   # depth of the plane with normal n through the nearest corners below the extreme one
    h = np.sort(np.unique((V @ n).round(9)))[::-1]; return h[1]
def make(name):
    G = [list(n) + [-2 / 3] for n in gold]; T = [list(n) + [-dT] for n in tri]
    base = body(G + T)
    if name == 'companion': return base
    if name in ('equal edges', 'midsphere', 'cell volume'):
        d = {'equal edges': 0.680007577905, 'midsphere': 0.7000739082, 'cell volume': 0.646696050973}[name]
        return body(G + [list(n) + [-d] for n in tri])
    if name == 'stella star': return body(G + [list(n) + [-dT] for n in tri if not diag(n)])
    if name == '4-fold star': return body([list(n) + [-2 / 3] for n in gold if not axis(n)] + T)
    if name == '5-fold cut':
        five = [v / np.linalg.norm(v) for v in base if np.linalg.norm(v) > np.linalg.norm(base, axis=1).max() - 1e-6]
        return body(G + T + [list(n) + [-first_ring(base, n)] for n in five])
    if name == 'stella cut': return body(G + [list(n) + [-(first_ring(base, n) if diag(n) else dT)] for n in tri])
    if name == 'trimmed to its cell': return body(G + T + VOR)
NAMES = ['companion', 'equal edges', 'midsphere', 'cell volume', 'stella star', '4-fold star', '5-fold cut', 'stella cut', 'trimmed to its cell']
# the OCD's bcc packing (data/network.json): basis [T0 + T1, T0 + T2, T0] as in densest.py; same frame and scale as adapter-render.json
N = json.load(open('data/network.json')); TT = np.array(N['T'])
assert np.allclose(np.sort(np.linalg.norm(np.array(N['ocd']), axis=1)), np.sort(np.linalg.norm(np.array(json.load(open('data/adapter-render.json'))['ocd']['v']), axis=1)), atol=1e-6)
BCC = np.array([TT[0] + TT[1], TT[0] + TT[2], TT[0]]).T
CELL = abs(np.linalg.det(BCC))   # the packing cell (bcc Voronoi cell) volume; adapter-render.json "cell" is a different body
VOR = [list(t / np.linalg.norm(t)) + [-(t @ t) / 2 / np.linalg.norm(t)] for t in (BCC @ np.array([m for m in itertools.product(range(-2, 3), repeat=3) if any(m)], float).T).T]
W4 = np.array([m for m in itertools.product(range(-4, 5), repeat=3) if any(m)], float)
M = np.array([m for m in itertools.product(range(-2, 3), repeat=3) if any(m)], float); M = M[[i for i in range(len(M)) if tuple(M[i]) > tuple(-M[i])]]
def gfun(V):
    P = planes_of(V); n = P[:, :3]; d = -P[:, 3]; return lambda X: np.max((X @ n.T) / (2 * d), axis=-1)
def bcc_density(V):
    g = gfun(V); s = min(1.0, g((BCC @ W4.T).T).min()); return s ** 3 * ConvexHull(V).volume / CELL, s
def reduce(B):
    B = B.copy()
    for _ in range(20):
        ch = False
        for i, j in itertools.permutations(range(3), 2):
            k = np.round(B[:, i] @ B[:, j] / (B[:, j] @ B[:, j]))
            if k: B[:, i] -= k * B[:, j]; ch = True
        if not ch: break
    return B
def densest(V, starts=160):   # densest.py's local search (Betke-Henk style), body as a parameter
    P = planes_of(V); n_f = P[:, :3]; d_f = -P[:, 3]; VOL = ConvexHull(V).volume
    g = lambda X: np.max((X @ n_f.T) / (2 * d_f), axis=-1); adm = lambda B: 1 / g((B @ M.T).T).min()
    def local(B, iters=60):
        B = reduce(B); B *= adm(B) * (1 + 1e-9)
        for it in range(iters):
            X = (B @ M.T).T; gx = g(X); near = np.where(gx < 1.25)[0]
            fsel = np.argmax((X[near] @ n_f.T) / (2 * d_f), axis=1)
            b0 = B.ravel().copy(); delta = 0.15 * np.abs(np.linalg.det(B)) ** (1 / 3)
            cons = [{'type': 'ineq', 'fun': (lambda b, m=M[k], f=fsel[i]: n_f[f] @ (b.reshape(3, 3) @ m) / (2 * d_f[f]) - 1)} for i, k in enumerate(near)]
            cons.append({'type': 'ineq', 'fun': lambda b: delta ** 2 - np.sum((b - b0) ** 2)})
            sgn = np.sign(np.linalg.det(B))
            r = minimize(lambda b: sgn * np.linalg.det(b.reshape(3, 3)), b0, method='SLSQP', constraints=cons, options={'maxiter': 200, 'ftol': 1e-12})
            Bn = reduce(r.x.reshape(3, 3)); Bn *= adm(Bn) * (1 + 1e-12)
            if abs(np.linalg.det(Bn)) > abs(np.linalg.det(B)) * (1 - 1e-10): break
            B = Bn
        return B
    best = None
    for seed in range(starts):
        rng = np.random.default_rng(seed)
        B0 = BCC.copy() if seed == 0 else (BCC + rng.normal(0, 0.25, (3, 3)) if seed < 40 else rng.normal(0, 1, (3, 3)))
        try: B = local(B0)
        except Exception: continue
        ok = g((B @ W4.T).T).min() >= 1 - 1e-9
        if ok and (best is None or abs(np.linalg.det(B)) < best): best = abs(np.linalg.det(B))
    return VOL / best
def job(name):
    V = make(name); F = planes_of(V); dV, s = bcc_density(V)
    return dict(name=name, corners=len(V), faces=len(F), volume=float(ConvexHull(V).volume), bcc_scale=float(s), bcc_density=float(dV),
                densest_lattice=float(densest(V)), v=V.round(8).tolist())
if __name__ == '__main__':
    with Pool(4) as pool: res = pool.map(job, NAMES, chunksize=1)
    json.dump(res, open('data/companion-variants.json', 'w'))
    lines = ['DICTO · dictospheres.com', 'Companion variants and space filling (float)', f'  bcc cell volume {CELL:.6f}; OCD in its bcc packing fills 0.7743, densest lattice 0.7893']
    for r in res: lines.append(f"  {r['name']:22s} corners {r['corners']:3d} faces {r['faces']:3d} volume {r['volume']:.5f} | bcc: scale {r['bcc_scale']:.4f}, fills {r['bcc_density']:.4f} | densest lattice found {r['densest_lattice']:.4f}")
    print('\n'.join(lines)); open('data/companion-variants.txt', 'w').write('\n'.join(lines) + '\n')
