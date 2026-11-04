#!/usr/bin/env python3
"""Do the centre pyramids of the rhombic triacontahedron (RT) tile space? (Concordance gap G2; DICTO 4 Nov 2026 "continue with other important research")
The RT pyramid's dihedral angles are 72 deg (base edges: half the RT's 144), 72 deg (lateral edges to 5-fold corners) and 120 deg (lateral edges to 3-fold corners).
All are multiples of 24 deg; 360 = 15 x 24 needs five 72s or three 120s; 180 = 7.5 x 24 is impossible, so no edge lies inside a face of another tile.
Search (edge-to-edge assumption: tiles meeting along an edge share the whole edge): every edge of a placed piece needs its other sectors (4 of 72 deg, or 2 of 120)
filled by a piece having that same segment as an edge of the same kind; candidates = the piece rotated by k sectors, with the four symmetries of a sector
(identity, swap ends, swap the two faces, both). Overlap: separating axes. Depth-first; reports if every branch dies (no edge-to-edge tiling) or the depth reached."""
import itertools, math, sys, json, os
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
EPS = 1e-9; phi = (1 + 5**.5)/2
# RT = polar of the icosidodecahedron
ID = [p for p in {tuple(s*x for s, x in zip(sg, q)) for q in itertools.permutations((phi, 0, 0)) for sg in itertools.product((1, -1), repeat=3)}]
for k in range(3):
    for sg in itertools.product((1, -1), repeat=3):
        v = [0, 0, 0]; v[k] = sg[0]*0.5; v[(k+1) % 3] = sg[1]*phi/2; v[(k+2) % 3] = sg[2]*phi**2/2; ID.append(tuple(v))
ID = np.unique(np.round(np.array(ID, float), 12), axis=0)
H = np.array([[*v, -1.0] for v in ID]); RTV = np.unique(np.round(HalfspaceIntersection(H, np.zeros(3)).intersections, 10), axis=0)
n0 = ID[0]; F = np.array([v for v in RTV if abs(v @ n0 - 1) < 1e-8]); c = F.mean(0); u = F[0] - c; w = np.cross(n0, u)
F = F[np.argsort([math.atan2((p - c) @ w, (p - c) @ u) for p in F])]
P0 = np.array([np.zeros(3), *F])
KIND = sys.argv[3] if len(sys.argv) > 3 else 'RT'
if KIND == 'C6': P0 = np.array([np.zeros(3), (.5, .5, .5), (.5, -.5, .5), (.5, -.5, -.5), (.5, .5, -.5)])
if KIND == 'RD': P0 = np.array([np.zeros(3), (1., 0, 0), (.5, .5, .5), (0, 1., 0), (.5, .5, -.5)])
def hull_info(t):
    h = ConvexHull(t); return [eq[:3] for eq in h.equations], [t[j] - t[i] for s in h.simplices for i, j in itertools.combinations(s, 2)]
def overlap(a, b):
    aa, ea = hull_info(a); ab, eb = hull_info(b); cand = aa + ab
    for x in ea:
        for y in eb:
            cc = np.cross(x, y); n = np.linalg.norm(cc)
            if n > 1e-12: cand.append(cc/n)
    for n in cand:
        pa, pb = a @ n, b @ n
        if min(pa.max() - pb.min(), pb.max() - pa.min()) <= EPS: return False
    return True
def same(a, b): return np.allclose(a[0], b[0], atol=1e-7) and all(np.min(np.linalg.norm(b - p, axis=1)) < 1e-7 for p in a)
def edges_of(t):
    """true edges (i, j) of the pyramid with their dihedral angle"""
    h = ConvexHull(t); fn = {}
    for s, eq in zip(h.simplices, h.equations):
        for i, j in itertools.combinations(sorted(s), 2): fn.setdefault((i, j), []).append(eq[:3])
    out = []
    for (i, j), ns in fn.items():
        if len(ns) == 2 and np.linalg.norm(ns[0] - ns[1]) > 1e-6:
            dih = math.pi - math.acos(max(-1, min(1, ns[0] @ ns[1]))); out.append((i, j, dih))
    return out
def rot(Pp, X, Y, ang):
    k = (Y - X)/np.linalg.norm(Y - X); c_, s_ = math.cos(ang), math.sin(ang)
    return np.array([X + (p - X)*c_ + np.cross(k, p - X)*s_ + k*(k @ (p - X))*(1 - c_) for p in Pp])
def refl_perp(Pp, X, Y):
    m = (X + Y)/2; k = (Y - X)/np.linalg.norm(Y - X); return np.array([p - 2*((p - m) @ k)*k for p in Pp])
