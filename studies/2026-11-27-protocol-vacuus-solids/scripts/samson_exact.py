"""Exact derivation of Samson's fixed-shape ratio (27 Nov 2026, DICTO "great"). With Claude (Anthropic).
Samson (DICTO's Delian bond, #51): unit cube with its 4 odd corners cut off at leg a = 2^(-1/3). Core rule (#78 Prop. 5, study 2 of
2026-10-30): tips at t x the feet of the face perpendiculars; core = intersection, family by family, of the hulls of the tips.
w = unit diagonal towards an odd corner (4 of them). Truncated tetrahedron T(A, B): planes -w.x <= A (hexagon family, 4 planes) and
w.x <= B (triangle family), A < B < 3A."""
import sympy as sp
a, t = sp.symbols('a t', positive=True); s3 = sp.sqrt(3)
d_tri = s3/2 - a/s3                     # Samson's triangle planes: distance along w (corner sqrt3/2 cut at depth a/sqrt3)
d_hex = sp.Rational(1, 2)               # Samson's six (cut) square faces, along +-e_k
# turn 1: triangle-tip hull = tetrahedron, circumradius t d_tri along w, so faces at t d_tri/3 along -w;
#         hexagon-tip hull = octahedron with corners t/2 e_k, faces at t/(2 sqrt3) along all 8 diagonals (+w and -w)
A1 = sp.Min(t*d_tri/3, t/(2*s3)); B1 = t/(2*s3)
A1 = t*d_tri/3                          # smaller of the two along -w, since d_tri/3 < 1/(2 sqrt3) <=> a > 0
assert sp.simplify(t/(2*s3) - t*d_tri/3 - 2*a*t/(6*s3)) == 0
q = sp.simplify(B1/A1)                  # triangle distance / hexagon distance
print('turn 1 core: q = B/A =', q, '; truncated tetrahedron needs 1 < q < 3:', sp.simplify(q), '(holds for 0 < a < 1)')
# every later turn: tips of T(A,B): triangle tips at tB along w -> tetrahedron, faces tB/3 along -w; hexagon tips at tA along -w ->
# faces tA/3 along +w. New shape: -w.x <= tB/3, w.x <= tA/3, i.e. the point reflection of T(A, B) scaled by t/3: SAME SHAPE.
A, B = sp.symbols('A B', positive=True)
newA, newB = t*B/3, t*A/3              # along -w, along +w
print('next turn: (along +w, along -w) =', (newB, newA), '= (t/3)(A, B) with w -> -w: point reflection of T(A,B) at scale t/3')
# edge ratio of T(A,B): parent tetrahedron (planes -w.x <= A) has corners at 3A w; triangle planes cut at w.x = B; cut fraction along
# an edge u = (3A - B)/(4A); triangle side = u L, long hexagon side = (1 - 2u) L.
u = (3 - q)/4; r = sp.simplify((1 - 2*u)/u)
c = sp.cbrt(2); r_samson = sp.nsimplify(sp.simplify(r.subs(a, 1/c)))
target = 2/(3*(c - 1))
print('r(a) =', sp.simplify(r), '; at a = 2^(-1/3): r - 2/(3(cbrt2 - 1)) =', sp.simplify(sp.radsimp(r.subs(a, 1/c) - target)))
print('value', sp.N(target, 20), '; cubic 27r^3-54r^2-36r-8 at r:', sp.simplify(sp.expand(27*target**3 - 54*target**2 - 36*target - 8)))
ok = sp.simplify(sp.radsimp(r.subs(a, 1/c) - target)) == 0
print('FINAL ok' if ok else 'FINAL FAIL')
