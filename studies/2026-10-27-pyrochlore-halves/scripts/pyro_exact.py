# Pyrochlore Halves, EXACT (DICTO 2026-10-27), by #57's method (k-research studies/2026-10-25-stackings/scripts exact_halves.py,
# exact_proof2.py), with #57's census engine unchanged. Sites per gap: S (ball, layer k), C (diamond atom, nearest layer k+1),
# O and Y (empty holes, cut at the gap's mid-height). For each of the 16 windows (h/c of the four layers round the central gap: every
# close-packed stacking looks like one of them near a gap) and rational λ inside every stretch of the common walk (-11/36, 1/4):
#   (A) S and C whole: congruent (exact squared corner distances) to the same site's piece in the pure stacking of its layer;
#   (B) O and Y halves (cut points included): congruent to the matching half in the pure stacking of the layer on that side;
#   (C) locality: every corner of every central cell within squared distance R2 of its site (reported), which with the weight bound
#       |λ| <= 11/36 limits the cell to the window's layers (hand step, as #57).
import itertools, sys, os
sys.path.insert(0, os.path.expanduser('~/kres-tmp/st57/scripts')); os.chdir(os.path.expanduser('~/kres-tmp/st57/scripts'))
from fractions import Fraction as Fr
from engine import Net, Cell, aff_eval, gdot, vsub
from catalogue import word_for
sys.path.insert(0, os.path.expanduser('~/kres-tmp/pyro')); from pyro_walk import net_for
_h = open('exact_halves.py').read(); exec(_h[_h.index('def corners_at'):_h.index('# references:')])   # #57's helpers: corners_at, edges, half, fp, cell, layer_types
def build(word):
    spec = net_for(word); return Net(word, spec['G'], spec['T'], spec['motif'], spec['w']), spec
ROLE = ['S', 'C', 'O', 'Y']                       # motif order per gap in pyro_walk.net_for
REF = {'c': build('ABC'), 'h': build('AB')}
def ref(t, lam):
    net, spec = REF[t]; out = {}
    for i, (k, p) in enumerate(spec['motif']):
        r = ROLE[i % 4]; c = cell(net, i, lam)
        if c is None: continue
        if r in 'SC': out.setdefault(r, set()).add(tuple(fp(net.G, corners_at(c, lam))))
        else:
            mid = Fr(p[2]) if r == 'O' else Fr(p[2]) + Fr(1, 4) / (len(spec['motif']) // 4)   # z in cell heights: O at mid-gap; Y a quarter gap below it
            out.setdefault(r + 'up', set()).add(tuple(fp(net.G, half(c, lam, mid, True)))); out.setdefault(r + 'dn', set()).add(tuple(fp(net.G, half(c, lam, mid, False))))
    return out
STOPS = [Fr(-11, 36), Fr(-1, 4), Fr(-3, 20), Fr(0), Fr(1, 8), Fr(1, 6), Fr(1, 4)]
lams = [a + (b - a) * Fr(k, 3) for a, b in zip(STOPS, STOPS[1:]) for k in (1, 2)]
ok = bad = 0; report = []; R2max = Fr(0)
WINDOWS = sys.argv[1:] or [''.join(w) for w in itertools.product('hc', repeat=4)]   # one window per process for speed
for hc in WINDOWS:
    word = word_for(hc); net, spec = build(word); n = len(word); T = layer_types(word)
    for lam in lams:
        R = {t: ref(t, lam) for t in 'hc'}; g = 2
        for j in range(4):
            i = 4 * g + j; r = ROLE[j]; k, p = spec['motif'][i]; c = cell(net, i, lam)
            if c is None: continue
            P = corners_at(c, lam); R2max = max(R2max, max(gdot(net.G, vsub(x, p), vsub(x, p)) for x in P))
            if r == 'S': good = tuple(fp(net.G, P)) in R[T[g % n]]['S']
            elif r == 'C': good = tuple(fp(net.G, P)) in R[T[(g + 1) % n]]['C']
            else:
                mid = Fr(p[2]) if r == 'O' else Fr(p[2]) + Fr(1, 4) / n
                u = tuple(fp(net.G, half(c, lam, mid, True))); d = tuple(fp(net.G, half(c, lam, mid, False)))
                good = (u in R[T[(g + 1) % n]][r + 'up']) and (d in R[T[g % n]][r + 'dn'])
            ok += good; bad += (not good)
            if not good: report.append(f'FAIL window {hc} ({word}) λ={lam} site {r}')
    print(f'window {hc}: running {ok} PASS, {bad} FAIL', flush=True)
print('\n'.join(report[:40])); print(f'TOTAL {ok} PASS, {bad} FAIL; largest squared corner distance from its site {R2max} = {float(R2max):.6f}')
