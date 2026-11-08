"""Which conditions make the all-equilateral yantra impossible? Drop the fewest equations (any 1, then any 2) from the 23 of
lattice_yantra.py and report every consistent choice that still gives a VALID yantra (tips and bases in the right order, every
triangle of positive size). Names each dropped condition."""
import sympy as sp, itertools, json
a = sp.symbols('a1:10'); b = sp.symbols('b1:10'); A = dict(zip(range(1, 10), a)); B = dict(zip(range(1, 10), b))
E = []
for i, j, k in [(1, 2, 7), (2, 3, 7), (1, 3, 8), (1, 4, 6), (1, 5, 9), (4, 6, 9), (2, 7, 9), (3, 7, 8), (3, 8, 9)]:
    E.append((f'marma ({i},{j},{k})', sp.Eq(B[j], (A[i] + A[k]) / 2)))
for x, y in [(8, 1), (6, 2), (9, 3), (1, 6), (5, 7), (4, 8), (2, 9)]: E.append((f'tip of t{x} on base of t{y}', sp.Eq(A[x], B[y])))
for i, j in [(4, 8), (5, 6), (6, 2)]: E.append((f'corner of t{i} on t{j}', sp.Eq(B[i], (A[i] + A[j]) / 2)))
E += [('t3 tip at bottom', sp.Eq(A[3], 1)), ('t3 base 1/4', sp.Eq(B[3], sp.Rational(1, 4))), ('t7 tip at top', sp.Eq(A[7], 0)), ('t7 base 3/4', sp.Eq(B[7], sp.Rational(3, 4)))]
DOWN = [1, 2, 3, 4, 5]
def valid(s):
    try:
        vals = {k: float(v) for k, v in s.items() if not sp.sympify(v).free_symbols}
    except Exception: return False
    if len(vals) < 18: return None            # free parameters left: report separately
    for i in range(1, 10):
        ai, bi = vals[A[i]], vals[B[i]]
        if not (0 <= ai <= 1 and 0 <= bi <= 1): return False
        if (i in DOWN and not ai > bi) or (i not in DOWN and not bi > ai): return False
    return True
found = []
for k in (1, 2):
    for drop in itertools.combinations(range(len(E)), k):
        sub = [e for n, (nm, e) in enumerate(E) if n not in drop]
        s = sp.solve(sub, list(a) + list(b), dict=True)
        if s:
            v = valid(s[0]); found.append(([E[n][0] for n in drop], v, s[0]))
    if found: break
print('fewest conditions to drop:', k if found else '>2')
for names, v, s in found:
    print('  drop', names, '->', 'valid yantra' if v else ('free parameters left' if v is None else 'invalid (order/size)'))
json.dump([[n, str(v)] for n, v, s in found], open('lattice-clash.json', 'w'), indent=1)
print('FINAL ok' if found else 'FINAL FAIL: dropping two conditions is not enough')
