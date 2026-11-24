"""Exact companion of polar_aequi.py. For every die, group its corners into classes of CONGRUENT normal cones:
two corners are in one class when the Gram matrices of their face normals agree exactly (over Q(sqrt5)) after a dihedral
relabelling of the cyclic order. Congruent cones have equal solid angle, so equal curvature is then PROVED exactly.
Compared with the curvature classes of data/polar-aequi.jsonl (ball arithmetic): if, for a die, the number of congruence
classes equals the number of curvature classes, every curvature equality of that die is exact and every inequality certified.
Usage: gram_check.py polar-aequi.jsonl OUT.json NPROC.  FINAL ok when every die is decided this way."""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import polar_aequi as PA
from q5 import Q, PHI
C = PA.C
EX = [tuple(Q(a) + Q(b) * PHI for a, b in q) for q in C.EXACT]
def qd(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
N2 = [qd(q, q) for q in EX]
def ent(i, j):
    if i == j: return (1,)
    d = qd(EX[i], EX[j]); c2 = d * d / (N2[i] * N2[j]); return (c2.key(), d.sign())

def canon(order, idx):
    m = len(order); best = None
    for r in (1, -1):
        for s in range(m):
            perm = [order[(s + r * t) % m] for t in range(m)]
            key = tuple(ent(idx[perm[a]], idx[perm[b]]) for a in range(m) for b in range(a + 1, m))
            if best is None or key < best: best = key
    return (m, best)

def work(rec):
    idx, sizes = rec['idx'], rec['sizes']
    V, inc = C.combinatorics(idx, sizes, rec['depths']); nf = C.DIRS[idx]; keys = []
    for I in inc:
        mvec = sum(nf[i] for i in I); mvec = mvec / np.linalg.norm(mvec)
        e1 = np.cross(mvec, [1, 0, 0] if abs(mvec[0]) < 0.9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(mvec, e1)
        order = sorted(I, key=lambda i: np.arctan2(nf[i] @ e2, nf[i] @ e1))
        keys.append(canon(order, idx))
    return (rec['part'], rec['study'], rec['sid'], len(set(keys)), len(V))

if __name__ == '__main__':
    inp, outp, npr = sys.argv[1], sys.argv[2], int(sys.argv[3])
    pa = {(o['part'], o['study'], o['sid']): o for o in map(json.loads, open(inp))}
    recs = PA.records(); t0 = time.time(); res = {}
    with Pool(npr) as pool:
        for k, (part, study, sid, ncong, nv) in enumerate(pool.imap(work, recs, chunksize=8)):
            res[(part, study, sid)] = ncong
            if (k + 1) % 2000 == 0: print('PROGRESS %.3f %d dice %.0fs' % ((k + 1) / len(recs), k + 1, time.time() - t0), flush=True)
    rows = []; agree = 0; fair_polar = []
    for key, o in pa.items():
        nc = res[key]; ok = nc == o['curv_classes']; agree += ok
        if not ok: rows.append(dict(part=key[0], study=key[1], sid=key[2], label=o['label'], curvature_classes=o['curv_classes'], congruence_classes=nc))
        if nc == 1: fair_polar.append(dict(part=key[0], study=key[1], sid=key[2], label=o['label'], name=o['name'], group=o['group'], N=o['N'], corners=o['corners'],
                                           corner_orbits_frame=o['corner_orbits'], polar_face_sides=o['polar_face_sides'], polar_radii=o['polar_radii']))
    json.dump(dict(dice=len(pa), decided=agree, undecided=rows, polar_fair=fair_polar), open(outp, 'w'), indent=1, ensure_ascii=False)
    print('dice', len(pa), '| congruence classes = curvature classes:', agree, '| undecided:', len(rows), rows[:10])
    print('dice whose corners are all congruent (polar fair, exact):', len(fair_polar), [(r['part'], r['sid'], r['label']) for r in fair_polar])
    cand = [k for k, o in pa.items() if o['curv_classes'] == 1]
    cand_open = [dict(part=k[0], study=k[1], sid=k[2], label=pa[k]['label'], congruence_classes=res[k], curvature=pa[k]['curv_min'],
                      over_4pi_120=pa[k]['curv_min'] / (4 * 3.141592653589793 / 120), over_4pi_48=pa[k]['curv_min'] / (4 * 3.141592653589793 / 48))
                 for k in cand if res[k] != 1]
    print('candidates (one curvature class):', len(cand), '| all corners congruent:', len(cand) - len(cand_open), '| not explained by congruence:', cand_open)
    out = json.load(open(outp)); out['candidates'] = len(cand); out['candidates_not_congruent'] = cand_open; json.dump(out, open(outp, 'w'), indent=1, ensure_ascii=False)
    if len(pa) == len(recs) == len(res): print('FINAL ok')
