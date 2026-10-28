# Figure of #67: the pieces of rock salt (cubic stacking ABC, NaCl) and nickel arsenide (hexagonal stacking AB, NiAs) at weight
# lam = 1/3, as solids. Same net as the run (#64 rock salt: pyro_walk.py net with kinds ball S atom, C hole, O atom, Y hole; ball
# spacing 1, layer spacing sqrt(2/3); power distance |x - p|^2 - w, atoms w = lam, holes 0). Each piece is the power cell of one site,
# computed from its neighbours (periodic images) as an intersection of half-spaces; its volume is checked against the exact census
# volumes of the run (out/rocksalt_mix.json, ratio pure h / pure c and the shares within a stacking).
import os, sys, json, itertools
import numpy as np
from fractions import Fraction as F
from scipy.spatial import HalfspaceIntersection, ConvexHull
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
POS = {'A': (0, 0), 'B': (1 / 3, 1 / 3), 'C': (2 / 3, 2 / 3)}
LAM = 1 / 3
a1 = np.array([1.0, 0, 0]); a2 = np.array([0.5, np.sqrt(3) / 2, 0]); h = np.sqrt(2 / 3)
def sites(word):
    n = len(word); S = []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
        for role, P, f, w in (('S', X, 0, LAM), ('C', X, .75, 0), ('O', Z, .5, LAM), ('Y', Y, .25, 0)):
            u, v = POS[P]; S.append((role, k, u * a1 + v * a2 + np.array([0, 0, (k + f) * h]), w))
    return S, n * h
def cell(word, role, gap=0):
    S, c = sites(word)
    i = next(j for j, s in enumerate(S) if s[0] == role and s[1] == gap); p, wp = S[i][2], S[i][3]
    H = []
    for j, (r, k, q, w) in enumerate(S):
        for da, db, dc in itertools.product(range(-2, 3), range(-2, 3), range(-2, 3)):
            qq = q + da * a1 + db * a2 + np.array([0, 0, dc * c])
            if j == i and da == db == dc == 0: continue
            if np.linalg.norm(qq - p) > 2.2: continue
            # |x-p|^2 - wp <= |x-q|^2 - w  <=>  2(q-p).x <= |q|^2 - |p|^2 - w + wp
            nrm = 2 * (qq - p); off = qq @ qq - p @ p - w + wp
            H.append(np.r_[nrm, -off])
    hs = HalfspaceIntersection(np.array(H), p)
    hull = ConvexHull(hs.intersections)
    return hs.intersections - p, hull
ROLES = [('S', 'ball (Na / Ni)'), ('O', 'octahedral atom (Cl / As)'), ('C', 'tetrahedral hole')]
vols = {}
fig = plt.figure(figsize=(15, 10.5), facecolor='#0b0d12')
for r, (word, lab, col) in enumerate([('ABC', 'cubic stacking ABC: rock salt (NaCl)', '#5b9bd5'), ('AB', 'hexagonal stacking AB: nickel arsenide (NiAs)', '#d4af37')]):
    for c_, (role, name) in enumerate(ROLES):
        P, hull = cell(word, role); vols[(word, role)] = hull.volume
        ax = fig.add_subplot(2, 3, r * 3 + c_ + 1, projection='3d'); ax.set_facecolor('#0b0d12'); ax.set_axis_off()
        light = np.array([0.4, -0.5, 0.8]); light /= np.linalg.norm(light)
        # merge coplanar triangles into faces for drawing edges
        faces = {}
        for simp, eq in zip(hull.simplices, hull.equations):
            key = tuple(np.round(eq, 6)); faces.setdefault(key, set()).update(simp)
        for key, idx in faces.items():
            idx = list(idx); pts = P[idx]; nrm = np.array(key[:3]); ctr = pts.mean(0)
            e1 = pts[0] - ctr; e1 /= np.linalg.norm(e1); e2 = np.cross(nrm, e1)
            order = np.argsort(np.arctan2((pts - ctr) @ e2, (pts - ctr) @ e1)); poly = pts[order]
            shade = 0.45 + 0.55 * max(0, nrm @ light)
            rgb = np.array(matplotlib.colors.to_rgb(col)) * shade
            ax.add_collection3d(Poly3DCollection([poly], facecolor=np.clip(rgb, 0, 1), edgecolor='#f0ead8', linewidths=0.7, alpha=0.97))
        m = np.abs(P).max() * 1.05
        ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_zlim(-m, m); ax.set_box_aspect((1, 1, 1)); ax.view_init(18, 30)
        ax.set_title(f'{name}\n{len(faces)} faces', color='#e8e4d8', fontsize=12)
    fig.text(0.02, 0.73 - r * 0.47, lab, color=col, fontsize=14, rotation=90, va='center')
fig.suptitle('The pieces of rock salt and nickel arsenide (weight λ = 1/3): the same kinds of piece, cubic and hexagonal', color='#e8e4d8', fontsize=16, y=0.97)
fig.text(0.5, 0.015, 'not to scale: each piece fills its panel; the tetrahedral holes are about a thousandth of the others', color='#9a9a9a', fontsize=12, ha='center')
fig.text(0.98, 0.02, 'DICTO', color='#d4af37', fontsize=18, ha='right', family='serif', weight='bold')
plt.subplots_adjust(left=0.05, right=0.98, top=0.9, bottom=0.03, wspace=0.0, hspace=0.12)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures'); os.makedirs(out, exist_ok=True)
fig.savefig(os.path.join(out, 'pieces-rocksalt.png'), dpi=110, facecolor=fig.get_facecolor())
# check against the exact run: ratios hh/cc per role and share of each role within ABC
ex = json.load(open(sys.argv[1]))
w = next(w for w in ex['windows'] if F(w['lo']) < F(1, 3) < F(w['hi']))
ev = lambda e: float(eval(e.replace('lam', '(F(1,3))').replace('/', '*F(1,1)/'), {'F': F}))
for role, _ in ROLES:
    V = {k: ev(e) for k, e in w['roles'][role]['volumes'].items()}
    print(role, 'computed hh/cc', round(vols[('AB', role)] / vols[('ABC', role)], 9), 'exact', round(V['hh'] / V['cc'], 9))
tot = sum(vols[('ABC', r)] for r in ('S', 'O')) + 2 * vols[('ABC', 'C')]
print('ABC shares S, O, C:', [round(vols[('ABC', r)] / tot, 9) for r in ('S', 'O', 'C')])
EX = {r: ev(w['roles'][r]['volumes']['cc']) for r in ('S', 'O', 'C')}; T = EX['S'] + EX['O'] + 2 * EX['C']
print('exact shares       :', [round(EX[r] / T, 9) for r in ('S', 'O', 'C')])
