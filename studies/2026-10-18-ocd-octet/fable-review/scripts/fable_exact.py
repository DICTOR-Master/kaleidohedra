# Fable review 2026-10-18 of the OCD octet study -- INDEPENDENT exact verification in Q(sqrt5).
# Own polytope engine (not exactpoly.py): a convex body is a list of planes n.x <= d (exact). Its corners are found by solving ALL
# plane triples: a float pre-screen may discard a triple only when its float solution violates some plane by > 1e-7 (or the triple
# is well-conditioned and clearly off); ill-conditioned triples are always solved exactly. Every kept corner is checked exactly
# against every plane. Volumes come from the exact corners (qhull gives only the facet combinatorics; every facet plane is
# re-proved exactly as a supporting plane). Interior-disjointness of two convex bodies = exact zero volume of their intersection.
# Output: data/fable-exact-checks.json. Run locally (light).
import sys, os, json, itertools, time, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, QhullError
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.join(HERE, '..', '..'); sys.path.insert(0, os.path.join(STUDY, 'scripts'))
from q5 import q, qs_, qa, qs, qm, qn, qr, qd, qinv, qf, sgn, vadd, vsub, vmul, dot, cross, det3, PHI, ONE, Z, MARK
OUT = os.path.join(HERE, '..', 'data'); os.makedirs(OUT, exist_ok=True)
loadS = lambda n: json.load(open(os.path.join(STUDY, 'data', n)))
f3 = lambda v: np.array([qf(x) for x in v], float)
qv = lambda v: [q(x) for x in v]
def qstr(x): return qs_(x) + f' ({qf(x):.9f})'
TOL_PRESCREEN = 1e-7

# ---------------------------------------------------------------- exact polytopes
def same_plane(p1, p2):
    (n1, d1), (n2, d2) = p1, p2
    if any(x != Z for x in cross(n1, n2)) or sgn(dot(n1, n2)) <= 0: return False
    return all(qm(d1, n2[i]) == qm(d2, n1[i]) for i in range(3))
def solve3(A, b):
    D = det3(*A)
    if D == Z: return None
    cols = lambda k: [[b[i] if j == k else A[i][j] for j in range(3)] for i in range(3)]
    return [qd(det3(*cols(k)), D) for k in range(3)]
def enumerate_corners(planes):
    """exact corners of {x : n.x <= d for all (n,d)}; empty list if empty or lower-dimensional"""
    m = len(planes)
    if m < 3: return []
    nf = np.array([f3(n) for n, d in planes]); df = np.array([qf(d) for n, d in planes]); nrm = np.linalg.norm(nf, axis=1)
    trip = np.array(list(itertools.combinations(range(m), 3)), int)
    cand = []
    for s in range(0, len(trip), 20000):
        T = trip[s:s + 20000]; A = nf[T]; b = df[T]
        det = np.linalg.det(A); scale = nrm[T].prod(1)
        ill = np.abs(det) < 1e-9 * scale
        X = np.zeros((len(T), 3))
        ok = ~ill
        if ok.any(): X[ok] = np.linalg.solve(A[ok], b[ok][..., None])[..., 0]
        viol = ((X @ nf.T) - df) / nrm
        keep = ill | (viol.max(1) <= TOL_PRESCREEN)
        cand += [tuple(t) for t in T[keep]]
    corners = []
    for i, j, k in cand:
        x = solve3([planes[i][0], planes[j][0], planes[k][0]], [planes[i][1], planes[j][1], planes[k][1]])
        if x is None: continue
        if all(sgn(qs(d, dot(n, x))) >= 0 for n, d in planes) and not any(all(a == b for a, b in zip(x, y)) for y in corners): corners.append(x)
    return corners
def exact_volume(corners):
    """exact volume of conv(corners); each qhull facet is re-proved exactly to be a supporting plane"""
    if len(corners) < 4: return Z
    Pf = np.array([f3(p) for p in corners])
    try: h = ConvexHull(Pf)
    except QhullError:
        return Z   # flat (all corners satisfy one plane both ways; a flat set has volume 0 by definition)
    vol = Z
    for s in h.simplices:
        a, b, c = corners[s[0]], corners[s[1]], corners[s[2]]; n = cross(vsub(b, a), vsub(c, a))
        if all(x == Z for x in n): continue
        side = [sgn(dot(n, vsub(p, a))) for p in corners]
        assert all(t <= 0 for t in side) or all(t >= 0 for t in side), 'facet plane is not a supporting plane'
        d = det3(a, b, c)
        if all(t <= 0 for t in side): vol = qa(vol, d)        # outward normal: signed fan from the origin
        else: vol = qs(vol, d)
    vol = qm(vol, qr(Fr(1, 6)))
    assert sgn(vol) >= 0 and abs(qf(vol) - h.volume) < 1e-9, ('volume mismatch', qf(vol), h.volume)
    return vol
