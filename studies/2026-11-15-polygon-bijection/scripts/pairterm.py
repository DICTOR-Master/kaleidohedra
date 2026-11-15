"""Where the nearest-neighbour product terms of p24 come from (study 2026-11-15-polygon-bijection, section 8).
For each flip kf, the four-crossing Delta (Theorem B) is split by (R, F) = (root bonds, far bonds); the change of each split when
the letter of a neighbouring bilayer is switched c -> h shows which side's asymmetry table carries the dependence, and at which size.
Also: the smallest F at which a half's asymmetry table depends on the letter of the half's first bilayer (kf +- 1) or second."""
import sys, os, itertools
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import halves24 as H
out = lambda *a: print(*a, flush=True)
FMAX = 14; LMAX = 24

def split(cr, cf, wtype):
    tab_r, _ = H.cached(cr, FMAX); _, Af = H.cached(cf, FMAX)
    Ar = H.asym(tab_r, 1 + H.WTYPES.index(wtype))
    byS = defaultdict(list)
    for (S, M, F), v in Af.items(): byS[S].append((M, F, v))
    res = defaultdict(int)
    for (S, M, R), vr in Ar.items():
        for (Mp, F, vf) in byS.get(S, ()):
            if Mp != M and R + F + 4 == LMAX: res[(R, F)] += vr * vf
    return {k: -v // 2 for k, v in res.items() if v}

def word(kf, letters):
    w = ['c'] * 19
    for b, x in letters.items(): w[b + 9] = x
    w[kf + 9] = 'c'; return ''.join(w)

# 1. dependence of a single half's tables on its own bilayers 1 and 2 (letters c[0..3]: c[2] decides bilayer 1, c[3] bilayer 2)
pats = {}
for c1 in (1, 2):
    for h1 in (0, 1):
        for h2 in (0, 1):
            c = [0, c1]; c.append(c[0] if h1 else (2 * c[1] - c[0]) % 3); c.append(c[1] if h2 else (2 * c[2] - c[1]) % 3)
            pats[(c1, h1, h2)] = c
for (c1, h1, h2), c in sorted(pats.items()):
    if h1 == 0 and h2 == 0:
        for name, other in (('bilayer 1 (next to the cut)', pats[(c1, 1, 0)]), ('bilayer 2', pats[(c1, 0, 1)])):
            ta, Aa = H.cached(c, FMAX); tb, Ab = H.cached(other, FMAX)
            dF = sorted({k[2] for k in set(Aa) | set(Ab) if Aa.get(k, 0) != Ab.get(k, 0)})
            dw = {}
            for wt in H.WTYPES:
                A1 = H.asym(ta, 1 + H.WTYPES.index(wt)); A2 = H.asym(tb, 1 + H.WTYPES.index(wt))
                d = sorted({k[2] for k in set(A1) | set(A2) if A1.get(k, 0) != A2.get(k, 0)})
                if d: dw[wt] = d[0]
            out(f'HALF letters c1={c1}: switching {name} c->h changes A_far first at F = {dF[:1]} (all F: {dF}); weighted A_root first at {dw}')
out('PROGRESS 0.5 half tables done')
# 2. split of Delta4 at l = 24 by (R, F), and its change with each neighbour letter
for kf in (-3, -2, -1, 0, 1, 2):
    base = split(*H.halves_of(word(kf, {}), kf))
    out(f'SPLIT flip {kf} (all other letters c): Delta24 = {sum(base.values())} by (R,F): {dict(sorted(base.items()))}')
    for nb in (kf - 2, kf - 1, kf + 1, kf + 2):
        alt = split(*H.halves_of(word(kf, {nb: 'h'}), kf))
        diff = {k: alt.get(k, 0) - base.get(k, 0) for k in set(alt) | set(base) if alt.get(k, 0) != base.get(k, 0)}
        side = 'root' if (nb - kf) * (1 if kf >= 0 else -1) < 0 else 'far'
        out(f'   neighbour {nb} ({side} side) c->h: change {sum(diff.values())} by (R,F): {dict(sorted(diff.items()))}')
ok = all(sum(split(*H.halves_of(word(kf, {}), kf)).values()) == v for kf, v in zip((-3, -2, -1, 0, 1, 2), (-732, -483, -4485, -7518, 666, -1128)))
out('CONTROL split totals (all letters c) = DELTA4 l24 of polylaw24-tables:', 'ok' if ok else 'FAIL')
out('PROGRESS 1.0 splits done')
out('ALLCHECKS', 'ok' if ok else 'FAIL')
