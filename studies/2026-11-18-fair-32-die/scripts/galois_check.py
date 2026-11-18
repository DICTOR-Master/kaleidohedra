# For each fair die's (R/r)^2: discriminant primes, normality and abelianness (roots as Q-polynomials of one root, by PSLQ at
# 400 digits, then commutation of the automorphisms checked numerically). Abelian = lies in the field of some regular polygon
# (Kronecker-Weber).
import sympy as sp
from mpmath import mp, mpf, pslq, polyroots, nstr
mp.dps = 400
X = sp.symbols('x')
POLYS = {
 'tr (16)': [-82944, 1050624, -2972160, 3545088, -2222080, 724800, -108432, 5616, -81],
 'co (14, Lucky 7)': [-7, 35, -21, 1],
 'tc (10)': [-6561, 285768, -358668, 290376, -133510, 28696, -2508, 88, -1],
 'cr (18)': [81, -648, 1620, -1872, 1440, -576, 64],
 'or (20)': [144, -432, 412, -132, 9],
 'di (32)': [-625, 35000, -255500, 609000, -483350, 121800, -10220, 280, -1],
}
allok = True
for name, c in POLYS.items():
    P = sum(k*X**i for i, k in enumerate(c)); d = len(c) - 1
    disc = sp.discriminant(P, X); fac = sp.factorint(abs(disc))
    roots = polyroots(list(reversed([mpf(k) for k in c])), maxsteps=4000, extraprec=2000)
    nreal = sum(1 for r in roots if abs(mp.im(r)) < mpf(10)**-300)
    if 0 < nreal < d:
        print(name, '| degree', d, '| disc primes', sorted(fac), '| real roots', nreal, 'of', d, '=> mixed signature: not Galois, so not abelian (no polygon field)', flush=True); continue
    r0 = roots[0]
    maps = []
    for r in roots:
        rel = pslq([r] + [r0**k for k in range(d)], maxcoeff=10**30, maxsteps=10**7)
        maps.append(rel)
    normal = all(m is not None and m[0] != 0 for m in maps)
    abelian = None
    if normal:
        g = [[-mpf(m[k+1])/m[0] for k in range(d)] for m in maps]
        ev = lambda coeffs, z: sum(coeffs[k]*z**k for k in range(d))
        abelian = all(abs(ev(g[i], ev(g[j], r0)) - ev(g[j], ev(g[i], r0))) < mpf(10)**-300 for i in range(d) for j in range(d))
    print(name, '| degree', d, '| disc primes', sorted(fac), '| normal', normal, '| abelian', abelian, flush=True)
    if name.startswith('co') and not (normal and abelian): allok = False   # control: the heptagon field is abelian
print('FINAL ok' if allok else 'FINAL FAIL (control)')
