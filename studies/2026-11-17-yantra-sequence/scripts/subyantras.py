"""The 3-, 5- and 7-triangle yantras inside a nine-triangle yantra (17 Nov 2026): take off the pairs
(t4, t8), then (t1, t6), then (t2, t9) (the only way to take off one up-and-down pair at a time keeping
every remaining apex on a remaining base, family.py) and count what remains.  Run on R1 and Q3 (exact),
the DICTO Yantra and Kulaichev's yantra (stored decimals, points merged within 1e-25).
usage: python3 subyantras.py <study dir>"""
import sys, os, json
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else '.']
ST = sys.argv[1]
from yarr import Arr, QF
import calibrate_loaders as CL

KEEP = {9: list(range(1, 10)), 7: [1, 2, 3, 5, 6, 7, 9], 5: [2, 3, 5, 7, 9], 3: [3, 5, 7]}


def quad_example(name):
    e = json.load(open(os.path.join(ST, 'data', 'input', 'quadratic-examples.json')))[name]
    if e['Delta'] is None:
        g = lambda z: Fr(z['a'])
    else:
        QF.D = Fr(e['Delta']); g = lambda z: QF(Fr(z['a']), Fr(z.get('b', '0')))
    return [(g(e['b'][str(i)]), g(e['w'][str(i)]), g(e['apex'][str(i)])) for i in range(1, 10)]


EPS, EPSC = Fr(1, 10 ** 25), Fr(1, 10 ** 22)
out = {}
for name, loader, eps in (('R1', lambda: quad_example('R1'), None), ('DICTO Yantra', lambda: CL.gf1(ST), EPS),
                          ('Q3', lambda: quad_example('Q3'), None), ('Kulaichev', lambda: CL.kulaichev(ST), EPS)):
    T9 = loader()
    out[name] = {}
    for n in (3, 5, 7, 9):
        T = [T9[i - 1] for i in KEEP[n]]
        r = Arr(T, eps, EPSC if eps else None).analyse(); r.pop('area2')
        out[name][n] = r
        print(f"{name:13s} n={n}: odd {r['odd']:3d} rings {[r['rings'].get(c, 0) for c in range(1, n + 1, 2)]} "
              f"({r['odd_tri']} tri, {r['odd_quad']} four-sided, {r['odd_other']} other); star {r['star']} {r['star_by']}; "
              f"all regions {r['faces']} = {r['tri']} tri + {r['quad']} four + {r['other']} other", flush=True)
json.dump(out, open(os.path.join(ST, 'data', 'subyantras.json'), 'w'), indent=1, default=str)
same = {n: len({out[k][n]['odd'] for k in out}) == 1 for n in (3, 5, 7, 9)}
print('one odd-region count across the four yantras, by n:', same)
ok = (out['DICTO Yantra'][9]['odd'] == 43 and out['R1'][9]['odd'] == 43 and out['Kulaichev'][9]['odd'] == 45
      and out['Q3'][9]['odd'] == 45 and all(len(out[k]) == 4 for k in out))
print("FINAL ok" if ok else "FINAL FAIL (calibration at n = 9)")
