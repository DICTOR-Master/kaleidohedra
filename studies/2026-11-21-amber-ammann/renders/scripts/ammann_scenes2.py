# DICTO · dictospheres.com — four more scenes of the Amber-Ammann study for #118 Version 2, with the helpers of ammann_scenes.py
# (its definitions are run unchanged; its scenes are not). Geometry: ../../data/patch.json (the exact 402-cell patch, floats here) and
# data/geom_*.json written by ammann_dump.py (= ammann_cell.py + float geometry):
#   geom_C2_<triple>_S0_cen.json for all 20 triples (Rollerball, S0, centroid seeds: the setting of Theorem 1);
#   geom_<core>_023_S65_cproj.json for the five cores (6/5 S0, projected seeds: one setting valid for all five, Table 2).
# Scenes: patch402.html (the whole patch), cores5.html (five cores in the prolate cell 134 = scripts' 023), slab.html (the
# Scutoid-Frusta layer in one slab of the patch), piece.html (one Scutoid-Frustum, whole and pulled apart). Checks printed, then FINAL ok.
import json, os, math, itertools
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, 'ammann_scenes.py')).read(); exec(src[:src.index('# ---------------- 1. the patch')])
LOG = []
VIOLET = '#8a5cc4'                                                     # the dodecahedron colour (element colours); BLUE = the icosahedron's
TRI = [''.join(map(str, A)) for A in itertools.combinations(range(6), 3)]; assert len(TRI) == 20
GA = {t: json.load(open(os.path.join(D, f'geom_C2_{t}_S0_cen.json'))) for t in TRI}
for t, g in GA.items(): assert g['valid'] and g['n_scutoid_pieces'] == 72 and g['n_Y'] == 30 and g['n_kinds'] == 8 and abs(g['s'] - S_) < 1e-12
LOG.append('geom_C2_*_S0_cen: all 20 orientations valid, 72 Scutoid-Frusta, 30 Y-vertices, 8 kinds each, one common s')
# ---------------- A. the whole 402-cell patch ----------------
kinds = [t['kind'] for t in T]; nP, nO = kinds.count('P'), kinds.count('O'); orients = {tuple(t['A']) for t in T}
assert len(T) == 402 and (nP, nO) == (278, 124) and len(orients) == 20 and P['shared_faces'] == 998 and P['boundary_faces'] == 416
parts = []
for t in T:
    S = rhombo(t['A'], np.array(t['centre']), 0.86)
    parts.append(solid_part(S, SAND if t['kind'] == 'P' else SLATE, rad=0.0011, edge_col=EDGE))
DIRA = np.array([0.50, 0.38, 1.0]); EA = ext(parts, DIRA, 1.04)
write(os.path.join(OUT, 'patch402.html'), [{'E': EA, 'dir': DIRA.tolist(), 'parts': parts}])
LOG.append(f'patch402.html: all {len(T)} cells, {nP} prolate + {nO} oblate, {len(orients)} orientations, cells drawn at 0.86')
# ---------------- B. five cores in the prolate cell 134 (scripts 023), 6/5 S0, projected seeds ----------------
CORES = [('C2', 'Rollerball', 72, 72, 30), ('C1', 'Fullerene Star', 66, 80, 48), ('icosidodecahedron', 'icosidodecahedron', 20, 32, 30),
         ('icosahedron', 'icosahedron', 18, 20, 12), ('dodecahedron', 'dodecahedron', 0, 12, 0)]
def core_colour(name, n):
    if name == 'C2': return PEARL if n == 10 else BLUE                 # decagons pearl, icosahedron centre pyramids blue
    if name == 'C1': return PEARL if n == 6 else VIOLET                # hexagons pearl, dodecahedron centre pyramids violet
    return {'icosahedron': BLUE, 'dodecahedron': VIOLET}.get(name, PEARL)
def core_mesh(g, name, scale, rad):
    X = np.array(g['geom']['X'][:g['geom']['nC1']]) * scale; T_, C = [], []
    for pc in g['geom']['pieces']:
        for poly, lab in pc['polys']:
            if lab != 'bottom': continue
            for a, b in zip(poly[1:-1], poly[2:]): T_.append([poly[0], a, b]); C.append(core_colour(name, len(poly)))
    for t in T_:
        n = np.cross(X[t[1]] - X[t[0]], X[t[2]] - X[t[0]])
        if n @ X[t[0]] < 0: t[1], t[2] = t[2], t[1]
    return mesh_part(X, T_, C, rad)
