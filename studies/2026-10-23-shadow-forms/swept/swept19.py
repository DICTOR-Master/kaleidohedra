# Counter-rotation by continuation (DICTO 10-24): start from the 84.17% lattice split into two families (an index-2 sublattice and its
# coset, 7 ways), then turn family 1 by +theta and family 2 by -theta in steps of 0.25 degrees, re-optimising from the previous answer.
import numpy as np, itertools, json
from scipy.optimize import minimize
from multiprocessing import Pool
exec(open('swept18.py').read().split("def run(job):")[0])
B0 = lll(np.array(json.load(open('swept-general-more.json'))['general']['basis']))
SUBS = [np.array(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1)]]
def sublattice(v):
    # index-2 sublattice: vectors w with (w . v) even in coefficient terms; build basis via Smith-like construction
    M = [np.array(e) for e in itertools.product(range(-2, 3), repeat=3) if (np.array(e) @ v) % 2 == 0 and any(e)]
    best = None
    for a, b, c in itertools.combinations(M[:200], 3):
        d = round(abs(np.linalg.det(np.array([a, b, c]))))
        if d == 2: best = np.array([a, b, c]); break
    return best
def run(job):
    axis, si = job; v = SUBS[si]; S = sublattice(v); M = S @ B0; t = v @ B0 * 1.0
    t = np.array([c for c in itertools.product((0, 1), repeat=3) if (np.array(c) @ v) % 2 == 1][0]) @ B0
    p = np.concatenate([M.ravel(), t]); out = []
    for k in range(0, 49):
        deg = k * .25; G = setup(axis, deg); f = lambda q: -dens(q, G)
        r = minimize(f, p, method='Nelder-Mead', options={'maxiter': 6000, 'xatol': 1e-10, 'fatol': 1e-13, 'adaptive': True})
        r = minimize(f, r.x, method='Powell', options={'maxiter': 8000, 'xtol': 1e-10, 'ftol': 1e-14})
        if -r.fun >= -f(p): p = r.x
        out.append((deg, -f(p)))
    return axis, si, out, p.tolist()
if __name__ == '__main__':
    jobs = [(a, i) for a in AX for i in range(7)]
    with Pool(21) as pool: res = pool.map(run, jobs)
    summary = {}
    for a in AX:
        best = {}
        for ax, si, out, p in res:
            if ax != a: continue
            for deg, dv in out: best[deg] = max(best.get(deg, 0), dv)
        row = sorted(best.items()); summary[a] = row
        print(f'{a:7s} ' + '  '.join(f'{d:g}°:{v*100:.2f}' for d, v in row if d in (0, .25, .5, 1, 1.5, 2, 3, 4, 6, 8, 10, 12)))
        m = max(row, key=lambda x: x[1]); print(f'        best {m[1]*100:.3f}% at {m[0]}°')
    json.dump({'summary': summary, 'runs': res}, open('swept-counter-cont.json', 'w'))
