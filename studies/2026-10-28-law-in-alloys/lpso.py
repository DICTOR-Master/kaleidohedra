# Mg-Zn-Y LPSO phases (Egusa and Abe, arXiv 1106.4944): hcp Mg with a stacking fault every k layers (k = 5, 6, 7, 8 -> 10H, 18R,
# 14H, 24R), each fault making a local ABCA unit whose two middle layers are cubic (Jagodzinski c) and enriched in Zn and Y.
# Build each from its type string (cc + h^(k-2)) repeated until it closes, check with Jagodzinski's rule, give the hexagonality.
from fractions import Fraction as F
def letters(types):
    s = [1]
    for t in types[1:]: s.append(s[-1] if t == 'c' else -s[-1])
    ok = ((s[-1] == s[0]) == (types[0] == 'c')) and sum(s) % 3 == 0
    pos = [0]
    for x in s[:-1]: pos.append((pos[-1] + x) % 3)
    return ''.join('ABC'[p] for p in pos), ok
for k, name in ((5, '10H'), (6, '18R'), (7, '14H'), (8, '24R')):
    unit = 'cc' + 'h' * (k - 2)
    for rep in (1, 2, 3, 6):
        L, ok = letters(unit * rep)
        if ok: break
    n = len(L); t = ''.join('h' if L[i - 1] == L[(i + 1) % n] else 'c' for i in range(n))
    assert t == unit * rep
    print(f'{name}: fault every {k} layers, period {n} layers {L}, types {t}, hexagonality {F(t.count("h"), n)} = {t.count("h")/n:.3f}')
