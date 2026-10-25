# Keyed gyrated pair (DICTO 2026-10-25, "do that"): the gyrated Delian pair at its equal-volume point (hcp holes, lam = root of
# 1536 l^3 + 5184 l^2 - 3384 l + 11, ~0.003266957) keyed as the keyed pairs were (study 2026-10-25-keyed-choices): a cap moved
# through every shared tet|oct face, cap = cone over the face shrunk by K toward its centre.
#   A: apex at the giving piece's centre (deepest key); B: a tooth, height sqrt(2/3) x mean edge of the shrunk face.
# Both directions (tet -> oct, oct -> tet). Checks: total volume per cell set conserved, pieces watertight; whether the 9-sided
# face (and which neighbour it faces) survives. Floats (manifold3d); output keyed_gyrated.txt, keyed_gyrated.png.
import sys, itertools, numpy as np, manifold3d as m3, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog
sys.path.insert(0, '../2026-10-25-relay-census/scripts')
from networks import NETS
import os; LAM = 0.003266957; K = float(os.environ.get("K", "0.8"))
net = NETS['hcpholes']; G = np.array(net['G'], float); L = np.linalg.cholesky(G)
T = [np.array(t, float) for t in net['T']]; M = [(k, np.array(p, float)) for k, p in net['motif']]
sites = [(k, L.T @ (p + sum(c * t for c, t in zip(n, T)))) for n in itertools.product(range(-2, 3), repeat=3) for k, p in M]
w = lambda k: LAM if k == 'tet' else 0.0
def cell(p, kp):
    H, nb = [], []
    for k, q in sites:
        d = q - p
        if np.allclose(d, 0) or d @ d > 6: continue
        H.append(np.r_[2 * d, -(q @ q - p @ p - w(k) + w(kp))]); nb.append((k, q))
    H = np.array(H); A, b = H[:, :3], -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    V = np.unique(np.round(HalfspaceIntersection(H, r.x[:3]).intersections, 9), axis=0)
    faces = []
    for h, (k, q) in zip(H, nb):
        on = [v for v in V if abs(h[:3] @ v + h[3]) < 1e-7]
        if len(on) >= 3:
            n = h[:3] / np.linalg.norm(h[:3]); c = np.mean(on, 0); u = on[0] - c; u /= np.linalg.norm(u); v2 = np.cross(n, u)
            on = sorted(on, key=lambda x: np.arctan2((x - c) @ v2, (x - c) @ u)); faces.append(dict(P=np.array(on), n=n, k=k, q=q))
    return V, faces
hull = lambda P: m3.Manifold.hull_points([list(map(float, x)) for x in P])
tetc = next(q for k, q in sites if k == 'tet' and np.allclose(q, L.T @ M[2][1]))
octc = next(q for k, q in sites if k == 'oct' and np.allclose(q, L.T @ M[0][1]))
Vt, Ft = cell(tetc, 'tet'); Vo, Fo = cell(octc, 'oct')
out = []
def say(s): print(s); out.append(s)
say(f"lam = {LAM}: tet piece {len(Vt)} corners, faces " + str(sorted(len(f['P']) for f in Ft)) + f", volume {ConvexHull(Vt).volume:.6f}")
say(f"               oct piece {len(Vo)} corners, faces " + str(sorted(len(f['P']) for f in Fo)) + f", volume {ConvexHull(Vo).volume:.6f}")
for f in Ft: 
    if len(f['P']) >= 6: say(f"  tet face with {len(f['P'])} sides faces a {f['k']} neighbour")
for f in Fo:
    if len(f['P']) >= 5: say(f"  oct face with {len(f['P'])} sides faces a {f['k']} neighbour")
def capfor(F, giver_c, opt, sign):
    c = F['P'].mean(0); S = c + K * (F['P'] - c)
    h = np.sqrt(2 / 3) * np.mean([np.linalg.norm(S[i] - S[(i + 1) % len(S)]) for i in range(len(S))])
    apex = giver_c if opt == 'A' else c + sign * h * F['n']
    if sign < 0: S = S + 1e-4 * F['n']   # a removed key's base is pushed just past the face so it cuts through it (not a hollow inside)
    return hull(np.vstack([S, [apex]]))
res = {}
for direction in ('tet->oct', 'oct->tet'):
    for opt in ('A', 'B'):
        tp, op = hull(Vt), hull(Vo)
        for F in Ft:   # faces of the tet piece shared with oct neighbours (n points out of the tet piece)
            if F['k'] != 'oct': continue
            if direction == 'tet->oct': tp = tp - capfor(F, tetc, opt, -1)
            else: tp = tp + capfor(F, F['q'], opt, +1)
        for F in Fo:   # faces of the oct piece shared with tet neighbours
            if F['k'] != 'tet': continue
            if direction == 'tet->oct': op = op + capfor(F, F['q'], opt, +1)
            else: op = op - capfor(F, octc, opt, -1)
        vt, vo = tp.volume(), op.volume(); tot0 = 4 * ConvexHull(Vt).volume + 2 * ConvexHull(Vo).volume
        ok = abs(4 * vt + 2 * vo - tot0) < 1e-6
        say(f"{direction} {opt}: tet piece vol {vt:.6f} genus {tp.genus()}, oct piece vol {vo:.6f} genus {op.genus()}, "
            f"total conserved {ok} (4 tet + 2 oct = {4*vt+2*vo:.6f} vs {tot0:.6f}); watertight {tp.status()==m3.Error.NoError and op.status()==m3.Error.NoError}")
        res[(direction, opt)] = (tp, op)
fig = plt.figure(figsize=(16, 8))
for i, ((d, o), (tp, op)) in enumerate(res.items()):
    for j, (man, col, nm) in enumerate([(tp, '#d4a72c', 'tet piece'), (op, '#8a6bd6', 'oct piece')]):
        ax = fig.add_subplot(2, 4, 1 + i * 2 + j if i < 2 else 1 + i * 2 + j, projection='3d') if False else fig.add_subplot(2, 4, i * 2 + j + 1, projection='3d')
        mesh = man.to_mesh(); P = np.array(mesh.vert_properties)[:, :3]; Tr = np.array(mesh.tri_verts)
        ax.add_collection3d(Poly3DCollection(P[Tr], facecolor=col, edgecolor='#00000022', linewidth=0.2, alpha=1))
        c = P.mean(0); r = np.abs(P - c).max(); ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(c[2]-r, c[2]+r)
        ax.set_box_aspect((1, 1, 1)); ax.view_init(22, 35); ax.axis('off'); ax.set_title(f"{d} {o}: {nm}", fontsize=10)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=8, color='#b08d2a')
plt.tight_layout(); plt.savefig(f'keyed_gyrated_K{K}.png', dpi=110)
open(f'keyed_gyrated_K{K}.txt', 'w').write('\n'.join(out) + '\n')
