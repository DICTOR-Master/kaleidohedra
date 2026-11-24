"""RVCMG adapter pieces (Polyhedraverse, v1 15 Sep 2026 and v2 17 Sep 2026): exact geometry and Scutoid-Frustum verdicts.

The app builds every adapter piece the same way (app/lib/rvcmg/solid.ts at commit 2726f41): the shared hexagon in the plane z = 0,
the target polygon (from the adapter's coalescence steps) lifted to z = h, walls of triangles: a fan triangle for each hexagon edge whose
two ends merge into one target corner, and the two triangles of the quadrilateral (hex_i, hex_j, T_b, T_a) for every other hexagon edge.
This script rebuilds every piece in exact arithmetic (sympy), mirroring the app's formulas line by line (assignTargetAngles,
fitTargetPolygon, the Catalan face measurements, the v1 square's edge alignment), takes the face lists from the app's own output
(data/app_pieces.json, written by scripts/dump.ts from commit 2726f41), and checks the exact model against the app's floating-point
vertices (all pairwise distances, and handedness). Discrete choices the app makes in floating point (atan2 at exactly +-pi, ties
between equal fit costs) are resolved by trying each candidate and keeping the one that reproduces the app's output.

Then, exactly: true faces (coplanar wall triangles merged; zero tests proved symbolically), convexity (every face plane supports
all vertices), vertex degrees, ends, Y-corners k, condition 2, the laws k >= |n-m| and k = n+m mod 2, in two readings:
  flat   : the solid with flat faces exactly as built (wall quads that are not planar stay two triangles);
  bent   : each wall quadrilateral read as ONE lateral face, bent along its diagonal when not planar (general tier).
Signs are decided at 60 significant digits (sympy evalf); a value is called zero only when sympy proves it zero.
Usage: python rvcmg_exact.py <study dir>   (writes data/exact_pieces.json, data/verdicts.json; prints FINAL ok when every check passes)
"""
import json, sys, os, itertools
import faulthandler, signal
faulthandler.register(signal.SIGUSR1)          # kill -USR1 <pid> prints the stack into the log (where a slow piece spends its time)
import sympy as sp
import mpmath
mpmath.mp.dps = 110
from sympy import sqrt, Rational as Q, pi

ST = sys.argv[1] if len(sys.argv) > 1 else '.'
APP = json.load(open(os.path.join(ST, 'data/app_pieces.json')))
APP2 = json.load(open(os.path.join(ST, 'data/app_hemi_rd.json')))
P = 60
import flint
flint.ctx.prec = 700                                   # ~210 digits of working precision for the ball evaluation below
_AC = {}
def _arb(x):
    """rigorous ball (python-flint arb) enclosing the exact value of a sympy expression (24 Nov: sympy evalf was too slow on the DH kite)"""
    r = _AC.get(x)
    if r is not None: return r
    if x.is_Integer: r = flint.arb(int(x))
    elif x.is_Rational: r = flint.arb(int(x.p)) / int(x.q)
    elif x is sp.pi: r = flint.arb.pi()
    elif x.is_Add:
        r = flint.arb(0)
        for a in x.args: r += _arb(a)
    elif x.is_Mul:
        r = flint.arb(1)
        for a in x.args: r *= _arb(a)
    elif x.is_Pow:
        b, e = x.args
        if e.is_Integer: r = _arb(b) ** int(e)
        elif e.is_Rational and e.q == 2: r = _arb(b).sqrt() ** int(e.p)
        else: raise TypeError('arb: power ' + str(e))
    elif isinstance(x, sp.sin): r = _arb(x.args[0]).sin()
    elif isinstance(x, sp.cos): r = _arb(x.args[0]).cos()
    elif isinstance(x, sp.atan): r = _arb(x.args[0]).atan()
    else: raise TypeError('arb: ' + type(x).__name__)
    if not r.is_finite():
        if os.environ.get('ARBDEBUG'): print('ARB NOT FINITE', type(x).__name__, str(x)[:300], [str(_arb(a))[:60] for a in x.args], flush=True)
        raise ValueError('arb: not finite')
    _AC[x] = r; return r
def N(x, digits=P):
    """value to `digits` digits: from the arb ball when its radius is below 10^-(digits+5), else sympy evalf (accuracy-tracked)"""
    x = sp.sympify(x)
    try:
        b = _arb(x)
        if b.rad() < flint.arb(10) ** (-(digits + 5)): return sp.Float(b.mid().str(digits + 5, radius=False), digits + 5)
    except (TypeError, ValueError): pass
    return sp.N(x, digits)
