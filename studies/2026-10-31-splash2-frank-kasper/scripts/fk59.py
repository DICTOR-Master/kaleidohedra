# Frank-Kasper 1959 layered family (kagome slabs), read off AFLOW C14, C36, Zr4Al3 (Z) and Fe7W6 (mu) and COD 9R Laves:
# a word t_1..t_n over {0, +, -}; kagome nets B3 with hexagons centred at close-packed letters a_i, a_{i+1} = a_i + t_i (mod 3).
#   t_i = +/- (Laves slab, height sqrt(2/3)): caps at a_i (3/8) and a_{i+1} (5/8), one atom at the third letter (1/2);
#   t_i = 0   (Z slab, height 1):             caps at a_i (1/4, 3/4), two atoms at the two other letters (1/2).
# The cell repeats the word until the letters close (sum t = 0 mod 3). Ideal geometry, kagome lattice a = 1.
import numpy as np
P = [(0.0, 0.0), (1 / 3, 2 / 3), (2 / 3, 1 / 3)]
STEP = {'0': 0, '+': 1, '-': 2}
def closed(word):
    s = sum(STEP[c] for c in word) % 3
    return word if s == 0 else word * 3
def build(word):
    w = closed(word); a = 0; z = 0.0; pts = []
    H = {'0': 1.0, '+': np.sqrt(2 / 3), '-': np.sqrt(2 / 3)}
    for t in w:
        b = (a + STEP[t]) % 3; h = H[t]; ax, ay = P[a]
        for d in ((.5, 0), (0, .5), (.5, .5)): pts.append((ax + d[0], ay + d[1], z))
        if t == '0':
            o = [k for k in range(3) if k != a]
            pts += [(ax, ay, z + h / 4), (ax, ay, z + 3 * h / 4), (*P[o[0]], z + h / 2), (*P[o[1]], z + h / 2)]
        else:
            m = 3 - a - b
            pts += [(ax, ay, z + 3 * h / 8), (*P[m], z + h / 2), (*P[b], z + 5 * h / 8)]
        a = b; z += h
    L = np.array([[1.0, 0, 0], [-.5, np.sqrt(3) / 2, 0], [0, 0, z]])
    frac = np.array([[p[0] % 1, p[1] % 1, (p[2] / z) % 1] for p in pts])
    return L, frac, w
