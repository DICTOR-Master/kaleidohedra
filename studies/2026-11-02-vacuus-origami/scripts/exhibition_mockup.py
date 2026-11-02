# Exhibition mock-up of the slot-together (Disc) Vacuus pieces (DICTO): which solids have a Vacuus made of whole flat discs
# through O (every fin lies in a plane whose fins close all the way round O), then a small room with those pieces at
# car-transport size (largest disc <= 0.9 m wide... scaled so every piece is 1.27 m across) and a 1.7 m visitor for scale.
# Usage: exhibition_mockup.py <star-cores scripts dir> <out.png>
import sys, os, numpy as np
from scipy.spatial import ConvexHull
SC, OUTP = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); sys.path.insert(0, SC)
sys.argv = [sys.argv[0], '.', os.path.dirname(OUTP), os.path.expanduser('~/kres-tmp/book/dicto-logo.png')]
import figs_paper_a as A
import matplotlib.pyplot as plt

phi = (1 + 5 ** .5) / 2
def perms(v):  # even (cyclic) permutations with all sign changes
    out = set()
    for c in (v, v[1:] + v[:1], v[2:] + v[:2]):
        for s in np.ndindex(2, 2, 2):
            out.add(tuple(round(c[i] * (-1) ** s[i], 9) for i in range(3)))
    return np.array(sorted(out))
SOLIDS = {
    'Octahedron': perms([1.0, 0, 0]), 'Cube': perms([1.0, 1, 1]), 'Cuboctahedron': perms([1.0, 1, 0]),
    'Icosidodecahedron': np.vstack([perms([phi, 0, 0]), perms([0.5, phi / 2, phi ** 2 / 2])]),
    'Rhombic dodecahedron': np.vstack([perms([1.0, 1, 1]), perms([2.0, 0, 0])]),
    'Icosahedron': perms([0, 1.0, phi]), 'Dodecahedron': np.vstack([perms([1.0, 1, 1]), perms([0, 1 / phi, phi])]),
}
def edges(P):
    h = ConvexHull(P); E = set()
    for Q, n in A.hull_faces(P):
        idx = [int(np.argmin(np.linalg.norm(P - q, axis=1))) for q in Q]
        for i in range(len(idx)): E.add(tuple(sorted((idx[i], idx[(i + 1) % len(idx)]))))
    return sorted(E)
def discs(P):
    """group the fins (O, u, v) by their plane; a plane is a disc when its edges form one closed polygon round O"""
    planes = {}
    for i, j in edges(P):
        n = np.cross(P[i], P[j]); n /= np.linalg.norm(n); k = np.argmax(np.abs(n)); n = n * np.sign(n[k])
        key = tuple(np.round(n, 6)); planes.setdefault(key, []).append((i, j))
    out = []
    for key, E in planes.items():
        deg = {}
        for i, j in E: deg[i] = deg.get(i, 0) + 1; deg[j] = deg.get(j, 0) + 1
        closed = len(E) >= 3 and all(d == 2 for d in deg.values())
        out.append((np.array(key), E, closed))
    return out

report, show = [], []
for nm, P in SOLIDS.items():
    D = discs(P); ok = all(c for _, _, c in D)
    report.append(f'{nm}: {len(D)} planes, fins per plane {sorted({len(E) for _, E, _ in D})}, all closed discs: {ok}')
    if ok: show.append((nm, P, D))
print('\n'.join(report))

# ---- room: floor 5 x 4 m, back and left walls 2.6 m; pieces 1.27 m across, standing on a face (lowest point at the floor)
M = A.rot(16, -30); S = A.Scene(M)
W, Dp, H = 5.0, 4.0, 2.6
def quad(P, col, layer): S.items.append((layer, 0, (np.array(P) @ M.T)[:, :2], col, (0.55, 0.57, 0.62, 1), 0.3))
quad([[0, 0, 0], [W, 0, 0], [W, Dp, 0], [0, Dp, 0]], (0.93, 0.92, 0.89, 1), -3)
quad([[0, Dp, 0], [W, Dp, 0], [W, Dp, H], [0, Dp, H]], (0.97, 0.97, 0.96, 1), -2)
quad([[0, 0, 0], [0, Dp, 0], [0, Dp, H], [0, 0, H]], (0.95, 0.95, 0.94, 1), -2)
spots = [(1.0, 2.6), (2.6, 1.6), (4.1, 2.5)]
LABELS = []
COLS = [A.GOLD, A.VIOLET, A.TEAL, '#d4823a', '#5b8ed6', '#c4a6ee']
for (nm, P, D), (x, y) in zip(show, spots):
    P = P / np.linalg.norm(P, axis=1).max() * 0.635                     # 1.27 m across
    faces = A.hull_faces(P); Q, n = min(faces, key=lambda f: -len(f[0]) * 0 + f[1][2])   # rest on the face whose normal points most down
    zax = -n / np.linalg.norm(n); xax = np.cross([0.3, 0.5, 0.8], zax); xax /= np.linalg.norm(xax); yax = np.cross(zax, xax)
    Rr = np.array([xax, yax, zax]); Pw = P @ Rr.T; Pw[:, 2] -= Pw[:, 2].min(); Pw[:, :2] += [x, y]; O = np.array([x, y, -(P @ Rr.T)[:, 2].min()])
    TV, TF, TC = [], [], []
    for k, (nrm, E, _) in enumerate(D):
        for i, j in E:
            for tri in ((O, Pw[i], Pw[j]), (O, Pw[j], Pw[i])):                # both sides of each fin
                b = len(TV); TV += list(tri); TF.append([b, b + 1, b + 2]); TC.append(COLS[k % len(COLS)])
    S.tris(np.array(TV), TF, TC)
    LABELS.append(((np.array([[x, y, 0]]) @ M.T)[0, :2], nm))
# visitor: a simple 1.7 m silhouette (two quads, front and side)
vx, vy = 4.5, 0.6
for P in ([[vx - .22, vy, 0], [vx + .22, vy, 0], [vx + .22, vy, 1.45], [vx - .22, vy, 1.45]],
          [[vx - .11, vy, 1.45], [vx + .11, vy, 1.45], [vx + .11, vy, 1.7], [vx - .11, vy, 1.7]]):
    quad(P, (0.45, 0.47, 0.52, 1), 4)
fig = plt.figure(figsize=(10, 6.6)); ax = fig.add_axes([0, 0.05, 1, 0.88])
S.draw(ax, 4.2)
c = (np.array([[W / 2, Dp / 2, 0.8]]) @ M.T)[0, :2]; ax.set_xlim(c[0] - 3.6, c[0] + 3.6); ax.set_ylim(c[1] - 2.2, c[1] + 2.5)
for p, nm in LABELS: ax.text(p[0], p[1] - 0.1, nm, ha='center', va='top', fontsize=9)
fig.text(0.5, 0.95, 'DICTO Vacuus: slot-together pieces in a 5 m x 4 m room (each 1.27 m across; visitor 1.7 m)', ha='center', fontsize=11, weight='bold')
fig.text(0.5, 0.045, 'Whole discs through the centre (slot-together possible): ' + ', '.join(r.split(':')[0] for r in report if 'True' in r), ha='center', fontsize=8.5)
fig.text(0.5, 0.02, 'Not discs (fins meet only at the centre): ' + ', '.join(r.split(':')[0] for r in report if 'True' not in r), ha='center', fontsize=8.5)
A.mark(fig); fig.savefig(OUTP, dpi=200, facecolor='white'); print('written', OUTP)
