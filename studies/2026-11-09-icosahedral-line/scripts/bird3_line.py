# bird3_line.py -- DICTO Hopscotch, icosahedral line, bird 3 (study 2026-11-09-icosahedral-line).
# The dodecahedron-icosahedron line S_lam = {a.x <= phi+2 (12 five-fold normals a, |a|^2 = phi+2)} n {b.x <= lam (20 three-fold
# normals b, |b|^2 = 3)}: five-fold faces at distance sqrt(phi+2), three-fold faces at distance lam/sqrt3.
# Antipol (same normals, inverted distances d -> |N|^2/d): S_lam^v = S_{k0/lam}/(phi+2), k0 = 3(phi+2): the turn is lam -> k0/lam.
# In the unit-distance coordinate mu = (lam/sqrt3)/sqrt(phi+2) = lam/sqrt(k0) it is mu -> 1/mu, fixed point mu = 1.
# t_min(S) = max x.y over corners x of S and y of S^v (bilinear form of the polarity). Exact in Q(sqrt5): corners are P + lam Q,
# corners of S^v are U + V/lam, so every corner pair gives A + B lam + C/lam; in each region between walls the maximising pair is
# proved exactly (lam * difference is a quadratic, checked >= 0 on the closed region).
import sys, time, itertools
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from q5 import *
t0 = time.time()
checks = {}
K0 = 3 * (PHI + 2)
LO = PHI * PHI; HI = K0 / (PHI * PHI)
print('line: lam in (phi^2, k0/phi^2) =', (LO.f(), HI.f()), ' k0 =', K0, '=', K0.f(), ' fixed point sqrt(k0) =', K0.f() ** .5)

def planes(lam):   # S_lam
    return [(a, PHI + 2) for a in AX5] + [(b, lam) for b in AX3]
def dual_planes(lam):   # S_lam^v: inverted distances
    return [(a, ONE) for a in AX5] + [(b, Q5(3) / lam) for b in AX3]
def sig(lam):
    C = corners(planes(lam))
    return (len(C), tuple(sorted((sum(1 for i in act if i < 12), sum(1 for i in act if i >= 12)) for _, act in C)))

# known cases first: the two ends are the icosahedron and the dodecahedron, t_min = 15 - 6 sqrt5 (Theorem 1 equality)
def tmin_exact(P, Dp):
    X = [x for x, _ in corners(P)]; Y = [y for y, _ in corners(Dp)]
    best = None
    for x in X:
        for y in Y:
            v = dot(x, y)
            if best is None or v > best: best = v
    return best
ico = [(b, Q5(3)) for b in AX3]; ico_d = [(b, Q5(1)) for b in AX3]
dod = [(a, PHI + 2) for a in AX5]; dod_d = [(a, ONE) for a in AX5]
checks['known: t_min(icosahedron) = t_min(dodecahedron) = 15 - 6 sqrt5'] = tmin_exact(ico, ico_d) == Q5(15, -6) and tmin_exact(dod, dod_d) == Q5(15, -6)
# the ends: at lam = phi^2 the five-fold planes touch the icosahedron's corners, at k0/phi^2 the three-fold planes touch the dodecahedron's
Cl = corners([(b, LO) for b in AX3]); Ch = corners(dod)
checks['ends: icosahedron (b.x <= phi^2) corners lie on the five-fold planes; dodecahedron corners on the three-fold planes at k0/phi^2'] = \
    all(max(dot(a, x) for a in AX5) == PHI + 2 for x, _ in Cl) and all(max(dot(b, x) for b in AX3) == HI for x, _ in Ch)

# walls: float scan of the combinatorics (float signature only), then the exact concurrency value
from scipy.spatial import HalfspaceIntersection
def fplanes(l):
    return np.array([np.r_[fl(a), -(PHI + 2).f()] for a in AX5] + [np.r_[fl(b), -l] for b in AX3])
