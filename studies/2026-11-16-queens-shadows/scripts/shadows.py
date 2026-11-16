#!/usr/bin/env python3
"""DICTO's shadows test (16 Nov 2026). DICTO: "all of the shadows seem to carry interconnected lattices of possible vacuus".
Restatement confirmed by DICTO: when a Queen (White Queen = 600-cell, Red Queen = 120-cell) is projected to 3D along d, every wall that
CONTAINS d survives in the shadow as a flat central plane (its trace in d-perp); the others smear out. A 3D shape in the shadow whose
central plates all lie in those planes is a possible Vacuus. Shadows along different directions share walls, so the plane sets join up.

WALLS (as studies/2026-11-16-600cell-walls): the 60 H4 mirrors (normals = 600-cell corners) and the 300 cross walls (central sections
parallel to a pair of opposite cells of the 600-cell; normals = cell centres = 120-cell corners). DICTO: "cross walls also count".
A wall with normal n contains d iff n.d = 0; its trace in the shadow is the central plane n-perp ∩ d-perp, and a point P(x) of the shadow
lies on it iff n.x = 0 (since n.d = 0), so every test is an exact dot product in Q(sqrt5) on the 4D coordinates, no basis needed.
PLATES of a 3D shape (as #87): one fin per edge, the plane spanned by the edge and a centre.
  'O' = the shadow's centre (the projection of the Queen's centre): the edge pq is in wall n iff n.p = n.q = 0;
  'own' = the shape's own centre c: the fin through c is PARALLEL to wall n's trace iff n.(p-c) = n.(q-c) = 0, and lies IN it iff also n.c = 0.
  An edge whose fin is undefined (edge on a line through the centre, or an edge seen end-on) is counted apart.
Classes: possible Vacuus = every defined plate in a surviving plane; partly = some; not = none.
Symmetry: the group W(H4) is generated exactly as permutations of the 120 corners (exact reflections); the stabiliser of the line ±d acts
on the shadow; orbits of cells under it are congruent images. Congruence classes of projected cells: tetrahedra by the canonical
(min over 24 labellings) 6-tuple of exact squared edge lengths (a complete invariant up to isometry, mirror images merged); dodecahedra by
the exact multisets of squared distances and squared radii from their centroid (an invariant; orbits merged only when it agrees).
Hulls: face lattice from a float hull (echo_lib.hull3), then certified exactly (every face plane exact, every point on the inner side).
Coordinates: the 600-cell from ../../2026-11-15-echo-shapes/scripts/shadow_echoes.py (cell600, 120 unit corners); the 120-cell built here
as its exact dual (corners = centroids of the 600 tetrahedra), so the two Queens are dual-aligned and share one wall system.
Usage: shadows.py out.json [--pilot]"""
import sys, os, json, time, itertools
import numpy as np
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ST, '2026-11-15-echo-shapes', 'scripts'))
_argv = sys.argv; sys.argv = ['shadow_echoes.py', 'unused.json']
import shadow_echoes as SE
sys.argv = _argv
from echo_lib import Q5, q5, PHI, dot, vsub, vadd, vscale, vkey, to_np, hull3, fvec, face_census, name_of
OUT = sys.argv[1]; PILOT = '--pilot' in sys.argv
T0 = time.time(); FAILS = []
def check(c, msg):
    print(('CHECK ok   ' if c else 'CHECK FAIL ') + msg, flush=True)
    if not c: FAILS.append(msg)
def log(*a): print(*a, flush=True)
Z = Q5(0)

def canon_dir(v):
    for x in v:
        if not x.iszero(): return tuple((y/x).key() for y in v)
    raise ValueError('zero')
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0])
            + M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0]))
def gcross4(a, b, c):
    out = []
    for i in range(4):
        cols = [j for j in range(4) if j != i]
        out.append(det3([[r[j] for j in cols] for r in (a, b, c)]) * (1 if i % 2 == 0 else -1))
    return tuple(out)
def det4(a, b, c, e): return dot(gcross4(a, b, c), e)
def cent(pts): n = len(pts); return tuple(sum((p[t] for p in pts), Z)/n for t in range(4))
def vneg(v): return tuple(-x for x in v)
def iszero(v): return all(x.iszero() for x in v)

# ------------------------------------------------------------------ the two Queens, exact
V = SE.cell600(); NV = len(V)
check(NV == 120 and all(dot(p, p) == 1 for p in V), '600-cell: 120 unit corners')
VK = {vkey(p): i for i, p in enumerate(V)}
NEG = [VK[vkey(vneg(p))] for p in V]
E6 = SE.edges4(V); check(len(E6) == 720, '600-cell: 720 edges')
ADJ = defaultdict(set)
for i, j in E6: ADJ[i].add(j); ADJ[j].add(i)
TRI = sorted({tuple(sorted((i, j, k))) for i, j in E6 for k in ADJ[i] & ADJ[j]}); check(len(TRI) == 1200, '600-cell: 1200 triangles')
TET = sorted({tuple(sorted(t + (k,))) for t in TRI for k in ADJ[t[0]] & ADJ[t[1]] & ADJ[t[2]]}); check(len(TET) == 600, '600-cell: 600 tetrahedra')
TK = {t: i for i, t in enumerate(TET)}
R = [cent([V[i] for i in t]) for t in TET]                         # 120-cell corners (dual)
r2 = dot(R[0], R[0]); check(all(dot(p, p) == r2 for p in R), f'120-cell: 600 corners on one sphere (r^2 = {r2})')
TET_OF_TRI = defaultdict(list)
for ti, t in enumerate(TET):
    for f in itertools.combinations(t, 3): TET_OF_TRI[f].append(ti)
