# Figure for paper #87 (DICTO Vacuus Solids), Section 8: the Star step (DICTO proposed), each centre pyramid mirrored in
# its own face (centre rule t = 2 of #78). Top row the five Platonic solids, bottom row DICTO solids of the #87 plates.
# Checks Proposition 2 (a): volume of the Star = 2 x volume of the solid. Same renderer as figs_paper_a.py (imported).
# Usage: figs_vacuus_star.py <dataset dir> <out dir> <logo png>
import json, os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figs_paper_a as A                     # sets the dataset dir as cwd, OUT and the logo from sys.argv
from star_core import faces_info, polyvol, load
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

phi = (1 + 5 ** .5) / 2
def platonic(name):
    if name == 'tetrahedron': P = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
    elif name == 'cube': P = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float)
    elif name == 'octahedron': P = np.vstack([np.eye(3), -np.eye(3)])
    elif name == 'icosahedron': P = np.array([p for a in (-1, 1) for b in (-1, 1) for p in ([0, a, b * phi], [a, b * phi, 0], [b * phi, 0, a])], float)
    else: P = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)] +
                       [p for a in (-1, 1) for b in (-1, 1) for p in ([0, a / phi, b * phi], [a / phi, b * phi, 0], [b * phi, 0, a / phi])], float)
    return [(Q, n, float(n @ Q.mean(0))) for Q, n in A.hull_faces(P)], ConvexHull(P).volume

def dicto(fn):
    _, V, F = load('solids/' + fn); V = V - V.mean(0)
    return [(V[f], n, d) for f, n, d in faces_info(V, F)], polyvol(V, F)

def star(faces):
    """turned-out centre pyramids: tip of face (n, d) at 2 d n, the mirror image of O in the face plane"""
    return [(np.vstack([Q, 2 * d * n]), Q, d) for Q, n, d in faces]

COLS = [A.VIOLET, A.TEAL, A.GOLD]
ROWS = [[('dodecahedron', 'Dodecahedron', '2δ = 233.13°'), ('icosahedron', 'Icosahedron', '2δ = 276.38°'), ('cube', 'Cube', '2δ = 180°: rhombic dodecahedron'),
         ('tetrahedron', 'Tetrahedron', '2δ = 141.06°'), ('octahedron', 'Octahedron', '2δ = 218.94°')],   # DICTO order D·I·C·T·O
        [('dicto-shadow-17.json', 'Kagemusha (D86)', ''), ('dicto-lion.json', 'Lion (D87)', ''), ('dicto-ogdoecontahedron.json', 'OG (D28)', ''),
         ('dicto-cube-pearl.json', 'Cube Pearl', ''), ('dicto-golden-clasp.json', 'Golden Clasp', '')]]

fig, axs = plt.subplots(2, 5, figsize=(10, 4.6), gridspec_kw=dict(wspace=0.02, hspace=0.18)); M = A.rot(*A.VIEW); info = []
for r, row in enumerate(ROWS):
    for ax, (key, nm, sub) in zip(axs[r], row):
        faces, VP = platonic(key) if r == 0 else dicto(key)
        sp = star(faces)
        # colour by face class (vertex count, distance from O), largest class first
        cls = sorted({(len(Q), round(d, 6)) for _, Q, d in sp}, key=lambda c: -sum(1 for _, Q, d in sp if (len(Q), round(d, 6)) == c))
        S = A.Scene(M)
        # one surface: the side triangles of every turned-out pyramid (outward ccw), each depth-sorted on its own
        TV, TF, TC = [], [], []
        for piece, Q, d in sp:
            tip = piece[-1]; col = COLS[min(cls.index((len(Q), round(d, 6))), 2)]
            for i in range(len(Q)):
                k = len(TV); TV += [Q[i], Q[(i + 1) % len(Q)], tip]; TF.append([k, k + 1, k + 2]); TC.append(col)
        S.tris(np.array(TV), TF, TC)
        VS = VP + sum(ConvexHull(piece).volume for piece, _, _ in sp)
        lim = 1.03 * max(np.linalg.norm(piece, axis=1).max() for piece, _, _ in sp)
        S.draw(ax, lim); ax.set_title(nm + ('\n' + sub if sub else ''), fontsize=8)
        info.append(dict(shape=nm, faces=len(faces), star_over_solid=VS / VP))
fig.text(0.5, 0.02, 'Stars: every centre pyramid turned out over its face (apex = mirror image of the centre); volume exactly twice the solid',
         ha='center', fontsize=8.5)
A.mark(fig); fig.savefig(os.path.join(A.OUT, 'vacuus-stars.png'), dpi=300, facecolor='white'); plt.close(fig)
json.dump(info, open(os.path.join(A.OUT, 'vacuus-stars-info.json'), 'w'), indent=1); print(json.dumps(info, indent=1))
