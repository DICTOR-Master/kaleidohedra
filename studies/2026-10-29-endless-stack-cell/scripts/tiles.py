# Endless Stack Cell (DICTO's idea, 2026-10-29). The layer tile of layer L: the top half of gap L-1's octahedral piece, the
# tetrahedral pieces at heights L-1/4 and L+1/4 (each takes layer L's type, #57), and the bottom half of gap L's octahedral piece.
# Checks, exact (census engine of #53/#57, rational arithmetic), over many periodic stackings covering all 32 five-layer contexts
# (types of layers L-2..L+2) and 10 sample weights λ across the walk:
#  1. flat: every tetrahedral piece of the tile lies between the cut planes z = L-1/2 and z = L+1/2 (in layer units);
#  2. one tile per type: the whole tile (all four pieces at once) is carried onto the tile of the pure stacking of layer L's type
#     (ABC for c, AB for h) by ONE motion: a symmetry of the triangular lattice about layer L's ball, z kept (also tried: z -> -z);
#  3. the joint: the section of gap L's octahedral piece on the plane z = L+1/2 (shared by tiles L and L+1) is the same for all
#     contexts at that λ, up to the same lattice symmetries.
import itertools, sys
from fractions import Fraction as Fr
from engine import Net, Cell, aff_eval, gdot, vsub
from stackings import net_for, POS

def build(word):
    s = net_for(word); return Net(word, s['G'], s['T'], s['motif'], s['w']), s

def types(word):
    n = len(word); return ['h' if word[(k - 1) % n] == word[(k + 1) % n] else 'c' for k in range(n)]

def corners(c, lam): return [tuple(aff_eval(p['P'][r], (lam,)) for r in range(3)) for p in c.corners]

def edges(c):
    F = set(c.faces()); return [(a, b) for a, b in itertools.combinations(range(len(c.corners)), 2)
                                if len(c.corners[a]['on'] & c.corners[b]['on'] & F) >= 2]

def half(c, X, zc, up):
    keep = [x for x in X if (x[2] >= zc if up else x[2] <= zc)]
    for a, b in edges(c):
        za, zb = X[a][2], X[b][2]
        if (za - zc) * (zb - zc) < 0:
            t = (zc - za) / (zb - za); keep.append(tuple(X[a][r] + t * (X[b][r] - X[a][r]) for r in range(3)))
    return sorted(set(keep))

def section(c, X, zc):
    return sorted(set([x for x in X if x[2] == zc] + [p for p in half(c, X, zc, True) if p[2] == zc]))

# the 12 symmetries of the triangular lattice (metric [[1,1/2],[1/2,1]]) as integer matrices on (u, v)
SYM = [M for M in itertools.product((-1, 0, 1), repeat=4)
       if (lambda a, b, c, d: a * d - b * c in (1, -1) and
           (a * a + a * c + c * c, 2 * a * b + a * d + b * c + 2 * c * d, b * b + b * d + d * d) == (1, 1, 1))(*M)]
assert len(SYM) == 12, len(SYM)

def tile(word, L, lam):
    """Pieces of layer L's tile, in coordinates centred on layer L's ball, z in layer units. Returns (pieces, tet z-ranges)."""
    net, spec = build(word); n = len(word); m = spec['motif']
    ball = (*POS[word[L]], Fr(L))
    def loc(p): return (p[0] - ball[0], p[1] - ball[1], p[2] * n - ball[2])
    g0, g1 = (L - 1) % n, L % n
    want = [(3 * g0, 'oct', True), (3 * g0 + 1, 'tet', None), (3 * g1 + 2, 'tet', None), (3 * g1, 'oct', False)]
    pieces, tz = [], []
    for i, k, up in want:
        c = Cell(net, i, (lam,), Fr(12))
        if c.empty: continue
        X = corners(c, lam); site = m[i][1]
        sh = round((site[2] * n - L) / n) * n               # periodic copy of the site nearest layer L
        X = [(x[0], x[1], x[2] - Fr(sh, n)) for x in X]; site = (site[0], site[1], site[2] - Fr(sh, n))
        if k == 'oct':
            P = half(c, X, site[2], up); joint = section(c, X, site[2]) if up is False else None
        else:
            P = X; joint = None
        Pl = [loc(p) for p in P]; sl = loc(site)
        if k == 'tet': tz.append((min(p[2] for p in Pl), max(p[2] for p in Pl)))
        pieces.append((k, up, sl, Pl, [loc(p) for p in joint] if joint else None))
    return pieces, tz

