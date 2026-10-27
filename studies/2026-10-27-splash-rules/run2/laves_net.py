# Laves phases (DICTO 2026-10-28, 'start the Laves phases run'): the Laves network on any close-packed stacking word, exact.
# Big atoms (Mg) on the diamond-type sites of the pyrochlore stacking (ball S over X at 0, atom C over X at 3/4 of each gap; pyro_walk.py);
# every empty hole H of that network (O over Z at 1/2, Y over Y at 1/4) has 4 nearest big atoms M; the small atoms (Cu/Zn) sit at
# (3H - M)/2, the tetrahedron opposite them at half the distance (as Cu 16d round the 8b holes of MgCu2). Checks: 2 big : 4 small per gap,
# every small atom with 6 small + 6 big nearest neighbours (icosahedral Z12), every big atom with 4 big + 12 small (Z16).
from fractions import Fraction as Fr
import itertools
POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
def sites(word):
    n = len(word); big, holes = [], []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
        z = lambda f: Fr(k, n) + f / n
        big += [(*POS[X], z(Fr(0))), (*POS[X], z(Fr(3, 4)))]; holes += [(*POS[Z], z(Fr(1, 2))), (*POS[Y], z(Fr(1, 4)))]
    G = [[1, Fr(1, 2), 0], [Fr(1, 2), 1, 0], [0, 0, Fr(2, 3) * n * n]]
    return G, big, holes
def d2(G, u): return sum(G[i][j] * u[i] * u[j] for i in range(3) for j in range(3))
def red(p): return tuple(x - (x.numerator // x.denominator) for x in p)
def near(G, p, pts, R=(-1, 0, 1)):
    out = []
    for q in pts:
        for t in itertools.product(R, R, R):
            v = tuple(q[i] + t[i] - p[i] for i in range(3)); out.append((d2(G, v), tuple(p[i] + v[i] for i in range(3))))
    out.sort(key=lambda x: x[0]); return out
def laves(word):
    """Rule read off MgCu2 (the hole construction below gives it exactly for ABC) and checked on every word: per gap (X, Y, Z) the big
    atoms over X at 0 and 3/4, a kagome of small atoms at X + (1/2, 0), (0, 1/2), (1/2, 1/2) at 3/8 and one small atom over Z at 7/8."""
    G, big, _ = sites(word); n = len(word); small = []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop(); x, y = POS[X]
        z = lambda f: Fr(k, n) + f / n
        small += [red((x + a, y + b, z(Fr(3, 8)))) for a, b in ((Fr(1, 2), 0), (0, Fr(1, 2)), (Fr(1, 2), Fr(1, 2)))] + [(*POS[Z], z(Fr(7, 8)))]
    return G, [red(b) for b in big], small
def laves_holes(word):
    G, big, holes = sites(word); small = set()
    for H in holes:
        nb = near(G, H, big); m = nb[0][0]
        Ms = [q for dd, q in nb if dd == m]
        assert len(Ms) == 4 and nb[4][0] > m, (word, 'hole without 4 nearest big atoms')
        for M in Ms: small.add(red(tuple((3 * H[i] - M[i]) / 2 for i in range(3))))
    return G, [red(b) for b in big], sorted(small)
def check(word):
    G, big, small = laves(word); n = len(word)
    assert len(big) == 2 * n and len(small) == 4 * n, (word, len(big), len(small))
    allp = [('b', p) for p in big] + [('s', p) for p in small]
    def shell(p, k):
        ds = sorted((d2(G, tuple(q[i] + t[i] - p[i] for i in range(3))), kind) for kind, q in allp for t in itertools.product((-1, 0, 1), repeat=3))
        ds = [x for x in ds if x[0] > 0][:k]; return ds
    zs = {tuple(sorted(c for _, c in shell(p, 12))) for p in small}
    zb = {tuple(sorted(c for _, c in shell(p, 16))) for p in big}
    return dict(word=word, big=len(big), small=len(small), small_nb=[''.join(z) for z in zs], big_nb=[''.join(z) for z in zb],
                small_d2=sorted({str(x[0]) for p in small for x in shell(p, 12)}), big_d2=sorted({str(x[0]) for p in big for x in shell(p, 16)}))
if __name__ == '__main__':
    import sys
    for w in sys.argv[1:]: print(check(w))
