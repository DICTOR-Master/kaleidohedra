# DICTO 2026-10-21: "turn the inside towers out and start a new sequence" -> flip the 80 Aktis of the OG core outward: each Aktis
# (pyramid from the centre over one OG face) is mirrored in its own face, so its tip lands at the centre's mirror image in that face
# plane (2 x the face's foot point). New first solid = hull of the OG and the 80 tips. Then the same rule again: each face of the solid
# gets the outward-flipped pyramid (tip = mirror of the centre in that face), next solid = hull. Float exploration: per beat the
# corners, faces, face kinds, radii, volume and growth, to see whether a Fibonacci build (1,1,2,3,5 beats) gets tall and stays clean.
import os, json, numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
V = np.array(json.load(open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'ocd-vertices.json'))), float)
def faces(P, tol=1e-7):
    H = ConvexHull(P); out = []
    for eq in H.equations:
        if not any(np.allclose(eq, e, atol=1e-6) for e in out): out.append(eq)
    F = []
    for e in out:
        ids = np.where(np.abs(P @ e[:3] + e[3]) < 1e-6)[0]; F.append((e[:3], -e[3], ids))
    return H, F
def flip(P):
    H, F = faces(P); tips = np.array([2 * d * n for n, d, _ in F])
    Q = np.vstack([P, tips]); H2 = ConvexHull(Q); keep = np.unique(H2.vertices); return Q[keep], H.volume, F
P = V; log = []
for beat in range(0, 9):
    H, F = faces(P); kinds = {}
    for n, d, ids in F: kinds[len(ids)] = kinds.get(len(ids), 0) + 1
    r = np.linalg.norm(P, axis=1); dist = sorted({round(d, 3) for _, d, _ in F})
    row = dict(beat=beat, corners=len(P), faces=len(F), kinds=dict(sorted(kinds.items())), r_min=round(r.min(), 4), r_max=round(r.max(), 4),
               face_dist=dist[:6], volume=round(H.volume, 4), out_of_round=round(r.max() / r.min() - 1, 4))
    print(row, flush=True); log.append(row)
    if len(P) > 6000: break
    P, _, _ = flip(P)
json.dump(log, open(os.path.join(HERE, 'flip-float.json'), 'w'), indent=1)
