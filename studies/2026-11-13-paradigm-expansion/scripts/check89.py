# Check, against #89's own data and construction, the reading proposed for the Paradigm book (PROPOSAL.html, "to check"):
# every section of the tesseract across a long diagonal is a permutohedron of repeated values.
# #89 (studies/2026-11-03-golden-cuts-beyond-plato, s5_exact4d.py and data/s5-exact4d.json): tesseract corners (±1)^4,
# hyperplanes x1 + x2 + x3 + x4 = 2h, corner layers h = 0 (6 corners), ±1 (4), ±2 (1); for 0 < h < 1 the section is the
# tetrahedron cut at x = (1 − h)/(2 − h). The sections are computed here exactly in R^4 (not projected), with #89's own
# edge-crossing rule, at #89's stored heights and at control heights, and compared with the orderings of a value vector.
import itertools, json, os, sys
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
S89 = os.path.expanduser(os.environ.get('S89', '' + os.path.join(HERE, '..', 'data', 's5-exact4d-from-89.json') + ''))
ok_all = True
def check(name, ok):
    global ok_all; ok_all &= bool(ok); print(('PASS ' if ok else 'FAIL ') + name, flush=True)
V = [sp.Matrix(v) for v in itertools.product([1, -1], repeat=4)]
def section(h):
    pts = set()
    for v in V:
        if sp.simplify(sum(v) - 2 * h) == 0: pts.add(tuple(sp.nsimplify(c) for c in v))
    for i, j in itertools.combinations(range(16), 2):
        if sum(abs(V[i][k] - V[j][k]) for k in range(4)) != 2: continue
        a, b = sum(V[i]) - 2 * h, sum(V[j]) - 2 * h
        if sp.N(a * b) < 0:
            t = a / (a - b); p = V[i] + t * (V[j] - V[i]); pts.add(tuple(sp.radsimp(sp.simplify(c)) for c in p))
    return pts
def orderings(vals): return {tuple(sp.radsimp(sp.simplify(c)) for c in p) for p in itertools.permutations(vals)}
def eq(A, B): return len(A) == len(B) and all(any(all(sp.simplify(a[k] - b[k]) == 0 for k in range(4)) for b in B) for a in A)
data = json.load(open(S89)); rows = data['sections']['tesseract']
check(f"#89 data read: {len(rows)} tesseract rows", len(rows) == 3)
for r in rows:
    h = sp.nsimplify(sp.sympify(r['height'])); S = section(h); W = orderings([-1, 2 * h - 1, 1, 1])
    # on [0,1] scale: (x + 1)/2 gives the values 0, h, 1, 1
    check(f"#89 height h = {r['height']} ({r['solid']}): {len(S)} corners = the orderings of (−1, 2h − 1, 1, 1), i.e. of (0, h, 1, 1) after x ↦ (x + 1)/2", eq(S, W) and len(S) == 12)
    x = (1 - h) / (2 - h)
    check(f"   its hexagons have sides in the ratio of the gaps h : 1 − h, and the cut x = (1 − h)/(2 − h) = {sp.nsimplify(sp.radsimp(x))} gives short : long = x : (1 − 2x) = (1 − h) : h", sp.simplify(x / (1 - 2 * x) - (1 - h) / h) == 0)
for h, vals, what in ((sp.Rational(1, 3), [-1, sp.Rational(-1, 3), 1, 1], '0 < h < 1'), (sp.Rational(3, 2), [2 * sp.Rational(3, 2) - 3, 1, 1, 1], '1 < h < 2: a regular tetrahedron, values (2h − 3, 1, 1, 1)'),
                      (sp.Integer(0), [-1, -1, 1, 1], 'h = 0: the octahedron, values (−1, −1, 1, 1)'), (sp.Integer(1), [-1, 1, 1, 1], 'h = 1: a layer of 4 corners, values (−1, 1, 1, 1)')):
    S = section(h); check(f"control h = {h} ({what}): section = orderings of {vals}", eq(S, orderings(vals)))
# negative control: a non-diagonal direction is not a permutohedron section in general
pts = set()
for i, j in itertools.combinations(range(16), 2):
    if sum(abs(V[i][k] - V[j][k]) for k in range(4)) != 2: continue
    f = lambda v: v[0] + 2 * v[1] + 3 * v[2] + 4 * v[3] - 1
    a, b = f(V[i]), f(V[j])
    if a * b < 0: t = sp.Rational(a, a - b); pts.add(tuple(V[i] + t * (V[j] - V[i])))
check(f"negative control: the section by x1 + 2x2 + 3x3 + 4x4 = 1 ({len(pts)} corners) is not closed under permuting coordinates", any(tuple(p[k] for k in (1, 0, 2, 3)) not in pts for p in pts))
print('FINAL ok' if ok_all else 'FINAL FAIL')
sys.exit(0 if ok_all else 1)
