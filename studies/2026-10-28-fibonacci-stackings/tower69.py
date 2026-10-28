# "Fibonacci tower" (DICTO 10-28): rock salt / NiAs at lam = 1/3 on the 16-layer Fibonacci approximant ABACBCACBABCACBC.
# Ball piece of every layer (at its true position A/B/C) and octahedral piece of every gap, each the exact power cell of its site
# (same net and weights as #64 / pieces67.py), coloured by kind; volumes checked against the exact pure values of the run.
import os, sys, json, itertools
import numpy as np
from fractions import Fraction as F
from scipy.spatial import HalfspaceIntersection, ConvexHull
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
POS = {'A': (0, 0), 'B': (1 / 3, 1 / 3), 'C': (2 / 3, 2 / 3)}
LAM = 1 / 3; WORD = 'ABACBCACBABCACBC'
a1 = np.array([1.0, 0, 0]); a2 = np.array([0.5, np.sqrt(3) / 2, 0]); h = np.sqrt(2 / 3)
n = len(WORD); cz = n * h
def types(w): return ['h' if w[k - 1] == w[(k + 1) % len(w)] else 'c' for k in range(len(w))]
T = types(WORD)
S = []
for k in range(n):
    X, Y = WORD[k], WORD[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
    for role, P, f, w in (('S', X, 0, LAM), ('C', X, .75, 0), ('O', Z, .5, LAM), ('Y', Y, .25, 0)):
        u, v = POS[P]; S.append((role, k, u * a1 + v * a2 + np.array([0, 0, (k + f) * h]), w))
def cell(i):
    p, wp = S[i][2], S[i][3]; H = []
    for j, (r, k, q, w) in enumerate(S):
        for da, db, dc in itertools.product(range(-2, 3), range(-2, 3), (-1, 0, 1)):
            qq = q + da * a1 + db * a2 + np.array([0, 0, dc * cz])
            if j == i and da == db == dc == 0: continue
            if np.linalg.norm(qq - p) > 2.2: continue
            H.append(np.r_[2 * (qq - p), -(qq @ qq - p @ p - w + wp)])
    hs = HalfspaceIntersection(np.array(H), p); return hs.intersections, ConvexHull(hs.intersections)
COL = {('S', 'c'): '#5b9bd5', ('S', 'h'): '#d4af37', ('O', 'cc'): '#9ec3e6', ('O', 'ch'): '#c77dab', ('O', 'hc'): '#a8507f'}
fig = plt.figure(figsize=(16, 7.2), facecolor='#0b0d12'); ax = fig.add_axes([0, 0, 1, 0.86], projection='3d'); ax.set_facecolor('#0b0d12'); ax.set_axis_off()
light = np.array([0.3, -0.6, 0.75]); light /= np.linalg.norm(light)
vols = {}; allp = []
for i, (role, k, p, w) in enumerate(S):
    if role not in ('S', 'O'): continue
    P0, hull = cell(i)
    kind = T[k] if role == 'S' else T[k] + T[(k + 1) % n]
    vols.setdefault((role, kind), set()).add(round(hull.volume, 9))
    faces = {}
    for simp, eq in zip(hull.simplices, hull.equations): faces.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    for shift in (np.zeros(3), a1, a2):
     P = P0 + shift
     allp.append(P[:, [2, 0, 1]])
     for key, idx in faces.items():
        idx = list(idx); pts = P[idx]; nrm = np.array(key[:3]); ctr = pts.mean(0)
        e1 = pts[0] - ctr; e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
        poly = pts[np.argsort(np.arctan2((pts - ctr) @ e2, (pts - ctr) @ e1))]
        poly = poly[:, [2, 0, 1]]                     # stacking axis drawn horizontally
        rgb = np.array(matplotlib.colors.to_rgb(COL[(role, kind)])) * (0.45 + 0.55 * max(0, nrm[[2, 0, 1]] @ light))
        ax.add_collection3d(Poly3DCollection([poly], facecolor=np.clip(rgb, 0, 1), edgecolor='#f0ead8', linewidths=0.35, alpha=0.98))
A = np.vstack(allp); lo, hi = A.min(0), A.max(0)
ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
ax.set_box_aspect(tuple(hi - lo), zoom=0.98); ax.view_init(20, -72)
fig.text(0.02, 0.93, 'A Fibonacci crystal: rock salt on the 16-layer Fibonacci stacking ABACBCACBABCACBC (λ = 1/3)', color='#e8e4d8', fontsize=15)
fig.text(0.02, 0.885, 'balls: cubic layer blue, hexagonal layer gold · octahedral atoms between layers: cubic–cubic pale blue, cubic–hexagonal and hexagonal–cubic rose · never hexagonal–hexagonal',
         color='#bdb8a8', fontsize=10.5)
fig.text(0.98, 0.03, 'DICTO', color='#d4af37', fontsize=18, ha='right', family='serif', weight='bold')
out = os.path.expanduser('~/kres-tmp/fig69'); os.makedirs(out, exist_ok=True)
fig.savefig(os.path.join(out, 'fibonacci-tower.png'), dpi=240, facecolor=fig.get_facecolor())
# check: kinds present, and each kind one volume; ball kinds against the run's pure pieces (halves: ball = pure piece of its own type)
ex = json.load(open(sys.argv[1])); wv = next(w for w in ex['windows'] if F(w['lo']) < F(1, 3) < F(w['hi']))
ev = lambda e: float(eval(e.replace('lam', '(F(1,3))').replace('/', '*F(1,1)/'), {'F': F}))
cc = ev(wv['roles']['S']['volumes']['cc']); hh = ev(wv['roles']['S']['volumes']['hh'])
print('kinds and volumes:', {k: sorted(v) for k, v in vols.items()})
print('ball c / h ratio computed', round(max(vols[('S', 'h')]) / max(vols[('S', 'c')]), 9), 'exact', round(hh / cc, 9))
print('layer types', ''.join(T), 'h share', T.count('h'), '/', n)
