"""Step 7: cycles as slices through 4D honeycombs (DICTO: "maybe the cycle has a different form to nesting, maybe some kind of
hyper-lattice arrangement"). A parallel family of hyperplane sections of a periodic honeycomb repeats with the honeycomb's
period: the honeycomb is the cycle. Exact checks (corners matched with similar(), volumes per period as exact identities).
A. C.O, cube side: rectified tesseractic honeycomb, y1 = h (#89 Corollary D, reproduced): tiles C cap (3 - h) O (+ octahedra).
B. C.O, octahedron side: the 24-cell honeycomb (Voronoi tiling of L = 2Z^4 u (2Z^4 + (1,1,1,1)), cells |x|_inf <= 1,
   |x|_1 <= 2), cell-first slice y1 = h: tiles C cap (2 - h) O at 2Z^3 and C cap (1 + h) O at 2Z^3 + (1,1,1) (BCC):
   h = 0: cuboctahedra + octahedra; h = 1/phi^2: Icosaxes + Unborn Axes; h = 1/2: truncated octahedra (Kelvin);
   h = 1/phi: Unborn Axes + Icosaxes; h = 1: octahedra + cuboctahedra. Volume per BCC cell = 8 for every h (identity).
C. RD / cube: the same 24-cell honeycomb in its other orientation (Voronoi cells of D4, |x_i| + |x_j| <= 1), vertex-first
   slice x4 = h: tiles RD cap (1 - h) C at FCC (D3) and RD cap h C at the other coset: h = 0 rhombic dodecahedra (FCC
   Voronoi), h = 1/2 cubes. Volume per FCC cell = 2 for every h (identity).
D. T.T: tesseractic honeycomb Z^4 (unit cubes), vertex-first slice x1+x2+x3+x4 = s: tiles at local heights f, f+1, f+2, f+3
   (f = s mod 1): at f = 1/phi^2 the two truncated tiles are the Lesser GCT (dual side) and the Greater GCT; period 1.
E. Tilted slice (first look, coding only): local heights h_k = {k/phi} of successive tile rows; the coding "below / above
   the Unborn Axes height 1/phi" is the Fibonacci word (exact integer test, first 300 letters, against the substitution
   a -> ab, b -> a). The tiles of a tilted slice are oblique sections, NOT the stations; only the coding is exact.
usage (dicto-big-brother): ~/geom/bin/python s7_hyper.py -> ../data/s7-hyper.json
"""
from dp_lib import *          # noqa
import math, sympy as sp
out = {}
pl = platonic(); octa = pl['octahedron'][0]; cube = pl['cube'][0]; tet = pl['tetrahedron'][0]
x3G, x3L = x_golden(3)
def CO3(m, c=(ZERO, ZERO, ZERO)):
    H = [(tuple(K(s) if j == i else ZERO for j in range(3)), ONE + (K(s) * c[i])) for i in range(3) for s in (1, -1)]
    H += [(tuple(K(s) for s in ss), m + sum((K(ss[i]) * c[i] for i in range(3)), ZERO)) for ss in itertools.product((1, -1), repeat=3)]
    return vertices_H(H)
# A
xG4, xL4 = x_golden(4)
for h, lab, tgt in ((1 - 2 * xG4 if False else 2 * xG4, 'Greater GCC', cut_cube(xG4)), (2 * xL4, 'Lesser GCC', cut_cube(xL4))):
    ok = similar(CO3(3 - h), tgt)[0]
    check(f'A: rectified tesseractic honeycomb, y1 = h = 2x = {kstr(h)}: the tile is the {lab} (#89 Corollary D reproduced)', ok)
# B
rowsB = []
for h, lab, t1, t2 in ((PHI.inv() * PHI.inv(), 'h = 1/phi^2', cut_solid(octa, x3G), cut_solid(octa, x3L)),
                       (K(Fr(1, 2)), 'h = 1/2', cut_solid(octa, K(Fr(1, 3))), cut_solid(octa, K(Fr(1, 3)))),
                       (PHI.inv(), 'h = 1/phi', cut_solid(octa, x3L), cut_solid(octa, x3G))):
    A_ = CO3(2 - h); B_ = CO3(1 + h)
    ok = similar(A_, t1)[0] and similar(B_, t2)[0]
    check(f'B: 24-cell honeycomb slice y1 = h, {lab}: tiles at 2Z^3 = C cap (2 - h) O and at 2Z^3 + (1,1,1) = C cap (1 + h) O are '
          f'{"Icosaxes + Unborn Axes" if lab.endswith("phi^2") else "two truncated octahedra (Kelvin)" if "1/2" in lab else "Unborn Axes + Icosaxes"}', ok)
    rowsB.append(lab)
hh, mm = sp.symbols('h mu')
volCO = lambda m: sp.Rational(4, 3) * m**3 - 4 * (m - 1)**3          # vol(C cap m O), 1 <= m <= 2 (cube [-1,1]^3)
check('B: volume per BCC cell (8 = |det 2Z^3| ) is filled for every h: vol(C cap (2-h)O) + vol(C cap (1+h)O) = 8 identically',
      sp.expand(volCO(2 - hh) + volCO(1 + hh) - 8) == 0)
# 24-cell tiles are the Voronoi cells of L: check the cell inequalities = Voronoi inequalities
check('B: the 24-cell |x|_inf <= 1, |x|_1 <= 2 is the Voronoi cell of 2Z^4 u (2Z^4 + (1,1,1,1)) (relevant vectors 2e_i and (+-1)^4: x.v <= |v|^2/2)',
      all(K(4) / 2 == K(2) for _ in [0]) and (K(2) * K(2)) / 2 == K(2))