def refl_plane(Pp, X, n):
    return np.array([p - 2*((p - X) @ n)*n for p in Pp])
E0 = edges_of(P0)
kinds = sorted({(round(np.linalg.norm(P0[i] - P0[j]), 6), round(math.degrees(d), 4), 'lateral' if 0 in (i, j) else 'base') for i, j, d in E0})
print('RT pyramid edges (length, dihedral deg, kind):', kinds)
def sector_candidates(t, i, j, dih):
    X, Y = t[i], t[j]; m = int(round(2*math.pi/dih)); out = []
    # the half-plane through the edge containing t's two faces: get unit normal of t's faces at this edge via a rotation trick
    for k in range(1, m):
        base = rot(t, X, Y, k*dih)
        # bisector plane of that sector: contains line XY, at angle (k+1/2)*dih from t's sector middle -> use mid-direction
        axis = (Y - X)/np.linalg.norm(Y - X); h = ConvexHull(t); ns = []
        for sm, eq in zip(h.simplices, h.equations):
            if i in sm and j in sm and not any(np.allclose(eq[:3], q) for q in ns): ns.append(eq[:3])
        r0 = -(ns[0] + ns[1]); r0 = r0 - axis*(r0 @ axis); r0 /= np.linalg.norm(r0)   # middle of t's own wedge
        mid = rot(np.array([X + r0]), X, Y, k*dih)[0] - X; nplane = np.cross(axis, mid); nplane /= np.linalg.norm(nplane)
        vs = [base, refl_perp(base, X, Y), refl_plane(base, X, nplane), refl_perp(refl_plane(base, X, nplane), X, Y)]
        uniq = []
        for v in vs:
            if not any(same(v, q) for q in uniq): uniq.append(v)
        out.append(uniq)
    return out
import time
def progress(tiles, st):
    if len(tiles) > st.get('best', 0):
        st['best'] = len(tiles); ap = {}
        for t in tiles: k = tuple(np.round(t[0], 6)); ap[k] = ap.get(k, 0) + 1
        st['best_patch'] = {'pieces': len(tiles), 'centres': len(ap), 'pieces_per_centre': sorted(ap.values(), reverse=True)}
        json.dump({'best': st['best_patch'], 'tiles': [t.tolist() for t in tiles]}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'{KIND}-best-{st["maxd"]}.json'), 'w'))
    if st['nodes'] % 50000 == 0:
        print(f"[{time.time() - st['t0']:.0f} s] nodes {st['nodes']}, deepest patch {st.get('best', 0)} pieces, {st.get('best_patch', {}).get('centres')} centres", flush=True)
def search(tiles, todo, maxd, st):
    st['nodes'] += 1; progress(tiles, st)
    if st['nodes'] > st['cap']: st['capped'] = True; return True
    if len(tiles) >= maxd:
        ap = {}
        for t in tiles: k = tuple(np.round(t[0], 6)); ap[k] = ap.get(k, 0) + 1
        st['cluster'] = {'pieces': len(tiles), 'apexes': len(ap), 'pieces_per_apex': sorted(ap.values(), reverse=True)}
        return True
    while todo:
        ti, i, j, dih, k = todo[0]; cs = sector_candidates(tiles[ti], i, j, dih)[k]
        if any(same(c, u) for c in cs for u in tiles): todo = todo[1:]; continue
        for c in cs:
            if any(overlap(c, u) for u in tiles): continue
            n = len(tiles); E = edges_of(c)
            if search(tiles + [c], todo[1:] + [(n, a, b, d, kk) for a, b, d in E for kk in range(int(round(2*math.pi/d)) - 1)], maxd, st): return True
        return False
    return True
maxd = int(sys.argv[1]) if len(sys.argv) > 1 else 40
st = {'nodes': 0, 'cap': int(sys.argv[2]) if len(sys.argv) > 2 else 200000, 'capped': False, 't0': time.time(), 'maxd': maxd}
todo = [(0, a, b, d, kk) for a, b, d in E0 for kk in range(int(round(2*math.pi/d)) - 1)]
ok = search([P0], todo, maxd, st)
res = {'best_patch': st.get('best_patch'), 'cluster': st.get('cluster'), 'edge_kinds': kinds, 'max_pieces': maxd, 'some_branch_reaches_max': ok, 'nodes': st['nodes'], 'capped': st['capped']}
print(res)
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'), exist_ok=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'{KIND}-search-{maxd}.json'), 'w'), indent=1)
