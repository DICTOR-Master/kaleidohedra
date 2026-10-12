# Figure: the Chain of Karma kit at edge 1 (AXE, CLEO, FUJI, pentagonal pyramid, J11), every edge labelled with its length.
# Pieces taken from the checked Lotus seed data (studies/2026-10-11-self-building-kit/data/ms-kit.json), rescaled to edge 1.
import json, itertools, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2
D = json.load(open(__file__.replace('papers/chain-of-karma/fig/kit_figure.py', 'studies/2026-10-11-self-building-kit/data/ms-kit.json')))
pick = lambda r: np.array(next(x for x in D if x['role'] == r)['vertices'], float)
A0 = pick('axe'); EL = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(A0, 2)); s = 1 / EL[-1]   # AXE: five edges 1, one 1/phi
ico = max((np.array(x['vertices'], float) for x in D if x['role'] == 'ico'), key=lambda W: np.ptp(W[:, 0]))
I = ico * s; I -= I.mean(0); assert abs(min(np.linalg.norm(I[0] - w) for w in I[1:]) - 1) < 1e-6
top = I[np.argmax(I[:, 2])]; nb = [v for v in I if abs(np.linalg.norm(v - top) - 1) < 1e-6]
pyr = np.vstack([top] + nb); j11 = np.array([v for v in I if np.linalg.norm(v - top) > 1e-6])
pieces = [('AXE', pick('axe') * s, '#4dd0e1'), ('CLEO', pick('cleo') * s, '#c792ea'), ('FUJI', pick('fuji') * s, '#c792ea'),
          ('pentagonal pyramid', pyr, '#e8c25a'), ('J11', j11, '#5fd38a')]
def lab(L):
    for v, t in ((1, '1'), (1 / PHI, '1/φ'), (PHI, 'φ')):
        if abs(L - v) < 1e-6: return t
    return f'{L:.4f}'
def faces(W):
    H = ConvexHull(W); F = []
    for e in H.equations:
        idx = np.where(np.abs(W @ e[:3] + e[3]) < 1e-7)[0]
        if not any(set(idx) == set(f) for f in F): F.append(list(idx))
    out = []
    for f in F:
        P = W[f]; c = P.mean(0); n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
        a = P[0] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
        out.append([f[i] for i in np.argsort(np.arctan2((P - c) @ b, (P - c) @ a))])
    return out
fig = plt.figure(figsize=(20, 5), dpi=150)
for k, (name, W, col) in enumerate(pieces):
    W = W - W.mean(0); ax = fig.add_subplot(1, 5, k + 1, projection='3d'); F = faces(W)
    ax.add_collection3d(Poly3DCollection([W[f] for f in F], facecolor=col, edgecolor='#0b1220', alpha=.82, linewidths=1.2))
    E = {tuple(sorted((f[i], f[(i + 1) % len(f)]))) for f in F for i in range(len(f))}
    if name != 'J11':
        for a, b in E:
            m = (W[a] + W[b]) / 2; m = m * 1.12
            ax.text(*m, lab(np.linalg.norm(W[a] - W[b])), fontsize=9, ha='center', color='#111')
    r = np.abs(W).max(); ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.set_box_aspect((1, 1, 1)); ax.axis('off')
    ax.view_init(elev=22, azim=35 + 20 * k)
    ax.set_title(f'{name}\n{len(W)} corners, {len(F)} faces, volume {ConvexHull(W).volume:.6f}', fontsize=11)
fig.suptitle('The kit at edge 1. Every dihedral angle is an integer combination of α = arccos(√5/3) = 41.81° and δ = arctan(3−√5) = 37.38° (mod 180°)', fontsize=12)
plt.tight_layout(); plt.savefig(__file__.replace('kit_figure.py', 'kit.png'), facecolor='white')
print('ok')