def image(pieces, M, flip):
    a, b, c, d = M; out = []
    for k, up, s, P, J in pieces:
        f = lambda p: (a * p[0] + b * p[1], c * p[0] + d * p[1], -p[2] if flip else p[2])
        s2 = f(s); off = (s2[0] - s2[0] % 1, s2[1] - s2[1] % 1, 0)   # lattice translation bringing the site into [0,1)
        rel = frozenset(vsub(f(p), off) for p in P)
        out.append((k, (not up) if (flip and up is not None) else up, (s2[0] % 1, s2[1] % 1, s2[2]), rel))
    return frozenset(out)

def canon_joint(J):
    if not J: return None
    best = None
    for M in SYM:
        a, b, c, d = M; Q = [(a * p[0] + b * p[1], c * p[0] + d * p[1]) for p in J]
        o = min(Q); key = tuple(sorted((x - o[0], y - o[1]) for x, y in Q))
        best = key if best is None or key < best else best
    return best

if __name__ == '__main__':
    # words covering every five-layer context
    words, ctx = [], {}
    for n in range(2, 11):
        for w in itertools.product('ABC', repeat=n):
            if w[0] != 'A' or any(w[i] == w[(i + 1) % n] for i in range(n)): continue
            w = ''.join(w); T = types(w); new = False
            for L in range(n):
                key = ''.join(T[(L + j) % n] for j in range(-2, 3))
                if key not in ctx: ctx[key] = (w, L); new = True
        if len(ctx) == 32: break
    print(f'{len(ctx)} five-layer contexts covered', flush=True)
    lams = [Fr(-7, 16), Fr(-5, 12), Fr(-1, 4), Fr(-3, 16), Fr(-1, 16), Fr(1, 300), Fr(1, 10), Fr(1, 4), Fr(1, 3), Fr(5, 16)]
    lams = [Fr(x) for x in sys.argv[1:]] or lams
    tot = {'flat': [0, 0], 'one': [0, 0], 'flip_only': 0}
    for lam in lams:
        REF = {'c': tile('ABC', 1, lam)[0], 'h': tile('AB', 0, lam)[0]}
        RIMG = {t: image(REF[t], (1, 0, 0, 1), False) for t in 'ch'}
        joints = set(); notflat = []
        for key, (w, L) in sorted(ctx.items()):
            P, tz = tile(w, L, lam); t = key[2]
            flat = all(lo >= Fr(-1, 2) and hi <= Fr(1, 2) for lo, hi in tz)
            tot['flat'][0 if flat else 1] += 1
            if not flat: notflat.append((key, [(str(a), str(b)) for a, b in tz]))
            one = any(image(P, M, False) == RIMG[t] for M in SYM)
            flip = (not one) and any(image(P, M, True) == RIMG[t] for M in SYM)
            tot['one'][0 if one else 1] += 1; tot['flip_only'] += flip
            if not one: print(f'  λ={lam} context {key} ({w}, layer {L}): NOT one motion' + (' (matches with z -> -z)' if flip else ''), flush=True)
            J = [p[4] for p in P if p[4]]
            if J: joints.add(canon_joint(J[0]))
        print(f'λ={lam}: flat {32 - len(notflat)}/32; joint sections distinct: {len(joints)}', flush=True)
        for x in notflat[:4]: print('   not flat:', x, flush=True)
    print(f"TOTAL flat {tot['flat'][0]} yes / {tot['flat'][1]} no; one-motion tile {tot['one'][0]} yes / {tot['one'][1]} no "
          f"(of the no: {tot['flip_only']} match after z -> -z)")