class Poly:
    def __init__(self, planes, corners=None, name=''):
        self.planes = planes; self.name = name
        self.corners = enumerate_corners(planes) if corners is None else corners
        self.cf = np.array([f3(p) for p in self.corners]) if self.corners else np.zeros((0, 3))
        self._vol = None
    @property
    def vol(self):
        if self._vol is None: self._vol = exact_volume(self.corners)
        return self._vol
    def centre_radius(self):
        c = self.cf.mean(0); return c, np.linalg.norm(self.cf - c, axis=1).max()
    def shifted(self, t):
        return Poly([(n, qa(d, dot(n, t))) for n, d in self.planes], [vadd(p, t) for p in self.corners], self.name)
    def mapped(self, G, t):
        """image under x -> G x + t, G an exact 3x3 signed permutation (orthogonal), t exact"""
        Gt = [[G[j][i] for j in range(3)] for i in range(3)]                  # G^T
        mv = lambda M, v: [dot(M[i], v) for i in range(3)]
        planes = [(mv(G, n), qa(d, dot(mv(G, n), t))) for n, d in self.planes]   # (G n).(x) <= d + (G n).t
        return Poly(planes, [vadd(mv(G, p), t) for p in self.corners], self.name)
def hull_poly(points, name=''):
    """exact supporting planes of conv(points) from qhull facets, each proved exactly; corners re-enumerated and checked = points"""
    Pf = np.array([f3(p) for p in points]); h = ConvexHull(Pf); planes = []
    for s in h.simplices:
        a, b, c = points[s[0]], points[s[1]], points[s[2]]; n = cross(vsub(b, a), vsub(c, a))
        if all(x == Z for x in n): continue
        side = [sgn(dot(n, vsub(p, a))) for p in points]
        if all(t <= 0 for t in side): pl = (n, dot(n, a))
        elif all(t >= 0 for t in side): pl = ([qn(x) for x in n], qn(dot(n, a)))
        else: raise AssertionError('qhull facet not supporting')
        if not any(same_plane(pl, p2) for p2 in planes): planes.append(pl)
    P = Poly(planes, name=name)
    pts = [tuple(p) for p in points]
    assert all(tuple(c) in pts for c in P.corners), 'hull has a corner that is not an input point'
    return P
def intersect(A, B, name=''):
    """exact A & B with exact pruning: planes not cutting the other body are redundant; a plane excluding the other body -> empty"""
    if len(A.corners) == 0 or len(B.corners) == 0: return Poly([], [], name)
    cA, rA = A.centre_radius(); cB, rB = B.centre_radius()
    if np.linalg.norm(cA - cB) > rA + rB + 1e-6: return Poly([], [], name)
    planes = []
    for P, Q in ((A, B), (B, A)):
        for n, d in P.planes:
            s = [sgn(qs(d, dot(n, x))) for x in Q.corners]
            if all(t > 0 for t in s): continue                  # does not cut Q: redundant
            if all(t < 0 for t in s): return Poly([], [], name)   # excludes Q: empty
            if not any(same_plane((n, d), p2) for p2 in planes): planes.append((n, d))
    return Poly(planes, name=name)
def inter(*bodies, name=''):
    P = bodies[0]
    for B in bodies[1:]:
        P = intersect(P, B, name)
        if not P.corners: break
    return P

# ---------------------------------------------------------------- the geometry, rebuilt from the sources
t0 = time.time(); CH = {}
S1 = loadS('step1-ocd-exact.json'); V = [qv(v) for v in S1['V']]; R = q(S1['R']); faces = S1['faces']
assert R == qm(qr(Fr(2, 3)), PHI)
OCD = hull_poly(V, 'OCD'); CH['ocd_faces'] = len(OCD.planes); CH['ocd_corners'] = len(OCD.corners)
assert len(OCD.planes) == 80 and len(OCD.corners) == 102
sign_sets = list(itertools.product([1, -1], repeat=3))
octa_planes = [([qr(a), qr(b), qr(c)], R) for a, b, c in sign_sets]
OCTA = Poly(octa_planes, name='octa'); assert len(OCTA.corners) == 6
E = [[ONE if i == j else Z for j in range(3)] for i in range(3)]
TP = hull_poly([vmul(E[0], R), vmul(E[1], R), vmul(E[2], R), [R, R, R]], 'T+')
TM = hull_poly([[qn(x) for x in p] for p in TP.corners], 'T-')
L = [[R, R, Z], [R, Z, R], [Z, R, R]]
cell = det3(*L); cell = cell if sgn(cell) > 0 else qn(cell)
CH['cell'] = qstr(cell); CH['octa_vol'] = qstr(OCTA.vol); CH['tet_vol'] = qstr(TP.vol); CH['ocd_vol'] = qstr(OCD.vol)
CH['frame_volume_sum_equals_cell'] = qa(OCTA.vol, qa(TP.vol, TM.vol)) == cell
def lattice(nmax):
    for ijk in itertools.product(range(-nmax, nmax + 1), repeat=3):
        t = [Z, Z, Z]
        for c, Lv in zip(ijk, L): t = vadd(t, vmul(Lv, qr(c)))
        yield t
