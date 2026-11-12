"""Checks for the paper on the turn law (DICTO's polar lines). Every line prints ok/FAIL; the last line is FINAL ok or FINAL FAIL.
usage: python3 turn_law_checks.py STUDIES_DIR   (STUDIES_DIR holds 2026-11-09-ab-turn/scripts/zono.py)
Parts:
 A  the general turn law on a polar line S(mu) = {n.x <= h} cap {v^.x <= mu/R}: every plane a facet on (h^2, R^2), the antipol
    rule S(mu)^v = h^-2 S(c/mu), the polar S(mu)^o = feet hull of S(mu)^v, the fixed point hR (tangent solid) and linear walls,
    exact (sympy) for the cube; numerically for two non-regular solids with one inradius and one circumradius (rhombic disphenoid,
    tetragonal disphenoid); t_min symmetric under the turn there, and where its maximum lies (numerical).
 B  the summit for regular polytopes (DICTO's Turn Theorem): the peaks and breaks of Table 1 recomputed exactly from the squared flag
    radii; the d-cube corollary; the 600-cell peak simplified; log-concavity and symmetry on a float scan of each line.
 C  the cuboctahedron example: the antipol of S(2) is S(3/2), the uniform truncated octahedron; the polar of S(2) is the rhombic
    dodecahedron, the feet hull of S(3/2).
 D  the Ammann-Beenker line: the turn map with its exact signs; t = 1/sqrt2 is the AB star (a rotation by 135 degrees after the
    Galois twist); Pell pairs: equal vertex-star frequencies; tile level: n accepted at (t, gamma) iff A n accepted at
    (1/(2t), gamma'), gamma' = -M gamma - eps_0(1/(2t)), on a box of Z^4, with negative controls; edge-direction ratios and squares
    per rhombus on 10 distinct slopes."""
import sys, os, math, itertools, random
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy.spatial import HalfspaceIntersection, ConvexHull

sys.path.insert(0, os.path.join(sys.argv[1], '2026-11-09-ab-turn', 'scripts'))
from zono import zonogon, arrangement, area, halfplanes, cross, sub

OK = True
def check(name, cond):
    global OK
    OK &= bool(cond); print(('  ok   ' if cond else '  FAIL ') + name, flush=True)

# ------------------------------------------------------------------ A: the general law
print('A  the general turn law', flush=True)
def corners(N, d):
    """corners of {N x <= d} (float), 0 strictly inside"""
    H = np.hstack([N, -np.asarray(d, float)[:, None]])
    hs = HalfspaceIntersection(H, np.zeros(N.shape[1]))
    P = hs.intersections; out = []
    for p in P:
        if not any(np.linalg.norm(p - q) < 1e-9 for q in out): out.append(p)
    return np.array(out)
def facet_planes(N, d, C):
    """indices of planes that carry a facet of the solid with corners C (at least dim corners spanning the plane)"""
    dim = N.shape[1]; idx = []
    for i in range(len(N)):
        on = C[np.abs(C @ N[i] - d[i]) < 1e-9]
        if len(on) >= dim and np.linalg.matrix_rank(on[1:] - on[0], tol=1e-9) == dim - 1: idx.append(i)
    return idx
def line(Nf, h, V):
    """the polar line of a solid with unit facet normals Nf (all at h) and corners V (all at radius R)"""
    R = float(np.linalg.norm(V[0])); Vh = V / R
    def S(mu): return np.vstack([Nf, Vh]), np.array([h] * len(Nf) + [mu / R] * len(Vh))
    return S, R
def tmin(N, d):
    """t_min = max x.y over S x S^v (form (B)); S^v keeps the normals and inverts the distances"""
    C = corners(N, d); Cv = corners(N, 1 / d)
    return float(np.max(C @ Cv.T)), C, Cv

def disphenoid(a, b, c):
    V = np.array([[a, b, c], [a, -b, -c], [-a, b, -c], [-a, -b, c]], float)
    faces = [f for f in itertools.combinations(range(4), 3)]
    Nf = []
    for f in faces:
        p, q, r = V[list(f)]; n = np.cross(q - p, r - p); n /= np.linalg.norm(n)
        if n @ p < 0: n = -n
        Nf.append(n)
    Nf = np.array(Nf); h = float(Nf[0] @ V[faces[0][0]])
    return Nf, h, V