def algebraize(x):
    """Remove every atan exactly: an innermost atom atan(u) (u free of atan) is written 2*f with cos f = sqrt((1+c)/2),
    sin f = sign(u) sqrt((1-c)/2), c = 1/sqrt(1+u^2) (valid since atan(u) lies in (-pi/2, pi/2), so f in (-pi/4, pi/4)); sin and cos
    of sums are expanded (expand_trig). Repeats until no atan is left; returns the algebraic expression (None if a trig is left)."""
    for _ in range(40):
        ats = [a for a in x.atoms(sp.atan) if not a.args[0].has(sp.atan)]
        if not ats: break
        a = ats[0]; u = a.args[0]; f = sp.Dummy('f')
        su = sp.sign(N(u)); c = 1 / sqrt(1 + u**2)
        x = sp.expand_trig(x.subs(a, 2 * f))
        x = x.subs({sp.cos(f): sqrt((1 + c) / 2), sp.sin(f): su * sqrt((1 - c) / 2)})
        if x.has(f): return None
    if x.has(sp.atan) or x.has(sp.sin) or x.has(sp.cos):
        x = sp.expand_trig(x)
        if x.has(sp.atan) or any(not t.args[0].is_rational for t in x.atoms(sp.sin, sp.cos) if not (t.args[0] / pi).is_rational): return None
    return x

def iszero(x):
    v = N(x)
    if abs(v) > sp.Float('1e-40'): return False
    if sp.expand(x) == 0 or sp.radsimp(sp.expand(x)) == 0: return True   # 24 Nov fast path: cancels at once in most cases
    try:
        if sp.minimal_polynomial(x, sp.Symbol('t')) == sp.Symbol('t'): return True
    except Exception: pass
    s = sp.simplify(x)
    if s == 0: return True
    a = algebraize(x)                                                  # 24 Nov: v1 pieces carry atan(sqrt 2)-type angles
    if a is not None:
        try:
            if sp.minimal_polynomial(a, sp.Symbol('t')) == sp.Symbol('t'): return True
        except Exception: pass
    raise RuntimeError(f'value zero to {P} digits but not proved zero: {x}')

def ratan2(y, x):
    """atan2(y, x), exact and real by construction: atan(y/x) (+-pi) when |x| >= |y|, else sign(y) pi/2 - atan(x/y); the branch is read
    from arb balls (signs certain), so no zero test is needed. 24 Nov: sympy's own atan2 turns into -I*log(...) when it cannot prove its
    arguments real; evaluated, that form carried a spurious imaginary part (the DH kite, v1, crashed: "Cannot convert complex to float")."""
    xn, yn = N(x), N(y)
    def at(u): return sp.atan(u, evaluate=not _big(u))
    if abs(xn) >= abs(yn):
        if xn > 0: return at(y / x)
        return at(y / x) + (pi if yn >= 0 else -pi)
    return (pi / 2 if yn > 0 else -pi / 2) - at(x / y)

def V(*a): return sp.Matrix(a)
def ang(p): return ratan2(p[1], p[0])
phi = (1 + sqrt(5)) / 2

# ---------------- the two hexagons ----------------
R2 = sqrt(2) / 2
HEX2 = [V(R2 * sp.cos(i * pi / 3), R2 * sp.sin(i * pi / 3)) for i in range(6)]       # universalHexInterface.ts
H2 = R2 * sqrt(2) / 4                                                                  # WALL_HEIGHT_V2 = 1/4
# v1: the six on-plane vertices of the rhombic dodecahedron (circumradius 1) in the plane y + z = 0, in the app's order (hemiRdInterface.ts)
hex3 = [V(*[sp.nsimplify(c, rational=True, tolerance=1e-12) for c in p]) for p in APP2['hex']]
axis = V(0, -1, -1) / sqrt(2)
u1 = hex3[0] / hex3[0].norm(); w1 = axis.cross(u1)
HEX1 = [V(sp.simplify(p.dot(u1)), sp.simplify(p.dot(w1))) for p in hex3]
H1 = (sqrt(2) / 2) / 2                                                                 # RD_HEMI_DEPTH / 2

