# Step 14c: are the holes of the densest packing separate? Voxel flood fill of the gap over a 2x2x2 block of lattice cells.
# A gap component longer than one cell along a lattice direction percolates (labyrinth); if every component stays inside one
# cell's span, the holes are separate (a Dogstar analog). Two resolutions, since thin channels can slip between samples.
import json, itertools, numpy as np, sys
from scipy.spatial import ConvexHull
from scipy import ndimage
N = json.load(open('data/network.json')); O = np.array(N['ocd']); B = np.array(json.load(open('data/densest.json'))['B'])
EO = ConvexHull(O).equations
for res in (int(a) for a in sys.argv[1:] or ['40', '64']):
    n = 2 * res; f = (np.arange(n) + 0.5) / res                     # fractional coordinates over 2 cells per axis
    F = np.stack(np.meshgrid(f, f, f, indexing='ij'), -1).reshape(-1, 3); X = F @ B.T
    solid = np.zeros(len(X), bool)
    for m in itertools.product(range(-1, 4), repeat=3):
        c = B @ np.array(m, float)
        for s in range(0, len(X), 400000):
            Y = X[s:s + 400000] - c; solid[s:s + 400000] |= np.all(Y @ EO[:, :3].T + EO[:, 3] <= 0, axis=1)
    gap = ~solid.reshape(n, n, n)
    lab, k = ndimage.label(gap)
    span = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        span.append(max((s.stop - s.start) / res for s in sl))
    big = sum(1 for x in span if x > 1.0 + 1e-9)
    print(f'grid {res}^3 per cell: gap fraction {gap.mean():.4f} (expected {1 - 0.789260:.4f}); {k} gap pieces in the 2x2x2 block; '
          f'pieces longer than one cell: {big}; longest {max(span):.2f} cells', flush=True)
