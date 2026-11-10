"""A random irregular simple 4-polytope (DICTO 10 Nov: "test a random irregular simple 4D polytope"; the laws were first seen in regular
geometry - do they need it?). Random points near the 3-sphere (radii 0.8-1.2) -> their hull (simplicial, no symmetry) -> its polar, a simple
4-polytope. Predict births h1 = cells - 4, swaps h2 = corners - 2 - 2 h1, deaths h1 from the face counts alone; count in three random
directions; three random polytopes."""
import numpy as np, sys
from scipy.spatial import ConvexHull
sys.argv = ['sweep5d.py']; src = open('sweep5d.py').read().split("print('START the 5D test'")[0]; exec(src)
rng = np.random.default_rng(1110); ok = True
print('START three random simple 4-polytopes', flush=True)
for t, N in enumerate((24, 40, 64)):
    Pts = rng.normal(size=(N, 4)); Pts /= np.linalg.norm(Pts, axis=1)[:, None]; Pts *= rng.uniform(0.8, 1.2, size=(N, 1))
    h = ConvexHull(Pts); used = sorted(set(h.vertices)); cen = Pts[used].mean(0)
    # polar about the centre: each hull facet -> one corner; each original point -> one cell (the corners of the facets containing it)
    dual = np.array([eq[:4] / (-(eq[4] + eq[:4] @ cen)) for eq in h.equations])
    facets = [[k for k, simp in enumerate(h.simplices) if v in simp] for v in used]
    cells, corners = len(facets), len(dual); h1 = cells - 4; h2 = corners - 2 - 2 * h1
    print(f'polytope {t + 1}: {corners} corners, {cells} cells (from {len(used)} random points); predicted births {h1}, swaps {h2}, deaths {h1}', flush=True)
    ok &= analyse(f'random #{t + 1}', dual, {'facet born': h1, '1 lost / 1 gained': h2, 'facet dies': h1}, facets=facets)
print('FINAL ok' if ok else 'FINAL FAIL')
