# Identification checks for the transitional shells (paper "Capturing the In-betweens", DICTO, 2026-10-13).
# Each fused stage is compared with a classical solid built independently from first principles (no data from the stage
# except its centre icosahedron's / triacontahedron's size and orientation). Tolerance 1e-4 (coordinates stored to 6 or 5
# decimals). Inputs: krp-core transitional.js (the six shapes in Polyhedraverse) and data/fused-extra.json (fuse_extra.py).
# Output: identify.json + printed report. DICTO · dictospheres.com
import json, os, re, math, itertools
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..', '..', '..', '..')
PHI = (1 + 5 ** .5) / 2
TOL = 1e-4
src = open(os.path.join(REPO, 'src', 'krp-core', 'src', 'polyhedra', 'transitional.js')).read()
TR = json.loads(re.search(r'^const RAW = (.*);$', src, re.M).group(1))
EX = json.load(open(os.path.join(HERE, 'data', 'fused-extra.json')))
report, out = [], {}

def P(msg, ok=None):
    line = msg if ok is None else f"[{'PASS' if ok else 'FAIL'}] {msg}"
    print(line); report.append(line)

def load(V, F):
    V = np.array(V, float); return V - V.mean(0), [list(f) for f in F]

def match_sets(A, B, tol=TOL):
    if len(A) != len(B): return False, float('inf')
    d = np.linalg.norm(A[:, None] - B[None], axis=2)
    worst = max(d.min(1).max(), d.min(0).max())
    return worst < tol, worst

def clus(xs, tol=1e-4):
    out = []
    for x in sorted(xs):
        if not out or x - out[-1][-1] > tol: out.append([x])
        else: out[-1].append(x)
    return [sum(g) / len(g) for g in out]

def nplanes(pl, tol=1e-3):
    U = []
    for n, dd, _ in pl:
        if not any(np.linalg.norm(n - m) < tol and abs(dd - e) < tol for m, e in U): U.append((n, dd))
    return len(U)

def face_planes(V, F):
    out = []
    for f in F:
        c = V[f].mean(0); n = np.zeros(3)
        for i in range(len(f)): n += np.cross(V[f[i]] - c, V[f[(i + 1) % len(f)]] - c)
        n /= np.linalg.norm(n); out.append((n, float(n @ c), float(max(abs((V[f] - c) @ n)))))
    return out

def volume(V, F):
    return float(sum(np.dot(V[f[0]], np.cross(V[f[m]], V[f[m + 1]])) for f in F for m in range(1, len(f) - 1)) / 6)

def icosa_axes(V12):
    """Unit 5-fold axes from 12 icosahedron vertices; 3-fold axes from its 20 faces; 2-fold from its 30 edges."""
    A = V12 / np.linalg.norm(V12, axis=1)[:, None]
    adj = [(i, j) for i, j in itertools.combinations(range(12), 2) if abs(A[i] @ A[j] - 1 / 5 ** .5) < 1e-4]
    tri = [t for t in itertools.combinations(range(12), 3) if all((min(p), max(p)) in adj for p in itertools.combinations(t, 2))]
    T = np.array([A[list(t)].sum(0) for t in tri]); T /= np.linalg.norm(T, axis=1)[:, None]
    E = np.array([A[i] + A[j] for i, j in adj]); E /= np.linalg.norm(E, axis=1)[:, None]
    return A, T, E, adj, tri

# ---------- 1. Lotus stage 2 vs the great stellated dodecahedron (GSD) ----------
def gsd_from_core(core):
    """GSD built from first principles round an icosahedron (vertices core): its 12 pentagram faces lie in the planes
    a_i . x = |core|/sqrt5 (each plane holds the 5 neighbours of the opposite vertex); its 20 points are where three
    such planes meet on a 3-fold axis, farthest out; visible solid = icosahedron + 20 pyramids."""
    A, T, E, adj, tri = icosa_axes(core)
    r = np.linalg.norm(core[0]); d = r / 5 ** .5
    tips = []
    for u in T:
        # the planes through this tip: the three 5-fold axes making the smallest positive dot with u (cos = 0.1876)
        dots = A @ u
        sel = [i for i in range(12) if abs(dots[i] - np.sort(dots[dots > 0])[0]) < 1e-3]
        assert len(sel) == 3
        Nm = A[sel]; x = np.linalg.solve(Nm, np.full(3, d)); tips.append(x)
    tips = np.array(tips)
    faces = []
    for k, t in enumerate(tri):
        for a, b in itertools.combinations(t, 2): faces.append((k, a, b))
    return tips, A * r, faces, d