E12 = sorted(tuple(sorted(v)) for v in TET_OF_TRI.values()); check(len(E12) == 1200 and all(len(e) == 2 for e in E12), '120-cell: 1200 edges (tetrahedra sharing a triangle)')
el = {dot(vsub(R[a], R[b]), vsub(R[a], R[b])).key() for a, b in E12}; check(len(el) == 1, '120-cell: all 1200 edges equal')
TET_OF_V = defaultdict(list)
for ti, t in enumerate(TET):
    for v in t: TET_OF_V[v].append(ti)
CELL12 = [sorted(TET_OF_V[v]) for v in range(NV)]; check(all(len(c) == 20 for c in CELL12), '120-cell: 120 cells of 20 corners (dodecahedra round a 600-cell corner)')
TET_OF_E = defaultdict(list)
for ti, t in enumerate(TET):
    for e in itertools.combinations(t, 2): TET_OF_E[e].append(ti)
PENT = [sorted(TET_OF_E[e]) for e in map(tuple, E6)]; check(all(len(p) == 5 for p in PENT), '120-cell: 720 pentagons (5 tetrahedra round a 600-cell edge)')
E12S = set(E12)
CELL12_EDGES = [[(a, b) for a, b in itertools.combinations(c, 2) if (a, b) in E12S] for c in CELL12]
check(all(len(x) == 30 for x in CELL12_EDGES), '120-cell: each cell has 30 edges')
TNEG = [TK[tuple(sorted(NEG[i] for i in t))] for t in TET]

# ------------------------------------------------------------------ walls
MIRROR = []; seen = set()
for i, p in enumerate(V):
    k = canon_dir(p)
    if k not in seen: seen.add(k); MIRROR.append(i)
CROSS = []; seen = set()
for i, p in enumerate(R):
    k = canon_dir(p)
    if k not in seen: seen.add(k); CROSS.append(i)
WALLS = [('mirror', V[i], ('v', i)) for i in MIRROR] + [('cross', R[i], ('t', i)) for i in CROSS]
check(len(MIRROR) == 60 and len(CROSS) == 300, f'walls: 60 mirrors + 300 cross walls ({len(MIRROR)} + {len(CROSS)})')
check(len({canon_dir(w[1]) for w in WALLS}) == 360, 'walls: 360 distinct normals (no cross wall is a mirror)')
# reflection in each mirror maps the 600-cell to itself (they are its mirrors)
ok = True
for i in MIRROR[:60 if not PILOT else 6]:
    n = V[i]
    for p in V:
        q = vsub(p, vscale(2*dot(p, n), n))
        if vkey(q) not in VK: ok = False
check(ok, 'mirrors: reflection in each maps the 600 cell onto itself (exact)')
WALL_ID = {}
for wi, (kind, n, (typ, idx)) in enumerate(WALLS):
    if typ == 'v': WALL_ID[('v', idx)] = wi; WALL_ID[('v', NEG[idx])] = wi
    else: WALL_ID[('t', idx)] = wi; WALL_ID[('t', TNEG[idx])] = wi

# ------------------------------------------------------------------ the group, exact as permutations of the corners
def refl_perm(n):
    return np.array([VK[vkey(vsub(p, vscale(2*dot(p, n)/dot(n, n), n)))] for p in V], dtype=np.int16)
GEN = [refl_perm(V[i]) for i in MIRROR]
def closure(gens):
    idp = np.arange(NV, dtype=np.int16); G = {idp.tobytes(): idp}; frontier = [idp]
    while frontier:
        new = []
        for g in frontier:
            for s in gens:
                h = s[g]
                k = h.tobytes()
                if k not in G: G[k] = h; new.append(h)
        frontier = new
    return list(G.values())
GROUP = closure(GEN); check(len(GROUP) == 14400, f'W(H4) generated exactly by the 60 reflections: {len(GROUP)} elements')
GA = np.array(GROUP)
# action on tetrahedra (as sorted corner tuples)
def act_set(g, s): return tuple(sorted(int(g[i]) for i in s))

# ------------------------------------------------------------------ directions
def dir_sets():
    """vertex sets whose centroid gives each standard direction (600-cell face of each dimension; 120-cell faces via duality)"""
    return {'V': [(i,) for i in range(NV)], 'E': [tuple(e) for e in E6], 'F': TRI, 'C': TET}
DS = dir_sets()
def dvec(s): return cent([V[i] for i in s])
LINES = {}
for typ, sets in DS.items():
    L = {}
    for s in sets:
        k = canon_dir(dvec(s))
        L.setdefault(k, s)
    LINES[typ] = list(L.values())
check([len(LINES[t]) for t in 'VEFC'] == [60, 360, 600, 300], f'direction lines V/E/F/C: {[len(LINES[t]) for t in "VEFC"]} (60/360/600/300)')
# 120-cell directions coincide with the 600-cell's by duality (exact line equality)
def lineset(vecs): return {canon_dir(v) for v in vecs}
L600 = {t: lineset([dvec(s) for s in LINES[t]]) for t in 'VEFC'}
d120 = {'corner': lineset(R), 'edge': lineset([cent([R[a], R[b]]) for a, b in E12]),
        'pentagon': lineset([cent([R[i] for i in p]) for p in PENT]), 'cell': lineset([cent([R[i] for i in c]) for c in CELL12])}
