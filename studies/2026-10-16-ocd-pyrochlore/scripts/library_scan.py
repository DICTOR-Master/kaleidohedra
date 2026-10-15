# Step 12 (DICTO: "these aren't our only tiles"). Scan every convex piece in the studies' data for adapter candidates.
# Each distinct shape (up to scale) is turned into the icosahedral frame (searching rotations that send two face normals to
# frame directions at the same angle) and every face is classified: perpendicular to a 5-, 3- or 2-fold axis, lying in an OCD
# kite plane (the 60 kite-normal directions), or none. Flags: hexagon adapter = a 3-fold face + golden-rhombus (2-fold) faces;
# kite adapter = a kite-plane face + golden-rhombus faces.
import json, glob, itertools, sys, os, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, '../_lib'); import geomcheck as gc
O = np.array(json.load(open('data/network.json'))['ocd']); r = np.linalg.norm(O, axis=1)
ax = gc.icosa_axes(O[np.abs(r - r.max()) < 1e-9])
pl = []
for e in ConvexHull(O).equations:
    if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
kite = np.array([e[:3] / np.linalg.norm(e[:3]) for e in pl if sum(np.abs(O @ e[:3] + e[3]) < 1e-7) == 4])
DIRS = {'5': np.vstack([ax['5'], -ax['5']]), '3': np.vstack([ax['3'], -ax['3']]), '2': np.vstack([ax['2'], -ax['2']]), 'kite': kite}
ALL = np.vstack(list(DIRS.values()))
def pieces_in(x, d=0):
    if isinstance(x, list) and len(x) >= 4 and all(isinstance(v, list) and len(v) == 3 and all(isinstance(c, (int, float)) for c in v) for v in x):
        yield np.array(x, float); return
    if d > 5: return
    if isinstance(x, dict):
        for v in x.values(): yield from pieces_in(v, d + 1)
    elif isinstance(x, list):
        for v in x: yield from pieces_in(v, d + 1)
def normals(P):
    try: h = ConvexHull(P)
    except Exception: return None
    out = []
    for e in h.equations:
        if not any(np.allclose(e[:3], q, atol=1e-6) for q in out): out.append(e[:3])
    return np.array(out)
def signature(P, N):
    E = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(P, 2)); m = max(E)
    return (len(P), len(N), tuple(np.round(np.array(E) / m, 4)))
def classify(N):
    best = None
    pairs = [(i, j) for i, j in itertools.combinations(range(len(N)), 2) if abs(abs(N[i] @ N[j]) - 1) > 1e-6][:1]   # two faces that are not parallel
    for i, j in pairs:
        a = N[i] @ N[j]
        for u in ALL:
            for w in ALL:
                if abs(u @ w - a) > 1e-6: continue
                A = np.array([N[i], N[j], np.cross(N[i], N[j])]).T; B = np.array([u, w, np.cross(u, w)]).T
                R = B @ np.linalg.inv(A)
                if not np.allclose(R @ R.T, np.eye(3), atol=1e-6) or np.linalg.det(R) < 0: continue
                labs = []
                for n in N:
                    m = R @ n; lab = next((k for k, D in DIRS.items() if np.max(D @ m) > 1 - 1e-6), '-'); labs.append(lab)
                sc = sum(l != '-' for l in labs)
                if best is None or sc > best[0]: best = (sc, labs)
    return best[1] if best else ['-'] * len(N)
seen = {}
files = [f for f in glob.glob('../*/data/*.json') + glob.glob('../*/scripts/*.json') if not f.endswith('-raw.json')]
for f in files:
    try: J = json.load(open(f))
    except Exception: continue
    n = 0
    for P in pieces_in(J):
        n += 1
        if n > 4000: break
        P = np.unique(np.round(P, 9), axis=0)
        if len(P) < 4: continue
        N = normals(P)
        if N is None or len(N) < 4: continue
        N = N / np.linalg.norm(N, axis=1)[:, None]
        s = signature(P, N)
        if s in seen: seen[s]['count'] += 1; continue
        seen[s] = {'count': 1, 'file': f, 'labs': classify(N), 'faces': len(N), 'corners': len(P)}
hexa = [v for v in seen.values() if '3' in v['labs'] and '2' in v['labs']]
kit = [v for v in seen.values() if 'kite' in v['labs'] and '2' in v['labs']]
out = [f'scanned {len(files)} files: {len(seen)} distinct convex shapes (up to scale)',
       f'hexagon adapters (a three-fold face and golden-rhombus faces): {len(hexa)}',
       *[f'   {v["corners"]} corners, {v["faces"]} faces {sorted(v["labs"])}; seen {v["count"]}x; first in {v["file"]}' for v in sorted(hexa, key=lambda v: -v['labs'].count('2'))[:15]],
       f'kite adapters (a kite-plane face and golden-rhombus faces): {len(kit)}',
       *[f'   {v["corners"]} corners, {v["faces"]} faces {sorted(v["labs"])}; seen {v["count"]}x; first in {v["file"]}' for v in kit[:15]]]
print('\n'.join(out)); open('data/library-scan.txt', 'w').write('\n'.join(out) + '\n')
