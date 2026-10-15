# Step 29 render data (DICTO: "render the fork at height 12.8"). Re-runs the step-29 setup (exact), then writes, for the renderer:
# the OCD's faces, the target copy and its ring, the rival copy (height 13.80) and its ring, the copies touching the target, the
# other nearby copies, the canonical chain heights near the target, and the overlap lens of target and rival (float hull of the
# two copies' face half-spaces; the overlap itself is exact, from step 29).
import json, numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
exec(open('scripts/chorus_h128.py').read().split("# the chorus's greedy")[0])
assert len(ov) == 1; iR = ov[0]
faces = []
for idx, n, d in PO:                                                   # polygon order round each face
    c = Of[idx].mean(axis=0); nn = f(n) / np.linalg.norm(f(n)); e = Of[idx[0]] - c; e /= np.linalg.norm(e); e2_ = np.cross(nn, e)
    faces.append(sorted(idx, key=lambda i: np.arctan2((Of[i] - c) @ e2_, (Of[i] - c) @ e)))
nU = np.array([f(n) / np.linalg.norm(f(n)) for _, n, d in PO]); dU = np.array([d.f() / np.linalg.norm(f(n)) for _, n, d in PO])
hs = np.vstack([np.c_[nU, -(dU + nU @ LP[iT])], np.c_[nU, -(dU + nU @ LP[iR])]])
lens = HalfspaceIntersection(hs, (LP[iT] + LP[iR]) / 2).intersections; LH = ConvexHull(lens)
pen = best(XT, loc[iR][1])
chain = []
for p in range(-60, 61):
    for q in range(-60, 61):
        t = tb1 * Q(p) + tb2 * Q(q); h = (hb1 * Q(p) + hb2 * Q(q)).f() / vv.f() ** .5
        if abs(h - hT) < 6 and 0 <= t.f() < Lw.f(): chain.append(h)
J = {'ocd': Of.tolist(), 'faces': faces, 'a5': ax.tolist(), 'hT': hT, 'target': LP[iT].tolist(), 'targetRing': [LP[j].tolist() for j in rT],
     'rival': LP[iR].tolist(), 'rivalRing': [LP[j].tolist() for j in ring(iR) if j is not None],
     'touch': [LP[j].tolist() for j in to], 'near': [LP[j].tolist() for j in nb if j not in to and j != iR],
     'lens': lens.tolist(), 'lensTri': LH.simplices.tolist(), 'lensVol': LH.volume, 'ocdVol': ConvexHull(Of).volume,
     'pen': str(pen), 'penF': pen.f(), 'chain': sorted(chain)}
json.dump(J, open('data/chorus-fork.json', 'w'))
print(f'fork data: rival at height {LP[iR] @ ax:.4f}; overlap lens volume {LH.volume:.5f} = {LH.volume / ConvexHull(Of).volume * 100:.2f}% of one copy; '
      f'deepest face separation (exact) {pen} = {pen.f():.6f}; chain heights near the target {[round(h, 3) for h in sorted(chain)]}')
