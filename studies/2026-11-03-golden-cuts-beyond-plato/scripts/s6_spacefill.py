"""Step 6 (light, positive checks only; house rule: no negative fill tests).
Cutting every cell of a face-to-face tiling at the same distance along every edge (per corner kind) turns each tiling
corner into a hole bounded by the corner polygons of the cells round it; cut cells + holes fill space. We check that
the hole is the stated solid by volume: (number of cells at the corner) x (corner pyramid volume) = volume of the hole.
 (1) tetrahedra + octahedra (fcc): 8 tetrahedron and 6 octahedron corners -> cuboctahedron of edge x;
     the Greater (Lesser) Golden Cut Tetrahedron has the same x as Icosaxes (Unborn Axes).
 (2) cubes: 8 cube corners -> octahedron of edge sqrt2 x (the Greater/Lesser Golden Cut Cube + octahedra).
 (3) rhombic dodecahedra: 6 sharp corners -> cube of edge a, 4 blunt corners -> regular tetrahedron of edge a.
 (4) truncated octahedra (bcc): 4 corners -> tetragonal disphenoid with faces (sqrt2 x, sqrt3 x, sqrt3 x).
usage: python s6_spacefill.py -> ../data/s6-spacefill.json
"""
import json, os, itertools
import numpy as np
import gcb
G = gcb.g
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True); assert ok, name


def corner_pyramid(V, F, v, y):
    """Volume of the cap cut from corner v at distance y[v] along its edges (apex v, base the corner polygon)."""
    nb = sorted({w for f in F for i, w in enumerate(f) if f[i - 1] == v or f[(i + 1) % len(f)] == v} - {v})
    nb = [w for w in nb if any((f[i - 1] == v and f[i] == w) or (f[i] == v and f[i - 1] == w) for f in F for i in range(len(f)))]
    P = np.array([V[v] + y[v] * (V[w] - V[v]) / np.linalg.norm(V[w] - V[v]) for w in nb])
    from scipy.spatial import ConvexHull
    return ConvexHull(np.vstack([P, V[v]])).volume


def cm_volume(d):   # Cayley-Menger volume of a tetrahedron from its 6 squared edge lengths d[(i,j)]
    M = np.ones((5, 5)); M[0, 0] = 0
    for i in range(4):
        for j in range(4):
            M[i + 1, j + 1] = 0 if i == j else d[(min(i, j), max(i, j))]
    return np.sqrt(np.linalg.det(M) / 288)


out = []
xs = {'greater': lambda k: G / (k + 2 * G), 'lesser': lambda k: 1 / (G * k + 2)}
for lab, xf in xs.items():
    x = xf(1.0)
    T = gcb.platonic('tetrahedron'); FT = gcb.faces(T); O = gcb.platonic('octahedron'); FO = gcb.faces(O)
    capT = corner_pyramid(T, FT, 0, [x] * 4); capO = corner_pyramid(O, FO, 0, [x] * 6)
    co = 5 * 2 ** .5 / 3 * x ** 3
    check(f'(1) {lab}: 8 tetrahedron caps + 6 octahedron caps = cuboctahedron of edge x={x:.6f} ({8 * capT + 6 * capO:.12f} vs {co:.12f})', abs(8 * capT + 6 * capO - co) < 1e-12)
    out.append({'fill': f'{lab} golden cut tetrahedra + {"Icosaxes" if lab == "greater" else "Unborn Axes"} + cuboctahedra (edge x)', 'x': x,
                'per_lattice_point': '2 tetrahedra, 1 octahedron, 1 cuboctahedron'})
    xc = xf(2 ** .5)
    C = gcb.platonic('cube'); FC = gcb.faces(C); capC = corner_pyramid(C, FC, 0, [xc] * 8)
    oc = 2 ** .5 / 3 * (2 ** .5 * xc) ** 3
    check(f'(2) {lab}: 8 cube caps = octahedron of edge sqrt2 x ({8 * capC:.12f} vs {oc:.12f})', abs(8 * capC - oc) < 1e-12)
    out.append({'fill': f'{lab} golden cut cubes + octahedra (edge sqrt2 x)', 'x': xc, 'per_lattice_point': '1 cube, 1 octahedron'})
rh = json.load(open(os.path.join(DATA, 's2b-rhombic.json')))['rhombic']['rhombic dodecahedron']
V, F, orb = gcb.catalan('cuboctahedron'); L = np.linalg.norm(V[F[0][0]] - V[F[0][1]]); V = V / L
for c in rh['cuts']:
    a = c['a_decimal']; y = [c['y_sharp_decimal'] if o.startswith('4') else c['y_blunt_decimal'] for o in orb]
    vs = next(i for i, o in enumerate(orb) if o.startswith('4')); vb = next(i for i, o in enumerate(orb) if o.startswith('3'))
    cs, cb = corner_pyramid(V, F, vs, y), corner_pyramid(V, F, vb, y)
    check(f'(3) rhombic dodecahedron {c["cut"]}: 6 sharp caps = cube a^3 ({6 * cs:.12f} vs {a ** 3:.12f}); 4 blunt caps = regular tetrahedron ({4 * cb:.12f} vs {a ** 3 / (6 * 2 ** .5):.12f})',
          abs(6 * cs - a ** 3) < 1e-12 and abs(4 * cb - a ** 3 / (6 * 2 ** .5)) < 1e-12)
    out.append({'fill': f'rhombic dodecahedron {c["cut"]} + cubes + regular tetrahedra (edge a)', 'a': a, 'per_cell': '1 cut rhombic dodecahedron, 1 cube, 2 tetrahedra'})
TO = gcb.archimedean('truncated octahedron'); FTO = gcb.faces(TO)
for n, k in ((4, 2 ** .5), (6, 3 ** .5)):
    for lab, xf in xs.items():
        x = xf(k); cap = corner_pyramid(TO, FTO, 0, [x] * 24)
        d = {(0, 1): 2 * x * x, (2, 3): 2 * x * x}
        for e in [(0, 2), (0, 3), (1, 2), (1, 3)]: d[e] = 3 * x * x
        dv = cm_volume(d)
        check(f'(4) truncated octahedron, {n}-gons golden {lab}: 4 caps = disphenoid (sqrt2 x, sqrt3 x) ({4 * cap:.12f} vs {dv:.12f})', abs(4 * cap - dv) < 1e-12)
        out.append({'fill': f'truncated octahedron cut with its {n}-gons golden ({lab}) + tetragonal disphenoids', 'x': x, 'per_cell': '1 cut cell, 6 disphenoids'})
json.dump({'fills': out, 'checks': CHECKS}, open(os.path.join(DATA, 's6-spacefill.json'), 'w'), indent=1)
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