# OCD inside the octahedron, 48 corners on it, 8 hexagons on its faces
l1 = lambda v: qa(qa(*[x if sgn(x) >= 0 else qn(x) for x in v[:2]]), v[2] if sgn(v[2]) >= 0 else qn(v[2]))
CH['ocd_inside_octa'] = all(sgn(qs(R, l1(v))) >= 0 for v in V); CH['ocd_corners_on_octa'] = sum(l1(v) == R for v in V)
hexes = {}
for s in sign_sets:
    idx = [i for i, v in enumerate(V) if l1(v) == R and all(sgn(x) == si for x, si in zip(v, s))]
    hexes[s] = idx
CH['joint_hexagons'] = {''.join('+' if x > 0 else '-' for x in s): len(ix) for s, ix in hexes.items()}
assert all(len(ix) == 6 for ix in hexes.values())
# key from the RT (golden envelope), independently of step 3
G = json.load(open(os.path.join(STUDY, '..', '2026-10-16-ocd-pyrochlore', 'data', 'gbpc-geom-exact.json'))); RT = [qv(v) for v in G['RT']]
ssum = lambda v: qa(qa(v[0], v[1]), v[2])
apex = max(RT, key=lambda v: qf(ssum(v))); base = [v for v in RT if ssum(v) == R and all(sgn(x) >= 0 for x in v)]
assert len(base) == 3
S3 = loadS('step3-key-candidate.json'); assert sorted(map(tuple, [apex] + base)) == sorted(map(tuple, [qv(p) for p in S3['key']])), 'key differs from step 3'
CH['key_apex'] = [qs_(x) for x in apex]; CH['key_base'] = [[qs_(x) for x in p] for p in base]
CH['key_base_on_octa_edges'] = all(any(x == Z for x in p) for p in base)
CH['key_base_at_edge_midpoints'] = all(all(x == Z or x == qm(R, qr(Fr(1, 2))) for x in p) for p in base)
CH['key_base_splits_edge_in_ratio'] = 'phi : 1' if all(qd(max(p, key=qf), min([x for x in p if x != Z], key=qf)) == PHI for p in base) else 'other'
sv = lambda v, s: [x if si > 0 else qn(x) for x, si in zip(v, s)]
KEY = {s: hull_poly([sv(p, s) for p in [apex] + base], 'key' + ''.join('+' if x > 0 else '-' for x in s)) for s in sign_sets}
K0 = KEY[(1, 1, 1)]; CH['key_vol'] = qstr(K0.vol)
# key beyond the joint plane (zero-volume meeting with the octahedron) and inside T+
CH['key_outside_octa_exact'] = all(sgn(qs(ssum(p), R)) >= 0 for p in K0.corners) and intersect(K0, OCTA).vol == Z
CH['key_inside_Tplus_exact'] = all(all(sgn(qs(d, dot(n, p))) >= 0 for n, d in TP.planes) for p in K0.corners)
# hexagon inside the key base triangle? (hexagon corners lie on the base plane; test the 3 side half-spaces of the key)
side_planes = [(n, d) for n, d in K0.planes if not same_plane((n, d), ([qn(ONE)] * 3, qn(R)))]   # key lies on x+y+z >= R
assert len(side_planes) == 3
hex_in = [all(sgn(qs(d, dot(n, V[i]))) >= 0 for n, d in side_planes) for i in hexes[(1, 1, 1)]]
CH['hexagon_corners_inside_key_base'] = sum(hex_in); CH['hexagon_inside_key_base'] = all(hex_in)
# is the key mirror-symmetric in the face (x<->y)? exact: compare corner sets
swap = lambda p: [p[1], p[0], p[2]]
CH['key_mirror_symmetric_xy'] = sorted(map(tuple, [swap(p) for p in K0.corners])) == sorted(map(tuple, K0.corners))
print('setup', round(time.time() - t0, 1), 's', {k: CH[k] for k in ('key_base_at_edge_midpoints', 'key_base_splits_edge_in_ratio', 'hexagon_inside_key_base', 'key_mirror_symmetric_xy')}, flush=True)

# ---------------------------------------------------------------- the frame tiles space (exact)
# interior-disjointness of all frame bodies near the origin + volume per cell = cell  =>  exact tiling (closed pieces, density 1)
bodies = []
for t in lattice(2):
    for B in (OCTA, TP, TM):
        Bt = B.shifted(t); c, r = Bt.centre_radius()
        if np.linalg.norm(c) < 2.6: bodies.append(Bt)
ov = 0
for A, B in itertools.combinations(bodies, 2):
    if intersect(A, B).vol != Z: ov += 1
CH['frame_bodies_tested'] = len(bodies); CH['frame_pairs_with_positive_overlap'] = ov
print('frame', round(time.time() - t0, 1), 's; overlapping pairs', ov, flush=True)