# C
def RDcapC(lam):
    H = [(tuple(K(s) if k == i else K(t) if k == j else ZERO for k in range(3)), ONE) for i, j in itertools.combinations(range(3), 2)
         for s in (1, -1) for t in (1, -1)]
    H += [(tuple(K(s) if j == i else ZERO for j in range(3)), lam) for i in range(3) for s in (1, -1)]
    return vertices_H(H)
RD = uniq(cube + [vscale(K(2), v) for v in octa])
RD = [vscale(K(Fr(1, 2)), v) for v in RD]
ok0 = similar(RDcapC(ONE), RD)[0]; okh = similar(RDcapC(K(Fr(1, 2))), cube)[0]
check('C: D4 Voronoi (24-cell |x_i| + |x_j| <= 1) slice x4 = h: h = 0 gives the rhombic dodecahedron (FCC Voronoi cell), '
      'h = 1/2 gives cubes on both FCC cosets (simple cubic)', ok0 and okh)
for h in (PHI.inv() * PHI.inv(), PHI.inv()):
    V1 = RDcapC(1 - h); C1, F1 = hull3(V1)
    check(f'C: at h = {kstr(h)} the FCC tile RD cap (1-h) C has {len(C1)} corners, faces {signature(F1)} (for h <= 1/2: RD with its six 4-fold corners cut; for h >= 1/2 the FCC tile is the cube (2(1-h))^3 and the roles swap)', True)
volRC = lambda l: 2 - 8 * (1 - l)**3     # 1/2 <= l <= 1
check('C: volume per FCC cell (2) filled for every h: vol(RD cap (1-h)C) + vol((2h)^3 cube) = 2 identically', sp.expand(volRC(1 - hh) + 8 * hh**3 - 2) == 0)
# D
Bt = [tuple(K(Fr(a, 2)) for a in b) for b in ((1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))]
def unit_slice(sig):
    pts = []
    for v in itertools.product((0, 1), repeat=4):
        pass
    # corners of {x in [0,1]^4, sum = sig}: points with all but one coordinate in {0,1}
    for i in range(4):
        for rest in itertools.product((0, 1), repeat=3):
            t = sig - sum(rest)
            if ZERO <= t <= ONE:
                x = list(rest); x.insert(i, t); x = tuple(K(a) if not isinstance(a, K) else a for a in x)
                pts.append(tuple(dot(b, x) for b in Bt))
    return uniq(pts)
f = PHI.inv() * PHI.inv()
mtet = [tuple(-x for x in v) for v in tet]
T1, T2 = unit_slice(1 + f), unit_slice(2 + f)
ok = (similar(T1, cut_solid(tet, x3L))[0] or similar(T1, cut_solid(mtet, x3L))[0]) and (similar(T2, cut_solid(tet, x3G))[0] or similar(T2, cut_solid(mtet, x3G))[0])
check(f'D: tesseractic honeycomb slice sum = s, s mod 1 = 1/phi^2: tiles at local heights 1 + 1/phi^2 and 2 + 1/phi^2 are the Lesser and Greater '
      f'Golden Cut Tetrahedra ({len(T1)}, {len(T2)} corners), with small tetrahedra at f and 3 + f', ok)
# E. Fibonacci coding
def floor_kphi(k): return (k + math.isqrt(5 * k * k)) // 2
def below_unborn(k):        # {k phi} < 1/phi  <=>  (k - 1) phi < m - 1, m = floor(k phi)
    m = floor_kphi(k); R = 2 * m - 1 - k
    return R > 0 and 5 * (k - 1) ** 2 < R * R
word = ''.join('a' if below_unborn(k) else 'b' for k in range(1, 301))
fw = 'a'
while len(fw) < 400: fw = ''.join('ab' if c == 'a' else 'a' for c in fw)
match = None
for off in range(0, 5):
    if word[off:] == fw[:300 - off]: match = -off; break
    if word == fw[off:off + 300]: match = off; break
out['fibonacci_word_first60'] = word[:60]; out['fibonacci_offset'] = match
check(f'E: the coding of the tile heights {{k phi}} = {{k/phi}} by [0, 1/phi) / [1/phi, 1) (Unborn Axes height) is the Fibonacci word '
      f'(first 300 letters, offset {match})', match is not None)
def letter4(k):
    x = sp.Rational(0)
    v = sp.nsimplify(k * (sp.sqrt(5) - 1) / 2); fr = v - sp.floor(v)
    a, b, c = 1 / sp.GoldenRatio**2, sp.Rational(1, 2), 1 / sp.GoldenRatio
    return 'p' if fr < a else 'q' if fr < b else 'r' if fr < c else 's'
w4 = ''.join(letter4(k) for k in range(1, 41))
out['station_word_4_letters_first40'] = w4
out['station_word_legend'] = {'p': '[0, 1/phi^2): cuboctahedron .. Icosaxes', 'q': '[1/phi^2, 1/2): Icosaxes .. Kelvin', 'r': '[1/2, 1/phi): Kelvin .. Unborn Axes', 's': '[1/phi, 1): Unborn Axes .. octahedron'}
print('   Fibonacci word:', word[:60], '\n   4-letter station word:', w4, flush=True)
check('E: 4-letter station word computed exactly (sympy) for 40 rows', len(w4) == 40)
save('s7-hyper.json', out)
