# Fable review 4 (2026-10-18): exploration of the W_star bump face 1 = (A0, E0, T+) in the plane z = x: socket rim (OCD section), OCD shadow
# (projection along the face normal), kite shape, where the star's kite edges pierce the plane. Float from exact data. -> data/explore-face.json
import sys, os, json, math, itertools, numpy as np
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/2026-10-18-p4-golden-octet-adaptor/fable-review-3/scripts')
from fable3_engine import *
from fable3_engine import loadS, f3, qv, hull_poly, Poly
from q5 import *
from scipy.spatial import ConvexHull
S1 = loadS('step1-ocd-exact.json'); V = [qv(v) for v in S1['V']]; R = qf(q(S1['R'])); faces = S1['faces']
OCD = hull_poly(V, 'OCD'); Vf = np.array([f3(v) for v in V])
u = np.array([0, 1, 0.]); w = np.array([1, 0, 1.]) / np.sqrt(2); n = np.array([1, 0, -1.]) / np.sqrt(2)
uv = lambda P: np.c_[P @ u, P @ w]
A, E, T = np.zeros(3), np.array([0, R, 0]), np.array([R / 2, R / 2, R / 2]); tri = uv(np.array([A, E, T]))
# section by z = x (through the centre): exact corners via the engine
sec = Poly(OCD.planes + [([ONE, Z, qn(ONE)], Z), ([qn(ONE), Z, ONE], Z)], name='sec'); S = np.array([f3(c) for c in sec.corners]); Suv = uv(S); Suv = Suv[ConvexHull(Suv).vertices]
# shadow = projection of all corners along n
Sh = uv(Vf); Sh = Sh[ConvexHull(Sh).vertices]
# kite geometry
def poly_of(pl):
    on = [c for c in OCD.corners if dot(pl[0], c) == pl[1]]; P = np.array([f3(c) for c in on]); c0 = P.mean(0); nf = f3(pl[0]); a = P[0] - c0; a -= nf * (a @ nf) / (nf @ nf); b = np.cross(nf, a)
    return P[np.argsort(np.arctan2((P - c0) @ b, (P - c0) @ a))]
quads = [poly_of(pl) for pl in OCD.planes if len(poly_of(pl)) == 4]; hexs = [poly_of(pl) for pl in OCD.planes if len(poly_of(pl)) == 6]
def edges_angles(P):
    e = [np.linalg.norm(P[(i + 1) % len(P)] - P[i]) for i in range(len(P))]
    ang = [math.degrees(math.acos(np.clip((P[i - 1] - P[i]) @ (P[(i + 1) % len(P)] - P[i]) / np.linalg.norm(P[i - 1] - P[i]) / np.linalg.norm(P[(i + 1) % len(P)] - P[i]), -1, 1))) for i in range(len(P))]
    return [round(x, 5) for x in e], [round(x, 3) for x in ang]
kite_e, kite_a = edges_angles(quads[0]); hex_e, hex_a = edges_angles(hexs[0])
# star centre facing m
r = np.linalg.norm(Vf, axis=1); five = [i for i in range(len(V)) if abs(r[i] - r.max()) < 1e-9]
i1 = [i for i in five if abs(Vf[i, 0]) < 1e-9 and Vf[i, 1] > 0 and Vf[i, 2] > 0][0]; c1 = Vf[i1]
star_faces = [f for f in faces if i1 in f]
# all OCD edges (from faces), those crossing the plane z = x, with the crossing point and in-plane direction; mark star edges
edges = set()
for f in faces:
    for k in range(len(f)): edges.add((min(f[k], f[(k + 1) % len(f)]), max(f[k], f[(k + 1) % len(f)])))
star_edges = set()
for f in star_faces:
    for k in range(len(f)): star_edges.add((min(f[k], f[(k + 1) % len(f)]), max(f[k], f[(k + 1) % len(f)])))
pierce = []
for a, b in edges:
    za, zb = Vf[a] @ n, Vf[b] @ n
    if za * zb < 0:
        t = za / (za - zb); P = Vf[a] + t * (Vf[b] - Vf[a]); d = Vf[b] - Vf[a]; d = d if zb < 0 else -d     # direction pointing from the + side (cell) down through the plane
        din = d - (d @ n) * n; ang = math.degrees(math.atan2(din @ w, din @ u))
        puv = uv(P[None])[0]
        pierce.append(dict(edge=[a, b], uv=puv.round(4).tolist(), inplane_dir_deg=round(ang, 2), star_edge=(a, b) in star_edges, in_triangle=bool(puv[1] >= -1e-9 and puv[1] <= np.sqrt(2) * min(puv[0], R - puv[0]) + 1e-9), len=round(np.linalg.norm(Vf[b] - Vf[a]), 5)))
pierce_tri = [p for p in pierce if p['in_triangle']]
out = dict(R=R, frame=dict(u=u.tolist(), w=w.tolist(), n=n.tolist()), triangle_uv=tri.round(5).tolist(), section_uv=Suv.round(5).tolist(), shadow_uv=Sh.round(5).tolist(),
           section_corners=len(sec.corners), shadow_corners=len(Sh), kite_edges=kite_e, kite_angles=kite_a, hex_edges=hex_e, hex_angles=hex_a,
           c1=c1.round(5).tolist(), c1_uv=uv(c1[None])[0].round(5).tolist(), c1_height_above_plane=float(c1 @ n), star_faces=len(star_faces),
           pierce_in_triangle=sorted(pierce_tri, key=lambda p: p['uv'][0]), n_pierce_total=len(pierce))
# free zone area: triangle minus shadow (shapely-free: sample)
rng = np.random.default_rng(0); P = rng.random((200000, 2)); P = P[P[:, 1] <= np.sqrt(2) * np.minimum(P[:, 0], 1 - P[:, 0])]; P = P * np.array([R, 1]); P[:, 1] *= R / np.sqrt(2) / (R / np.sqrt(2)) * 1
pts = np.c_[rng.random(400000) * R, rng.random(400000) * R / np.sqrt(2)]; intri = pts[:, 1] <= np.sqrt(2) * np.minimum(pts[:, 0], R - pts[:, 0]); pts = pts[intri]
def inside(poly, X):
    ok = np.ones(len(X), bool)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]; ok &= (b[0] - a[0]) * (X[:, 1] - a[1]) - (b[1] - a[1]) * (X[:, 0] - a[0]) >= -1e-12
    return ok
tri_area = R * R / np.sqrt(2) / 2
out['area'] = dict(triangle=tri_area, minus_section=float(tri_area * (~inside(Suv, pts)).mean()), minus_shadow=float(tri_area * (~inside(Sh, pts)).mean()))
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', 'data', 'explore-face.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('pierce_in_triangle',)}, indent=1)); print('pierce in triangle:'); [print(p) for p in out['pierce_in_triangle']]
