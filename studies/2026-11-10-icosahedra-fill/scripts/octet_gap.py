"""Icosahedral (gyrated) octet, DICTO 10 Nov 2026: 'new pieces for icosahedral gyrated octet'. A regular icosahedron inscribed in the
regular octahedron (corners on the 12 edges, dividing each in the golden ratio); the octahedron minus the icosahedron splits into the
new pieces. Exact (sympy): corners, volumes, faces, dihedral angles."""
import sympy as sp, itertools
phi = (1 + sp.sqrt(5)) / 2
# octahedron corners (±1,0,0)...; edge from (1,0,0) to (0,1,0): point at golden division. Standard pseudo-icosahedral choice:
# icosahedron corners = cyclic perms of (0, ±1, ±phi) scaled; it lies in the octahedron |x|+|y|+|z| <= 1+phi after scaling.
I = []
for s1, s2 in itertools.product((1, -1), repeat=2):
    for v in ((0, s1, s2 * phi), (s1, s2 * phi, 0), (s2 * phi, 0, s1)): I.append(sp.Matrix(v) / (1 + phi))
O = [sp.Matrix(v) for v in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))]
assert all(sp.simplify(sum(abs(c) for c in v) - 1) == 0 for v in I)     # every corner on the octahedron surface (on an edge)
# piece at octahedron corner (0,0,1): its corner plus the icosahedron corners on its 4 edges
V = O[4]; near = [v for v in I if v[2] > 0]
print('icosahedron corners on the edges at (0,0,1):', len(near), [list(map(sp.nsimplify, v)) for v in near])
def vol(a, b, c, d): return sp.Abs(sp.Matrix.hstack(b - a, c - a, d - a).det()) / 6
volO = sp.Rational(4, 3); volI = sp.nsimplify(sp.simplify(5 * (3 + sp.sqrt(5)) / 12 * (sp.sqrt(2) / (1 + phi) * 2) ** 3))
# edge of the inscribed icosahedron = distance between adjacent corners
e = min(sp.simplify((a - b).norm()) for a, b in itertools.combinations(I, 2))
volI = sp.simplify(sp.Rational(5, 12) * (3 + sp.sqrt(5)) * e ** 3)
print('octahedron edge sqrt2; icosahedron edge', sp.nsimplify(sp.simplify(e)), float(e))
gap = sp.simplify((volO - volI) / 6)
print('volumes: octahedron', volO, '; icosahedron', sp.simplify(volI), float(volI), '; each of 6 gap pieces', gap, float(gap))
# the gap piece = conv(V, near): which icosahedron edge splits its base
pairs = [(a, b) for a, b in itertools.combinations(range(4), 2) if sp.simplify((near[a] - near[b]).norm() - e) == 0]
print('icosahedron edges among the 4 base corners:', pairs)
# volume check of conv(V, near) as two tetrahedra over the shared edge
(a, b) = [p for p in pairs if all(sp.simplify((near[p[0]]-near[q]).norm()-e)==0 and sp.simplify((near[p[1]]-near[q]).norm()-e)==0 for q in set(range(4))-set(p))][0]
c, d = sorted(set(range(4)) - {a, b})
v2 = sp.simplify(vol(V, near[a], near[b], near[c]) + vol(V, near[a], near[b], near[d]))
print('conv(corner, 4 points) as 2 tetrahedra over the shared icosahedron edge:', v2, '; equals gap piece:', sp.simplify(v2 - gap) == 0)
def dih(p, q, r, s):    # dihedral angle along edge pq between faces pqr and pqs
    n1 = (q - p).cross(r - p); n2 = (q - p).cross(s - p)
    return sp.acos(sp.simplify(n1.dot(n2) / (n1.norm() * n2.norm())))
P = [V, near[a], near[b], near[c], near[d]]
print('faces: 2 icosahedron faces (base, folded), 4 triangles on octahedron faces')
for (i, j, k, l), name in [((1, 2, 3, 4), 'fold edge (icosahedron edge), between the two base faces, inside the piece'),
                          ((0, 1, 2, 3), 'not an edge'),]:
    pass
fold = dih(near[a], near[b], near[c], near[d]); print('angle at the fold (inside piece) =', sp.nsimplify(sp.cos(fold)), float(sp.deg(2*sp.pi - fold) if False else sp.deg(fold)))
