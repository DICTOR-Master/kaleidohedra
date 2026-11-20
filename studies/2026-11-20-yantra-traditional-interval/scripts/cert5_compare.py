"""Certificate 5: where named yantras sit against the window, exactly (PARI).
 (1) Kulaichev's yantra (equal great triangles, (b), (c), (d)): u = v = the root of f348 (#103 Theorem 10,
     inputs/kulaichev-minpoly-u.txt) near 0.7504385160222; isolated by polsturm in a rational interval. Its product is c_K = u^2.
 (2) The window ends: u* = the root of f180 (inputs/threshold-minpoly-u.txt) isolated as in certificate 2; c* = u*^2, c_lo from
     g90 (data/g90-c.txt, data/window-exact.json).
 (3) Comparisons of the isolating intervals: c* < c_K; c_lo < 2/phi^3 < c*; Rh345 (c = 9/16) and the sweep ends.
usage: python -u cert5_compare.py"""
import os, json
from fractions import Fraction as Fr
import cypari2
pari = cypari2.Pari(); pari.allocatemem(int(2e9))
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
f348 = pari(open(os.path.join(ROOT, 'inputs', 'kulaichev-minpoly-u.txt')).read().strip().replace('x', 'u'))
f180 = pari(open(os.path.join(ROOT, 'inputs', 'threshold-minpoly-u.txt')).read().strip())
g90 = pari(open(os.path.join(ROOT, 'data', 'g90-c.txt')).read().strip())
def ns(f, lo, hi, var): return int(pari.polsturm(f, [pari(f'{lo.numerator}/{lo.denominator}'), pari(f'{hi.numerator}/{hi.denominator}')]))
ok = True
irr = bool(pari.polisirreducible(f348)); print('f348 irreducible:', irr, '; degree', pari.poldegree(f348, 'u')); ok &= irr
uK = (Fr(7504385160222140, 10 ** 16), Fr(7504385160222141, 10 ** 16))
n = ns(f348, *uK, 'u'); print(f'f348 roots in [{float(uK[0])!r}, {float(uK[1])!r}]: {n}'); ok &= n == 1
W = json.load(open(os.path.join(ROOT, 'data', 'window-exact.json')))
def frac(s): a, b = s.split('/'); return Fr(int(a), 10 ** int(b.split('^')[1]))
clo = tuple(frac(x) for x in W['c_intervals'][0][:2]); cst = tuple(frac(x) for x in W['c_intervals'][1][:2])
for nm, iv in (('c_lo', clo), ('c*', cst)):
    n = ns(g90, *iv, 'c'); print(f'g90 roots in the interval of {nm} [{float(iv[0])!r}, {float(iv[1])!r}]: {n}'); ok &= n == 1
cK = (uK[0] ** 2, uK[1] ** 2)
print(f"Kulaichev's product c_K = u_K^2 in [{float(cK[0])!r}, {float(cK[1])!r}]; c* < c_K: {cst[1] < cK[0]}; c_K - c* > {float(cK[0] - cst[1]):.6e}")
ok &= cst[1] < cK[0]
# 2/phi^3 = 2 sqrt5 - 4: 2.2360679 < sqrt5 < 2.2360680
p3 = (2 * Fr(22360679, 10 ** 7) - 4, 2 * Fr(22360680, 10 ** 7) - 4)
assert p3[0] ** 1 > 0 and (Fr(22360679, 10 ** 7)) ** 2 < 5 < (Fr(22360680, 10 ** 7)) ** 2
print(f'c_lo < 2/phi^3 < c*: {clo[1] < p3[0] and p3[1] < cst[0]}; 2/phi^3 sits {float((p3[0] - clo[1]) / (cst[0] - clo[1])):.4f} of the way from c_lo to c*')
ok &= clo[1] < p3[0] and p3[1] < cst[0]
for nm, c in (('Rh345 (u = 3/4)', Fr(9, 16)), ('sweep start (u = 29/50)', Fr(29, 50) ** 2), ('sweep end (u = 751/1000)', Fr(751, 1000) ** 2), ('u = 7/10', Fr(49, 100))):
    where = 'below c_lo' if c < clo[0] else ('inside the window' if clo[1] < c < cst[0] else ('above c*' if c > cst[1] else '??'))
    print(f'{nm}: c = {c} = {float(c):.6f}, {where}'); ok &= where != '??'
print(f'Kulaichev lies inside the certified stretch above the window (c* < c_K < (751/1000)^2): {cst[1] < cK[0] and cK[1] < Fr(751, 1000) ** 2}')
ok &= cK[1] < Fr(751, 1000) ** 2
print('FINAL ok' if ok else 'FINAL FAIL')