# ---------------------------------------------------------------- keyed kit (step 5) lemmas, exact
# (a) the 6 corner cones partition R^3 (trivial: largest |coordinate| decides); cap_j = cone_j & octa - OCD
def cone(axis, sg):
    pl = []
    for k in range(3):
        if k == axis: continue
        for s in (1, -1):
            n = [Z, Z, Z]; n[k] = qr(s); n[axis] = qr(-sg); pl.append((n, Z))     # s*x_k - sg*x_axis <= 0
    return Poly(pl + octa_planes, name=f'cone{axis}{sg}')
CONES = {(ax, sg): cone(ax, sg) for ax in range(3) for sg in (1, -1)}
cap_vols = {}
for key_, C in CONES.items():
    cap_vols[key_] = qs(C.vol, intersect(C, OCD).vol)
import functools
CH['cone_octa_vol_each'] = qstr(CONES[(2, 1)].vol); CH['cones_sum_to_octa'] = functools.reduce(qa, [C.vol for C in CONES.values()], Z) == OCTA.vol
CH['cap_vols_all_equal'] = len({cv for cv in cap_vols.values()}) == 1; CH['cap_vol'] = qstr(cap_vols[(2, 1)])
CH['caps_plus_ocd_equals_octa'] = qa(functools.reduce(qa, cap_vols.values(), Z), OCD.vol) == OCTA.vol
# (b) keys: all keys of all nearby OCDs; pairwise zero overlap; each inside exactly one tetrahedron; zero overlap with octahedra
keys_all = []
for t in lattice(2):
    if np.linalg.norm(f3(t)) > 3.3: continue
    for s in sign_sets: keys_all.append((t, s, KEY[s].shifted(t)))
near_keys = [(t, s, K) for t, s, K in keys_all if np.linalg.norm(K.centre_radius()[0]) < 2.0]
CH['keys_tested'] = len(near_keys)
kk = sum(1 for (t1, s1, A), (t2, s2, B) in itertools.combinations(near_keys, 2) if np.linalg.norm(A.centre_radius()[0] - B.centre_radius()[0]) < 0.5 and intersect(A, B).vol != Z)
CH['key_pairs_with_positive_overlap'] = kk
tets_near = [B for B in bodies if B.name in ('T+', 'T-')]
octas_near = [B for B in bodies if B.name == 'octa']
def keys_in(T):
    out = []
    for t, s, K in keys_all:
        if np.linalg.norm(K.centre_radius()[0] - T.centre_radius()[0]) > 1.0: continue
        v = intersect(K, T).vol
        if v != Z: out.append((t, s, K, v))
    return out
kin_p = keys_in(TP); kin_m = keys_in(TM)
CH['keys_in_Tplus'] = len(kin_p); CH['keys_in_Tminus'] = len(kin_m)
CH['keys_in_Tplus_fully'] = all(v == K.vol for t, s, K, v in kin_p); CH['keys_in_Tminus_fully'] = all(v == K.vol for t, s, K, v in kin_m)
CH['keys_vs_octahedra_positive_overlap'] = sum(1 for O in octas_near for t, s, K in near_keys if np.linalg.norm(K.centre_radius()[0] - O.centre_radius()[0]) < 1.2 and intersect(K, O).vol != Z)
keyed_ocd = qa(OCD.vol, qm(qr(8), K0.vol)); dented_p = qs(TP.vol, functools.reduce(qa, [v for *_, v in kin_p], Z)); dented_m = qs(TM.vol, functools.reduce(qa, [v for *_, v in kin_m], Z))
CH['keyed_OCD_vol'] = qstr(keyed_ocd); CH['dented_tet_vol'] = qstr(dented_p); CH['dented_tets_equal'] = dented_p == dented_m
CH['keyed_kit_sum_equals_cell'] = qa(qa(keyed_ocd, functools.reduce(qa, cap_vols.values(), Z)), qa(dented_p, dented_m)) == cell
# (c) chirality of the dented tetrahedron: the 24 symmetries of T+ as exact affine maps (vertex permutations); which map the 4 keys to the 4 keys?
Tv = TP.corners
def affine_from_perm(perm):
    # x -> G x + t with G[Tv[i]] + t = Tv[perm[i]]; solve from differences (exact)
    D = [vsub(Tv[i], Tv[0]) for i in (1, 2, 3)]; Dp = [vsub(Tv[perm[i]], Tv[perm[0]]) for i in (1, 2, 3)]
    # G D = Dp  ->  G = Dp D^-1 ; columns
    Dm = [[D[j][i] for j in range(3)] for i in range(3)]; Dpm = [[Dp[j][i] for j in range(3)] for i in range(3)]   # as matrices with columns D[j]
    # solve for G row by row: row_i of G satisfies row_i . D[j] = Dpm[i][j]
    Grows = [solve3(D, [Dpm[i][j] for j in range(3)]) for i in range(3)]
    G = Grows; t = vsub(Tv[perm[0]], [dot(G[i], Tv[0]) for i in range(3)])
    return G, t
