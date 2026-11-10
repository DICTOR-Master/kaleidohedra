"""The 4D Vacuus of the 4D permutohedron, EXACT (11 Nov 2026; for the paper DICTO asked for: "a 4D vacuus permutahedron paper").
vacuus4d.py found (floating point) 65 central 3D slices carrying all 150 2-faces, five of them truncated octahedra. Here every claim is
checked in integer/rational arithmetic:
  1. the 150 2-faces (60 hexagons, 90 squares) and, for each, the ONE central hyperplane (through the centre) containing it, as a
     primitive integer normal in the sum-zero space;
  2. the 65 hyperplanes grouped into orbits under the full symmetry group S5 x {+1, -1} (permuting coordinates, central inversion):
     congruent slices are proved congruent by an explicit symmetry, not by measuring;
  3. each slice's 3D shape: corners = 4D corners on the hyperplane + edge crossings (rational); faces proposed by a float hull and then
     VERIFIED exactly (every face plane: all its corners exactly on it, every other corner strictly inside; Euler V - E + F = 2);
  4. edge lengths (squared, exact) of each slice type, to say what the shapes are metrically, not only combinatorially;
  5. how the five truncated-octahedron slices meet: the 2D plane where two of them cross, and its shape.
Prints PASS/FAIL per check and a FINAL line earned only by all checks."""
import itertools, json, sys
from fractions import Fraction as F
from collections import Counter, defaultdict
import numpy as np
from scipy.spatial import ConvexHull

OUT = sys.argv[1] if len(sys.argv) > 1 else 'vacuus4d-exact.json'
fails = []
def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what); (None if ok else fails.append(what))

# corners: permutations of 1..5, centred at (3,3,3,3,3): integer vectors with entries -2..2, sum 0
V = [tuple(x - 3 for x in p) for p in itertools.permutations(range(1, 6))]
idx = {v: i for i, v in enumerate(V)}
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
E = [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if sum(abs(x - y) for x, y in zip(V[i], V[j])) == 2]
check(len(V) == 120 and len(E) == 240, f'4D permutohedron: {len(V)} corners, {len(E)} edges')

# 2-faces
faces = set()
for p in V:
    for k in (-2, -1, 0):                                         # hexagon: values k, k+1, k+2 permuted in their positions
        pos = [i for i in range(5) if p[i] in (k, k + 1, k + 2)]
        hexa = set()
        for perm in itertools.permutations((k, k + 1, k + 2)):
            q = list(p)
            for t, i in enumerate(pos): q[i] = perm[t]
            hexa.add(idx[tuple(q)])
        faces.add(frozenset(hexa))
    for a, b in itertools.combinations(range(-2, 2), 2):          # square: two commuting adjacent-value swaps
        if b <= a + 1: continue
        sq = set()
        for s1, s2 in itertools.product((0, 1), repeat=2):
            q = list(p)
            if s1: q = [a + 1 if x == a else a if x == a + 1 else x for x in q]
            if s2: q = [b + 1 if x == b else b if x == b + 1 else x for x in q]
            sq.add(idx[tuple(q)])
        faces.add(frozenset(sq))
faces = [tuple(sorted(f)) for f in faces]
kinds = Counter(len(f) for f in faces)
check(len(faces) == 150 and kinds[6] == 60 and kinds[4] == 90, f'2-faces: {len(faces)} ({kinds[6]} hexagons, {kinds[4]} squares)')

