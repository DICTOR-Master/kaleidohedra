import json, math, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
d = json.load(open('data/narcissus-together.json')); V = np.array(d['vertices'])
fig = plt.figure(figsize=(11, 6), dpi=140); light = np.array([.4, -.5, .8]); light /= np.linalg.norm(light)
for k, (el, az) in enumerate(((18, -55), (18, 35))):
    ax = fig.add_subplot(1, 2, k + 1, projection='3d'); polys = []; cols = []
    for f, c in zip(d['faces'], d['faceColours']):
        P = V[f]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n) + 1e-12
        base = np.array([(c >> 16) & 255, (c >> 8) & 255, c & 255])/255; polys.append(P); cols.append(np.clip(base*(0.55 + 0.45*max(0, n @ light)), 0, 1))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=cols, edgecolor='#222', linewidths=0.3))
    r = 1.2; ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r); ax.view_init(el, az); ax.set_axis_off()
fig.suptitle(f"Narcissus (gold, h layers) and cubes (purple, c layers) filling a Fibonacci stacking — word {d['word'][:8]}…, types {''.join(d['types'])}", fontsize=10)
try: m = plt.imread('dicto-mark.png'); a = fig.add_axes([0.9, 0.02, 0.08, 0.1]); a.imshow(m); a.axis('off')
except Exception: pass
fig.savefig('renders/narcissus-together.png', bbox_inches='tight'); print('ok')
