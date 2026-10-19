# Export the Kepler–Poinsot–PiTet pieces (float, from the exact construction) for the paper's figures: role, corners, faces.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('cleo_pattern.py').read().split("def pattern")[0])
def faces(V):
    V = np.asarray(V); h = ConvexHull(V); out = []; seen = []
    for e in h.equations:
        if any(np.allclose(e, q, atol=1e-7) for q in seen): continue
        seen.append(e); idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]; P = V[idx]; c = P.mean(0)
        a = P[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); out.append([idx[i] for i in np.argsort(np.arctan2((P - c) @ b, (P - c) @ a))])
    return out
def kit(core, spk, hull, tag):
    n, d = planes(hull); out = [[f'{tag}spike', p.tolist(), faces(p)] for p in spk]
    for k in range(len(d)):
        P = np.vstack([hull[np.abs(hull @ n[k] - d[k]) < 1e-9], [core[np.argmax(core @ n[k])]]]); out.append([f'{tag}pyr', P.tolist(), faces(P)])
    e = min(np.linalg.norm(a - b) for a, b in itertools.combinations(core, 2))
    for i, j in itertools.combinations(range(len(core)), 2):
        if abs(np.linalg.norm(core[i] - core[j]) - e) > 1e-9: continue
        two = [s[-1] for s in spk if sum(np.min(np.linalg.norm(s[:-1] - core[x], axis=1)) < 1e-9 for x in (i, j)) == 2]
        if len(two) == 2: P = np.array([core[i], core[j], *two]); out.append([f'{tag}tet', P.tolist(), faces(P)])
    return out
core = [['core', I.tolist(), faces(I)]]
data = {'core': core, 'g': kit(I, GSD, D1, 'g'), 's': kit(D1, SSD, I2, 's'), 'phi3': float(PHI ** 3)}
open('kp-figs-data.js', 'w').write('export default ' + json.dumps(data, separators=(',', ':')) + ';\n'); print({k: len(v) for k, v in data.items() if k != 'phi3'})