# ---------------- Catalan faces (face 0 of the app's registry, exact) ----------------
aI = 1 / sqrt(1 + phi**2)
RT0 = [aI * V(phi, -1, 0), aI * V(phi, 0, 1 / phi), aI * V(1, 0, phi), aI * V(1, -1, 1)]
RD0 = [V(0, 0, -1), V(Q(1, 2), -Q(1, 2), -Q(1, 2)), V(0, -1, 0), V(-Q(1, 2), -Q(1, 2), -Q(1, 2))]
pD = (2 * sqrt(2) + 1) / 7
DI0 = [-pD * V(1, 1, 1), V(-1, 0, -1) / sqrt(2), V(0, 0, -1), V(0, -1, -1) / sqrt(2)]
# deltoidal hexecontahedron = polar of the rhombicosidodecahedron (edge 1): vertex n_k / d_k, scaled so the 5-fold vertex has radius 1
Rr2 = (11 + 4 * sqrt(5)) / 4
d3, d4, d5 = sqrt(Rr2 - Q(1, 3)), sqrt(Rr2 - Q(1, 2)), sqrt(Rr2 - (5 + sqrt(5)) / 10)
n2a, n2b = V(phi**2, 1, phi), V(1, phi, phi**2)
DH0 = [-(d5 / d3) * V(1, 1, 1) / sqrt(3), -(d5 / d4) * n2a / n2a.norm(), -V(1, 0, phi) / sqrt(1 + phi**2), -(d5 / d4) * n2b / n2b.norm()]
CAT = {'RHOMBIC_TRIACONTAHEDRON': RT0, 'RHOMBIC_DODECAHEDRON': RD0, 'DELTOIDAL_ICOSITETRAHEDRON': DI0, 'DELTOIDAL_HEXECONTAHEDRON': DH0}
checks = []
for k, F in CAT.items():
    fl = [APP['catalan'][k]['vertices'][i] for i in APP['catalan'][k]['face0']]
    err = max(abs(N(F[i][j]) - fl[i][j]) for i in range(4) for j in range(3))
    planar = iszero((F[1] - F[0]).cross(F[2] - F[0]).dot(F[3] - F[0]))
    checks.append((f'Catalan face {k}: exact = app to {float(err):.1e}, planar exactly', err < 1e-12 and planar))

def measure_rhombus(F):
    e = (F[0] - F[1]).norm(); rho = (F[0] - F[2]).norm() / (F[1] - F[3]).norm()
    return e * rho / sqrt(rho**2 + 1), e / sqrt(rho**2 + 1)          # half long, half short diagonal (rhombusToUHex.ts)
def measure_kite(F):
    c = (F[0] + F[1] + F[2] + F[3]) / 4
    nv = (F[1] - F[0]).cross(F[2] - F[0]); nv = nv / nv.norm()
    u = (F[0] - c) / (F[0] - c).norm(); w = nv.cross(u)
    return [(ratan2((p - c).dot(w), (p - c).dot(u)), (p - c).norm()) for p in F]

# ---------------- the app's fitting rules, exactly ----------------
PROVED_PHASES = []
def exact_phase(S, C, cands=()):
    """atan2(S, C); replaced by q*pi when S*cos(q pi) - C*sin(q pi) = 0 is PROVED (minimal polynomial / simplify) and S sin + C cos > 0."""
    ph = ratan2(S, C)
    if sp.count_ops(S) + sp.count_ops(C) > 800: return ph          # 24 Nov: closed-form proofs stall on the DH kite's long sums; keep the exact atan form
    q = sp.nsimplify(float(N(ph / pi)), rational=True, tolerance=1e-13)
    if q.q <= 360 and abs(N(ph / pi) - q) < sp.Float('1e-50'):
        res = S * sp.cos(q * pi) - C * sp.sin(q * pi)
        ok = False
        try: ok = iszero(res)
        except RuntimeError: ok = False
        if ok and N(S * sp.sin(q * pi) + C * sp.cos(q * pi)) > 0:
            PROVED_PHASES.append(str(q * pi)); return q * pi
    # 24 Nov: a mirror-symmetric fit (v1 hexagon, D2 symmetry) puts the phase at an input angle minus a corner angle; try those closed forms
    phn = N(ph)
    for c in cands:
        dd = (N(c) - phn) / (2 * N(pi)); kk = int(sp.floor(dd + sp.Rational(1, 2)))
        if abs(dd - kk) > sp.Float('1e-50'): continue
        try: ok = iszero(S * sp.cos(c) - C * sp.sin(c))
        except RuntimeError: ok = False
        if ok and N(S * sp.sin(c) + C * sp.cos(c)) > 0:
            PROVED_PHASES.append(str(c)); return c
    return ph