for name, (a, b, c) in [('rhombic disphenoid (1, 1.3, 1.7)', (1, 1.3, 1.7)), ('tetragonal disphenoid (1, 1, 1.6)', (1, 1, 1.6))]:
    Nf, h, V = disphenoid(a, b, c)
    hs_ = Nf @ V.T; dist = [max(Nf[i] @ V[j] for j in range(4)) for i in range(4)]
    check(f'{name}: one inradius h = {h:.6f} (spread {max(dist) - min(dist):.1e}) and one circumradius', max(dist) - min(dist) < 1e-12 and np.ptp(np.linalg.norm(V, axis=1)) < 1e-12)
    S, R = line(Nf, h, V); cc = h * h * R * R
    mus = np.exp(np.linspace(math.log(h * h) + 1e-3, math.log(R * R) - 1e-3, 401))
    ts = []; okf = okt = True
    for mu in mus:
        N, d = S(mu); t, C, Cv = tmin(N, d)
        okf &= len(facet_planes(N, d, C)) == len(N)
        N2, d2 = S(cc / mu); C2 = corners(N2, d2)
        okt &= len(C2) == len(Cv) and all(min(np.linalg.norm(C2 - h * h * y, axis=1)) < 1e-8 for y in Cv)
        ts.append(t)
    ts = np.array(ts)
    check(f'{name}: every plane is a facet on the whole open line (401 points)', okf)
    check(f'{name}: antipol rule S(mu)^v = h^-2 S(c/mu) at all 401 points', okt)
    sym = max(abs(np.interp(math.log(cc) - math.log(m), np.log(mus), ts) - t) for m, t in zip(mus, ts) if h * h * 1.01 < cc / m < R * R / 1.01)
    check(f'{name}: t_min symmetric under the turn (largest gap {sym:.1e}, interpolated)', sym < 1e-3)
    k = int(np.argmax(ts)); NF, dF = S(h * R); tF, CF, _ = tmin(NF, dF)
    print(f'     argmax of t_min on the grid mu = {mus[k]:.6f}, fixed point hR = {h * R:.6f}; max {ts[k]:.9f}, at hR {tF:.9f}, R(S)^2/h^2 = {max(np.sum(CF**2, 1)) / h / h:.9f}')
    check(f'{name}: at hR, t_min = R(S)^2/h^2 (tangent solid)', abs(tF - max(np.sum(CF**2, 1)) / h / h) < 1e-9)
    check(f'{name}: the largest t_min on the grid is the value at hR (numerical; within grid step)', tF >= ts.max() - 1e-9)
    lt = np.log(ts); x = np.log(mus); sl = np.diff(lt) / np.diff(x)
    check(f'{name}: log t_min concave in log mu on the grid (slopes non-increasing up to 1e-6)', np.all(np.diff(sl) <= 1e-6))

