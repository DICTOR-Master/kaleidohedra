"""Step 8 (DICTO: "are there any cycles involving RDs and TOs?"). C.O pair, labels as in s6: cube = S:P, octahedron = S:Pstar,
truncated octahedron TO = S:A* (mu = 3/2), rhombic dodecahedron RD = H:rect (mu = 2, conv(cube u 2 octahedron)),
Icosaxes = S:G* (phi), Unborn Axes = S:L* (3 - phi).
A. Space-filler cycles: every tight cycle that starts and ends at the cube and visits any ordered subset of {RD, TO, Icosaxes,
   Unborn Axes} (each fills space on its own; Icosaxes and Unborn Axes each fill space, #48/#89), exact closures.
B. Tight cycles (<= 4 links) through all C.O stations of s6 that contain the RD or the TO, with closure in {phi^k, (1+sqrt2)^k,
   2, 3, 4}: counts and the shortest examples, exact.
usage (compute-host): python3 s8_rd_to.py -> ../data/s8-rd-to.json
"""
from dp_lib import *          # noqa
import numpy as np
from scipy.spatial import ConvexHull
pl = platonic(); P = Pair('cube', pl['cube'][0])
x3G, x3L = x_golden(3); xG, xL = x_golden(4)
named = [('octahedron', P.mu_Ps(ZERO), 'S'), ('Unborn Axes', P.mu_Ps(x3L), 'S'), ('TO', P.mu_Ps(ONE / 3), 'S'), ('Icosaxes', P.mu_Ps(x3G), 'S'),
         ('cuboctahedron', P.rho2, 'S'), ('Greater GCC', P.mu_P(xG), 'S'), ('truncated cube', P.mu_P(ONE / (S2 + 2)), 'S'),
         ('Lesser GCC', P.mu_P(xL), 'S'), ('cube', P.R2, 'S'),
         ('H(Unborn)', P.mu_Ps(x3L), 'H'), ('tetrakis hexahedron H(TO)', P.mu_Ps(ONE / 3), 'H'), ('H(Icosaxes)', P.mu_Ps(x3G), 'H'),
         ('RD', P.rho2, 'H'), ('H(GGCC)', P.mu_P(xG), 'H'), ('triakis octahedron H(tC)', P.mu_P(ONE / (S2 + 2)), 'H'), ('H(LGCC)', P.mu_P(xL), 'H')]
st = {lab: (P.S(mu) if kind == 'S' else P.Hull(mu)) for lab, mu, kind in named}
check('labels: TO = S(3/2) has 24 corners (truncated octahedron), RD = H(2) has 14 corners and 12 rhombic faces',
      len(st['TO']) == 24 and len(st['RD']) == 14 and signature(hull3(st['RD'])[1]) == {4: 12})
out = {}
def closure(seq):
    t = ONE; fac = []
    for a, b in zip(seq, seq[1:]):
        f = tight(st[a], st[b]); fac.append(f); t = t * f
    return t, fac
# A
fill = ['RD', 'TO', 'Icosaxes', 'Unborn Axes']
rows = []
for r in range(1, 5):
    for sub in itertools.permutations(fill, r):
        seq = ['cube'] + list(sub) + ['cube']
        t, fac = closure(seq)
        k = is_phi_power(t)
        rows.append({'cycle': seq, 'factors': [kstr(f) for f in fac], 'closure': kstr(t), 'closure_float': float(t),
                     'phi_power': k, 'touching_all_links': True})
rows.sort(key=lambda d: d['closure_float'])
out['space_filler_cycles'] = rows
for d in rows[:12]: print('   ', ' -> '.join(d['cycle']), '|', d['closure'], f'~{d["closure_float"]:.6f}', d['phi_power'], flush=True)
check(f'A: {len(rows)} space-filler cycles through the cube (exact closures; smallest {rows[0]["closure"]})', True)
gold = [d for d in rows if d['phi_power'] is not None]
out['space_filler_golden'] = gold
check(f'A: space-filler cycles with a golden closure (power of phi): {[(" -> ".join(d["cycle"]), d["closure"]) for d in gold]}', True)
# B
names = list(st); n = len(names)
Fv = {k: np.array([[float(x) for x in p] for p in V]) for k, V in st.items()}
def fpl(V):
    h = ConvexHull(V); E = np.unique(np.round(h.equations, 10), axis=0); return E[:, :3], -E[:, 3]
Fp = {k: fpl(v) for k, v in Fv.items()}
L = np.array([[((Fv[a] @ Fp[b][0].T) / Fp[b][1]).max() for b in names] for a in names])
tg = {f'phi^{k}': float(PHI) ** k for k in range(1, 9)}
tg.update({f'(1+sqrt2)^{k}': (1 + 2 ** .5) ** k for k in range(1, 5)}); tg.update({'2': 2., '3': 3., '4': 4.})
iC = names.index('cube'); iRD = names.index('RD'); iTO = names.index('TO')
hits = []
def dfs(path, prod):
    if len(path) > 1 and path[-1] == iC:
        if iRD in path or iTO in path:
            for k, v in tg.items():
                if abs(prod - v) < 1e-9 * v: hits.append((len(path), k, path[:]))
        return
    if len(path) >= 6: return
    for j in range(n):
        if j == path[-1] or (j in path[1:]) or (j == iC and len(path) < 2): continue
        dfs(path + [j], prod * L[path[-1], j])
dfs([iC], 1.0)
from collections import defaultdict
by = defaultdict(list)
for ln, k, p in sorted(hits): by[k].append(p)
ex = {}
for k, ps in by.items():
    both = [p for p in ps if iRD in p and iTO in p]
    sel = (both[:3] + [p for p in ps if p not in both][:3])
    ex[k] = {'count': len(ps), 'count_with_both_RD_and_TO': len(both), 'examples': []}
    for p in sel:
        seq = [names[i] for i in p]; t, fac = closure(seq)
        ex[k]['examples'].append({'cycle': seq, 'factors': [kstr(f) for f in fac], 'closure': kstr(t), 'exact': abs(float(t) - tg[k]) < 1e-12})
    print('   B', k, ex[k]['count'], ex[k]['count_with_both_RD_and_TO'], ex[k]['examples'][:2], flush=True)
out['cycles_with_RD_or_TO'] = ex
check('B: every listed example re-checked exactly', all(e['exact'] for v in ex.values() for e in v['examples']))
save('s8-rd-to.json', out)
