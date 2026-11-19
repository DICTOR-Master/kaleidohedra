# Enumerate every subgroup of Oh and of Ih (on these frames), their admissible orbits (orbits of the 74 frame
# directions lying wholly inside the frames), reduce subgroups up to conjugacy by frame maps that carry the admissible
# directions onto each other, and count orbit subsets (m >= 2, positively spanning = bounded solid), reduced by the
# normaliser. Writes data/classes.json.
import json, itertools, sys, numpy as np
from math import comb
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import *
from scipy.optimize import linprog
MMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 8
subs = {}
import time; t0 = time.time()
SG = {'Oh': subgroups(OH), 'Ih': subgroups(IH)}
print('subgroups found in', round(time.time() - t0, 1), 's', flush=True)
for G in SG.values():
    for H in G: subs[frozenset(key(h) for h in H)] = H
print('subgroups: Oh', len(SG['Oh']), 'Ih', len(SG['Ih']), 'union', len(subs), flush=True)
PERM = {key(g): dperm(g) for g in ALLG}
def orbits(H):
    seen = set(); orbs = []
    for i in range(74):
        if i in seen: continue
        O = {PERM[key(h)][i] for h in H}
        seen |= {j for j in O if j >= 0}
        if -1 in O: continue
        orbs.append(tuple(sorted(O)))
    return orbs
def adm(H): return frozenset(j for O in orbits(H) for j in O)
recs = []
for K, H in subs.items():
    recs.append(dict(K=K, H=H, name=schoenflies(H), orbs=orbits(H)))
# conjugacy classes w.r.t. frame maps preserving the admissible set
classes = []
for r in sorted(recs, key=lambda r: (-len(r['H']), r['name'])):
    A = frozenset(j for O in r['orbs'] for j in O)
    if not A: continue
    found = False
    for c in classes:
        if len(c['H']) != len(r['H']) or len(c['orbs']) != len(r['orbs']): continue
        for g in ALLG:
            gi = g.T
            if frozenset(key(g @ h @ gi) for h in r['H']) == c['K']:
                p = PERM[key(g)]
                if all(p[j] >= 0 for j in A) and frozenset(p[j] for j in A) == c['A']:
                    found = True; break
        if found: c['n_conj'] += 1; break
    if not found:
        r['A'] = A; r['n_conj'] = 1; classes.append(r)
# drop classes dominated by another: some frame map g carries H' onto H and adm(H') into adm(H) (then every
# orbit subset of H' is congruent to one of H, already searched there)
keep = []
for c in classes:
    dom = None
    for c2 in classes:
        if c2 is c or len(c2['H']) != len(c['H']) or len(c2['A']) <= len(c['A']): continue
        for g in ALLG:
            if frozenset(key(g @ h @ g.T) for h in c['H']) == c2['K']:
                p = PERM[key(g)]
                if all(p[j] >= 0 for j in c['A']) and {p[j] for j in c['A']} <= c2['A']: dom = c2; break
        if dom is not None: break
    if dom is None: keep.append(c)
    else: print('dominated:', c['name'], len(c['orbs']), 'orbits, by', dom['name'], len(dom['orbs']), 'orbits')
classes = keep
print('classes', len(classes))
def bounded(idx):
    V = DIRS[list(idx)]
    # bounded iff 0 is strictly inside conv hull: max t s.t. sum l_i v_i = 0, sum l = 1, l_i >= t
    if np.linalg.matrix_rank(np.asarray(V), tol=1e-9) < 3: return False
    n = len(V); c = np.zeros(n + 1); c[-1] = -1
    Aeq = np.zeros((4, n + 1)); Aeq[:3, :n] = V.T; Aeq[3, :n] = 1
    Aub = np.hstack([-np.eye(n), np.ones((n, 1))])
    res = linprog(c, A_ub=Aub, b_ub=np.zeros(n), A_eq=Aeq, b_eq=[0, 0, 0, 1], bounds=[(0, None)] * n + [(None, None)])
    return res.status == 0 and -res.fun > 1e-9
out = []
for c in classes:
    H = c['H']; orbs = c['orbs']; k = len(orbs)
    # normaliser within frame maps preserving the admissible set
    Nm = []
    for g in ALLG:
        if frozenset(key(g @ h @ g.T) for h in H) == c['K']:
            p = PERM[key(g)]
            if all(p[j] >= 0 for j in c['A']): Nm.append(p)
    oi = {O: i for i, O in enumerate(orbs)}
    Nperm = [tuple(oi[tuple(sorted(p[j] for j in O))] for O in orbs) for p in Nm]
    fixed = all(np.allclose(h, np.eye(3)) for h in H) or False
    # unique fixed point? (non-polar): the only common fixed vector of H is 0
    M = np.vstack([h - np.eye(3) for h in H]); polar = np.linalg.matrix_rank(M, tol=1e-8) < 3
    cnt = {}
    for m in range(2, k + 1):
        if comb(k, m) > 20000 or m > MMAX: cnt[m] = ('unreduced', comb(k, m)); continue
        reps = set()
        for S in itertools.combinations(range(k), m):
            can = min(tuple(sorted(P[i] for i in S)) for P in Nperm)
            reps.add(can)
        nb = sum(1 for S in reps if bounded([j for i in S for j in orbs[i]]))
        cnt[m] = (len(reps), nb)
    print('%-5s |H|=%3d conj=%2d polar=%d orbits=%2d sizes=%s  subsets(m: reduced, bounded)=%s' % (
        c['name'], len(H), c['n_conj'], polar, k, sorted(len(O) for O in orbs), cnt), flush=True)
    out.append(dict(name=c['name'], order=len(H), polar=bool(polar), n_conj=c['n_conj'],
                    elements=[np.round(h, 12).tolist() for h in H], orbits=[list(O) for O in orbs],
                    orbit_fams=[sorted(set(DFAM[j] for j in O)) for O in orbs], normaliser_perms=sorted(set(Nperm)),
                    counts={str(m): v for m, v in cnt.items()}))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
ok = len(out) > 0 and all(c['orbits'] for c in out) and sum(1 for c in out if c['name'] in ('Oh', 'O', 'Td', 'Th', 'T', 'Ih', 'I')) == 7
print('FINAL ok' if ok else 'FINAL FAIL: classes missing or empty')
