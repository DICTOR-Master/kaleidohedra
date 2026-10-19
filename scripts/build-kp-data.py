# The DICTO Kepler–Poinsot–UP Cycle (DICTO 2026-10-19): data for its film world (src/app/kp-film-data.js). Built in float from the
# construction proved exactly in the research study studies/2026-10-19-kepler-poinsot-up (exact_kp.py): the icosahedron I of edge 1,
# the great stellated dodecahedron (spikes to 3x the face distance), its hull D1 (edge phi), the small stellated dodecahedron (spires to
# sqrt5 x the face distance), its hull I*phi^3; and each shell's pieces in the Cleo star's pattern (spikes, inward pyramids, valley
# tetrahedra). The build re-checks the fills by volume.
import itertools, json, os
import numpy as np
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'app', 'kp-film-data.js')
hv = lambda P: ConvexHull(np.asarray(P)).volume
def planes(V):
    q = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, w, atol=1e-7) for w in q): q.append(e)
    q = np.array(q); return q[:, :3], -q[:, 3]
def faces(V):
    V = np.asarray(V); n, d = planes(V); out = []
    for k in range(len(d)):
        idx = [i for i in range(len(V)) if abs(V[i] @ n[k] - d[k]) < 1e-7]; P = V[idx]; c = P.mean(0); a = P[0] - c; a /= np.linalg.norm(a); b = np.cross(n[k], a)
        out.append([idx[i] for i in np.argsort(np.arctan2((P - c) @ b, (P - c) @ a))])
    return out
solid = lambda V: {'v': np.round(np.asarray(V), 6).tolist(), 'f': faces(V)}
z = 0.0
I = np.array([v for a, b in ((0.5, PHI / 2),) for v in [(z, sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)] +
              [(sb * b, z, sa * a) for sa in (1, -1) for sb in (1, -1)] + [(sa * a, sb * b, z) for sa in (1, -1) for sb in (1, -1)]])
def spikes(core, f):
    n, d = planes(core); return [np.vstack([core[np.abs(core @ n[k] - d[k]) < 1e-9], [n[k] * d[k] * f]]) for k in range(len(d))]
def valleys(core, spk, hull):
    n, d = planes(hull); pyr = [np.vstack([hull[np.abs(hull @ n[k] - d[k]) < 1e-9], [core[np.argmax(core @ n[k])]]]) for k in range(len(d))]
    e = min(np.linalg.norm(a - b) for a, b in itertools.combinations(core, 2)); tets = []
    for i, j in itertools.combinations(range(len(core)), 2):
        if abs(np.linalg.norm(core[i] - core[j]) - e) > 1e-9: continue
        two = [s[-1] for s in spk if sum(np.min(np.linalg.norm(s[:-1] - core[x], axis=1)) < 1e-9 for x in (i, j)) == 2]
        if len(two) == 2: tets.append(np.array([core[i], core[j], *two]))
    return pyr, tets
GSD = spikes(I, 3.0); D1 = np.array([p[-1] for p in GSD]); SSD = spikes(D1, 5 ** .5); I2 = np.array([p[-1] for p in SSD])
assert np.max(np.linalg.norm(I2[:, None] - (I * PHI ** 3)[None], axis=2).min(1)) < 1e-9
gpyr, gtet = valleys(I, GSD, D1); spyr, stet = valleys(D1, SSD, I2)
assert abs(hv(I) + sum(map(hv, GSD + gpyr + gtet)) - hv(D1)) < 1e-9 and abs(hv(D1) + sum(map(hv, SSD + spyr + stet)) - hv(I2)) < 1e-9
data = {'K': PHI ** 3, 'radius': float(np.linalg.norm(I2, axis=1).max()),
        'stations': {'I': [solid(I)], 'GSD': [solid(I)] + [solid(p) for p in GSD], 'D1': [solid(D1)], 'SSD': [solid(D1)] + [solid(p) for p in SSD]},
        'pieces': {'D1': [dict(solid(p), kind='cap') for p in gpyr] + [dict(solid(p), kind='axe') for p in gtet],
                   'Ik': [dict(solid(p), kind='cleo') for p in spyr] + [dict(solid(p), kind='stet') for p in stet]},
        'view': {'dir': [0.45, 0.35, 1.0], 'up': [0.0, 1.0, 0.0]}}
with open(OUT, 'w') as f:
    f.write('// Built by scripts/build-kp-data.py (the DICTO Kepler–Poinsot–UP Cycle, DICTO 2026-10-19). Do not edit.\nexport default ' + json.dumps(data, separators=(',', ':')) + ';\n')
print('bytes', os.path.getsize(OUT))