# exact, cube line: facets on (1, 3), antipol rule, linear walls
mu = sp.symbols('mu', positive=True)
Nc = [sp.Matrix(v) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
Vc = [sp.Matrix(v) / sp.sqrt(3) for v in itertools.product((1, -1), repeat=3)]
def conc_det(rows):
    return sp.factor(sp.Matrix([list(n.T) + [dd] for n, dd in rows]).det())
dets = set(); planes = [(n, 1) for n in Nc] + [(v, mu / sp.sqrt(3)) for v in Vc]
for quad in itertools.combinations(range(14), 4):
    D = conc_det([planes[i] for i in quad])
    if D != 0: dets.add(D)
degs = {sp.degree(sp.numer(sp.together(D)), mu) for D in dets}
roots = sorted({r for D in dets for r in sp.solve(D, mu)})
check(f'cube line: every concurrency determinant of 4 of its 14 planes is of degree <= 1 in mu: degrees {sorted(degs)}', degs <= {0, 1})
print(f'     their roots: {roots}')
check('cube line: the walls 1, 2, 3 are among the roots; the turn sends 1 -> 3, 2 -> 3/2', {1, 2, 3} <= set(roots))

# ------------------------------------------------------------------ B: the summit for regular P
print('B  the summit (regular P, DICTO\'s Turn Theorem)', flush=True)
s5, s2, s3 = sp.sqrt(5), sp.sqrt(2), sp.sqrt(3); phi = (1 + s5) / 2
R_ = sp.Rational
TAB = {  # squared flag radii h^2 .. R^2, stated peak, stated breaks (None = no break, a single value = the turn only)
 'dodecahedron': ([1 + 2 * s5 / 5, phi**2, 3], 10 - s5 - sp.sqrt(30 + 6 * s5)),
 'icosahedron': ([R_(7, 6) + s5 / 2, phi**2, phi + 2], 10 - s5 - sp.sqrt(30 + 6 * s5)),
 'cube': ([1, 2, 3], 5 - 2 * s3),
 'tetrahedron': ([R_(1, 3), 1, 3], 3),
 'octahedron': ([R_(1, 3), R_(1, 2), 1], 5 - 2 * s3),
 '5-cell': ([R_(1, 5), R_(8, 15), R_(6, 5), R_(16, 5)], R_(16, 5)),
 'tesseract': ([1, 2, 3, 4], 2),
 '16-cell': ([R_(1, 4), R_(1, 3), R_(1, 2), 1], 2),
 '24-cell': ([1, R_(4, 3), R_(3, 2), 2], 24 - 16 * s2),
 '600-cell': ([R_(7, 16) + 3 * s5 / 16, R_(1, 2) + s5 / 6, R_(5, 8) + s5 / 8, 1], 26 - 2 * s5 - 10 * s2 - 2 * sp.sqrt(10)),
 '120-cell': ([R_(7, 2) + 3 * s5 / 2, 4 + 8 * s5 / 5, R_(9, 2) + 3 * s5 / 2, 8], 26 - 2 * s5 - 10 * s2 - 2 * sp.sqrt(10)),
 '5-cube': ([1, 2, 3, 4, 5], 11 - 4 * s5),
 '5-orthoplex': ([R_(1, 5), R_(1, 4), R_(1, 3), R_(1, 2), 1], 11 - 4 * s5),
}
def same(a, b):
    return abs(sp.N(a - b, 60)) < sp.Float(10)**-50 and sp.minimal_polynomial(a, sp.Symbol('z')) == sp.minimal_polynomial(b, sp.Symbol('z'))
def closed(nodes, m):
    """h^2 t_min at mu = m (float), the closed form of part 2"""
    nodes = [float(x) for x in nodes]; h2, R2 = nodes[0], nodes[-1]; c = h2 * R2; m2 = c / m
    for r, A in zip(nodes, nodes[1:]):
        if r <= m <= A and r <= m2 <= A: return r + (m - r) * (m2 - r) / (A - r)
    return min(m, m2)
for P, (nodes, peak) in TAB.items():
    h2, R2 = nodes[0], nodes[-1]; c = sp.nsimplify(h2 * R2) if False else sp.simplify(h2 * R2); sc = sp.sqrt(c)
    hop = None
    for r, A in zip(nodes, nodes[1:]):
        if sp.N(r - sc, 50) < 0 < sp.N(A - sc, 50): hop = (r, A)
    if hop is None:
        val = sc / h2; where = 'node'
    else:
        r, A = hop; val = (r + (sc - r)**2 / (A - r)) / h2; where = 'hop'
    check(f'{P}: peak at mu = hR ({where}) = {sp.N(val, 12)} equals the stated {peak}', same(sp.simplify(val), sp.simplify(peak)))
    xs = np.exp(np.linspace(math.log(float(h2)) + 1e-6, math.log(float(R2)) - 1e-6, 4001))
    ys = np.array([closed(nodes, x) for x in xs]) / float(h2); ly = np.log(ys); lx = np.log(xs)
    sl = np.diff(ly) / np.diff(lx)
    k = int(np.argmax(ys))
    check(f'{P}: float scan of the closed form: argmax {xs[k]:.6f} vs hR {float(sc):.6f}, concave in log mu, symmetric',
          abs(xs[k] - float(sc)) / float(sc) < 2e-3 and np.all(np.diff(sl) <= 1e-7) and max(abs(np.interp(math.log(float(c)) - lx, lx, ly) - ly)) < 1e-6)
for dd in range(2, 9):
    m = math.isqrt(dd); nodes = list(range(1, dd + 1)); sc = sp.sqrt(dd)
    hop = [(r, A) for r, A in zip(nodes, nodes[1:]) if r < sc < A]
    val = sc if not hop else hop[0][0] + (sc - hop[0][0])**2 / (hop[0][1] - hop[0][0])
    check(f'd-cube corollary d = {dd}: peak m + (sqrt d - m)^2 = {sp.N(m + (sc - m)**2, 10)}', sp.simplify(val - (m + (sc - m)**2)) == 0)
check('600-cell peak: -10 sqrt(7 + 3 sqrt5) - 2 sqrt5 + 2 sqrt(35 + 15 sqrt5) + 26 = 26 - 2 sqrt5 - 10 sqrt2 - 2 sqrt10',
      same(-10 * sp.sqrt(7 + 3 * s5) - 2 * s5 + 2 * sp.sqrt(35 + 15 * s5) + 26, 26 - 2 * s5 - 10 * s2 - 2 * sp.sqrt(10)))
# breaks of t_min on the cube line: mu1 = max(r, c/A), mu2 = min(A, c/r) with [r, A] = [1, 2]
check('cube line: t_min breaks at the turned pair 3/2, 2 (product c = 3)', max(1, R_(3, 2)) == R_(3, 2) and min(2, 3) == 2)

# ------------------------------------------------------------------ C: the cuboctahedron example
print('C  antipol and polar of the cuboctahedron', flush=True)
def int_corners(planes):
    pts = set()
    for tri in itertools.combinations(planes, 3):
        M = sp.Matrix([list(n) for n, _ in tri]); b = sp.Matrix([dd for _, dd in tri])
        if M.det() == 0: continue
        x = M.solve(b)
        if all((sp.Matrix(n).T * x)[0] <= dd for n, dd in planes): pts.add(tuple(x))
    return pts
cube = [(e, 1) for e in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
def Sline(m): return cube + [(v, m) for v in itertools.product((1, -1), repeat=3)]   # v^.x <= mu/R with v = (+-1,+-1,+-1)
CO = int_corners(Sline(2)); TO = int_corners(Sline(R_(3, 2)))
check('S(2) is the cuboctahedron (12 corners, permutations of (+-1, +-1, 0))', CO == {p for q in itertools.product((1, -1), repeat=2) for p in set(itertools.permutations((q[0], q[1], 0)))})
want_TO = {p for s in itertools.product((1, -1), repeat=2) for p in set(itertools.permutations((s[0], s[1] * R_(1, 2), 0)))}
check('S(3/2) has the 24 corners (+-1, +-1/2, 0) permuted: the uniform truncated octahedron', TO == want_TO and len(TO) == 24)
# antipol of S(2): normals e_i at 1 stay at 1; normals (+-1,+-1,+-1)/sqrt3 at 2/sqrt3 go to sqrt3/2, i.e. +-x+-y+-z <= 3/2: S(3/2)
check('antipol of S(2): distances 1 -> 1 and 2/sqrt3 -> sqrt3/2, i.e. the planes of S(3/2) (h = 1, c = 3, turn 2 -> 3/2)', sp.simplify(1 / (2 / s3) * s3) == R_(3, 2))
RD = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)} | {tuple(R_(x, 2) for x in v) for v in itertools.product((1, -1), repeat=3)}
# polar of S(2) = conv{n/d}: e_i / 1 and (v/sqrt3)/(2/sqrt3) = v/2
polar_pts = {tuple(sp.Rational(x, 1) for x in n) for n, _ in cube} | {tuple(sp.Rational(x, 2) for x in v) for v in itertools.product((1, -1), repeat=3)}   # n_i/h_i: e_i/1, (v/sqrt3)/(2/sqrt3)
check('polar of S(2) = conv{n_i/h_i} = conv{(+-1,0,0) perms, (+-1/2,+-1/2,+-1/2)}: the rhombic dodecahedron', polar_pts == RD)
# feet hull of S(3/2): feet h_i n_i = e_i and (3/2)/sqrt3 * v/sqrt3 = v/2: the same 14 points
feet = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)} | {tuple(R_(3, 2) * x / 3 for x in v) for v in itertools.product((1, -1), repeat=3)}
check('feet hull of S(3/2) has the same 14 points as the polar of S(2) (rhombic dodecahedron); the antipol is not the polar', feet == RD and TO != RD)

