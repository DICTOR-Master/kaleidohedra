# DICTO Kyushindo Cores (#43), 2026-10-21: numerical check of the COVERING LEMMA behind the icosahedral nesting theorem.
# Lemma: for every unit u and w there is a rotation g of the icosahedral group I with (g u).w >= c, c = cos 37.377 deg = r/R of the
# icosahedron = sqrt((5+2 sqrt5)/15); i.e. the hull of every I-orbit on the unit sphere contains the ball of radius c.
# Proof (see README): the (2,3,5) Moebius triangle T has diameter exactly arccos c (its longest side A3A5), and the kite T u sT
# (s = reflection in A3A5) also has diameter arccos c because its other diagonal A2A2' is 2 x 18 deg = 36 deg < 37.377 deg.
# Checked here: the sides and the altitude of T, the kite's diameter, the lemma on a grid of u over T (worst case = the 5-fold and
# 3-fold axes, i.e. icosahedron/dodecahedron), and the same quantities for the octahedral group (kite fails there, lemma holds
# numerically with c = 1/sqrt3).
import numpy as np, itertools
from scipy.spatial import ConvexHull
PHI = (1 + 5 ** .5) / 2; deg = np.degrees
unit = lambda v: np.asarray(v, float) / np.linalg.norm(v)
def ico_vertices(): return np.array([s * np.roll((0, 1, PHI), r) for r in range(3) for s in itertools.product((1, -1), repeat=3)])
def rot_group(pts):
    """rotations mapping the point set to itself (float), from pairs of adjacent points."""
    pts = np.unique(np.round(pts, 9), axis=0); pts = pts / np.linalg.norm(pts, axis=1)[:, None]
    d = pts @ pts[0]; nb = np.argsort(-d)[1]; mats = []
    for i in range(len(pts)):
        for j in range(len(pts)):
            if i == j or abs(pts[i] @ pts[j] - pts[0] @ pts[nb]) > 1e-9: continue
            A = np.array([pts[0], pts[nb], np.cross(pts[0], pts[nb])]).T; B = np.array([pts[i], pts[j], np.cross(pts[i], pts[j])]).T
            M = B @ np.linalg.inv(A)
            if all(np.min(np.linalg.norm(pts - M @ p, axis=1)) < 1e-8 for p in pts) and not any(np.allclose(M, N) for N in mats): mats.append(M)
    return mats
def inradius_of_orbit(G, u):
    P = np.array([M @ u for M in G]); P = np.unique(np.round(P, 10), axis=0)
    if len(P) < 4: return 0.0
    h = ConvexHull(P); return min(-e[3] / np.linalg.norm(e[:3]) for e in h.equations)
def altitude(a, b, c): return np.degrees(np.arcsin(np.sin(a) * np.sin(b) / np.sin(c)))     # right spherical triangle, legs a, b, hypotenuse c
def check(name, G, A2, A3, Ahi, c_claim):
    ang = lambda p, q: deg(np.arccos(np.clip(p @ q, -1, 1)))
    a, b, cc = ang(A2, A3), ang(A2, Ahi), ang(A3, Ahi); h = altitude(np.radians(a), np.radians(b), np.radians(cc))
    print(f'{name}: Moebius triangle sides A2A3 {a:.4f}, A2A{"5" if name[0]=="i" else "4"} {b:.4f}, A3A{"5" if name[0]=="i" else "4"} {cc:.4f} deg; diameter = longest side {cc:.4f} = arccos({np.cos(np.radians(cc)):.6f}); claim c = {c_claim:.6f}')
    print(f'   altitude from A2 onto the longest side {h:.4f} deg -> kite diagonal A2A2\' = {2*h:.4f} deg; kite diameter = {max(cc, 2*h):.4f} deg -> kite argument {"WORKS" if 2*h < cc else "FAILS"}')
    worst = 1.0; where = None
    for i in range(0, 41):
        for j in range(0, 41 - i):
            l = np.array([i, j, 40 - i - j]) / 40; u = unit(l[0] * A2 + l[1] * A3 + l[2] * Ahi)
            r = inradius_of_orbit(G, u)
            if r < worst: worst, where = r, (round(l[0], 3), round(l[1], 3), round(l[2], 3))
    print(f'   min over a grid of u in the triangle of inradius(hull(orbit u)) = {worst:.6f} at barycentric (A2,A3,Ahi) = {where}; claim c = {c_claim:.6f}: {"holds" if worst >= c_claim - 1e-9 else "FAILS"}')
    for nm, u in (('A2 axis', A2), ('A3 axis', A3), ('high axis', Ahi)):
        print(f'   orbit of the {nm}: inradius {inradius_of_orbit(G, u):.6f}')
I = rot_group(ico_vertices()); assert len(I) == 60
A2, A5, A3 = unit((0, 0, 1)), unit((0, 1, PHI)), unit((PHI, 0, 2 * PHI + 1))
c_ico = ((5 + 2 * 5 ** .5) / 15) ** .5
check('icosahedral', I, A2, A3, A5, c_ico)
print(f'   1/c^2 = {1 / c_ico**2:.6f} = 15 - 6 sqrt5 = {15 - 6 * 5 ** .5:.6f} < phi = {PHI:.6f}  (29 < 13 sqrt5: 841 < 845); margin phi - (15-6sqrt5) = {PHI - 15 + 6 * 5 ** .5:.6f}')
O = rot_group(np.array(list(itertools.product((1, -1), repeat=3)), float)); assert len(O) == 24
check('octahedral', O, unit((1, 1, 0)), unit((1, 1, 1)), unit((1, 0, 0)), 1 / 3 ** .5)
print('   -> octahedral: S inside 3 P(S) for every octahedrally symmetric polytope is supported numerically (cube/octahedron sharp) but the kite proof does not cover it.')