def sigf(l, tol=1e-9):
    A = fplanes(l); hs = HalfspaceIntersection(A, np.zeros(3)); pts = []
    for p in hs.intersections:
        if not any(np.abs(p - q).max() < 1e-7 for q in pts): pts.append(p)
    acts = [tuple(np.nonzero(np.abs(A[:, :3] @ p + A[:, 3]) < tol)[0]) for p in pts]
    return (len(pts), tuple(sorted((sum(1 for i in a if i < 12), sum(1 for i in a if i >= 12)) for a in acts)))
grid = np.linspace(LO.f() + 1e-6, HI.f() - 1e-6, 1601)
sigs = [sigf(l) for l in grid]
changes = [i for i in range(len(grid) - 1) if sigs[i] != sigs[i + 1]]
walls = []
for i in changes:
    a, b = grid[i], grid[i + 1]
    for _ in range(30):
        m = (a + b) / 2
        if sigf(m) == sigs[i]: a = m
        else: b = m
    walls.append((a + b) / 2)
def wall_exact(lw):
    A = fplanes(lw); hs = HalfspaceIntersection(A, np.zeros(3))
    for p in hs.intersections:
        act = list(np.nonzero(np.abs(A[:, :3] @ p + A[:, 3]) < 1e-5)[0])
        if len(act) < 4 or not any(i >= 12 for i in act): continue
        for tri in itertools.combinations(act, 3):
            N = [AX5[i] if i < 12 else AX3[i - 12] for i in tri]
            if dot(N[0], cross(N[1], N[2])) == ZERO: continue
            P = solve3(N, [PHI + 2 if i < 12 else ZERO for i in tri]); Q = solve3(N, [ZERO if i < 12 else ONE for i in tri])
            for i4 in act:
                if i4 in tri: continue
                N4 = AX5[i4] if i4 < 12 else AX3[i4 - 12]; dc = PHI + 2 if i4 < 12 else ZERO; dl = ZERO if i4 < 12 else ONE
                den = dot(N4, Q) - dl
                if den == ZERO: continue
                lw_ex = (dc - dot(N4, P)) / den
                if abs(lw_ex.f() - lw) < 1e-6: return lw_ex
    return None
WX = [wall_exact(l) for l in walls]
print('walls of S_lam (exact):', WX, [w.f() for w in WX])
checks['every combinatorial wall of S_lam found exactly (a four-plane concurrency, linear in lam)'] = all(w is not None for w in WX)
for w in WX:
    C = corners(planes(w)); C2 = corners(planes(Q5(Fr(w.f() - 1e-4).limit_denominator(10**8)))); C3 = corners(planes(Q5(Fr(w.f() + 1e-4).limit_denominator(10**8))))
    print(f'  wall {w.f():.9f}: {len(C)} corners at the wall (active-plane counts {sorted(set(len(a) for _, a in C))}); {len(C2)} before, {len(C3)} after')
WALLS = sorted(set(WX) | {K0 / w for w in WX}, key=lambda q: q.f())
print('walls of the antipol pair (S_lam, S_lam^v), closed under the turn:', [w.f() for w in WALLS])
lamID = [w for w in WX if len(corners(planes(w))) == 30]
checks['one wall is the icosidodecahedron (30 corners)'] = len(lamID) == 1
# regions and the closed form
bounds = [LO] + WALLS + [HI]
def sym_corners(lam0, dual=False):
    pl = dual_planes(lam0) if dual else planes(lam0)
    out = []
    for x, act in corners(pl):
        for tri in itertools.combinations(sorted(act), 3):
            N = [pl[i][0] for i in tri]
            if dot(N[0], cross(N[1], N[2])) != ZERO: break
        if not dual:
            dc = [PHI + 2 if i < 12 else ZERO for i in tri]; dl = [ZERO if i < 12 else ONE for i in tri]
        else:
            dc = [ONE if i < 12 else ZERO for i in tri]; dl = [ZERO if i < 12 else Q5(3) for i in tri]
        P = solve3(N, dc); Q = solve3(N, dl)
        out.append((P, Q))
    return out