# ------------------------------------------------------------------ D: the Ammann-Beenker line
print('D  the Ammann-Beenker line', flush=True)
t = sp.symbols('t', positive=True)
eps = lambda s: [sp.Matrix([-s, s]), sp.Matrix([1, 0]), sp.Matrix([-s, -s]), sp.Matrix([0, 1])]
Rot = sp.Matrix([[1, -1], [1, 1]]) / s2
Mt = Rot / (s2 * t)                                    # = [[1,-1],[1,1]]/(2t): rational for rational t
phys = [sp.Matrix([sp.cos(k * sp.pi / 4), sp.sin(k * sp.pi / 4)]) for k in range(4)]
sig = [1, 1, 1, -1]                                    # Rot e_k = sig_k e_{k+1 mod 4}
check('physical: Rot45 e_k = sig_k e_{k+1}, sig = (+,+,+,-)', all(sp.simplify(Rot * phys[k] - sig[k] * phys[(k + 1) % 4]) == sp.zeros(2, 1) for k in range(4)))
E, E2 = eps(t), eps(1 / (2 * t))
check('internal: -M eps_k(t) = sig_k eps_{k+1}(1/(2t)) with the SAME signs (M = Rot45/(sqrt2 t)): one lattice map A of Z^4',
      all(sp.simplify(-Mt * E[k] - sig[k] * E2[(k + 1) % 4]) == sp.zeros(2, 1) for k in range(4)))
