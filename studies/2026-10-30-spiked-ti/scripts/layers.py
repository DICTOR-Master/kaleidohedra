# The doubling cycle of the spiked TI: TI -> spiked TI (TI + 32 outward pyramids) -> spike hull (60 triangles) -> 2 TI.
# Candidate fill pieces, checked by volume and by pairwise overlap:
#   layer 1 (spiked TI -> hull): at each TI corner v the tetrahedron (v, three tips over the faces at v); over each TI edge vw the
#     tetrahedron (v, w, the two tips over the faces at vw);
#   layer 2 (hull -> 2 TI): at each corner 2v of 2 TI the tetrahedron (2v, three tips), the tips being the centres of 2 TI's faces;
#     over each edge of 2 TI the tetrahedron (its two ends, the two tips over its faces).
import json, itertools, os, numpy as np
SCN = os.environ.get('SCALE', '2'); SC = {'2': 2.0, 'phi': (1 + 5 ** .5) / 2}[SCN]   # tip = SC x face centre; 2 = mirrored pyramids (doubling cycle), phi = golden cycle
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
h = ConvexHull(P); F = []; seen = set()
for eq in h.equations:
    k = tuple(np.round(eq, 7))
    if k in seen: continue
    seen.add(k); F.append([i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8])
tip = [SC * P[f].mean(0) for f in F]
e = min(np.linalg.norm(P[0] - P[j]) for j in range(1, len(P)))
E = [(i, j) for i, j in itertools.combinations(range(len(P)), 2) if abs(np.linalg.norm(P[i] - P[j]) - e) < 1e-9]
faces_at = {v: [fi for fi, f in enumerate(F) if v in f] for v in range(len(P))}
vol = lambda Q: abs(np.linalg.det(np.array([Q[1] - Q[0], Q[2] - Q[0], Q[3] - Q[0]]))) / 6
VT = h.volume
corner1 = [[P[v]] + [tip[f] for f in faces_at[v]] for v in range(len(P))]
edge1 = [[P[i], P[j]] + [tip[f] for f in F_ if True] for (i, j) in E for F_ in [[fi for fi, f in enumerate(F) if i in f and j in f]]]
corner2 = [[SC * P[v]] + [tip[f] for f in faces_at[v]] for v in range(len(P))]
edge2 = [[SC * Q[0], SC * Q[1], Q[2], Q[3]] for Q in edge1]   # over each edge of 2 TI: its two ends and the centres of its two faces
kinds = lambda L: sorted({round(vol(Q), 9) for Q in L})
spiked = SC * VT; hT = ConvexHull(np.array(tip)); hull = hT.volume
inside_TI = bool(np.all(P @ hT.equations[:, :3].T + hT.equations[:, 3] <= 1e-9))
out = dict(TI=VT, spiked=spiked, hull=hull, outer=SC ** 3 * VT, scale=SC, hull_contains_TI_corners=inside_TI,
           layer1=dict(corner_tets=len(corner1), corner_vol=kinds(corner1), edge_tets=len(edge1), edge_vols=kinds(edge1),
                       sum=sum(map(vol, corner1)) + sum(map(vol, edge1)), needed=hull - spiked),
           layer2=dict(corner_tets=len(corner2), corner_vol=kinds(corner2), edge_tets=len(edge2), edge_vols=kinds(edge2), sum=sum(map(vol, corner2)) + sum(map(vol, edge2)), needed=SC ** 3 * VT - hull))
print(json.dumps(out, indent=1), flush=True)
# overlap: separating-axis test for convex pieces, for every pair whose bounding spheres meet (face normals and edge cross products)
pieces = [np.array(Q) for Q in corner1 + edge1 + corner2 + edge2] + [np.vstack([P[f], tip[fi]]) for fi, f in enumerate(F)] + [P]
def axes(Q):
    hq = ConvexHull(Q); n = [eq[:3] for eq in hq.equations]
    ed = {tuple(sorted((a, b))) for sm in hq.simplices for a, b in [(sm[0], sm[1]), (sm[1], sm[2]), (sm[0], sm[2])]}
    return n, [Q[b] - Q[a] for a, b in ed]
AX = [axes(Q) for Q in pieces]; C = [Q.mean(0) for Q in pieces]; Rr = [np.linalg.norm(Q - Q.mean(0), axis=1).max() for Q in pieces]
def separated(i, j):
    A_, B_ = pieces[i], pieces[j]
    cand = AX[i][0] + AX[j][0] + [np.cross(u, v) for u in AX[i][1] for v in AX[j][1]]
    for ax in cand:
        nn = np.linalg.norm(ax)
        if nn < 1e-12: continue
        ax = ax / nn; pa, pb = A_ @ ax, B_ @ ax
        if pa.max() <= pb.min() + 1e-9 or pb.max() <= pa.min() + 1e-9: return True
    return False
bad = []
for i, j in itertools.combinations(range(len(pieces)), 2):
    if np.linalg.norm(C[i] - C[j]) > Rr[i] + Rr[j] + 1e-9: continue
    if not separated(i, j): bad.append((i, j))
out['pieces checked'] = len(pieces)
import sympy as sp
ident = lambda x: str(sp.nsimplify(round(x, 12), [sp.sqrt(5)], tolerance=1e-10))
out['exact volumes'] = {k: [ident(v) for v in L] for k, L in [('layer1 corner', kinds(corner1)), ('layer1 edge', kinds(edge1)), ('layer2 corner', kinds(corner2)), ('layer2 edge', kinds(edge2)), ('TI', [VT]), ('hull', [hull])]}; out['overlapping pairs (separating axis)'] = len(bad); out['first overlaps'] = bad[:5]
print(json.dumps(out, indent=1)); json.dump(out, open('data/layers-%s.json' % SCN, 'w'), indent=1)
