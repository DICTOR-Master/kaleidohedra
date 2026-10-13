# The graded set: the DICTO Spheroid-13 RD's centre at minimum thickness 0.08, 0.15, 0.25, 0.35, at true relative size, viewed along
# the block's three-fold axis (top) and from the side (bottom). Usage: python3 centres.py out.png m0.08.json m0.15.json m0.25.json m0.35.json
import sys, json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
files = sys.argv[2:]
fig = plt.figure(figsize=(3.2 * len(files), 6.6), facecolor='#0b0f14')
for k, fn in enumerate(files):
    R = json.load(open(fn)); faces = [np.array(f) for f in R['cells'][0]]
    c = np.unique(np.round(np.concatenate(faces), 7), axis=0).mean(0)
    for row, (el, az) in enumerate([(35.26, 45), (5, -45)]):
        ax = fig.add_subplot(2, len(files), row * len(files) + k + 1, projection='3d', facecolor='#0b0f14')
        ax.add_collection3d(Poly3DCollection([f - c for f in faces], facecolor='#e8c25a', edgecolor='#0b1220', linewidths=0.6))
        ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7); ax.set_zlim(-1.7, 1.7); ax.set_box_aspect((1, 1, 1)); ax.axis('off'); ax.view_init(el, az)
        if row == 0: ax.set_title(f"thickness {R['margin']}\ncentre {R['volumes'][0]:.2f} ({R['volumes'][0] / 2:.2f} RD)", color='#e6e9f0', fontsize=10)
plt.subplots_adjust(0, 0, 1, 0.9, 0, 0)
plt.savefig(sys.argv[1], dpi=120, facecolor='#0b0f14')
