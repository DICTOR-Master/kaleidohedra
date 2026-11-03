"""Shared exact tools for the 6D study (2026-11-03-6d-golden-cubes). Builds on cubes_lib.py (copied unchanged from
studies/2026-11-03-golden-cuts-beyond-plato): exact field K = Q(sqrt2, sqrt5).
3D hulls: floats propose the facets, every facet is then verified exactly (cubes_lib.faces_exact on (x, y, z, 0)).
"""
import itertools, json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data'); sys.path.insert(0, HERE)
from cubes_lib import *          # noqa

E4 = (ZERO, ZERO, ZERO, ONE)
CHECKS = []


def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)
    return ok


def dump(fname, out):
    out['checks'] = CHECKS; out['all_pass'] = all(c['pass'] for c in CHECKS)
    with open(os.path.join(DATA, fname), 'w') as f: json.dump(out, f, indent=1, default=str)
    print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks pass -> data/{fname}')


def d2(u, w): return dot(vsub(u, w), vsub(u, w))
def in_q5(x): return x.v[1] == 0 and x.v[3] == 0          # no sqrt2, sqrt10 part
def in_q(x): return x.v[1] == x.v[2] == x.v[3] == 0


def uniq(P):
    seen = {}; [seen.setdefault(key(p), p) for p in P]; return list(seen.values())


def hull3(P):
    """exact facets of conv(P), P points in K^3; returns (corner list, facets as index lists into the corner list)"""
    P = uniq(P)
    P4 = [tuple(p) + (ZERO,) for p in P]
    F = faces_exact(P4, E4)
    used = sorted({i for f in F for i in f})
    idx = {i: k for k, i in enumerate(used)}
    return [P[i] for i in used], [[idx[i] for i in f] for f in F]


def solve3(A, b):
    """exact solution of the 3x3 system A x = b (Cramer), or None if singular"""
    D = det3(*A)
    if D.iszero(): return None
    out = []
    for k in range(3):
        M = [list(r) for r in A]
        for r in range(3): M[r][k] = b[r]
        out.append(det3(*M) / D)
    return tuple(out)


def vertices_H(H):
    """vertices of {x : n.x <= r for (n, r) in H}, exact, by all triples of planes"""
    V = {}
    for (n1, r1), (n2, r2), (n3, r3) in itertools.combinations(H, 3):
        x = solve3([n1, n2, n3], [r1, r2, r3])
        if x is None: continue
        if all(dot(n, x) <= r for n, r in H): V.setdefault(key(x), x)
    return list(V.values())


def signed_perms(n):
    for p in itertools.permutations(range(n)):
        for s in itertools.product((1, -1), repeat=n):
            yield p, s


def act(g, v):
    """signed permutation g = (p, s): (g v)_p[i] = s[i] v_i"""
    p, s = g; out = [None] * len(v)
    for i in range(len(v)): out[p[i]] = v[i] * s[i]
    return tuple(out)


# ------------------------------------------------------------------ Platonic solids (D, I, C, T, O order) and cuts
def platonic():
    ip = PHI.inv()
    cyc = lambda a, b, c: [(a, b, c), (c, a, b), (b, c, a)]
    ico = uniq([v for s1 in (1, -1) for s2 in (1, -1) for v in cyc(ZERO, K(s1), PHI * s2)])
    dod = [tuple(K(s) for s in ss) for ss in itertools.product((1, -1), repeat=3)]
    dod += uniq([v for s1 in (1, -1) for s2 in (1, -1) for v in cyc(ZERO, ip * s1, PHI * s2)])
    cube = [tuple(K(s) for s in ss) for ss in itertools.product((1, -1), repeat=3)]
    tet = [tuple(K(s) for s in ss) for ss in itertools.product((1, -1), repeat=3) if ss[0] * ss[1] * ss[2] == 1]
    octa = [tuple(K(s) if j == i else ZERO for j in range(3)) for i in range(3) for s in (1, -1)]
    return {'dodecahedron': (dod, 5), 'icosahedron': (ico, 3), 'cube': (cube, 4), 'tetrahedron': (tet, 3),
            'octahedron': (octa, 3)}


C_N = {3: ONE, 4: S2, 5: PHI}
def x_golden(n): c = C_N[n]; return PHI / (c + 2 * PHI), ONE / (PHI * c + 2)


def cut_solid(V, x):
    """cut every corner at fraction x of each edge (edges = shortest distances)"""
    m = min(d2(a, b) for a, b in itertools.combinations(V, 2))
    out = []
    for a, b in itertools.combinations(V, 2):
        if d2(a, b) == m:
            out.append(vadd(a, vscale(x, vsub(b, a)))); out.append(vadd(b, vscale(x, vsub(a, b))))
    return uniq(out)


def dist_ratios(P):
    """all squared distances divided by the smallest one"""
    D = [d2(a, b) for a, b in itertools.combinations(P, 2)]
    m = min(D); return uniq_k([d / m for d in D])


def uniq_k(L):
    seen = {}; [seen.setdefault(x.v, x) for x in L]; return list(seen.values())


def fs(x): return f'{kstr(x)} (~{float(x):.6f})'
