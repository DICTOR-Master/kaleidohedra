# Step 4 (DICTO: "a paired shape with hexagons that shares rhombi?"). Exploratory, float first.
# Partner sites: the centres of the Voronoi cell's 6 square faces (bcc octahedral sites), each shared by 2 cells: 3 per OCD, each
# meeting 4 free hexagons (2 from each of the two OCDs on that cube axis), so 3 x 4 = all 12 free hexagons. Gather the gap pieces
# of a patch of cells, give each piece to its nearest partner site, and test whether each site's pieces fuse into one convex solid;
# if so, list its faces (hexagons? rhombi?).
import json, itertools, numpy as np, sys
from scipy.spatial import ConvexHull
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/_lib'); import geomcheck as gc
G = json.load(open('data/gaps.json')); N = json.load(open('data/network.json')); R = json.load(open('data/network-render.json'))
T = np.array(N['T']); cube = np.array(R['cube'])
a_half = abs(np.array(G['V']) @ cube[0]).max()                    # distance from the centre to a square face
L = [T[0] + T[1], T[0] + T[2], T[0] + T[3]]                        # the cube-axis lattice vectors (second neighbours)
assert all(abs(np.linalg.norm(l) - 2 * a_half) < 1e-9 for l in L)
# the patch: cells at bcc points near the origin
cells = []
for m in itertools.product(range(-2, 3), repeat=4):
    p = sum(k * t for k, t in zip(m, T))
    if np.linalg.norm(p) < 2.6 and not any(np.allclose(p, c) for c in cells): cells.append(p)
pieces = [(np.array(V) + c, i) for c in cells for i, V in enumerate(G['pieces'])]
site = cube[2] * a_half                                            # one partner site: a square-face centre of the origin cell
sites = [c + s * cube[k] * a_half for c in cells for k in range(3) for s in (1, -1)]
uniq = []
for s in sites:
    if not any(np.allclose(s, u) for u in uniq): uniq.append(s)
mine = [V for V, i in pieces if np.argmin([np.linalg.norm(V.mean(0) - u) for u in uniq]) == min(range(len(uniq)), key=lambda j: np.linalg.norm(uniq[j] - site))]
U = np.vstack(mine); hU = ConvexHull(U); vs = sum(ConvexHull(V).volume for V in mine)
convex = abs(hU.volume - vs) < 1e-9
gap_share = 0.335695 / 3
out = [f'partner site at a square-face centre; {len(mine)} gap pieces assigned (by nearest site); union volume {vs:.6f} (a third of the gap per OCD would be {gap_share:.6f})',
       f'union convex: {convex} (hull {hU.volume:.6f} vs pieces {vs:.6f})']
def faces(P):
    h = ConvexHull(P); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    res = []
    for e in pl:
        idx = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7]; Qp = P[idx]
        hh = ConvexHull(Qp @ np.linalg.svd(Qp - Qp.mean(0))[2][:2].T); C = Qp[hh.vertices]
        Lw = [np.linalg.norm(C[i] - C[(i + 1) % len(C)]) for i in range(len(C))]
        res.append('rhombus' if len(C) == 4 and max(Lw) - min(Lw) < 1e-7 else 'regular hexagon' if len(C) == 6 and max(Lw) - min(Lw) < 1e-7 else f'{len(C)}-gon')
    return res
fs = faces(np.unique(np.round(U, 9), axis=0))
out.append(f'hull of the union: {len(fs)} faces: ' + ', '.join(f'{fs.count(k)} {k}' for k in sorted(set(fs))))
print('\n'.join(out)); open('data/partner.txt', 'w').write('\n'.join(out) + '\n')

# Where partners meet: faces of this partner's pieces that are shared with pieces of OTHER partners, grouped by plane; for each
# plane, the merged contact polygon (union of the face polygons) and its shape. Faces lying on an OCD face are contacts with the OCD.
def face_polys(P):
    h = ConvexHull(P); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    return [(e, P[[i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7]]) for e in pl]
site_of = lambda V: min(range(len(uniq)), key=lambda j: np.linalg.norm(V.mean(0) - uniq[j]))
me = min(range(len(uniq)), key=lambda j: np.linalg.norm(uniq[j] - site))
others = [V for V, i in pieces if site_of(V) != me]
O = np.array(json.load(open('data/network.json'))['ocd'])
ocd_planes = []
for c in cells:
    for e in ConvexHull(O + c).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in ocd_planes): ocd_planes.append(e)
from collections import defaultdict
iface, ocdc = defaultdict(list), defaultdict(list)
for V in mine:
    for e, Pf in face_polys(V):
        if any(np.allclose(e, q, atol=1e-7) for q in ocd_planes): ocdc[tuple(np.round(e, 6))].append(Pf); continue
        for W in others:
            for e2, P2 in face_polys(W):
                if np.allclose(e[:3], -e2[:3], atol=1e-7) and abs(e[3] + e2[3]) < 1e-7: iface[tuple(np.round(e, 6))].append(Pf)
def shape(polys, e):
    pts = np.vstack(polys); n = np.array(e[:3]); b = np.linalg.svd(pts - pts.mean(0))[2][:2]
    xy = (pts - pts.mean(0)) @ b.T; h = ConvexHull(xy); C = xy[h.vertices]
    area_sum = sum(ConvexHull(((p - pts.mean(0)) @ b.T)).volume for p in polys)
    Lw = [np.linalg.norm(C[i] - C[(i + 1) % len(C)]) for i in range(len(C))]
    ang = [np.degrees(np.arccos(np.clip(np.dot(C[i - 1] - C[i], C[(i + 1) % len(C)] - C[i]) / np.linalg.norm(C[i - 1] - C[i]) / np.linalg.norm(C[(i + 1) % len(C)] - C[i]), -1, 1))) for i in range(len(C))]
    kind = 'rhombus' if len(C) == 4 and max(Lw) - min(Lw) < 1e-6 else f'{len(C)}-gon'
    return kind, abs(h.volume - area_sum) < 1e-9, [round(x, 4) for x in Lw], [round(x, 2) for x in ang]
out2 = [f'faces where this partner meets other partners: {len(iface)} planes']
for e, polys in iface.items():
    k, conv, Lw, ang = shape(polys, e); out2.append(f'   {k} (merged polygon {"convex" if conv else "NOT convex"}), sides {Lw}, angles {ang}')
out2.append(f'faces where it meets the OCDs: {len(ocdc)} planes, ' + ', '.join(sorted(shape(p, e)[0] for e, p in ocdc.items())))
print('\n'.join(out2)); open('data/partner.txt', 'a').write('\n'.join(out2) + '\n')
