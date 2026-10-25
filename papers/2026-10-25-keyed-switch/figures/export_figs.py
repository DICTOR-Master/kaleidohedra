# OBJs for the #56 figures (run on dicto-big-brother in a folder holding proof.py, app-solids.json, keyed_gyrated.py and the census).
# fig1: dodecahedron = cube + roofs, Dogstar = cube − roofs, one roof; fig2: the two walks' pieces (octet: Samson, Delilah, cube;
# twinned: Sonsam, Lahdeli, Ian Dury, rhombohedron, Blockhead).
import os, itertools, json, numpy as np, trimesh, manifold3d as m3
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
exec(open('proof.py').read().split('app = json.load')[0].replace("print(x); ", ""))
def save(man, fn):
    mesh = man.to_mesh(); V = np.array(mesh.vert_properties)[:, :3]; trimesh.Trimesh(V, np.array(mesh.tri_verts)).export(fn)
save(C, 'f1-cube.obj'); save(dodeca_built, 'f1-dodeca.obj'); save(dog_built, 'f1-dogstar.obj')
for i, r in enumerate(roofs_out): save(r, f'f1-roof{i}.obj')
import sys; sys.path.insert(0, 'census')
from networks import NETS
def cells(key, lam, picks):
    net = NETS[key]; G = np.array(net['G'], float); L = np.linalg.cholesky(G)
    T = [np.array(t, float) for t in net['T']]; M = [(k, np.array(p, float)) for k, p in net['motif']]
    sites = [(k, L.T @ (p + sum(c * t for c, t in zip(n, T)))) for n in itertools.product(range(-2, 3), repeat=3) for k, p in M]
    w = lambda k: float(net['w'][k][0]) + float(net['w'][k][1]) * lam
    res = {}
    for name, idx in picks:
        kp, p = M[idx][0], L.T @ M[idx][1]; H = []
        for k, q in sites:
            d = q - p
            if np.allclose(d, 0) or d @ d > 6: continue
            H.append(np.r_[2 * d, -(q @ q - p @ p - w(k) + w(kp))])
        H = np.array(H); A, b = H[:, :3], -H[:, 3]
        r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
        V = np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0); V -= V.mean(0)
        trimesh.Trimesh(V, ConvexHull(V).simplices).export(f'f2-{name}.obj')
lamD = float(sum([0.375, -(4 ** (1 / 3)) / 4]))
dl = NETS['delian']; ti = next(i for i, (k, p) in enumerate(dl['motif']) if k == 'tet'); oi = next(i for i, (k, p) in enumerate(dl['motif']) if k == 'oct')
cells('delian', lamD, [('samson', ti), ('delilah', oi)]); cells('delian', 0.374999, [('cube', ti)])
cells('hcpholes', 0.003266956983, [('sonsam', 2), ('lahdeli', 0)]); cells('hcpholes', 5 / 24, [('iandury', 2), ('rhombo', 0)]); cells('hcpholes', 0.374999, [('blockhead', 2)])
print('exported')
