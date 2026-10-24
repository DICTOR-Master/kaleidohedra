# Cut the 84% lattice's gap sheets into pieces: each gap point goes to the pair of neighbouring swept pieces it lies between
# (the two nearest by outward facet distance). One region per neighbour direction +-v; report volume, how much of its own
# convex hull it fills, thickness (volume / area estimate), and whether it is one connected piece.
import numpy as np, itertools, json
from scipy import ndimage
from scipy.spatial import ConvexHull
exec(open('swept1.py').read().split('# period:')[0])
B = np.array(json.load(open('swept-general-more.json'))['general']['basis']); det = abs(np.linalg.det(B))
n = int(__import__('sys').argv[1]) if len(__import__('sys').argv) > 1 else 120
g = (np.arange(n) + .5)/n; F = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3); X = F @ B
offs = np.array(list(itertools.product(range(-2, 3), repeat=3)))
Dist = np.stack([(np.einsum('ij,kj->ik', X - o @ B, ES[:, :3]) + ES[:, 3]).max(1) for o in offs], 1)   # >0 outside
gap = (Dist <= 1e-12).sum(1) == 0
Dg = Dist[gap]; o2 = np.argsort(Dg, 1)[:, :2]
pair_vec = offs[o2[:, 1]] - offs[o2[:, 0]]
key = [tuple(v) if tuple(v) > tuple(-v) else tuple(-v) for v in pair_vec]      # neighbour direction up to sign
types = {}
for k in set(key): types[k] = np.array([i for i, kk in enumerate(key) if kk == k])
vox = det / n**3; tot = gap.sum()
print(f'gap {gap.mean():.4f} of space, split by neighbour pair into {len(types)} directions (per cell)')
out = []
Xg = X[gap]; Fg = F[gap]
for k, idx in sorted(types.items(), key=lambda t: -len(t[1])):
    v = len(idx) * vox
    if len(idx) < 50: continue
    fr = Fg[idx]; fr = fr - np.round(fr - fr[0]); P = fr @ B          # unwrap
    try: hv = ConvexHull(P).volume
    except Exception: hv = float('nan')
    # thickness: extent along the normal of the best plane (smallest principal axis)
    c = P - P.mean(0); w, V = np.linalg.eigh(c.T @ c / len(c)); thick = 2*np.sqrt(3*w[0]); span = 2*np.sqrt(3*w[2])
    out.append({'dir': list(map(int, k)), 'vec': (np.array(k) @ B).round(4).tolist(), 'volume': v, 'hull_fill': v / hv, 'thickness': thick, 'span': span})
    print(f'  between pieces {k}: volume {v:.4f} ({100*len(idx)/tot:.1f}% of the gap), fills {100*v/hv:.0f}% of its hull, thickness ~{thick:.3f}, span ~{span:.2f}')
json.dump(out, open('swept-gap-split-84.json', 'w'), indent=1)
