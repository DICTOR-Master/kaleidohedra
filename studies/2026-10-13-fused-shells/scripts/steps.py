# What each step becomes (DICTO 2026-10-13): build each structure outwards one piece type at a time (by distance from the
# centre) and describe the whole build as ONE solid: its outer surface (faces of the union, coplanar neighbours merged),
# corners, convex or not, and which face planes it uses (icosahedron/dodecahedron/triacontahedron planes = a stellation).
import os, sys, json
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA

HERE = os.path.dirname(os.path.abspath(__file__))
PHI = (1 + 5 ** 0.5) / 2
AXES = {  # unit normals of the icosahedral face-plane families
    '5-fold (dodecahedron planes)': [(0, 1, PHI), (0, -1, PHI), (1, PHI, 0), (-1, PHI, 0), (PHI, 0, 1), (-PHI, 0, 1)],
    '3-fold (icosahedron planes)': [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (0, 1 / PHI, PHI), (0, -1 / PHI, PHI), (1 / PHI, PHI, 0), (-1 / PHI, PHI, 0), (PHI, 0, 1 / PHI), (-PHI, 0, 1 / PHI)],
    '2-fold (triacontahedron planes)': [(1, 0, 0), (0, 1, 0), (0, 0, 1)] + [s for a, b, c in [(1, PHI, PHI ** 2)] for s in
        [(a, b, c), (-a, b, c), (a, -b, c), (a, b, -c), (b, c, a), (-b, c, a), (b, -c, a), (b, c, -a), (c, a, b), (-c, a, b), (c, -a, b), (c, a, -b)]],
}


def plane(P, f, pc):
    a, b, c = P[f[0]], P[f[1]], P[f[2]]
    n = np.cross(b - a, c - a); n /= np.linalg.norm(n)
    if np.dot(n, a - pc) < 0: n = -n
    return n, float(np.dot(n, a))


def key_pt(p): return tuple(np.round(p, 5))


GAP = 2e-4  # well above the data's rounding, far below any real edge (shortest edges here are > 0.05)


def describe_union(pieces):
    """The union of the pieces as one solid, counted with build_transitional's face builder (Fable's check, 2026-10-13: faces that
    only touch at a corner must not merge): each piece face's visible part, neighbours in one plane merged while the face stays
    convex. So a face is a convex face of the solid (a star-shaped face would count as its convex parts; none occurs among the
    named stages). Planes: the distinct planes those faces lie in."""
    import build_transitional as bt
    V, F, _, holes, vol_surface, _ = bt.fused_polyhedron([('solid', P, Fc) for P, Fc in pieces])
    allP = np.vstack([P for P, _ in pieces])
    vol = sum(ConvexHull(P).volume for P, _ in pieces)
    hull = ConvexHull(allP)
    convex = bool(abs(hull.volume - vol) < 1e-5 * vol)
    if convex:  # a convex stage's faces are exactly its hull's faces (coplanar triangles merged), corners only
        from fuse import hull_faces, dedupe
        Q = dedupe(allP)
        _, HF = hull_faces(Q)
        keep = [i for i in sorted({i for _, _, f in HF for i in f}) if sum(i in f for _, _, f in HF) >= 3]
        V = Q[keep]
        _, HF = hull_faces(V)
        F = [f for _, _, f in HF]
    sides, planes, fams = {}, [], {}
    for f in F:
        sides[len(f)] = sides.get(len(f), 0) + 1
        a, b, c = V[f[0]], V[f[1]], V[f[2]]
        n = np.cross(b - a, c - a); n = n / np.linalg.norm(n); d = float(np.dot(n, a))
        if not any(np.allclose(n, q[0], atol=1e-4) and abs(d - q[1]) < 1e-3 for q in planes):
            planes.append((n, d))
            fam = next((name for name, ax in AXES.items() if any(abs(abs(np.dot(n, x)) - 1) < 1e-4 for x in ax)), 'other')
            fams.setdefault(fam, set()).add(round(d, 4))
    return {'faces': len(F), 'planes': len(planes), 'faceShapes': {f'{k}-gon': v for k, v in sorted(sides.items())},
            'planeFamilies': {k: sorted(v) for k, v in fams.items()}, 'holesInFaces': holes,
            'convex': convex, 'volume': round(vol, 5), 'radius': round(float(np.linalg.norm(allP, axis=1).max()), 4)}


