#!/usr/bin/env python3
"""Dual cats, minimal covers (DICTO 16 Nov 2026). From s4's per-copy whole coverage (dual_cover.pkl): the fewest polar-dual copies
whose fins cover all 720 pentagons (and all 1200 edges) of the 120-cell. 0/1 set cover solved by HiGHS (scipy.optimize.milp);
every cover found is re-checked as a set union; the lower bound comes from the mirrors: each pentagon lies on one of Q's 60 mirrors
(12 per mirror), a copy covers 6 pentagons on each of its S5's 10 mirrors, so every mirror needs at least 2 copies.
usage: s5_dual_min_cover.py OUTDIR"""
import os, sys, json, time, pickle
from collections import Counter
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rq_lib import Checks, World
OUT = sys.argv[1]; C = Checks(); T0 = time.time(); out = {}
def say(*a): print(*a, f'({time.time() - T0:.0f}s)', flush=True)
d = pickle.load(open(os.path.join(OUT, 'dual_cover.pkl'), 'rb'))
copies = d['copies']; WPn = [set(x) for x in d['whole_p']]; WEn = [set(x) for x in d['whole_e']]; pent_edge = d['pent_edge']
Wd = World(); Pf = Wd.Pf
def mkey(v):
    v = v/np.linalg.norm(v); i = np.argmax(np.abs(v) > 1e-9); v = v if v[i] > 0 else -v; return tuple(np.round(v, 6) + 0.0)
mir = [mkey(Pf[a] - Pf[b]) for a, b in pent_edge]; mids = {k: i for i, k in enumerate(sorted(set(mir)))}; mir = [mids[k] for k in mir]
C(len(mids) == 60 and set(Counter(mir).values()) == {12}, "the 720 pentagons lie 12 on each of Q's 60 mirrors")
per = Counter(tuple(sorted(Counter(mir[k] for k in s).values())) for s in WPn)
C(set(per) == {(6,)*10}, f'every copy covers exactly 6 pentagons on each of 10 mirrors ({dict((str(k), v) for k, v in per.items())})')
copym = [frozenset(mir[k] for k in s) for s in WPn]
s5s = sorted(set(copym), key=sorted); out['S5 mirror sets'] = len(s5s)
# within one S5: which halves do its five duals take on each mirror
halves = Counter()
for M in s5s:
    ix = [t for t in range(len(copies)) if copym[t] == M]
    labs = [copies[t][0] for t in ix]
    for m in M:
        hs = [frozenset(k for k in WPn[t] if mir[k] == m) for t in ix]
        halves[(tuple(sorted(Counter(labs).items())), len(set(hs)), tuple(sorted(Counter(hs).values())))] += 1
out['halves per mirror within one S5 (types, distinct halves, multiplicities)'] = {str(k): v for k, v in halves.items()}
say('S5 mirror sets', len(s5s), 'halves', dict(halves))
def solve(sel, target, sets):
    ix = [t for t in range(len(copies)) if copies[t][0] in sel]
    U = sorted(target); pos = {u: i for i, u in enumerate(U)}
    A = np.zeros((len(U), len(ix)))
    for j, t in enumerate(ix):
        for u in sets[t]: A[pos[u], j] = 1
    r = milp(c=np.ones(len(ix)), constraints=LinearConstraint(A, lb=np.ones(len(U)), ub=np.inf), integrality=np.ones(len(ix)), bounds=Bounds(0, 1),
             options={'time_limit': 240})
    if r.x is None: return None, r.status, None
    ch = [ix[j] for j in range(len(ix)) if r.x[j] > 0.5]
    ok = set().union(*[sets[t] for t in ch]) == set(target)
    return ch, r.status, ok, getattr(r, 'mip_dual_bound', None)
res = {}; covers = {}
for lab, sel in (('A*', ('A',)), ('B*', ('B',)), ('C3*', ('C3',)), ('A*+B*', ('A', 'B')), ('all', ('A', 'B', 'C3'))):
    row = {}
    for what, target, sets in (('pentagons', range(720), WPn), ('edges', range(1200), WEn)):
        ch, status, ok, bound = solve(sel, target, sets)
        row[what] = {'min copies': len(ch), 'HiGHS status (0 = optimal)': int(status), 'dual bound': bound, 'union re-checked': ok,
                     'types': dict(Counter(copies[t][0] for t in ch)), 'S5s used': len({copym[t] for t in ch})}
        if what == 'pentagons':
            row[what]['edges whole by the same copies'] = len(set().union(*[WEn[t] for t in ch]))
            row[what]['pentagon multiplicity'] = dict(Counter(sum(k in WPn[t] for t in ch) for k in range(720)))
            covers[lab] = ch
        C(ok, f'{lab}: a cover of all {what} by {len(ch)} copies (union re-checked); ' + ('PROVED minimal (HiGHS optimal)' if status == 0 else f'NOT proved minimal (solver bound {bound})'))
        print('PROGRESS', round((list(('A*', 'B*', 'C3*', 'A*+B*', 'all')).index(lab)*2 + (what == 'edges') + 1)/10, 2), lab, what, flush=True)
    res[lab] = row; say('MIN', lab, json.dumps(row, default=str))
out['minimal covers'] = res
pickle.dump({'covers': covers, 'mir': mir}, open(os.path.join(OUT, 'dual_min_cover.pkl'), 'wb'))
out['seconds'] = time.time() - T0
json.dump(out, open(os.path.join(OUT, 'dual_min_cover.json'), 'w'), indent=1, default=str)
C.final()