check('negative control: +M (no sign) does not match the physical signs', not all(sp.simplify(Mt * E[k] - sig[k] * E2[(k + 1) % 4]) == sp.zeros(2, 1) for k in range(4)))
check('A has det +-1 (a lattice automorphism)', abs(sp.Matrix(4, 4, lambda i, j: sig[j] if i == (j + 1) % 4 else 0).det()) == 1)
check('the turn t -> 1/(2t) has the single positive fixed point 1/sqrt2', sp.solve(sp.Eq(t, 1 / (2 * t)), t) == [1 / s2])
a = 1 / s2; star_AB = [sp.Matrix([1, 0]), sp.Matrix([-a, -a]), sp.Matrix([0, 1]), sp.Matrix([a, -a])]   # Galois twist of e_0..e_3
L = sp.Matrix([[-a, -a], [a, -a]])
check('t = 1/sqrt2: eps(t) = L * (Galois-twisted physical star), L a rotation by 135 degrees: the Ammann-Beenker scheme',
      all(sp.simplify(L * star_AB[k] - E[k].subs(t, a)) == sp.zeros(2, 1) for k in range(4)) and sp.simplify(L.T * L) == sp.eye(2) and sp.simplify(L.det()) == 1)
def canon(st):
    b = tuple(st); best = None
    for r in range(8):
        for s_ in (1, -1):
            cc_ = tuple(b[(s_ * dd + r) % 8] for dd in range(8))
            if best is None or cc_ < best: best = cc_
    return ''.join('1' if x else '0' for x in best)
def freqs(tt):
    Ev = [(-tt, tt), (Fr(1), Fr(0)), (-tt, -tt), (Fr(0), Fr(1))]; W = zonogon(Ev); A_ = area(W); out = {}
    for P, st in arrangement(W, Ev):
        cname = canon(st); out[cname] = out.get(cname, 0) + area(P) / A_
    return out
pairs = [(Fr(2, 3), Fr(3, 4)), (Fr(5, 7), Fr(7, 10)), (Fr(12, 17), Fr(17, 24)), (Fr(29, 41), Fr(41, 58))]
for p, q in pairs:
    fa, fb = freqs(p), freqs(q)
    check(f'Pell pair {p} <-> {q} (= 1/(2t)): {len(fa)} vertex stars, frequencies identical (exact); distances from 1/sqrt2 {float(p) - 2**-.5:+.5f}, {float(q) - 2**-.5:+.5f}', fa == fb and q == 1 / (2 * p))
# tile level
def Mrat(tt): return [[1 / (2 * tt), -1 / (2 * tt)], [1 / (2 * tt), 1 / (2 * tt)]]
def epsr(tt): return [(-tt, tt), (Fr(1), Fr(0)), (-tt, -tt), (Fr(0), Fr(1))]
def accept(tt, gam, N):
    Ev = epsr(tt); W = zonogon(Ev); H = halfplanes(W); acc = set(); onb = 0
    for n in itertools.product(range(-N, N + 1), repeat=4):
        y = (sum(n[k] * Ev[k][0] for k in range(4)) - gam[0], sum(n[k] * Ev[k][1] for k in range(4)) - gam[1])
        s = [cross(sub(b, a_), sub(y, a_)) for a_, b in H]
        if min(s) > 0: acc.add(n)
        elif min(s) == 0 and all(x >= 0 for x in s): onb += 1
    return acc, onb