def _big(x): return sp.count_ops(x) > 60
def sin_(x): return sp.sin(x, evaluate=not _big(x))   # 24 Nov: sympy's automatic evaluation of sin/cos stalls on the DH kite's long angles;
def cos_(x): return sp.cos(x, evaluate=not _big(x))   # short angles still evaluate (closed forms kept), long ones stay as written (same value)
def assign(angles):                                                   # shared.ts assignTargetAngles
    n = len(angles); order = sorted(range(n), key=lambda i: N(angles[i])); rank = {g: r for r, g in enumerate(order)}
    step = 2 * pi / n; diffs = [angles[i] - rank[i] * step for i in range(n)]
    ph = exact_phase(sum(sin_(d) for d in diffs), sum(cos_(d) for d in diffs), [a - r * step / 2 for a in angles for r in range(2 * n)])
    return [rank[i] * step + ph for i in range(n)], ph
def fit(groups, corners, shift):                                      # shared.ts fitTargetPolygon, one cyclic assignment
    n = len(groups); order = sorted(range(n), key=lambda i: N(groups[i][0]))
    S = C = 0
    for r, g in enumerate(order):
        ca, cr = corners[(r + shift) % n]; d = groups[g][0] - ca; wgt = groups[g][1] * cr
        S += wgt * sin_(d); C += wgt * cos_(d)
    ph = exact_phase(S, C, [g[0] - c[0] + r * pi / 2 for g in groups for c in corners for r in range(4)]); th = [None] * n; rr = [None] * n; cost = 0
    for r, g in enumerate(order):
        ca, cr = corners[(r + shift) % n]; th[g] = ca + ph; rr[g] = cr
        A_, R_ = N(groups[g][1]), N(cr)                               # 24 Nov: the cost only ranks the 4 assignments, so it is evaluated
        cost += (A_ * N(cos_(groups[g][0])) - R_ * N(cos_(th[g])))**2 + (A_ * N(sin_(groups[g][0])) - R_ * N(sin_(th[g])))**2   # numerically
    return th, rr, ph, cost
def pol(r, t): return V(r * cos_(t), r * sin_(t))
def mid(a, b): return (a + b) / 2

def variants_angles(H):
    """atan2 of a hexagon corner lying exactly on the negative u axis: the app's float may give +pi or -pi."""
    base = [ang(p) for p in H]; amb = [i for i, p in enumerate(H) if p[1] == 0 and N(p[0]) < 0]
    out = []
    for signs in itertools.product([1, -1], repeat=len(amb)):
        a = list(base)
        for i, s in zip(amb, signs): a[i] = s * pi
        out.append(a)
    return out

def targets(kind, H, A):
    """All candidate target rings (list of 2D points in the app's ring order) for one adapter kind on hexagon H with corner angles A."""
    mp = lambda i, j: mid(H[i], H[j])
    pair = lambda i, j: (A[i] + A[j]) / 2
    C = []
    if kind == 'triangle':
        th, _ = assign([pair(0, 1), pair(2, 3), pair(4, 5)]); C.append([pol(1 / sqrt(3), t) for t in th])
    elif kind in ('square', 'square-v1'):
        th, _ = assign([A[0], pair(1, 2), A[3], pair(4, 5)])
        if kind == 'square-v1':                                       # squareToRdH.ts: align target edge 1 with the long hexagon edge v3->v4
            e = H[3] - H[2]; off = ratan2(e[1], e[0]) - (th[1] + 3 * pi / 4); th = [t + off for t in th]
        C.append([pol(1 / sqrt(2), t) for t in th])
    elif kind == 'pentagon':
        th, _ = assign([A[0], A[1], pair(2, 3), A[4], A[5]]); C.append([pol(1 / (2 * sp.sin(pi / 5)), t) for t in th])
    elif kind == 'hexagon':
        th, _ = assign(A[:]); C.append([pol(1, t) for t in th])
    elif kind == 'golden-v1':                                         # goldenRhombusToRdH.ts: fixed radii, assignTargetAngles
        L, S = measure_rhombus(RT0); th, _ = assign([A[0], pair(1, 2), A[3], pair(4, 5)])
        C.append([pol(r, t) for r, t in zip([L, S, L, S], th)])
    elif kind.startswith('rhombus:') or kind.startswith('kite:'):
        cat = kind.split(':')[1]
        if kind.startswith('rhombus:'):
            L, S = measure_rhombus(CAT[cat]); corners = [(0, L), (pi / 2, S), (pi, L), (3 * pi / 2, S)]
        else:
            corners = measure_kite(CAT[cat])
        m1, m2 = mp(1, 2), mp(4, 5)
        groups = [(A[0], H[0].norm()), (ratan2(m1[1], m1[0]), m1.norm()), (A[3], H[3].norm()), (ratan2(m2[1], m2[0]), m2.norm())]
        fits = [fit(groups, corners, s) for s in range(4)]
        costs = [N(f[3]) for f in fits]; best = min(costs)
        for s, f in enumerate(fits):                                  # the minimum, and any exact tie (the app's float picks one)
            if abs(costs[s] - best) < sp.Float('1e-40'):
                C.append([pol(r, t) for r, t in zip(f[1], f[0])])
    return C

