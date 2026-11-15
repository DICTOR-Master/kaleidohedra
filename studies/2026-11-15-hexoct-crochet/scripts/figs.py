#!/usr/bin/env python3
"""Figures for the crochet plan, all from exact geometry, plus two checks:
  (1) Narcissus net: unfolded from the 3D piece across shared edges; checked: every face keeps its true side lengths, no two faces overlap;
  (2) the two Narcissus of one h-layer tile, joined on their hexagons, form one convex solid with 12 faces (the twisted cube);
  fig/face-hexagon.png  one crocheted hexagon: rows of sc as bars, true outline on top;
  fig/net-narcissus.png the net, faces labelled with their crochet pattern;
  fig/block-4H.png      a 4H block (h c h c) of Narcissus and cubes in 3D, layers drawn apart.
Usage: python3 figs.py <keyed-hexoct scripts> <dicto-mark.png>"""
import os, sys, math, json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.geometry import Polygon as SPoly
HEX = os.path.abspath(sys.argv[1]); MARK = os.path.abspath(sys.argv[2]); here = os.getcwd(); sys.path.insert(0, HEX); os.chdir(HEX)
import tiles as T
from stackings import POS
os.chdir(here); os.makedirs('fig', exist_ok=True)
GOLD, PURPLE, INK = '#d4a020', '#7a5fb0', '#222222'
H = math.sqrt(2/3); s3 = math.sqrt(3)
def cart(p): return np.array([float(p[0]) + float(p[1])/2, float(p[1])*s3/2, float(p[2])*H])
pat = json.load(open('data/pattern.json')); fj = json.load(open('data/faces.json'))
def mark(fig):
    try: a = fig.add_axes([0.88, 0.01, 0.1, 0.1]); a.imshow(plt.imread(MARK)); a.axis('off')
    except Exception as e: print('mark missing', e)
def faces_of(X):
    h = ConvexHull(X); fs = {}
    for eq, s in zip(h.equations, h.simplices): fs.setdefault(tuple(np.round(eq, 7)), set()).update(s)
    out = []
    for k, idx in fs.items():
        n = np.array(k[:3]); idx = list(idx); c = X[idx].mean(0); u = X[idx[0]] - c; w = np.cross(n, u)
        out.append(sorted(idx, key=lambda i: math.atan2((X[i]-c) @ w, (X[i]-c) @ u)))
    return out
checks = {}
# ---------- (1) net of Narcissus ----------
X = np.array([(0,0,0),(0,1/s3,-H/2),(0,1/s3,0),(.5,-1/(2*s3),-H/2),(.5,-1/(2*s3),0),(.5,1/(2*s3),-H),(.5,s3/2,0),(1,0,0),(1,1/s3,-H/2),(1,1/s3,0)])   # paper #98
F = faces_of(X); nF = len(F); assert nF == 10, nF
def edges(f): return {frozenset((f[i], f[(i+1) % len(f)])) for i in range(len(f))}
root = next(i for i, f in enumerate(F) if len(f) == 6)
pos2 = {root: None}; placed = {}
def local2d(f):
    P = X[f]; c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n); u = (P[0] - c)/np.linalg.norm(P[0] - c); w = np.cross(n, u)
    return np.array([[(p - c) @ u, (p - c) @ w] for p in P])
placed[root] = dict(zip(F[root], local2d(F[root])))
order = [root]; parent = {}
while len(placed) < nF:
    for i in list(order):
        for j in range(nF):
            if j in placed: continue
            sh = edges(F[i]) & edges(F[j])
            if not sh: continue
            a, b = tuple(next(iter(sh))); L2 = local2d(F[j]); la, lb = L2[F[j].index(a)], L2[F[j].index(b)]
            pa, pb = placed[i][a], placed[i][b]
            best = None
            for refl in (1, -1):
                M = L2*np.array([1, refl]); ma, mb = M[F[j].index(a)], M[F[j].index(b)]
                ang = math.atan2(*(pb - pa)[::-1]) - math.atan2(*(mb - ma)[::-1]); R = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]])
                Q = (M - ma) @ R.T + pa
                cpar = np.mean(list(placed[i].values()), 0); e = pb - pa; nrm = np.array([-e[1], e[0]])
                if np.sign((Q.mean(0) - pa) @ nrm) != np.sign((cpar - pa) @ nrm): best = Q
            placed[j] = dict(zip(F[j], best)); parent[j] = i; order.append(j)
            break
