"""Traditional counts for a yantra given by base depth b, half-width w, apex a (data files): number of up / down triangles,
points where exactly three sides meet (marmas, tradition 18), points where exactly two sides cross (sandhis), corners of one
triangle lying on another's side (touches). Exact Fractions from the stored decimals; a point counts as a meeting when the
lines agree to 1e-30 (stored values carry 40 digits). Also the 43 small triangles via figure.py's own count (not repeated here)."""
import json, itertools, sys
from fractions import Fraction as F
def load(path, key):
    e = json.load(open(path))[key]; g = lambda d: {int(k): F(v['a']) for k, v in d.items()}
    return g(e['b']), g(e['w']), g(e['apex'])
def counts(b, w, a):
    segs = []
    for i in b:
        L, R, A = (-w[i], b[i]), (w[i], b[i]), (F(0), a[i]); segs += [((L, R), i), ((L, A), i), ((R, A), i)]
    TOL = F(1, 10**30); pts = []
    def same(p, q): return abs(p[0] - q[0]) < TOL and abs(p[1] - q[1]) < TOL
    for (s, i), (t, j) in itertools.combinations(segs, 2):
        (x1, y1), (x2, y2) = s; (x3, y3), (x4, y4) = t
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0: continue
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
        on = lambda p, q: min(p[0], q[0]) - TOL <= px <= max(p[0], q[0]) + TOL and min(p[1], q[1]) - TOL <= py <= max(p[1], q[1]) + TOL
        if not (on(*s) and on(*t)): continue
        for P in pts:
            if same(P[0], (px, py)): P[1].update({id(s), id(t)}); break
        else: pts.append([(px, py), {id(s), id(t)}])
    corners = [((-w[i], b[i]), i) for i in b] + [((w[i], b[i]), i) for i in b] + [((F(0), a[i]), i) for i in b]
    def is_corner(p): return any(same(p, c) for c, _ in corners)
    marma = sum(1 for p, s in pts if len(s) == 3 and not is_corner(p))
    sandhi = sum(1 for p, s in pts if len(s) == 2 and not is_corner(p))
    up = sum(1 for i in b if a[i] < b[i]); down = len(b) - up
    return up, down, marma, sandhi
rows = [('DICTO Yantra (K1, Cleo-Octangula)', 'figures/kites.json', 'K1'), ('K2 (stella above, Cleo below)', 'figures/kites.json', 'K2'),
        ('K3 (golden phi/2 above, stella below)', 'figures/kites.json', 'K3'), ('Cleo yantra (rhombus)', 'figures/cleo-yantra.json', 'Cleo'),
        ('R1 rational', 'data/quadratic-examples.json', 'R1')]
res = {}
for name, path, key in rows:
    up, down, m, sa = counts(*load(path, key)); res[name] = (up, down, m, sa)
    print(f'{name}: up {up}, down {down}, marmas (three lines) {m}, sandhis (two lines) {sa}')
ok = res['DICTO Yantra (K1, Cleo-Octangula)'] == (4, 5, 18, 24)
print('FINAL ok' if ok else 'FINAL FAIL: the DICTO Yantra misses a traditional count (4 up, 5 down, 18 marmas, 24 sandhis)')
