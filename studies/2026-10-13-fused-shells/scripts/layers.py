# Which partial builds are convex solids: add piece types (roles) from the centre outwards, every order consistent with
# their mean radius, and report each convex union (these are the classic solids the layers run between).
import json, os, itertools
import numpy as np
from scipy.spatial import ConvexHull
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fuse import DATA, describe
for view, pieces in DATA.items():
    allP = np.array([p for _, V, _ in pieces for p in V], float); c0 = allP.mean(0)
    roles = {}
    for r, V, F in pieces:
        P = np.array(V, float) - c0
        roles.setdefault(f'{r}@{np.linalg.norm(P.mean(0)):.2f}', []).append((P, ConvexHull(P).volume))
    order = sorted(roles, key=lambda r: np.mean([np.linalg.norm(P.mean(0)) for P, _ in roles[r]]))
    print('==', view, 'roles by radius:', order)
    # every subset closed downward is too many; test all subsets of up to all roles, cheap enough for <=12 roles
    found = []
    for n in range(1, len(order) + 1):
        for S in itertools.combinations(order, n):
            P = np.vstack([P for r in S for P, _ in roles[r]]); v = sum(v for r in S for _, v in roles[r])
            h = ConvexHull(P)
            if abs(h.volume - v) < 1e-5 * h.volume:
                found.append((h.volume, S, describe(P)))
    for vol, S, d in sorted(found):
        print(f"  vol {vol:9.4f}  {'+'.join(S)}  ->  {d['name']} {d['faces']} V{d['V']}")
