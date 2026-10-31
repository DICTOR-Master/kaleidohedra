# Splash Rules II: perovskite polytypes (DICTO 2026-10-31). Exact model of ABX3 hexagonal perovskites on every stacking.
# Ideal geometry: X and A are equal close-packed balls of diameter 1; AX3 layers (A on a 2x2 sublattice of each layer);
# B in the octahedral holes made of X only. Integer coordinates: lateral (x, y) in units of 1/3 of the triangular-lattice
# basis, height z in units of 1/4 of the layer spacing d (d^2 = 2/3). Then 72 * r^2 = 8(x^2 + xy + y^2) + 3 z^2, an integer:
# every distance below is exact.
# Usage: python3 perov.py <out.json> <word> [<word> ...]   (word = c/h word of one period, cyclic)
import sys, json, itertools
from fractions import Fraction as Fr
from collections import Counter

def n72(dx, dy, dz): return 8 * (dx * dx + dx * dy + dy * dy) + 3 * dz * dz
IMG = [(6 * a, 6 * b) for a in range(-2, 3) for b in range(-2, 3)]   # lateral period 2 cells = 6 units

def letters_from_types(w):
    """c/h word (cyclic; w[k] = type of layer k) -> ABC letters (0,1,2) of the shortest closed period, L_0 = 0, L_1 = 1."""
    n = len(w); L = [0, 1]
    for k in range(1, 12 * n + 2):
        L.append(L[k - 1] if w[k % n] == 'h' else 3 - L[k - 1] - L[k])
        if (k + 1) % n == 0 and L[k + 1] == 0 and len(L) > k + 1:
            pass
    for N in range(n, 6 * n + 1, n):
        if L[N] == 0 and L[N + 1] == 1: return L[:N]
    raise RuntimeError('no closure')

def site_species(k, L, o, x, y):
    """species of the close-packed site at lateral (x, y) (1/3 units) in layer k, or None if not a site."""
    s = L[k]
    if (x - s) % 3 or (y - s) % 3: return None
    i, j = (x - s) // 3, (y - s) // 3
    return 'A' if (i % 2, j % 2) == o[k] else 'X'


def tri_sites(px, py, s):
    """the 3 sites of letter s at lateral distance^2 1/3 from point (px, py) (1/3 units)."""
    out = []
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if 8 * (dx * dx + dx * dy + dy * dy) == 24 and (px + dx - s) % 3 == 0 and (py + dy - s) % 3 == 0:
                out.append((px + dx, py + dy))
    assert len(out) == 3, (px, py, s, out)
    return out

def build(w):
    L = letters_from_types(w)
    nL = len(L)
    # A cosets: o_0 = (0,0); o_{k+1} forced (B hole of gap k must avoid A of both layers). Close the period (maybe doubled).
    o = [(0, 0)]
    def b_hole(k, ok, ok1, Lk, Lk1):
        t = 3 - Lk - Lk1; good = []
        for a, b in itertools.product(range(2), repeat=2):
            px, py = 3 * a + t, 3 * b + t
            def sp(s, oo, x, y):
                i, j = (x - s) // 3, (y - s) // 3
                return 'A' if (i % 2, j % 2) == oo else 'X'
            lo = [sp(Lk, ok, x, y) for x, y in tri_sites(px, py, Lk)]
            hi = [sp(Lk1, ok1, x, y) for x, y in tri_sites(px, py, Lk1)]
            if 'A' not in lo and 'A' not in hi: good.append((px % 6, py % 6))
        return good
    Lf, of = [], []
    k = 0
    while True:
        Lk, Lk1 = L[k % nL], L[(k + 1) % nL]
        cand = [oo for oo in itertools.product(range(2), repeat=2) if len(b_hole(k, o[-1], oo, Lk, Lk1)) == 1]
        assert len(cand) == 1, cand
        # check no choice gives more than one B hole and that the forced one is unique
        assert all(len(b_hole(k, o[-1], oo, Lk, Lk1)) <= 1 for oo in itertools.product(range(2), repeat=2))
        o.append(cand[0]); k += 1
        if k % nL == 0 and o[k] == o[0]: break
        assert k <= 4 * nL
    N = k
    L = [L[i % nL] for i in range(N)]; o = o[:N]
    return L, o, N, nL

def ltype(L, k):
    N = len(L); return 'h' if L[(k - 1) % N] == L[(k + 1) % N] else 'c'

