# Figure + piece shapes for kagemusha_variants.py: the step-1 surfaces (gold: solid face, violet: cap spikes, teal: notch pieces) and the
# face sizes / edge lengths of one notch piece per variant. Usage: kagemusha_variants_fig.py <data dir>
import json, sys, os, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
D = sys.argv[1]; R = json.load(open(os.path.join(D, 'kagemusha-variants.json')))
col = dict(solid='#c9a227', spike='#9b7fd4', notch='#2a9d8f')
fig = plt.figure(figsize=(12, 3.4), dpi=170); light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
for k, r in enumerate(R):
    V = np.array(r['step1']['V']); F = r['step1']['F']; kind = r['step1']['kind']
    ax = fig.add_subplot(1, 4, k + 1, projection='3d'); polys, fc = [], []
    for f, kd in zip(F, kind):
        P = V[f]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n); sh = 0.55 + 0.45 * max(0, n @ light)
        c = np.array(matplotlib.colors.to_rgb(col[kd])) * sh; polys.append(P); fc.append(np.clip(c, 0, 1))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=fc, edgecolors='#1a1a1a', linewidths=0.9))
    m = 0.62 * np.abs(V).max(); ax.set_xlim(-m, m); ax.set_ylim(-m, m); ax.set_zlim(-m, m); ax.set_box_aspect((1, 1, 1)); ax.view_init(18, 30); ax.axis('off')
    ax.set_title(('conjoined' if r['variant'] == 'conjoined' else 'sloping bases') + ', t = ' + ('φ' if r['t'] == 'phi' else '2') + f"\nafter step 1: ×{r['steps'][0]['volume_over_last']:.4f}", fontsize=9)
plt.subplots_adjust(0, 0, 1, 0.9, 0.02, 0); plt.savefig(os.path.join(D, 'kagemusha-variants.png'), facecolor='white')
# notch-piece shapes: faces of the union of notch pieces round one notch, from the step-1 surface
for r in R:
    V = np.array(r['step1']['V']); F = [f for f, kd in zip(r['step1']['F'], r['step1']['kind']) if kd == 'notch']
    n = len(F) // 5; P = F[:n]; vs = sorted({v for f in P for v in f})
    L = sorted({round(float(np.linalg.norm(V[f[a]] - V[f[(a + 1) % len(f)]])), 6) for f in P for a in range(len(f))})
    print(r['variant'], r['t'], 'outer faces per notch', n, 'sizes', sorted(len(f) for f in P), 'corners', len(vs), 'outer edge lengths', L)
