# DICTO 2026-10-21: his older B1NR build (14 security rings: a 3-ring triangle domed at top and bottom, not turned, and a band of 6
# rings in pairs tip to tip with 3 square gaps; dome = triangle + 3 pentagons + 3 triangles; 23 faces). Rings = the 14 triangles,
# gaps = 6 pentagons + 3 squares; two rings meet tip to tip at each of 21 joints: the RECTIFIED J51 (triaugmented triangular prism;
# corners at J51's edge midpoints). With all edges equal the triangles and squares are flat but the pentagons cannot be: they bend.
# DICTO: "just bend it" (no ring simulation). So: flat triangles and squares, each pentagon a smooth bent surface spanning its five
# straight edges (mean-value interpolation from a flat regular pentagon: exact straight edges, smooth inside).
import os, json, itertools, numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
h = np.sqrt(3) / 3; tri = [np.array([np.cos(a), np.sin(a), 0]) * h for a in np.radians([90, 210, 330])]
J = [t + [0, 0, .5] for t in tri] + [t + [0, 0, -.5] for t in tri]
for i in range(3):
    m = (tri[i] + tri[(i + 1) % 3]) / 2; J.append(m + m / np.linalg.norm(m) * np.sqrt(.5))   # square-pyramid caps, edge 1
J = np.array(J); E = sorted({(min(i, j), max(i, j)) for s in ConvexHull(J).simplices for i, j in itertools.combinations(s, 2)
                             if abs(np.linalg.norm(J[i] - J[j]) - 1) < 1e-6})
assert len(J) == 9 and len(E) == 21
V = np.array([(J[i] + J[j]) / 2 for i, j in E]) * 2          # rectified, scaled to edge 1
def ring(idx, axis):                                          # cyclic order of points round an axis
    c = V[idx].mean(0); a = axis / np.linalg.norm(axis); u = np.cross(a, [0.3, 0.5, 0.8]); u /= np.linalg.norm(u); w = np.cross(a, u)
    return [idx[k] for k in np.argsort([np.arctan2((V[i] - c) @ w, (V[i] - c) @ u) for i in idx])]
faces = []                                                    # (kind, ordered corner list)
for v in range(9):                                            # vertex figures of J51: squares (degree 4), pentagons (degree 5)
    idx = [k for k, (i, j) in enumerate(E) if v in (i, j)]; faces.append(('sq' if len(idx) == 4 else 'pent', ring(idx, J[v])))
for s in ConvexHull(J).simplices:                             # J51's 14 triangles, shrunk = the 14 rings
    idx = [k for k, (i, j) in enumerate(E) if i in s and j in s]; n = np.cross(*(J[s[1:]] - J[s[0]])); n = n if n @ J[s].mean(0) > 0 else -n
    faces.append(('tri', ring(idx, n)))
cnt = {k: sum(1 for f in faces if f[0] == k) for k in ('tri', 'sq', 'pent')}
edges = sorted({tuple(sorted((f[1][a], f[1][(a + 1) % len(f[1])]))) for f in faces for a in range(len(f[1]))})
L = [np.linalg.norm(V[a] - V[b]) for a, b in edges]
print('faces', cnt, 'total', len(faces), '| corners', len(V), 'edges', len(edges), '| edge lengths', round(min(L), 6), round(max(L), 6))
for k in ('sq', 'pent'):
    f = next(f for f in faces if f[0] == k); Q = V[f[1]]; s = np.linalg.svd(Q - Q.mean(0))[1]
    print(k, 'out of plane (rms, edge 1):', round(float(s[-1] / np.sqrt(len(Q))), 4))
def mvc(p, P):                                                # mean-value coordinates of 2D point p in polygon P
    d = P - p; r = np.linalg.norm(d, axis=1)
    if r.min() < 1e-12: w = (r < 1e-12).astype(float); return w / w.sum()
    ang = [np.arctan2(d[i][0] * d[(i + 1) % len(P)][1] - d[i][1] * d[(i + 1) % len(P)][0], d[i] @ d[(i + 1) % len(P)]) for i in range(len(P))]
    w = np.array([(np.tan(ang[i - 1] / 2) + np.tan(ang[i] / 2)) / r[i] for i in range(len(P))]); return w / w.sum()