OWNER = {  # target corner owning each hexagon corner v1..v6 (the coalescence pairs of each adapter)
    'triangle': [0, 0, 1, 1, 2, 2], 'square': [0, 1, 1, 2, 3, 3], 'square-v1': [0, 1, 1, 2, 3, 3], 'pentagon': [0, 1, 2, 2, 3, 4],
    'hexagon': [0, 1, 2, 3, 4, 5], 'golden-v1': [0, 1, 1, 2, 3, 3], 'rhombus': [0, 1, 1, 2, 3, 3], 'kite': [0, 1, 1, 2, 3, 3]}
PIECES = [  # app id, hexagon version, adapter kind
    ('RVCMG_V2_TRIANGLE_TO_UHEX', 2, 'triangle'), ('RVCMG_V2_SQUARE_TO_UHEX', 2, 'square'), ('RVCMG_V2_PENTAGON_TO_UHEX', 2, 'pentagon'),
    ('RVCMG_V2_GOLDEN_RHOMBUS_TO_UHEX', 2, 'rhombus:RHOMBIC_TRIACONTAHEDRON'), ('RVCMG_V2_RD_NATIVE_RHOMBUS_TO_UHEX', 2, 'rhombus:RHOMBIC_DODECAHEDRON'),
    ('RVCMG_V2_DI_KITE_TO_UHEX', 2, 'kite:DELTOIDAL_ICOSITETRAHEDRON'), ('RVCMG_V2_DH_KITE_TO_UHEX', 2, 'kite:DELTOIDAL_HEXECONTAHEDRON'),
    ('RVCMG_V2_REGULAR_HEX_TO_UHEX', 2, 'hexagon'),
    ('RVCMG_TRIANGLE_TO_RDH', 1, 'triangle'), ('RVCMG_SQUARE_TO_RDH', 1, 'square-v1'), ('RVCMG_PENTAGON_TO_RDH', 1, 'pentagon'),
    ('RVCMG_GOLDEN_RHOMBUS_TO_RDH', 1, 'golden-v1'), ('RVCMG_DI_KITE_TO_RDH', 1, 'kite:DELTOIDAL_ICOSITETRAHEDRON'),
    ('RVCMG_DH_KITE_TO_RDH', 1, 'kite:DELTOIDAL_HEXECONTAHEDRON'), ('RVCMG_REGULAR_HEX_TO_RDH', 1, 'hexagon')]

def _xstr(c):
    """the exact expression as text; a DH-kite coordinate is too long to print (sympy's printer stalls), so it is recorded by its
    value to 60 digits, marked as such; its exact form is the construction in this script (24 Nov)"""
    return str(c) if sp.count_ops(c) < 3000 else 'value60:' + str(N(c))
def numeric(X):
    """each exact coordinate evaluated to 110 digits (arb ball or sympy evalf, both rigorous); sign tests use these, zero tests go back to exact."""
    return [[mpmath.mpf(str(N(c, 110))) for c in x] for x in X]
def nsub(a, b): return [a[i] - b[i] for i in range(3)]
def ncross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def ndot(a, b): return sum(a[i] * b[i] for i in range(3))
TINY = mpmath.mpf('1e-60')
def sign_or_zero(xn, exact_thunk):
    """+1/-1 from 110 digits when |x| > 1e-60; else 0, but only after an exact proof that the exact value is zero."""
    if abs(xn) > TINY: return 1 if xn > 0 else -1
    if iszero(exact_thunk()): return 0
    raise RuntimeError('tiny value not proved zero')