def analyse(w):
    L, o, N, nL = build(w)
    T = [ltype(L, k) for k in range(N)]
    # consistency with the word
    n = len(w); assert all(T[k] == w[k % n] for k in range(N)), (w, T)
    # sites: layer k, z = 4k
    sites = []                                     # (kind, k, x, y, z)
    for k in range(N):
        s = L[k]
        for a, b in itertools.product(range(2), repeat=2):
            x, y = 3 * a + s, 3 * b + s
            sites.append(('A' if (a, b) == o[k] else 'X', k, x % 6, y % 6, 4 * k))
    def _spec(k, x, y):
        k %= N; s = L[k]
        i, j = (x - s) // 3, (y - s) // 3
        return 'A' if (i % 2, j % 2) == o[k] else 'X'
    B, octE, tet = [], [], []
    for k in range(N):
        p, q = L[k], L[(k + 1) % N]; t = 3 - p - q
        for a, b in itertools.product(range(2), repeat=2):
            px, py = 3 * a + t, 3 * b + t
            lo = sorted(_spec(k, x, y) for x, y in tri_sites(px, py, p))
            hi = sorted(_spec(k + 1, x, y) for x, y in tri_sites(px, py, q))
            nA = (lo.count('A'), hi.count('A'))
            if nA == (0, 0): B.append((k, px % 6, py % 6, 4 * k + 2, frozenset((X - px, Y - py, -2) for X, Y in tri_sites(px, py, p)) | frozenset((X - px, Y - py, 2) for X, Y in tri_sites(px, py, q))))
            else:
                Al = [(X, Y, -2) for X, Y in tri_sites(px, py, p) if _spec(k, X, Y) == 'A']
                Ah = [(X, Y, 2) for X, Y in tri_sites(px, py, q) if _spec(k + 1, X, Y) == 'A']
                aa = sorted(n72(u[0] - w_[0], u[1] - w_[1], u[2] - w_[2]) for u in Al for w_ in Ah)
                octE.append((k, nA, aa))
        # tetrahedral holes: apex on a layer-k site, base in layer k+1 ('up'); apex on a layer-(k+1) site, base in k ('down')
        for a, b in itertools.product(range(2), repeat=2):
            x, y = 3 * a + p, 3 * b + p
            base = [_spec(k + 1, X, Y) for X, Y in tri_sites(x, y, q)]
            tet.append((k, 'up', _spec(k, x, y), base.count('A')))
            x, y = 3 * a + q, 3 * b + q
            base = [_spec(k, X, Y) for X, Y in tri_sites(x, y, p)]
            tet.append((k, 'down', _spec(k + 1, x, y), base.count('A')))
    assert len(B) == N
    Bk = {b[0]: b for b in B}
    # neighbour helper with periodic images (vertical period 4N)
    def disps(p1, p2, maxr):
        """all displacement vectors p2 - p1 over periodic images with 72 r^2 <= maxr"""
        dz0 = (p2[2] - p1[2]) % (4 * N); out = []
        for j in range(-3, 3):
            dzz = dz0 + 4 * N * j
            if 3 * dzz * dzz > maxr: continue
            for ix, iy in IMG:
                v = ((p2[0] - p1[0]) % 6 + ix, (p2[1] - p1[1]) % 6 + iy, dzz)
                if n72(*v) <= maxr: out.append(v)
        return out
    RB = 864                                       # B-B shells up to r^2 = 12
    def near(k1, k2, lim): d = (k2 - k1) % N; return min(d, N - d) <= lim
    perB = []
    for b in B:
        k = b[0]; V1 = b[4]
        shells = Counter(); share = Counter()
        for b2 in B:
            if not near(k, b2[0], 5): continue
            for v in disps(b[1:4], b2[1:4], RB):
                r = n72(*v)
                if r == 0: continue
                shells[r] += 1
                sh = len(V1 & frozenset((x + v[0], y + v[1], z + v[2]) for x, y, z in b2[4]))
                if sh: share[sh] += 1
        ash = Counter()                            # B-A shells up to r^2 = 2 (144)
        for s_ in sites:
            if s_[0] != 'A' or not near(k, s_[1], 2): continue
            for v in disps(b[1:4], s_[2:5], 144): ash[n72(*v)] += 1
        perB.append(dict(k=k, shells=dict(shells), share=dict(share), A=dict(ash)))
    perX, perA = [], []
    for s_ in sites:
        k = s_[1]; pos = s_[2:5]
        nb = Counter()
        for s2 in sites:
            if not near(k, s2[1], 1): continue
            for v in disps(pos, s2[2:5], 72):
                if n72(*v) == 72: nb[(s2[0], 'up' if v[2] > 0 else 'down' if v[2] < 0 else 'in')] += 1
        bn = []
        for b in B:
            if not near(k, b[0], 1): continue
            for v in disps(pos, b[1:4], 36): bn.append((v, b))      # B-X distance^2 = 1/2
        nA = sum(c for (sp, _), c in nb.items() if sp == 'A'); nX = sum(c for (sp, _), c in nb.items() if sp == 'X')
        if s_[0] == 'X':
            assert len(bn) == 2, bn
            ((x1, y1, z1), b1), ((x2, y2, z2), b2) = bn
            dot = Fr(8 * (2 * x1 * x2 + x1 * y2 + x2 * y1 + 2 * y1 * y2) + 6 * z1 * z2, 2 * 36)   # cos of B-X-B (|XB|^2 = 1/2)
            d = (x2 - x1, y2 - y1, z2 - z1)
            sh = len(b1[4] & frozenset((x + d[0], y + d[1], z + d[2]) for x, y, z in b2[4]))
            perX.append(dict(k=k, nA=nA, nX=nX, Aupdown=[nb[('A', 'in')], nb[('A', 'up')], nb[('A', 'down')]], nB=2, cosBXB=str(dot), nface=int(sh == 3), share=sh))
        else:
            assert nX == 12 and nA == 0
            perA.append(dict(k=k, nA=nA, nX=nX, cage='anticubo' if T[k] == 'h' else 'cubo', nB=len(bn)))
    # face-sharing clusters (chains of B joined across h layers)
    seen = set(); clusters = []
    if all(t == 'h' for t in T): clusters = None
    else:
        start = [k for k in range(N) if T[k] == 'c'][0]
        cur = 1
        for j in range(1, N + 1):
            k = (start + j) % N                         # layer k joins gap k-1 and gap k if h
            if T[k] == 'h': cur += 1
            else: clusters.append(cur); cur = 1
    return dict(word=w, N=N, nL=nL, letters=''.join('ABC'[x] for x in L), types=''.join(T), cosets=[list(c) for c in o],
                perB=perB, perX=perX, perA=perA, octE=[[e[0], list(e[1]), e[2]] for e in octE],
                tet=[list(t) for t in tet], clusters=clusters)

if __name__ == '__main__':
    out = sys.argv[1]; res = [analyse(w) for w in sys.argv[2:]]
    json.dump(res, open(out, 'w'))
    for r in res: print(r['word'], r['N'], r['nL'], r['letters'][:24], r['clusters'][:8] if r['clusters'] else r['clusters'])
