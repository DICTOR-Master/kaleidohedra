"""Step 10 (paper #89): the golden cubes in honeycombs. Exact in K = Q(sqrt2, sqrt5) (cubes_lib).
1. 3D (DICTO proposed, from Rhombiverse): cubes of the cubic lattice cut at any depth 0 < x < 1/2 and regular octahedra
   of edge x sqrt2 fill space: the 8 corner pieces round a lattice point are the 8 orthant pieces of one octahedron.
   Checked exactly at the two golden depths: corner faces = octahedron faces, volume per lattice point = 1.
2. 4D: the rectified tesseractic honeycomb (rectified tesseracts {|y-c|_inf <= 1, |y-c|_1 <= 3}, c in 2Z^4, and 16-cells
   {|y-v|_1 <= 1}, v in (1,1,1,1) + 2Z^4) cut by y1 = h, 0 < h < 1, is the 3D filling of part 1 (scale 2) with x = h/2.
   Exact: section of the rectified tesseract (corners: all permutations of (±1,±1,±1,0)) at h = 2 x_G and 2 x_L matched
   corner to corner with the Greater and Lesser Golden Cut Cubes; section of the 16-cell at v = (1,1,1,1) is the regular
   octahedron with corners v' ± h e_j; its faces are the corner triangles of the cut cube; 4D and 3D volume identities.
3. The three regular honeycombs {4,3,3,4}, {3,3,4,3}, {3,4,3,3}: every tile of a hyperplane section is a hyperplane
   section of a tesseract, 16-cell or 24-cell, which has no octagonal face (s9 Part A), so no section contains a cube cut
   at its corners, in any direction.
usage (compute-host): python3 s10_honeycomb_cubes.py -> ../data/s10-honeycomb-cubes.json
"""
import sys, os, json, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data'); sys.path.insert(0, HERE)
from cubes_lib import *          # noqa
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)


xG, xL = golden_x()
out = {'golden_depths': {'greater': kstr(xG), 'lesser': kstr(xL)}}
check(f'x_G(4) = {kstr(xG)} = {float(xG):.9f}, x_L(4) = {kstr(xL)} = {float(xL):.9f}; corner/original side ratios '
      f'phi and 1/phi (side sqrt2 x against 1 - 2x)', S2 * xG / (1 - 2 * xG) == PHI and S2 * xL / (1 - 2 * xL) == 1 / PHI)

# ---------------------------------------------------------------- 1. 3D filling
for lab, x in (('Greater', xG), ('Lesser', xL)):
    C = cut_cube(x, K(Fr(1, 2)))                                   # unit cube centred at 0, corners (±1/2)^3
    v = (K(Fr(1, 2)),) * 3                                          # the lattice point at the corner (1/2,1/2,1/2)
    tri = [p for p in C if all((p[k] - v[k]).sign() <= 0 for k in range(3)) and sum((v[k] - p[k] for k in range(3)), ZERO) == x]
    octa = [tuple(v[k] + (s if k == j else 0) * x for k in range(3)) for j in range(3) for s in (1, -1)]
    face = [o for o in octa if all((o[k] - v[k]).sign() <= 0 for k in range(3))]
    check(f'3D, {lab} Golden Cut Cube (edge 1): its corner triangle at a lattice point is exactly a face of the regular octahedron '
          f'with corners at distance x from that point (edge x sqrt2)', sorted(map(key, tri)) == sorted(map(key, face)) and len(tri) == 3)
    vol = 1 - 8 * x * x * x / 6 + K(Fr(4, 3)) * x * x * x
    check(f'3D, {lab}: volume per lattice point, cut cube 1 - 8 x^3/6 plus octahedron 4 x^3/3, is exactly 1', vol == ONE)
    ok, lam = similar(C, cut_cube(x)); check(f'3D, {lab}: the cut unit cube is the {lab} Golden Cut Cube (corner-to-corner, exact)', ok)

# ---------------------------------------------------------------- 2. rectified tesseractic honeycomb
RT = sorted({key(p): p for p in (tuple(K(s[i]) * (0 if i == z else 1) for i in range(4))
                                  for z in range(4) for s in itertools.product((1, -1), repeat=4))}.values(), key=lambda p: [float(c) for c in p])
check('rectified tesseract: 32 corners, all permutations of (±1,±1,±1,0); each satisfies |y|_inf <= 1 and |y|_1 = 3',
      len(RT) == 32 and all(sum((K(abs(float(c))) for c in p), ZERO) == K(3) for p in RT))
ERT = edges_at(RT, K(2))
check('rectified tesseract: 96 edges of length sqrt2', len(ERT) == 96)
X16 = [tuple(K(1) + (K(s) if k == j else ZERO) for k in range(4)) for j in range(4) for s in (1, -1)]   # 16-cell at v=(1,1,1,1)
E16 = edges_at(X16, K(2))
rows = []
for lab, x in (('Greater', xG), ('Lesser', xL)):
    h = 2 * x
    S = section(RT, ERT, (ONE, ZERO, ZERO, ZERO), h)
    ok, lam = similar([p[1:] for p in S], cut_cube(x))
    check(f'4D, {lab}: the rectified tesseract cut by y1 = h = 2x = {kstr(h)} = {float(h):.9f} has {len(S)} corners and is the '
          f'{lab} Golden Cut Cube of edge 2 (corner-to-corner, all 276 squared distances equal, exact)', ok and lam == ONE)
    O = section(X16, E16, (ONE, ZERO, ZERO, ZERO), h)
    want = [tuple(K(1) + (s * h if k == j else ZERO) for k in range(3)) for j in range(3) for s in (1, -1)]
    check(f'4D, {lab}: the 16-cell at (1,1,1,1) cut by y1 = h is the regular octahedron with corners (1,1,1) ± h e_j (edge h sqrt2)',
          sorted(map(key, [p[1:] for p in O])) == sorted(map(key, want)))
    corner = (ONE, ONE, ONE)
    tri = [p[1:] for p in S if sum((corner[k] - p[1 + k] for k in range(3)), ZERO) == h]
    face = [w for w in want if all((w[k] - corner[k]).sign() <= 0 for k in range(3))]
    check(f'4D, {lab}: the corner triangle of the cut cube at (1,1,1) is exactly a face of that octahedron (face to face)',
          len(tri) == 3 and sorted(map(key, tri)) == sorted(map(key, face)))
    rows.append({'solid': f'{lab} Golden Cut Cube', 'x': kstr(x), 'height_h': kstr(h), 'height_float': float(h),
                 'cut_cube_corners': len(S), 'octahedron_corners': len(O)})
v4 = 16 - 16 * Fr(1, 24) + Fr(16, 24)
check('4D volume per point of 2Z^4: rectified tesseract 16 - 16 (1/24) plus one 16-cell 16/24 = 16 = 2^4 (the honeycomb fills space)', v4 == 16)
out['rectified_tesseractic_honeycomb'] = rows
out['regular_honeycombs'] = 'no octagon in any section of a tesseract, 16-cell or 24-cell (s9 Part A), so no corner-cut cube in any section'
json.dump({'result': out, 'checks': CHECKS}, open(os.path.join(DATA, 's10-honeycomb-cubes.json'), 'w'), indent=1)
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
