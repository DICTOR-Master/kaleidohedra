# Orbit sets of the five-cube directions (study 2026-11-25-aequi-five-cubes; after classes2a.py of study
# 2026-11-24-aequi-certify-extend). Every subgroup of Ih with one fixed point (no fixed line or plane), up to conjugation
# in Ih (Ih permutes the 122 directions); its orbits on the 122; NEW orbit sets (RD directions from at least two of the
# five cubes; groups.mixed), bounded, reduced by the normaliser in Ih. Counts per m; m capped when C(k, m) > MAXSETS.
# Vector-sum check (Theorem B / Corollary B1 of study 2026-11-24-aequi-uniqueness): every orbit sums to 0, so every
# set does.   usage: classes.py out.json MAXSETS
import json, itertools, sys, numpy as np
from math import comb
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import *
from solve import bounded
MAXSETS = int(sys.argv[2])
PERM = {key(g): dperm(g) for g in IH}
SG = subgroups(IH); print('subgroups of Ih', len(SG), flush=True)
def polar(H): return np.linalg.matrix_rank(np.vstack([h - np.eye(3) for h in H]), tol=1e-8) < 3
cls = []
for H in sorted(SG, key=lambda H: -len(H)):
    K = frozenset(key(h) for h in H)
    if polar(H) or any(K in c['conj'] for c in cls): continue
    cls.append(dict(H=H, K=K, conj={frozenset(key(g @ h @ g.T) for h in H) for g in IH}))
out = []; maxsum = 0
for c in cls:
    H = c['H']; K = c['K']
    seen = set(); orbs = []
    for i in range(len(DIRS)):
        if i in seen: continue
        O = tuple(sorted({PERM[key(h)][i] for h in H})); seen |= set(O); orbs.append(O)
    for O in orbs: maxsum = max(maxsum, np.linalg.norm(DIRS[list(O)].sum(0)))
    fams = [sorted({DFAM[j] for j in O}) + sorted({'cube%d' % DCUBE[j] for j in O if DCUBE[j] >= 0}) for O in orbs]
    Nm = [PERM[key(g)] for g in IH if frozenset(key(g @ h @ g.T) for h in H) == K]
    oi = {O: i for i, O in enumerate(orbs)}
    Nperm = sorted({tuple(oi[tuple(sorted(p[j] for j in O))] for O in orbs) for p in Nm})
    k = len(orbs); cnt = {}; cap = None
    for m in range(2, k + 1):
        if comb(k, m) > MAXSETS: cap = m - 1; break
        reps = {min(tuple(sorted(P[i] for i in S)) for P in Nperm) for S in itertools.combinations(range(k), m)}
        mx = [S for S in reps if mixed([fams[i] for i in S]) and bounded(DIRS[[j for i in S for j in orbs[i]]])]
        cnt[m] = len(mx)
    name = schoenflies(H)
    print('%-4s |H|=%3d conj=%2d orbits=%2d (sizes %s) cap m<=%s  new bounded sets by m: %s  total %d' % (
        name, len(H), len(c['conj']), k, sorted({len(O) for O in orbs}), cap if cap else 'all', cnt, sum(cnt.values())), flush=True)
    out.append(dict(name=name, order=len(H), polar=False, n_conj=len(c['conj']), elements=[np.round(h, 12).tolist() for h in H],
                    orbits=[list(O) for O in orbs], orbit_fams=fams, normaliser_perms=[list(p) for p in Nperm],
                    counts={str(m): v for m, v in cnt.items()}, cap=cap))
print('largest |sum of an orbit| = %.2e (every orbit of a group fixing only the centre sums to 0, so every set is balanced)' % maxsum)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print('FINAL ok' if out and maxsum < 1e-12 else 'FINAL FAIL')
