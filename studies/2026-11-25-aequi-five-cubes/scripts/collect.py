# Copy from study 2026-11-24-aequi-certify-extend; only edit: family sizes RDa, RDb in label_orbit (groups.py here: the five-cube directions; mixed = RD directions from two or more cubes).
# Merge the double-precision search results, check every planned subset was searched, and classify each solution:
# centroid, full symmetry group (every isometry fixing the centroid that maps the face planes onto themselves; not only
# frame maps), face orbits under it, sides, corners; then remove repeats (congruence signature, mirror images merged).
# usage: collect.py classes.json plan.json out_dice.json sol1.jsonl [sol2.jsonl ...]
import json, sys, itertools, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import DIRS, DFAM, schoenflies, mixed, FAMS
from solve import face_omegas, bounded
from exact import combinatorics, centroid, symmetry
cls = json.load(open(sys.argv[1])); plan = json.load(open(sys.argv[2]))
recs = {}
for f in sys.argv[4:]:
    for L in open(f):
        r = json.loads(L); recs[(r['cls'], r['m'], tuple(r['subset']))] = r
# completeness of each planned (class, m)
status = []
for ci, m in plan:
    C = cls[ci]; orbs = C['orbits']; k = len(orbs); Np = [tuple(p) for p in C['normaliser_perms']]
    reps = sorted({min(tuple(sorted(P[i] for i in S)) for P in Np) for S in itertools.combinations(range(k), m)})
    reps = [S for S in reps if bounded(DIRS[[j for i in S for j in orbs[i]]]) and mixed([C['orbit_fams'][i] for i in S])]
    got = [recs.get((ci, m, S)) for S in reps]
    ns = [len(r['sols']) for r in got if r]
    status.append(dict(cls=ci, group=C['name'], order=C['order'], polar=C['polar'], m=m, subsets=len(reps),
                       searched=sum(1 for r in got if r), sols_hist={str(n): ns.count(n) for n in sorted(set(ns))}))
    print('class %2d %-4s m=%d subsets %5d searched %5d  solutions per set %s' % (ci, C['name'], m, len(reps), status[-1]['searched'], status[-1]['sols_hist']), flush=True)
def label_orbit(idx):
    fams = sorted(set(DFAM[j] for j in idx), key=FAMS.index)
    full = {'C6': 6, 'O8': 8, 'RD12': 12, 'D12': 12, 'I12': 12, 'RT24': 24, 'RDa': 24, 'RDb': 24}
    if len(fams) == 1:
        f = fams[0]; return f if len(idx) == full[f] else '%s/%d' % (f, len(idx))
    return '+'.join(fams) + '/%d' % len(idx)
def classify(args):
    ci, m, S, dep = args
    orbs = cls[ci]['orbits']
    idx = [j for i in S for j in orbs[i]]; sizes = [len(orbs[i]) for i in S]
    D = np.repeat(dep, sizes); Nrm = DIRS[idx]; N = len(idx)
    om = face_omegas(Nrm, D)
    assert np.abs(om - 4 * np.pi / N).max() < 1e-9
    V, inc, trip, faces = combinatorics(Nrm, D)
    cen, vol = centroid(V, faces, Nrm, D)
    G, forbs = symmetry(Nrm, D, cen)
    here = dict(cls=ci, group_searched=cls[ci]['name'], m_searched=m, subset=list(S))
    gname = schoenflies(G)
    forbs = sorted(forbs, key=lambda O: (-len(O), min(idx[j] for j in O)))
    order = sorted(range(len(forbs)), key=lambda k: (FAMS.index(DFAM[idx[forbs[k][0]]]), -len(forbs[k])))
    forbs = [forbs[k] for k in order]
    fidx = [[idx[j] for j in O] for O in forbs]
    # symmetrise: one depth per full-group orbit (the mean), then rebuild the solid from those depths
    dep_o = [float(np.mean(D[O])) for O in forbs]; assert max(np.ptp(D[O]) for O in forbs) < 1e-8
    idx2 = [j for O in fidx for j in O]; sizes2 = [len(O) for O in forbs]
    D2 = np.repeat(dep_o, sizes2); N2 = DIRS[idx2]
    V, inc, trip, faces = combinatorics(N2, D2)
    cen, vol = centroid(V, faces, N2, D2)
    s = vol ** (1 / 3)
    sigv = np.r_[np.sort((D2 - N2 @ cen) / s), np.sort(np.linalg.norm(V - cen, axis=1) / s)]
    key = (N, len(V), gname, tuple(sorted(len(f) for f in faces)))
    d0 = dep_o[0]
    cut2 = np.cumsum([0] + sizes2)
    labels = [label_orbit(O) for O in fidx]
    for L in set(labels):
        if labels.count(L) > 1:
            n = 0
            for i in range(len(labels)):
                if labels[i] == L: n += 1; labels[i] = L + 'abcdefghijkl'[n - 1]
    return key, here, dict(group=gname, sym_order=len(G), chiral=bool(all(np.linalg.det(g) > 0 for g in G)),
                     m=len(forbs), N=N, corners=len(V), orbit_labels=labels, orbit_sizes=[len(O) for O in forbs],
                     idx=[j for O in fidx for j in O], sizes=[len(O) for O in forbs],
                     depths=[x / d0 for x in dep_o], sigv=sigv.tolist(),
                     sides_by_orbit=[sorted({len(faces[j]) for j in range(cut2[k], cut2[k + 1])}) for k in range(len(forbs))],
                     centroid_at_origin=bool(np.abs(cen).max() < 1e-9), centroid=cen.tolist(),
                     face_transitive=len(forbs) == 1)
planset = {tuple(p) for p in plan}
jobs = [(ci, m, S, dep) for (ci, m, S), r in sorted(recs.items()) if (ci, m) in planset for dep in r['sols']]
occ = len(jobs); dice = {}
import multiprocessing as mpc
with mpc.get_context('fork').Pool(int(__import__('os').environ.get('NPROC', '20'))) as pool:
    for key, here, d in pool.imap(classify, jobs, chunksize=16):
        hit = None
        for d2 in dice.get(key, []):
            if len(d2['sigv']) == len(d['sigv']) and np.abs(np.array(d2['sigv']) - np.array(d['sigv'])).max() < 1e-6: hit = d2; break
        if hit is not None: hit['found_under'].append(here); continue
        d['found_under'] = [here]; dice.setdefault(key, []).append(d)
out = [d for L_ in dice.values() for d in L_]
for i, d in enumerate(sorted(out, key=lambda d: (-d['sym_order'], d['group'], d['m'], d['N']))): d['sid'] = i
out.sort(key=lambda d: d['sid'])
json.dump(dict(status=status, dice=out, occurrences=occ), open(sys.argv[3], 'w'), indent=1)
aeq = [d for d in out if d['centroid_at_origin'] and not d['face_transitive']]
print('solutions', occ, 'distinct solids', len(out), '| face-transitive', sum(d['face_transitive'] for d in out),
      '| centroid off the frame centre', sum(not d['centroid_at_origin'] for d in out), '| Aequi', len(aeq))
from collections import Counter
print('Aequi by group', sorted(Counter(d['group'] for d in aeq).items(), key=lambda t: -t[1]))
ok = all(st['searched'] == st['subsets'] for st in status) and len(out) > 0
print('FINAL ok' if ok else 'FINAL FAIL: some planned orbit sets were not searched')
