# TI Star, exhaustive (DICTO 10-30: "are you really sure the cycle can not progress through any more solids/hulls?").
# One turn is made of 9 symmetric families of pieces: TI; 12 pentagonal spikes; 20 hexagonal spikes; layer 1: 60 corner tetrahedra,
# 60 pentagon-hexagon edge tetrahedra, 30 hexagon-hexagon edge tetrahedra; layer 2: the same three. Every solid made of whole families
# and containing TI (2^8 = 256 unions) is built; for each: volume, whether it is convex (volume = hull volume), and its hull. Distinct
# solids and distinct hulls are listed with their nesting. Then DICTO's growth rule of The Golden Cycle (each corner of a solid gives
# a face plane of the next: the plane through the corner at right angles to its radius) is applied to every convex solid found.
import json, itertools, os, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
SCN = os.environ.get('SCALE', 'phi'); phi = (1 + 5 ** .5) / 2; s = {'2': 2.0, 'phi': phi}[SCN]
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
h = ConvexHull(P); F = []; seen = set()
for eq in h.equations:
    k = tuple(np.round(eq, 7))
    if k in seen: continue
    seen.add(k); F.append([i for i, p in enumerate(P) if abs(eq[:3] @ p + eq[3]) < 1e-8])
VT = h.volume
tip = [s * P[f].mean(0) for f in F]
e = min(np.linalg.norm(P[0] - P[j]) for j in range(1, len(P)))
E = [(i, j) for i, j in itertools.combinations(range(len(P)), 2) if abs(np.linalg.norm(P[i] - P[j]) - e) < 1e-9]
fa = {v: [fi for fi, f in enumerate(F) if v in f] for v in range(len(P))}
def ekind(i, j): return 'ph' if sorted(len(F[x]) for x in fa[i] if x in fa[j]) == [5, 6] else 'hh'
fam = {'TI': [P],
       'pent spikes': [np.vstack([P[f], tip[fi]]) for fi, f in enumerate(F) if len(f) == 5],
       'hex spikes': [np.vstack([P[f], tip[fi]]) for fi, f in enumerate(F) if len(f) == 6],
       'L1 corner': [np.array([P[v]] + [tip[f] for f in fa[v]]) for v in range(len(P))],
       'L1 edge ph': [np.array([P[i], P[j]] + [tip[f] for f in fa[i] if f in fa[j]]) for i, j in E if ekind(i, j) == 'ph'],
       'L1 edge hh': [np.array([P[i], P[j]] + [tip[f] for f in fa[i] if f in fa[j]]) for i, j in E if ekind(i, j) == 'hh'],
       'L2 corner': [np.array([s * P[v]] + [tip[f] for f in fa[v]]) for v in range(len(P))],
       'L2 edge ph': [np.array([s * P[i], s * P[j]] + [tip[f] for f in fa[i] if f in fa[j]]) for i, j in E if ekind(i, j) == 'ph'],
       'L2 edge hh': [np.array([s * P[i], s * P[j]] + [tip[f] for f in fa[i] if f in fa[j]]) for i, j in E if ekind(i, j) == 'hh']}
vol = {k: sum(ConvexHull(Q).volume for Q in v) for k, v in fam.items()}
names = list(fam)[1:]
def faceinfo(Q):
    hq = ConvexHull(Q); planes = {}
    for eq in hq.equations: planes.setdefault(tuple(np.round(eq, 6)), eq)
    V = Q[hq.vertices]; kinds = {}
    for eq in planes.values():
        n = sum(1 for p in V if abs(eq[:3] @ p + eq[3]) < 1e-7); kinds[n] = kinds.get(n, 0) + 1
    return len(V), dict(sorted(kinds.items())), np.array(list(planes.values()))
solids = []
for r in range(len(names) + 1):
    for sub in itertools.combinations(names, r):
        parts = fam['TI'] + [Q for n in sub for Q in fam[n]]
        V = vol['TI'] + sum(vol[n] for n in sub)
        pts = np.vstack(parts); hv = ConvexHull(pts).volume
        nv, kinds, _ = faceinfo(pts)
        solids.append(dict(families=('TI',) + sub, volume=V / VT, hull_volume=hv / VT, convex=abs(hv - V) < 1e-9 * hv,
                           hull_corners=nv, hull_faces=kinds))
conv = [x for x in solids if x['convex']]
hulls = {}
for x in solids: hulls.setdefault((round(x['hull_volume'], 7), x['hull_corners'], json.dumps(x['hull_faces'])), []).append(x['families'])
# growth rule: from each distinct convex solid, the solid whose face planes pass through its corners at right angles to the radii
def grow(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; n = V / np.linalg.norm(V, axis=1)[:, None]
    H = np.hstack([n, -np.linalg.norm(V, axis=1)[:, None]])
    W = HalfspaceIntersection(H, np.zeros(3)).intersections; return W[ConvexHull(W).vertices]
distinct_hull_pts = {}
for x in solids:
    key = (round(x['hull_volume'], 7), x['hull_corners'])
    if key not in distinct_hull_pts:
        parts = [Q for n in x['families'] for Q in fam[n]]; distinct_hull_pts[key] = np.vstack(parts)
grown = []
for key, pts in sorted(distinct_hull_pts.items()):
    G = grow(pts); nv, kinds, _ = faceinfo(G); gv = ConvexHull(G).volume / VT
    match = [k2 for k2 in distinct_hull_pts if abs(k2[0] - gv) < 1e-6]
    grown.append(dict(from_hull_volume=key[0], from_corners=key[1], grown_volume=round(gv, 6), grown_corners=nv, grown_faces=kinds,
                      equals_a_hull_of_the_turn=bool(match), over_sTI=round(gv / s ** 3, 6)))
out = dict(scale=SCN, family_volumes={k: round(v / VT, 6) for k, v in vol.items()}, unions=len(solids),
           convex_unions=[dict(families=x['families'], volume=round(x['volume'], 6), corners=x['hull_corners'], faces=x['hull_faces']) for x in conv],
           distinct_hulls=[dict(volume=k[0], corners=k[1], faces=json.loads(k[2]), made_by=len(v), example=v[0]) for k, v in sorted(hulls.items())],
           growth_rule=grown)
json.dump(out, open(f'data/families-{SCN}.json', 'w'), indent=1, ensure_ascii=False)
print('unions', len(solids), 'convex', len(conv), 'distinct hulls', len(hulls))
for x in conv: print(' convex:', round(x['volume'], 6), x['hull_corners'], x['hull_faces'], '+'.join(x['families'][1:]) or 'TI only')
for k, v in sorted(hulls.items()): print(' hull', k[0], k[1], k[2], 'from', len(v), 'unions')
for g in grown: print(' grow', g)
