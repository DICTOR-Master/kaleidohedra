# DICTO · dictospheres.com — the first two figures of the Dehn packets paper in the 3D card style.
# (A) ring.html: the 540 degree ring of lead 1 round one edge: pyramid base 58.2825, TI pentagon-hexagon 142.6226, hexagon-hexagon 138.1897, 142.6226, 58.2825 deg,
#     each wedge a prism (the corner of the piece at the edge); the first turn solid, what lies beyond 360 degrees ghosted on top. Exact angles from alpha = atan(phi), beta = acos(1/sqrt6).
# (B) screen.html: 12 example centre pyramids of the screen of Proposition 6 (base face + the centre of the solid), 3 per class, built from the exact solids
#     (duals as polar reciprocals in the midsphere): each shot one pyramid.
import os, sys, itertools, json, math
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0], os.path.join(H, 'data', 'resin.json')]
import scenes as S
from render3d import write, solid_part
LOG = []
# ---------- A: ring ----------
phi = (1 + 5 ** .5) / 2; al = math.degrees(math.atan(phi)); be = math.degrees(math.acos(1 / 6 ** .5))
RING = [('pyramid base', al, '#7a50b4'), ('TI pentagon–hexagon', 135 - al + be, '#bdb8aa'), ('TI hexagon–hexagon', 270 - 2 * be, '#8b877c'),
        ('TI pentagon–hexagon', 135 - al + be, '#bdb8aa'), ('pyramid base', al, '#7a50b4')]
assert abs(sum(a for _, a, _ in RING) - 540) < 1e-9
GAP = 360 - sum(a for _, a, _ in RING[:3]); assert abs(GAP - (be - 45)) < 1e-9
def sector(d0, d1, r, h, n=None):
    n = n or max(2, int(math.ceil((d1 - d0) / 12))); pts = []
    for k in range(n + 1):
        t = math.radians(d0 + (d1 - d0) * k / n); pts += [[r * math.cos(t), r * math.sin(t), -h], [r * math.cos(t), r * math.sin(t), h]]
    pts += [[0, 0, -h], [0, 0, h]]; return S.hull(np.array(pts))
parts, ghosts, lab = [], [], []; cum = 0.0
for k, (nm, a, col) in enumerate(RING):
    d0, d1 = cum, cum + a; cum = d1
    if d0 < 360: parts.append(solid_part(sector(d0, min(d1, 360), 1.0, 0.34), col, rad=0.004, edge_col=S.EDGE))
    if d1 > 360: ghosts.append(solid_part(sector(max(d0, 360), d1, 1.08, 0.46), col, alpha=0.5, rad=0.005, edge_col='#d33a2c'))
    lab.append((k + 1, nm, a, ((d0 + d1) / 2) % 360 if (d0 + d1) / 2 < 360 or True else 0, d0, d1))
DIRA = np.array([0.25, -0.95, 0.78])
allp = parts + ghosts; E = float(max(abs(np.vstack([p['v'] for p in allp]) @ b).max() for b in list(__import__('render3d').basis(DIRA))[:2]) * 1.12)
write(os.path.join(S.OUT, 'ring.html'), [{'E': E, 'dir': DIRA.tolist(), 'parts': parts + ghosts}])
json.dump({'E': E, 'dir': DIRA.tolist(), 'wedges': [[k, nm, a, d0, d1] for k, nm, a, _, d0, d1 in lab], 'gap': GAP}, open(os.path.join(S.OUT, 'ring.json'), 'w'))
LOG.append(f'ring: wedges {[round(a, 4) for _, a, _ in RING]} sum 540; first three {sum(a for _, a, _ in RING[:3]):.4f}, gap to 360 = beta - 45 = {GAP:.4f}')
# ---------- B: example pyramids ----------
r5 = 5 ** .5
def perms(v): return {tuple(p) for p in itertools.permutations(v)}
def signs(v): return {tuple(s * x for s, x in zip(sg, v)) for sg in itertools.product((1, -1), repeat=3)}
def cyc(v): return {v, (v[1], v[2], v[0]), (v[2], v[0], v[1])}
def pts(*sets): return np.array(sorted({q for s_ in sets for q in s_}), float)
ico = pts(*[signs(c) for v in [(0, 1, phi)] for c in cyc(v)])
dod = pts(signs((1, 1, 1)), *[signs(c) for c in cyc((0, 1 / phi, phi))])
cube = pts(signs((1, 1, 1))); tet = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
octa = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], float)
cubo = pts(*[signs(c) for c in perms((1, 1, 0))])
ttet = pts(*[{tuple(s_ * x for s_, x in zip(sg, c)) for sg in itertools.product((1, -1), repeat=3) if sg[0] * sg[1] * sg[2] > 0} for c in perms((3, 1, 1))])
tc = pts(*[signs(c) for c in perms((2 ** .5 - 1, 1, 1))])
rcub = pts(*[signs(c) for c in perms((1, 1, 1 + 2 ** .5))])
idod = pts(*[signs(c) for c in cyc((0, 0, phi))], *[signs(c) for c in cyc((.5, phi / 2, phi * phi / 2))])
def faces_of(P):
    h = S.hull(P); return [(n, d, [P[i] if False else h.V[i] for i in o]) for n, d, o in h.F], h
