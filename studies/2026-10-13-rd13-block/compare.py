# Side by side: the rounded RD 13 block at several minimum thicknesses (top: whole block; bottom: pulled apart).
import json, sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
files = sys.argv[2:]
fig = plt.figure(figsize=(3.2 * len(files), 6.6), facecolor='#0b0f14')
for k, fn in enumerate(files):
    R = json.load(open(fn))
    cells = [[np.array(f) for f in c] for c in R['cells']]
    v = R['volumes']
    cols = ['#ffc857'] + ['#5fd38a' if abs(x - v[1]) < 1e-3 else '#4dd0e1' for x in v[1:]]
    iq = 36 * np.pi * 26 ** 2 / R['area'] ** 3
    for row, apart in enumerate([0.0, 0.45]):
        ax = fig.add_subplot(2, len(files), row * len(files) + k + 1, projection='3d', facecolor='#0b0f14')
        for ci, c in enumerate(cells):
            cen = np.mean([p for f in c for p in f], axis=0)
            ax.add_collection3d(Poly3DCollection([f + cen * apart for f in c], facecolor=cols[ci], edgecolor='#0b1220', linewidths=0.4))
        ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.2, 3.2); ax.set_zlim(-3.2, 3.2); ax.set_box_aspect((1, 1, 1)); ax.axis('off'); ax.view_init(22, 35)
        if row == 0:
            outer = sorted(set(round(x, 3) for x in v[1:]))
            kind = 'exact RD centre' if 'rdcentre' in fn else 'free centre'
            ax.set_title(f"thickness {R['margin']} · {kind}\nroundness {iq:.3f}\ncentre {v[0]:.2f}, outer {' / '.join(f'{x:.2f}' for x in outer)}", color='#e8c25a' if 'rdcentre' in fn else '#e6e9f0', fontsize=9)
plt.subplots_adjust(0, 0, 1, 0.9, 0, 0)
plt.savefig(sys.argv[1], dpi=120, facecolor='#0b0f14')
