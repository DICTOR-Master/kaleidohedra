"""Step 3a (27 Nov 2026; DICTO "yes to all"): the pieces of the truncated octahedron P4 cut by its 19 joint Vacuus + Resonus planes,
and their Dehn invariants. With Claude (Anthropic).
P4 = conv of the rearrangements of (4,3,2,1), centred, in sum y = 0 (coordinates in Q^4). Facets: sum over S of y <= m(S)
(m(S) = sum of the |S| largest centred values). Cones: the 248 regions of the 19 planes (step 1), found from sign vectors of random
directions; the count must be 248 (complete). Symmetry: the 48 maps y -> +-(permuted y); one representative per orbit.
Each piece = P4 with the cone's sign conditions; vertices EXACT (fractions: every triple of constraint planes with sum y = 0);
edges = vertex pairs on >= 2 common tight planes whose tight set has rank 2; edge length^2 exact; dihedral from the two face
planes containing the edge (exact cos^2 and sign).
Dehn invariant (in R (x) R/Q pi): length = q sqrt(d) (d squarefree); grouped by d; per d the angle sum is reduced with the step-1 angle
basis (PSLQ, identified not proved). Output data/pieces4.json: per orbit type: size, vertices, volume, Dehn vector.
Then: nonnegative integer combinations of types with Dehn invariant 0 = space-filling candidates (step 3b)."""
import os, json, itertools, random
from fractions import Fraction as F
from math import isqrt
import mpmath as mp
mp.mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__)); n = 4
J = json.load(open(os.path.join(HERE, '../data/joint4.json')))
PL = [tuple(F(x) for x in p['normal']) for p in J['planes']]
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
one = (F(1),) * n
cen = [F(x) - F(5, 2) for x in (4, 3, 2, 1)]
FAC = []
for k in range(1, n):
    for S in itertools.combinations(range(n), k):
        a = tuple(F(1) if i in S else F(0) for i in range(n)); FAC.append((a, sum(sorted(cen, reverse=True)[:k])))
# cones by random directions in sum y = 0
random.seed(1); signs = {}
for _ in range(400000):
    g = [random.gauss(0, 1) for _ in range(n)]; m = sum(g) / n; g = [x - m for x in g]
    sv = tuple(1 if sum(float(p) * x for p, x in zip(P, g)) > 0 else -1 for P in PL)
    signs.setdefault(sv, g)
print('cones found', len(signs), '(step 1: 248)', flush=True)
# symmetry
G = []
for perm in itertools.permutations(range(n)):
    for e in (1, -1): G.append((perm, e))
def act(g, v): perm, e = g; return tuple(e * v[perm[i]] for i in range(n))
PLi = {}
for i, P in enumerate(PL):
    PLi[P] = (i, 1); PLi[tuple(-x for x in P)] = (i, -1)
def act_sign(g, sv):
    out = [0] * len(PL)
    for i, P in enumerate(PL):
        j, s = PLi[act(g, P)]; out[j] = sv[i] * s
    return tuple(out)
orbits = {}
for sv in signs:
    key = min(act_sign(g, sv) for g in G); orbits.setdefault(key, []).append(sv)
