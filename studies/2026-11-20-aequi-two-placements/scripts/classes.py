# Th and T on the 122 directions of both icosahedron placements: orbits, normaliser (all 48 Oh maps normalise Th and T
# and permute the 122 directions; the quarter turn swaps the placements), and the orbit sets that use BOTH placements
# (at least one orbit from D12/I12/RT24 and one from D12p/I12p/RT24p), m >= 2, bounded, reduced by the normaliser
# (a set and its quarter-turned or mirrored image count once). Sets using one placement only are counted and excluded
# (they were searched in study 2026-11-19-aequi-complete). Writes data/classes.json in that study's format.
# usage: classes.py out.json
import json, itertools, sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import *
from solve import bounded
TH = closure([P3, rot((0, 0, 1), np.pi), -np.eye(3)])
T = closure([P3, rot((0, 0, 1), np.pi)])
assert len(TH) == 24 and len(T) == 12 and schoenflies(TH) == 'Th' and schoenflies(T) == 'T'
OHK = {key(g) for g in OH}
assert all(key(g) in OHK for g in TH)
PERM = {key(g): dperm(g) for g in OH}
out = []
for name, H in [('Th', TH), ('T', T)]:
    K = frozenset(key(h) for h in H)
    seen = set(); orbs = []
    for i in range(len(DIRS)):
        if i in seen: continue
        O = tuple(sorted({PERM[key(h)][i] for h in H})); seen |= set(O); orbs.append(O)
    assert all(len({DFAM[j] for j in O}) == 1 for O in orbs)
    Nm = [PERM[key(g)] for g in OH if frozenset(key(g @ h @ g.T) for h in H) == K]
    assert len(Nm) == 48
    oi = {O: i for i, O in enumerate(orbs)}
    Nperm = sorted({tuple(oi[tuple(sorted(p[j] for j in O))] for O in orbs) for p in Nm})
    fams = [[DFAM[O[0]]] for O in orbs]; k = len(orbs)
    cnt = {}; reps_all = {}
    for m in range(2, k + 1):
        reps = sorted({min(tuple(sorted(P[i] for i in S)) for P in Nperm) for S in itertools.combinations(range(k), m)})
        mx = [S for S in reps if mixed([fams[i] for i in S])]
        one = [S for S in reps if not mixed([fams[i] for i in S])]
        nb = [S for S in mx if bounded(DIRS[[j for i in S for j in orbs[i]]])]
        cnt[m] = dict(reduced=len(reps), one_placement=len(one), both_placements=len(mx), both_bounded=len(nb))
        reps_all[m] = nb
    print('%-3s |H|=%d orbits=%d %s' % (name, len(H), k, ' '.join('%s%d' % (f[0], len(O)) for f, O in zip(fams, orbs))))
    for m in cnt: print('   m=%2d %s' % (m, cnt[m]))
    print('   both placements, all m:', sum(c['both_bounded'] for c in cnt.values()), flush=True)
    out.append(dict(name=name, order=len(H), polar=False, n_conj=1, elements=[np.round(h, 12).tolist() for h in H],
                    orbits=[list(O) for O in orbs], orbit_fams=fams, normaliser_perms=[list(p) for p in Nperm],
                    counts={str(m): v for m, v in cnt.items()}))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print('FINAL ok' if len(out) == 2 else 'FINAL FAIL')
