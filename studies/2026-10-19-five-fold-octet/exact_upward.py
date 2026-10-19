# EXACT builds of the OG's upward family (DICTO 2026-10-19, names DICTO's): the UP step run outward from the exact OG of exact_inner.py
#   step 1 DICTO KRE   Kite-Rhombic Enneacontahedron
#   step 2 DICTO PHE   Pentagon-Hexagon Enneacontadihedron
#   step 3 DICTO TPP   Triangle-Pentagon Polyhedron
#   step 4 DICTO DPHP  Decagon-Pentagon-Hexagon Polyhedron
# In Q(sqrt5) with exact_cycle.step (corners proved exactly, faces closed, Euler). For each solid: exact face kinds (squared side
# lengths and corner count), exact volume, corner radii; and the four shells' pieces (one per face of the inner solid, the cone over
# it cut by the outer solid) with exact volumes, sum = gap, one symmetry orbit per kind (exact_shells.shell).
import itertools, json, os
from collections import Counter
import numpy as np
from exact_cycle import Q5, Fr, PHI, dot, step
from exact_shells import polytope, volume, solid, cross, sub, rotations, shell

HERE = os.path.dirname(os.path.abspath(__file__))
z, h = Q5(0), Q5(Fr(1, 2))
I = [v for a, b in ((h, PHI / 2),) for v in [(z, sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)] +
     [(sb * b, z, sa * a) for sa in (1, -1) for sb in (1, -1)] + [(sa * a, sb * b, z) for sa in (1, -1) for sb in (1, -1)]]
CI, FI = polytope(solid(I)); tri = [[CI[j] for j in o] for o, _ in FI]
cent = lambda P: tuple(sum((p[k] for p in P), Q5(0)) / len(P) for k in range(3))
ID = list({tuple(x + y for x, y in zip(p, q)) for t in tri for p, q in itertools.combinations(t, 2)})
CD, FD = polytope(solid(ID)); T3 = [[CD[j] for j in o] for o, _ in FD if len(o) == 3]
RT = step(ID)[0]
A5 = [v for v in RT if len([w for w in ID if (dot(v, w) - dot(w, w)).sign() == 0]) == 5]
X = list(dict.fromkeys(tuple(2 * cent(t)[k] - v[k] for k in range(3)) for t in T3 for v in t))
apex = []
for a5 in A5:
    cs = sorted(ID, key=lambda v: -dot(v, a5).f())[:5]; xs = sorted(X, key=lambda v: -dot(v, a5).f())[:5]; c0 = cs[0]
    x2 = sorted(xs, key=lambda v: sum((v[k] - c0[k]).f() ** 2 for k in range(3)))[:2]
    n = cross(sub(x2[0], c0), sub(x2[1], c0)); t_ = dot(n, c0) / dot(n, a5); apex.append(tuple(t_ * x for x in a5))
OG = ID + X + apex; assert len(set(OG)) == 102

# the group in this frame: the 60 rotations of exact_shells, conjugated by the coordinate swap that maps its frame onto this one
G0 = rotations(); IDs = set(ID)
app = lambda M, v: tuple(sum((M[i][k] * v[k] for k in range(3)), Q5(0)) for i in range(3))
G = None
for perm in itertools.permutations(range(3)):
    Pm = tuple(tuple(Q5(1 if perm[i] == j else 0) for j in range(3)) for i in range(3))
    Pt = tuple(tuple(Pm[j][i] for j in range(3)) for i in range(3))
    mul = lambda A, B: tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), Q5(0)) for j in range(3)) for i in range(3))
    cand = [mul(mul(Pm, g), Pt) for g in G0]
    if all({app(M, v) for v in ID} == IDs for M in cand[:6]): G = cand; break
assert G is not None and all({app(M, v) for v in OG} == set(OG) for M in G)

def kinds(S):
    C, F = polytope(solid(S)); out = Counter()
    for o, _ in F:
        P = [C[j] for j in o]; e = sorted((dot(sub(P[(i + 1) % len(P)], P[i]), sub(P[(i + 1) % len(P)], P[i])) for i in range(len(P))), key=lambda q: q.f())
        out[(len(P), tuple(repr(x) for x in e))] += 1
    return C, F, out

names = ['DICTO KRE', 'DICTO PHE', 'DICTO TPP', 'DICTO DPHP']
log = {'mark': 'DICTO OG upward family, exact builds, 2026-10-19', 'solids': {}, 'shells': []}
S = OG; chain = [OG]
for nm in names:
    S, nf, ne = step(S); chain.append(S)
    C, F, K = kinds(S); r2 = sorted({repr(dot(v, v)) for v in S}, key=lambda s: s)
    log['solids'][nm] = {'corners': len(S), 'faces': nf, 'edges': ne, 'face_kinds': [{'sides': k[0], 'count': c, 'squared_sides': list(k[1])} for k, c in K.items()],
                         'volume': repr(volume(C, F)), 'distinct_corner_radii': len(r2), 'symmetric_under_60_rotations': all({app(M, v) for v in S} == set(S) for M in G[:12])}
    print(nm, {k: v for k, v in log['solids'][nm].items() if k != 'face_kinds'}, [(k[0], c) for k, c in K.items()], flush=True)
for a, b, nm in zip(chain, chain[1:], ['OG -> KRE', 'KRE -> PHE', 'PHE -> TPP', 'TPP -> DPHP']):
    log['shells'].append(shell(a, b, G, nm))
json.dump(log, open(os.path.join(HERE, 'data', 'exact_upward.json'), 'w'), indent=1)
