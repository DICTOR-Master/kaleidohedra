# Step 16 (DICTO: "combine the limb crossing with the tip ring" + "and five-fold symmetry"). Exploratory, float.
# At one square-face centre: the two crossing limbs (step 7/8, through the four facing free hexagons) and the four trimmed tips
# (step 15). Overlaps, union volume, which golden-rhombus faces stay outside; edges and faces of the junction along 5-fold axes.
# Five-fold beyond one copy: a lattice cannot carry it; the only icosahedral way to join by hexagons is all 20 around one copy.
import json, itertools, numpy as np, sys
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
sys.path.insert(0, '../_lib'); import geomcheck as gc
N = json.load(open('data/network.json')); O = np.array(N['ocd']); T = np.array(N['T']); r = np.linalg.norm(O, axis=1)
ax = gc.icosa_axes(O[np.abs(r - r.max()) < 1e-9])
Tp = json.load(open('data/tips-meet.json')); tips = [np.array(P) for P in Tp['trimmed']]; site = np.array(Tp['site'])
classes = [np.array(c['P']) for c in json.load(open('data/limb-sets.json'))['classes']]
cells = []
for m in itertools.product(range(-2, 3), repeat=4):
    p = sum(k * t for k, t in zip(m, T))
    if np.linalg.norm(p) < 2.6 and not any(np.allclose(p, c) for c in cells): cells.append(p)
def inter(Ps):
    H = np.vstack([ConvexHull(P).equations for P in Ps]); nrm = np.linalg.norm(H[:, :3], axis=1)
    rr = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if rr.status != 0 or rr.x[3] < 1e-9: return None
    return np.unique(np.round(HalfspaceIntersection(H, rr.x[:3]).intersections, 10), axis=0)
vol = lambda X: 0.0 if X is None else ConvexHull(X).volume
# the limbs through this junction: translates of the limb classes whose middle is near the site
limbs = []
for P in classes:
    for c in cells:
        Q = P + c
        if np.linalg.norm(Q.mean(0) - site) < 0.12 and not any(np.allclose(np.sort(Q, 0), np.sort(L, 0)) for L in limbs): limbs.append(Q)
parts = limbs + tips; kind = ['limb'] * len(limbs) + ['tip'] * len(tips)
# union volume by inclusion-exclusion over all nonempty intersections
U = 0.0
for k in range(1, len(parts) + 1):
    for sub in itertools.combinations(range(len(parts)), k):
        U += (-1) ** (k + 1) * vol(inter([parts[i] for i in sub]))
inside = [vol(inter([t, L])) / vol(inter([t])) for t in tips for L in limbs]
out = [f'junction: {len(limbs)} limbs crossing and {len(tips)} tips; limb {vol(inter([limbs[0]])):.6f} each, tip {vol(inter([tips[0]])):.6f} each',
       f'each tip lies inside a limb by (fractions over the tip x limb pairs): {[round(x, 3) for x in inside]}',
       f'union of limbs and tips {U:.6f}; limbs alone {vol(inter([limbs[0]])) * 2 - vol(inter(limbs)):.6f}; the tips add {U - (vol(inter([limbs[0]])) * 2 - vol(inter(limbs))):.6f}']
# five-fold: edges of the crossing zone, the tips and the limbs along 5-fold axes
def edges_on5(P):
    h = ConvexHull(P); E = {tuple(sorted(e)) for s in h.simplices for e in itertools.combinations(s, 2)}
    dirs = [(P[a] - P[b]) / np.linalg.norm(P[a] - P[b]) for a, b in E if np.linalg.norm(P[a] - P[b]) > 1e-9]
    return sum(np.max(np.abs(ax['5'] @ d)) > 1 - 1e-7 for d in dirs), len(dirs)
Z = inter(limbs)
for name, P in [('crossing zone', Z), ('a limb', limbs[0]), ('a trimmed tip', tips[0])]:
    k5, kt = edges_on5(P); out.append(f'{name}: {k5} of {kt} hull edges (incl. diagonals of faces) along five-fold axes')
# icosahedral cluster: copies joined on all 20 hexagons of a central copy (the only icosahedral hexagon joins)
pl = []
for e in ConvexHull(O).equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
hexn = [e for e in pl if sum(np.abs(O @ e[:3] + e[3]) < 1e-7) == 6]
shell = [2 * (-e[3]) * e[:3] / np.linalg.norm(e[:3]) ** 2 for e in hexn]
EO = ConvexHull(O).equations; sh = lambda c: EO - np.c_[np.zeros((len(EO), 3)), EO[:, :3] @ c]
clash = sum(1 for a, b in itertools.combinations(range(20), 2) if inter([O + shell[a], O + shell[b]]) is not None)
out.append(f'icosahedral cluster (copies on all 20 hexagons of one copy): {clash} of 190 neighbour pairs collide' + (' -> five-fold symmetry cannot extend past one copy by hexagon joins' if clash else ''))
print('\n'.join(out)); open('data/combine.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'limbs': [L.tolist() for L in limbs], 'tips': [t.tolist() for t in tips], 'zone': Z.tolist(), 'site': site.tolist()}, open('data/combine.json', 'w'))
