# TI Pyramids (DICTO, 2026-10-30): fill the truncated icosahedron ("TI", the midpoint cell of #76) from its centre with
# its 12 pentagonal and 20 hexagonal face pyramids; compare with the truncated tetrahedron's pyramids (the other midpoint cell);
# test which faces can meet, and whether the four pyramids can tile space face to face (the #77 argument).
# Exact in sympy; edge 1. Writes data/pyramids.json. Run on dicto-big-brother: ~/geom/bin/python scripts/pyramids.py
import itertools, json, math
import sympy as sp
r5 = sp.sqrt(5); phi = (1 + r5) / 2; r2 = sp.sqrt(2)

def even_perms(v): return [(v[0], v[1], v[2]), (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def signs(v): return {tuple(s * x for s, x in zip(sg, v)) for sg in itertools.product([1, -1], repeat=3)}
# truncated icosahedron, edge 2 -> scale 1/2: even permutations of (0, ±1, ±3φ), (±1, ±(2+φ), ±2φ), (±φ, ±2, ±(2φ+1))
TI = set()
for b in [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, 2 * phi + 1)]:
    for q in even_perms(b): TI |= signs(q)
TI = [sp.Matrix([sp.nsimplify(x) / 2 for x in p]) for p in TI]
# truncated tetrahedron, edge 1: permutations of (3,1,1) with an even number of minus signs, / (2√2)
TT = []
for q in set(itertools.permutations((3, 1, 1))):
    for sg in itertools.product([1, -1], repeat=3):
        if sg[0] * sg[1] * sg[2] == 1: TT.append(sp.Matrix([s * x for s, x in zip(sg, q)]) / (2 * r2))
TT = [sp.Matrix(v) for v in {tuple(sp.nsimplify(x) for x in v) for v in TT}]
assert len(TI) == 60 and len(TT) == 12

def faces(V):
    """Faces of a convex solid with vertices V (centred at 0): planes through >= 3 vertices with all others on one side."""
    Vf = [[float(x) for x in v] for v in V]; out = {}
    import numpy as np
    from scipy.spatial import ConvexHull
    h = ConvexHull(np.array(Vf))
    for eq in h.equations:
        key = tuple(round(x, 7) for x in eq)
        if key in out: continue
        ids = [i for i, v in enumerate(Vf) if abs(np.dot(eq[:3], v) + eq[3]) < 1e-7]
        out[key] = ids
    return list(out.values())

def simp(x): return sp.nsimplify(sp.simplify(x)) if x.is_number else x
def describe(V, name):
    F = faces(V); res = []
    for ids in F:
        P = [V[i] for i in ids]; c = sum(P, sp.zeros(3, 1)) / len(P)
        h = sp.sqrt(sp.simplify(c.dot(c)))   # distance from the centre to the face = pyramid height
        side = sp.sqrt(sp.simplify(P[0].dot(P[0])))
        res.append(dict(n=len(ids), height=sp.simplify(h), side=sp.simplify(side), ids=ids, centre=c))
    return F, res

out = {}
for name, V in [('TI', TI), ('truncated tetrahedron', TT)]:
    F, R = describe(V, name); kinds = {}
    for r in R:
        k = r['n']; kinds.setdefault(k, r)
        assert sp.simplify(r['height'] - kinds[k]['height']) == 0
    vol = 0; info = {}
    for k, r in kinds.items():
        cnt = sum(1 for x in R if x['n'] == k)
        area = {5: sp.Rational(5, 4) / sp.tan(sp.pi / 5), 6: 3 * sp.sqrt(3) / 2, 3: sp.sqrt(3) / 4}[k]
        v = sp.simplify(area * r['height'] / 3); vol += cnt * v
        # side face: isosceles triangle with base 1 (an edge) and legs = circumradius R; apex angle cos = 1 - 1/(2R^2)
        R2 = sp.simplify(r['side'] ** 2); apex_cos = sp.simplify(1 - sp.Rational(1, 2) / R2)
        info[f'{k}-gon pyramid'] = dict(count=cnt, height=str(sp.radsimp(r['height'])), height_num=float(r['height']), volume=str(sp.radsimp(v)), volume_num=float(v),
                                        side_edge=str(sp.radsimp(r['side'])), side_edge_num=float(r['side']), side_apex_cos=str(sp.radsimp(apex_cos)), side_apex_deg=math.degrees(math.acos(float(apex_cos))))
    # dihedral angles of the solid, per pair of face kinds, and the share each pyramid carries along that edge
    nrm = {tuple(ids): R[i]['centre'] for i, ids in enumerate(F)}
    dih = {}
    for (a, ia), (b, ib) in itertools.combinations(list(enumerate(F)), 2):
        if len(set(ia) & set(ib)) != 2: continue
        ca, cb = R[a]['centre'], R[b]['centre']
        cosd = sp.simplify(-ca.dot(cb) / sp.sqrt(ca.dot(ca) * cb.dot(cb)))   # dihedral = pi - angle between outward normals
        e = [V[i] for i in set(ia) & set(ib)]; m = (e[0] + e[1]) / 2
        # pyramid share along the edge: angle between the face plane and the plane through the centre and the edge
        def share(c):   # angle at the edge midpoint between the face centre direction and the centre
            u = c - m; w = -m
            u = u - (u.dot(e[1] - e[0]) / (e[1] - e[0]).dot(e[1] - e[0])) * (e[1] - e[0]); w = w - (w.dot(e[1] - e[0]) / (e[1] - e[0]).dot(e[1] - e[0])) * (e[1] - e[0])
            return sp.acos(sp.simplify(u.dot(w) / sp.sqrt(u.dot(u) * w.dot(w))))
        key = '%d-%d' % tuple(sorted((len(ia), len(ib))))
        if key in dih: continue
        sa, sb = share(ca), share(cb)
        dih[key] = dict(dihedral_cos=str(sp.radsimp(cosd)), dihedral_deg=math.degrees(math.acos(float(cosd))),
                        shares_deg={str(len(ia)): math.degrees(float(sa)), str(len(ib)): math.degrees(float(sb))},
                        shares_cos2={str(len(ia)): str(sp.radsimp(sp.simplify(sp.cos(sa) ** 2))), str(len(ib)): str(sp.radsimp(sp.simplify(sp.cos(sb) ** 2)))})
    out[name] = dict(pyramids=info, total_volume=str(sp.radsimp(sp.simplify(vol))), total_volume_num=float(vol), dihedrals=dih)

# the icosahedron's dihedral, for comparison: cos = -sqrt5/3
out['icosahedron dihedral cos'] = '-sqrt(5)/3'
# the hexagonal bipyramid: TI's hexagon pyramid on the truncated tetrahedron's, base to base
hF = sp.sympify(out['TI']['pyramids']['6-gon pyramid']['height']); hT = sp.sympify(out['truncated tetrahedron']['pyramids']['6-gon pyramid']['height'])
out['hexagonal bipyramid'] = dict(height=str(sp.radsimp(hF + hT)), height_num=float(hF + hT), volume_num=float((hF + hT) * 3 * sp.sqrt(3) / 2 / 3))

# which side faces can meet: congruent side triangles (base 1, legs = side edge)
sides = {f'{s} {k}': out[s]['pyramids'][k]['side_edge_num'] for s in ['TI', 'truncated tetrahedron'] for k in out[s]['pyramids']}
out['side faces'] = sides

# face-to-face tiling by TIs and truncated tetrahedra: angles round an edge must add to 2*pi
A = {}
for s in ['TI', 'truncated tetrahedron']:
    for k, d in out[s]['dihedrals'].items(): A[f'{s} {k}'] = math.radians(d['dihedral_deg'])
stars = []
names = list(A)
for n in range(2, 6):
    for combo in itertools.combinations_with_replacement(names, n):
        t = sum(A[c] for c in combo)
        if abs(t - 2 * math.pi) < 1e-6: stars.append(combo)
out['edge stars of whole solids (angles adding to 360 degrees)'] = stars
json.dump(out, open('data/pyramids.json', 'w'), indent=1, default=str)
print(json.dumps(out, indent=1, default=str)[:6000])
