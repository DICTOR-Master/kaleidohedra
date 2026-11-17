"""Calibration (17 Nov 2026): the counter of yarr.py on four nine-triangle yantras of #103.
Exact: R1 (rational, Theorem 2) and Q3 (in Q(sqrt Delta), u = v = 3/4).  Stored decimals: the DICTO Yantra
(GF1, 40 digits) and Kulaichev's yantra (60 digits), points merged within 1e-25.
Expected (#103 Proposition 3, Proposition 11; study 2026-11-15-chapati-vs-103):
  odd regions 43 = 14, 10, 10, 8, 1 (all triangles) for R1 and GF1; 45 = 14, 10, 12, 8, 1 (41 triangles,
  4 four-sided) for Q3 and Kulaichev; bounded regions 74 = 53 triangles + 21 four-sided for GF1 (and R1);
  78 = 53 + 25 for Kulaichev (and Q3).  Star points, outline taken from the arrangement (yarr.py):
  43 = 14, 10, 10, 8, 1 for R1 and GF1, the same per circuit as Chapati and Chapati's code; on Q3 and
  Kulaichev's yantra this version gives 45 = 14, 10, 10, 10, 1 (the eight-cornered outline has two more
  convex corners), where Chapati's code, with Huet's transcribed outlines, gives 43 (chapati_cross.py).
usage: python3 calibrate.py <study dir>"""
import sys, os, json, re
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yarr import Arr, QF

ST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
INP = os.path.join(ST, 'data', 'input')


def quad_example(name):
    e = json.load(open(os.path.join(INP, 'quadratic-examples.json')))[name]
    if e['Delta'] is None:                        # R1: every coordinate rational
        def g(z):
            assert Fr(z.get('b', '0')) == 0
            return Fr(z['a'])
    else:
        QF.D = Fr(e['Delta'])
        def g(z):
            return QF(Fr(z['a']), Fr(z.get('b', '0')))
    return [(g(e['b'][str(i)]), g(e['w'][str(i)]), g(e['apex'][str(i)])) for i in range(1, 10)]


def gf1():
    g = json.load(open(os.path.join(INP, 'golden_family.json')))['GF1']
    f = lambda z: Fr(z['a']) if isinstance(z, dict) else Fr(z)
    return [(f(g['b'][str(i)]), f(g['w'][str(i)]), f(g['apex'][str(i)])) for i in range(1, 10)]


def kulaichev():
    txt = open(os.path.join(INP, 'kulaichev-numeric-data.txt')).read()
    b = {int(m.group(1)): Fr(m.group(2)) for m in re.finditer(r"b(\d) = ([0-9.]+)", txt)}
    w = {int(m.group(1)): Fr(m.group(2)) for m in re.finditer(r"w(\d) = ([0-9.]+)", txt)}
    a = {8: b[1], 6: b[2], 9: b[3], 1: b[6], 5: b[7], 4: b[8], 2: b[9], 3: Fr(1), 7: Fr(0)}
    return [(b[i], w[i], a[i]) for i in range(1, 10)]


EPS, EPSC = Fr(1, 10 ** 25), Fr(1, 10 ** 22)
runs = [('R1 (exact, rational)', quad_example('R1'), None),
        ('Q3 (exact, Q(sqrt Delta))', quad_example('Q3'), None),
        ('DICTO Yantra GF1 (40 digits)', gf1(), EPS),
        ('Kulaichev yantra (60 digits)', kulaichev(), EPS)]
res = {}
for name, T, eps in runs:
    if name.startswith('Q3'):
        quad_example('Q3')
    if name.startswith('R1'):
        quad_example('R1')
    r = Arr(T, eps, EPSC if eps else None).analyse()
    r.pop('area2')
    res[name] = r
    print(f"{name}: bounded regions {r['faces']} = {r['tri']} triangles + {r['quad']} four-sided + {r['other']} other; "
          f"rings {r['rings']}; odd {r['odd']} ({r['odd_tri']} triangles, {r['odd_quad']} four-sided); "
          f"star points {r['star']} {r['star_by']}", flush=True)

ring = lambda r: [r['rings'].get(c, 0) for c in (1, 3, 5, 7, 9)]
T43, T45 = [14, 10, 10, 8, 1], [14, 10, 10, 10, 1]
want = {'R1': (43, [14, 10, 10, 8, 1], 43, 0, 43, T43, 74, 53, 21),
        'Q3': (45, [14, 10, 12, 8, 1], 41, 4, 45, T45, 78, 53, 25),
        'DICTO': (43, [14, 10, 10, 8, 1], 43, 0, 43, T43, 74, 53, 21),
        'Kulaichev': (45, [14, 10, 12, 8, 1], 41, 4, 45, T45, 78, 53, 25)}
bad = []
for name, r in res.items():
    key = [k for k in want if name.startswith(k)][0]
    got = (r['odd'], ring(r), r['odd_tri'], r['odd_quad'], r['star'], r['star_by'], r['faces'], r['tri'], r['quad'])
    if got != want[key]:
        bad.append((name, got, want[key]))
json.dump(res, open(os.path.join(ST, 'data', 'calibration.json'), 'w'), indent=1, default=str)
print("FINAL ok" if not bad and len(res) == 4 else f"FINAL FAIL {bad}")
