"""4D lift of (periodic in the 4th dimension) #61's power cells (DICTO 10 Nov: "something about the corners sounds familiar with shapes ... from 4th dimension";
"yes run the 4D lift test"). A power diagram is the slice x4 = 0 of the ordinary Voronoi diagram of the lifted sites (p, sqrt(C - w)).
Sites: the holes of the stacking (octahedral w = 0, tetrahedral w = λ); s = layer squash (d^2 = s·2/3). For each (word, s, λ, C) the 4D
Voronoi cell of every motif site is built (scipy halfspace intersection, neighbours within a radius) and classified: vertices, facets,
vertex radii spread, facet vertex counts. A regular 4D polytope shows as: 5-cell (5 v, 5 f), 16-cell (8, 16), tesseract (16, 8),
24-cell (24, 24) with equal vertex radii. Usage: python lift4d.py  (grid split over 6 processes) -> lift4d.json, summary lines, FINAL"""
import itertools, json, sys, os, numpy as np
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, os.path.expanduser('~/kres-tmp/splash')); from splash import net_for
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog
WORDS = ['ABC', 'AC']
def cart(G):
    L = np.linalg.cholesky(np.array(G, float)); return L.T                  # x_cart = L.T @ coords
def cell4(word, s, T, t):
    """4D point pattern: octahedral holes at x4 in T·Z, tetrahedral holes at t + T·Z (periodic lift); closed 4D Voronoi cells"""
    spec = net_for(word, Fr(s).limit_denominator(10 ** 6)); M = cart(spec['G']); motif = spec['motif']; n = len(word)
    pts, kinds = [], []
    for a, b, c, e in itertools.product(range(-3, 4), range(-3, 4), range(-2, 3), range(-2, 3)):
        for k, (kind, p) in enumerate(motif):
            x = M @ (np.array([float(v) for v in p]) + [a, b, c]); h = e * T + (t if kind == 'tet' else 0.0)
            pts.append(np.r_[x, h]); kinds.append((k, kind, (a, b, c, e)))
    pts = np.array(pts); out = []
    for k in range(len(motif)):
        i0 = [q for q, kk in enumerate(kinds) if kk[0] == k and kk[2] == (0, 0, 0, 0)][0]; p0 = pts[i0]
        d = np.linalg.norm(pts - p0, axis=1); nb = list(np.argsort(d)[1:260])
        # always include every motif site of the home cell in the 4D layers above and below (bounds the cell in x4 for large T)
        nb += [q for q, kk in enumerate(kinds) if kk[2][:3] == (0, 0, 0) and kk[2][3] in (-1, 0, 1) and q != i0 and q not in nb]
        nb = np.array(nb)
        A = 2 * (pts[nb] - p0); b = (pts[nb] ** 2).sum(1) - (p0 ** 2).sum()
        # bounded? the lifted sites all lie on one side in x4: a Voronoi cell is unbounded in ±x4 -> cap with the mirror images
        try:
            hs = HalfspaceIntersection(np.c_[A, -b], p0); V = np.unique(np.round(hs.intersections, 7), axis=0)
            h = ConvexHull(V)
        except Exception as e: out.append({'site': k, 'err': str(e)[:60]}); continue
        capped = False
        r = np.linalg.norm(V - V.mean(0), axis=1); eq = {tuple(np.round(e, 6)) for e in h.equations}
        out.append({'site': k, 'kind': motif[k][0], 'nv': len(V), 'nf': len(eq), 'rspread': float(np.ptp(r) / r.mean()), 'unbounded': capped})
    return out
def task(args):
    word, s, T, t = args
    try: res = cell4(word, s, T, t)
    except Exception as e: res = [{'err': str(e)[:80]}]
    return {'word': word, 's': s, 'T': T, 't': t, 'cells': res}
if __name__ == '__main__':
    S = [1 / 8, 1 / 7, 1 / 6, 1 / 5, 9 / 40, 1 / 4, 1 / 3, 1 / 2, 1.0]
    jobs = [(word, sv, T, T * f) for word in WORDS for sv in S for T in np.linspace(0.4, 3.0, 27) for f in np.linspace(0.05, 0.5, 10)]
    print(f'START {len(jobs)} periodic lifts (2 words x 9 spacings x 27 periods T x 10 offsets t), 6 processes', flush=True)
    res = []
    with Pool(6) as pool:
        for t, r in enumerate(pool.imap_unordered(task, jobs, chunksize=4)):
            res.append(r)
            if (t + 1) % 60 == 0: print(f'PROGRESS {(t + 1) / len(jobs):.2f}', flush=True)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lift4d.json')
    with open(out_path, 'w') as fh: json.dump(res, fh, default=float)
    print(f'data written: {out_path} ({os.path.getsize(out_path)} bytes)', flush=True)
    reg = {(5, 5): '5-cell', (8, 16): '16-cell', (16, 8): 'tesseract', (24, 24): '24-cell'}
    hits = []
    for r in res:
        for c in r['cells']:
            if 'nv' in c and not c['unbounded'] and (c['nv'], c['nf']) in reg and c['rspread'] < 1e-3: hits.append((r['word'], r['s'], r['T'], r['t'], c['kind'], reg[(c['nv'], c['nf'])]))
    bounded = sum(1 for r in res for c in r['cells'] if 'nv' in c and not c['unbounded'])
    from collections import Counter
    print(f'bounded 4D cells: {bounded}; regular-polytope cells: {len(hits)}'); print('cell types (vertices, facets) seen most:', Counter((c['nv'], c['nf']) for r in res for c in r['cells'] if 'nv' in c).most_common(12))
    near = sorted(((c['rspread'], r['word'], r['s'], round(r['T'], 3), round(r['t'], 3), c['kind'], c['nv'], c['nf']) for r in res for c in r['cells'] if 'nv' in c), key=lambda x: x[0])[:12]
    for x in near: print('  most regular:', x)
    for h in hits[:40]: print('  HIT', h)
    nerr = sum(1 for r in res for c in r['cells'] if 'err' in c)
    print(f'cells with errors: {nerr}')
    print('FINAL ok' if bounded > 0 and nerr < 0.05 * bounded and len(res) == len(jobs) else 'FINAL FAIL: too few closed cells or too many errors')