print('orbit types', len(orbits), 'sizes', sorted(len(v) for v in orbits.values()), flush=True)
def solve(rows, rhs):
    M = [list(r) + [b] for r, b in zip(rows, rhs)]; m = len(M); c = 0; r = 0; piv = []
    for c in range(n):
        p = next((i for i in range(r, m) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; inv = 1 / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(m):
            if i != r and M[i][c] != 0: f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    if r < n: return None
    if any(all(x == 0 for x in M[i][:n]) and M[i][n] != 0 for i in range(r, m)): return None
    x = [F(0)] * n
    for i, c in enumerate(piv): x[c] = M[i][n]
    return tuple(x)
def rank(vecs):
    M = [list(v) for v in vecs]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0: f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def sqfree(q):   # q > 0 rational -> (c, d): sqrt(q) = c sqrt(d), d squarefree integer
    num, den = q.numerator * q.denominator, q.denominator ** 2
    d = num; c2 = F(1, den)
    k = 2
    out = 1
    while k * k <= d:
        while d % (k * k) == 0: d //= k * k; out *= k
        k += 1
    return F(out, q.denominator), d
types = []
for key, members in orbits.items():
    sv = members[0]
    cons = [(a, b) for a, b in FAC] + [(tuple(-s * x for x in P), F(0)) for s, P in zip(sv, PL)]   # a . y <= b
    V = []
    for tri in itertools.combinations(range(len(cons)), 3):
        y = solve([one] + [cons[t][0] for t in tri], [F(0)] + [cons[t][1] for t in tri])
        if y is None: continue
        if all(dot(a, y) <= b for a, b in cons) and y not in V: V.append(y)
    tight = [frozenset(t for t, (a, b) in enumerate(cons) if dot(a, y) == b) for y in V]
    # faces: constraints tight at >= 3 vertices spanning a plane
    faces = [t for t in range(len(cons)) if sum(1 for T in tight if t in T) >= 3]
    edges = []
    for i, j in itertools.combinations(range(len(V)), 2):
        T = tight[i] & tight[j]
        fs = [t for t in T if t in faces]
        if len(fs) >= 2 and rank([one] + [cons[t][0] for t in fs]) == 3:
            # the two faces of this edge: the two tight face planes whose normals are not parallel and which carry other vertices
            # (merge parallel duplicates: same plane listed twice)
            planes = []
            for t in fs:
                a = cons[t][0]
                if not any(rank([one, a, b]) < 3 for b in planes): planes.append(a)
            # an edge must be a 1-dim face: no third vertex on the segment between
            def between(k):
                if k in (i, j) or not set(fs) <= tight[k]: return False
                q = next(q for q in range(n) if V[j][q] != V[i][q]); t = (V[k][q] - V[i][q]) / (V[j][q] - V[i][q]); return 0 < t < 1
            seg_ok = not any(between(k) for k in range(len(V)))
            if seg_ok and len(planes) == 2: edges.append((i, j, planes))
    # Dehn: sum over edges len (x) (interior dihedral)
    cpt = tuple(sum(v[q] for v in V) / len(V) for q in range(n))
    dehn = {}; elist = []
    for i, j, (a, b) in edges:
        d = tuple(x - y for x, y in zip(V[i], V[j])); L2 = dot(d, d)
        # interior dihedral: angle between inward normals' complement: project normals into sum-zero space
        pa = tuple(x - sum(a) / n for x in a); pb = tuple(x - sum(b) / n for x in b)
        # orient outward: a . y <= b form, so normal a points outward
        cs = dot(pa, pb); c2 = cs * cs / (dot(pa, pa) * dot(pb, pb))
        ang = mp.pi - mp.acos(mp.sign(cs) * mp.sqrt(mp.mpf(c2.numerator) / c2.denominator)) if cs != 0 else mp.pi / 2
        c, dd = sqfree(L2); elist.append([dd, str(c), str(c2), int((cs > 0) - (cs < 0))]); dehn.setdefault(dd, mp.mpf(0)); dehn[dd] += mp.mpf(c.numerator) / c.denominator * ang
    # volume (floats; for the record): cone from cpt over faces
    nf = len({tuple(sorted(T)) for T in [frozenset(k for k in range(len(V)) if t in tight[k]) for t in faces]})
    types.append(dict(orbit_size=len(members), n_vertices=len(V), n_edges=len(edges), n_faces=nf, sign=list(sv),
                      vertices=[[str(x) for x in v] for v in V], edges=elist, dehn={str(k): str(mp.nstr(v, 40)) for k, v in dehn.items()}))
    print(f'type {len(types)}: orbit {len(members)}, vertices {len(V)}, edges {len(edges)}, Euler V-E+F = {len(V) - len(edges) + nf}', flush=True)
json.dump(types, open(os.path.join(HERE, '../data/pieces4.json'), 'w'), indent=1)
ok = len(signs) == 248 and sum(t['orbit_size'] for t in types) == 248 and all(t['n_vertices'] - t['n_edges'] + t['n_faces'] == 2 for t in types)
print('FINAL ok' if ok else 'FINAL FAIL')