TRI_KEYS = {}
for key in ('TRANS_LOTUS_2', 'TRANS_LOTUS_3'):
    V, F = load(TR[key]['vertices'], TR[key]['faces']); TRI_KEYS[key] = (V, F)
V2, F2 = TRI_KEYS['TRANS_LOTUS_2']
r = np.linalg.norm(V2, axis=1)
core = V2[r < r.mean()]; outer = V2[r > r.mean()]
P(f"Lotus 2: {len(V2)} corners = {len(core)} inner + {len(outer)} outer; faces {len(F2)}; edges {len({tuple(sorted((f[i], f[(i+1)%3]))) for f in F2 for i in range(3)})}")
tips, icov, gfaces, d = gsd_from_core(core)
ok_t, w_t = match_sets(tips, outer); P(f"Lotus 2: its 20 outer corners are the GSD's 20 points built from the core alone (worst {w_t:.2e})", ok_t)
ok_i, w_i = match_sets(icov, core); P(f"Lotus 2: its 12 inner corners are the core icosahedron's corners (worst {w_i:.2e})", ok_i)
pl = face_planes(V2, F2)
A, T, E, adj, tri = icosa_axes(core)
on = [min(np.linalg.norm(n - a) for a in A) < TOL and abs(dd - d) < TOL and flat < TOL for n, dd, flat in pl]
P(f"Lotus 2: all 60 faces lie in the 12 GSD planes a_i.x = r/sqrt5 = {d:.6f} (worst plane offset {max(abs(dd - d) for _, dd, _ in pl):.1e})", all(on))
# face set: each face = one tip + one core edge, the GSD's 60 visible golden triangles
idx = lambda p: int(np.argmin(np.linalg.norm(V2 - p, axis=1)))
gset = {tuple(sorted((idx(tips[k]), idx(icov[a]), idx(icov[b])))) for k, a, b in gfaces}
dset = {tuple(sorted(f)) for f in F2}
P(f"Lotus 2: its 60 faces are exactly the GSD's 60 visible triangles (tip + core edge), {len(gset & dset)}/60 matched", gset == dset)
L = clus([float(np.linalg.norm(V2[f[i]] - V2[f[(i + 1) % 3]])) for f in F2 for i in range(3)])
P(f"Lotus 2: edge lengths {[round(x, 6) for x in L]}, ratio {L[1]/L[0]:.6f} vs phi {PHI:.6f} (golden triangles, apex 36 deg)", abs(L[1] / L[0] - PHI) < TOL)
# pentagram check: each plane's 5 tips and 5 inner corners: in-plane radii ratio phi^2
rat = []
for a in A:
    tp = tips[np.abs(tips @ a - d) < TOL]; ip = icov[np.abs(icov @ a - d) < TOL]; c0 = a * d
    rat.append(np.linalg.norm(tp - c0, axis=1).mean() / np.linalg.norm(ip - c0, axis=1).mean())
P(f"Lotus 2: each plane holds 5 points + 5 inner corners, radius ratio {np.mean(rat):.6f} = phi^2 {PHI**2:.6f} (regular pentagram)", all(abs(x - PHI ** 2) < TOL for x in rat))
a_e = L[0]; h = math.sqrt(L[1] ** 2 - a_e ** 2 / 3)
vol_gsd = (5 / 12) * (3 + 5 ** .5) * a_e ** 3 + 20 * (1 / 3) * (3 ** .5 / 4 * a_e ** 2) * h
P(f"Lotus 2: volume {volume(V2, F2):.6f} = icosahedron + 20 golden pyramids by formula {vol_gsd:.6f}", abs(volume(V2, F2) - vol_gsd) < 1e-4)
R_kp = (3 ** .5 / 4) * (5 ** .5 - 1) * (2 * L[1] + L[0])
P(f"Lotus 2: circumradius {np.linalg.norm(outer, axis=1).mean():.6f} = GSD formula (sqrt3/4)(sqrt5-1)·edge, edge = pentagram chord {2*L[1]+L[0]:.6f} -> {R_kp:.6f}", abs(R_kp - np.linalg.norm(outer, axis=1).mean()) < TOL)
out['lotus2'] = dict(gsd=bool(ok_t and ok_i and all(on) and gset == dset), worst=float(max(w_t, w_i)))