def corners2d(pts):
    """Number of true corners of a 2D polygon (points along a straight edge dropped)."""
    q = []
    for p in pts:
        if not q or np.hypot(p[0] - q[-1][0], p[1] - q[-1][1]) > 1e-4: q.append(p)
    if len(q) > 1 and np.hypot(q[0][0] - q[-1][0], q[0][1] - q[-1][1]) <= 1e-4: q.pop()
    pts = q
    k, n = 0, len(pts)
    for i in range(n):
        a, b, c = np.array(pts[i - 1]), np.array(pts[i]), np.array(pts[(i + 1) % n])
        u, v = b - a, c - b
        if np.linalg.norm(u) > 1e-5 and np.linalg.norm(v) > 1e-5 and abs(u[0] * v[1] - u[1] * v[0]) > 2e-3 * np.linalg.norm(u) * np.linalg.norm(v): k += 1
    return k


def area(poly):
    c = poly.mean(0)
    return sum(np.linalg.norm(np.cross(poly[i] - c, poly[(i + 1) % len(poly)] - c)) / 2 for i in range(len(poly)))


def set_axes(groups):
    """Symmetry axes of the data itself, from the icosahedron (Karma, Dharma) or triacontahedron (Bodhi) at the centre:
    corner directions, face normals and edge-midpoint directions, named by how many faces meet / sides there are."""
    P, F = min((x for xs in groups.values() for x in xs), key=lambda x: np.linalg.norm(x[0].mean(0)))
    from scipy.spatial import ConvexHull
    h = ConvexHull(P)
    u = lambda v: v / np.linalg.norm(v)
    corner = [u(p) for p in P]
    normal = [u(e[:3]) for e in h.equations]
    edge = [u((P[a] + P[b]) / 2) for a in range(len(P)) for b in range(a + 1, len(P)) if abs(np.linalg.norm(P[a] - P[b]) - min(np.linalg.norm(P[i] - P[j]) for i in range(len(P)) for j in range(i + 1, len(P)))) < 1e-4]
    AXES.clear()
    AXES.update({'5-fold': [], '3-fold': [], '2-fold': edge})
    for v in corner + normal:
        k = sum(abs(np.dot(v, w) - np.dot(v, v)) < 1e-6 for w in [v])  # placeholder, classified below
    # classify corner/normal directions by their symmetry: count faces of the centre solid touching the corner
    ico = len(P) == 12
    AXES['5-fold' if ico else '3-fold'].extend(corner if ico else [])
    AXES['3-fold' if ico else '5-fold'].extend(normal if ico else [])
    if not ico:  # triacontahedron: corners are 5-fold (12) and 3-fold (20); face normals are 2-fold
        r = np.linalg.norm(P, axis=1)
        AXES['5-fold'] = [u(p) for p, ri in zip(P, r) if ri > r.mean()]
        AXES['3-fold'] = [u(p) for p, ri in zip(P, r) if ri <= r.mean()]
        AXES['2-fold'] = normal
    AXES['2-fold'] = AXES['2-fold'] or edge


if __name__ == '__main__':
    out = {}
    for view, pieces in DATA.items():
        allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
        groups = {}
        for r, V, F in pieces:
            P = np.array(V, float) - c0
            groups.setdefault(f'{r}@{np.linalg.norm(P.mean(0)):.2f}', []).append((P, F))
        set_axes(groups)
        order = sorted(groups, key=lambda g: np.mean([np.linalg.norm(P.mean(0)) for P, _ in groups[g]]))
        print('==', view)
        built, steps = [], []
        for g in order:
            built += groups[g]
            d = describe_union(built); d['added'] = f'{g} x{len(groups[g])}'
            steps.append(d)
            print(f"  + {d['added']:<16} -> {'CONVEX' if d['convex'] else 'non-convex'}, {d['faces']} faces {d['faceShapes']}; plane distances {d['planeFamilies']}")
        out[view] = steps
    json.dump(out, open(os.path.join(HERE, '..', 'steps.json'), 'w'), indent=1)
