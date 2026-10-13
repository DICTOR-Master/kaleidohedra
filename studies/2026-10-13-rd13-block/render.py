# Renders the RD 13 block: the plain cluster, the rounded block (free volumes), pulled apart, and two keyed neighbours.
import json, sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R = json.load(open(sys.argv[1]))
cells = [[np.array(f) for f in c] for c in R['cells']]
L = np.array(R['L'])
cols = ['#ffc857'] + ['#5fd38a' if abs(v - R['volumes'][1]) < 1e-3 else '#4dd0e1' for v in R['volumes'][1:]]
def plain():
    import itertools
    NB = [np.array(v) for v in itertools.product([-1, 0, 1], repeat=3) if sorted(map(abs, v)) == [0, 1, 1]]
    out = []
    for p in [np.zeros(3)] + NB:
        fs = []
        for n in NB:
            i, j = [k for k in range(3) if n[k]]; k = 3 - i - j; e = np.eye(3)
            fs.append(np.array([p + n[i]*e[i], p + (n[i]*e[i] + n[j]*e[j] + e[k])/2, p + n[j]*e[j], p + (n[i]*e[i] + n[j]*e[j] - e[k])/2]))
        out.append(fs)
    return out
def draw(ax, blocks, title, apart=0.0, alpha=1.0):
    for cs, shift, palette in blocks:
        for ci, c in enumerate(cs):
            cen = np.mean([v for f in c for v in f], axis=0)
            off = cen * apart + shift
            ax.add_collection3d(Poly3DCollection([f + off for f in c], facecolor=palette[ci], edgecolor='#0b1220', linewidths=0.4, alpha=alpha))
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2); ax.set_zlim(-3.2, 3.2); ax.set_box_aspect((1, 1, 1)); ax.axis('off')
    ax.view_init(22, 35); ax.set_title(title, color='#e6e9f0', fontsize=10)
fig = plt.figure(figsize=(12, 4.2), facecolor='#0b0f14')
ax = fig.add_subplot(141, projection='3d', facecolor='#0b0f14'); draw(ax, [(plain(), 0, ['#ffc857'] + ['#9fb4c8'] * 12)], 'RD 13 as it is')
ax = fig.add_subplot(142, projection='3d', facecolor='#0b0f14'); draw(ax, [(cells, 0, cols)], 'rounded, keyed')
ax = fig.add_subplot(143, projection='3d', facecolor='#0b0f14'); draw(ax, [(cells, 0, cols)], 'pulled apart', apart=0.45)
ax = fig.add_subplot(144, projection='3d', facecolor='#0b0f14')
dim = ['#8a7440'] + ['#3f7a57' if c == '#5fd38a' else '#33808a' for c in cols[1:]]
draw(ax, [(cells, np.zeros(3), cols), (cells, L[0], dim)], 'two blocks, keyed')
ax.set_xlim(-3.5, 5); ax.set_ylim(-3.5, 5); ax.set_zlim(-3.5, 5)
plt.subplots_adjust(0, 0, 1, 0.92, 0, 0)
plt.savefig(sys.argv[2], dpi=130, facecolor='#0b0f14')
