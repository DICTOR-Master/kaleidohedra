# DICTO · dictospheres.com — 3D scenes of C2 (name to come): truncated dodecahedron, edge 1, with a regular icosahedron centre pyramid
# on each of its 20 triangles, built exactly as tree/branch-D-resin/scripts/c2.py builds it (here in floats, checks against the exact
# values); and C2 in its tightest mould (fcc, rhombic dodecahedron at s = 5 + 2 sqrt5) with the central division R1 of data/c2.json
# (4 kinds, moved by T_h). Checks printed, then FINAL ok.
import json, os, sys, itertools
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0], os.path.join(H, 'data', 'resin.json')]
import scenes as S
from render3d import write
PHI = S.PHI; LOG = []
BLUE = '#3a70cd'                                    # icosahedron colour (element-colours.md): the pyramids are icosahedron centre pyramids
TV = []
for b in [(0, PHI - 1, 2 + PHI), (PHI - 1, PHI, 2 * PHI), (PHI, 2, PHI + 1)]:
    for sg in itertools.product((1, -1), repeat=3):
        t = [b[i] * sg[i] * PHI / 2 for i in range(3)]
        for c in ([t[0], t[1], t[2]], [t[2], t[0], t[1]], [t[1], t[2], t[0]]):
            if not any(np.allclose(c, q) for q in TV): TV.append(c)
TV = np.array(TV); assert len(TV) == 60
TD = S.hull(TV)
decs = [f for f in TD.F if len(f[2]) == 10]; tris = [f for f in TD.F if len(f[2]) == 3]
assert len(decs) == 12 and len(tris) == 20
assert all(abs(np.linalg.norm(TV[o[i]] - TV[o[(i + 1) % len(o)]]) - 1) < 1e-12 for n, d, o in TD.F for i in range(len(o)))
Rico = (PHI + 2) ** .5 / 2; hico = PHI ** 2 / (2 * 3 ** .5)  # icosahedron (edge 1) circumradius and inradius
apex = []
for n, d, o in tris:
    A = TV[o].mean(0) + hico * n
    for i in o: assert abs(np.linalg.norm(A - TV[i]) - Rico) < 1e-12
    apex.append(A)
pyr = [S.hull(np.vstack([TV[o], A])) for (n, d, o), A in zip(tris, apex)]
vC2 = S.volume(TD) + sum(S.volume(p) for p in pyr)
assert abs(vC2 - (42.5 + 20 * 5 ** .5)) < 1e-9
LOG.append(f'C2: truncated dodecahedron edge 1 (all 90 edges = 1) + 20 pyramids, lateral edges = icosahedron circumradius; vol {vC2:.10f} = 85/2 + 20 sqrt5')
V2 = np.vstack([TV, apex]); F2 = [(n, d, list(o)) for n, d, o in decs]
for p, (n, d, o) in enumerate(tris):
    for i in range(3):
        tri = [o[i], o[(i + 1) % 3], 60 + p]; m = np.cross(V2[tri[1]] - V2[tri[0]], V2[tri[2]] - V2[tri[0]]); m /= np.linalg.norm(m)
        if m @ V2[tri[0]] < 0: tri = tri[::-1]; m = -m
        F2.append((m, m @ V2[tri[0]], tri))
C2 = S.Solid(V2, F2)
PEARL, EDGE = S.PEARL, S.EDGE


def c2_parts(t, rad=0.005):
    return [S.solid_part(TD, PEARL, rad=rad, edge_col=EDGE)] + [S.solid_part(S.moved(P, t * n), BLUE, rad=rad, edge_col=EDGE) for (n, d, o), P in zip(tris, pyr)]


DIR = np.array([0.36, 0.30, 1.0])
sc = [{'E': S.ext(c2_parts(0.9), DIR), 'dir': DIR.tolist(), 'parts': c2_parts(0)}]
p = c2_parts(0.9); sc.append({'E': S.ext(p, DIR), 'dir': DIR.tolist(), 'parts': p})
write(os.path.join(S.OUT, 'c2.html'), sc); LOG.append('c2.html: whole; pyramids pulled out by 0.9 along their 3-fold axes')

# cell: fcc at s = 5 + 2 sqrt5, R1
D = json.load(open(os.path.join(H, 'data', 'c2.json')))
A = [a for a in D['arrangements'] if a['lattice'] == 'fcc'][0]; assert A['valid'] and A['s'] == '5+2r5'
s = 5 + 2 * 5 ** .5
mould = S.hull([v for i in range(3) for g in (1, -1) for v in [np.eye(3)[i] * g * s / 2]] + [np.array(g) * s / 4 for g in itertools.product((1, -1), repeat=3)])
assert len(mould.F) == 12
pieces = []
for kn, kd in enumerate(A['kinds'], 1):
    base = np.array(kd['verts']); seen = []
    for g in S.TH:
        Y = S.act(g, base); key = tuple(sorted(map(tuple, np.round(Y, 6) + 0.0)))
        if key not in seen: seen.append(key); pieces.append((kn, S.hull(Y)))
    assert len(seen) == kd['orbit']
vm = S.volume(mould); vp = sum(S.volume(P) for _, P in pieces)
assert len(pieces) == 72 and abs(vm - s ** 3 / 4) < 1e-9 and abs(vp - (vm - vC2)) < 1e-8
for _, P in pieces: assert all((P.V @ n - d).max() < 1e-7 for n, d, o in mould.F)
LOG.append(f'fcc s = 5 + 2 sqrt5 = {s:.9f}: mould vol {vm:.9f}; 72 pieces (kinds 12, 24, 24, 12), sum vol {vp:.9f} = mould - C2 {vm - vC2:.9f}; all inside the mould')


def c2_whole(rad):
    return S.solid_part(C2, [PEARL if len(o) == 10 else BLUE for n, d, o in C2.F], rad=rad, edge_col=EDGE)


f = 0.85
parts = [c2_whole(0.0028)] + [S.solid_part(S.moved(P, f * P.V.mean(0)), S.KIND[kn - 1], rad=0.0022, edge_col=EDGE) for kn, P in pieces]
shell = S.Solid(mould.V * (1 + f), [(n, d * (1 + f), o) for n, d, o in mould.F])
parts.append(S.solid_part(shell, S.GLASS, alpha=0.16, rad=0.0018, edge_col=S.LIGHT, faces=S.back(shell, DIR)))
E = S.ext(parts, DIR, 1.04)
together = [c2_whole(0.0028)] + [S.solid_part(P, S.KIND[kn - 1], rad=0.0022, edge_col=EDGE) for kn, P in pieces]
write(os.path.join(S.OUT, 'c2cell.html'), [{'E': E, 'dir': DIR.tolist(), 'parts': together}, {'E': E, 'dir': DIR.tolist(), 'parts': parts}])
LOG.append('c2cell.html: together; pulled apart (f = 0.85, mould far side see-through at (1+f) x)')
open(os.path.join(H, 'scenes3.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