def Amap(n): return (-n[3], n[0], n[1], n[2])          # n'_{k+1} = sig_k n_k
random.seed(11)
for p, q in [(Fr(2, 3), Fr(3, 4)), (Fr(5, 7), Fr(7, 10))]:
    gam = (Fr(random.randint(1, 10**6), 10**6 + 3), Fr(random.randint(1, 10**6), 10**6 + 7))
    M = Mrat(p); mg = (-(M[0][0] * gam[0] + M[0][1] * gam[1]), -(M[1][0] * gam[0] + M[1][1] * gam[1]))
    e0 = epsr(q)[0]; gam2 = (mg[0] - e0[0], mg[1] - e0[1])
    N = 5
    A1, b1 = accept(p, gam, N); A2, b2 = accept(q, gam2, N)
    check(f'tile level t = {p}: {len(A1)} accepted lattice points in the box |n_k| <= {N}, none on the window boundary; '
          f'n accepted at (t, gamma) iff A n accepted at ({q}, gamma\') (exact)', b1 == 0 and b2 == 0 and len(A1) > 50 and {Amap(n) for n in A1} == A2)
    A3, _ = accept(q, mg, N)
    check(f'negative control: without the shift -eps_0, gamma\' = -M gamma, the sets differ ({len(A3 ^ {Amap(n) for n in A1})} points)', A3 != {Amap(n) for n in A1})
    A4, _ = accept(q + Fr(1, 100), gam2, N)
    check(f'negative control: at 1/(2t) + 1/100 the sets differ', A4 != {Amap(n) for n in A1})
# physical rotation through the lattice map
xs_ = lambda n: sum((n[k] * phys[k] for k in range(4)), sp.zeros(2, 1))
nn = sp.symbols('n0:4')
check('physical: x(A n) = Rot45 x(n) for every n (symbolic)', sp.simplify(xs_(Amap(nn)) - Rot * xs_(nn)) == sp.zeros(2, 1))
# edge directions and squares per rhombus on 10 distinct slopes
okE = True
slopes = [Fr(11, 20), Fr(3, 5), Fr(2, 3), Fr(7, 10), Fr(5, 7), Fr(12, 17), Fr(17, 24), Fr(3, 4), Fr(4, 5), Fr(9, 10)]
for tt in slopes:
    Ev = epsr(tt); W = zonogon(Ev); A_ = area(W); e = [Fr(0)] * 4
    for P, st in arrangement(W, Ev):
        f = area(P) / A_
        for dd in range(8):
            if st[dd]: e[dd % 4] += f
    want = [1 + 2 * tt, 2 * tt + 2 * tt * tt, 1 + 2 * tt, 2 * tt + 2 * tt * tt]
    okE &= all(e[k] * want[0] == e[0] * want[k] for k in range(4))
check(f'edge directions in the ratio (1+2t) : (2t+2t^2) : (1+2t) : (2t+2t^2), exact, on {len(set(slopes))} distinct slopes 11/20 .. 9/10', okE and len(set(slopes)) == 10)
f = (1 + 2 * t**2) / (4 * t)
check('squares per rhombus f(t) = (1+2t^2)/(4t): f(1/(2t)) = f(t), f\' = 0 only at 1/sqrt2, f(1/sqrt2) = 1/sqrt2',
      sp.simplify(f.subs(t, 1 / (2 * t)) - f) == 0 and sp.solve(sp.diff(f, t), t) == [1 / s2] and sp.simplify(f.subs(t, 1 / s2) - 1 / s2) == 0)
check('window area of the complementary pairs: 1 (axis squares) + 2t^2 (diagonal squares) + 4 t (rhombi) = area of the octagon W(t)',
      all(area(zonogon(epsr(tt))) == 1 + 2 * tt * tt + 4 * tt for tt in slopes))
print('FINAL ok' if OK else 'FINAL FAIL')