def key_set_image(G, t, keyset):
    S = [sorted(tuple(vadd([dot(G[i], p) for i in range(3)], t)) for p in K.corners) for K in keyset]
    return S
kset_p = [K for t, s, K, v in kin_p]; kset_ref = sorted(sorted(tuple(p) for p in K.corners) for K in kset_p)
sym = dict(proper_symmetries=0, improper_symmetries=0, proper_tested=0, improper_tested=0)
for perm in itertools.permutations(range(4)):
    G, t = affine_from_perm(perm); detG = det3(*G); improper = sgn(detG) < 0
    ok = sorted(key_set_image(G, t, kset_p)) == kset_ref
    sym['improper_tested' if improper else 'proper_tested'] += 1
    if ok: sym['improper_symmetries' if improper else 'proper_symmetries'] += 1
CH['dented_tet_symmetry'] = sym
CH['dented_tet_is_chiral'] = sym['improper_symmetries'] == 0
print('keyed kit', round(time.time() - t0, 1), 's', sym, flush=True)

# ---------------------------------------------------------------- the middle pieces (full kit)
r2 = [dot(v, v) for v in V]; rmax = max(r2, key=qf); five = [i for i in range(len(V)) if r2[i] == rmax]
assert len(five) == 12
def star_of(i): return [V[j] for j in sorted({j for f in faces if i in f for j in f})]
def H_of(i):
    c = V[i]; o = [qm(R, qr(sgn(x))) for x in c]; st = star_of(i)
    return hull_poly(st + [vsub(o, p) for p in st], f'H{i}'), o
Hs = {}
for i in five:
    H, o = H_of(i); m = vmul(o, qr(Fr(1, 2))); Hs[i] = (H, o, m)
CH['star_corners'] = len(star_of(five[0])); CH['H_corners'] = len(Hs[five[0]][0].corners); CH['H_faces'] = len(Hs[five[0]][0].planes)
CH['H_vol'] = qstr(Hs[five[0]][0].vol); CH['H_vols_all_equal'] = len({H.vol for H, o, m in Hs.values()}) == 1
# all distinct middle hulls near the origin (dedupe by midpoint m + t)
Mlist = {}
for t in lattice(2):
    if np.linalg.norm(f3(t)) > 3.3: continue
    for i in five:
        H, o, m = Hs[i]; mm = tuple(vadd(m, t))
        if np.linalg.norm(f3(list(mm))) < 2.2 and mm not in Mlist: Mlist[mm] = (H.shifted(t), i, t)
CH['middle_hulls_near_origin'] = len(Mlist)
# the inversion through m maps H to itself (exact corner sets)
H1, o1, m1 = Hs[[i for i in five if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]]
CH['H_inversion_symmetric'] = sorted(tuple(vsub(o1, p)) for p in H1.corners) == sorted(tuple(p) for p in H1.corners)
# K4: H lies in the 4 cells round its edge? exact: vol(H) = sum over ALL nearby frame bodies of vol(H & body); list the nonzero ones
def cells_hit(H):
    hits = []; tot = Z
    for B in bodies:
        if np.linalg.norm(B.centre_radius()[0] - H.centre_radius()[0]) > B.centre_radius()[1] + H.centre_radius()[1] + 1e-6: continue
        v = intersect(H, B).vol
        if v != Z: hits.append((B.name, B.centre_radius()[0].round(6).tolist(), v)); tot = qa(tot, v)
    return hits, tot
hits, tot = cells_hit(H1)
CH['H_cells_hit'] = [(n, c, qstr(v)) for n, c, v in hits]; CH['H_vol_equals_sum_over_cells'] = tot == H1.vol
CH['H_within_4_cells_round_edge'] = tot == H1.vol and len(hits) == 4 and sorted(n for n, c, v in hits) == ['T+', 'T-', 'octa', 'octa']
# K5: H against every nearby keyed OCD (OCD translates and all keys): which have positive overlap?
ocds_near = [(t, OCD.shifted(t)) for t in lattice(2) if np.linalg.norm(f3(t)) < 2.6]
def keyed_hits(H):
    out = []
    for t, O in ocds_near:
        if np.linalg.norm(O.centre_radius()[0] - H.centre_radius()[0]) > O.centre_radius()[1] + H.centre_radius()[1] + 1e-6: continue
        v = intersect(H, O).vol
        if v != Z: out.append(('OCD', f3(t).round(6).tolist(), '', v))
    for t, s, K in keys_all:
        if np.linalg.norm(K.centre_radius()[0] - H.centre_radius()[0]) > K.centre_radius()[1] + H.centre_radius()[1] + 1e-6: continue
        v = intersect(H, K).vol
        if v != Z: out.append(('key', f3(t).round(6).tolist(), ''.join('+' if x > 0 else '-' for x in s), v))
    return out