check(d120['corner'] == L600['C'], '120-cell corner-first lines = 600-cell cell-first lines')
check(d120['edge'] == L600['F'], '120-cell edge-first lines = 600-cell face-first lines')
check(d120['pentagon'] == L600['E'], '120-cell pentagon-first lines = 600-cell edge-first lines')
check(d120['cell'] == L600['V'], '120-cell cell-first lines = 600-cell corner-first lines')
NAME600 = {'V': 'corner-first', 'E': 'edge-first', 'F': 'face-first', 'C': 'cell-first'}
NAME120 = {'C': 'corner-first', 'F': 'edge-first', 'E': 'pentagon-first', 'V': 'cell-first'}

def walls_containing(d): return [wi for wi, (k, n, _) in enumerate(WALLS) if dot(n, d).iszero()]

# representatives: a flag (corner in edge in triangle in tetrahedron), as #63's turnings (18 deg corner-edge)
t0 = TET[0]; FLAG = {'V': (t0[0],), 'E': (t0[0], t0[1]), 'F': (t0[0], t0[1], t0[2]), 'C': t0}
check(tuple(sorted(FLAG['E'])) in set(map(tuple, E6)), 'flag: edge is an edge')

def stab_line(s):
    S = tuple(sorted(s)); Sn = tuple(sorted(NEG[i] for i in s)); out = []
    for g in GROUP:
        im = act_set(g, s)
        if im == S: out.append((g, 1))
        elif im == Sn: out.append((g, -1))
    return out

# ------------------------------------------------------------------ exact hull of projected points
def proj(x, d, dd): return vsub(x, vscale(dot(x, d)/dd, d))
def basis(d):
    return SE.basis_perp(d, 4)
def exact_hull(P4, d, B):
    """P4: exact projected 4D points (distinct). Returns (rank, faces as index cycles, edges as index pairs), certified exactly."""
    X = np.array([to_np(p) for p in P4]) @ B
    c = X.mean(0); s = np.linalg.svd(X - c, compute_uv=False) if len(X) > 1 else np.zeros(3)
    rank = int((s > 1e-9).sum())
    if rank == 3:
        H = hull3(X)
        # hull3 orders every point of a face plane by angle; points inside a face (images of side-on cells) would zigzag the cycle,
        # so each face's cycle is re-made as the 2D convex hull of its points
        from scipy.spatial import ConvexHull
        newf = []
        for f in H['faces']:
            Y = X[f]; c0 = Y.mean(0); U = np.linalg.svd(Y - c0)[2][:2]; h2 = ConvexHull((Y - c0) @ U.T)
            cyc = [f[k] for k in h2.vertices]
            keep = []
            for t in range(len(cyc)):                        # drop points in the relative interior of a hull edge
                a_, b_, c_ = X[cyc[t - 1]], X[cyc[t]], X[cyc[(t + 1) % len(cyc)]]
                if np.linalg.norm(np.cross(b_ - a_, c_ - b_)) > 1e-9 * max(1, np.abs(X).max()): keep.append(cyc[t])
            newf.append(keep)
        H['faces'] = newf; H['verts'] = sorted({i for f in newf for i in f})
        faces = H['faces']
        for f in faces:                                      # exact certificate
            a, b, cc = P4[f[0]], P4[f[1]], P4[f[2]]
            m = gcross4(d, vsub(b, a), vsub(cc, a))
            if iszero(m): FAILS.append('hull: degenerate face triple'); continue
            vals = [dot(m, vsub(p, a)) for p in P4]
            if not all(vals[i].iszero() for i in f): FAILS.append('hull: face not exactly planar')
            sg = {v.sign() for v in vals if not v.iszero()}
            if len(sg) > 1: FAILS.append('hull: point outside a face plane')
        E = set()
        for f in faces:
            for t in range(len(f)): E.add(tuple(sorted((f[t - 1], f[t]))))
        return 3, faces, sorted(E), H
    if rank == 2:
        from scipy.spatial import ConvexHull
        U = np.linalg.svd(X - c)[2][:2]; Y = (X - c) @ U.T
        h = ConvexHull(Y); cyc = list(h.vertices)
        E = sorted(tuple(sorted((cyc[t - 1], cyc[t]))) for t in range(len(cyc)))
        return 2, [cyc], E, None
    if rank == 1:
        i = int(np.argmin(X @ (X[1] - X[0]))); j = int(np.argmax(X @ (X[1] - X[0])))
        return 1, [], [tuple(sorted((i, j)))], None
    return 0, [], [], None

# ------------------------------------------------------------------ plates
def fin_defined(a, b, d):
    # fin = span(P a, P b) in d-perp; undefined if P a, P b dependent  <=> d, a, b dependent  <=> all 3x3 minors of [d; a; b] vanish
    for cols in itertools.combinations(range(4), 3):
        if not det3([[r[j] for j in cols] for r in (d, a, b)]).iszero(): return True
    return False
