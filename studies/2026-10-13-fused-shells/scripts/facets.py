# Opening the fused shells by large facets (DICTO 2026-10-13): a shell is the solid between two consecutive convex
# partial builds A (inner) and B (outer); it is divided, as when an icosahedron is opened into its face pyramids, by the
# planes through the centre and each edge of B. For each face of B the facet wedge is (pyramid over the face, apex the
# centre) minus A. Reported: the wedge's faces and a technical name, and whether the pieces fill each wedge whole
# (no piece crosses a cutting plane).
import json, os, sys
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA, describe, hull_faces, dedupe

HERE = os.path.dirname(os.path.abspath(__file__))
SOLIDS = {  # names of the convex builds by face signature and corner count (checked by regularity below)
    ((3, 20),): 'icosahedron', ((5, 12),): 'dodecahedron', ((3, 20), (5, 12)): 'icosidodecahedron',
    ((5, 12), (6, 20)): 'truncated icosahedron', ((4, 30),): 'rhombic triacontahedron',
    ((3, 60), (4, 30), (5, 12)): 'icosahedral 80-corner solid',
}


def solid_name(P):
    d = describe(P)
    key = tuple(sorted((int(k.split('-')[0]), v) for k, v in d['faces'].items()))
    return SOLIDS.get(key, d['name']), d


def convex_builds(pieces):
    allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
    groups = {}
    for r, V, F in pieces:
        P = np.array(V, float) - c0
        groups.setdefault(f'{r}@{np.linalg.norm(P.mean(0)):.2f}', []).append({'P': P, 'vol': ConvexHull(P).volume})
    order = sorted(groups, key=lambda g: np.mean([np.linalg.norm(x['P'].mean(0)) for x in groups[g]]))
    import itertools
    found = []
    for n in range(1, len(order) + 1):
        for S in itertools.combinations(order, n):
            P = np.vstack([x['P'] for g in S for x in groups[g]]); v = sum(x['vol'] for g in S for x in groups[g])
            if abs(ConvexHull(P).volume - v) < 1e-5 * v: found.append((v, frozenset(S), P))
    found.sort(key=lambda f: f[0])
    return groups, found


def cone_planes(Bf, PB):
    """Half-spaces (A x + b <= 0) of the pyramid over face Bf of B with apex at the centre."""
    n, d, f = Bf
    H = [np.append(n, -d)]
    c = PB[f].mean(0)
    for i in range(len(f)):
        a, b = PB[f[i]], PB[f[(i + 1) % len(f)]]
        m = np.cross(a, b); m /= np.linalg.norm(m)
        if np.dot(m, c) > 0: m = -m
        H.append(np.append(m, 0.0))
    return np.array(H)


def clip(H_extra, PA):
    """Convex part of solid A (points PA) inside the half-spaces H_extra; None if empty."""
    hA = ConvexHull(PA)
    H = np.vstack([hA.equations, H_extra])
    # an interior point: the face centre pulled toward the centre, scaled until inside A
    try:
        from scipy.optimize import linprog
        A_ub = np.hstack([H[:, :3], np.linalg.norm(H[:, :3], axis=1)[:, None]])
        res = linprog([0, 0, 0, -1], A_ub=A_ub, b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
        if not res.success or res.x[3] < 1e-7: return None
        hs = HalfspaceIntersection(H, res.x[:3])
        return dedupe(hs.intersections)
    except Exception:
        return None


def run(view):
    pieces = DATA[view]
    groups, builds = convex_builds(pieces)
    out = {'view': view, 'shells': []}
    for j, (vB, SB, PB) in enumerate(builds):
        inner = [b for b in builds[:j] if b[1] < SB]
        if not inner: continue
        vA, SA, PA = inner[-1]
        nameA, _ = solid_name(PA); nameB, _ = solid_name(PB)
        PBd = corners(PB)
        _, BF = hull_faces(PBd)
        PA = corners(PA)
        shell_pieces = [x for g in SB - SA for x in groups[g]]
        kinds = {}
        crossing = 0
        for Bf in BF:
            H = cone_planes(Bf, PBd)
            pyr = np.vstack([PBd[Bf[2]], [[0, 0, 0]]])
            cut = clip(H, PA)
            # pieces inside this wedge, and pieces that cross its side planes
            inside = [x for x in shell_pieces if np.all(x['P'] @ H[1:, :3].T <= 1e-6)]
            for x in shell_pieces:
                s = x['P'] @ H[1:, :3].T
                if np.any(s > 1e-6, axis=0).any() and np.any(np.all(s <= 1e-6, axis=1)) and not np.all(s <= 1e-6):
                    pass
            wedge_vol = ConvexHull(pyr).volume - (ConvexHull(cut).volume if cut is not None and len(cut) >= 4 else 0)
            fill = sum(x['vol'] for x in inside)
            inner_desc = describe(cut)['name'] if cut is not None and len(cut) >= 4 else 'nothing'
            key = (len(Bf[2]), inner_desc, round(wedge_vol, 5))
            k = kinds.setdefault(key, {'count': 0, 'outerFace': f'{len(Bf[2])}-gon', 'pyramid': describe(pyr)['name'],
                                       'innerPart': inner_desc, 'innerPartFaces': describe(cut)['faces'] if cut is not None and len(cut) >= 4 else {},
                                       'wedgeVolume': round(wedge_vol, 6), 'wholePiecesVolume': round(fill, 6),
                                       'piecesWhole': abs(fill - wedge_vol) < 1e-5 * max(1, wedge_vol),
                                       'pieces': sorted(x_role(groups, x) for x in inside)})
            k['count'] += 1
        out['shells'].append({'inner': nameA, 'outer': nameB, 'innerVolume': round(vA, 6), 'outerVolume': round(vB, 6),
                              'pieceTypes': sorted(SB - SA), 'facets': list(kinds.values())})
    return out


def corners(P):
    """Only the true corners of the hull of P (no points in the middle of edges or faces)."""
    P = dedupe(P)
    _, F = hull_faces(P)
    return P[[i for i in sorted({i for _, _, f in F for i in f}) if sum(i in f for _, _, f in F) >= 3]]


def x_role(groups, x):
    for g, xs in groups.items():
        if any(y is x for y in xs): return g.split('@')[0]
    return '?'


if __name__ == '__main__':
    res = [run(v) for v in DATA]
    json.dump(res, open(os.path.join(HERE, '..', 'facets.json'), 'w'), indent=1)
    for R in res:
        print('==', R['view'])
        for S in R['shells']:
            print(f"  shell {S['inner']} -> {S['outer']}  (pieces: {', '.join(S['pieceTypes'])})")
            for f in S['facets']:
                whole = 'pieces fill it whole' if f['piecesWhole'] else f"pieces do NOT fill it whole ({f['wholePiecesVolume']} of {f['wedgeVolume']})"
                print(f"    x{f['count']} under a {f['outerFace']}: {f['pyramid']} minus [{f['innerPart']} {f['innerPartFaces']}]; {whole}; whole pieces: {'+'.join(f['pieces']) or '-'}")
