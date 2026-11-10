"""B1 #81 exact check at a FIXED depth (DICTO 10 Nov: clear outcomes). Uses chain_sym5.py's exact routines (field Q(sqrt5)(s)) with the
two-fold feet set to the constant s0, so no polynomial in s grows. Checks: step 4 is step 0 scaled by 10/phi^4 = 35 - 15 sqrt5 (same
corner directions, exact ratio). Usage: python chain_exact_fixed5.py s0"""
import sys, time
sys.argv = [sys.argv[0], sys.argv[1], '0']
src = open('chain_sym5.py').read().split("if __name__ == '__main__':")[0]
exec(src)
import itertools
s0 = Fr(sys.argv[1]); ph = (1 + r5) / 2; t0 = time.time()
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
five = {tuple(sp.nsimplify(x) for x in w) for a, b in itertools.product((1, -1), repeat=2) for w in cyc((0, a, b * ph))}
two = {w for c in (1, -1) for w in cyc((0, 0, c * ph))}
two |= {w for a, b, c in itertools.product((1, -1), repeat=3) for w in cyc((sp.Rational(a, 2), b * ph ** 2 / 2, c * ph / 2))}
five = [tuple(kel(sp.expand(x)) for x in v) for v in five]; two = [tuple(kel(sp.expand(x)) for x in v) for v in two]
planes = [(n, dot(n, n)) for n in five] + [(n, kel(sp.Rational(s0.numerator, s0.denominator)) * dot(n, n)) for n in two]
V, T, polys, kinds = sym_halfspace(planes, s0); hist = [V]
print(f'step 0: {len(V)} corners ({time.time()-t0:.0f} s)', flush=True)
for k in range(1, 5):
    V, T, polys, kinds = sym_halfspace([(v, dot(v, v)) for v in V], s0); hist.append(V)
    print(f'step {k}: {len(V)} corners ({time.time()-t0:.0f} s)', flush=True)
g = similar_sym(hist[0], hist[4])
target = kel(sp.expand((35 - 15 * r5) ** 2))          # similar_sym returns the ratio of SQUARED lengths
eq = g is not None and not (g - target).numer
print('step 4 similar to step 0 (exact):', g is not None, '; squared scale =', sp.nsimplify(sp.simplify(K.to_sympy(g))) if g is not None else None, '; equals (35 - 15 sqrt5)^2:', eq)
print('FINAL ok' if eq else 'FINAL FAIL: exact closure not confirmed')
