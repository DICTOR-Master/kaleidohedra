# r7_table.py -- the results table of item R7 from data/exact_census.json, plus the exact face-distance ratios of each solid
# (h_k^2 / h_max^2 for each face family, as a minimal polynomial over Q and, when it has one, a radical form), and three controls:
#  - positive: the cube's Star (t = 2) is the rhombic dodecahedron (the same solid, exactly; the regular census, 2026-11-09);
#  - negative: the octahedron's Star (t = 2) has the tetrakis hexahedron's corners but other faces (not that solid; it is not convex);
#  - negative: the cuboctahedron's Star Halo with its square feet pushed out by 1/100 is no longer the tetrakis hexahedron (exact).
# Usage: python -u r7_table.py <work dir> <exact_census.json> <out csv>
import sys, os, json, csv
from fractions import Fraction as Fr
import sympy as sp
W, IN, CSV_OUT = sys.argv[1:4]
sys.argv = [sys.argv[0], W, '/dev/null']          # exact_census reads its arguments at import; it is only used as a library here
src = open(os.path.join(os.path.dirname(__file__), 'exact_census.py')).read().split('res = []; fails = []')[0]
exec(src)
fails = []
def check(label, ok):
    print(('PASS ' if ok else 'FAIL ') + label, flush=True)
    if not ok: fails.append(label)
X = sp.Symbol('x')
def minpoly(e):
    F = e.F; n = F.n; cols = []
    for j in range(n):
        ej = F(*[1 if k == j else 0 for k in range(n)]); cols.append((e * ej).c)
    M = sp.Matrix(n, n, lambda i, j: sp.Rational(cols[j][i].numerator, cols[j][i].denominator))
    cp = M.charpoly(X).as_expr(); v = e.mp()
    for f, _ in sp.factor_list(cp)[1]:
        if abs(complex(f.subs(X, sp.Float(str(v), 60)))) < 1e-30: return sp.Poly(f, X).monic().as_expr()
    raise ValueError
def nice(e):
    p = minpoly(e); d = sp.degree(p, X)
    if d <= 2:
        for r in sp.solve(p, X):
            if abs(float(r) - float(e)) < 1e-12: return str(sp.nsimplify(sp.radsimp(r)))
    return f'root {float(e):.10f} of {p}'
R = json.load(open(IN)); rows = []
for rec in R:
    F, V, Fc = load(rec['slug']); feet, poles = feet_and_poles(V, Fc)
    fam = {}
    for f, x in zip(Fc, feet): fam.setdefault(len(f), []).append(dot(x, x))
    hmax = max((v[0] for v in fam.values()), key=lambda y: y.mp())
    for k, v in fam.items(): assert all(y == v[0] for y in v)    # one distance per face kind (vertex-transitive / face-transitive)
    ratios = {k: nice(v[0] / hmax) for k, v in sorted(fam.items())}
    def desc(part):
        r = rec[part]; ex = [m for m, s in r['exact_matches'] if s in ('same', 'same solid')]; co = [m for m, s in r['exact_matches'] if s == 'same corners only']
        known = '; '.join(ex) if ex else ('same corners as ' + '; '.join(co) + ', other faces' if co else 'NEW')
        cv = '' if 'convex' not in r else (', convex' if r['convex'] else ', not convex')
        return f"{r['corners']} corners, {r['faces']} faces {r['faces_by_sides']}, {r['symmetry']}{cv} -> {known}"
    row = dict(solid=rec['name'], family=rec['family'], field=rec['field'], face_kinds=len(fam),
               face_distance2_ratios='; '.join(f'{k}-gons {v}' for k, v in ratios.items()),
               star_halo=desc('centre_halo'), polar_halo=desc('polar_halo'), star_2=desc('star_2'), golden_star=desc('star_phi'))
    rows.append(row); print(' | '.join(str(v) for v in row.values()), flush=True)
with open(CSV_OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# controls
by = {r['slug']: r for r in R}
check('control (positive): the cube Star at t = 2 is exactly the rhombic dodecahedron (same corners and faces)',
      any(s == 'same solid' and 'rhombic dodecahedron' in m for m, s in by['cube']['star_2']['exact_matches']))
check('control (negative): the octahedron Star at t = 2 has the tetrakis hexahedron corners but other faces, and is not convex',
      any(s == 'same corners only' for m, s in by['octahedron']['star_2']['exact_matches']) and by['octahedron']['star_2']['convex'] is False)
F, V, Fc = load('cuboctahedron'); feet, _ = feet_and_poles(V, Fc)
pushed = [vmul(Fr(101, 100), x) if len(f) == 4 else x for f, x in zip(Fc, feet)]
HF, ok = exact_hull(pushed); _, TP, TF = load('tetrakis-hexahedron')
check('control (negative): the cuboctahedron halo with its square feet pushed out by 1/100 is NOT the tetrakis hexahedron (exact), the true halo IS',
      ok and same_up_to_scale(pushed, TP) is None and same_up_to_scale(feet, TP) is not None)
check('every Catalan Star Halo and Polar Halo is its Archimedean dual, exactly (one face family: the feet are h^2 times the poles)',
      all(any(s == 'same' for m, s in r[p]['exact_matches']) for r in R if r['family'] == 'Catalan' for p in ('centre_halo', 'polar_halo')))
check('every Archimedean Polar Halo is its Catalan dual, exactly',
      all(any(s == 'same' and 'Catalan' in m or s == 'same' for m, s in r['polar_halo']['exact_matches']) for r in R if r['family'] == 'Archimedean'))
print('FINAL ok' if not fails else 'FINAL FAIL')