kh = keyed_hits(H1)
CH['H_keyed_OCD_hits'] = [(a, b, c, qstr(v)) for a, b, c, v in kh]
CH['H_hits_only_its_two_OCDs'] = sorted(b for a, b, c, v in kh if a == 'OCD') == sorted([[0.0, 0.0, 0.0], f3(o1).round(6).tolist()])
CH['H_key_hits_count'] = sum(1 for a, *_ in kh if a == 'key')
CH['H_key_hits_belong_to_its_two_OCDs'] = all(b in ([0.0, 0.0, 0.0], f3(o1).round(6).tolist()) for a, b, c, v in kh if a == 'key')
vM = H1.vol
for a, b, c, v in kh: vM = qs(vM, v)
CH['middle_vol'] = qstr(vM); S11 = loadS('step11-exact.json')['checks']; CH['middle_vol_matches_step11'] = vM == q(S11['middle'])
# M with keys removed from the design (improvement A): M0 = H - two OCDs only
vM0 = H1.vol
for a, b, c, v in kh:
    if a == 'OCD': vM0 = qs(vM0, v)
CH['middle_vol_without_keys'] = qstr(vM0)
print('middle', round(time.time() - t0, 1), 's; cells', [(n, qf(v)) for n, c, v in hits], 'keyed hits', [(a, c, qf(v)) for a, b, c, v in kh], flush=True)
# K6: middle hulls pairwise: positive overlap of H_e & H_e'? if so, is the overlap entirely inside OCDs/keys (then M_e & M_e' is still empty)?
pairs_tested = 0; pairs_H_overlap = 0; pairs_M_overlap = 0; worst = []
Ml = list(Mlist.items())
for (ma, (Ha, ia, ta)), (mb, (Hb, ib, tb)) in itertools.combinations(Ml, 2):
    if np.linalg.norm(f3(list(ma)) - f3(list(mb))) > 2 * H1.centre_radius()[1] + 1e-6: continue
    if np.linalg.norm(f3(list(ma))) > 1.3: continue                      # one of the pair close to the origin cell suffices by symmetry; test all with ma near
    pairs_tested += 1
    X = intersect(Ha, Hb)
    if X.vol == Z: continue
    pairs_H_overlap += 1
    cover = Z
    for t, O in ocds_near:
        v = intersect(X, O).vol; cover = qa(cover, v)
    for t, s, K in keys_all:
        if np.linalg.norm(K.centre_radius()[0] - X.centre_radius()[0]) > K.centre_radius()[1] + X.centre_radius()[1] + 1e-6: continue
        cover = qa(cover, intersect(X, K).vol)
    if cover != X.vol: pairs_M_overlap += 1; worst.append((ma, mb, qstr(X.vol), qstr(cover)))
    else: worst.append(([round(qf(x), 4) for x in ma], [round(qf(x), 4) for x in mb], 'H&H', qstr(X.vol), 'all inside OCDs/keys'))
CH['middle_pairs_tested'] = pairs_tested; CH['middle_pairs_with_hull_overlap'] = pairs_H_overlap; CH['middle_pairs_with_PIECE_overlap'] = pairs_M_overlap
CH['middle_pair_details'] = worst[:12]
print('M pairs', round(time.time() - t0, 1), 's', pairs_tested, pairs_H_overlap, pairs_M_overlap, flush=True)

# ---------------------------------------------------------------- exact piece volumes WITHOUT symmetry shortcuts
# notched cap_j = cone_j & octa - OCD - all middle hulls that reach it (keys and other OCDs do not enter this octahedron)
Hnear = [(H, i, t) for mm, (H, i, t) in Mlist.items()]
ncap = {}
for key_, C in CONES.items():
    v = cap_vols[key_]; taken = []
    for H, i, t in Hnear:
        if np.linalg.norm(H.centre_radius()[0] - C.centre_radius()[0]) > H.centre_radius()[1] + C.centre_radius()[1] + 1e-6: continue
        X = intersect(H, C)
        if X.vol == Z: continue
        share = qs(X.vol, intersect(X, OCD).vol); v = qs(v, share)
        if share != Z: taken.append(share)
    ncap[key_] = (v, taken)
CH['notched_cap_vols_all_equal'] = len({v for v, tk in ncap.values()}) == 1
CH['notched_cap_vol'] = qstr(ncap[(2, 1)][0]); CH['notched_cap_matches_step11'] = ncap[(2, 1)][0] == q(S11['notched_cap'])
CH['middles_notching_one_cap'] = len(ncap[(2, 1)][1]); CH['cap_notch_shares'] = sorted({qs_(x) for x in ncap[(2, 1)][1]})
CH['cap_notch_shares_equal'] = len({x for x in ncap[(2, 1)][1]}) == 1
# notched tetrahedron = dented tet - sum over middle hulls of [vol(H & T) - sum over keys of vol(H & T & key)]
def notched_tet(T, kin):
    v = qs(T.vol, functools.reduce(qa, [vv for *_, vv in kin], Z)); shares = []
    for H, i, t in Hnear:
        if np.linalg.norm(H.centre_radius()[0] - T.centre_radius()[0]) > H.centre_radius()[1] + T.centre_radius()[1] + 1e-6: continue
        X = intersect(H, T)
        if X.vol == Z: continue
        s = X.vol
        for tk, sk, K, vk in kin: s = qs(s, intersect(X, K).vol)
        if s != Z: shares.append(s); v = qs(v, s)
    return v, shares