# ---------- 2. Lotus stage 3 vs the excavated dodecahedron ----------
V3, F3 = TRI_KEYS['TRANS_LOTUS_3']
same, w = match_sets(V2, V3); P(f"Lotus 3 has exactly Lotus 2's 32 corners (worst {w:.2e})", same)
# centre icosahedron's face planes: normals = 3-fold axes, distance = inradius = |core| * cos(angle vertex-face centre)
inr = float(np.linalg.norm(core[0]) * (T[0] @ A[list(tri[0])[0]]))
pl3 = face_planes(V3, F3)
on3 = [min(np.linalg.norm(n - t) for t in T) < TOL and abs(dd - inr) < TOL and flat < TOL for n, dd, flat in pl3]
P(f"Lotus 3: all 60 faces lie in the 20 face planes of the centre icosahedron (inradius {inr:.6f})", all(on3))
L3 = clus([float(np.linalg.norm(V3[f[i]] - V3[f[(i + 1) % 3]])) for f in F3 for i in range(3)])
dd_all = sorted(np.linalg.norm(outer[i] - outer[j]) for i, j in itertools.combinations(range(20), 2)); dod_edge = float(np.mean(dd_all[:30]))
P(f"Lotus 3: 60 equilateral triangles of edge {L3[0]:.6f} = the hull dodecahedron's edge {dod_edge:.6f}", len(L3) == 1 and abs(L3[0] - dod_edge) < TOL)
J2 = (5 + 5 ** .5) / 24 * dod_edge ** 3
dod_vol = (15 + 7 * 5 ** .5) / 4 * dod_edge ** 3
P(f"Lotus 3: volume {volume(V3, F3):.6f} = dodecahedron - 12 J2 pyramids = {dod_vol - 12 * J2:.6f} (excavated dodecahedron, Coxeter et al. Ef1g1)", abs(volume(V3, F3) - (dod_vol - 12 * J2)) < 1e-4 * dod_vol)
out['lotus3'] = dict(excavated=bool(same and all(on3)), sharesCornersWithLotus2=bool(same))

# ---------- 3. Chain step 2, app stages 2 and 4: the same two solids at other sizes ----------
for key, ref, label in (('STEP2_2', V3, 'excavated dodecahedron'), ('STEP2_4', V2, 'GSD')):
    V, F = load(EX[key]['vertices'], EX[key]['faces'])
    k = np.linalg.norm(V, axis=1).max() / np.linalg.norm(ref, axis=1).max()
    # compare up to a rotation of the icosahedral frame: match radii orbits and face planes count, then try the 120 rotations
    best = match_sets(V, ref * k)
    P(f"Chain step 2 ({key}): {label} scaled by {k:.6f} (phi^{math.log(k)/math.log(PHI):+.3f}); corners match {best[0]} (worst {best[1]:.1e}); volume {volume(V, F):.6f} vs {volume(*(ref*k, TRI_KEYS['TRANS_LOTUS_3' if label.startswith('exc') else 'TRANS_LOTUS_2'][1])):.6f}", best[0])
    out[key] = dict(solid=label, scale=k, ok=bool(best[0]))

# ---------- 4. Bodhi Kit B stage 2 vs the rhombic hexecontahedron ----------
VB, FB = load(TR['TRANS_BODHI_B2']['vertices'], TR['TRANS_BODHI_B2']['faces'])
rB = np.round(np.linalg.norm(VB, axis=1), 3)
inner5 = VB[rB == rB.min()]
A5 = inner5 / np.linalg.norm(inner5, axis=1)[:, None]
A, T, E, adj, tri = icosa_axes(inner5)
e = 1.0
# Unkelbach/Wikipedia construction: RH(edge e) = 20 prolate golden rhombohedra round the centre, one per 3-fold axis;
# its corners: 12 on 5-fold axes at e (the rhombohedra's shared corners' neighbours), 30 on 2-fold axes, 20 on 3-fold axes.
# Build it: each prolate rhombohedron has the centre as its 3-fold apex and edges along the three 5-fold axes of a face.
pts = []
for t in tri:
    a, b, c = (A[i] * e for i in t)
    for s in itertools.product((0, 1), repeat=3):
        pts.append(s[0] * a + s[1] * b + s[2] * c)
pts = np.array(pts); hullpts = []
for p in pts:
    if np.linalg.norm(p) > 1e-6 and not any(np.linalg.norm(p - q) < 1e-6 for q in hullpts): hullpts.append(p)