def classify_edges(edges, pts, d, surv, centre):
    """edges: list of (i, j) into pts (exact 4D, may be unprojected); surv: list of wall indices containing d.
    centre None -> shadow centre O; else the shape's own centre (4D point). Returns tally and the walls hit."""
    t = Counter(); hits = Counter(); inwall = 0
    for i, j in edges:
        a, b = (pts[i], pts[j]) if centre is None else (vsub(pts[i], centre), vsub(pts[j], centre))
        if not fin_defined(a, b, d): t['undefined'] += 1; continue
        hit = None
        for wi in surv:
            n = WALLS[wi][1]
            if dot(n, a).iszero() and dot(n, b).iszero(): hit = wi; break
        if hit is None: t['none'] += 1
        else:
            t[WALLS[hit][0]] += 1; hits[hit] += 1
            if centre is not None and dot(WALLS[hit][1], centre).iszero(): inwall += 1
    return t, hits, inwall
def verdict(t):
    good = t['mirror'] + t['cross']; tot = good + t['none']
    if tot == 0: return 'no plates'
    return 'possible Vacuus' if t['none'] == 0 else ('partly' if good else 'not')

def regular_name(P4, edges, d, rank, faces, H):
    dd = dot(d, d)
    if rank < 3:
        return {0: 'point', 1: 'segment', 2: f'{len(edges)}-gon'}[rank]
    nm = name_of(H)
    Pp = [proj(p, d, dd) for p in P4]; c = cent(Pp)
    L = {dot(vsub(Pp[i], Pp[j]), vsub(Pp[i], Pp[j])).key() for i, j in edges}
    Rr = {dot(vsub(p, c), vsub(p, c)).key() for p in Pp}
    tag = ('equal edges' if len(L) == 1 else f'{len(L)} edge lengths') + (', one sphere' if len(Rr) == 1 else f', {len(Rr)} radii')
    return f'{nm} ({tag})'

