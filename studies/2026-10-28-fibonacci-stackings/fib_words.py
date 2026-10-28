# Fibonacci stackings (DICTO 10-28): layer types c/h in the Fibonacci order (substitution c -> ch, h -> c), turned into
# close-packed letter sequences. A layer is h when its two neighbouring steps differ (Jagodzinski); so steps follow from types:
# s_{k} = s_{k-1} if layer k is c, -s_{k-1} if h. A periodic stacking needs an even number of h (signs close) and the steps'
# sum = 0 mod 3 (positions close). Periodic approximants: the Fibonacci words of Fibonacci lengths, doubled or tripled if needed.
from fractions import Fraction as F
def fib(n):
    w = 'c'
    while len(w) < n: w = ''.join('ch' if x == 'c' else 'c' for x in w)
    return w
def letters(types):
    s = [1]
    for t in types[1:]: s.append(s[-1] if t == 'c' else -s[-1])
    # layer k sits between step k-1 and step k (cyclically): check closure of the type of layer 0
    ok_sign = (s[-1] == s[0]) == (types[0] == 'c')
    pos = [0]
    for x in s[:-1]: pos.append((pos[-1] + x) % 3)
    ok_pos = (pos[-1] + s[-1]) % 3 == 0
    return ''.join('ABC'[p] for p in pos), ok_sign and ok_pos
out = {}
for n in (5, 8, 13, 21):
    w = fib(n)[:n]
    for rep in (1, 2, 3, 6):
        L, ok = letters(w * rep)
        if ok:
            # recheck with Jagodzinski on the letters, cyclically
            m = len(L); t = ''.join('h' if L[k - 1] == L[(k + 1) % m] else 'c' for k in range(m))
            assert t == w * rep, (t, w * rep)
            out[n] = (w, rep, L)
            print(f'Fibonacci {n:2d}: types {w} x{rep} -> {L} ({len(L)} layers), hexagonality {F(t.count("h"), m)}')
            break
    else: print(n, 'no closure up to x6')
import math
phi = (1 + 5 ** .5) / 2
print('limit hexagonality 1/phi^2 =', 1 / phi ** 2)
