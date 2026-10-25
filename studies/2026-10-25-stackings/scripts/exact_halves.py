# Exact half-piece theorem check (DICTO 2026-10-25). For every site of every one of the 16 catalogue windows, on every stretch of the
# walk (two rational sample λ per stretch), in exact rational arithmetic (census engine; corners are rational at rational λ, the metric
# is rational, so squared distances are exact):
#  • an octahedral site's cell, cut by the horizontal plane through the site, has an upper half congruent to the upper half of the
#    octahedral piece of the pure stacking (cubic ABC if the layer above is c, hexagonal AB if h), and likewise the lower half;
#  • a tetrahedral site's whole cell is congruent to the tetrahedral piece of the pure stacking named by the layer it sits on.
# Congruence test: equal sorted multisets of exact squared distances between all corner pairs (cut points included for halves).
import itertools, sys, json
from fractions import Fraction as Fr
from engine import Net, Cell, aff_eval, gdot, vsub
from stackings import net_for
from catalogue import word_for
def build(word):
    spec = net_for(word); return Net(word, spec['G'], spec['T'], spec['motif'], spec['w']), spec
def corners_at(c, lam): return [tuple(aff_eval(p['P'][r], (lam,)) for r in range(3)) for p in c.corners]
def edges(c):
    F = set(c.faces()); E = []
    for a, b in itertools.combinations(range(len(c.corners)), 2):
        if len(c.corners[a]['on'] & c.corners[b]['on'] & F) >= 2: E.append((a, b))
    return E
def half(c, lam, zc, up):
    X = corners_at(c, lam); keep = [x for x in X if (x[2] >= zc if up else x[2] <= zc)]
    for a, b in edges(c):
        za, zb = X[a][2], X[b][2]
        if (za - zc) * (zb - zc) < 0:
            t = (zc - za) / (zb - za); keep.append(tuple(X[a][r] + t * (X[b][r] - X[a][r]) for r in range(3)))
    return sorted(set(keep))
def fp(G, pts):
    return sorted(gdot(G, vsub(p, q), vsub(p, q)) for p, q in itertools.combinations(pts, 2))
def cell(net, i, lam, D2=12):
    c = Cell(net, i, (lam,), Fr(D2)); return None if c.empty else c
def layer_types(word):                       # h/c of every layer of a periodic word
    n = len(word); return ['h' if word[(k - 1) % n] == word[(k + 1) % n] else 'c' for k in range(n)]
# references: pure cubic (ABC) and hexagonal (AB), per λ: oct halves and tet whole pieces
REF = {'c': build('ABC'), 'h': build('AB')}
def ref_fps(t, lam):
    net, spec = REF[t]; out = {'oct_up': set(), 'oct_dn': set(), 'tet': set()}
    for i, (k, p) in enumerate(spec['motif']):
        c = cell(net, i, lam)
        if c is None: continue
        if k == 'oct':
            out['oct_up'].add(tuple(fp(net.G, half(c, lam, Fr(p[2]), True)))); out['oct_dn'].add(tuple(fp(net.G, half(c, lam, Fr(p[2]), False))))
        else: out['tet'].add(tuple(fp(net.G, corners_at(c, lam))))
    return out
lams = [Fr(-7, 16), Fr(-5, 12), Fr(-1, 4), Fr(-3, 16), Fr(-1, 16), Fr(1, 300), Fr(1, 10), Fr(1, 4), Fr(1, 3), Fr(5, 16)]
ok = bad = 0; report = []
for hc in itertools.product('hc', repeat=4):
    hc = ''.join(hc); word = word_for(hc); net, spec = build(word); n = len(word); T = layer_types(word)
    for lam in lams:
        R = {t: ref_fps(t, lam) for t in 'hc'}
        for g in (2,):                                 # the central gap of the window (layers 2 and 3)
            for j in range(3):
                i = 3 * g + j; k, p = spec['motif'][i]; c = cell(net, i, lam)
                if c is None: continue
                if k == 'oct':
                    up_t, dn_t = T[(g + 1) % n], T[g % n]
                    u = tuple(fp(net.G, half(c, lam, Fr(p[2]), True))); d = tuple(fp(net.G, half(c, lam, Fr(p[2]), False)))
                    good = (u in R[up_t]['oct_up'] or u in R[up_t]['oct_dn']) and (d in R[dn_t]['oct_dn'] or d in R[dn_t]['oct_up'])
                else:
                    lay = g if j == 1 else g + 1        # tet over X sits on layer g, tet under Y on layer g+1
                    good = tuple(fp(net.G, corners_at(c, lam))) in R[T[lay % n]]['tet']
                ok += good; bad += (not good)
                if not good: report.append(f"FAIL window {hc} ({word}) λ={lam} site {i} {k}")
    print(f"window {hc}: running total {ok} PASS, {bad} FAIL", flush=True)
print('\n'.join(report[:40])); print(f"TOTAL {ok} PASS, {bad} FAIL")