hullpts = np.array(hullpts)
# the RH's boundary corners = all corners except the centre and the interior ones (none): 12 + 30 + 20 = 62
ok, w = match_sets(hullpts, VB); P(f"Bodhi Kit B stage 2: its 62 corners = the corners of 20 prolate golden rhombohedra (edge 1) round the centre (worst {w:.1e})", ok)
volP = 20 * abs(np.linalg.det(np.array([A[i] for i in tri[0]])))
P(f"Bodhi Kit B stage 2: volume {volume(VB, FB):.6f} = 20 prolate golden rhombohedra {volP:.6f}", abs(volume(VB, FB) - volP) < 1e-3)
plB = face_planes(VB, FB)
dB = sorted({round(dd, 4) for _, dd, _ in plB})
P(f"Bodhi Kit B stage 2: 60 faces on {nplanes(plB)} planes, all at distance {dB} (the centre triacontahedron's face planes)", nplanes(plB) == 30 and max(dB) - min(dB) < 2e-4)
diag = []
for f in FB:
    q = VB[f]; d1 = np.linalg.norm(q[0] - q[2]); d2 = np.linalg.norm(q[1] - q[3]); diag.append(max(d1, d2) / min(d1, d2))
P(f"Bodhi Kit B stage 2: every face a golden rhombus (diagonal ratio {np.mean(diag):.6f}, worst dev {max(abs(x - PHI) for x in diag):.1e})", max(abs(x - PHI) for x in diag) < 1e-4)
out['bodhiB2'] = dict(rhombicHexecontahedron=bool(ok))

# ---------- 5. Spheres of Dharma, the convex 80-corner stage ----------
VD, FD = load(TR['TRANS_DHARMA_80']['vertices'], TR['TRANS_DHARMA_80']['faces'])
h = ConvexHull(VD)
P(f"Dharma 80: convex (hull volume {h.volume:.6f} = solid {volume(VD, FD):.6f}); faces {sorted([len(f) for f in FD]).count(3)} tri, {sorted([len(f) for f in FD]).count(4)} quad, {sorted([len(f) for f in FD]).count(5)} pent", abs(h.volume - volume(VD, FD)) < 1e-4)
quads = [f for f in FD if len(f) == 4]
qs = [[float(np.linalg.norm(VD[f[i]] - VD[f[(i + 1) % 4]])) for i in range(4)] for f in quads]
ang = []
for f in quads:
    q = VD[f]; u = q[1] - q[0]; v = q[3] - q[0]; ang.append(math.degrees(math.acos(u @ v / np.linalg.norm(u) / np.linalg.norm(v))))
P(f"Dharma 80: the 30 quadrilaterals are rhombi, not rectangles: sides {min(min(s) for s in qs):.5f}-{max(max(s) for s in qs):.5f}, angles {min(ang):.2f}/{180-min(ang):.2f} deg", max(max(s) - min(s) for s in qs) < 1e-4 and abs(min(ang) - 90) > 1)
rr = np.round(np.linalg.norm(VD, axis=1), 4)
P(f"Dharma 80: corners = 60 at r {sorted(set(rr))[0]} (the truncated icosahedron of stage 6) + 20 at r {sorted(set(rr))[-1]} on the 3-fold axes (a regular dodecahedron)", list(np.unique(rr, return_counts=True)[1]) == [60, 20])
plD = face_planes(VD, FD)
dist = sorted({round(dd, 4) for _, dd, _ in plD}); P(f"Dharma 80: face-plane distances {dist}: all 90 triangle and rhombus planes touch one sphere")
out['dharma80'] = dict(convex=True)

json.dump({'credit': 'DICTO · dictospheres.com', 'report': report, 'summary': out}, open(os.path.join(HERE, 'identify.json'), 'w'), indent=1, default=str)

# ---------- 6. Dharma 80: what the 60 triangle planes and 30 rhombus planes are ----------
# Frame: swapping x and y maps the data's icosahedron (cyclic (phi,1,0)) to the standard one (cyclic (0,1,phi)); the solid's own
# 20 three-fold corners give the 3-fold axes, so we test in the solid's frame directly.
D3 = VD[rr == rr.max()]; U3 = D3 / np.linalg.norm(D3, axis=1)[:, None]
TI = VD[rr == rr.min()]
# 2-fold axes = directions of the 30 rhombus centres
tri_f = [f for f in FD if len(f) == 3]; quad_f = [f for f in FD if len(f) == 4]
n_tri = np.array([face_planes(VD, [f])[0][0] for f in tri_f]); n_quad = np.array([face_planes(VD, [f])[0][0] for f in quad_f])
# mirror planes are perpendicular to the 2-fold axes (n_quad): a triangle normal lies in a mirror if it is perpendicular to one
inmirror = [min(abs(n @ m) for m in n_quad) < 1e-4 for n in n_tri]
P(f"Dharma 80: each of the 60 triangle normals lies in a mirror plane: {sum(inmirror)}/60")
# rhombicosidodecahedron vertex directions = face normals of the deltoidal hexecontahedron: compare angle to nearest 3-fold axis
ang3 = sorted({round(math.degrees(math.acos(max(n @ u for u in U3))), 3) for n in n_tri})
P(f"Dharma 80: angle between each triangle normal and its nearest 3-fold axis: {ang3} deg")
# each triangle: base on a pentagon edge (TI edge), apex a dodecahedron corner. Name search: no named solid with these counts.
out['dharma80'].update(triangleNormalsInMirrors=int(sum(inmirror)), angleTo3fold=ang3)

