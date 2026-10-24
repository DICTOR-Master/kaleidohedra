# Gap pieces of the 84% lattice, cut by neighbour pair, done carefully: per type, connected components on the periodic voxel grid,
# each unwrapped by walking its voxels (breadth first) so it lies in one piece of space; then volume, hull fill, flatness.
import numpy as np, itertools, json, collections
from scipy.spatial import ConvexHull
exec(open('swept1.py').read().split('# period:')[0])
B = np.array(json.load(open('swept-general-more.json'))['general']['basis']); det = abs(np.linalg.det(B))
n = int(__import__('sys').argv[1]) if len(__import__('sys').argv) > 1 else 100
g = (np.arange(n) + .5)/n; F = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3); X = F @ B
offs = np.array(list(itertools.product(range(-2, 3), repeat=3)))
Dist = np.stack([(np.einsum('ij,kj->ik', X - o @ B, ES[:, :3]) + ES[:, 3]).max(1) for o in offs], 1)
gap = (Dist <= 1e-12).sum(1) == 0
o2 = np.argsort(Dist, 1)[:, :2]; pv = offs[o2[:, 1]] - offs[o2[:, 0]]
keys = sorted({tuple(v) if tuple(v) > tuple(-v) else tuple(-v) for v in pv[gap]})
T = np.full(len(X), -1); 
for i in np.where(gap)[0]:
    v = tuple(pv[i]); v = v if v > tuple(-np.array(v)) else tuple(-np.array(v)); T[i] = keys.index(v)
T = T.reshape(n, n, n); vox = det / n**3
seen = np.zeros((n, n, n), bool); pieces = []; PTS = []
for start in zip(*np.where(T >= 0)):
    if seen[start]: continue
    t = T[start]; q = collections.deque([(start, (0, 0, 0))]); seen[start] = True; pts = []
    while q:
        (a, b, c), w = q.popleft(); pts.append((np.array([a, b, c]) + .5)/n + np.array(w))
        for d in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            na, nb, nc = a + d[0], b + d[1], c + d[2]; ww = list(w)
            for j, x in enumerate((na, nb, nc)):
                if x < 0: ww[j] -= 1
                if x >= n: ww[j] += 1
            na, nb, nc = na % n, nb % n, nc % n
            if T[na, nb, nc] == t and not seen[na, nb, nc]: seen[na, nb, nc] = True; q.append(((na, nb, nc), tuple(ww)))
    if len(pts) < 30: continue
    P = np.array(pts) @ B; v = len(pts) * vox
    try: hv = ConvexHull(P).volume
    except Exception: hv = float('nan')
    c = P - P.mean(0); w, V = np.linalg.eigh(c.T @ c / len(c))
    pieces.append((keys[t], v, v / hv, 2*np.sqrt(3*w[0]), 2*np.sqrt(3*w[2]))); PTS.append(P)
pieces.sort(key=lambda p: -p[1])
print(f'{len(pieces)} gap pieces per cell after cutting by neighbour pair (gap {gap.mean():.4f} of space)')
for k, v, f, th, sp in pieces: print(f'  between {tuple(int(x) for x in k)}: volume {v:.4f}, fills {100*f:.0f}% of its hull, thickness ~{th:.3f}, span ~{sp:.2f}')
json.dump([{'dir': [int(x) for x in k], 'volume': v, 'hull_fill': f, 'thickness': th, 'span': sp} for k, v, f, th, sp in pieces], open('swept-gap-pieces-84.json', 'w'), indent=1)

import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
order = np.argsort([-p[1] for p in pieces])[:6]
fig = plt.figure(figsize=(18, 11), dpi=100)
for j, i in enumerate(order):
    P = PTS[i] - PTS[i].mean(0); k, v, f, th, sp = pieces[i]
    c = P - P.mean(0); w, V = np.linalg.eigh(c.T @ c); Q = c @ V[:, ::-1]      # view face-on and edge-on
    for r, (a, b, ttl) in enumerate([(0, 1, 'face-on'), (0, 2, 'edge-on')]):
        ax = fig.add_subplot(2, 6, j + 1 + 6*r); ax.scatter(Q[:, a], Q[:, b], s=1, c=Q[:, 3-a-b] if r == 0 else Q[:, 1], cmap='plasma', linewidths=0)
        ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
        lim = np.abs(Q).max()*1.05; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
        ax.set_title((f'piece {j+1}: vol {v:.2f}, {100*f:.0f}% of hull\n' if r == 0 else '') + ttl, fontsize=10)
fig.suptitle('Swept dodecahedra, 84.2% lattice: the gap cut by neighbour pair = 6 thin plates per cell (dots = gap; same scale per piece)', fontsize=13)
fig.text(.98, .01, 'DICTO', ha='right', color='0.4', fontsize=12)
plt.savefig('swept-gap-plates-84.png', bbox_inches='tight'); print('saved picture')
