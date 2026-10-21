# DICTO 2026-10-21, "what could Aristotle have meant" (paper #44): render scenes (float copies of the exact solids of
# pyramid_checks.py) into renders/aristotle.html with the family.html viewer of 2026-10-19-five-fold-octet; shots with
# jewel-shots.mjs, compose with aristotle_compose.py. (1) the five face pyramids, each in its solid (glass); (2) the octet's
# 60-degree rhombohedron = tetrahedron + octahedron + tetrahedron, whole and cut into its 16 face pyramids, drawn apart;
# (3) the prolate golden rhombohedron = Cleo-Icos + Antonius + Cleo-Icos (#20), whole and drawn apart.
import os, json, itertools, numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); phi = (1 + 5 ** .5) / 2
GOLD, PURPLE, LILAC, CREAM = '#d9a441', '#6b3fa0', '#9a78c8', '#efe4cc'
cyc = lambda v: [np.roll(v, k) for k in range(3)]
S = {'Cube': list(itertools.product((1, -1), repeat=3)),
     'Tetrahedron': [p for p in itertools.product((1, -1), repeat=3) if np.prod(p) > 0],
     'Octahedron': [s * e for e in np.eye(3) for s in (1, -1)],
     'Dodecahedron': list(itertools.product((1, -1), repeat=3)) + [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(np.array([0, a / phi, b * phi]))],
     'Icosahedron': [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(np.array([0, a, b * phi]))]}
# the viewer's camera (family.html): direction, screen right and up
def rot(v, axis, a):
    axis = np.array(axis, float); return v * np.cos(a) + np.cross(axis, v) * np.sin(a) + axis * (axis @ v) * (1 - np.cos(a))
cd = rot(rot(np.array([0, 0.525731, 0.850651]), [1, 0, 0], 0.30), [0, 1, 0], 0.22); cd /= np.linalg.norm(cd)
cx = np.cross([0, 1, 0], cd); cx /= np.linalg.norm(cx); cy = np.cross(cd, cx)
def part(P, col, a=1.0):
    P = np.array(P, float); h = ConvexHull(P); T = []
    c = P.mean(0)
    for s in h.simplices:                                           # outward winding
        t = list(s)
        if np.cross(P[t[1]] - P[t[0]], P[t[2]] - P[t[0]]) @ (P[t[0]] - c) < 0: t = [t[0], t[2], t[1]]
        T.append(t)
    return {'v': np.round(P, 6).tolist(), 't': [list(map(int, t)) for t in T], 'c': [col] * len(T), 'e': None, 'a': a}
def faces(P):
    P = np.array(P, float); h = ConvexHull(P); F = {}
    for s, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 6)), set()).update(s)
    return [(np.array(eq[:3]), [P[i] for i in sorted(f)]) for eq, f in F.items()]
scenes = []
# (1) the five face pyramids
ANG = {'Cube': '45° and 120°', 'Tetrahedron': '35.26° and 120°', 'Octahedron': '54.74° and 90°', 'Dodecahedron': '58.28° and 120°', 'Icosahedron': '69.09° and 72°'}
for name, P in S.items():
    P = np.array(P, float); P /= np.linalg.norm(P[0])
    n, f = faces(P)[0]
    n0 = -0.93 * cy - 0.37 * cd; n0 /= np.linalg.norm(n0)              # turn the solid so this face is at the bottom, seen a little from above
    k = np.cross(n, n0); sn, cs = np.linalg.norm(k), n @ n0; k = k / sn
    Rm = lambda x: rot(np.asarray(x, float), k, np.arctan2(sn, cs))
    P = np.array([Rm(q) for q in P]); f = [Rm(q) for q in f]
    sc = {'title': f'{name} pyramid' if name != 'Icosahedron' else 'Icosahedron pyramid (Cleo-Icos)', 'sub': 'base and side edges ' + ANG[name],
          'parts': [part(list(f) + [np.zeros(3)], GOLD), part(P, LILAC, 0.12)]}
    scenes.append(sc)
# helpers for the rhombohedra: put the long axis along the screen's x, pieces drawn apart along it
def frame(a, b):
    a = a / np.linalg.norm(a); b = b - (b @ a) * a; b /= np.linalg.norm(b); c = np.cross(a, b)
    M = np.stack([cx, cy, cd], 1) @ np.stack([a, b, c], 0)
    Rt = np.stack([rot(rot(e, cx, 0.55), cy, 0.30) for e in np.eye(3)], 1)   # tilt: about the screen's x, then its y
    return lambda X: np.asarray(X) @ (Rt @ M).T
def rhombo(u, v, w):
    R = {p: p[0] * u + p[1] * v + p[2] * w for p in itertools.product((0, 1), repeat=3)}
    return ([R[p] for p in R if sum(p) <= 1], [R[p] for p in R if sum(p) in (1, 2)], [R[p] for p in R if sum(p) >= 2])
def pyramids(P):
    c = np.mean(P, 0); return [(list(f) + [c], n) for n, f in faces(P)]
# (2) the octet's 60-degree rhombohedron
u, v, w = np.array([1., 1, 0]), np.array([1., 0, 1]), np.array([0., 1, 1])
T1, M, T2 = rhombo(u, v, w); L = u + v + w; F = frame(L, u - v); c0 = L / 2
X = lambda P, s=0: F(np.array(P) - c0 + s * L / np.linalg.norm(L))
scenes.append({'title': 'The octet\'s rhombohedron', 'sub': 'tetrahedron + octahedron + tetrahedron', 'E': 1.85,
               'parts': [part(X(T1), GOLD), part(X(M), PURPLE), part(X(T2), GOLD)]})
pp = []
for P, col, s in [(T1, GOLD, -2.3), (M, PURPLE, 0.0), (T2, GOLD, 2.3)]:
    for Q, n in pyramids(np.array(P)): pp.append(part(X(np.array(Q) + 0.22 * n, s), col))
scenes.append({'title': 'Cut into face pyramids', 'sub': '8 octahedron + 2 × 4 tetrahedron pyramids, drawn apart', 'E': 2.55, 'parts': pp})
# (3) the prolate golden rhombohedron from the icosahedron's centre-to-corner lines of one face
I = np.array(S['Icosahedron'], float); n, f = faces(I)[0]; u, v, w = f
C1, A, C2 = rhombo(u, v, w); L = u + v + w; F = frame(L, u - v); c0 = L / 2
X = lambda P, s=0: F(np.array(P) - c0 + s * L / np.linalg.norm(L))
scenes.append({'title': 'The prolate golden rhombohedron', 'sub': 'Cleo-Icos + Antonius + Cleo-Icos (#20)', 'E': 2.3,
               'parts': [part(X(C1), GOLD), part(X(A), PURPLE), part(X(C2), GOLD)]})
scenes.append({'title': 'Drawn apart', 'sub': 'two Cleo-Icos (gold) and Antonius (purple)', 'E': 2.9,
               'parts': [part(X(C1, -0.55), GOLD), part(X(A), PURPLE), part(X(C2, 0.55), GOLD)]})
for sc in scenes:                                                  # frame each scene to fit (orthographic camera)
    Q = np.vstack([np.array(p['v']) for p in sc['parts']]); sc['E'] = round(float(np.abs(np.stack([Q @ cx, Q @ cy])).max()) * 1.06, 4)
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
open(os.path.join(HERE, 'renders', 'aristotle.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'aristotle-labels.json'), 'w'), indent=1, ensure_ascii=False)
print('aristotle.html', len(scenes))