def dual(P):
    F, h = faces_of(P); edges = {tuple(sorted(e)) for e in h.E}
    rm2 = np.mean([np.dot((h.V[a] + h.V[b]) / 2, (h.V[a] + h.V[b]) / 2) for a, b in edges])
    return np.array([rm2 * n / d for n, d, o in F])
def pyramid(P, sides, pick=0):
    F, h = faces_of(P); fs = [f for f in F if len(f[2]) == sides]; n, d, o = fs[pick]
    return S.hull(np.vstack([np.array(o), [[0, 0, 0]]]))
tt_ok = len(ttet) == 12
CASES = [('zero', 'cube', pyramid(cube, 4)), ('zero', 'rhombic dodecahedron', pyramid(dual(cubo), 4)), ('zero', 'rhombic triacontahedron', pyramid(dual(idod), 4)),
         ('one', 'tetrahedron', pyramid(tet, 3)), ('one', 'octahedron', pyramid(octa, 3)), ('one', 'dodecahedron', pyramid(dod, 5)),
         ('two', 'truncated tetrahedron', pyramid(ttet, 3)), ('two', 'rhombicuboctahedron', pyramid(rcub, 3)), ('two', 'icosidodecahedron', pyramid(idod, 3)),
         ('none', 'triakis tetrahedron', pyramid(dual(ttet), 3)), ('none', 'triakis octahedron', pyramid(dual(tc), 3)), ('none', 'deltoidal icositetrahedron', pyramid(dual(rcub), 4))]
assert tt_ok, len(ttet)
CC = {'zero': '#d6b46a', 'one': '#7f93a8', 'two': '#9c7448', 'none': '#c99e95'}
DIRB = np.array([0.36, 0.55, 1.0]); sc = []
for cl, nm, P in CASES:
    a, b, _ = __import__('render3d').basis(DIRB)
    # orient: the base's normal toward the viewer
    ctr = P.V.mean(0); base = max(P.F, key=lambda f: len(f[2]) if len(f[2]) > 3 else 0)
    c = [CC[cl]] * len(P.F)
    # rotate so that the apex (origin) is at the back: rotation taking the base normal to DIRB
    nb = [f for f in P.F if abs(f[1]) > 1e-9][0][0]   # the one face whose plane misses the centre = the base
    nb = nb / np.linalg.norm(nb); v = np.cross(nb, DIRB / np.linalg.norm(DIRB)); s_ = np.linalg.norm(v); cth = nb @ (DIRB / np.linalg.norm(DIRB))
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]); R = np.eye(3) + K + K @ K * ((1 - cth) / (s_ ** 2 + 1e-18)) if s_ > 1e-9 else np.eye(3)
    Pr = S.Solid(P.V - P.V.mean(0), P.F); tt = np.cross(nb, [0.31, 0.77, 0.55]); tt /= np.linalg.norm(tt)
    part = solid_part(Pr, c, rad=0.012, edge_col=S.EDGE)
    dv = nb * math.cos(math.radians(64)) + np.cross(nb, tt) * math.sin(math.radians(64)); sc.append({'E': S.ext([part], dv, 1.12), 'dir': dv.tolist(), 'parts': [part]})
write(os.path.join(S.OUT, 'screen.html'), sc); LOG.append('screen.html: 12 pyramids ' + ', '.join(n for _, n, _ in CASES))
open(os.path.join(H, 'scenes6.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