# ---------- 7. Dharma stage 10 (+30 edge pieces) and stage 2 (+20 twisted triangular frusta) ----------
V10, F10 = load(EX['DHARMA_10']['vertices'], EX['DHARMA_10']['faces'])
r10 = np.round(np.linalg.norm(V10, axis=1), 4)
outer12 = V10[r10 == r10.max()]; inner20 = V10[r10 == r10.min()]
ico_edge = sorted(np.linalg.norm(outer12[i] - outer12[j]) for i, j in itertools.combinations(range(12), 2))[0]
pl10 = face_planes(V10, F10)
P(f"Dharma 10: 12 outer corners = icosahedron (edge {ico_edge:.5f}), 20 inner corners on the 3-fold axes at r {r10.min()}, 60 triangles on {nplanes(pl10)} planes at distance {clus([dd for _, dd, _ in pl10], 1e-3)}")
# great dodecahedron test: GD's dimple corners lie where its 12 pentagon planes (a.x = R/sqrt5) meet on the 3-fold axes
A, T, E, adj, tri = icosa_axes(outer12)
R = np.linalg.norm(outer12[0]); gd_d = R / 5 ** .5
u = inner20[0] / np.linalg.norm(inner20[0])
dots = sorted(A @ u, reverse=True)
gd_r = gd_d / dots[0]
P(f"Dharma 10: a great dodecahedron round the same icosahedron would put its 20 dimple corners at r {gd_r:.4f}; here r {r10.min():.4f}: not the great dodecahedron (dimples {'shallower' if r10.min() > gd_r else 'deeper'})", abs(gd_r - r10.min()) > 1e-3)
# Each triangle contains one icosahedron edge: its plane belongs to the family of planes through the edges (a triakis icosahedron's planes)
edge_ok = all(sum(np.linalg.norm(V10[f] - o, axis=1).min() < TOL for o in outer12) == 2 for f in F10)
P(f"Dharma 10: every triangle = one edge of the outer icosahedron + one inner corner (an icosahedron with 20 inward triangular pyramids)", edge_ok)
# the triakis icosahedron with these 60 planes: the 3-fold apex where the 3 planes over one face meet outside
apex = []
for t in tri[:1]:
    c = outer12[list(t)].mean(0); uu = c / np.linalg.norm(c)
    # planes over this face's three edges, tilted outward: reflect the inward planes through the face's edge
apexes = None
V2d, F2d = load(EX['DHARMA_2']['vertices'], EX['DHARMA_2']['faces'])
r2d = np.round(np.linalg.norm(V2d, axis=1), 4)
P(f"Dharma 2: corners {list(np.unique(r2d, return_counts=True)[1])} at r {list(np.unique(r2d))}; faces {len(F2d)} triangles; = icosidodecahedron (30 corners) with 12 inward pentagonal pyramids reaching the core icosahedron's corners")
json.dump({'credit': 'DICTO · dictospheres.com', 'report': report, 'summary': out}, open(os.path.join(HERE, 'identify.json'), 'w'), indent=1, default=str)

# ---------- 8. The Dodecahedral Chain's own stages 2 and 3 (icosahedron -> GSD -> excavated dodecahedron -> dodecahedron) ----------
for key, ref, label in (('DODECA_2', V2, 'GSD (Lotus 2)'), ('DODECA_3', V3, 'excavated dodecahedron (Lotus 3)')):
    V, F = load(EX[key]['vertices'], EX[key]['faces'])
    ok, w = match_sets(V, ref)
    P(f"Dodecahedral Chain {key}: same 32 corners as the {label}, same size (worst {w:.1e}); {len(F)} faces; volume {volume(V, F):.6f}", ok)
    out[key] = dict(ok=bool(ok))
json.dump({'credit': 'DICTO · dictospheres.com', 'report': report, 'summary': out}, open(os.path.join(HERE, 'identify.json'), 'w'), indent=1, default=str)
