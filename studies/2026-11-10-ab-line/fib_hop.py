"""Aim 1, step 3 (DICTO 10 Nov 2026, option A): the Fibonacci line and its HOP. Line: Sturmian (1D cut-and-project) tilings with
s = (short tiles) / (long tiles); s = p/q rational gives the periodic word of period p + q (a crystal), s = 1/phi the Fibonacci
quasicrystal. Hop: the Fibonacci substitution L -> LS, S -> L, which sends slope s to h(s) = 1/(1+s); fixed point 1/phi.
Checks: (1) for every rational s = p/q with p + q <= 40, the hop of the canonical word at s is the canonical word at h(s) up to a
cyclic shift (exact strings); (2) the approximants: h carries F(n-1)/F(n) to F(n)/F(n+1); (3) Hurwitz/Markov: q^2 |x - p/q| over the
convergents tends to 1/sqrt5 = 0.4472 for x = 1/phi (the largest possible limit, Hurwitz 1891) and to 1/sqrt8 = 0.3536 for
x = 1/sqrt2 (the AB turning point; second in Markov's spectrum). usage: python3 fib_hop.py"""
from fractions import Fraction as Fr
from math import gcd, floor
import mpmath as mp
def word(p, q):            # canonical periodic Sturmian word with p S's and q L's per period (characteristic word)
    n = p + q; r = Fr(p, n)
    return ''.join('S' if floor((k + 2) * r) - floor((k + 1) * r) == 1 else 'L' for k in range(n))
def hop(w): return ''.join('LS' if c == 'L' else 'L' for c in w)
def rot_eq(a, b): return len(a) == len(b) and b in (a + a)
ok1 = True; n1 = 0
for n in range(2, 41):
    for p in range(1, n):
        q = n - p
        if gcd(p, q) != 1: continue
        w, w2 = word(p, q), word(q, p + q)          # h(p/q) = q/(p+q): q S's, p+q L's
        if not rot_eq(hop(w), w2): ok1 = False; print('mismatch at', p, q)
        n1 += 1
print(f'(1) hop of the crystal at s = p/q equals the crystal at 1/(1+s), up to a shift: {ok1} ({n1} slopes, p+q <= 40)')
F = [1, 1]
while len(F) < 14: F.append(F[-1] + F[-2])
chain = [Fr(F[i-1], F[i]) for i in range(1, 12)]
ok2 = all(1 / (1 + chain[i]) == chain[i+1] for i in range(len(chain) - 1))
print('(2) h carries Fibonacci approximants along:', ' -> '.join(str(c) for c in chain[:7]), '...', ok2)
mp.mp.dps = 40
def conv(x, k):
    a = []; y = x
    for _ in range(k): ai = int(mp.floor(y)); a.append(ai); y = 1 / (y - ai)
    h, h1, g, g1 = 1, 0, 0, 1; out = []
    for ai in a:
        h, h1 = ai * h + h1, h; g, g1 = ai * g + g1, g; out.append((h, g))
    return out
for name, x, lim in (('1/phi (Fibonacci, fixed point of the hop)', 2 / (1 + mp.sqrt(5)), 1 / mp.sqrt(5)),
                     ('1/sqrt2 (Ammann-Beenker, fixed point of the turn)', 1 / mp.sqrt(2), 1 / mp.sqrt(8))):
    vals = [q * q * abs(x - mp.mpf(p) / q) for p, q in conv(x, 26)[6:]]
    print(f'(3) {name}: q^2|x - p/q| over the convergents -> {mp.nstr(vals[-1], 8)} / {mp.nstr(vals[-2], 8)}; limit {mp.nstr(lim, 8)}')
ok3 = abs(vals[-1] - 1 / mp.sqrt(8)) < 1e-3
print('FINAL ok' if ok1 and ok2 and ok3 else 'FINAL FAIL')
