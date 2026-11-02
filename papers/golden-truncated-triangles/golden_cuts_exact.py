# Exact check of the ten golden truncations (DICTO-Kepler golden truncations, DICTO 11-03): Platonic solid with edge 1, every corner cut
# at distance x along its edges; x exact (corner-polygon side k*x, k = 1, sqrt2, phi for triangles, squares, pentagons). For each member,
# in exact arithmetic (sympy): the two side lengths of a truncated original face and their ratio (must be phi or 1/phi... reported long/short),
# corner polygon regular side, and the exact volume (Platonic volume minus the corner pyramids). Output golden-cuts-exact.md
import sympy as sp
g = (1 + sp.sqrt(5)) / 2
# Platonic data at edge 1: volume, number of vertices, vertex degree q, face size p, corner-cut side factor k, volume of one corner pyramid at cut x
PL = {'dodecahedron': dict(V=(15 + 7 * sp.sqrt(5)) / 4, n=20, p=5, k=g),
      'icosahedron': dict(V=5 * (3 + sp.sqrt(5)) / 12, n=12, p=3, k=1),
      'cube': dict(V=1, n=8, p=4, k=sp.sqrt(2)),
      'tetrahedron': dict(V=sp.sqrt(2) / 12, n=4, p=3, k=1),
      'octahedron': dict(V=sp.sqrt(2) / 3, n=6, p=3, k=1)}
# corner pyramid at cut x = x^3 * (volume of the corner pyramid at x = 1), the latter from the vertex figure: computed from coordinates below
import itertools
def corner_unit_volume(name):
    # exact vertex coordinates scaled to edge 1, take one vertex and its neighbours, pyramid apex = vertex, base = neighbours at distance 1 along edges
    s5 = sp.sqrt(5)
    if name == 'tetrahedron': P = [sp.Matrix(v) for v in ([1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1])]
    elif name == 'cube': P = [sp.Matrix([a, b, c]) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
    elif name == 'octahedron': P = [sp.Matrix([s * (i == k) for i in range(3)]) for k in range(3) for s in (1, -1)]
    elif name == 'icosahedron': P = [sp.Matrix(p) for a in (-1, 1) for b in (-1, 1) for p in ([0, a, b * g], [a, b * g, 0], [b * g, 0, a])]
    else: P = [sp.Matrix([a, b, c]) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)] + [sp.Matrix(p) for a in (-1, 1) for b in (-1, 1) for p in ([0, a / g, b * g], [a / g, b * g, 0], [b * g, 0, a / g])]
    d2 = min(sp.nsimplify((P[0] - Q).dot(P[0] - Q)) for Q in P[1:]); e = sp.sqrt(d2)
    v = P[0]; nb = [Q for Q in P[1:] if sp.simplify((v - Q).dot(v - Q) - d2) == 0]
    U = [v + (Q - v) / e for Q in nb]                       # points at distance 1 along each edge
    c = sum(U, sp.zeros(3, 1)) / len(U)                      # centre of the corner polygon
    # pyramid volume = sum of tetrahedra (v, c, U_i, U_{i+1}) with U ordered round c
    import math
    n = (c - v); n = n / sp.sqrt(n.dot(n)); a0 = U[0] - c
    ang = lambda u: math.atan2(float((n.cross(a0)).dot(u - c)), float(a0.dot(u - c)))
    U = sorted(U, key=ang)
    vol = sum(abs((U[i] - v).dot((U[(i + 1) % len(U)] - v).cross(c - v))) / 6 for i in range(len(U)))
    return sp.nsimplify(sp.simplify(vol))
out = ['# The ten golden truncations, exact (edge 1)\n', '| solid | case | cut x | face sides (corner-shared, original) | long/short | volume |', '|---|---|---|---|---|---|']
for name in ['dodecahedron', 'icosahedron', 'cube', 'tetrahedron', 'octahedron']:
    d = PL[name]; k = d['k']; cu = corner_unit_volume(name)
    for case, x in (('corner sides long', g / (k + 2 * g)), ('original sides long', 1 / (g * k + 2))):
        x = sp.radsimp(sp.simplify(x)); a = sp.radsimp(sp.simplify(k * x)); b = sp.radsimp(sp.simplify(1 - 2 * x))
        r = sp.radsimp(sp.simplify(max(a, b, key=float) / min(a, b, key=float)))
        assert sp.simplify(r - g) == 0, (name, case, r)
        vol = sp.radsimp(sp.simplify(d['V'] - d['n'] * cu * x ** 3))
        out.append(f'| {name} | {case} | {x} ≈ {float(x):.6f} | {a}, {b} | φ (exact) | {vol} ≈ {float(vol):.6f} |')
open('golden-cuts-exact.md', 'w').write('\n'.join(out) + '\n\nEvery long/short ratio checked symbolically equal to φ = (1+√5)/2.\n'); print('\n'.join(out))
