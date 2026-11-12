"""Aim 2, chunk 5c, DICTO's extra case (12 Nov 2026): the canonical-form analysis of 5c on E1, the most even exact yantra of #103
(43 regions, corners inside the circle), compared with the DICTO Yantra (GF1) and Kulaichev's yantra. Does "most even" show in the forms?
E1 has no exact form (studies/2026-11-10-g1-e1-exact: one incidence + three stationarity equations, open); its u, v, Q are taken from the
90-digit refinement (e1-refined.json, Newton step 2.7e-60) and S is re-solved at the working precision from E1's incidence (t4's right leg
through t5's corner, where t5's base and t6's right leg meet), so the yantra used lies exactly on E1's edge to working precision.
Usage: python -u e1_regions.py [pilot]"""
import sys, os, json, math, time
from fractions import Fraction as Fr
from multiprocessing import get_context

PILOT = sys.argv[1:] == ['pilot']
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import yantra_regions45 as Y45
from yantra_regions45 import B, Ctx, analyse, arrangement, area2, polar_area2, SRI
E1J = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-10-g1-e1-exact', 'e1-refined.json'))


def load_e1(K, log):
    mp = K.mp
    from model import solve, all_conditions, order_ok, det3
    e = json.load(open(E1J))
    u, v, Q = mp.mpf(e['u']), mp.mpf(e['v']), mp.mpf(e['Q'])
    tri = lambda S: solve(v * v / (1 + v * v), Q, 1 / (1 + u * u), S, v / (1 + v * v), u / (1 + u * u), mp.sqrt, root=1)
    def C(S):
        t = tri(S); b, w, a = t['b'], t['w'], t['a']
        return det3(((w[4], b[4]), (0, a[4])), ((-w[5], b[5]), (w[5], b[5])), ((w[6], b[6]), (0, a[6])))
    S = mp.findroot(C, mp.mpf(e['S']), tol=mp.mpf(10) ** (-(K.dps - 20)))
    t = tri(S)
    worst = max(abs(x) for n, x in all_conditions(t))
    lim = mp.mpf(10) ** (-(K.dps - 50))
    dS = abs(S - mp.mpf(e['S']))
    cb = t['w'][1] ** 2 + t['b'][1] ** 2 - t['b'][1]; cc = t['w'][9] ** 2 + t['b'][9] ** 2 - t['b'][9]
    ok = worst < lim and abs(C(S)) < lim and order_ok(t, lim) and dS < mp.mpf(10) ** -50
    log(('ok   ' if ok else 'FAIL ') + f'E1 at {K.dps} digits: u, v, Q from the 90-digit refinement; S re-solved on E1\'s edge: the 4-line meeting at '
        f't5\'s corner holds to {mp.nstr(abs(C(S)), 3)}, worst Huet condition {mp.nstr(worst, 3)}, S agrees with the stored value to '
        f'{mp.nstr(dS, 3)}; t1, t9 corners inside the circle by {mp.nstr(-cb, 4)}, {mp.nstr(-cc, 4)} (in x^2 + d^2 - d)')
    return {i: (t['b'][i], t['w'][i], t['a'][i]) for i in range(1, 10)}, ok


def region_stats(K, Y, name, log):
    """areas, and the least value of each region's form (Omega_min = 2 x least polar area, at the region's Santalo point;
    for a triangle Omega_min = 27 / (2 area) exactly); spread/mean of each over the regions."""
    import mpmath as mp
    A = arrangement(K, Y); odd = [f for f in A['faces'] if f['c'] % 2]
    with mp.workdps(40):
        areas, omin, prod = [], [], []
        for f in odd:
            V = [(mp.mpf(p[0]), mp.mpf(p[1])) for p in f['V']]
            ar = abs(area2(V)) / 2
            if len(V) == 3:
                om = mp.mpf(27) / (2 * ar)
            else:
                g = lambda x, y: polar_area2(V, (x, y))
                X0 = B.centroid(V)
                sol = mp.findroot([lambda x, y: mp.diff(g, (x, y), (1, 0)), lambda x, y: mp.diff(g, (x, y), (0, 1))], X0)
                om = g(sol[0], sol[1])
            areas.append(ar); omin.append(om); prod.append(om * ar)
        cv = lambda L: mp.sqrt(sum((x - sum(L) / len(L)) ** 2 for x in L) / len(L)) / (sum(L) / len(L))
        r = {'n': len(odd), 'cv_area': float(cv(areas)), 'cv_omin': float(cv(omin)), 'cv_inv_omin': float(cv([1 / x for x in omin])),
             'omin_range': (float(min(omin)), float(max(omin))), 'omin_ratio': float(max(omin) / min(omin)),
             'omin_x_area': sorted({round(float(p), 6) for p in prod})}
    log(f'FIND {name}: {r["n"]} regions: spread/mean of the areas {r["cv_area"]:.6f}; of the least form values Omega_min {r["cv_omin"]:.6f} '
        f'(of 1/Omega_min {r["cv_inv_omin"]:.6f}); Omega_min from {r["omin_range"][0]:.4g} to {r["omin_range"][1]:.4g} (ratio {r["omin_ratio"]:.4g}); '
        f'Omega_min x area takes the values {r["omin_x_area"]} (27/2 for every triangle)')
    return r