polys = {i: np.array([placed[i][v] for v in F[i]]) for i in placed}
ok_len = all(abs(np.linalg.norm(polys[i][k] - polys[i][(k+1) % len(F[i])]) - np.linalg.norm(X[F[i][k]] - X[F[i][(k+1) % len(F[i])]])) < 1e-9 for i in polys for k in range(len(F[i])))
ov = max(SPoly(polys[i]).intersection(SPoly(polys[j])).area for i, j in itertools.combinations(polys, 2))
checks['net'] = {'faces': nF, 'true_side_lengths': bool(ok_len), 'largest_overlap_area': float(ov), 'no_overlap': bool(ov < 1e-9)}
L = pat['L_cm']; S = L*math.sqrt(2)   # a in cm: corners are in ball units a = 1
fig, ax = plt.subplots(figsize=(6.2, 6.2), dpi=200)
lab = {3: (f"triangle\n{pat['triangle']['first_row_sts']} sc × {pat['triangle']['rows']} rows", '#8fc7c0'),
       4: (f"square\n{pat['square']['sts']} sc × {pat['square']['rows']} rows", '#b9a6dc'),
       6: (f"hexagon\n{pat['hexagon']['bottom_sts']}→{pat['hexagon']['middle_sts']}→{pat['hexagon']['bottom_sts']} sc\n{pat['hexagon']['total_rows']} rows", '#ecc95c')}
for i, P in polys.items():
    t, c = lab[len(P)]; ax.add_patch(MPoly(P*S, closed=True, fc=c, ec=INK, lw=1.2))
    ax.text(*(P.mean(0)*S), t, ha='center', va='center', fontsize=7 if len(P) > 3 else 4.6)
allP = np.vstack(list(polys.values()))*S; ax.set_xlim(allP[:, 0].min() - 1, allP[:, 0].max() + 1); ax.set_ylim(allP[:, 1].min() - 1, allP[:, 1].max() + 1)
ax.set_aspect('equal'); ax.set_xlabel('cm (square side %.1f cm)' % L, fontsize=8); ax.tick_params(labelsize=7)
ax.set_title('Narcissus: net of its 10 crocheted faces (exact, to scale)', fontsize=10); mark(fig)
fig.savefig('fig/net-narcissus.png', bbox_inches='tight'); plt.close(fig)
# ---------- face diagram: one crocheted hexagon ----------
hx = pat['hexagon']; gs, gr = pat['gauge']['sts_per_10cm']/10, pat['gauge']['rows_per_10cm']/10
w = []; cur = hx['bottom_sts']
for r in range(1, hx['total_rows'] + 1):
    if r in hx['increase_rows']: cur += 2
    if r > hx['rows_each_half'] + 1 and (hx['total_rows'] + 2 - r) in hx['increase_rows']: cur -= 2
    w.append(cur)
checks['hexagon_rows'] = {'first': w[0], 'widest': max(w), 'last': w[-1], 'symmetric': w == w[::-1]}
fig, ax = plt.subplots(figsize=(5.2, 4.6), dpi=200)
for r, n in enumerate(w):
    x0 = -n/2/gs
    for k in range(n): ax.add_patch(plt.Rectangle((x0 + k/gs, r/gr), 1/gs, 1/gr, fc='#ecc95c' if (r % 2 == 0) else '#f3dc8e', ec='#9a7a20', lw=0.3))
