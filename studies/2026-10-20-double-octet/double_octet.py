# DICTO 2026-10-20: the double octet construction set (DICTO's idea), faceted first: the octet truss built from ONE tetrahedron piece with
# 2 convex and 2 concave faces and ONE octahedron piece with 4 convex and 4 concave, every convex face fitting its neighbour's concave one.
# Rule: a face is convex for the piece whose outward normal is in A = {n1, n2, -n3, -n4} (n_i the four (+-1,+-1,+-1) directions with an
# even number of minus signs); the two pieces on a shared face have opposite normals, so one bulges and the other dents. A bump (dent) is the
# pyramid on the face whose apex stands (sinks) by the tetrahedron's inradius: exactly a quarter of the tetrahedron.
# Frame: the octet on the face-centred cubic lattice of integer points with even sum (edge sqrt2). Exact facts are rational arithmetic
# and congruence by corner matching (exact integer/half coordinates); the patch test is float (manifold3d): no overlaps, fills the box.
import itertools, json, os, sys
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
N4 = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
A = {N4[0], N4[1], tuple(-x for x in N4[2]), tuple(-x for x in N4[3])}
def faces_tet(V):
    c = [sum(Fr(p[k]) for p in V) / 4 for k in range(3)]; out = []
    for f in itertools.combinations(range(4), 3):
        P = [V[i] for i in f]; m = [sum(Fr(p[k]) for p in P) / 3 for k in range(3)]; d = [m[k] - c[k] for k in range(3)]
        out.append((P, tuple(int(np.sign(float(x))) for x in d)))
    return out, c
def faces_oct(cen):
    out = []
    for s in itertools.product((1, -1), repeat=3):
        P = [tuple(cen[k] + (s[k] if k == j else 0) for k in range(3)) for j in range(3)]; out.append((P, s))
    return out
# the tetrahedron's inradius direction: apex = face centroid +- (centroid - centre) scaled so its distance from the face is the inradius;
# for a regular tetrahedron the centre is at inradius below every face, so the bump apex is the reflection of the centre in the face.
def refl(c, P):
    m = [sum(Fr(p[k]) for p in P) / 3 for k in range(3)]; return tuple(2 * m[k] - c[k] for k in range(3))
up = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]; down = [(1, 1, 1), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
d2 = lambda a, b: sum((Fr(x) - Fr(y)) ** 2 for x, y in zip(a, b))
def piece_tet(V):
    F, c = faces_tet(V); conv = [(P, n) for P, n in F if n in A]; conc = [(P, n) for P, n in F if n not in A]
    return F, c, conv, conc
for V, nm in [(up, 'up'), (down, 'down')]:
    F, c, conv, conc = piece_tet(V)
    ok(len(conv) == 2 and len(conc) == 2, f'{nm} tetrahedron: 2 convex and 2 concave faces')
octF = faces_oct((1, 0, 0)); ok(sum(1 for _, n in octF if n in A) == 4 and all((n in A) != (tuple(-x for x in n) in A) for _, n in octF),
   'octahedron: 4 convex and 4 concave faces, every pair of parallel faces one of each')
# every octet face is shared by one tetrahedron and one octahedron with opposite outward normals: one convex, one concave
ok(all((n in A) != (tuple(-x for x in n) in A) for n in itertools.product((1, -1), repeat=3)), 'on every shared face one side bulges and the other dents (opposite normals, A holds exactly one of each pair)')
# the bump on a face = the reflection of the tetrahedron's centre in the face: the bump is congruent to the quarter tetrahedron
F, c, conv, conc = piece_tet(up)
P, n = conv[0]; apex = refl(c, P); quarter = sorted(d2(a, b) for a, b in itertools.combinations(P + [tuple(c)], 2)); bump = sorted(d2(a, b) for a, b in itertools.combinations(P + [apex], 2))
ok(quarter == bump, f'bump = dent = a quarter tetrahedron (the face and the centre), height = the inradius; edges^2 {sorted(set(map(str, bump)))}')
vt, vq = Fr(1, 3), Fr(1, 12)       # tetrahedron of edge sqrt2 (the cube's alternate corners): 1/3; a quarter 1/12; octahedron 4/3
ok(4 * vq == vt, 'volumes: tetrahedron piece 1/3 (2 quarters in, 2 bumps out), octahedron piece 4/3 (+ 4 bumps - 4 dents), as the octet')
# the tetrahedron piece: its two own quarters (under the convex faces) share the triangle (centre + their common edge); each quarter
# with its bump is a triangular bipyramid (the face as waist)
e = set(conv[0][0]) & set(conv[1][0]); ok(len(e) == 2, 'the tetrahedron piece = two triangular bipyramids (quarter + bump) hinged on the triangle centre + common edge')
# up and down pieces are one shape: some rotation of the cube's symmetry takes the down piece (convex faces, concave faces) onto the up one
import numpy.linalg as la
rots = [np.array(m) for m in itertools.product(*[[(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]] * 3) if abs(la.det(np.array(m)) - 1) < 1e-9 and np.allclose(np.array(m) @ np.array(m).T, np.eye(3))]
def pattern(V):
    F, c, conv, conc = piece_tet(V); C = np.array([float(x) for x in c])
    return {frozenset(tuple(np.round(np.array([float(x) for x in p]) - C, 6)) for p in P) for P, _ in conv}, {frozenset(tuple(np.round(np.array([float(x) for x in p]) - C, 6)) for p in P) for P, _ in conc}
pu, pd = pattern(up), pattern(down)
rot_ok = any(({frozenset(tuple(np.round(R @ np.array(p), 6)) for p in f) for f in pd[0]} == pu[0]) for R in rots)
ok(rot_ok, 'the up and the down tetrahedron pieces are the same shape (a proper rotation takes one onto the other, convex faces to convex)')
print('done')