def quad_nonneg(c0, c1, c2, a, b):
    # q(l) = c0 + c1 l + c2 l^2 >= 0 on [a, b], exact
    q = lambda l: c0 + c1 * l + c2 * l * l
    if q(a) < ZERO or q(b) < ZERO: return False
    if c2 > ZERO:
        v = -c1 / (2 * c2)
        if a < v < b and q(v) < ZERO: return False
    return True
forms = []
for r in range(len(bounds) - 1):
    a, b = bounds[r], bounds[r + 1]
    lam0 = Q5(Fr((a.f() + b.f()) / 2).limit_denominator(1000))
    X = sym_corners(lam0); Y = sym_corners(lam0, dual=True)
    F = []
    for P, Q in X:
        for U, V in Y:
            F.append((dot(P, U) + dot(Q, V), dot(Q, U), dot(P, V)))       # A + B lam + C/lam
    val = [A.f() + B.f() * lam0.f() + C.f() / lam0.f() for A, B, C in F]
    A0, B0, C0 = F[int(np.argmax(val))]
    proved = all(quad_nonneg(C0 - C, A0 - A, B0 - B, a, b) for A, B, C in F)
    forms.append((A0, B0, C0))
    print(f'region {r}: lam in [{a.f():.6f}, {b.f():.6f}]: t_min = {A0} + ({B0}) lam + ({C0})/lam   proved max on the closed region: {proved}', flush=True)
    checks[f'region {r}: maximising pair proved exactly on the closed region'] = proved
    # exact spot checks against full corner enumeration
    for l in (a + (b - a) / 3, a + (b - a) * 2 / 3):
        tm = tmin_exact(planes(l), dual_planes(l))
        checks[f'region {r}: closed form = full enumeration at two interior points'] = checks.get(f'region {r}: closed form = full enumeration at two interior points', True) and tm == A0 + B0 * l + C0 / l
# turn symmetry: t(lam) = t(k0/lam): region r <-> region n-1-r with A' = A, B' = C/k0, C' = B k0
n = len(forms)
checks['turn: t_min(lam) = t_min(k0/lam) (regions exchanged in pairs, the middle one symmetric)'] = all(
    forms[n - 1 - r][0] == forms[r][0] and forms[n - 1 - r][1] == forms[r][2] / K0 and forms[n - 1 - r][2] == forms[r][1] * K0 for r in range(n))