t = L*math.sqrt(2/3); hexP = np.array([(t*math.cos(math.radians(60*k + 0)), t*math.sin(math.radians(60*k)) ) for k in range(6)])
hexP = np.array([[-t/2, 0], [t/2, 0], [t, t*s3/2], [t/2, t*s3], [-t/2, t*s3], [-t, t*s3/2]])
ax.add_patch(MPoly(hexP, closed=True, fill=False, ec=INK, lw=1.6))
for r in hx['increase_rows']: ax.text(t + 0.6, (r - 0.5)/gr, 'inc', fontsize=5, va='center')
ax.set_aspect('equal'); ax.set_xlim(-t - 1, t + 2); ax.set_ylim(-0.5, t*s3 + 0.5); ax.tick_params(labelsize=7)
ax.set_title(f"One crocheted hexagon: {hx['total_rows']} rows of sc, {w[0]} to {max(w)} to {w[-1]} stitches\n(boxes = stitches at the stated gauge; black = true regular hexagon, side {t:.2f} cm)", fontsize=8)
ax.set_xlabel('cm', fontsize=8); mark(fig); fig.savefig('fig/face-hexagon.png', bbox_inches='tight'); plt.close(fig)
# ---------- 3D: 4H block, and the twisted-cube check ----------
w4 = 'ABCB'; types = T.types(w4); pieces = []
for Lr in range(4):
    os.chdir(HEX); pcs, _ = T.tile(w4, Lr, Fr(3, 8)); os.chdir(here)
    ball = cart((*POS[w4[Lr]], Lr))
    for k, up, s_, P, J in pcs:
        X0 = np.unique(np.round(np.array([cart(p) for p in P]), 12), axis=0) + ball
        for i, j in ((0, 0), (1, 0), (0, 1), (1, 1)): pieces.append((Lr, X0 + cart((i, j, 0))))
hl = [X for Lr, X in pieces[:2] ] if types[0] == 'h' else None
pair = [X for Lr, X in pieces if Lr == 0][:2]
for A_, B_ in itertools.combinations([X for Lr, X in pieces if Lr == 0 and len(X) == 10], 2):
    ha = {tuple(np.round(p, 6)) for p in A_}; hb = {tuple(np.round(p, 6)) for p in B_}
    if len(ha & hb) == 6:
        U = np.vstack([A_, B_]); hU = ConvexHull(U)
        checks['h_tile_union'] = {'convex': bool(abs(hU.volume - ConvexHull(A_).volume - ConvexHull(B_).volume) < 1e-9), 'faces': len(faces_of(U)),
                                  'corners': int(len(np.unique(np.round(U[hU.vertices], 6), axis=0)))}
        break
fig = plt.figure(figsize=(6.4, 6.4), dpi=200); ax = fig.add_subplot(projection='3d')
light = np.array([.4, -.5, .8]); light /= np.linalg.norm(light); gap = 0.55
cen0 = np.mean([X.mean(0) for _, X in pieces], 0)
for Lr, X in pieces:
    Y = X - cen0 + np.array([0, 0, gap*Lr]); col = np.array(matplotlib.colors.to_rgb(GOLD if len(X) == 10 else PURPLE))
    for f in faces_of(X):
        P = Y[f]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        if n @ (P.mean(0) - Y.mean(0)) < 0: n = -n
        ax.add_collection3d(Poly3DCollection([P], facecolors=[np.clip(col*(0.55 + 0.45*max(0, n @ light)), 0, 1)], edgecolors=INK, linewidths=0.35))
for Lr in range(4): ax.text2D(0.0, 0.355 + 0.155*Lr, f"{w4[Lr]}  {types[Lr]} layer: {'Narcissus' if types[Lr] == 'h' else 'cubes'}", fontsize=7, transform=ax.transAxes)
r = 2.2; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-1.7, 2.2); ax.view_init(16, -60); ax.set_axis_off()
ax.set_title('A 4H block (layers ABCB, h c h c) in three dimensions,\nlayers drawn apart: gold Narcissus in h layers, purple cubes in c layers', fontsize=8)
fig.savefig('fig/_block-raw.png', bbox_inches='tight'); plt.close(fig)
img = plt.imread('fig/_block-raw.png'); ink = np.where(img[..., :3].min(2) < 0.97); y0, y1, x0, x1 = ink[0].min(), ink[0].max(), ink[1].min(), ink[1].max()
img = img[max(0, y0 - 10):y1 + 10, max(0, x0 - 10):x1 + 10]; hgt, wid = img.shape[:2]   # trim the empty margin of the 3D axes
fig = plt.figure(figsize=(wid/200, hgt/200 + 0.35), dpi=200); a = fig.add_axes([0, 0.35/(hgt/200 + 0.35), 1, hgt/200/(hgt/200 + 0.35)]); a.imshow(img); a.axis('off')
mark(fig); fig.savefig('fig/block-4H.png'); plt.close(fig); os.remove('fig/_block-raw.png')
json.dump(checks, open('data/fig-checks.json', 'w'), indent=1); print(json.dumps(checks, indent=1))
print('FINAL', 'OK' if checks['net']['no_overlap'] and checks['net']['true_side_lengths'] and checks['hexagon_rows']['symmetric'] else 'CHECK')
