# DICTO · partial Vacuus sheet (26 Nov 2026): exact render scenes of the built-out Vacuus families. With Claude (Anthropic).
# Each scene: the excavated body (pit walls, pale, dark edges) and its core (the solid's polar dual scaled, see-through). Core colour:
# the app colour of the solid the core IS (icosahedron blue, dodecahedron violet, cube green, octahedron yellow, tetrahedron red);
# other cores neutral grey (rule: app colours only for the solid they stand for). Writes <out.html> + <out.json> (captions).
# Usage: python sheet_scenes.py <out.html>
import sys, os, json
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
os.environ.setdefault('SET', 'platonic+cubo')
import build_out_general as G
OUTH = sys.argv[1]
COL = {'icosahedron': '#3a70cd', 'dodecahedron': '#8a5cc4', 'cube': '#488e48', 'octahedron': '#e8c852', 'tetrahedron': '#cd3e28'}
CORE = {'dodecahedron': 'icosahedron', 'icosahedron': 'dodecahedron', 'cube': 'octahedron', 'octahedron': 'cube', 'tetrahedron': 'tetrahedron'}
G.SET = 'platonic+cubo'; base = {n: (V, F) for n, V, F in G.load()}
G.SET = 'mccooey'; mc = {n: (V, F) for n, V, F in G.load()}
d = json.load(open(os.path.join(HERE, '../data-build-out-mccooey.json')))
best = sorted([s for s in d['solids'] if s.get('t_as_solid_as_classics') is not None], key=lambda s: s['t_as_solid_as_classics'])
picks = [best[0]['name'], best[len(best) // 2]['name']]
rows = [('dodecahedron', [0.25, 5 - 2 * 5 ** .5, 0.85]), ('icosahedron', [0.25, 0.5, 3 * 5 ** .5 - 6]), ('cube', [0.25, 0.56, 0.85]),
        ('cuboctahedron', [0.25, 0.64, 0.85])] + [(p, [0.3, next(s for s in d['solids'] if s['name'] == p)['t_as_solid_as_classics'], 0.9]) for p in picks]
scenes, caps = [], []
for name, ts in rows:
    V, F = (base.get(name) or mc[name]); B = G.Body(V, F); R = np.abs(B.V).max()
    for t in ts:
        A = B.apex(t); verts, T, tubes = [], [], []
        for fi, f in enumerate(B.F):
            for a, b in zip(f, f[1:] + f[:1]):
                k = len(verts); verts += [B.V[a].tolist(), B.V[b].tolist(), A[fi].tolist()]; T.append([k, k + 1, k + 2])
                tubes += [[k, k + 1, '#2b261e', None], [k + 1, k + 2, '#5a5248', None], [k + 2, k, '#5a5248', None]]
        H = ConvexHull(A); ct = [[int(x) for x in s] for s in H.simplices]
        cc = COL.get(CORE.get(name, ''), '#9a9a9a')
        body = {'v': np.round(np.array(verts), 6).tolist(), 't': T, 'c': ['#e9e4da'] * len(T), 'a': 0.5, 'tubes': tubes, 'rad': 0.006 * R, 'balls': []}
        core = {'v': np.round(A, 6).tolist(), 't': ct, 'c': [cc] * len(ct), 'a': 0.95, 'tubes': [], 'rad': 0.004 * R, 'balls': []}
        scenes.append({'E': float(1.75 * R), 'dir': [0.55, 0.35, 1.0], 'parts': [body, core]})
        caps.append(dict(solid=name, t=float(t), wedge=round(B.wedge(t), 1), special=bool(abs(B.flat(t)) < 1e-6)))
R3.write(OUTH, scenes); json.dump(caps, open(OUTH.replace('.html', '.json'), 'w'), indent=1)
print('scenes', len(scenes), 'mccooey picks', picks); print('FINAL ok')