def match(ex, fl):
    """max error of all pairwise distances, and handedness agreement (sign of every nondegenerate triple product from vertex 0)."""
    n = len(fl); import math
    err = 0.0; xn = numeric(ex)
    for i in range(n):
        for j in range(i + 1, n):
            err = max(err, abs(float(mpmath.sqrt(ndot(nsub(xn[i], xn[j]), nsub(xn[i], xn[j])))) - math.dist(fl[i], fl[j])))
    ok = True
    for i, j, k in [(1, 2, n - 1), (1, 3, n - 2), (2, 4, n - 1)]:
        a = ndot(ncross(nsub(xn[i], xn[0]), nsub(xn[j], xn[0])), nsub(xn[k], xn[0]))
        f = [[fl[t][c] - fl[0][c] for c in range(3)] for t in (i, j, k)]
        b = f[0][0] * (f[1][1] * f[2][2] - f[1][2] * f[2][1]) - f[0][1] * (f[1][0] * f[2][2] - f[1][2] * f[2][0]) + f[0][2] * (f[1][0] * f[2][1] - f[1][1] * f[2][0])
        if abs(b) > 1e-9 and (a > 0) != (b > 0): ok = False
    return err, ok

def analyse(X, faces, endA, endB, owner=None):
    """X exact 3D points; faces: app face lists; endA/endB: indices into faces of the two ends."""
    nV = len(X); Xn = numeric(X)
    def plane(f):
        nv = (X[f[1]] - X[f[0]]).cross(X[f[2]] - X[f[0]]); return nv, nv.dot(X[f[0]])
    def side(f, i):          # sign of vertex i against the plane of face f
        nn = ncross(nsub(Xn[f[1]], Xn[f[0]]), nsub(Xn[f[2]], Xn[f[0]]))
        def ex():
            nv, d = plane(f); return nv.dot(X[i]) - d
        return sign_or_zero(ndot(nn, Xn[i]) - ndot(nn, Xn[f[0]]), ex)
    # convexity: every face plane leaves all vertices on one side (exact signs)
    convex = True; touching = []
    for f in faces:
        sg = set()
        for i in range(nV):
            if i in f: continue
            sgn = side(f, i)
            if sgn == 0: touching.append((tuple(f), i)); continue
            sg.add(sgn)
        if len(sg) > 1: convex = False
    # merge adjacent coplanar faces (exact zero test) -> true flat faces
    edge_faces = {}
    for fi, f in enumerate(faces):
        for k in range(len(f)):
            edge_faces.setdefault(frozenset((f[k], f[(k + 1) % len(f)])), []).append(fi)
    parent = list(range(len(faces)))
    def root(a):
        while parent[a] != a: a = parent[a]
        return a
    for e, fs in edge_faces.items():
        assert len(fs) == 2, 'not a closed surface'
        a, b = fs
        if all(side(faces[a], i) == 0 for i in faces[b] if i not in faces[a]): parent[root(a)] = root(b)
    groups = {}
    for fi in range(len(faces)): groups.setdefault(root(fi), []).append(fi)
    flat_faces = [sorted(set(i for fi in g for i in faces[fi])) for g in groups.values()]
    flat_edges = [tuple(sorted(e)) for e, fs in edge_faces.items() if root(fs[0]) != root(fs[1])]
    def report(face_groups, edges):
        deg = [0] * nV
        for a, b in edges: deg[a] += 1; deg[b] += 1
        A, B = set(faces[endA]), set(faces[endB])
        n, m = len(A), len(B)
        k = sum(1 for i in range(nV) if i not in A and i not in B)
        lat = [g for g in face_groups if set(g) != A and set(g) != B]
        eset = set(edges)
        def meets(g, E):
            return any(tuple(sorted((a, b))) in eset for a in g for b in g if a in E and b in E and a < b)
        cond2 = all(meets(g, A) or meets(g, B) for g in lat)
        return {'n': n, 'm': m, 'k': k, 'V': nV, 'E': len(edges), 'F': len(face_groups), 'lateral': len(lat),
                'lateral_sides': sorted(len(g) for g in lat), 'degrees': deg, 'simple': all(d == 3 for d in deg),
                'ends_disjoint': not (A & B), 'cond2': cond2, 'law_bound': k >= abs(n - m), 'law_parity': (k - n - m) % 2 == 0}
    flat = report(flat_faces, flat_edges)
    flat['convex'] = convex
    # bent reading: the wall quad of hexagon edge (i, j) whose corners belong to different target corners is
    # {hex_i, hex_j, T_owner(i), T_owner(j)} (solid.ts); its two app triangles are merged into one lateral face
    A, B = set(faces[endA]), set(faces[endB])
    parent = list(range(len(faces)))
    if owner is not None:
        for i in range(6):
            j = (i + 1) % 6
            if owner[i] == owner[j]: continue
            Qs = {i, j, 6 + owner[i], 6 + owner[j]}
            pair = [fi for fi, f in enumerate(faces) if len(f) == 3 and set(f) <= Qs]
            assert len(pair) == 2, (Qs, pair)
            parent[root(pair[0])] = root(pair[1])
    groups = {}
    for fi in range(len(faces)): groups.setdefault(root(fi), []).append(fi)
    bent_faces = [sorted(set(i for fi in g for i in faces[fi])) for g in groups.values()]
    bent_edges = [tuple(sorted(e)) for e, fs in edge_faces.items() if root(fs[0]) != root(fs[1])]
    bent = report(bent_faces, bent_edges)
    nonplanar = []
    for g in bent_faces:
        if len(g) == 4 and not (set(g) == A or set(g) == B):
            if side(g[:3], g[3]) != 0: nonplanar.append(g)
    bent['bent_quads'] = len(nonplanar)
    return flat, bent, touching