A023 = [0, 2, 3]; ax = sum(E6[a] for a in A023); ax /= np.linalg.norm(ax); tt = np.cross(ax, [0, 1, 0]); tt /= np.linalg.norm(tt)
DIRB = ax * math.cos(math.radians(72)) + tt * math.sin(math.radians(72))
scB = []; infoB = []
for key, nm, nsf, nf, ny in CORES:
    g = json.load(open(os.path.join(D, f'geom_{key}_023_S65_cproj.json')))
    assert g['valid'] and g['n_scutoid_pieces'] == nsf and g['n_faces'] == nf and g['n_Y'] == ny and g['factor'] == 'S65' and g['seeds'] == 'cproj', key
    k = 3 / g['s']                                                     # every mould drawn at the patch size (edge |e|)
    S = rhombo(A023, np.zeros(3), 1.0)
    ps = core_mesh(g, key, k, 0.0028)
    ps.append(solid_part(S, GLASS, alpha=0.16, rad=0.0018, edge_col=LIGHT, faces=[i for i, (n, d, o) in enumerate(S.F) if n @ DIRB < 0]))
    scB.append(ps); infoB.append([nm, nsf, nf, ny, g['s0'], round(g['s'], 6), round(1 / k, 6)])
EB = max(ext(ps, DIRB, 1.03) for ps in scB)
write(os.path.join(OUT, 'cores5.html'), [{'E': EB, 'dir': DIRB.tolist(), 'parts': ps} for ps in scB])
LOG.append('cores5.html: prolate cell 134 (023), 6/5 S0, projected seeds: ' + '; '.join(f'{a} {b}/{c} Scutoid-Frusta, {d} Y' for a, b, c, d, *_ in infoB))
# ---------------- C. the Scutoid-Frusta layer in one slab ----------------
cen = np.array([t['centre'] for t in T]); NZ = np.array([0.0, 0.0, 1.0]); HZ = 0.9; RS = 6.2
sel = [i for i in range(len(T)) if abs(cen[i] @ NZ) < HZ and np.linalg.norm(cen[i] - (cen[i] @ NZ) * NZ) < RS]
parts = []; ntop = 0; nreg = 0
for i in sel:
    t = T[i]; g = GA[''.join(map(str, t['A']))]; X = np.array(g['geom']['X']) * SC; c = np.array(t['centre'])
    tops = [X[poly] for pc in g['geom']['pieces'] for poly, lab in pc['polys'] if lab == 'top']
    regs = {pc['F'] for pc in g['geom']['pieces'] if any(lab == 'top' for _, lab in pc['polys'])}; assert len(regs) == 72
    nreg += len(regs); ntop += len(tops)
    Vs, Ts, Es, ids = [], [], set(), {}
    def vid(p):
        kk = tuple(np.round(p, 6))
        if kk not in ids: ids[kk] = len(Vs); Vs.append(c + 0.94 * np.asarray(p))
        return ids[kk]
    for q in tops:
        ii = [vid(p) for p in q]
        for a, b in zip(ii[1:-1], ii[2:]): Ts.append([ii[0], a, b])
        for a, b in zip(ii, ii[1:] + ii[:1]): Es.add((min(a, b), max(a, b)))
    col = SAND if t['kind'] == 'P' else SLATE
    parts.append({'v': np.round(Vs, 6).tolist(), 't': Ts, 'c': [col] * len(Ts), 'a': 1.0, 'tubes': [[a, b, EDGE, None] for a, b in sorted(Es)], 'rad': 0.0009, 'balls': []})
sP = sum(T[i]['kind'] == 'P' for i in sel); sO = len(sel) - sP; sOr = len({tuple(T[i]['A']) for i in sel})
DIRC = np.array([0.30, 0.55, 1.0]); EC = ext(parts, DIRC, 1.04)
write(os.path.join(OUT, 'slab.html'), [{'E': EC, 'dir': DIRC.tolist(), 'parts': parts}])
LOG.append(f'slab.html: cells of the patch with centre |z| < {HZ}, distance from the z axis < {RS}: {len(sel)} cells, {sP} prolate + {sO} oblate, '
           f'{sOr} orientations, {nreg} pieces ({len(sel)} x 72) seen by their tops on the cell walls ({ntop} top polygons), cells drawn at 0.94')
# ---------------- D. one Scutoid-Frustum, whole and pulled apart ----------------
g = G['023']; KO = kind_of(g); X = np.array(g['geom']['X']); Y = set(g['geom']['Y'])
pc = next(p for p in g['geom']['pieces'] if p['F'] == 0); kd = next(k for k in g['kinds'] if 0 in k['members'])
tris = pc['tris']; idx = sorted({v for tr in tris for v in tr}); Yp = [v for v in idx if v in Y]
nor = {}
for j, (a, b, c_) in enumerate(tris):
    n = np.cross(X[b] - X[a], X[c_] - X[a]); nor[j] = n / np.linalg.norm(n)
edges = {}
for j, tr in enumerate(tris):
    for k in range(3): edges.setdefault(frozenset((tr[k], tr[(k + 1) % 3])), []).append(j)
