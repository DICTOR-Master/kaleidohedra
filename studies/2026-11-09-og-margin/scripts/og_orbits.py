# og_orbits.py, DICTO 11 Nov 2026 ("run possibility 3"). Step A1 counted by symmetry classes. Under the full group I_h (120 elements)
# the faces of D_k fall into classes of size 12 (five-fold axes), 20 (three-fold), 30 (two-fold), 60 (on a mirror plane), 120 (generic).
# cut c = sum over dying classes of their sizes; c < n/2  <=>  60*(C120 - N120/2)*2 + 60*(C60 - N60/2) + axis terms < 0, so A1 is a
# class inequality. Per level: classes of each size, how many die, the cut share carried by each kind; the class form of A1 and its margin.
# Classes = orbits of the face normals under the 120 matrices of I_h (rotations and their negatives). Control: class sizes divide 120
# and add up to n; cut set = hull test (og_sweep convention).
# usage: python -u og_orbits.py <five-fold-octet dir> <kmax> <out.json>
import sys, os, json, numpy as np
here = os.path.dirname(os.path.abspath(__file__)); KM = int(sys.argv[2]); OUTJ = os.path.abspath(sys.argv[3])
sys.argv = ['x', sys.argv[1], '0', '/dev/null']; exec(open(os.path.join(here, 'og_sweep.py')).read().split('rows_out = []')[0])
from scipy.spatial import cKDTree
GH = np.concatenate([Gf, -Gf])
rows = []; ok = True; V = OGf; FF = faces(V)
for k in range(KM + 1):
    M, Dd, cor = FF
    W = symmetrise(M * Dd[:, None]); FN = faces(W); act = np.zeros(len(W), bool); act[FN[2]] = True; n = len(W)
    U = W / np.linalg.norm(W, axis=1)[:, None]; tr = cKDTree(U)
    lab = -np.ones(n, int); sizes = []; dies = []
    for i in range(n):
        if lab[i] >= 0: continue
        img = np.unique(tr.query(U[i] @ GH.transpose(0, 2, 1))[1]); lab[img] = len(sizes); sizes.append(len(img)); dies.append(bool(not act[i]))
        if len(set(act[img].tolist())) != 1: ok = False                    # a class must die or survive as a whole
    sizes = np.array(sizes); dies = np.array(dies)
    ok &= int(sizes.sum()) == n and all(120 % s == 0 for s in sizes)
    tab = {}
    for s in (12, 20, 30, 60, 120):
        m = sizes == s; tab[s] = (int(m.sum()), int((m & dies).sum()))
    c = int(sizes[dies].sum())
    # class form of A1: sum over classes of size*(die - 1/2) < 0 ; contributions per kind
    contrib = {s: float(s * (tab[s][1] - tab[s][0] / 2)) for s in tab}
    rows.append(dict(k=k, n=n, cut=c, frac=c / n, classes={s: tab[s] for s in tab}, contrib=contrib, margin=float(-sum(contrib.values()))))
    print(f'PROGRESS {(k + 1) / (KM + 1):.3f}', flush=True)
    print(f"k {k:2d}: n {n:6d} cut {c:5d} ({c / n:.3f}) | classes [all, dying]: 12:{tab[12]} 20:{tab[20]} 30:{tab[30]} 60:{tab[60]} 120:{tab[120]} "
          f"| share of 120-classes dying {tab[120][1] / max(1, tab[120][0]):.3f}, of 60-classes {tab[60][1] / max(1, tab[60][0]):.3f} | A1 margin n/2 - c = {n / 2 - c:.0f}", flush=True)
    V, FF = W, FN
json.dump(rows, open(OUTJ, 'w'), indent=1)
r1 = [r for r in rows if r['cut']]
print('max share of generic (120) classes dying:', max(r['classes'][120][1] / max(1, r['classes'][120][0]) for r in r1))
print('max share of mirror (60) classes dying:', max(r['classes'][60][1] / max(1, r['classes'][60][0]) for r in r1))
print('axis classes dying (12, 20, 30) by level:', [(r['k'], r['classes'][12][1], r['classes'][20][1], r['classes'][30][1]) for r in r1])
print('FINAL ok' if ok else 'FINAL FAIL: a class split between cut and surviving, or class sizes inconsistent')
