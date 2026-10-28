# Endless Stack Cell: stretch-by-stretch proof of the two-tile statement, and the exact λ where the tiles stop being flat.
# For one five-layer context (argv[1], e.g. 'chchh'): all breakpoints of the tile's four cells in its word and of the pure tile of
# the same type (ABC or AB) are found exactly along -11/24 <= λ <= 3/8 (engine: Cell.interval). On each open sub-interval the
# combinatorics of every cell is fixed, corners are affine in λ and the cut points of the octahedral halves are rational functions
# of λ; the tile is mapped by the lattice symmetry found at the mid-point and compared with the pure tile SYMBOLICALLY (sympy,
# identical rational functions), so equality holds on the whole sub-interval. At each breakpoint the tiles are compared exactly.
# Flatness: on each sub-interval, the tetrahedral corners' heights (affine) are compared with the cut planes ±1/2 exactly.
import sys, itertools
from fractions import Fraction as Fr
import sympy as sp
from engine import Cell, aff_eval, LAM
from tiles import build, types, corners, edges, image, SYM, tile, ctx_words
from stackings import POS

LO, HI = Fr(-11, 24), Fr(3, 8)

def cells_of(word, L):
    net, spec = build(word); n = len(word); g0, g1 = (L - 1) % n, L % n
    return net, spec, n, [(3 * g0, 'oct', True), (3 * g0 + 1, 'tet', None), (3 * g1 + 2, 'tet', None), (3 * g1, 'oct', False)]

def breakpoints(word, L):
    net, spec, n, want = cells_of(word, L); B = set()
    for i, k, up in want:
        l = LO
        while l < HI:
            s = l + Fr(1, 7919)
            c = Cell(net, i, (s,), Fr(12))
            if c.empty: iv = (None, None)
            else: iv = c.interval()
            if iv[0] == 'breakpoint':
                B.add(s); l = s; continue
            hi = iv[1] if iv[1] is not None and iv[1] < HI else HI
            B.add(hi); l = hi
    return B

def sym_tile(word, L, lam):
    """Tile at a generic λ of a sub-interval, corners as sympy rational functions of LAM, centred on layer L's ball."""
    net, spec, n, want = cells_of(word, L); m = spec['motif']; ball = (*POS[word[L]], Fr(L)); out = []; tz = []
    for i, k, up in want:
        c = Cell(net, i, (lam,), Fr(12))
        if c.empty: continue
        site = m[i][1]; sh = round((site[2] * n - L) / n) * n
        X = [tuple(sp.Rational(p['P'][r][0]) + sp.Rational(p['P'][r][1]) * LAM for r in range(3)) for p in c.corners]
        X = [(x[0] - sp.Rational(ball[0]), x[1] - sp.Rational(ball[1]), x[2] * n - sh - L) for x in X]
        s = (site[0] - ball[0], site[1] - ball[1], site[2] * n - sh - L)
        Xn = [tuple(aff_eval(p['P'][r], (lam,)) for r in range(3)) for p in c.corners]
        zc = s[2]
        if k == 'oct':
            keep = [X[a] for a in range(len(X)) if ((Xn[a][2] * n - sh - L) >= zc if up else (Xn[a][2] * n - sh - L) <= zc)]
            for a, b in edges(c):
                za, zb = Xn[a][2] * n - sh - L, Xn[b][2] * n - sh - L
                if (za - zc) * (zb - zc) < 0:
                    t = (zc - X[a][2]) / (X[b][2] - X[a][2]); keep.append(tuple(sp.cancel(X[a][r] + t * (X[b][r] - X[a][r])) for r in range(3)))
            P = keep
        else:
            P = X; tz += [x[2] for x in X]
        out.append((k, up, s, [tuple(sp.cancel(v) for v in p) for p in P]))
    return out, tz

def sym_image(pieces, M):
    a, b, c, d = M; out = []
    for k, up, s, P in pieces:
        s2 = (a * s[0] + b * s[1], c * s[0] + d * s[1], s[2]); off = (s2[0] - s2[0] % 1, s2[1] - s2[1] % 1)
        rel = frozenset(tuple(sp.cancel(v) for v in (a * p[0] + b * p[1] - off[0], c * p[0] + d * p[1] - off[1], p[2])) for p in P)
        out.append((k, up, (s2[0] % 1, s2[1] % 1, s2[2]), rel))
    return frozenset(out)

if __name__ == '__main__':
    key = sys.argv[1]; w, L = ctx_words()[key]; t = key[2]; pw, pL = ('ABC', 1) if t == 'c' else ('AB', 0)
    B = sorted(breakpoints(w, L) | breakpoints(pw, pL) | {LO, HI})
    sub = ok = 0; bad = []; cross = []
    for a, b in zip(B, B[1:]):
        lm = (a + b) / 2; sub += 1
        P, _ = tile(w, L, lm); R, _ = tile(pw, pL, lm)
        Ms = [M for M in SYM if image(P, M, False) == image(R, (1, 0, 0, 1), False)]
        SP, tz = sym_tile(w, L, lm); SR, _ = sym_tile(pw, pL, lm)
        good = any(sym_image(SP, M) == sym_image(SR, (1, 0, 0, 1)) for M in Ms)
        ok += good
        if not good: bad.append(f'({a}, {b})')
        for z in tz:                       # where a tetrahedral corner meets a cut plane inside this sub-interval
            for side in (sp.Rational(1, 2), sp.Rational(-1, 2)):
                for r in sp.solve(sp.Eq(z, side), LAM):
                    if a < Fr(str(r)) < b: cross.append(str(r))
        zmax = max(abs(z.subs(LAM, sp.Rational(lm))) for z in tz) if tz else 0
        if zmax > sp.Rational(1, 2): cross.append(f'over in ({a}, {b})')
    nb = 0
    for l in B:                            # the breakpoints themselves, exactly
        if l in (LO, HI): continue
        P, _ = tile(w, L, l); R, _ = tile(pw, pL, l)
        nb += any(image(P, M, False) == image(R, (1, 0, 0, 1), False) for M in SYM) or (bad.append(f'at {l}') or False)
    first = next((c for c in cross if not c.startswith('over')), None)
    firstover = next((c for c in cross if c.startswith('over')), None)
    print(f'{key} ({w}, layer {L}): {ok}/{sub} sub-intervals symbolic PASS, {nb}/{len(B) - 2} breakpoints PASS; '
          f'tet meets cut plane at λ = {sorted(set(c for c in cross if not c.startswith("over")), key=lambda x: Fr(x))}; first over: {firstover}'
          + (f'; FAIL {bad}' if bad else ''), flush=True)
