# Part 2(a): both icosahedron placements under every subgroup of Oh with one fixed point that does not contain T
# (sets of Oh, O, Td orbits are sets of T orbits, searched in study 2026-11-20-aequi-two-placements; Th and T were
# searched there). Groups with a fixed line or plane (C_n, C_nv, C_s, C_1) are left out: their fair solids found in
# study 2026-11-19-aequi-complete never had the centroid at the centre (README there), so they give no Aequus.
# Subgroups up to conjugation by Oh (every Oh map permutes the 122 directions); orbits on the 122 directions;
# orbit sets with m >= 2 that use both placements (some orbit with a D12/I12/RT24 direction and some with a
# D12p/I12p/RT24p direction), bounded, reduced by the normaliser in Oh. Counts per m up to the cap.
# usage: classes2a.py out.json MAXSETS
import json, itertools, sys, numpy as np
from math import comb
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import *
from solve import bounded
MAXSETS = int(sys.argv[2])
PERM = {key(g): dperm(g) for g in OH}
SG = subgroups(OH); print('subgroups of Oh', len(SG), flush=True)
def polar(H): return np.linalg.matrix_rank(np.vstack([h - np.eye(3) for h in H]), tol=1e-8) < 3
Tk = frozenset(key(h) for h in closure([P3, rot((0, 0, 1), np.pi)]))
cls = []
for H in sorted(SG, key=lambda H: -len(H)):
    K = frozenset(key(h) for h in H)
    if polar(H) or Tk <= K: continue
    if any(frozenset(key(g @ h @ g.T) for h in H) in c['conj'] for c in cls for g in OH[:1]): continue
    if any(K in c['conj'] for c in cls): continue
    conj = {frozenset(key(g @ h @ g.T) for h in H) for g in OH}
    cls.append(dict(H=H, K=K, conj=conj))
out = []
for c in cls:
    H = c['H']; K = c['K']
    seen = set(); orbs = []
    for i in range(len(DIRS)):
        if i in seen: continue
        O = tuple(sorted({PERM[key(h)][i] for h in H})); seen |= set(O); orbs.append(O)
    fams = [sorted({DFAM[j] for j in O}) for O in orbs]
    Nm = [PERM[key(g)] for g in OH if frozenset(key(g @ h @ g.T) for h in H) == K]
    oi = {O: i for i, O in enumerate(orbs)}
    Nperm = sorted({tuple(oi[tuple(sorted(p[j] for j in O))] for O in orbs) for p in Nm})
    k = len(orbs); cnt = {}; cap = None
    for m in range(2, k + 1):
        if comb(k, m) > MAXSETS: cap = m - 1; break
        reps = {min(tuple(sorted(P[i] for i in S)) for P in Nperm) for S in itertools.combinations(range(k), m)}
        mx = [S for S in reps if mixed([fams[i] for i in S]) and bounded(DIRS[[j for i in S for j in orbs[i]]])]
        cnt[m] = len(mx)
    name = schoenflies(H)
    print('%-4s |H|=%2d conj=%d orbits=%2d cap m<=%s  mixed bounded sets by m: %s  total %d' % (name, len(H), len(c['conj']), k, cap if cap else 'all', cnt, sum(cnt.values())), flush=True)
    out.append(dict(name=name, order=len(H), polar=False, n_conj=len(c['conj']), elements=[np.round(h, 12).tolist() for h in H],
                    orbits=[list(O) for O in orbs], orbit_fams=fams, normaliser_perms=[list(p) for p in Nperm],
                    counts={str(m): v for m, v in cnt.items()}, cap=cap))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print('FINAL ok' if out else 'FINAL FAIL')
