"""DICTO's Polyhedraverse build "RD-Hemi (bare) + 13x face-attached RD-Hemi (bare)" (exported 11 Nov 2026 from Rhombiverse's world export),
rebuilt exactly from its 14 transforms. Questions (DICTO 11 Nov): what is the solid; are its hexagons truncated triangles or stretched
hexagons; where are the open squares/dents; do the dents echo how the 30 cells of the 4D permutohedron meet round one permutohedron cell?
Prints: pieces, overlaps (none expected), glued faces, the outer surface, the convex hull and its faces, the dents (hull minus union)."""
import json, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
B = json.load(open(sys.argv[1]))
# the Hemi RD in its own frame (Polyhedraverse RVCMG_RD_HEMI at identity, from the app's record)
LV = np.array([[-0.5,-0.3,0.7],[-1,0.2,0.2],[-0.5,0.7,-0.3],[0.5,0.7,-0.3],[1,0.2,0.2],[0.5,-0.3,0.7],[-0.5,-0.3,-0.3],[0.5,-0.3,-0.3],[0,-0.8,0.2],[0,0.2,-0.8]])
LF = [[4,3,2,1,0,5],[9,7,8,6],[8,0,1,6],[4,5,8,7],[4,7,9,3],[9,6,1,2],[8,5,0],[9,2,3]]
def rot(q):
    x,y,z,w = q; n = (x*x+y*y+z*z+w*w) ** .5; x,y,z,w = x/n,y/n,z/n,w/n
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
P = [(LV @ rot(n['transform']['quaternion']).T + np.array(n['transform']['position'])) for n in B['nodes']]
def vol(V, F):
    c = V.mean(0); s = 0
    for f in F:
        for k in range(1, len(f) - 1): s += abs(np.linalg.det(np.array([V[f[0]] - c, V[f[k]] - c, V[f[k + 1]] - c]))) / 6
    return s
hv = vol(LV, LF); print(f'pieces {len(P)}, one Hemi RD volume {hv:.6f} (an RD of this size: {2*hv:.6f}); union volume if disjoint {len(P)*hv:.6f}')
# face keys to find glued faces (same corner set) and outer faces
key = lambda pts: tuple(sorted(tuple(np.round(p, 6)) for p in pts))
cnt = {}
for i, V in enumerate(P):
    for j, f in enumerate(LF): cnt.setdefault(key(V[f]), []).append((i, j, len(f)))
glued = [v for v in cnt.values() if len(v) == 2]; outer = [v[0] for v in cnt.values() if len(v) == 1]
print(f'glued face pairs {len(glued)}; outer faces {len(outer)} by size', dict(sorted({s: sum(1 for (_, _, k) in outer if k == s) for s in (3, 4, 6)}.items())))
# overlaps: sample interior points of each piece and test inside others (convex pieces)
def inside(Vp, x):
    h = ConvexHull(Vp); return np.all(h.equations[:, :3] @ x + h.equations[:, 3] < -1e-7)
rng = np.random.default_rng(1); ov = 0
for i, V in enumerate(P):
    for _ in range(200):
        w = rng.dirichlet(np.ones(len(V))); x = w @ V
        ov += sum(inside(P[j], x) for j in range(len(P)) if j != i)
print('overlap samples (should be 0):', ov)
A = np.vstack(P); H = ConvexHull(A); print(f'convex hull volume {H.volume:.6f}; dents (hull minus pieces) {H.volume - len(P)*hv:.6f} = {(H.volume - len(P)*hv)/hv:.3f} Hemi RDs')
groups = {}
for simp, eq in zip(H.simplices, H.equations): groups.setdefault(tuple(np.round(eq, 6)), set()).update(map(tuple, np.round(A[simp], 6)))
faces = []
for eq, pts in groups.items():
    pts = np.array(sorted(pts)); c = pts.mean(0); n = np.array(eq[:3]); u = pts[0] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
    o = sorted(range(len(pts)), key=lambda k: np.arctan2((pts[k] - c) @ w, (pts[k] - c) @ u)); pts = pts[o]
    # drop collinear corners
    keep = [k for k in range(len(pts)) if np.linalg.norm(np.cross(pts[k] - pts[k - 1], pts[(k + 1) % len(pts)] - pts[k])) > 1e-6]
    pts = pts[keep]; sides = [round(float(np.linalg.norm(pts[k] - pts[(k + 1) % len(pts)])), 4) for k in range(len(pts))]
    faces.append((len(pts), sides, np.round(n, 4)))
from collections import Counter
print('hull faces:', dict(Counter(f[0] for f in faces)))
for k, sides, n in sorted(faces, key=lambda f: (-f[0], list(f[2]))): print(f'  {k}-gon sides {sides} normal {list(n)}')
# the dents: is each hull square the base of an empty square pyramid (apex half a side inside), i.e. a missing cube pyramid?
def in_union(x): return any(inside(V, x) for V in P)
def in_hull(x): return np.all(H.equations[:, :3] @ x + H.equations[:, 3] < -1e-7)
print('dents under the six squares (cube pyramid = base side 1, apex 0.5 inside, volume 1/6):')
tot = 0
for k, sides, n in faces:
    if k != 4: continue
    n = np.array(n, float); c = A[np.argmax(A @ n)] if False else None
    d0 = max(A @ n); sq_c = n * d0                      # square centre lies on the axis through the hull's centre (hull centred at origin?)
    ctr = A.mean(0)
    sq_c = ctr + n * (d0 - ctr @ n)
    # Monte Carlo: fraction of the pyramid (base the square, apex sq_c - 0.5 n) that is empty of pieces
    t1 = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); t1 /= np.linalg.norm(t1); t2 = np.cross(n, t1)
    m = 0; tot_s = 0
    for _ in range(3000):
        h = rng.random() * 0.5; s = 1 - h / 0.5                    # depth h, square half-side shrinks linearly to the apex
        a, b = (rng.random(2) - .5) * s
        # the hull squares are axis-aligned in the cube frame: use the square's own edge directions
        x = sq_c - n * h + t1 * a + t2 * b
        tot_s += 1; m += (not in_union(x)) and in_hull(x)
    print(f'  square normal {list(np.round(n,3))}: empty fraction of the pyramid under it {m / tot_s:.3f}')
    tot += m / tot_s
print(f'sum of empty fractions {tot:.3f} (6.000 = six whole empty cube pyramids)')
