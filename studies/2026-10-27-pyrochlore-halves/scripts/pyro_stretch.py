# Pyrochlore Halves, stretch-wide proof (DICTO 2026-10-27), #57's method (exact_stretch.py, exact_proof2.py) on four sites per gap.
# On each stretch of the walk every corner of every cell is an affine function of λ (census engine). For each window and stretch:
#  (1) LOCALITY: every corner of every central cell within squared distance R2 of its site (exact at the stretch ends; convexity) —
#      reported; the hand step needs R2 below the bound for sites 2.25 layer spacings away (S sits on the gap's lower layer).
#  (2) S, C whole: one symmetry g of the layer (24) maps the corner FUNCTIONS onto those of the pure piece (S: its own layer; C: its
#      nearest layer above) — equal for every λ in the stretch.
#  (3) O, Y halves: functions measured from the gap's mid-plane; the stretch is split where a corner crosses it; on each part one g
#      maps the corners above / on / below and the section points (exact rational functions of λ, sympy) onto the pure half's.
import itertools, sys, os
sys.path.insert(0, os.path.expanduser('~/work/st57/scripts')); os.chdir(os.path.expanduser('~/work/st57/scripts'))
from fractions import Fraction as Fr
import sympy as sp
from engine import Net, Cell, aff_eval, gdot, vsub
from catalogue import word_for
sys.path.insert(0, os.path.expanduser('~/work/pyro')); from pyro_walk import net_for
_h = open('exact_halves.py').read(); exec(_h[_h.index('def corners_at'):_h.index('# references:')])
_s = open('exact_stretch.py').read(); exec(_s[_s.index('def ops():'):_s.index('REFN = ')])          # ops/OPS, funcs, apply, side
def build(word):
    spec = net_for(word); return Net(word, spec['G'], spec['T'], spec['motif'], spec['w']), spec
ROLE = ['S', 'C', 'O', 'Y']; ZMID = {'O': Fr(0), 'Y': Fr(1, 4)}       # mid-plane height above the site, in layer spacings
REF = {'c': build('ABC'), 'h': build('AB')}; REFN = {'c': 3, 'h': 2}
STOPS = [Fr(-11, 36), Fr(-1, 4), Fr(-3, 20), Fr(0), Fr(1, 8), Fr(1, 6), Fr(1, 4)]
L = sp.Symbol('lam')
def shift(F, zc): return [(x, y, (z[0] - zc, z[1])) for x, y, z in F]
def d2_layer(v): x, y, z = v; return x * x + x * y + y * y + Fr(2, 3) * z * z
def corner_at(f, lam): return tuple(f[r][0] + f[r][1] * lam for r in range(3))
def crossing_edges(F, E, lam):
    return [(a, b) for a, b in E if (F[a][2][0] + F[a][2][1] * lam) * (F[b][2][0] + F[b][2][1] * lam) < 0]
def section(F, E2):
    pts = set()
    for a, b in E2:
        za = F[a][2][0] + F[a][2][1] * L; zb = F[b][2][0] + F[b][2][1] * L; t = sp.cancel(-za / (zb - za))
        pts.add(tuple(sp.cancel((F[a][r][0] + F[a][r][1] * L) + t * ((F[b][r][0] + F[b][r][1] * L) - (F[a][r][0] + F[a][r][1] * L))) for r in range(3)))
    return frozenset(pts)
def ref_cells(t, role, lam):
    net, spec = REF[t]; out = []
    for i2, (k2, p2) in enumerate(spec['motif']):
        if ROLE[i2 % 4] != role: continue
        c2 = cell(net, i2, lam)
        if c2 is not None: out.append((c2, funcs(c2, spec, i2, REFN[t])))
    return out
ok = bad = 0; R2max = Fr(0); fails = []
for hc in (sys.argv[1:] or [''.join(w) for w in itertools.product('hc', repeat=4)]):
    word = word_for(hc); net, spec = build(word); n = len(word); T = layer_types(word); g0 = 2
    for lo, hi in zip(STOPS, STOPS[1:]):
        mid = (lo + hi) / 2
        for j in range(4):
            i = 4 * g0 + j; role = ROLE[j]; c = cell(net, i, mid)
            if c is None: continue
            iv = c.interval()
            if not ((iv[0] is None or iv[0] <= lo) and (iv[1] is None or iv[1] >= hi)):   # combinatorics change inside: split at the engine's breakpoints
                fails.append(f'SPLIT {hc} ({lo},{hi}) {role}: interval {iv}'); bad += 1; continue
            F = funcs(c, spec, i, n)
            R2max = max([R2max] + [d2_layer(corner_at(f, lam)) for f in F for lam in (lo, hi)])
            if role in 'SC':
                t = T[g0 % n] if role == 'S' else T[(g0 + 1) % n]
                cands = {frozenset(F2) for _, F2 in ref_cells(t, role, mid)}
                good = any(frozenset(apply(g, f) for f in F) in cands for g in OPS)
            else:
                Fz = shift(F, ZMID[role]); E = edges(c)
                cuts = sorted({-f[2][0] / f[2][1] for f in Fz if f[2][1] != 0 and lo < -f[2][0] / f[2][1] < hi})
                good = True
                for a, b in zip([lo] + cuts, cuts + [hi]):
                    ls = (a + b) / 2
                    for sgn, t in ((1, T[(g0 + 1) % n]), (-1, T[g0 % n])):
                        found = False
                        for c2, F2 in ref_cells(t, role, ls):
                            F2z = shift(F2, ZMID[role]); S2 = section(F2z, crossing_edges(F2z, edges(c2), ls))
                            for g in OPS:
                                G = [apply(g, f) for f in Fz]
                                if side(G, sgn, ls) != side(F2z, sgn, ls) or side(G, 0, ls) != side(F2z, 0, ls): continue
                                if section(G, crossing_edges(G, E, ls)) == S2: found = True; break
                            if found: break
                        good &= found
                        if not found: fails.append(f'HALF {hc} ({a},{b}) {role} side {sgn}')
            ok += good; bad += (not good)
            if not good and role in 'SC': fails.append(f'WHOLE {hc} ({lo},{hi}) {role}')
    print(f'window {hc}: {ok} ok, {bad} bad; R2 so far {R2max} = {float(R2max):.6f}', flush=True)
print('\n'.join(fails[:30])); print(f'TOTAL {ok} ok, {bad} bad; R2max {R2max} = {float(R2max):.6f}')
