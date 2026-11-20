# DICTO · dictospheres.com — scenes for the figure "where CLEO, AXE and FUJI come from" (renders/pieces.html + labels).
# (a, b) the 63-piece build of [11]: the icosahedron of edge φ² = dodecahedron (edge 1) + 12 J11 + 30 AXE + 20 FUJI, put together
#        and pulled apart; corners from studies/2026-10-10-icosa-13/data/ico13-dodeca-j11-parts-unit.json (copied beside this
#        script as lotus-63.json), made exact in Q(√5). Checked exactly: every AXE and FUJI has the edges and angles of Table 2,
#        every J11 has unit edges, every corner lies in the big icosahedron, and the volumes add up to it. Overlap: the source
#        study checked it by separating axes; here a float sampling check besides.
# (c, d) inside the dodecahedron: the small icosahedron of edge g and the 20 CLEO standing on its faces, tips at the
#        dodecahedron's 20 corners; each CLEO checked exactly against Table 2.
import json, os
from fractions import Fraction as Fr
import numpy as np
import canon_solids as cs
from exact3d import Q5, R5, PHI, G, q, dot, sub, det3, from_vertices, perms3, signs, uniq
from render3d import solid_part, write, PX

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'renders')
COL = {'dodecahedron': '#8a5cc4', 'icosahedron': '#3a70cd', 'AXE': '#4dd0e1', 'FUJI': '#c792ea', 'CLEO': '#c792ea', 'J11': '#cfc6b4'}
log = []


def volume(S):
    p0 = S.V[0]; v = Q5()
    for n, d, o in S.F:
        if 0 in o: continue
        for a, b in zip(o[1:-1], o[2:]):
            t = det3([sub(S.V[o[0]], p0), sub(S.V[a], p0), sub(S.V[b], p0)]); v = v + (t if t.sign() > 0 else -t)
    return v / 6


D = json.load(open(os.path.join(HERE, 'lotus-63.json')))
parts = [(p['role'], from_vertices([tuple(cs.snap(x) for x in v) for v in p['vertices']])) for p in D['parts']]
from collections import Counter
assert Counter(r for r, _ in parts) == {'AXE': 30, 'FUJI': 20, 'J11': 12, 'dodecahedron': 1}
for r, S in parts:
    if r in ('AXE', 'FUJI'): assert S.classes() == cs.EXPECT[r], r
    if r == 'J11': assert len(S.V) == 11 and all(e[2] == 1 for e in S.E)
    if r == 'dodecahedron': assert len(S.F) == 12 and all(e[2] == 1 for e in S.E)
from scipy.spatial import ConvexHull
allv = uniq([v for _, S in parts for v in S.V]); hv = ConvexHull(np.array([[float(x) for x in v] for v in allv])).vertices
big = from_vertices([allv[i] for i in sorted(hv)])
assert len(big.V) == 12 and len(big.F) == 20 and len({e[2] for e in big.E}) == 1
e2 = big.E[0][2]; assert e2 == PHI * PHI * PHI * PHI, e2                                  # edge φ²
for _, S in parts:
    for v in S.V: assert all((dot(n, v) - d).sign() <= 0 for n, d, _ in big.F)
vs = sum((volume(S) for _, S in parts), Q5()); vb = volume(big)
assert vs == vb, (vs, vb)
log.append(f'63-piece build: 30 AXE and 20 FUJI as in Table 2, 12 J11 with unit edges, dodecahedron edge 1; all inside the icosahedron of edge φ²; volumes add up exactly ({vb})')
# float sampling: no point in two pieces
rng = np.random.default_rng(1); Pb = big.vf(); lo, hi = Pb.min(0), Pb.max(0); X = rng.uniform(lo, hi, (40000, 3))
cnt = np.zeros(len(X), int)
for _, S in parts:
    A = np.array([[float(x) for x in n] for n, d, o in S.F]); b = np.array([float(d) for n, d, o in S.F])
    cnt += np.all(X @ A.T < b - 1e-9, axis=1)
Ab = np.array([[float(x) for x in n] for n, d, o in big.F]); bb = np.array([float(d) for n, d, o in big.F]); inside = np.all(X @ Ab.T < bb - 1e-9, axis=1)
assert cnt.max() == 1, 'overlap'
log.append(f'sampling: {inside.sum()} random points inside, none in two pieces, {(inside & (cnt == 0)).sum()} in no piece (on cuts)')

# the small icosahedron of edge g: cyclic (0, ±1/2, ±g/2); the dodecahedron of the build; the 20 CLEO
dod = [S for r, S in parts if r == 'dodecahedron'][0]
small = from_vertices(uniq([w for v in signs(q(0, Fr(1, 2), G / 2)) for w in perms3(v)]))
assert len(small.V) == 12 and all(e[2] == G * G for e in small.E)
cleos = []
for c in dod.V:
    near = sorted(range(12), key=lambda i: -float(dot(small.V[i], c)))[:3]
    S = from_vertices([c] + [small.V[i] for i in near]); assert S.classes() == cs.EXPECT['CLEO']
    cleos.append(S)
faces_small = sorted(tuple(sorted(f[2])) for f in small.F)
bases = sorted(tuple(sorted(small.V.index(v) for v in S.V if v in small.V)) for S in cleos)
assert faces_small == bases                                                  # the 20 CLEO stand on the 20 faces
given = cs.word('CLEO'); assert any(set(given.V) == set(S.V) for S in cleos)   # the CLEO of [11] is one of them
log.append('20 CLEO: each as in Table 2, standing on the 20 faces of the small icosahedron of edge g, tips at the 20 corners of the dodecahedron')


def mv(S, k):
    P = S.vf(); c = P.mean(0); return P + c * k


DIR = (0.36, 0.58, 0.73); sc = []
ext = lambda k, Ss: max(np.linalg.norm(mv(S, k), axis=1).max() for S in Ss)
Ea = ext(0.4, [S for _, S in parts]) * 1.04
for k in (0.0, 0.4):
    pp = []
    for r, S in parts:
        if r == 'J11': pp.append(solid_part(S, COL[r], mv(S, k), alpha=0.32, rad=0.0035, edge_col='#5c5244'))
        else: pp.append(solid_part(S, COL[r], mv(S, k), rad=0.0035))
    sc.append({'E': Ea, 'dir': DIR, 'parts': pp})
Ec = ext(0.55, cleos) * 1.04
for k in (0.0, 0.55):
    pp = [solid_part(dod, COL['dodecahedron'], dod.vf(), alpha=0.22, rad=0.004, edge_col='#5c5244'),
          solid_part(small, COL['icosahedron'], small.vf(), rad=0.004)]
    for S in cleos: pp.append(solid_part(S, COL['CLEO'], mv(S, k), rad=0.004))
    sc.append({'E': Ec, 'dir': DIR, 'parts': pp})
write(os.path.join(OUT, 'pieces.html'), sc)
open(os.path.join(OUT, 'fig-pieces.log'), 'w').write('\n'.join(log) + '\n'); print('\n'.join(log)); print('scenes', len(sc)); print('FINAL ok')