par = list(range(len(tris)))
def fd(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for e, L in edges.items():                                              # flat faces = coplanar edge-neighbour triangles
    assert len(L) == 2
    if nor[L[0]] @ nor[L[1]] > 1 - 1e-9: par[fd(L[0])] = fd(L[1])
faces = {}
for j in range(len(tris)): faces.setdefault(fd(j), []).append(j)
nE = sum(fd(L[0]) != fd(L[1]) for L in edges.values()); nV = len(idx); nF = len(faces)
assert (nF, nV, nE, len(Yp)) == (kd['n_facets'], kd['n_vertices'], kd['n_edges'], kd['Y']) == (29, 21, 48, 5) and nV - nE + nF == 2
bot = next(p for p, l in pc['polys'] if l == 'bottom'); top = [p for p, l in pc['polys'] if l == 'top']
assert len(bot) == 10 and len(top) == 1 and len(top[0]) == 5 and len(kd['Nin']) == 10 and len(kd['Nout']) == 5 and kd['scutoid']
bset, tset = set(bot), set(top[0]); TOPC, BOTC, WALLC = GLASS, PEARL, KIND[KO[0]]          # the face on the mould in the mould colour of Figure 5
def fcol(js):
    vs = {v for j in js for v in tris[j]}
    return BOTC if vs <= bset else TOPC if vs <= tset else WALLC
cc = X[idx].mean(0); bc, tc = X[bot].mean(0), X[top[0]].mean(0); L = np.linalg.norm(tc - bc); u = (tc - bc) / L   # piece axis: decagon to pentagon
w = np.cross(u, [0.3, 1.0, 0.2]); w /= np.linalg.norm(w)
RD = np.array([np.cross(-u, w), -u, w])                                   # drawing frame: the piece axis upright, the decagon on top (lit from above)
DIRD = np.array([0.0, math.sin(math.radians(38)), math.cos(math.radians(38))])    # side-on, tilted 38 deg towards the core side so the decagon shows
def piece_parts(pull):
    """pull = 0: the whole piece; pull > 0: the decagon moved down the axis, the pentagon up it, each flat side face out from the axis"""
    ps = []
    for js in faces.values():
        vs = sorted({v for j in js for v in tris[j]}); m = {v: i for i, v in enumerate(vs)}
        fc = X[vs].mean(0); col = fcol(js); r = fc - cc - ((fc - cc) @ u) * u
        sh = pull * (-L * u if col == BOTC else L * u if col == TOPC else 0.7 * r)
        V = (X[vs] - cc + sh) @ RD.T; ed = {}
        for j in js:
            for k in range(3): e = frozenset((tris[j][k], tris[j][(k + 1) % 3])); ed[e] = ed.get(e, 0) + 1
        tubes = [[m[a], m[b], EDGE, None] for e, n in ed.items() if n == 1 for a, b in [tuple(e)]]
        ps.append({'v': np.round(V, 6).tolist(), 't': [[m[v] for v in tris[j]] for j in js], 'c': [col] * len(js), 'a': 1.0, 'tubes': tubes, 'rad': 0.0030, 'balls': []})
        yy = [v for v in vs if v in Y]
        if yy: ps.append({'v': np.round((X[yy] - cc + sh) @ RD.T, 6).tolist(), 't': [], 'c': [], 'a': 1.0, 'tubes': [], 'rad': 0.0110, 'balls': [[i, YCOL] for i in range(len(yy))]})
    return ps
whole = piece_parts(0.0); apart = piece_parts(0.5)
ED = max(ext(whole, DIRD, 1.05), ext(apart, DIRD, 1.05))
write(os.path.join(OUT, 'piece.html'), [{'E': ED, 'dir': DIRD.tolist(), 'parts': p} for p in (whole, apart)])
nYdots = sum(len([v for v in {v for j in js for v in tris[j]} if v in Y]) for js in faces.values())
LOG.append(f'piece.html: prolate cell 134 (023), piece on Rollerball face 0 (a decagon), kind volume {kd["vol"]:.6f}: bottom decagon, top pentagon, '
           f'{len(kd["Nin"])} neighbours on the core side, {len(kd["Nout"])} on the mould side, {len(Yp)} Y-vertices, {nV} vertices, {nE} edges, {nF} flat faces; '
           f'pulled apart: decagon and pentagon 0.5 x their distance along the axis, side faces 0.35 x their distance from it; {nYdots} Y dots in the pulled-apart view')
json.dump({'A': [len(T), nP, nO, len(orients)], 'B': infoB, 'C': [len(sel), sP, sO, sOr, nreg], 'D': [len(kd['Nin']), len(kd['Nout']), len(Yp), nV, nE, nF, round(kd['vol'], 6), nYdots]},
          open(os.path.join(OUT, 'info2.json'), 'w'))
open(os.path.join(H, 'ammann_scenes2.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
