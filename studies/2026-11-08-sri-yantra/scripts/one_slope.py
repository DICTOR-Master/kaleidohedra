"""Can any yantra have all nine triangles similar (one leg slope s for all: equilateral grid s = 1/sqrt3, the Cleo grid s = 1/phi, any
s)? With one slope the marma, tip-on-base and corner conditions do not involve s: two legs of slope s cross at the average of their
tips depths. Solve those 19 homogeneous linear conditions alone: if every solution has all tips and bases at one depth (zero-size
triangles), no yantra with one slope exists, for every s at once."""
import sympy as sp
a = sp.symbols("a1:10"); b = sp.symbols("b1:10"); A = dict(zip(range(1, 10), a)); B = dict(zip(range(1, 10), b))
E = [sp.Eq(B[j], (A[i] + A[k]) / 2) for i, j, k in [(1, 2, 7), (2, 3, 7), (1, 3, 8), (1, 4, 6), (1, 5, 9), (4, 6, 9), (2, 7, 9), (3, 7, 8), (3, 8, 9)]]
E += [sp.Eq(A[x], B[y]) for x, y in [(8, 1), (6, 2), (9, 3), (1, 6), (5, 7), (4, 8), (2, 9)]]
results = []
for name, extra in (("marmas + tips on bases", []), ("+ corner touches", [sp.Eq(B[i], (A[i] + A[j]) / 2) for i, j in [(4, 8), (5, 6), (6, 2)]])):
    s = sp.solve(E + extra, list(a) + list(b), dict=True)[0]
    vals = {k: sp.simplify(v) for k, v in s.items()}
    free = sorted({str(f) for v in vals.values() for f in sp.sympify(v).free_symbols})
    sizes = [sp.simplify(vals.get(A[i], A[i]) - vals.get(B[i], B[i])) for i in range(1, 10)]
    print(name + ": free", free, "; triangle sizes (tip - base):", sizes)
    degenerate = all(z == 0 for z in sizes)
    print("   every triangle has zero size:", degenerate); results.append(degenerate)
print("FINAL ok" if results == [False, True] else "FINAL FAIL: expected a proper solution without corner touches and only zero size with them")
