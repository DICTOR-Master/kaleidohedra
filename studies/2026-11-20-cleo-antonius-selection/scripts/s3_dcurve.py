"""Step 3 (computed, 50 digits): the yantras meeting (b), (c), (d) with uv = c, for c across (0, 0.76), and named products.
For each c: the bindu offset of the (unique) (b), (c) member with slopes (u, c/u) is a function of u; its root is the (d) member
(#103 Theorem 5: exactly one viewpoint centres the bindu).  Reports u, v, counts, and quantities for an extremal test:
k = incircle radius / circle radius (#103 sec. 9.4), spread/mean of the odd regions' areas (sec. 9.6), smallest/largest odd region,
and the smallest |det| over line triples that are not identities of the model (how far the yantra is from any change of its
arrangement).  Named products: every product of two slopes of the solids used in #103 Table 3 (Cleo-Icos 2/phi^2, Antonius side
1/phi, stella 1/sqrt2, phi/2, 3/4).  Writes data/dcurve.json.  usage: python s3_dcurve.py N"""
import sys, os, json, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
from multiprocessing import Pool
mp.mp.dps = 50
import yfam as Y
N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
IDENT = set(tuple(k) for k in json.load(open(os.path.join(Y.ROOT, 'data', 'events.json')))['identities'])

def dmember(c):
    def f(u):
        ms = Y.members(u, c / u); assert len(ms) == 1, len(ms)
        return Y.bindu(ms[0])[0]
    # bracket on lam in [0.5, 2]
    lams = [mp.mpf(k) / 20 for k in range(8, 41)]; vals = []
    for l in lams:
        try: vals.append((l, f(mp.sqrt(c) * l)))
        except Exception: vals.append((l, None))
    roots = []
    for (l1, f1), (l2, f2) in zip(vals, vals[1:]):
        if f1 is not None and f2 is not None and mp.sign(f1) != mp.sign(f2):
            u = mp.findroot(f, (mp.sqrt(c) * l1, mp.sqrt(c) * l2), solver='anderson', tol=mp.mpf(10) ** -45)
            roots.append(u)
    return roots

def quantities(y):
    r = Y.regions(y); m, s = Y.counts_traditional(y)
    A = [mp.mpf(a.numerator) / a.denominator for a in r['odd_areas']]
    mean = sum(A) / len(A); sd = mp.sqrt(sum((a - mean) ** 2 for a in A) / len(A))
    d = Y.dets(y); live = [abs(v) for k, v in d.items() if k not in IDENT]
    off, rad = Y.bindu(y)
    return dict(odd=r['odd'], odd_tri=r['odd_tri'], marma=m, sandhi=s, k=mp.nstr(2 * rad, 12), min_det=mp.nstr(min(live), 6),
                spread=mp.nstr(sd / mean, 12), min_over_max=mp.nstr(min(A) / max(A), 12))

def job(c):
    mp.mp.dps = 50
    c = mp.mpf(c); out = []
    for u in dmember(c):
        y = Y.members(u, c / u)[0]
        q = quantities(y); q.update(c=mp.nstr(c, 30), u=mp.nstr(u, 30), v=mp.nstr(c / u, 30), d=mp.nstr(Y.bindu(y)[0], 3)); out.append(q)
    return mp.nstr(c, 30), out

if __name__ == '__main__':
    t0 = time.time(); phi = (1 + mp.sqrt(5)) / 2
    sl = {'Cleo-Icos 2/phi^2': 2 / phi**2, 'Antonius 1/phi': 1 / phi, 'stella 1/sqrt2': 1 / mp.sqrt(2), 'phi/2': phi / 2, '3/4': mp.mpf(3) / 4}
    named = {}
    for (a, x), (b, z) in itertools.combinations_with_replacement(sl.items(), 2): named[f'{a} x {b}'] = x * z
    with Pool(22) as pool:
        nm = pool.map(job, [mp.nstr(v, 45) for v in named.values()])
        print('PROGRESS 0.4 named products', f'{time.time()-t0:.0f}s', flush=True)
        grid = pool.map(job, [mp.nstr(mp.mpf('0.76') * k / N, 30) for k in range(1, N)], chunksize=1)
    print('named products of two slopes (all conditions (b), (c), (d) with uv = product):')
    for (name, val), (c, rows) in sorted(zip(named.items(), nm), key=lambda z: z[0][1]):
        print(f'   {name:34s} c = {mp.nstr(val, 12):>14s}: ' + ('; '.join(f"u {r['u'][:10]} v {r['v'][:10]} odd {r['odd']} ({r['odd_tri']} tri) marmas {r['marma']} sandhis {r['sandhi']} k {r['k'][:9]} spread {r['spread'][:7]}" for r in rows) or 'no admissible yantra'))
    print('grid (c: number of (d) members; counts; k; smallest non-identity |det|):')
    for c, rows in grid:
        print(f'   {c[:8]}: ' + ' | '.join(f"{r['odd']}/{r['sandhi']} k {r['k'][:8]} spread {r['spread'][:7]} min/max {r['min_over_max'][:7]} mindet {r['min_det']}" for r in rows))
    win = [(mp.mpf(c), rows[0]) for c, rows in grid if rows and rows[0]['odd'] == 43]
    lo, hi = win[0][0], win[-1][0]
    print(f'window on this grid: c in [{mp.nstr(lo, 6)}, {mp.nstr(hi, 6)}] (43 / 24 at every grid point between)')
    ext = {}
    for key, sgn in (('k', -1), ('spread', 1), ('min_over_max', -1)):
        best = min(win, key=lambda z: sgn * mp.mpf(z[1][key]))
        a, b = best[0] - mp.mpf('0.0064'), best[0] + mp.mpf('0.0064')
        with Pool(22) as pool:
            fine = pool.map(job, [mp.nstr(a + (b - a) * j / 64, 30) for j in range(65)])
        fine = [(mp.mpf(c), rows[0]) for c, rows in fine if rows and rows[0]['odd'] == 43]
        fb = min(fine, key=lambda z: sgn * mp.mpf(z[1][key]))
        interior = fine[0][0] < fb[0] < fine[-1][0]
        ext[key] = dict(c=mp.nstr(fb[0], 10), value=fb[1][key], interior=interior)
        print(f"   {'max' if sgn < 0 else 'min'} of {key} in the window: c = {mp.nstr(fb[0], 8)} (to 2e-4), value {fb[1][key][:12]}; "
              f"interior: {interior}; at 2/phi^3 = 0.4721: {[r for n, r in zip(named, nm) if n.startswith('Cleo-Icos 2/phi^2 x Antonius')][0][1][0][key][:12]}")
    json.dump(dict(extrema=ext, named={n: rows for n, (c, rows) in zip(named, nm)}, grid=grid), open(os.path.join(Y.ROOT, 'data', 'dcurve.json'), 'w'), indent=0)
    ok = all(len(rows) == 1 for c, rows in grid if mp.mpf(c) < mp.mpf('0.7'))
    print(f'time {time.time()-t0:.0f}s'); print('FINAL ok' if ok else 'FINAL FAIL (not exactly one (d) member at some c < 0.7)')
