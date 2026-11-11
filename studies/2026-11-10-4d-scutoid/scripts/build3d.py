"""The 4D scutoid as a 3D build (DICTO 10 Nov: "lets do a 3D build, it's a lot easier for humans to understand"). Cut the stacking
(word ACABC, s = 1/5) with a vertical plane through an octahedral hole and the stacking axis; in the plane each hole's power cell is a
polygon (a 2D power diagram: weight w - distance² to the plane). Stand the polygons on λ (vertical): each hole becomes a 3D column
{(u, v, λ): linear inequalities}, a flat-faced polyhedron. Across the wall λ = -5s/8 = -1/8 neighbours change: a 3D scutoid whose height
is λ. Output: columns (vertices, faces) for the render, the neighbour pairs below / above the wall, FINAL."""
import sys, os, json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog
sys.path.insert(0, os.path.expanduser('~/work/b1-walls/swap')); sys.path.insert(0, os.path.expanduser('~/work/st57/scripts')); sys.path.insert(0, os.path.expanduser('~/work/splash'))
from validate import net_for, ROLE_OF
word, s = 'ACABC', Fr(1, 5); la, lb, wall = -0.155, -0.095, -0.125
spec = net_for(word, s); n = len(word); G = np.array(spec['G'], float); L = np.linalg.cholesky(G).T
sites = []
for a, b, c in itertools.product(range(-3, 4), range(-3, 4), range(-2, 3)):
    for k, (kind, p) in enumerate(spec['motif']):
        x = L @ (np.array([float(v) for v in p]) + [a, b, c]); sites.append((k, kind, x, (a, b, c)))
o = [x for k, kind, x, t in sites if k == 3 and t == (0, 0, 0)][0]           # octahedral hole 3 (the one that loses its 2-layer contacts)
up = np.array([0, 0, 1.0]); e1 = np.array([1.0, 0, 0])                       # the plane: through o, spanned by a horizontal axis and the vertical
P = np.array([x for _, _, x, _ in sites]); dpl = (P - o) @ np.cross(e1, up)   # distance of each site from the plane
U = (P - o) @ e1; Vv = (P - o) @ up
win = (np.abs(U) < 1.6) & (np.abs(Vv) < 1.2)                                  # the sites whose cells we build
def column(i):
    """3D polyhedron (u, v, λ) of site i's polygon over λ in [la, lb], window |u| <= 1.4, |v| <= 1.0"""
    rows = []; rj = []
    wi = lambda q: (1.0 if sites[q][1] == 'tet' else 0.0)                    # weight = λ·(1 if tet) ; power = |x - p|² - w ; in the plane add d²
    for j in range(len(sites)):
        if j == i or abs(dpl[j]) > 1.6: continue
        # |x-p_i|^2 - λ wi_i + d_i^2 <= |x-p_j|^2 - λ wi_j + d_j^2  with x = (u, v) in plane coords
        a_u = 2 * (U[j] - U[i]); a_v = 2 * (Vv[j] - Vv[i]); a_l = (wi(j) - wi(i)) * -1.0 * -1.0
        # move all to: a_u u + a_v v + a_l λ <= c
        c = (U[j] ** 2 + Vv[j] ** 2 + dpl[j] ** 2) - (U[i] ** 2 + Vv[i] ** 2 + dpl[i] ** 2)
        rows.append(np.r_[a_u, a_v, -(wi(j) - wi(i)) * -1.0, -c]); rj.append(j)
    for r in ([1, 0, 0, -1.4], [-1, 0, 0, -1.4], [0, 1, 0, -1.0], [0, -1, 0, -1.0], [0, 0, 1, -lb], [0, 0, -1, la]): rows.append(np.array(r, float))
    A = np.array(rows); M = A[:, :3]; bb = -A[:, 3]; nr = np.linalg.norm(M, axis=1)
    r = linprog(np.r_[0, 0, 0, -1], A_ub=np.c_[M, nr], b_ub=bb, bounds=[(None, None)] * 3 + [(0, None)], method='highs')
    if r.status != 0 or r.x[-1] < 1e-6: return None
    hs = HalfspaceIntersection(A, r.x[:3]); W = np.unique(np.round(hs.intersections, 9), axis=0); h = ConvexHull(W)
    faces = {}
    for simp, eq in zip(h.simplices, h.equations): faces.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    return W, [sorted(int(x) for x in f) for f in faces.values()], A, rj
cols = []
for i in np.where(win)[0]:
    R = column(i)
    if R is None: continue
    W, F, A, rj = R; cols.append({'i': int(i), 'kind': sites[i][1], 'layer': round(float(Vv[i]) / float(np.sqrt(float(G[2, 2]))) * 1, 3), 'V': W.tolist(), 'F': F})
# neighbours in the plane just below and just above the wall: two columns touch if they share a 2D face crossing λ
def touching(lv):
    pairs = set()
    for a, b in itertools.combinations(range(len(cols)), 2):
        Wa = np.array(cols[a]['V']); Wb = np.array(cols[b]['V'])
        sa = Wa[np.abs(Wa[:, 2] - lv) < 0.02]; sb = Wb[np.abs(Wb[:, 2] - lv) < 0.02]
        if len(sa) and len(sb) and np.min(np.linalg.norm(sa[:, None, :2] - sb[None, :, :2], axis=2)) < 1e-6: pairs.add((cols[a]['kind'], cols[b]['kind']))
    return pairs
print(f'{len(cols)} columns built (window around octahedral hole 3); λ from {la} to {lb}, wall {wall}')
json.dump({'cols': cols, 'la': la, 'lb': lb, 'wall': wall}, open('build3d.json', 'w'))
oct_center = [c for c in cols if c['i'] == int(np.where([(k == 3 and t == (0, 0, 0)) for k, _, _, t in sites])[0][0])]
print('centre column found:', bool(oct_center))
def nbrs(i, lv):
    W, F, A, rj = column(i); out = []
    for r, j in zip(A[:len(rj)], rj):
        # the edge of the polygon at height lv on row r: points of the column's slice on this line
        on = [w for w in W if abs(w[2] - lv) < 1e9]
        seg = []
        for f in F:
            pts = W[f]
            if np.all(np.abs(pts @ r[:3] + r[3]) < 1e-7) and pts[:, 2].min() < lv - 1e-9 and pts[:, 2].max() > lv + 1e-9: seg.append(j)
        if seg: out.append((sites[j][1], round(float(Vv[j]) / float(np.sqrt(G[2, 2]) / n), 2), round(float(U[j]), 2), int(j)))
    return sorted(set(out))
ci = oct_center[0]['i']
below, above = nbrs(ci, -0.14), nbrs(ci, -0.11)
print('centre octahedral column, neighbours (kind, layer offset, across) below the wall:', below)
print('                                                        above the wall:', above)
gained = sorted(set(above) - set(below)); print('lost:', sorted(set(below) - set(above)), ' gained:', gained)
d_ = json.load(open('build3d.json')); d_['centre'] = int(ci); d_['gained'] = [g[3] for g in gained]; json.dump(d_, open('build3d.json', 'w'))
print('FINAL ok' if cols and oct_center and set(below) != set(above) else 'FINAL FAIL: no neighbour change in this plane')
