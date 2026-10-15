# Step 14b: are the holes of the densest lattice packing separate (a Dogstar analog) or one connected labyrinth?
# The gap of a copy lies in its Voronoi cell D. Neighbouring gaps connect through any part of a wall of D that the solids do not
# cover; holes are separate only if every wall is fully covered. For each wall: its area and the area the OCD covers on it.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
N = json.load(open('data/network.json')); O = np.array(N['ocd']); B = np.array(json.load(open('data/densest.json'))['B'])
W = np.array([m for m in itertools.product(range(-3, 4), repeat=3) if any(m)], float); L = (B @ W.T).T
L = L[np.argsort(np.linalg.norm(L, axis=1))][:200]
H = np.array([np.r_[l, -(l @ l) / 2] for l in L])                       # bisector halfspaces l.x <= |l|^2/2
D = HalfspaceIntersection(H, np.zeros(3)).intersections; D = np.unique(np.round(D, 9), axis=0); hD = ConvexHull(D)
walls = []
for e in hD.equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in walls): walls.append(e)
EO = ConvexHull(O).equations
def area2d(P, n):
    b = np.linalg.svd(P - P.mean(0))[2][:2]; return ConvexHull((P - P.mean(0)) @ b.T).volume if len(P) >= 3 else 0.0
out = [f'Voronoi cell of the densest packing: {len(walls)} walls, volume {hD.volume:.6f} (OCD {ConvexHull(O).volume:.6f}, density {ConvexHull(O).volume / hD.volume:.6f})']
open_walls = 0
for e in walls:
    W_ = D[np.abs(D @ e[:3] + e[3]) < 1e-7]; aw = area2d(W_, e[:3])
    # the OCD's footprint on this wall plane: its face lying in the plane, if any
    onp = O[np.abs(O @ e[:3] + e[3]) < 1e-7]; ac = area2d(onp, e[:3]) if len(onp) >= 3 else 0.0
    if aw - ac > 1e-9: open_walls += 1
    out.append(f'   wall area {aw:.6f}, covered by the OCD {ac:.6f} ({100 * ac / aw:.1f}%)')
out.append(f'walls with an uncovered part (gap flows through): {open_walls} of {len(walls)} -> the holes are ' + ('SEPARATE' if open_walls == 0 else 'one connected labyrinth'))
print('\n'.join(out)); open('data/holes.txt', 'w').write('\n'.join(out) + '\n')
