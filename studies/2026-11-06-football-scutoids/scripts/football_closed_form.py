"""Football scutoid study, step 3e (DICTO 11-07: "go ahead with cos 6° closed form"): h and b written exactly in Q(cos π/30).
Exact algebra only (no numerical fitting): K = Q(c), c = 2 cos 6°, defined by x^8 − 7x^6 + 14x^4 − 8x^2 + 1 (step 3d). The minimal
polynomials of h and b (data-algdep.txt) are factored over K (PARI nfroots); the root that equals the 60-digit value is chosen by
evaluating at c = 2 cos 6°. Then √3, √5 and w = √(10 + 2√5) = 4 cos 18° are written in K the same way, and h, b are solved exactly in
the basis {1, √3} × {1, √5, w, √5·w} (a linear system over Q). Checks: the basis is independent (rank 8) and the expressions agree with
the 60-digit values. Run: python3 tools/runjob.py <this> <data file>"""
import re, math, cypari2
pari = cypari2.Pari()
txt = open('../data-algdep.txt').read()
polys = {k: pari(re.search(rf'^{k} \([^)]*\): minimal polynomial[^\n]*\n\s+(.+)$', txt, re.M).group(1)) for k in ('h', 'b')}
target = {'h': 3.437002375099093176690586445664303449286, 'b': 0.5610735087101498959736905116890006202855}
K = pari.nfinit('y^8 - 7*y^6 + 14*y^4 - 8*y^2 + 1')
c = 2 * math.cos(math.pi / 30)
ev = lambda e: float(pari.subst(pari.lift(e), 'y', c))
def root_in_K(P, val):   # P in x with rational coefficients; returns the root in K (polynomial in y) that equals val at y = c
    rs = [r for r in pari.nfroots(K, P) if abs(ev(r) - val) < 1e-9]
    assert len(rs) == 1, (P, val, len(rs)); return pari.lift(rs[0])
s3, s5 = root_in_K(pari('x^2-3'), 3 ** .5), root_in_K(pari('x^2-5'), 5 ** .5)
w = root_in_K(pari('x^4-20*x^2+80'), (10 + 2 * 5 ** .5) ** .5)          # w^2 = 10 + 2√5  =>  (w^2 − 10)^2 = 20
names = ['1', '√3', '√5', '√15', 'w', '√3·w', '√5·w', '√15·w']
basis = [pari(1), s3, s5, s3 * s5, w, s3 * w, s5 * w, s3 * s5 * w]
M = pari.matconcat([pari.nfalgtobasis(K, pari.Mod(b_, K[0]) if b_ != 1 else 1) for b_ in basis])
print(f"basis rank {pari.matrank(M)} of 8; c = 2 cos 6° = {c:.15f}")
ok = pari.matrank(M) == 8
for k, P in polys.items():
    e = root_in_K(P, target[k])
    coef = pari.matsolve(M, pari.nfalgtobasis(K, pari.Mod(e, K[0])))
    val = sum(float(q) * ev(b_ if b_ != 1 else pari(1)) for q, b_ in zip(coef, basis))
    good = abs(val - target[k]) < 1e-12; ok &= good
    print(f"{k} = " + ' + '.join(f"({q})·{n}" for q, n in zip(coef, names) if q != 0))
    print(f"   = {val:.15f} (60-digit value {target[k]:.15f}): {'EXACT, agrees' if good else 'MISMATCH'}")
    print(f"   as a polynomial in c = 2 cos 6°: {k} = {pari.subst(e, 'y', 'c')}")
print("   where w = √(10 + 2√5) = 4 cos 18°")
print("FINAL ok" if ok else "FINAL FAIL (basis or values did not check)")
