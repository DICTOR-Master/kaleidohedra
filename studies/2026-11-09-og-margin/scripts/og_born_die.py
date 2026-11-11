# og_born_die.py, DICTO 11-11 ("or the number of births to deaths being exchanged"): births at one hop vs deaths at the next.
# Faces of D_k: BORN at hop k-1 (normal not a face normal of D_{k-1}) or SURVIVING. At hop k a face of D_k is CUT when its foot point
# is not a corner of D_{k+1}. Test: are the faces cut at hop k only ones born at hop k-1? counts born_k, cut_k, cut among born / surviving.
# usage: python -u og_born_die.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json
import numpy as np
from scipy.spatial import cKDTree
OUT = os.path.abspath(sys.argv[3]); here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'og_sweep.py')).read().split('def death(')[0]
exec(src)
rows = []; ok = True
V = OGf; FF = faces(V); prevM = None
for k in range(KMAX + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None])                       # foot points, in the order of the merged face list? map by direction
    FN = faces(W); M2, D2, cor2 = FN
    act = np.zeros(len(W), bool); act[cor2] = True
    U = W / np.linalg.norm(W, axis=1)[:, None]            # face normal of each candidate
    born = np.ones(len(W), bool)
    if prevM is not None:
        d, _ = cKDTree(prevM).query(U); born = d > 1e-7
    cut = ~act
    nb, nc = int(born.sum()), int(cut.sum()); cb, cs = int((cut & born).sum()), int((cut & ~born).sum())
    print(f'PROGRESS {(k + 1) / (KMAX + 1):.3f}', flush=True)
    print(f'k {k:3d}: faces {len(W):6d} | born at hop {k - 1} {nb:6d} surviving {len(W) - nb:6d} | cut at hop {k} {nc:6d}: born {cb:6d}, surviving {cs:6d} | cut/born {nc / nb if nb else 0:.3f}', flush=True)
    rows.append(dict(k=k, faces=len(W), born=nb, cut=nc, cut_born=cb, cut_surv=cs)); prevM = U
    V, FF = W, FN
json.dump(rows, open(OUT, 'w'))
print('only born faces are ever cut (k >= 1):', all(r['cut_surv'] == 0 for r in rows[1:]))
print('cut <= born at every level:', all(r['cut'] <= r['born'] for r in rows[1:]))
KNOWN = {5: 60, 6: 60, 7: 90, 8: 0, 9: 252, 10: 192, 11: 132, 12: 252, 13: 192, 14: 552}   # cut counts of cut_lemma / og_sweep
ctrl = all(r['cut'] == KNOWN[r['k']] for r in rows if r['k'] in KNOWN) and all(r['cut_born'] + r['cut_surv'] == r['cut'] for r in rows)
print('FINAL ok' if ctrl else 'FINAL FAIL: cut counts differ from cut_lemma / og_sweep')
