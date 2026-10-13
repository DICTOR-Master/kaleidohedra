# How many stages lie between start and finish (DICTO 2026-10-13: "how many more stages there are"). A stage: the centre plus any
# set of whole piece groups (all the pieces of one kind at one distance: a full symmetric ring) that is one connected solid, each
# group touching the rest face to face. Counts them, and how many of them are convex.
import os, sys, json, itertools
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA
from steps import plane
from shapely.geometry import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))


def faces_of(P, F):
    pc = P.mean(0)
    return [(P[f], *plane(P, f, pc)) for f in F]


def touch(fa, fb):
    """Do two pieces share face area (coplanar, opposite normals, overlapping)?"""
    for qa, na, da in fa:
        for qb, nb, db in fb:
            if np.allclose(na, -nb, atol=1e-4) and abs(da + db) < 1e-4:
                u = np.cross(na, [1, 0, 0] if abs(na[0]) < 0.9 else [0, 1, 0]); u /= np.linalg.norm(u); v = np.cross(na, u)
                A = Polygon([(p @ u, p @ v) for p in qa]).buffer(0); B = Polygon([(p @ u, p @ v) for p in qb]).buffer(0)
                if A.intersection(B).area > 1e-6: return True
    return False


def run(view):
    pieces = DATA[view]
    allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
    groups = {}
    for r, V, F in pieces:
        P = np.array(V, float) - c0
        groups.setdefault(f'{r}@{np.linalg.norm(P.mean(0)):.2f}', []).append((P, F))
    names = sorted(groups, key=lambda g: np.mean([np.linalg.norm(P.mean(0)) for P, _ in groups[g]]))
    centre = names[0]
    F = {g: [faces_of(P, Fc) for P, Fc in groups[g]] for g in names}
    vol = {g: sum(ConvexHull(P).volume for P, _ in groups[g]) for g in names}
    # contact graph between groups (a quick box test first)
    box = {g: (np.vstack([P for P, _ in groups[g]]).min(0), np.vstack([P for P, _ in groups[g]]).max(0)) for g in names}
    edges = set()
    for a, b in itertools.combinations(names, 2):
        if np.any(box[a][1] < box[b][0] - 1e-6) or np.any(box[b][1] < box[a][0] - 1e-6): continue
        if any(touch(fa, fb) for fa in F[a] for fb in F[b]): edges.add((a, b)); edges.add((b, a))
    others = names[1:]
    stages, convex, every = 0, [], []
    for n in range(0, len(others) + 1):
        for S in itertools.combinations(others, n):
            S = (centre,) + S
            # connected from the centre
            seen, todo = {centre}, [centre]
            while todo:
                x = todo.pop()
                for y in S:
                    if y not in seen and (x, y) in edges: seen.add(y); todo.append(y)
            if len(seen) != len(S): continue
            stages += 1
            every.append(list(S))
            P = np.vstack([P for g in S for P, _ in groups[g]])
            if abs(ConvexHull(P).volume - sum(vol[g] for g in S)) < 1e-5 * sum(vol[g] for g in S): convex.append(S)
    return {'view': view, 'groups': len(names), 'contacts': len(edges) // 2, 'stages': stages, 'convexStages': len(convex),
            'convex': [list(S) for S in convex], 'catalogued': len(names), 'all': every}


if __name__ == '__main__':
    out = [run(v) for v in DATA]
    json.dump(out, open(os.path.join(HERE, '..', 'stages.json'), 'w'), indent=1)
    for R in out:
        print(f"{R['view']}: {R['groups']} groups, {R['stages']} connected stages ({R['convexStages']} convex); catalogue shows {R['catalogued']}")
