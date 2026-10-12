# Figure: the Ritsudo cycle of the Spheres of Dharma, one panel per step: the inner shell solid, the next shell as wire frame,
# all at true relative size (dodecahedron edge 1). Shells from network_screen.py, exact triacontahedron edge sqrt(45-18sqrt5)/2.
import itertools, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
el = lambda W: min(np.linalg.norm(W[0] - w) for w in W[1:])
S = [('icosahedron 1/φ', ref['I'] / el(ref['I']) / PHI, '#5fd38a'), ('icosidodecahedron φ/2', ref['ID'] / el(ref['ID']) * PHI / 2, '#e8c25a'),
     ('dodecahedron 1', ref['D'] / el(ref['D']), '#c792ea'), ('fullerene cage 1/φ', ref['TI'] / el(ref['TI']) / PHI, '#4dd0e1'),
     ('triacontahedron ½√(45−18√5)', ref['RT'] / el(ref['RT']) * np.sqrt(45 - 18 * np.sqrt(5)) / 2, '#e8c25a'), ('icosahedron φ²', ref['I'] / el(ref['I']) * PHI ** 2, '#5fd38a')]
def faces(W):
    H = ConvexHull(W); F = []
    for e in H.equations:
        idx = np.where(np.abs(W @ e[:3] + e[3]) < 1e-7)[0]
        if not any(set(idx) == set(f) for f in F): F.append(list(idx))
    out = []
    for f in F:
        P = W[f]; c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n); a = P[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        out.append([f[i] for i in np.argsort(np.arctan2((P - c) @ b, (P - c) @ a))])
    return out
R = np.linalg.norm(S[-1][1], axis=1).max()
fig = plt.figure(figsize=(20, 4.4), dpi=150)
for k in range(5):
    ax = fig.add_subplot(1, 5, k + 1, projection='3d')
    (n1, A, c1), (n2, B, c2) = S[k], S[k + 1]
    ax.add_collection3d(Poly3DCollection([A[f] for f in faces(A)], facecolor=c1, edgecolor='#0b1220', alpha=.9, linewidths=.6))
    segs = [[B[f[i]], B[f[(i + 1) % len(f)]]] for f in faces(B) for i in range(len(f))]
    ax.add_collection3d(Line3DCollection(segs, colors='#333', linewidths=.8))
    r = np.linalg.norm(B, axis=1).max(); ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.axis('off')
    ax.view_init(elev=18, azim=28); ax.set_title(f'{n1}\ninside {n2}', fontsize=11)
fig.suptitle('One Ritsudō cycle: each solid (filled) inside the next (wire), edges relative to the dodecahedron of edge 1; the last icosahedron is φ³ times the first', fontsize=12)
plt.tight_layout(rect=(0, 0, 1, 0.9)); plt.savefig('cycle.png', facecolor='white'); print('ok')