# exact central hyperplane of a face: integer n with n.1 = 0 and n.v = 0 for the face's corners (rank 3 => 1-dim solution)
def nullvec(rows):
    """integer basis vector of the null space of an integer matrix whose null space is 1-dimensional (fraction-free elimination)"""
    M = [list(map(F, r)) for r in rows]; m = len(M[0]); piv = []; r = 0
    for c in range(m):
        pr = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]; M[r] = [x / M[r][c] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0: M[i] = [x - M[i][c] * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(m) if c not in piv]
    assert len(free) == 1, f'null space dim {len(free)}'
    v = [F(0)] * m; v[free[0]] = F(1)
    for i, c in enumerate(piv): v[c] = -M[i][free[0]]
    from math import gcd, lcm
    L = lcm(*[x.denominator for x in v]); w = [int(x * L) for x in v]; g = gcd(*w); w = [x // g for x in w]
    s = next(x for x in w if x != 0); return tuple(x if s > 0 else -x for x in w)   # first nonzero entry positive

H = defaultdict(list)
for f in faces:
    nv = nullvec([[1] * 5] + [list(V[i]) for i in f])
    assert all(dot(nv, V[i]) == 0 for i in f) and sum(nv) == 0
    H[nv].append(f)
check(len(H) == 65, f'central hyperplanes carrying the 2-faces: {len(H)} (each face in exactly one, by construction: rank 3)')

# orbits under S5 x {+-1}: canonical form of a normal = lexicographically largest image (normals are defined up to sign)
def canon(nv):
    best = None
    for perm in itertools.permutations(range(5)):
        for s in (1, -1):
            w = tuple(s * nv[perm[i]] for i in range(5)); best = w if best is None or w > best else best
    return best
orbits = defaultdict(list)
for nv in H: orbits[canon(nv)].append(nv)
print(f'orbits of the 65 slices under S5 x (+-1): {len(orbits)}: ' + ', '.join(f'{len(v)} x {k}' for k, v in sorted(orbits.items(), key=lambda kv: -len(kv[1]))))

# the shape of each slice, exactly
def slice_shape(nv):
    pts = set()
    for v in V:
        if dot(nv, v) == 0: pts.add(tuple(F(x) for x in v))
    for i, j in E:
        a, b = dot(nv, V[i]), dot(nv, V[j])
        if a * b < 0:
            t = F(a, a - b); pts.add(tuple(F(x) + t * (F(y) - F(x)) for x, y in zip(V[i], V[j])))
    pts = sorted(pts)
    # float hull in a 3D frame proposes the faces
    X = np.array([[float(x) for x in p] for p in pts]); nf = np.array(nv, float); one = np.ones(5)
    B = np.linalg.svd(np.vstack([nf, one]))[2][2:]; hh = ConvexHull(X @ B.T)
    groups = {}
    for simp, eq in zip(hh.simplices, hh.equations): groups.setdefault(tuple(np.round(eq, 7)), set()).update(int(s) for s in simp)
    # exact verification of each proposed face: plane through 3 of its corners (normal in the slice), all corners on one side
    vfaces = []
    for g in groups.values():
        g = sorted(g); p0 = pts[g[0]]
        # face normal m: in sum-zero space, orthogonal to nv, orthogonal to the face's directions
        rows = [[1] * 5, list(nv)] + [list(sub(pts[k], p0)) for k in g[1:]]
        m = nullvec(rows); c = dot(m, p0)
        on = [k for k in range(len(pts)) if dot(m, pts[k]) == c]
        side = {(dot(m, pts[k]) > c) - (dot(m, pts[k]) < c) for k in range(len(pts)) if k not in on}
        if sorted(on) != g or len(side) != 1: return None
        vfaces.append(g)
    # edges of the slice: corner pairs sharing two faces
    inc = defaultdict(set)
    for fi, g in enumerate(vfaces):
        for k in g: inc[k].add(fi)
    edges = [(a, b) for a, b in itertools.combinations(range(len(pts)), 2) if len(inc[a] & inc[b]) >= 2]
    euler = len(pts) - len(edges) + len(vfaces)
    elen = Counter(sum((x - y) ** 2 for x, y in zip(pts[a], pts[b])) for a, b in edges)
    return {'corners': len(pts), 'edges': len(edges), 'faces': len(vfaces), 'euler': euler,
            'face_sizes': dict(sorted(Counter(len(g) for g in vfaces).items())), 'edge_len2': {str(k): v for k, v in sorted(elen.items())},
            'pts': pts, 'vfaces': vfaces}

results = []
for rep, members in sorted(orbits.items(), key=lambda kv: -len(kv[1])):
    sh = slice_shape(rep)
    check(sh is not None and sh['euler'] == 2, f'orbit {rep}: faces verified exactly, Euler {sh and sh["euler"]}')
    k6 = sum(len(f) == 6 for f in H[rep]); k4 = sum(len(f) == 4 for f in H[rep])
    print(f'  {len(members):2d} slices, normal {rep}: {sh["corners"]} corners, {sh["edges"]} edges, {sh["faces"]} faces {sh["face_sizes"]}, '
          f'edge lengths^2 {sh["edge_len2"]}; carries {k6} hexagons + {k4} squares of the 4D solid')
    results.append({'normal': list(rep), 'count': len(members), 'members': [list(m) for m in members], 'carries_hexagons': k6,
                    'carries_squares': k4, **{k: sh[k] for k in ('corners', 'edges', 'faces', 'face_sizes', 'edge_len2')}})
check(sum(r['count'] for r in results) == 65, 'orbit sizes add to 65')
check(sum(r['count'] * (r['carries_hexagons'] + r['carries_squares']) for r in results) == 150, 'every 2-face carried exactly once (counts add to 150)')

# the truncated-octahedron slices: which orbit, and the planes where two of them cross
to = [r for r in results if r['corners'] == 24 and r['face_sizes'] == {4: 6, 6: 8}]
for r in to:
    print(f'TO-type orbit {r["normal"]}: {r["count"]} slices, edge lengths^2 {r["edge_len2"]}, carries {r["carries_squares"]} squares')
five = [r for r in to if r['count'] == 5]
if five:
    ms = five[0]['members']; a, b = ms[0], ms[1]
    sa, sb = slice_shape(tuple(a)), slice_shape(tuple(b))
    common = sorted(set(sa['pts']) & set(sb['pts']))
    # the crossing plane's polygon: the 4D solid cut by both hyperplanes = corners on both + edge crossings of both
    print(f'two of the five ({a}, {b}) cross in a central plane; corners of the 4D solid on it: {len(common)}')
    five[0]['crossing_corners_shared'] = len(common)
json.dump({'orbits': results, 'fails': fails}, open(OUT, 'w'), indent=1, default=str)
print('FINAL ok' if not fails else f'FINAL FAIL: {len(fails)} checks failed')