ntp, shp = notched_tet(TP, kin_p); ntm, shm = notched_tet(TM, kin_m)
CH['notched_tet_vol'] = qstr(ntp); CH['notched_tets_equal_volume'] = ntp == ntm; CH['notched_tet_matches_step11'] = ntp == q(S11['notched_tet'])
CH['middles_notching_one_tet'] = len(shp); CH['tet_notch_shares_equal'] = len(set(shp)) == 1; CH['tet_notch_share'] = qstr(shp[0])
# M split between its 4 cells, directly
split_vals = []
for B in bodies:
    if np.linalg.norm(B.centre_radius()[0] - H1.centre_radius()[0]) > B.centre_radius()[1] + H1.centre_radius()[1] + 1e-6: continue
    X = intersect(H1, B)
    if X.vol == Z: continue
    s = X.vol
    for t, O in ocds_near: s = qs(s, intersect(X, O).vol)
    for t, sg, K in keys_all:
        if np.linalg.norm(K.centre_radius()[0] - X.centre_radius()[0]) > K.centre_radius()[1] + X.centre_radius()[1] + 1e-6: continue
        s = qs(s, intersect(X, K).vol)
    split_vals.append((B.name, qstr(s)))
CH['middle_split_over_its_cells'] = split_vals
# totals
sixM = qm(qr(6), vM); total_full = qa(qa(keyed_ocd, functools.reduce(qa, [v for v, tk in ncap.values()], Z)), qa(sixM, qa(ntp, ntm)))
CH['full_kit_sum_equals_cell'] = total_full == cell; CH['full_kit_sum'] = qstr(total_full)
print('pieces', round(time.time() - t0, 1), 's; full kit sum == cell:', total_full == cell, flush=True)

# ---------------------------------------------------------------- Penrose core (step 13/15): rhombus angles and exact volume
c1 = V[[i for i in five if V[i][0] == Z and sgn(V[i][1]) > 0 and sgn(V[i][2]) > 0][0]]; c2 = vsub(o1, c1); a = c1; aa = dot(a, a)
proj = lambda v: vsub(v, vmul(a, qd(dot(v, a), aa)))
st = star_of([i for i in five if V[i] == c1][0]); rel = [proj(vsub(p, c1)) for p in st]
rr = [dot(t, t) for t in rel]; rt = max(rr, key=qf); tips = [t for t, x in zip(rel, rr) if x == rt]; assert len(tips) == 5
d = proj(vsub(c2, c1)); iphi = qinv(PHI)
pair = [(i, j) for i in range(5) for j in range(i + 1, 5) if vmul(vadd(tips[i], tips[j]), iphi) == d]
CH['c1c2_projected_is_sum_of_two_spokes_over_phi'] = len(pair) == 1
i, j = pair[0]; e1, e2 = vmul(tips[i], iphi), vmul(tips[j], iphi)
cosang = qd(dot(e1, e2), dot(e1, e1))
CH['rhombus_edges_equal'] = dot(e1, e1) == dot(e2, e2); CH['rhombus_cos_at_c1'] = qstr(cosang)
CH['rhombus_angle_at_c1_deg'] = float(np.degrees(np.arccos(qf(cosang)))); CH['rhombus_is_thick_penrose_72_108'] = cosang == (Fr(-1, 4), Fr(1, 4))
CH['rhombus_long_diagonal_equals_tip_radius'] = dot(d, d) == rt
rh = [c1, vadd(c1, e1), vadd(c1, d), vadd(c1, e2)]; cen = [qm(functools.reduce(qa, [p[k] for p in rh], Z), qr(Fr(1, 4))) for k in range(3)]
side = []
for k in range(4):
    n = cross(vsub(rh[(k + 1) % 4], rh[k]), a); dd = dot(n, rh[k])
    if sgn(qs(dot(n, cen), dd)) > 0: n = [qn(x) for x in n]; dd = qn(dd)
    side.append((n, dd))
S15 = loadS('step15-core.json'); CH['rhombus_matches_step15'] = sorted(tuple(p) for p in rh) == sorted(tuple(qv(p)) for p in S15['rhombus'])
PH = Poly(side + H1.planes, name='prism&H')
vcore = PH.vol; core_hits = []
for t, O in ocds_near:
    v = intersect(PH, O).vol
    if v != Z: core_hits.append(('OCD', f3(t).round(6).tolist(), v)); vcore = qs(vcore, v)
