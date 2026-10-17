# DICTO 2026-10-17 night: "flat layer, try it" — after showing the classic scutoids (Gómez-Gálvez et al. 2018, Nat. Commun.): chunky
# column-like cells, pentagon at one end, hexagon at the other, a Y part-way up. Brief (scutoid-bundle-brief): every piece a classic scutoid,
# standing side by side in ONE flat layer (flat top and bottom, nothing crossing up or down), a small group repeats sideways to make the layer,
# layers stack straight, so the group tiles space; pieces chunky like a cube (sphericity ≈ cube 0.806), not twigs or slabs.
# Construction: 3D Voronoi cells of a periodic layer of seeds at DIFFERENT HEIGHTS, cut by the slab 0 <= z <= h. Every cell is a convex
# polyhedron; its cross-section at height z is a 2D power diagram whose weights change linearly with z, so neighbours swap part-way up (a Y,
# i.e. a scutoid) when the seeds sit at different heights. Search over the period (lattice), seed positions and heights, and h:
# maximise the least sphericity, requiring every cell to reach the top AND the bottom and to be a scutoid (neighbours differ top vs bottom).
# Float arithmetic (labelled). -> data/scutoid-flat.txt, data/scutoid-flat.json
import sys, json, itertools, numpy as np
from scipy.optimize import minimize
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection, ConvexHull
src = open('scripts/scutoid_hexlayers_poly.py').read()
for name in ('clean', 'cheb', 'poly', 'area3', 'psi'):
    i = src.index(f'def {name}('); j = src.index('\ndef ', i + 1); exec(src[i:j])

def layer(x, m):
    # x = (b1, b2, h, then per seed: u, v, z); lattice L1 = (1, 0), L2 = (b1, b2) scaled to area m (one unit of area per cell)
    b1, b2, h = x[0], abs(x[1]) + 1e-6, abs(x[2]) + 1e-6; sc = (m / b2) ** .5
    L1 = np.array([sc, 0.0]); L2 = np.array([b1 * sc, b2 * sc])
    S = np.array(x[3:3 + 3 * m]).reshape(m, 3)
    seeds = np.c_[S[:, 0:1] * L1 + S[:, 1:2] * L2, S[:, 2:3] * h]
    imgs = [(k, seeds[k] + np.r_[i * L1 + j * L2, 0], (i, j)) for k in range(m) for i in range(-2, 3) for j in range(-2, 3)]
    cells = []
    for k in range(m):
        s = seeds[k]; A = []; b = []; who = []
        for kk, t, ij in imgs:
            if kk == k and ij == (0, 0): continue
            n = t - s; A.append(n); b.append((t @ t - s @ s) / 2); who.append((kk, ij))
        A = np.array(A + [[0, 0, 1], [0, 0, -1]]); b = np.array(b + [h, 0])
        P = poly(A, b)
        if P is None: return None
        top = bot = None; side = {}
        for f in P['faces']:
            n = f[0]
            if n[2] > 1 - 1e-9: top = f
            elif n[2] < -1 + 1e-9: bot = f
        # neighbours touching the top / bottom: side faces with a vertex on z = h / z = 0
        Vt = set(); Vb = set()
        for i, (nrow, bi) in enumerate(zip(A[:-2], b[:-2])):
            nn = nrow / np.linalg.norm(nrow)
            for f in P['faces']:
                if abs(f[0] @ nn - 1) < 1e-9 and abs(f[1] - bi / np.linalg.norm(nrow)) < 1e-7:
                    zs = f[2][:, 2]
                    if (np.abs(zs - h) < 1e-7).sum() >= 2: Vt.add(who[i])
                    if (np.abs(zs) < 1e-7).sum() >= 2: Vb.add(who[i])
        vol = P['vol']; ar = sum(area3(f[2]) for f in P['faces'])
        cells.append(dict(P=P, top=top, bot=bot, nt=len(Vt), nb=len(Vb), scut=Vt != Vb, psi=psi(vol, ar), vol=vol,
                          ta=area3(top[2]) if top else 0, ba=area3(bot[2]) if bot else 0))
    return dict(cells=cells, L1=L1, L2=L2, h=h, seeds=seeds)

def score(x, m, want56=True):
    try: r = layer(x, m)
    except Exception: return 1.0, None
    if r is None: return 1.0, None
    pen = 0.0
    for c in r['cells']:
        if not c['top'] or not c['bot'] or min(c['ta'], c['ba']) < 0.05: pen += 1
        if not c['scut']: pen += 0.5
        if want56 and not ({c['nt'], c['nb']} <= {5, 6, 7}): pen += 0.3
    v = min(c['psi'] for c in r['cells'])
    return -v + pen, r

def describe(r):
    return [dict(top=c['nt'], bottom=c['nb'], scutoid=c['scut'], psi=round(c['psi'], 4), top_area=round(c['ta'], 3), bottom_area=round(c['ba'], 3)) for c in r['cells']]

if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    tries = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    out = ['DICTO · dictospheres.com', 'Flat layer of classic scutoids: 3D Voronoi of a periodic layer of seeds at different heights, cut by a flat slab (float)']
    found = []
    for m in (2, 3, 4, 6):
        best = (9, None, None)
        for t in range(tries):
            x0 = np.r_[rng.uniform(-.5, .5), rng.uniform(.7, 1.2), rng.uniform(.6, 1.6), np.c_[rng.uniform(0, 1, (m, 2)), rng.uniform(-.6, 1.6, m)].ravel()]
            f = lambda x: score(x, m)[0]
            res = minimize(f, x0, method='Nelder-Mead', options=dict(maxfev=600, xatol=1e-4, fatol=1e-5))
            v, r = score(res.x, m)
            if r is not None and v < best[0]: best = (v, res.x, r)
        v, x, r = best
        if r is None: out.append(f'  {m} cells per group: nothing valid'); continue
        ok = v < 0
        out.append(f'  {m} cells per group: least ψ {-v if ok else float("nan"):.3f}  valid={ok}  layer height {r["h"]:.3f} (cell area 1)  cells {describe(r)}')
        found.append(dict(m=m, x=list(map(float, x)), valid=bool(ok), least_psi=float(-v) if ok else None, cells=describe(r)))
        print(out[-1], flush=True)
    out.append('  comparison: cube 0.806, hexagonal prism (height = width) ≈ 0.81; earlier outer pieces 0.58-0.63')
    print('\n'.join(out)); open('data/scutoid-flat.txt', 'w').write('\n'.join(out) + '\n'); json.dump(found, open('data/scutoid-flat.json', 'w'))
