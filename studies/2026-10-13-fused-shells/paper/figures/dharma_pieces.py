# Figure: the Spheres of Dharma pieces in the app's colours, with DICTO's names, drawn like the Chain of Karma kit figure
# (papers/chain-of-karma/fig/kit_figure.py). Data: ../../pieces.json (dharma.cycle), at the dodecahedron-edge-1 scale.
import json, os, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, '..', '..', 'pieces.json')))['dharma.cycle']
ROLE = json.load(open(os.path.join(HERE, '..', '..', 'role-colours.json')))
NAMES = [('nfru3', 'Vajra (twist)'), ('npyr5', 'Stupa'), ('npyr3', 'Cleo-low'), ('nfru5', 'Monkey Staff'), ('nt1', 't1 (Mosseri–Sadoc)'),
         ('ncap6', 'Shield'), ('ncap5', 'pentagonal cap (J2)'), ('nwedge', 'Vajra-blade'), ('nedge', 'Sevenfold-blade'), ('nface', 'Cleo-low 2')]
def pick(key):
    if key.startswith('ncap'):
        n = 7 if key == 'ncap6' else 6
        r, V, F = next(x for x in D if x[0] == 'ncap' and len(x[1]) == n)
        return np.array(V, float), 0xffc857 if n == 7 else ROLE['ncap']
    r, V, F = next(x for x in D if x[0] == key)
    return np.array(V, float), ROLE[key]
def faces(W):
    H = ConvexHull(W); F = []
    for e in H.equations:
        idx = np.where(np.abs(W @ e[:3] + e[3]) < 2e-4)[0]
        if not any(set(idx) == set(f) for f in F): F.append(list(idx))
    out = []
    for f in F:
        P = W[f]; c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        a = P[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        out.append([f[i] for i in np.argsort(np.arctan2((P - c) @ b, (P - c) @ a))])
    return out
fig = plt.figure(figsize=(20, 9), dpi=150)
for k, (key, name) in enumerate(NAMES):
    W, col = pick(key); W = W - W.mean(0); F = faces(W)
    ax = fig.add_subplot(2, 5, k + 1, projection='3d')
    ax.add_collection3d(Poly3DCollection([W[f] for f in F], facecolor=f'#{col:06x}', edgecolor='#0b1220', alpha=.85, linewidths=1.2))
    r = np.abs(W).max() * 1.05; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1))
    ax.view_init(22, 35); ax.set_axis_off()
    vol = ConvexHull(W).volume
    ax.set_title(f'{name}\n{len(W)} corners, {len(F)} faces, volume {vol:.5f}', fontsize=12)
fig.suptitle('Spheres of Dharma: the pieces (dodecahedron of edge 1), in the app\'s colours; names by DICTO', fontsize=14)
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=10, color='#555')
plt.tight_layout(rect=(0, 0.02, 1, 0.95))
fig.savefig(os.path.join(HERE, 'fig8-dharma-pieces.png'), facecolor='white')
print('ok')