for t, s, K in keys_all:
    if np.linalg.norm(K.centre_radius()[0] - PH.centre_radius()[0]) > K.centre_radius()[1] + PH.centre_radius()[1] + 1e-6: continue
    v = intersect(PH, K).vol
    if v != Z: core_hits.append(('key', f3(t).round(6).tolist(), v)); vcore = qs(vcore, v)
CH['prism_and_H_vol'] = qstr(PH.vol); CH['core_vol'] = qstr(vcore); CH['core_matches_step15'] = vcore == q(S15['checks']['core'])
CH['core_hits'] = [(a, b, qstr(v)) for a, b, v in core_hits]; CH['core_clear_of_keys'] = not any(a == 'key' for a, b, v in core_hits)
CH['rest_vol'] = qstr(qs(vM, vcore))
# does the prism stay inside H (i.e. is the core a full prism between the OCD surfaces)? exact: prism & cells vs prism & H
# the prism is unbounded along a: bound it generously (2|a| each way), then keep what lies in the 4 cells and outside OCDs/keys
bound = Poly(side + [(a, dot(a, vadd(c1, vmul(a, qr(2))))), ([qn(x) for x in a], qn(dot(a, vsub(c1, vmul(a, qr(2))))))], name='prism_bounded')
# volume of the prism between the two OCD surfaces (inside octa1 u octa2 u T1 u T2), exact, vs inside H
cells4 = [B for B in bodies if any(B.name == n and np.allclose(B.centre_radius()[0], c) for n, c, v in hits)]
vprism_cells = Z
for B in cells4:
    X = intersect(bound, B); s = X.vol
    for t, O in ocds_near: s = qs(s, intersect(X, O).vol)
    for t, sg, K in keys_all:
        if np.linalg.norm(K.centre_radius()[0] - X.centre_radius()[0]) > K.centre_radius()[1] + X.centre_radius()[1] + 1e-6: continue
        s = qs(s, intersect(X, K).vol)
    vprism_cells = qa(vprism_cells, s)
CH['prism_between_OCDs_within_4_cells_vol'] = qstr(vprism_cells); CH['core_share_of_full_prism_between_OCDs'] = qf(vcore) / qf(vprism_cells)
print('core', round(time.time() - t0, 1), 's', CH['rhombus_angle_at_c1_deg'], qf(vcore), flush=True)

# ---------------------------------------------------------------- improvement A: key cut down to the part above the hexagon
# key' = key & (prism over the hexagon along the face normal); overhang parts stay with the tetrahedron. Exact volumes.
hexpts = [V[i] for i in hexes[(1, 1, 1)]]; nrm = [ONE, ONE, ONE]
hex_prism_planes = []
cenh = [qm(functools.reduce(qa, [p[k] for p in hexpts], Z), qr(Fr(1, 6))) for k in range(3)]
# order hexagon corners round the centre (float angles), planes through consecutive corners parallel to the normal
hf = np.array([f3(p) for p in hexpts]); cf = hf.mean(0); u = hf[0] - cf; w = np.cross(f3(nrm), u)
order = np.argsort(np.arctan2((hf - cf) @ w, (hf - cf) @ u))
for k in range(6):
    p1, p2 = hexpts[order[k]], hexpts[order[(k + 1) % 6]]; n = cross(vsub(p2, p1), nrm); dd = dot(n, p1)
    if sgn(qs(dot(n, cenh), dd)) > 0: n = [qn(x) for x in n]; dd = qn(dd)
    hex_prism_planes.append((n, dd))
KEYH = Poly(K0.planes + hex_prism_planes, name='key_hex')
CH['impA_key_hex_vol'] = qstr(KEYH.vol); CH['impA_key_hex_share_of_key'] = qf(KEYH.vol) / qf(K0.vol)
CH['impA_key_hex_corners'] = len(KEYH.corners)
# does the hexagon-trimmed key still reach the middle hull H? (exact) -- all 4 keys that met H, trimmed
hits_trim = []
for t, s, K in keys_all:
    if np.linalg.norm(K.centre_radius()[0] - H1.centre_radius()[0]) > K.centre_radius()[1] + H1.centre_radius()[1] + 1e-6: continue
    if intersect(H1, K).vol == Z: continue
    Kh = Poly([(sv(n, s), d) for n, d in KEYH.planes], name='kh').shifted(t)
    hits_trim.append(qstr(intersect(H1, Kh).vol))
CH['impA_trimmed_keys_meeting_H'] = hits_trim
CH['impA_trimmed_key_clear_of_H'] = all(x.startswith('0|0') for x in hits_trim)
json.dump(dict(mark=MARK, review='Fable 2026-10-18 independent exact verification', prescreen_tolerance=TOL_PRESCREEN, seconds=round(time.time() - t0, 1), checks=CH),
          open(os.path.join(OUT, 'fable-exact-checks.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(CH, indent=1, ensure_ascii=False)); print('done', round(time.time() - t0, 1), 's')
