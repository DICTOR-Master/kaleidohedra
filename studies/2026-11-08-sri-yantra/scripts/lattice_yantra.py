"""The lattice yantra (DICTO 11-08: Matos's painting 'looks much better'; 'I would have assumed a triangular grid for triangles').
All nine triangles equilateral, tips on the axis, bases level. With one slope for every leg, every condition is LINEAR in the
depths (depth d from the top, circle diameter 1; a_i tip, b_i base):
  marma (down-leg i, base j, up-leg k):  b_j = (a_i + a_k)/2     (the two legs cross at the average of the tips' depths)
  tip on base:                           a_x = b_y
  corner of i on leg of j:               b_i = (a_i + a_j)/2
  great triangles inscribed and equilateral: a3 = 1, b3 = 1/4 (t3 tip at the bottom), a7 = 0, b7 = 3/4 (the hexagram).
Solve exactly; report whether the system is consistent, the free parameters left, a valid yantra, and the counts."""
import sympy as sp, json
a = sp.symbols('a1:10'); b = sp.symbols('b1:10'); A = dict(zip(range(1, 10), a)); B = dict(zip(range(1, 10), b))
eqs = []
for i, j, k in [(1, 2, 7), (2, 3, 7), (1, 3, 8), (1, 4, 6), (1, 5, 9), (4, 6, 9), (2, 7, 9), (3, 7, 8), (3, 8, 9)]:
    eqs.append(sp.Eq(B[j], (A[i] + A[k]) / 2))
for x, y in [(8, 1), (6, 2), (9, 3), (1, 6), (5, 7), (4, 8), (2, 9)]:
    eqs.append(sp.Eq(A[x], B[y]))
corner = [(4, 8), (5, 6), (6, 2)]          # corner of t4 on t8's leg, of t5 on t6's leg, of t6 on t2's leg
for i, j in corner: eqs.append(sp.Eq(B[i], (A[i] + A[j]) / 2))
eqs += [sp.Eq(A[3], 1), sp.Eq(B[3], sp.Rational(1, 4)), sp.Eq(A[7], 0), sp.Eq(B[7], sp.Rational(3, 4))]
sol = sp.solve(eqs, list(a) + list(b), dict=True)
print('equations', len(eqs), 'unknowns 18; solutions:', len(sol))
if not sol:
    # find which conditions clash: drop one family at a time
    for name, drop in (('corner touches', set(range(16, 19))),):
        sub = [e for n, e in enumerate(eqs) if n not in drop]; s2 = sp.solve(sub, list(a) + list(b), dict=True)
        print('without', name, ':', s2)
else:
    s = sol[0]; free = sorted({str(f) for v in s.values() for f in sp.sympify(v).free_symbols})
    print('free parameters left:', free)
    for i in range(1, 10): print(f'  t{i}: tip {s.get(A[i], A[i])}, base {s.get(B[i], B[i])}')
    json.dump({str(k): str(v) for k, v in s.items()}, open('lattice.json', 'w'), indent=1)
print('FINAL ok' if sol else 'FINAL FAIL: the equilateral system is inconsistent')