def bent(ids, n=10):                                          # triangulated bent pentagon: rings of points in a flat pentagon, mapped
    P2 = np.array([[np.cos(2 * np.pi * k / 5), np.sin(2 * np.pi * k / 5)] for k in range(5)]); pts = [np.zeros(2)]; tris = []
    for r in range(1, n + 1):
        for k in range(5):
            for s in range(r): pts.append((P2[k] * (r - s) + P2[(k + 1) % 5] * s) / n)
    pts = np.array(pts); edge = [False] + [r == n for r in range(1, n + 1) for _ in range(5 * r)]
    idx = lambda r, i: 0 if r == 0 else 1 + 5 * r * (r - 1) // 2 + i % (5 * r)
    for r in range(1, n + 1):
        for k in range(5):
            for s in range(r):
                a, b = idx(r, k * r + s), idx(r, k * r + s + 1); c = idx(r - 1, k * (r - 1) + s) if r > 1 else 0; tris.append((a, b, c))
                if s < r - 1: tris.append((b, idx(r - 1, k * (r - 1) + s + 1), c))
    def onedge(p):                                            # boundary: straight edges, by linear interpolation
        k = int(np.floor((np.arctan2(p[1], p[0]) % (2 * np.pi)) / (2 * np.pi / 5) + 1e-9)) % 5
        t = np.linalg.norm(p - P2[k]) / np.linalg.norm(P2[(k + 1) % 5] - P2[k]); return V[ids[k]] * (1 - t) + V[ids[(k + 1) % 5]] * t
    X = np.array([onedge(p) if e else mvc(p, P2) @ V[ids] for p, e in zip(pts, edge)]); return X, tris
GOLD, PURPLE, LILAC = '#d9a441', '#6b3fa0', '#9a78c8'          # #18 standard: gold rings (triangles), purple bends, lilac squares
def solid(rot=None):
    v, t, c = [], [], []
    for kind, ids in faces:
        if kind == 'pent': X, T = bent(ids)
        else: X, T = V[ids], [(0, a, a + 1) for a in range(1, len(ids) - 1)]
        o = len(v); v += X.tolist(); t += [[o + a, o + b, o + cc] for a, b, cc in T]; c += [{'tri': GOLD, 'sq': LILAC, 'pent': PURPLE}[kind]] * len(T)
    v = np.array(v); v = v if rot is None else v @ rot.T
    ev = (V if rot is None else V @ rot.T)
    o = len(v); v = np.vstack([v, ev])
    return {'v': np.round(v, 5).tolist(), 't': t, 'c': c, 'e': [[o + a, o + b] for a, b in edges], 'a': 1.0}
Rx = lambda d: np.array([[1, 0, 0], [0, np.cos(np.radians(d)), -np.sin(np.radians(d))], [0, np.sin(np.radians(d)), np.cos(np.radians(d))]])
Rz = lambda d: np.array([[np.cos(np.radians(d)), -np.sin(np.radians(d)), 0], [np.sin(np.radians(d)), np.cos(np.radians(d)), 0], [0, 0, 1]])
scenes = [{'title': 'The dome', 'sub': 'ring triangle on top, 3 bent pentagons, 3 triangles', 'parts': [solid(Rx(-62))]},
          {'title': 'The band', 'sub': 'rings tip to tip, a square gap', 'parts': [solid(Rz(30))]},
          {'title': 'Turned', 'sub': '14 triangles, 3 squares, 6 bent pentagons', 'parts': [solid(Rx(-25) @ Rz(5))]}]
for s in scenes:
    pts = np.array(s['parts'][0]['v']); ctr = (pts.max(0) + pts.min(0)) / 2; s['parts'][0]['v'] = (pts - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True); os.makedirs(os.path.join(HERE, 'figures'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'b1nr.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'b1nr-labels.json'), 'w'), indent=1)
print('b1nr.html', len(scenes))
