# Figure: the eleven steps of the twelve-station golden cycle, each added region drawn as its pieces (slightly pulled apart), coloured by kind.
# From pieces.json (gnomon_shapes.py). DICTO mark small in a corner. -> gnomon-shapes.png
import json, os, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
H = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(H, 'pieces.json')))
COL = ['#c9a24a', '#8e5ea2', '#3f8f8a', '#c0533a', '#4a6fa5']
fig = plt.figure(figsize=(16, 12), facecolor='white')
for si, st in enumerate(D['steps']):
    ax = fig.add_subplot(3, 4, si + 1, projection='3d'); ax.set_axis_off(); ax.view_init(elev=18, azim=32)
    R = max(np.linalg.norm(np.array(D['stations'][st['to']]), axis=1)) * 1.12
    for ki, K in enumerate(st['kinds']):
        for P in K['pieces']:
            P = np.array(P); c = P.mean(0)
            if c @ np.array([0.55, -0.8, 0.25]) > 0.05 * R: continue      # cut away the front: see inside
            P = P + 0.10 * c; h = ConvexHull(P)
            ax.add_collection3d(Poly3DCollection([P[s] for s in h.simplices], facecolors=COL[ki], edgecolors='#33333344', linewidths=0.2, alpha=0.95, shade=True))
    lab = '\n'.join(f'{len(K["pieces"])} × {K["label"]}' for K in st['kinds'])
    ax.set_title(f'step {si + 1}: {st["from"]} → {st["to"]}\n{lab}', fontsize=9)
    ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.set_zlim(-R, R); ax.set_box_aspect((1, 1, 1))
ax = fig.add_subplot(3, 4, 12); ax.set_axis_off()
ax.text(0, 0.95, 'What each step adds (exact pieces)', fontsize=11, weight='bold', va='top')
ax.text(0, 0.80, 'Front half cut away; pieces pulled\napart 10 %. Colours: kinds within a step.\n'
        'Only step 11 (M → I·φ³) makes a whole\nsimilar to an earlier station (I, ratio φ³):\nthe classical gnomon of the turn.\n'
        'No two piece kinds of different\nsteps are similar.', fontsize=9, va='top')
logo = plt.imread(os.path.join(H, 'dicto-logo.png')); fig.figimage(logo[::max(1, logo.shape[0] // 60), ::max(1, logo.shape[0] // 60)], xo=fig.bbox.xmax - 90, yo=10, zorder=10)
fig.text(0.995, 0.005, 'DICTO · dictospheres.com', ha='right', fontsize=7, color='#8a6d1c')
plt.tight_layout(); fig.savefig(os.path.join(H, 'gnomon-shapes.png'), dpi=110)