# ------------------------------------------------------------------ one shadow
def shadow(queen, typ):
    global MAIN
    MAIN = (queen, typ) in (('600', 'V'), ('120', 'V'), ('600', 'C'), ('120', 'C'))
    s = FLAG[typ]; d = dvec(s); dd = dot(d, d); B = basis(d)
    surv = walls_containing(d)
    st = stab_line(s)
    kern = 2 if typ == 'V' else 1
    rec = {'queen': queen, 'direction': (NAME600 if queen == '600' else NAME120)[typ], 'type': typ,
           'walls': {'mirror': sum(WALLS[w][0] == 'mirror' for w in surv), 'cross': sum(WALLS[w][0] == 'cross' for w in surv)},
           'line_stabiliser': len(st), 'group_on_shadow': len(st)//kern}
    # wall orbits under the stabiliser + axis description
    def wall_img(g, wi):
        typ_, idx = WALLS[wi][2]
        if typ_ == 'v': return WALL_ID[('v', int(g[idx]))]
        return WALL_ID[('t', TK[act_set(g, TET[idx])])]
    orbs = []; left = set(surv)
    while left:
        w = min(left); o = {wall_img(g, w) for g, _ in st}; left -= o; orbs.append(sorted(o))
    check(all(set(o) <= set(surv) for o in orbs), f'{queen} {typ}: the stabiliser permutes the surviving walls')
    Bn = B
    oinfo = []
    for o in orbs:
        n = to_np(WALLS[o[0]][1]) @ Bn; n /= np.linalg.norm(n)
        fix = sum(1 for g, _ in st if wall_img(g, o[0]) == o[0])
        oinfo.append({'kind': WALLS[o[0]][0], 'planes': len(o), 'normal_line_stabiliser': fix})
    rec['plane_orbits'] = oinfo
    # angles between surviving normals (exact cos^2) -> arrangement fingerprint
    cos2 = Counter()
    for a, b in itertools.combinations(surv, 2):
        na, nb = WALLS[a][1], WALLS[b][1]
        cos2[str((dot(na, nb)*dot(na, nb)/(dot(na, na)*dot(nb, nb))))] += 1
    rec['normal_cos2'] = dict(cos2)
    # points of the Queen
    if queen == '600':
        P = V; cells = [list(t) for t in TET]; cell_edges = [[(a, b) for a, b in itertools.combinations(range(4), 2)] for _ in TET]
        allE = [tuple(e) for e in E6]
    else:
        P = R; cells = CELL12; cell_edges = None; allE = E12
    # ---- projected cells: side-on / front / back, orbits, classes, plates
    def cell_pts(ci): return [P[i] for i in cells[ci]]
    def cell_edge_list(ci):
        if queen == '600': return [(a, b) for a, b in itertools.combinations(range(4), 2)]
        loc = {v: k for k, v in enumerate(cells[ci])}
        return [(loc[a], loc[b]) for a, b in CELL12_EDGES[ci]]
    def side(ci):
        # a cell's outward normal is its centre direction (regular polytope): side-on iff its hyperplane contains d,
        # i.e. its projected volume is 0 (checked with det4 for the tetrahedra); front iff its normal points to the viewer
        pts = cell_pts(ci); h = dot(cent(pts), d)
        if queen == '600':
            v = det4(vsub(pts[1], pts[0]), vsub(pts[2], pts[0]), vsub(pts[3], pts[0]), d)
            if v.iszero() != h.iszero(): FAILS.append('side-on test disagrees with the volume test')
        return 'side-on' if h.iszero() else ('front' if h.sign() > 0 else 'back')
    def cell_img(g, ci):
        if queen == '600': return TK[act_set(g, TET[ci])]
        # 120-cell cell ci = tetrahedra round 600-corner ci
        return int(g[ci])
    corbs = []; left = set(range(len(cells)))
    while left:
        c0 = min(left); o = {cell_img(g, c0) for g, _ in st}; left -= o; corbs.append(sorted(o))
    rec['cell_orbits'] = len(corbs)
    rows = []
    for o in corbs:
        ci = o[0]; pts = cell_pts(ci); Pp = [proj(p, d, dd) for p in pts]
        sd = Counter(side(c) for c in o)
        if queen == '600':
            dist = [dot(vsub(Pp[i], Pp[j]), vsub(Pp[i], Pp[j])).key() for i, j in itertools.combinations(range(4), 2)]
            best = None
            pairs = list(itertools.combinations(range(4), 2))
            for pm in itertools.permutations(range(4)):
                key = tuple(dot(vsub(Pp[pm[i]], Pp[pm[j]]), vsub(Pp[pm[i]], Pp[pm[j]])).key() for i, j in pairs)
                if best is None or key < best: best = key
            ckey = str(best)
        else:
            c = cent(Pp)
            ckey = str((sorted(dot(vsub(a, b), vsub(a, b)).key() for a, b in itertools.combinations(Pp, 2)),
                        sorted(dot(vsub(a, c), vsub(a, c)).key() for a in Pp)))
        ce = cell_edge_list(ci)
        tO, _, _ = classify_edges(ce, pts, d, surv, None)
        cc = cent(pts)
        tC, _, inw = classify_edges(ce, pts, d, surv, cc)
        rows.append({'orbit_size': len(o), 'sides': dict(sd), 'class_key': ckey, 'plates_O': dict(tO), 'verdict_O': verdict(tO),
                     'plates_own': dict(tC), 'verdict_own': verdict(tC), 'own_fins_in_wall': inw, 'centre_at_O': iszero(proj(cc, d, dd)),
                     'rep': ci})
    keys = {}
    for r in rows: r['class'] = keys.setdefault(r['class_key'], len(keys) + 1)
    rec['cell_classes'] = len(keys)
    front_classes = {r['class'] for r in rows if r['sides'].get('front')}
    rec['front_classes'] = len(front_classes)
    rec['side_counts'] = dict(sum((Counter(r['sides']) for r in rows), Counter()))
    for r in rows: del r['class_key']
    rec['cells'] = rows
    # ---- layers (corners at one height x.d), outlines, and the hull
    H = defaultdict(list)
    for i, p in enumerate(P): H[dot(p, d).key()].append(i)
    heights = sorted(H, key=lambda k: float(Q5(*k)))
    layers = []
    def shape_record(label, idx, extra=None):
        Pp = [proj(P[i], d, dd) for i in idx]
        uniq = {};
        for k, p in enumerate(Pp): uniq.setdefault(vkey(p), k)
        keep = sorted(uniq.values()); Pu = [Pp[k] for k in keep]
        rank, faces, edges, Hh = exact_hull(Pu, d, B)
        c = cent(Pu)
        tO, hitsO, _ = classify_edges(edges, Pu, d, surv, None)
        own = None
        if not iszero(c):
            tC, _, inw = classify_edges(edges, Pu, d, surv, c); own = {'plates': dict(tC), 'verdict': verdict(tC), 'fins_in_wall': inw}
        nm = regular_name(Pu, edges, d, rank, faces, Hh) if rank == 3 else regular_name(Pu, edges, d, rank, faces, None)
        r = {'shape': label, 'points': len(idx), 'distinct_images': len(Pu), 'rank': rank, 'edges': len(edges),
             'vertices': len(Hh['verts']) if rank == 3 else len({k for e in edges for k in e}),
             'faces': len(faces) if rank == 3 else None, 'face_census': face_census(Hh) if rank == 3 else None, 'name': nm,
             'centre_at_O': iszero(c), 'plates_O': dict(tO), 'distinct_plates_O': len(hitsO), 'verdict_O': verdict(tO), 'own': own,
             'walls_used': sorted(hitsO)}
        if extra: r.update(extra)
        if rank == 3:
            # faces of this outline whose plane is parallel to a kept wall (exact: face normal parallel to the wall normal)
            fk = Counter()
            for f in faces:
                m = gcross4(d, vsub(Pu[f[1]], Pu[f[0]]), vsub(Pu[f[2]], Pu[f[0]])); km = canon_dir(m); hit = 'none'
                for wi in surv:
                    if canon_dir(WALLS[wi][1]) == km: hit = WALLS[wi][0]; break
                fk[hit] += 1
            r['faces_parallel_to_kept_walls'] = dict(fk)
        r['_dirs'] = ({canon_dir(p) for p in Pu if not iszero(p)}, {canon_dir(vsub(Pu[i], Pu[j])) for i, j in edges})
        if MAIN:
            r['X3'] = (np.array([to_np(p) for p in Pu]) @ B).round(9).tolist(); r['edge_list'] = [list(map(int, e)) for e in edges]
            r['face_list'] = [list(map(int, f)) for f in faces] if rank == 3 else []
        return r
    for hk in heights:
        idx = H[hk]; h = Q5(*hk)
        layers.append(shape_record(f'layer h = {h}', idx, {'height': str(h), 'height_float': float(h)}))
    rec['layers'] = layers
    rec['hull'] = shape_record('shadow hull', list(range(len(P))))
    rec['surviving'] = surv
    # law: a wall survives iff it is parallel to a side-on cell of one Queen (cross: White Queen tetrahedra; mirror: Red Queen
    # dodecahedra, centred on the 600-cell corners) -- equivalently, its normal is an equator corner of the other Queen
    side_t = {WALL_ID[('t', ti)] for ti in range(len(TET)) if dot(R[ti], d).iszero()}
    side_d = {WALL_ID[('v', vi)] for vi in range(NV) if dot(V[vi], d).iszero()}
    check(set(surv) == side_t | side_d and len(side_t) == rec['walls']['cross'] and len(side_d) == rec['walls']['mirror'],
          f"{queen} {typ}: kept walls = planes of the side-on cells of the two Queens, moved to the centre ({len(side_d)} + {len(side_t)})")
    # what each kept normal is parallel to: corner or edge directions of the layer outlines / hull
    shapes_ = rec['layers'] + [rec['hull']]
    for o, oi in zip(orbs, rec['plane_orbits']):
        k = canon_dir(WALLS[o[0]][1])
        oi['normal_parallel_to_corners_of'] = sorted({L['name'].split(' (')[0] + ' h=' + L.get('height', 'hull') for L in shapes_ if k in L['_dirs'][0]})
        oi['normal_parallel_to_edges_of'] = sorted({L['name'].split(' (')[0] + ' h=' + L.get('height', 'hull') for L in shapes_ if k in L['_dirs'][1]})
    for L in shapes_: del L['_dirs']
    if MAIN:
        rec['wall_normals_3d'] = [{'wall': w, 'kind': WALLS[w][0], 'n': (to_np(WALLS[w][1]) @ B).round(9).tolist()} for w in surv]
    return rec, d, surv, st, B

# ------------------------------------------------------------------ main
RESULTS = {'checks_failed': FAILS}
types = ['V', 'E', 'F', 'C'] if not PILOT else ['V', 'C']
queens = ['600', '120'] if not PILOT else ['600']
SH = {}
for qn in queens:
    for typ in types:
        t1 = time.time()
        rec, d, surv, st, B = shadow(qn, typ)
        SH[(qn, typ)] = (rec, d, surv, st, B)
        RESULTS.setdefault('shadows', []).append(rec)
        for o in rec['plane_orbits']: log(f"  planes: {o}")
        log(f"SHADOW {qn} {rec['direction']}: walls kept {rec['walls']} (group on shadow {rec['group_on_shadow']}); plane orbits "
            + ', '.join(f"{o['planes']} {o['kind']} (normal stab {o['normal_line_stabiliser']})" for o in rec['plane_orbits'])
            + f"; cells {rec['side_counts']} in {rec['cell_orbits']} orbits, {rec['cell_classes']} congruence classes ({rec['front_classes']} among front cells)  [{time.time()-t1:.0f}s]")
        for L in rec['layers'] + [rec['hull']]:
            log(f"  {L['shape']}: {L['distinct_images']} pts {L['name']}; edges {L['edges']}; plates(O) {L['plates_O']} -> {L['verdict_O']}"
                + f"; faces parallel to kept walls {L.get('faces_parallel_to_kept_walls')}"
                + (f"; own {L['own']['plates']} -> {L['own']['verdict']}" if L['own'] else ''))
        vc = Counter((r['verdict_O'], r['verdict_own']) for r in rec['cells'] for _ in range(r['orbit_size']))
        log(f"  cells (verdict at O, verdict at own centre): {dict(vc)}")
        log(f'PROGRESS {len(SH)/(len(queens)*len(types)):.2f} {qn} {typ}')

# ---- checks against #63 / the Red Queen
if not PILOT:
    want600 = {'V': (42, 120, 80, 270, 60, 7), 'E': (52, None, 80, 290, 20, 22), 'F': (56, None, 96, 288, 24, 33), 'C': (44, None, 78, 273, 54, 20)}
    for typ, (nv, ne, nf, fr, so, kinds) in want600.items():
        rec = SH[('600', typ)][0]
        check(rec['hull']['vertices'] == nv and rec['hull']['faces'] == nf, f"600 {typ}: hull faces {rec['hull']['faces']} = #63 {nf}")
        check(rec['side_counts'].get('front') == fr and rec['side_counts'].get('side-on') == so, f"600 {typ}: front/side-on {rec['side_counts']} = #63 {fr}/{so}")
        log(f"INFO 600 {typ}: front-cell congruence classes {rec['front_classes']} (#63 kinds of front piece: {kinds})")
    want120 = {'C': (158, 240, 84, 54, 12), 'F': (180, 282, 104, 56, 8), 'E': (160, 250, 92, 54, 12), 'V': (80, 120, 42, 45, 30)}
    for typ, (nv, ne, nf, fr, so) in want120.items():
        rec = SH[('120', typ)][0]; Hh = rec['hull']
        check(Hh['vertices'] == nv and Hh['faces'] == nf and Hh['edges'] == ne, f"120 {typ}: hull edges/faces {Hh['edges']}/{Hh['faces']} = Red Queen {ne}/{nf}")
        check(rec['side_counts'].get('front') == fr and rec['side_counts'].get('side-on') == so, f"120 {typ}: front/side-on {rec['side_counts']} = Red Queen {fr}/{so}")

# ------------------------------------------------------------------ the lattice: incidence of shadows and walls
if not PILOT:
    INC = {}
    for typ in 'VEFC':
        for s in LINES[typ]: INC[(typ, s)] = set(walls_containing(dvec(s)))
    per_type = {typ: Counter(len(INC[(typ, s)]) for s in LINES[typ]) for typ in 'VEFC'}
    check(all(len(c) == 1 for c in per_type.values()), f'every shadow of one type keeps the same number of walls: {dict(per_type)}')
    wall_lines = []
    for wi in range(360):
        wall_lines.append({typ: sum(1 for s in LINES[typ] if wi in INC[(typ, s)]) for typ in 'VEFC'})
    by_kind = defaultdict(Counter)
    for wi, c in enumerate(wall_lines): by_kind[WALLS[wi][0]][tuple(c[t] for t in 'VEFC')] += 1
    RESULTS['wall_contains_lines'] = {k: {str(kk): v for kk, v in c.items()} for k, c in by_kind.items()}
    log('LATTICE each wall contains (V, E, F, C) shadow lines: ' + str({k: dict(c) for k, c in by_kind.items()}))
    reached = {typ: len(set().union(*[INC[(typ, s)] for s in LINES[typ]])) for typ in 'VEFC'}
    reached_k = {typ: dict(Counter(WALLS[w][0] for w in set().union(*[INC[(typ, s)] for s in LINES[typ]]))) for typ in 'VEFC'}
    RESULTS['walls_reached_by_type'] = reached_k
    log(f'LATTICE walls reached by the shadows of each type: {reached_k}')
    # shared walls between pairs of shadows
    keys = list(INC)
    share = defaultdict(Counter)
    for a, b in itertools.combinations(keys, 2):
        k = len(INC[a] & INC[b])
        share[''.join(sorted((a[0], b[0])))][k] += 1
    RESULTS['shared_walls_pairs'] = {k: dict(sorted(v.items())) for k, v in share.items()}
    log('LATTICE pairs of shadows by number of shared walls: ' + str({k: dict(sorted(v.items())) for k, v in share.items()}))
    # connectivity: shadow graph (edge = shared wall), per type and all; wall graph (edge = both kept by one shadow)
    def components(nodes, nbr):
        seen = set(); comps = 0
        for n0 in nodes:
            if n0 in seen: continue
            comps += 1; stack = [n0]; seen.add(n0)
            while stack:
                x = stack.pop()
                for y in nbr(x):
                    if y not in seen: seen.add(y); stack.append(y)
        return comps
    W2S = defaultdict(set)
    for k, ws in INC.items():
        for w in ws: W2S[w].add(k)
    def nbr_s(types_):
        def f(x):
            out = set()
            for w in INC[x]:
                out |= {y for y in W2S[w] if y[0] in types_}
            return out
        return f
    conn = {}
    for types_ in ['V', 'E', 'F', 'C', 'VEFC']:
        nodes = [k for k in keys if k[0] in types_]
        conn[types_] = components(nodes, nbr_s(types_))
    RESULTS['shadow_graph_components'] = conn
    log(f'LATTICE components of the shadow graph (shadows joined when they share a wall): {conn}')
    for types_ in ['V', 'E', 'F', 'C', 'VEFC']:
        nodes = list(range(360))
        def nbr_w(w, types_=types_):
            out = set()
            for k in W2S[w]:
                if k[0] in types_: out |= INC[k]
            return out
        c = components(nodes, nbr_w)
        RESULTS.setdefault('wall_graph_components', {})[types_] = c
    log(f"LATTICE components of the wall graph (walls joined when one shadow keeps both): {RESULTS['wall_graph_components']}")
    # the six turnings (#63): a view strictly inside the turning d1 -> d2 keeps exactly the walls containing both
    turn = {}
    for a, b in itertools.combinations('VEFC', 2):
        da, db = dvec(FLAG[a]), dvec(FLAG[b])
        ang = float(np.degrees(np.arccos(float(dot(da, db))/np.sqrt(float(dot(da, da))*float(dot(db, db))))))
        mid = vadd(vscale(Q5(3)/7, da), vscale(Q5(4)/7, db))
        both = set(walls_containing(da)) & set(walls_containing(db)); inner = set(walls_containing(mid))
        check(both == inner, f'turning {a}-{b}: a view inside keeps exactly the walls shared by both ends ({len(inner)})')
        turn[a + b] = {'angle_deg': round(ang, 3), 'kept': dict(Counter(WALLS[w][0] for w in inner))}
    RESULTS['turnings'] = turn
    log(f'TURNINGS {turn}')
    check(abs(turn['VE']['angle_deg'] - 18) < 1e-6 and abs(turn['VF']['angle_deg'] - 20.905) < 1e-3, 'turning angles match #63 (18, 20.905 deg)')

# ------------------------------------------------------------------ controls
ctrl = {}
dg = (Q5(1), Q5(1, 0)/3, Q5(2, 0)/7, Q5(5, 0)/11)
ctrl['generic_direction_walls'] = len(walls_containing(dg)); check(ctrl['generic_direction_walls'] == 0, 'control: a generic direction keeps no wall')
dgg = (Q5(1), Q5(0, 1)/3, Q5(2, 0)/7, Q5(5, 1)/11)
ctrl['generic_golden_direction_walls'] = len(walls_containing(dgg)); check(ctrl['generic_golden_direction_walls'] == 0, 'control: a generic Q(sqrt5) direction keeps no wall')
# a direction inside one mirror only: keeps exactly that one
n0 = V[MIRROR[0]]
dm = vsub(dg, vscale(dot(dg, n0)/dot(n0, n0), n0))
ctrl['direction_in_one_mirror'] = len(walls_containing(dm)); check(ctrl['direction_in_one_mirror'] == 1, f'control: a direction inside one mirror keeps exactly 1 wall ({ctrl["direction_in_one_mirror"]})')
# shape controls in the 600-cell corner-first shadow
rec, d, surv, st, B = SH[('600', 'V')]; dd = dot(d, d)
def qmul(a, b):
    a0, a1, a2, a3 = a; b0, b1, b2, b3 = b
    return (a0*b0 - a1*b1 - a2*b2 - a3*b3, a0*b1 + a1*b0 + a2*b3 - a3*b2, a0*b2 - a1*b3 + a2*b0 + a3*b1, a0*b3 + a1*b2 - a2*b1 + a3*b0)
def qconj(a): return (a[0], -a[1], -a[2], -a[3])
qa = tuple(Q5(x, 0)/5 for x in (1, 2, 2, 4))                         # rational unit quaternion
qb = vscale(Q5(1)/dd, qmul(qmul(qconj(d), qconj(qa)), d))             # x -> qa x qb fixes d, is orthogonal
def rotx(x): return qmul(qmul(qa, x), qb)
check(vkey(rotx(d)) == vkey(d) and all(dot(rotx(p), rotx(p)) == dot(p, p) for p in V[:10]), 'control: the exact rotation fixes d and is orthogonal')
cand = [L for L in rec['layers'] if L['verdict_O'] == 'possible Vacuus' and L['rank'] == 3]
CTRL_SHAPES = []
for L in cand[:3]:
    hk = None
    Hd = defaultdict(list)
    for i, p in enumerate(V): Hd[dot(p, d).key()].append(i)
    idx = Hd[[k for k in Hd if str(Q5(*k)) == L['height']][0]]
    Pp = [proj(V[i], d, dd) for i in idx]
    rank, faces, edges, _ = exact_hull(Pp, d, B)
    t0_, _, _ = classify_edges(edges, Pp, d, surv, None)
    # (a) symmetric rotation: a non-trivial element of the stabiliser -> must pass
    g, sgn = [x for x in st if not np.array_equal(x[0], np.arange(NV)) and x[1] == 1][5]
    Pg = [proj(V[int(g[i])], d, dd) for i in idx]
    ta, _, _ = classify_edges(edges, Pg, d, surv, None)
    # (b) generic exact rotation about the shadow centre -> must fail
    Pr = [rotx(p) for p in Pp]
    tb, _, _ = classify_edges(edges, Pr, d, surv, None)
    tb_own, _, _ = classify_edges(edges, Pr, d, surv, cent(Pr))
    # (c) one corner perturbed inside the shadow -> its edges must fail
    eps = proj((Q5(1, 0)/50, Q5(1, 0)/70, Q5(-1, 0)/90, Q5(1, 0)/110), d, dd)
    Pc = list(Pp); Pc[0] = vadd(Pc[0], eps)
    tc, _, _ = classify_edges(edges, Pc, d, surv, None)
    deg0 = sum(1 for i, j in edges if 0 in (i, j))
    # (d) translated inside the shadow: fails at O, passes at its own centre (fins parallel to the walls)
    Pt = [vadd(p, eps) for p in Pp]
    td, _, _ = classify_edges(edges, Pt, d, surv, None); td_own, _, _ = classify_edges(edges, Pt, d, surv, cent(Pt))
    row = {'shape': L['name'], 'height': L['height'], 'edges': len(edges), 'original': dict(t0_), 'symmetric_rotation': dict(ta),
           'generic_rotation_O': dict(tb), 'generic_rotation_own': dict(tb_own), 'one_corner_moved': dict(tc), 'corner_degree': deg0,
           'translated_O': dict(td), 'translated_own': dict(td_own)}
    CTRL_SHAPES.append(row)
    check(verdict(ta) == 'possible Vacuus', f"control pass: {L['name']} turned by a symmetry of the shadow stays a possible Vacuus")
    check(verdict(tb) == 'not', f"control fail: {L['name']} turned generically: {dict(tb)}")
    check(verdict(tb_own) == 'not', f"control fail: same, at its own centre: {dict(tb_own)}")
    check(tc['none'] >= deg0, f"control fail: {L['name']} with one corner moved loses its {deg0} edges at that corner ({dict(tc)})")
    check(verdict(td) != 'possible Vacuus' and td_own == t0_, f"control: {L['name']} translated fails at O ({dict(td)}), keeps its parallel fins at its own centre")
ctrl['shapes'] = CTRL_SHAPES
RESULTS['controls'] = ctrl
log('CONTROLS ' + json.dumps(ctrl, default=str))

RESULTS['seconds'] = round(time.time() - T0, 1)
json.dump(RESULTS, open(OUT, 'w'), indent=1, default=str)
log(f'{len(FAILS)} checks failed; {RESULTS["seconds"]} s')
print('FINAL ok' if not FAILS else f'FINAL FAIL {FAILS[:5]}')
sys.exit(1 if FAILS else 0)