A1, B1, C1 = forms[n // 2]; A0, B0, C0 = forms[0]
print('middle region: t_min = A + B sqrt(k0) s, s = mu + 1/mu; A =', A1, ' B sqrt(k0) = sqrt(', B1 * B1 * K0, ') * sign', B1.sign())
# maximum at the fixed point: the middle form A1 + B1 sqrt(k0) s with B1 < 0 is largest at s = 2
checks['middle region: B < 0, so t_min is largest at s = 2 (mu = 1, the fixed point)'] = B1 < ZERO
tfix = A1.f() + 2 * B1.f() * K0.f() ** .5
# outer regions stay below: on region 0 t = A0 + B0 lam + C0/lam; compare with tfix (float, and exact square test)
lam_f = np.linspace(LO.f(), HI.f(), 20001)
def tf(l):
    for r in range(n):
        if l <= bounds[r + 1].f() + 1e-15: A, B, C = forms[r]; return A.f() + B.f() * l + C.f() / l
    A, B, C = forms[-1]; return A.f() + B.f() * l + C.f() / l
vals = np.array([tf(l) for l in lam_f])
print(f't_min at the fixed point = {tfix:.12f}; largest on a 20001-point grid {vals.max():.12f} at lam = {lam_f[vals.argmax()]:.6f} (sqrt(k0) = {K0.f() ** .5:.6f})')
checks['grid: the largest t_min on the open line is at the fixed point'] = abs(lam_f[vals.argmax()] - K0.f() ** .5) < 2 * (lam_f[1] - lam_f[0]) and vals.max() <= tfix + 1e-12
# exact: at the fixed point the solid is a self-antipol (all faces at distance 1 in unit form): t_min = R^2 = (R/r)^2.
# R^2 in the frame lam = sqrt(k0): corners of type (two fives, one three) or (one five, two threes); R^2/r^2 with r^2 = phi+2
# (A1 + 2 B1 sqrt(k0))^2 test: t_fix = A1 - 2 sqrt(B1^2 k0) since B1 < 0
Bk = B1 * B1 * K0
print('t_min at the fixed point = A - 2 sqrt(B^2 k0) =', A1, '- 2 sqrt(', Bk, ')')
# compare with Theorem 1 bound (R/r)^2 at the fixed point (float from corners at lam = sqrt(k0), float)
lamfix = Q5(Fr(K0.f() ** .5).limit_denominator(10**12))
Cf = corners(planes(lamfix)); R2 = max(dot(x, x).f() for x, _ in Cf); r2 = (PHI + 2).f()
print(f'(R/r)^2 at the fixed point = {R2 / r2:.12f}; t_min = {tfix:.12f}')
checks['at the fixed point t_min = (R/r)^2 (Theorem 1 equality, all faces tangent to one sphere)'] = abs(R2 / r2 - tfix) < 1e-9
# ends: the limits of the closed form at the two ends, against t_min of the end solids (15 - 6 sqrt5)
lim_lo = A0 + B0 * LO + C0 / LO
print('limit of t_min at the icosahedron end:', lim_lo, '=', lim_lo.f(), ' t_min(icosahedron) = 15 - 6 sqrt5 =', Q5(15, -6).f())
checks['limit at the ends < 15 - 6 sqrt5: t_min jumps at the ends (a family stops being facets)'] = lim_lo < Q5(15, -6)
# the closed form as one minimum, like min(mu, 3/mu, 5 - s) on the cube-octahedron line:
# t_min = min(lam/phi^2, k0/(phi^2 lam), 10 - sqrt5 - (lam + k0/lam)) on the open line
P2 = PHI * PHI
checks['region forms: lam/phi^2 | 10 - sqrt5 - (lam + k0/lam) | k0/(phi^2 lam)'] = forms[0] == (ZERO, ONE / P2, ZERO) and forms[1] == (Q5(10, -1), -ONE, -K0) and forms[2] == (ZERO, ZERO, K0 / P2)
g = lambda l: Q5(10, -1) - l - K0 / l - l / P2          # concave in lam (lam > 0)
checks['g = middle - lam/phi^2 vanishes at phi^2 and 3 (concave), so the middle form is >= lam/phi^2 on [phi^2, 3] and <= beyond'] = g(P2) == ZERO and g(Q5(3)) == ZERO
checks['in mu = lam/sqrt(k0): lam/phi^2 = mu/c, since k0/phi^4 = 15 - 6 sqrt5 = 1/c^2'] = K0 / (P2 * P2) == Q5(15, -6)
checks['t_min = 3/phi^2 exactly at both walls (lam = 3 and the icosidodecahedron lam = phi + 2)'] = Q5(3) / P2 == forms[0][1] * 3 and forms[2][2] / (PHI + 2) == Q5(3) / P2
print('closed form: t_min(S_lam) = min(lam/phi^2, k0/(phi^2 lam), 10 - sqrt5 - (lam + k0/lam)); unit form t = min(mu/c, 1/(c mu), 10 - sqrt5 - sqrt(k0) (mu + 1/mu))')
print('maximum at the fixed point mu = 1: 10 - sqrt5 - 2 sqrt(k0) = 10 - sqrt5 - sqrt(30 + 6 sqrt5) =', 10 - 5 ** .5 - (30 + 6 * 5 ** .5) ** .5)
for k, v in checks.items(): print(('  ok   ' if v else '  FAIL ') + k)
print(f'time {time.time() - t0:.0f} s')
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, v in checks.items() if not v))