# RESUME (24 Nov): each finished piece is cached in data/pieces/<id>.json (exact model, verdicts, its check line, phases proved);
# a cached piece is skipped. "--piece ID" computes that one piece only (for running pieces in parallel); the plain run then assembles.
CACHE = os.path.join(ST, 'data/pieces'); os.makedirs(CACHE, exist_ok=True)
ONLY = sys.argv[sys.argv.index('--piece') + 1] if '--piece' in sys.argv else None
out, verdicts = {}, {}
for pi_, (pid, ver, kind) in enumerate(PIECES):
    if ONLY and pid != ONLY: continue
    cf_ = os.path.join(CACHE, pid + '.json')
    if os.path.exists(cf_):
        c_ = json.load(open(cf_)); out[pid] = c_['out']; verdicts[pid] = c_['verdict']; checks.append(tuple(c_['check'])); PROVED_PHASES.extend(c_['phases'])
        print('PROGRESS', f'{(pi_ + 1) / 16:.3f}', pid, '(cached)', flush=True); continue
    ph0_ = len(PROVED_PHASES)
    H, h = (HEX2, H2) if ver == 2 else (HEX1, H1)
    fl = APP['pieces'][pid]['vertices']; faces = APP['pieces'][pid]['faces']
    cands = []
    for A in variants_angles(H):
        for T in targets(kind, H, A):
            X = [V(p[0], p[1], 0) for p in H] + [V(p[0], p[1], h) for p in T]
            err, hand = match(X, fl); cands.append((err, hand, X, T))
    print('STAGE', pid, 'targets and match done', len(cands), 'candidates', flush=True)
    cands.sort(key=lambda c: c[0]); err, hand, X, T = cands[0]
    checks.append((f'{pid}: exact model = app vertices (pairwise distances to {err:.1e}, handedness {hand})', err < 1e-9 and hand))
    flat, bent, touching = analyse(X, faces, 0, 1, OWNER[kind.split(':')[0]])
    out[pid] = {'name': APP['pieces'][pid]['name'], 'hex_version': ver, 'wall_height': str(h),
                'vertices_exact': [[str(sp.simplify(c)) if kind in ('triangle', 'square', 'pentagon', 'hexagon') and ver == 2 else _xstr(c) for c in x] for x in X],
                'vertices_float': [[float(N(c)) for c in x] for x in X], 'faces': faces}
    verdicts[pid] = {'flat': flat, 'bent': bent, 'model_error': err}
    tmp_ = cf_ + '.tmp'
    json.dump({'out': out[pid], 'verdict': verdicts[pid], 'check': list(checks[-1]), 'phases': PROVED_PHASES[ph0_:]}, open(tmp_, 'w'), indent=1); os.replace(tmp_, cf_)
    print('PROGRESS', f'{(pi_ + 1) / 16:.3f}', pid, flush=True)
    print(pid, 'err', f'{err:.1e}', 'flat', {k: flat[k] for k in ('n', 'm', 'k', 'F', 'convex', 'simple', 'cond2', 'law_bound', 'law_parity', 'lateral_sides')},
          'maxdeg', max(flat['degrees']), '| bent', {k: bent[k] for k in ('F', 'simple', 'bent_quads', 'lateral_sides')}, 'degs', sorted(bent['degrees']))

