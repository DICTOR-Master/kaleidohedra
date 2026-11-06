"""Football scutoid study, step 3a part 3: closed forms. Rebuild the three contact planes of the closest stacking in exact arithmetic
(sympy, sqrt(5) and the radicals of the unit axes; gap g kept as a SYMBOL so the result holds for every gap), solve for (h, a, b),
and check against the 60-digit values of stack_solve.py at g = 3/5."""
import json, sys, numpy as np, sympy as sp
P = json.load(open('../data-stack-planes.json'))
sys.argv = [sys.argv[0], '0.6']
exec(open('grid_layer.py').read().split('# overlap test')[0].replace('print(', '(lambda *a, **k: None)('))
s5 = sp.sqrt(5); phi = (1 + s5) / 2; g = sp.Symbol('g', positive=True)
cands = [0, 1, 2, phi, 2 * phi, 3 * phi, 2 + phi, phi ** 3]
def ex(x):
    out = []
    for c in x * 2:
        m = min(cands, key=lambda t: abs(float(t) - abs(c))); assert abs(float(m) - abs(c)) < 1e-9; out.append(sp.nsimplify(m) / 2 * (1 if c >= 0 else -1))
    return sp.Matrix(out)
VE = [ex(v) for v in V]
cen = lambda idx: sum((VE[i] for i in idx), sp.zeros(3, 1)) / len(idx)
A5, C3 = cen(P['face_a']), cen(P['face_c'])
H5, H6 = sp.sqrt(sp.simplify(A5.dot(A5))), sp.sqrt(sp.simplify(C3.dot(C3)))
E1, E2 = A5 / H5, C3 / H6; DD = H5 + H6 + g
bis = (E1 + E2); RY = 2 * bis * bis.T / sp.simplify(bis.dot(bis)) - sp.eye(3)
nrm = E1.cross(E2); P1, P2 = 2 * DD * E1, DD * (E1 + E2)
def ballv(i, j, k):
    R = sp.eye(3) if (i + j) % 2 == 0 else RY
    return R * VE[k] + DD * (i * E1 + j * E2)
h, a, b = sp.symbols('h a b')
T = h * nrm / sp.sqrt(sp.simplify(nrm.dot(nrm))) + a * P1 + b * P2
eqs = []
for pl in P['planes']:
    pts = [ballv(*pl['A'], k // 60) - ballv(*pl['B'], k % 60) - (pl['p'] * P1 + pl['q'] * P2) for k in pl['k']]
    nn = (pts[1] - pts[0]).cross(pts[2] - pts[0])
    eqs.append(sp.expand(nn.dot(T - pts[0])))
sol = sp.solve(eqs, [h, a, b], dict=True)[0]
print(f"H5 (centre to pentagon) = {sp.nsimplify(sp.simplify(H5))}, H6 (centre to hexagon) = {sp.simplify(H6)}")
import re as _re
h60 = float(_re.search(r'^h = ([\d.]+)', open('../data-stack-solve.txt').read(), _re.M).group(1)); vals = {}
for k in (a, b, h):
    e = sp.simplify(sp.radsimp(sol[k]))
    print(f"{k}(g) = {e}")
    v = sp.N(e.subs(g, sp.Rational(3, 5)), 40)
    print(f"   at g = 3/5: {v}"); vals[str(k)] = v
print("FINAL ok" if abs(float(vals["h"]) - h60) < 1e-12 else "FINAL FAIL (closed form does not match the 60-digit solve)")