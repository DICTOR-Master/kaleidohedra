# DICTO · partial Vacuus 1b: exact render scenes of the twelve special depths (26 Nov 2026). With Claude (Anthropic).
# Per depth: the excavated body (see-through) and its core, the solid bounded by ALL the pit-wall planes (scipy halfspace
# intersection about O); at a special depth this core is the scaled core solid Q (checked: its face count = Q's).
# Usage: python special_scenes.py <out.html>
import sys, os, json
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); OUTH = sys.argv[1]; sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.join(HERE, '../../2026-11-21-scutoid-stand-in/renders/scripts'))
import render3d as R3
exec(open(os.path.join(HERE, 'special_depths_all.py')).read().split('found = []')[0])
EX = json.load(open(os.path.join(HERE, '../data-exact-forms.json')))
COL = {'icosahedron': '#3a70cd', 'dodecahedron': '#8a5cc4', 'cube': '#488e48', 'octahedron': '#e8c852', 'tetrahedron': '#cd3e28'}
POLY = {p['name']: p for p in json.load(open(os.path.join(HERE, '../../2026-11-25-tacitus/data/polyhedra.json')))}
scenes, caps = [], []
for e in EX:
    V, F, N, D = S[e['P']]; s = e['s']; A = s * D[:, None] * N
    verts, T, tubes, H = [], [], [], []
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]):
            k = len(verts); verts += [V[a].tolist(), V[b].tolist(), A[fi].tolist()]; T.append([k, k + 1, k + 2])
            tubes += [[k, k + 1, '#2b261e', None], [k + 1, k + 2, '#5a5248', None], [k + 2, k, '#5a5248', None]]
            n = np.cross(V[b] - V[a], A[fi] - V[a]); n /= np.linalg.norm(n); d = n @ V[a]
            if d < 0: n, d = -n, -d
            H.append(list(n) + [-d])
    hs = HalfspaceIntersection(np.array(H), np.zeros(3)); C = ConvexHull(hs.intersections)
    nf = len({tuple(np.round(eq, 6)) for eq in C.equations}); nq = len(POLY[e['Q']]['faces'])
    R = np.abs(V).max()
    body = {'v': np.round(np.array(verts), 6).tolist(), 't': T, 'c': ['#e9e4da'] * len(T), 'a': 0.45, 'tubes': tubes, 'rad': 0.006 * R, 'balls': []}
    core = {'v': np.round(C.points, 6).tolist(), 't': [[int(x) for x in sm] for sm in C.simplices], 'c': [COL.get(e['Q'], '#9a9a9a')] * len(C.simplices), 'a': 0.95, 'tubes': [], 'rad': 0.004 * R, 'balls': []}
    scenes.append({'E': float(1.75 * R), 'dir': [0.55, 0.35, 1.0], 'parts': [body, core]})
    caps.append(dict(P=e['P'], Q=e['Q'], s=e['closed'], core_faces=nf, Q_faces=nq))
    print(e['P'], 'on', e['Q'], 's =', e['closed'], 'core faces', nf, 'Q faces', nq, 'OK' if nf == nq else 'MISMATCH', flush=True)
R3.write(OUTH, scenes); json.dump(caps, open(OUTH.replace('.html', '.json'), 'w'), indent=1)
print('FINAL ok' if all(c['core_faces'] == c['Q_faces'] for c in caps) else 'FINAL FAIL (core is not Q)')