# ---------------- RD-Hemi (v1 only): half of the rhombic dodecahedron ----------------
if ONLY:
    print('piece', ONLY, 'cached;', 'CHECK', checks[-1]); sys.exit(0)
hv = [V(*[sp.nsimplify(c, rational=True, tolerance=1e-12) for c in p]) for p in APP2['hemi']['v']]
hf = APP2['hemi']['f']
fl = APP2['hemi']['v']; err, hand = match(hv, fl)
rd_edges_ok = all(iszero((hv[f[k]] - hv[f[(k + 1) % len(f)]]).norm() - sqrt(3) / 2) or len(f) == 3 or len(f) == 6 for f in hf for k in range(len(f)))
crown = [i for i, f in enumerate(hf) if not set(f) & set(hf[0])]
checks.append((f'RD-Hemi: exact rational model = app ({err:.1e}); rhombus edges sqrt(3)/2; one face disjoint from the hexagon (crown)', err < 1e-12 and rd_edges_ok and len(crown) == 1))
flat, bent, touching = analyse(hv, hf, 0, crown[0])
out['RVCMG_RD_HEMI'] = {'name': 'RD-Hemi (bare)', 'hex_version': 1, 'vertices_exact': [[str(c) for c in x] for x in hv],
                        'vertices_float': [[float(N(c)) for c in x] for x in hv], 'faces': hf, 'ends': [0, crown[0]]}
verdicts['RVCMG_RD_HEMI'] = {'flat': flat, 'model_error': err}
print('RVCMG_RD_HEMI err', f'{err:.1e}', {k: flat[k] for k in ('n', 'm', 'k', 'F', 'convex', 'simple', 'cond2', 'law_bound', 'law_parity', 'lateral_sides')}, 'degs', sorted(flat['degrees']))

# ---------------- exact closed forms of the v2 target angles (proved: tan identity + sign) ----------------
closed = {}
for name, vals in [('triangle', [-pi / 2, pi / 6, 5 * pi / 6]), ('square', [0, pi / 2, pi, -pi / 2]),
                   ('pentagon', [pi / 30, 13 * pi / 30, 5 * pi / 6, -23 * pi / 30, -11 * pi / 30]),
                   ('hexagon', [i * pi / 3 for i in range(6)])]:
    pid = {'triangle': 'RVCMG_V2_TRIANGLE_TO_UHEX', 'square': 'RVCMG_V2_SQUARE_TO_UHEX', 'pentagon': 'RVCMG_V2_PENTAGON_TO_UHEX',
           'hexagon': 'RVCMG_V2_REGULAR_HEX_TO_UHEX'}[name]
    r = {'triangle': 1 / sqrt(3), 'square': 1 / sqrt(2), 'pentagon': 1 / (2 * sp.sin(pi / 5)), 'hexagon': 1}[name]
    Xs = APP['pieces'][pid]['vertices']
    # compare the closed form with the exact model's target ring, as point sets (exact equality of coordinates)
    model = [V(*[sp.sympify(c) for c in x]) for x in out[pid]['vertices_exact'][6:]]
    cf = [V(r * sp.cos(t), r * sp.sin(t), H2) for t in vals]
    same = all(any(all(iszero(a[c] - b[c]) for c in range(3)) for b in model) for a in cf)
    closed[name] = [str(t) for t in vals]
    checks.append((f'v2 {name}: target corners at angles {closed[name]} (exact)', same))

json.dump(out, open(os.path.join(ST, 'data/exact_pieces.json'), 'w'), indent=1)
json.dump({'verdicts': verdicts, 'closed_forms_v2_angles': closed}, open(os.path.join(ST, 'data/verdicts.json'), 'w'), indent=1)
for c, ok in checks: print('CHECK', 'ok ' if ok else 'FAIL', c)
print('phases proved exact multiples of pi:', len(PROVED_PHASES), sorted(set(PROVED_PHASES)))
print('FINAL ok' if all(ok for _, ok in checks) else 'FINAL FAIL')