def task(arg):
    name, dps = arg
    out = []; log = out.append; t0 = time.time()
    K = Ctx(dps)
    if name == 'E1': Y, ok0 = load_e1(K, log)
    elif name == 'GF1': Y, ok0 = B.load_gf1(K, log)
    else: Y, ok0 = Y45.load_kul(K, log)
    nm = f'{name}@{dps}'
    ok, res = analyse(K, Y, nm, log)
    res['stats'] = region_stats(K, Y, nm, log)
    res['fp'] = [str(v) for v in res['fp']]
    res['centre'] = [None if v is None else str(v) for v in res['centre']]
    res['rows'] = [(a, b, c, None if d is None else str(d), e, h) for a, b, c, d, e, h in res['rows']]
    log(f'{nm}: {time.time() - t0:.0f} s')
    return nm, ok and ok0, out, res


def main():
    t0 = time.time()
    tasks = [('E1', 120), ('GF1', 120)] if PILOT else [('E1', 300), ('E1', 600), ('GF1', 300), ('Kul', 300)]
    print(f'chunk 5c, E1: {len(tasks)} tasks on 4 cores', flush=True)
    results = {}; ok = True
    with get_context('fork').Pool(4) as pool:
        its = [pool.apply_async(task, (t,)) for t in tasks]
        for d, it in enumerate(its):
            name, good, out, res = it.get()
            for line in out: print(line, flush=True)
            print(f'PROGRESS {(d + 1) / len(tasks):.2f} {name}', flush=True)
            results[name] = res; ok = ok and good
    def say(c, m):
        nonlocal ok
        ok = ok and bool(c); print(('ok   ' if c else 'FAIL ') + m, flush=True)
    g = [v for k, v in results.items() if k.startswith('GF1')][0]
    say(g['counts']['regions'] == 43 and g['counts']['region_sides'] == {3: 43} and abs(Y45.QFstr(g['centre'][1]) + 86.08) < 0.01
        and g['table'].get("('sandhi', 2, 0)") == 24 and g['table'].get("('marma', 3, 2)") == 18,
        'positive control (known answer, chunk 5c): the DICTO Yantra again gives 43 triangles, 18 marmas of order 2, 24 sandhis, Omega_Y = -86.08 at the centre')
    e = [v for k, v in results.items() if k.startswith('E1')]
    say(e[0]['counts']['regions'] == 43 and abs(e[0]['stats']['cv_area'] - 0.614193120241354) < 1e-9,
        f'positive control (known answer, #103): E1 has 43 regions and spread/mean of the areas 0.614193120241 ({e[0]["stats"]["cv_area"]:.12f})')
    if len(e) == 2:
        import mpmath as mp
        mp.mp.dps = 320
        a, b = [mp.mpf(v) for v in e[0]['fp']], [mp.mpf(v) for v in e[1]['fp']]
        dev = max(abs(x - y) / abs(y) for x, y in zip(a, b))
        st = e[0]['table'] == e[1]['table'] and e[0]['counts'] == e[1]['counts']
        say(st and dev < mp.mpf(10) ** -200, f'E1 at 300 and 600 digits: same faces and point table; values agree to {mp.nstr(dev, 3)}')
    print('comparison (regions, sides, sandhis, centre Omega_Y, spread of areas, spread of Omega_min):', flush=True)
    for k, v in results.items():
        print(f'  {k}: {v["counts"]["regions"]} regions {v["counts"]["region_sides"]}, sandhis {v["table"].get("('sandhi', 2, 0)", "?")}, '
              f'sandhi |Res| {v["residues"].get("sandhi")}, centre {Y45.QFstr(v["centre"][1]):.6g}, cv area {v["stats"]["cv_area"]:.4f}, '
              f'cv Omega_min {v["stats"]["cv_omin"]:.4f}, Omega_min ratio {v["stats"]["omin_ratio"]:.4g}', flush=True)
    json.dump({k: {kk: vv for kk, vv in r.items() if kk not in ('pattern', 'rows')} for k, r in results.items()},
              open(os.path.join(HERE, '..', 'data', 'e1-regions-pilot.json' if PILOT else 'e1-regions.json'), 'w'), indent=1, default=str)
    print(f'total {time.time() - t0:.0f} s', flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL: see the FAIL lines above', flush=True)


if __name__ == '__main__':
    main()
