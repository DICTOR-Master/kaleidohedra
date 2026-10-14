# Checks for the DICTO Truncated-Icosahedral Hecatodihedron (DICTO, 2026-10-14, discovery #28): from Polyhedraverse's shape
# TRANS_DHARMA_80 (Spheres of Dharma stage 7). Faces by kind, corners, insphere, dihedral angles, volume, the 20 three-fold corners
# as a dodecahedron, and the truncated icosahedron inside. Writes tih-checks.json. DICTO · dictospheres.com
import json, math, sys, itertools
import numpy as np
from scipy.spatial import ConvexHull
s = json.load(open(sys.argv[1]))['TRANS_DHARMA_80']; V = np.array(s['v'], float); V -= V.mean(0)
h = ConvexHull(V)
planes = []
for e in h.equations:                      # group hull facets into faces (corners are stored to 6 decimals)
    if not any(np.abs(e - q).max() < 1e-4 for q in planes): planes.append(e)
faces = []
for e in planes:
    on = np.where(np.abs(V @ e[:3] + e[3]) < 1e-4)[0]; c = V[on].mean(0); a = V[on[0]] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
    o = on[np.argsort(np.arctan2((V[on] - c) @ b, (V[on] - c) @ a))]; faces.append((e, o))
kinds = {}
for e, o in faces:
    L = [np.linalg.norm(V[o[k]] - V[o[(k + 1) % len(o)]]) for k in range(len(o))]
    A = [math.degrees(math.acos(np.clip((V[o[k - 1]] - V[o[k]]) @ (V[o[(k + 1) % len(o)]] - V[o[k]]) / np.linalg.norm(V[o[k - 1]] - V[o[k]]) / np.linalg.norm(V[o[(k + 1) % len(o)]] - V[o[k]]), -1, 1))) for k in range(len(o))]
    key = (len(o), tuple(sorted(set(round(x, 4) for x in L))), tuple(sorted(set(round(x, 2) for x in A))), round(float(-e[3]), 4))
    kinds[key] = kinds.get(key, 0) + 1
dist = sorted(set(round(float(-e[3]), 4) for e, _ in faces))
radii = sorted(set(round(float(np.linalg.norm(v)), 5) for v in V))
corners = len(V); edges = len(set(tuple(sorted((int(o[k]), int(o[(k + 1) % len(o)])))) for _, o in faces for k in range(len(o))))
dih = sorted(set(round(math.degrees(math.pi - math.acos(np.clip(a[0][:3] @ b[0][:3], -1, 1))), 2) for a, b in itertools.combinations(faces, 2) if len(set(a[1]) & set(b[1])) == 2))
r_out = max(np.linalg.norm(V, axis=1)); far = V[np.abs(np.linalg.norm(V, axis=1) - r_out) < 1e-5]
dod = None
if len(far) == 20:
    d = np.linalg.norm(far[:, None] - far[None], axis=2); e = np.sort(d[d > 1e-6])[0]; dod = dict(count=20, edge=round(float(e), 6), neighbours_each=sorted(set(int((np.abs(row - e) < 1e-5).sum()) for row in d)))
inner = V[np.abs(np.linalg.norm(V, axis=1) - r_out) > 1e-5]
out = dict(faces=len(faces), corners=corners, edges=edges, euler=corners - edges + len(faces),
           face_kinds={f'{k[0]}-gon, sides {[float(x) for x in k[1]]}, angles {[float(x) for x in k[2]]}, distance {k[3]}': n for k, n in kinds.items()},
           face_plane_distances=dist, corner_radii=radii, dihedral_angles=dih, volume=round(h.volume, 6), surface=round(h.area, 6),
           outer_corners_dodecahedron=dod, inner_corners=len(inner), inner_corner_radius=sorted(set(round(float(np.linalg.norm(v)), 5) for v in inner)))
json.dump(out, open('tih-checks.json', 'w'), indent=1); print(json.dumps(out, indent=1))
