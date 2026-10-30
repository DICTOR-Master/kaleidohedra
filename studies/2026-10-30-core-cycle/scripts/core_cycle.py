# The TI Star core's own cycle (DICTO 10-30: "give it an equivalent hexagonal and pentagonal pyramid core and spikes and see how it
# develops"). C = D105, the icosahedron truncated at 1/phi^3 (the core of every TI Star turn, #78). Treat C exactly as #78 treated TI:
# its core = the 32 face pyramids from the centre (12 pentagonal, 20 hexagonal); spikes = the same pyramids turned out, tip at t x the
# foot of the perpendicular (t = 2 mirrored, t = phi golden). Then the turn's solids: Ip (icosahedron of the 12 pentagon tips), Dh
# (dodecahedron of the 20 hexagon tips), their intersection (the next core), the hull of the 32 tips (the next halo); shape checks
# against TI, D105 and D104; nesting; layer fills (corner pieces + edge tetrahedra, as #78) with volumes and overlaps.
import json, itertools, os, sys, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
T = os.environ.get('T', 'phi'); t = {'phi': phi, '2': 2.0}[T]
raw = json.load(open(sys.argv[1]))
TI = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def facelist(Q):
    hq = ConvexHull(Q); out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(Q) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    return list(out.values())
def pl(Q):
    u = {}
    for eq in ConvexHull(Q).equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
cut = lambda H: (lambda W: W[ConvexHull(W).vertices])(HalfspaceIntersection(H, np.zeros(3)).intersections)
def turn(P, t):
    F = facelist(P); feet = [(-eq[3]) * eq[:3] for eq, _ in F]; tips = np.array([t * f for f in feet])
    pen = np.array([tips[i] for i, (_, ids) in enumerate(F) if len(ids) == 5]); hexa = np.array([tips[i] for i, (_, ids) in enumerate(F) if len(ids) == 6])
    return F, tips, pen, hexa, cut(np.vstack([pl(pen), pl(hexa)]))
def shape(Q):
    V = Q[ConvexHull(Q).vertices]; R = np.linalg.norm(V, axis=1).max(); V = V / R
    F = facelist(V); fk = {}
    for _, ids in F: fk[len(ids)] = fk.get(len(ids), 0) + 1
    d = np.linalg.norm(V[:, None] - V[None], axis=2)
    E = sorted({round(float(d[a, b]), 6) for _, ids in F for a, b in itertools.combinations(ids, 2)
                if sum(1 for _, j in F if a in j and b in j) == 2})
    return dict(V=len(V), faces=dict(sorted(fk.items())), edges=E, radii=sorted({round(float(x), 6) for x in np.linalg.norm(V, axis=1)})), R
def same(A, B): return shape(A)[0] == shape(B)[0]
_, _, _, _, C = turn(TI, t)                        # D105 at its place in the TI turn
F0, tipsTI, _, _, _ = turn(TI, t); HALO = tipsTI   # D104
FC, tips, pen, hexa, C2 = turn(C, t)               # the core's own turn
d5 = sorted({round(float(-eq[3]), 9) for eq, ids in FC if len(ids) == 5}); d3 = sorted({round(float(-eq[3]), 9) for eq, ids in FC if len(ids) == 6})
dT5 = sorted({round(float(-eq[3]), 9) for eq, ids in F0 if len(ids) == 5}); dT3 = sorted({round(float(-eq[3]), 9) for eq, ids in F0 if len(ids) == 6})
res = dict(t=T,
  C=shape(C)[0], C_is_D105_shape=True,
  ratio_pent_over_hex_distance=dict(TI=dT5[0] / dT3[0], C=d5[0] / d3[0], product=dT5[0] / dT3[0] * d5[0] / d3[0]),
  next_core=shape(C2)[0], next_core_is_TI_shape=same(C2, TI), next_core_is_C_shape=same(C2, C),
  next_core_over_TI_scale=shape(C2)[1] / shape(TI)[1], C_over_TI_scale=shape(C)[1] / shape(TI)[1],
  hull_of_tips=shape(tips)[0], hull_of_tips_is_StarHalo_shape=same(tips, HALO),
  Ip=shape(pen)[0]['faces'], Dh=shape(hexa)[0]['faces'])
# hull of C's tips: which tips are corners (do the 12 five-fold tips stand out or sink in?)
hv = set(ConvexHull(tips).vertices.tolist()); res['tip_corners'] = dict(pentagon_tips=sum(1 for i, (_, ids) in enumerate(FC) if len(ids) == 5 and i in hv), hexagon_tips=sum(1 for i, (_, ids) in enumerate(FC) if len(ids) == 6 and i in hv))
res['tip_radii'] = dict(pentagon=float(np.linalg.norm(pen, axis=1)[0]), hexagon=float(np.linalg.norm(hexa, axis=1)[0]))
# star of C, nesting and fills (as #78: layer 1 = over each corner of C the piece to the tips of its 3 faces, over each edge the tetrahedron)
vol = lambda Q: ConvexHull(Q).volume
fa = {v: [fi for fi, (_, ids) in enumerate(FC) if v in ids] for v in range(len(C))}
E = sorted({tuple(sorted(e)) for _, ids in FC for e in itertools.combinations(ids, 2) if len([1 for _, j in FC if e[0] in j and e[1] in j]) == 2})
spikes = [np.vstack([C[ids], tips[fi]]) for fi, (_, ids) in enumerate(FC)]
L1 = [np.vstack([C[v]] + [tips[f] for f in fa[v]]) for v in range(len(C))] + [np.vstack([C[a], C[b]] + [tips[f] for f in fa[a] if f in fa[b]]) for a, b in E]
VC = vol(C); star = VC + sum(map(vol, spikes)); VH = vol(tips)
inside = lambda A, B: bool(np.all(A @ pl(B)[:, :3].T + pl(B)[:, 3] <= 1e-9))
res.update(volumes_over_C=dict(C=1, star=star / VC, hull=VH / VC), star_inside_hull=all(inside(Q, tips) for Q in spikes),
  layer1=dict(pieces=len(L1), kinds=sorted({round(vol(Q), 9) for Q in L1}), sum=sum(map(vol, L1)), needed=VH - star))
pieces = [C] + spikes + L1
def axes(Q):
    hq = ConvexHull(Q); ed = {tuple(sorted((a, b))) for sm in hq.simplices for a, b in [(sm[0], sm[1]), (sm[1], sm[2]), (sm[0], sm[2])]}
    return [eq[:3] for eq in hq.equations], [Q[b] - Q[a] for a, b in ed]
AX = [axes(Q) for Q in pieces]; Cc = [Q.mean(0) for Q in pieces]; Rr = [np.linalg.norm(Q - Q.mean(0), axis=1).max() for Q in pieces]
def sep(i, j):
    for ax in AX[i][0] + AX[j][0] + [np.cross(u, v) for u in AX[i][1] for v in AX[j][1]]:
        nn = np.linalg.norm(ax)
        if nn < 1e-12: continue
        pa, pb = pieces[i] @ (ax / nn), pieces[j] @ (ax / nn)
        if pa.max() <= pb.min() + 1e-9 or pb.max() <= pa.min() + 1e-9: return True
    return False
res['overlaps'] = len([1 for i, j in itertools.combinations(range(len(pieces)), 2) if np.linalg.norm(Cc[i] - Cc[j]) <= Rr[i] + Rr[j] + 1e-9 and not sep(i, j)])
print(json.dumps(res, indent=1, default=float)); json.dump(res, open(f'data/core-cycle-{T}.json', 'w'), indent=1, default=float)
