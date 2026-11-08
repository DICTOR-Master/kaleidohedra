"""The one-slope (grid) yantra (DICTO 11-08: triangular grid, then the Cleo grid). With one leg slope s, the 18 marmas and the 7
tips-on-bases fix every depth up to scale and shift: heights t5 : t1 : t4 : t6 : t8 : t9 : t2 : t3 : t7 = 2 : 4 : 4 : 4 : 6 : 6 : 8 : 8 : 9.
Place t7 (height 9) with its tip at the top of the circle and its corners on the circle; the slope s then sets the scale. Two grids:
equilateral (s = 1/sqrt3, as in the Matos painting) and the Cleo grid (s = 1/phi, the Cleo-Icos side face). json for figure.py."""
import sympy as sp, json
a = sp.symbols('a1:10'); b = sp.symbols('b1:10'); A = dict(zip(range(1, 10), a)); B = dict(zip(range(1, 10), b))
E = [sp.Eq(B[j], (A[i] + A[k]) / 2) for i, j, k in [(1, 2, 7), (2, 3, 7), (1, 3, 8), (1, 4, 6), (1, 5, 9), (4, 6, 9), (2, 7, 9), (3, 7, 8), (3, 8, 9)]]
E += [sp.Eq(A[x], B[y]) for x, y in [(8, 1), (6, 2), (9, 3), (1, 6), (5, 7), (4, 8), (2, 9)]]
k = sp.symbols('k', positive=True)
s0 = sp.solve(E + [sp.Eq(A[7], 0), sp.Eq(B[7], 9 * k)], list(a) + list(b), dict=True)[0]
out = {}; ok = True
for name, s in (('equilateral grid (s = 1/sqrt3)', 1 / sp.sqrt(3)), ('Cleo grid (s = 1/phi)', 2 / (1 + sp.sqrt(5)))):
    kv = [x for x in sp.solve(sp.Eq((s * 9 * k)**2 + (9 * k - sp.Rational(1, 2))**2, sp.Rational(1, 4)), k) if x > 0][0]
    dep = {i: (sp.simplify(s0.get(A[i], A[i]).subs(k, kv)), sp.simplify(s0.get(B[i], B[i]).subs(k, kv))) for i in range(1, 10)}
    w = {i: sp.simplify(s * abs(dep[i][0] - dep[i][1])) for i in range(1, 10)}
    key = 'G' + str(len(out) + 1)
    out[key] = {'label': name, 'b': {str(i): {'a': str(sp.N(dep[i][1], 40))} for i in dep}, 'w': {str(i): {'a': str(sp.N(w[i], 40))} for i in dep}, 'apex': {str(i): {'a': str(sp.N(dep[i][0], 40))} for i in dep}}
    off = {i: float(sp.N(sp.sqrt(w[i]**2 + (dep[i][1] - sp.Rational(1, 2))**2) - sp.Rational(1, 2), 8)) for i in (1, 3, 9)}
    print(key, name, ': unit k =', sp.nsimplify(kv), '; t3 tip depth', float(sp.N(dep[3][0])), '(circle bottom 1); corners off the circle (+ outside):', {i: round(v, 4) for i, v in off.items()})
    ok = ok and all(0 <= float(sp.N(dep[i][0])) <= 1.0000001 for i in dep)
json.dump(out, open('grid.json', 'w'), indent=1)
print('FINAL ok' if ok else 'FINAL FAIL: a tip lies outside the circle')
