# Exact fill check for chosen connected tiles (connect.py): every stacking word of length 2..6 (A first, no letter twice in a
# row, cyclically), weight λ, c-translates tc and h-translates th (one integer (u, v) per piece of the reference tile).
#  1. each layer L: the engine's pieces tile(word, L, λ) are carried onto the reference tile of L's type by one lattice symmetry
#     M (#75); the chosen piece r of the reference is pulled back by M and must be an in-layer lattice translate of exactly one
#     engine piece of layer L (so the layer's set of copies is unchanged); the chosen layer tile is congruent to the reference
#     choice by construction (one motion), so c sits on c, c on h, h on c, h on h exactly as the stacking needs;
#  2. geometry, independent of the #75 census: every chosen tile has volume one layer cell (6 x volume = 6 in lattice units),
#     and every piece of the tile of layer L (copy (0,0)) has interior disjoint from every piece of every other tile copy
#     (layers L-2..L+2 with the period, in-layer copies -3..3): a separating plane is found exactly (a facet plane of either
#     piece, else a plane through an edge of each). Disjoint tiles of one cell's volume per cell = a tiling of space.
# Usage: python3 verify.py <lam> '<tc json>' '<th json>' [RoH|W]
import itertools, json, sys
from fractions import Fraction as Fr
from tiles import tile, types, SYM, image
from stackings import POS
import exactfaces as E

def words(nmax=6):
    out = []
    for n in range(2, nmax + 1):
        for w in itertools.product('ABC', repeat=n):
            if w[0] == 'A' and all(w[i] != w[(i + 1) % n] for i in range(n)): out.append(''.join(w))
    return out

def lin(M, t): a, b, c, d = M; return (a * t[0] + b * t[1], c * t[0] + d * t[1])
def inv(M):
    a, b, c, d = M; det = a * d - b * c; return (d * det, -b * det, -c * det, a * det)
def f(M, p): q = lin(M, p); return (q[0], q[1], p[2])

def edges_of(Fs):
    es = set()
    for n, c, pts in Fs:
        Q = sorted(pts)
        for a, b in itertools.combinations(Q, 2):
            # a-b is an edge if it lies on two facets
            if sum(1 for n2, c2, p2 in Fs if a in p2 and b in p2) >= 2: es.add((a, b))
    return es

def separated(A, FA, B, FB):
    for Fs in (FA, FB):
        for n, c, pts in Fs:
            sa = [E.dot(n, p) - c for p in A]; sb = [E.dot(n, p) - c for p in B]
            if (max(sa) <= 0 and min(sb) >= 0) or (min(sa) >= 0 and max(sb) <= 0): return True
    for a1, a2 in edges_of(FA):
        for b1, b2 in edges_of(FB):
            n = E.cross(E.sub(a2, a1), E.sub(b2, b1))
            if n == (0, 0, 0): continue
            c = E.dot(n, a1); sa = [E.dot(n, p) - c for p in A]; sb = [E.dot(n, p) - c for p in B]
            if (max(sa) <= 0 and min(sb) >= 0) or (min(sa) >= 0 and max(sb) <= 0): return True
    return False

def pieces_W(w, L, lam):
    """split W of alt_split.py (λ = -1/8 only): layer L's two tetrahedra + the whole octahedron of the gap above"""
    from alt_split import whole, build
    T = [p for p in tile(w, L, lam)[0] if p[0] == 'tet']; n = len(w); net, spec = build(w); m = spec['motif']; i = 3 * (L % n)
    site = m[i][1]; sh = round((site[2] * n - L) / n) * n; ball = (*POS[w[L]], Fr(L))
    s = (site[0] - ball[0], site[1] - ball[1], (site[2] - Fr(sh, n)) * n - ball[2])
    return T + [('oct', None, s, whole(w, L, i), None)]

def main(lam, TR, mode='RoH'):
    get = (lambda w, L: tile(w, L, lam)[0]) if mode == 'RoH' else (lambda w, L: pieces_W(w, L, lam))
    REF = {'c': get('ABC', 1), 'h': get('AB', 0)}
    RIMG = {t: image(REF[t], (1, 0, 0, 1), False) for t in 'ch'}
    stats = dict(words=0, layers=0, pairs=0, fail=[])
    for w in words():
        n = len(w); T = types(w); layer_tiles = []
        for L in range(n):
            P = get(w, L); t = T[L]
            M = next(M for M in SYM if image(P, M, False) == RIMG[t]); Mi = inv(M)
            ref = REF[t]; used = []; chosen = []
            for k, up, s, X, J in P:
                Y = sorted(f(M, p) for p in X); hit = None
                for r, (k2, up2, s2, X2, J2) in enumerate(ref):
                    R = sorted(X2); g = E.sub(R[0], Y[0])
                    if g[2] == 0 and g[0].denominator == 1 and g[1].denominator == 1 and sorted(E.add(p, g) for p in Y) == R:
                        hit = (r, (g[0], g[1])); break
                assert hit, (w, L, 'piece not matched')
                r, g = hit; used.append(r); sh = lin(Mi, (TR[t][r][0] + g[0], TR[t][r][1] + g[1]))
                ball = (*POS[w[L]], Fr(L))
                chosen.append([(p[0] + sh[0] + ball[0], p[1] + sh[1] + ball[1], p[2] + ball[2]) for p in X])
            assert sorted(used) == list(range(len(ref))), (w, L, used)
            v6 = sum(E.piece_volume6(X) for X in chosen); assert v6 == 6, (w, L, v6)
            layer_tiles.append(chosen); stats['layers'] += 1
        # pairwise interiors
        FT = [[E.facets(X) for X in tl] for tl in layer_tiles]
        for L in range(n):
            for dl in range(-2, 3):
                L2 = L + dl; per, L2m = divmod(L2, n)
                for a, b in itertools.product(range(-3, 4), repeat=2):
                    if dl == 0 and (a, b) == (0, 0): continue
                    if (dl % n == 0) and per == 0 and (a, b) == (0, 0): continue
                    for i, A in enumerate(layer_tiles[L]):
                        for j, B0 in enumerate(layer_tiles[L2m]):
                            B = [(p[0] + a, p[1] + b, p[2] + per * n) for p in B0]
                            if any(min(p[r] for p in B) >= max(p[r] for p in A) or max(p[r] for p in B) <= min(p[r] for p in A) for r in range(3)): continue
                            FB = [(m, c + m[0] * a + m[1] * b + m[2] * per * n, [(p[0] + a, p[1] + b, p[2] + per * n) for p in pts]) for m, c, pts in FT[L2m][j]]
                            stats['pairs'] += 1
                            if not separated(A, FT[L][i], B, FB): stats['fail'].append((w, L, i, L2, j, a, b))
        stats['words'] += 1
    return stats

if __name__ == '__main__':
    lam = Fr(sys.argv[1]); TR = {'c': json.loads(sys.argv[2]), 'h': json.loads(sys.argv[3])}
    mode = sys.argv[4] if len(sys.argv) > 4 else 'RoH'
    s = main(lam, TR, mode)
    print(json.dumps(dict(lam=str(lam), split=mode, tc=TR['c'], th=TR['h'], words=s['words'], layers=s['layers'], pairs_tested=s['pairs'],
                          overlaps=len(s['fail']), first=[list(map(str, x)) for x in s['fail'][:5]]), indent=None), flush=True)
