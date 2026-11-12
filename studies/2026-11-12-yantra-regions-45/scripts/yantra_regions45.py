"""Aim 2, chunk 5c lead (a) (12 Nov 2026): the canonical-form analysis of chunk 5c run on the 45-region yantras: Kulaichev's yantra
(degree 348) and Rh345 (3-4-5 rhombus, degree 20), with Q3 (3-4-5 rhombus, coordinates in Q(sqrt Delta)) as the EXACT 45-region instance,
and R1 (exact, 43 regions) as the reference pattern of the DICTO Yantra. Method: ../README.md and the 5c study.
Usage: python -u yantra_regions45.py [pilot]"""
import sys, os, json, math, time, itertools
from fractions import Fraction as Fr
from multiprocessing import get_context

PILOT = sys.argv[1:] == ['pilot']
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-12-yantra-regions-canonical', 'scripts'))
sys.path.insert(0, BASE)
import yantra_regions as B                                       # chunk 5c functions (arrangement, forms, grid, lemmas)
from yantra_regions import (Ctx, det2, sub, vertex_form, fan_form, polar_area2, area2, arrangement, triangle_V, intersections, grid,
                            interpolate, deriv_at, Lval, Pts, line_of, parse_poly, poly_sign_at, SRI, GRID)
DSTAR = '0.745996537184295181585859787277476212880247765'          # rhombus threshold u* (sri-yantra study, 10 Nov)


# ---------------------------------------------------------------- exact arithmetic in Q(sqrt D)
class QF:
    """a + b sqrt(D), a, b Fractions; D a positive non-square Fraction (class attribute). Exact sign by a^2 vs b^2 D."""
    __slots__ = ('a', 'b')
    D = None

    def __init__(self, a, b=0):
        self.a = Fr(a); self.b = Fr(b)

    @staticmethod
    def of(x):
        return x if isinstance(x, QF) else QF(x, 0)

    def __add__(s, o): o = QF.of(o); return QF(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = QF.of(o); return QF(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return QF.of(o) - s
    def __neg__(s): return QF(-s.a, -s.b)
    def __mul__(s, o):
        if isinstance(o, QF): return QF(s.a * o.a + s.b * o.b * QF.D, s.a * o.b + s.b * o.a)
        o = Fr(o); return QF(s.a * o, s.b * o)
    __rmul__ = __mul__
    def __truediv__(s, o):
        if not isinstance(o, QF): o = Fr(o); return QF(s.a / o, s.b / o)
        n = o.a * o.a - o.b * o.b * QF.D
        return QF((s.a * o.a - s.b * o.b * QF.D) / n, (s.b * o.a - s.a * o.b) / n)
    def __rtruediv__(s, o): return QF.of(o) / s
    def __pow__(s, k):
        r = QF(1); x = s
        while k:
            if k & 1: r = r * x
            x = x * x; k >>= 1
        return r
    def sign(s):
        sa = (s.a > 0) - (s.a < 0); sb = (s.b > 0) - (s.b < 0)
        if sb == 0 or sa == sb: return sa if sa else sb
        if sa == 0: return sb
        d = s.a * s.a - s.b * s.b * QF.D
        return sa if d > 0 else sb
    def __eq__(s, o):
        if isinstance(o, (int, Fr)): return s.b == 0 and s.a == o
        if isinstance(o, QF): return s.a == o.a and s.b == o.b
        return NotImplemented
    def __hash__(s): return hash(s.a) if s.b == 0 else hash((s.a, s.b))
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0
    def __abs__(s): return -s if s.sign() < 0 else s
    def __bool__(s): return not (s.a == 0 and s.b == 0)
    def __float__(s):
        import mpmath as mp
        with mp.workdps(60):
            return float(mp.mpf(s.a.numerator) / s.a.denominator + mp.mpf(s.b.numerator) / s.b.denominator
                         * mp.sqrt(mp.mpf(QF.D.numerator) / QF.D.denominator))
    def __str__(s): return f'{s.a} + {s.b}*sqrt({QF.D})'
    __repr__ = __str__


def load_q3(K):
    e = json.load(open(os.path.join(SRI, 'data', 'quadratic-examples.json')))['Q3']
    D = Fr(e['Delta']); QF.D = D
    assert math.isqrt(D.numerator) ** 2 != D.numerator or math.isqrt(D.denominator) ** 2 != D.denominator, 'Delta a square'
    g = lambda d: {int(k): QF(Fr(v['a']), Fr(v['b'])) for k, v in d.items()}
    for d in (e['b'], e['w'], e['apex']):
        assert all(Fr(v.get('sqrt_of', e['Delta'])) == D for v in d.values() if Fr(v['b']) != 0), 'one sqrt for all coordinates'
    b, w, a = g(e['b']), g(e['w']), g(e['apex'])
    return {i: (b[i], w[i], a[i]) for i in range(1, 10)}


# ---------------------------------------------------------------- rhombus yantras (u = v) at high precision
def rhombus_yantra(K, u, start, log, name):
    mp = K.mp
    from model import solve, all_conditions, order_ok
    v = u
    yan = lambda Q, S: solve(v ** 2 / (1 + v ** 2), Q, 1 / (1 + u ** 2), S, v / (1 + v ** 2), u / (1 + u ** 2), mp.sqrt, root=1)
    G = lambda Q, S: (lambda t: [t['w'][1] ** 2 + t['b'][1] ** 2 - t['b'][1], t['w'][9] ** 2 + t['b'][9] ** 2 - t['b'][9]])(yan(Q, S))
    Q, S = mp.findroot(G, (mp.mpf(start[0]), mp.mpf(start[1])), tol=mp.mpf(10) ** (-(K.dps - 20)), maxsteps=300)
    t = yan(Q, S)
    b, w = t['b'], t['w']
    m1 = w[1] / (Q - b[1]); h = abs(Q - b[5]); hw = m1 * h; r = hw * h / (hw + mp.sqrt(hw ** 2 + h ** 2))
    third = b[5] + (r if Q > b[5] else -r) - mp.mpf(1) / 2
    worst = max(abs(e) for n, e in all_conditions(t))
    lim = mp.mpf(10) ** (-(K.dps - 50))
    ok = worst < lim and order_ok(t, lim)
    log(f'{name}: rebuilt with u = v = {mp.nstr(u, 30)}, Q = {mp.nstr(Q, 30)}, S = {mp.nstr(S, 30)}; worst Huet condition {mp.nstr(worst, 3)}; '
        f'bindu centring (Kulaichev\'s (d), not imposed) off by {mp.nstr(third, 6)}')
    return {i: (t['b'][i], t['w'][i], t['a'][i]) for i in range(1, 10)}, ok, Q, S, third, lim


def load_rh345(K, log):
    mp = K.mp
    Y, ok, Q, S, third, lim = rhombus_yantra(K, mp.mpf(3) / 4, ('0.5508', '0.9205'), log, 'Rh345')
    Sx = (21464 + 56 * mp.sqrt(56869)) / 37825
    txt = open(os.path.join(SRI, 'data', 'rhombus345-exact-data.txt')).read().split('\n')
    qline = [l for l in txt if l.startswith('MINPOLY Q = b6')][0].split(':', 2)[2]
    b1line = [l for l in txt if l.startswith('MINPOLY b1')][0].split(':', 2)[2]
    def isolated(line, val):
        coef = parse_poly_x(line)
        Kd = K.dps - 40
        lo = Fr(int(mp.floor(val * mp.mpf(10) ** Kd)), 10 ** Kd); hi = lo + Fr(1, 10 ** Kd)
        return poly_sign_at(coef, lo) * poly_sign_at(coef, hi) < 0, Kd
    isoQ, Kd = isolated(qline, Q); isob1, _ = isolated(b1line, Y[1][0])
    st = json.load(open(os.path.join(SRI, 'data', 'rhombus345-coordinates.json')))['Rh345']
    dev = max(abs(Y[i][0] - mp.mpf(st['b'][str(i)]['a'])) for i in range(1, 10))
    good = ok and abs(S - Sx) < lim and isoQ and isob1 and dev < mp.mpf(10) ** -45 and abs(abs(third) - mp.mpf('2.36e-5')) < mp.mpf('1e-7')
    log(('ok   ' if good else 'FAIL ') + f'Rh345 at {K.dps} digits: S = (21464 + 56 sqrt 56869)/37825 to {mp.nstr(abs(S - Sx), 3)}; Q = b6 and b1 '
        f'isolated exactly by sign changes of their degree-20 minimal polynomials on intervals of width 1e-{Kd}: {isoQ}, {isob1}; '
        f'stored 50 digits agree to {mp.nstr(dev, 3)}; (d) misses by 2.36e-5 as recorded')
    return Y, good


def parse_poly_x(line):
    return parse_poly_text(line.replace('x', 'u'))


def parse_poly_text(txt):
    import re
    txt = txt.replace(' ', '').replace('\n', '')
    coef = {}
    for sgn, c, var, e in re.findall(r'([+-]?)(\d*)\*?(u?)(?:\^(\d+))?', txt):
        if not c and not var: continue
        k = (int(e) if e else 1) if var else 0
        v = int(c) if c else 1
        coef[k] = coef.get(k, 0) + (-v if sgn == '-' else v)
    return coef


def load_kul(K, log):
    mp = K.mp
    coef = parse_poly_text(open(os.path.join(SRI, 'figures', 'kulaichev-minpoly-u.txt')).read().replace('x', 'u'))
    assert max(coef) == 348, 'Kulaichev polynomial degree'
    f = lambda u: sum(c * u ** k for k, c in coef.items())
    fp = lambda u: sum(k * c * u ** (k - 1) for k, c in coef.items() if k)
    u = mp.mpf('0.750438516022214024406084657051234510340891003639790315415314')
    for _ in range(60):
        du = f(u) / fp(u); u -= du
        if abs(du) < mp.mpf(10) ** (-(K.dps + 10)): break
    Kd = K.dps - 20
    lo = Fr(int(mp.floor(u * mp.mpf(10) ** Kd)), 10 ** Kd); hi = lo + Fr(1, 10 ** Kd)
    iso = poly_sign_at(coef, lo) * poly_sign_at(coef, hi) < 0
    Y, ok, Q, S, third, lim = rhombus_yantra(K, u, ('0.5507', '0.9200'), log, 'Kulaichev')
    txt = open(os.path.join(SRI, 'data', 'kulaichev-numeric-data.txt')).read()
    import re
    st = {int(i): mp.mpf(v) for i, v in re.findall(r'b(\d) = ([0-9.]+)', txt)}
    dev = max(abs(Y[i][0] - st[i]) for i in range(1, 10))
    good = ok and iso and abs(third) < lim and dev < mp.mpf(10) ** -55
    log(('ok   ' if good else 'FAIL ') + f'Kulaichev at {K.dps} digits: u isolated exactly by a sign change of its degree-348 polynomial on an interval '
        f'of width 1e-{Kd}: {iso}; (d) bindu centred (not imposed) to {mp.nstr(abs(third), 3)}; stored 60 digits agree to {mp.nstr(dev, 3)}')
    return Y, good


def load_threshold(K, log, side):
    mp = K.mp
    u = mp.mpf(DSTAR) + side * mp.mpf(10) ** -4
    Y, ok, Q, S, third, lim = rhombus_yantra(K, u, ('0.5520', '0.9246'), log, f'rhombus u* {"+" if side > 0 else "-"} 1e-4')
    return Y, ok


# ---------------------------------------------------------------- analysis (chunk 5c's analyse; controls asserted, answers recorded)
def analyse(K, Y, name, log):
    ok = True; res = {}
    def check(cond, msg):
        nonlocal ok
        ok = ok and bool(cond); log(('ok   ' if cond else 'FAIL ') + msg)
    def find(msg): log('FIND ' + msg)
    A = arrangement(K, Y)
    faces, lines, S = A['faces'], A['lines'], A['S']
    odd = [f for f in faces if f['c'] % 2]; even = [f for f in faces if f['c'] % 2 == 0 and f['c'] > 0]
    outside = [f for f in faces if f['c'] == 0]
    rings = [sum(1 for f in odd if f['c'] == c) for c in (1, 3, 5, 7, 9)]
    so, se = {}, {}
    for f in odd: so[len(f['V'])] = so.get(len(f['V']), 0) + 1
    for f in even: se[len(f['V'])] = se.get(len(f['V']), 0) + 1
    find(f'{name}: {len(faces)} bounded faces: {len(odd)} regions, {len(even)} even faces inside the yantra, {len(outside)} outside every triangle')
    find(f'{name}: regions by ring (c = 1,3,5,7,9): {rings}; regions by number of sides {dict(sorted(so.items()))}; even faces by sides {dict(sorted(se.items()))}')
    res['counts'] = {'faces': len(faces), 'regions': len(odd), 'rings': rings, 'region_sides': dict(sorted(so.items())),
                     'even_sides': dict(sorted(se.items())), 'even': len(even)}
    lab = lambda f: f't{"".join(map(str, sorted(f["tris"])))} (ring {f["c"]}), sides on ' + ', '.join(f't{S[j][2]} {"base" if j % 3 == 0 else "leg"}' for j in f['lines'])
    for f in odd:
        if len(f['V']) != 3: find(f'{name}:   region with {len(f["V"])} sides: {lab(f)}; area {float(area2(f["V"])) / 2:.3e}; centroid ({float(f["X"][0]):.4f}, {float(f["X"][1]):.4f})')
    small = sorted(odd, key=lambda f: area2(f['V']))[:2]
    for f in small: find(f'{name}:   smallest regions: {len(f["V"])} sides, {lab(f)}, area {float(area2(f["V"])) / 2:.3e}')
    res['nontri'] = [(sorted(f['tris']), len(f['V']), [(S[j][2], j % 3) for j in f['lines']]) for f in odd if len(f['V']) != 3]
    if not K.exact: log(f'{name}: point merging: largest spread inside one merged point {K.mp.nstr(A["spread"], 3)} (tolerance 1e-{K.dps // 2})')
    nonconvex = [f for f in faces if not f['convex']]
    find(f'{name}: convex faces: {len(faces) - len(nonconvex)} of {len(faces)}' + (f' (non-convex: sides {[len(f["V"]) for f in nonconvex]})' if nonconvex else ' (all convex)'))
    res['nonconvex'] = len(nonconvex)
    by_edge = {}
    for fi, f in enumerate(faces):
        for e in f['edges']: by_edge[e] = fi
    bad_par = 0; odd_odd = 0
    for (p, q), fi in by_edge.items():
        if (q, p) in by_edge:
            c1, c2 = faces[fi]['c'], faces[by_edge[(q, p)]]['c']
            if abs(c1 - c2) != 1: bad_par += 1
            if c1 % 2 and c2 % 2: odd_odd += 1
    check(bad_par == 0 and odd_odd == 0, f'{name}: parity lemma: across every wall the count changes by exactly 1, so no two regions share a wall '
          f'({bad_par} exceptions, {odd_odd} odd-odd walls)')
    xs, ys = grid(K, lines)
    GP = [(x, y) for x in xs for y in ys]
    P27 = [math.prod(Lval(l, X) for l in lines) for X in GP]
    vf_ok = pos_ok = polar_ok = True
    VAL = {}
    for fi, f in enumerate(faces):
        V = f['V']; VAL[fi] = [vertex_form(V, X) for X in GP]
        Xc = f['X']; om = vertex_form(V, Xc)
        if not om > 0: pos_ok = False
        if not K.zero(om - polar_area2(V, Xc), abs(om)): polar_ok = False
    for f in odd:
        fi = faces.index(f)
        for X, v in zip(GP, VAL[fi]):
            if not K.zero(v - fan_form(f['V'], X), abs(v) + 1): vf_ok = False; break
    check(vf_ok, f'{name}: each of the {len(odd)} regions: vertex formula = fan triangulation at all {len(GP)} grid points (grid lemma)')
    check(pos_ok and polar_ok, f'{name}: every face: Omega > 0 inside and Omega = 2 * area of the polar at an inside point (chunk-2 bridge)')
    tri_ok = True
    for i in range(1, 10):
        Vt = triangle_V(Y, i); inside = [fi for fi, f in enumerate(faces) if i in f['tris']]
        for g, X in enumerate(GP):
            tv = vertex_form(Vt, X)
            if not K.zero(sum(VAL[fi][g] for fi in inside) - tv, abs(tv) + 1): tri_ok = False; break
    check(tri_ok, f'{name}: positive control (known region sum): in each of the nine triangles the faces sum to the triangle\'s form, all grid points')
    TI = intersections(K, Y, lines)
    nI = [sum(1 for I in TI if len(I) == k) for k in range(1, 10)]
    OY = [sum(VAL[faces.index(f)][g] for f in odd) for g in range(len(GP))]
    RHS = [sum((-2) ** (len(I) - 1) * vertex_form(V, X) for I, V in TI.items()) for X in GP]
    check(all(K.zero(a - b, abs(a) + 1) for a, b in zip(OY, RHS)), f'{name}: valuation identity: sum of the {len(odd)} regions = sum over I of '
          f'(-2)^(|I|-1) Omega(cap T_I) ({len(TI)} nonempty intersections, by size {[n for n in nI if n]}), all grid points (grid lemma)')
    res['nI'] = nI
    plain = [sum(VAL[fi][g] * faces[fi]['c'] for fi in range(len(faces))) for g in range(len(GP))]
    nine = [sum(vertex_form(triangle_V(Y, i), X) for i in range(1, 10)) for X in GP]
    check(all(K.zero(a - b, abs(a) + 1) for a, b in zip(plain, nine)), f'{name}: sum of the nine triangles = sum of faces weighted by c')
    f0 = faces.index(odd[0])
    check(not all(K.zero(a - 2 * VAL[f0][g] - b, abs(a) + 1) for g, (a, b) in enumerate(zip(OY, RHS))),
          f'{name}: negative control: one region with its sign flipped breaks the valuation identity')
    nt = [f for f in odd if len(f['V']) > 3]
    if nt:   # the four-sided regions: vertex = fan also checked with the other diagonal, and a flipped normal must break it
        V = nt[0]['V']; Vr = V[1:] + V[:1]
        check(all(K.zero(vertex_form(V, X) - fan_form(Vr, X), abs(vertex_form(V, X)) + 1) for X in GP[::5]),
              f'{name}: a non-triangle region: vertex formula = fan from either diagonal')
    Vn = odd[0]['V']; Xt = GP[100]
    check(not K.zero(vertex_form(Vn, Xt, flip=0) - fan_form(Vn, Xt), 1), f'{name}: negative control: one flipped normal breaks vertex = fan')
    Nvals = [[OY[i * GRID + j] * P27[i * GRID + j] for j in range(GRID)] for i in range(GRID)]
    C = interpolate(K, xs, ys, Nvals)
    cscale = max(abs(C[a][b]) for a in range(GRID) for b in range(GRID))
    top = max((a + b for a in range(GRID) for b in range(GRID) if not K.zero(C[a][b], cscale)), default=-1)
    check(top <= 24, f'{name}: numerator N of the whole-yantra form has degree {top} (bound 24 from 27 lines)')
    oddx = max((abs(C[a][b]) for a in range(1, GRID, 2) for b in range(GRID)), default=0)
    find(f'{name}: N is even in x (mirror symmetry): {K.zero(oddx, cscale)}')
    res['degN'] = top
    poles = 0
    for j, l in enumerate(lines):
        P0, P1 = S[j][0], S[j][1]
        X = (P0[0] + (P1[0] - P0[0]) * K.c(Fr(3, 7)), P0[1] + (P1[1] - P0[1]) * K.c(Fr(3, 7)))
        if not K.zero(deriv_at(C, X, 0, 0), deriv_at(C, X, 0, 0, True)): poles += 1
    find(f'{name}: pole lines of the whole-yantra form: {poles} of the 27 sides')
    res['poles'] = poles
    corners = []
    for i in range(1, 10):
        b, w, a = Y[i]; corners += [((-w, b), i, 'base corner'), ((w, b), i, 'base corner'), ((0 * w, a), i, 'apex')]
    PP = Pts(K); far = 0
    for j, k in itertools.combinations(range(27), 2):
        l1, l2 = lines[j], lines[k]
        d = l1[0] * l2[1] - l1[1] * l2[0]
        if K.zero(d, 1): continue
        p = ((l1[1] * l2[2] - l1[2] * l2[1]) / d, (l1[2] * l2[0] - l1[0] * l2[2]) / d)
        if max(abs(p[0]), abs(p[1] - K.c(Fr(1, 2)))) > 3: far += 1; continue
        PP.id(p)
    table = {}; residues = {}; rows = []
    for p in PP.pts:
        th = [j for j, l in enumerate(lines) if K.zero(Lval(l, p), 1)]
        m = len(th)
        def seg_par(j):
            P0, P1 = S[j][0], S[j][1]; dx, dy = P1[0] - P0[0], P1[1] - P0[1]
            return ((p[0] - P0[0]) * dx + (p[1] - P0[1]) * dy) / (dx * dx + dy * dy)
        par = {j: seg_par(j) for j in th}
        inner = [j for j in th if not K.le(par[j], 0) and not K.le(1, par[j])]
        onseg = [j for j in th if K.le(0, par[j]) and K.le(par[j], 1)]
        cn = [c for c in corners if K.zero(c[0][0] - p[0]) and K.zero(c[0][1] - p[1])]
        if cn:
            kinds = {c[2] for c in cn}
            touch = [j for j in inner if all(S[j][2] != c[1] for c in cn)]
            typ = (('tip on a base' if 'apex' in kinds and any(S[j][3] == 'base' for j in touch) else
                    'corner touch' if 'base corner' in kinds else 'apex on a side') if touch else 'triangle corner')
        elif len(inner) == m:
            typ = {2: 'sandhi', 3: 'marma'}.get(m, f'{m}-fold crossing')
        elif not onseg:
            typ = 'outside crossing'
        else:
            typ = 'partly outside crossing'
        def nz(al, be):
            v = deriv_at(C, p, al, be)
            return v != 0 if K.exact else not K.zero(v, deriv_at(C, p, al, be, True))
        k = None
        for o in range(4):
            if any(nz(al, o - al) for al in range(o + 1)): k = o; break
        kk = k if k is not None else '>=4'
        r = None
        if m == 2 and k == 0:
            R = math.prod(Lval(lines[j], p) for j in range(27) if j not in th)
            r = deriv_at(C, p, 0, 0) / (R * det2(lines[th[0]][:2], lines[th[1]][:2]))
        hess = None
        if typ == 'marma' and k == 2:   # tangent cone of N = 0 at the marma: two real branches (crossing) or an isolated real point
            hxx, hxy, hyy = deriv_at(C, p, 2, 0), deriv_at(C, p, 1, 1), deriv_at(C, p, 0, 2)
            dd = hxy * hxy - hxx * hyy
            hess = 'two real branches' if dd > 0 else ('isolated real point' if dd < 0 else 'degenerate')
        key = (typ, m, kk)
        table[key] = table.get(key, 0) + 1
        if r is not None:
            residues.setdefault(typ, {}); rr = round(float(abs(r)), 9); residues[typ][rr] = residues[typ].get(rr, 0) + 1
        rows.append((typ, tuple(sorted((S[j][2], j % 3) for j in th)), kk, None if r is None else abs(r), (float(p[0]), float(p[1])), hess))
    for key in sorted(table, key=str):
        find(f'{name}:   {key[0]:24s} lines through it m = {key[1]}, N vanishes to order k = {key[2]}: {table[key]} points')
    for typ, d in residues.items():
        find(f'{name}:   point residue |Res| at {typ}s (m = 2, k = 0): {d}')
    hs = {}
    for r in rows:
        if r[5]: hs[r[5]] = hs.get(r[5], 0) + 1
    find(f'{name}:   N = 0 at the marmas (tangent cone of the order-2 zero): {hs}')
    log(f'{name}:   {far} crossings of extended side lines lie beyond the box |x| <= 3, |y - 1/2| <= 3 (not classified)')
    nm = sum(v for (t, m, k), v in table.items() if t == 'marma'); ns = sum(v for (t, m, k), v in table.items() if t == 'sandhi')
    find(f'{name}: {nm} marmas, {ns} sandhis; order of N at the marmas: {sorted({k for (t, m, k) in table if t == "marma"}, key=str)}; '
         f'|Res| at sandhis: {sorted(residues.get("sandhi", {}))}; off-figure crossings with k = 0: '
         f'{sum(v for (t, m, k), v in table.items() if "outside" in t and k == 0)}')
    res['table'] = {str(k): v for k, v in table.items()}; res['residues'] = {t: {str(a): b for a, b in d.items()} for t, d in residues.items()}
    res['rows'] = rows; res['marma_tangents'] = hs
    pick = None
    for F in sorted(odd, key=lambda f: -f['A2']):
        for e in F['edges']:
            if (e[1], e[0]) not in by_edge: continue
            G = faces[by_edge[(e[1], e[0])]]
            pA, pB = A['pts'][e[0]], A['pts'][e[1]]
            if all(any(v is q or v == q for v in F['V']) and any(v is q or v == q for v in G['V']) for q in (pA, pB)):
                pick = (F, G, pA, pB); break
        if pick: break
    F, G, pA, pB = pick
    mid = ((pA[0] + pB[0]) / 2, (pA[1] + pB[1]) / 2); nrm = (-(pB[1] - pA[1]), pB[0] - pA[0])
    def expo(fn):
        e1, e2 = K.c(Fr(1, 10 ** 20)), K.c(Fr(1, 10 ** 40))
        v1 = fn((mid[0] + e1 * nrm[0], mid[1] + e1 * nrm[1])); v2 = fn((mid[0] + e2 * nrm[0], mid[1] + e2 * nrm[1]))
        return math.log10(abs(float(v2)) / abs(float(v1))) / 20
    good = expo(lambda X: vertex_form(F['V'], X) + vertex_form(G['V'], X))
    dl = K.c(Fr(1, 1000)); Gs = [(v[0] + dl * nrm[0], v[1] + dl * nrm[1]) for v in G['V']]
    badj = expo(lambda X: vertex_form(F['V'], X) + vertex_form(Gs, X))
    check(abs(good) < 0.05 and abs(badj - 1) < 0.05, f'{name}: wall control: region + its even neighbour: pole exponent {good:.3f} on the shared wall '
          f'(cancels); neighbour moved 1/1000 off: {badj:.3f} (pole left)')
    tests = [K.c(Fr(1, 9)), K.c(Fr(1, 2)), K.c(Fr(2, 7))]
    res['fp'] = [vertex_form(odd[0]['V'], (tests[0], tests[2]))] + [sum(vertex_form(f['V'], (tests[0], t)) for f in odd) for t in tests]
    X0 = (K.c(0), K.c(Fr(1, 2)))
    bindu = [f for f in odd if f['c'] == 9]
    res['centre'] = (vertex_form(bindu[0]['V'], X0) if bindu else None, sum(vertex_form(f['V'], X0) for f in odd))
    inb = bool(bindu) and all(Lval(l, X0) * Lval(l, B.centroid(bindu[0]['V'])) > 0 for l in [line_of(bindu[0]['V'][i], bindu[0]['V'][(i + 1) % len(bindu[0]['V'])]) for i in range(len(bindu[0]['V']))])
    find(f'{name}: at the circle centre (0, 1/2) (inside the bindu region: {inb}): Omega(bindu region) = {float(res["centre"][0]) if bindu else float('nan'):.12g}, '
         f'Omega_Y = {float(res["centre"][1]):.12g}')
    res['pattern'] = sorted((tuple(sorted(f['tris'])), tuple(sorted((S[j][2], j % 3) for j in f['lines']))) for f in faces)
    return ok, res


# ---------------------------------------------------------------- tasks
def task(arg):
    name, dps = arg
    if name == 'lemmas':
        return B.task_lemmas(None)
    out = []; log = out.append
    t0 = time.time()
    if name in ('R1', 'Q3', 'Q3-probe'):
        K = Ctx(None); Y = load_r1(K) if name == 'R1' else load_q3(K); ok0 = True
    else:
        K = Ctx(dps)
        Y, ok0 = {'Rh345': load_rh345, 'Kul': load_kul}[name](K, log) if name in ('Rh345', 'Kul') else load_threshold(K, log, -1 if name == 'thr-' else 1)
    if name == 'Q3-probe':           # pilot: pattern only, and a timing probe for the exact grid work
        A = arrangement(K, Y); odd = [f for f in A['faces'] if f['c'] % 2]
        log(f'Q3-probe: {len(A["faces"])} faces, {len(odd)} regions, sides {sorted(len(f["V"]) for f in odd if len(f["V"]) != 3)} '
            f'(non-triangles), arrangement {time.time() - t0:.0f} s')
        t1 = time.time(); xs, ys = grid(K, A['lines'])
        for f in A['faces'][:10]:
            for y in ys[:5]: vertex_form(f['V'], (xs[3], y))
        per = (time.time() - t1) / 50
        TI = intersections(K, Y, A['lines'])
        est = per * 676 * (2 * len(A['faces']) + len(TI) + 9 * 2 + 12)
        log(f'Q3-probe: {per * 1000:.1f} ms per exact vertex form; {len(TI)} intersections; full Q3 estimate {est / 60:.0f} min plus interpolation')
        pat = sorted((tuple(sorted(f['tris'])), tuple(sorted((A['S'][j][2], j % 3) for j in f['lines']))) for f in A['faces'])
        return name, True, out, {'pattern': pat, 'counts': {'regions': len(odd)}}
    ok, res = analyse(K, Y, name if dps is None else f'{name}@{dps}', log)
    res['fp'] = [str(v) for v in res['fp']]
    res['centre'] = [None if v is None else str(v) for v in res['centre']]
    res['rows'] = [(a, b, c, None if d is None else str(d), e, h) for a, b, c, d, e, h in res['rows']]
    log(f'{name}: {time.time() - t0:.0f} s')
    return name, ok and ok0, out, res


def load_r1(K):
    return B.load_r1(K)


def main():
    t0 = time.time()
    if PILOT:
        tasks = [('Q3-probe', None), ('R1', None), ('Rh345', 120), ('Kul', 120), ('thr-', 120)]
    else:
        tasks = [('Q3', None), ('lemmas', None), ('R1', None), ('Rh345', 300), ('Kul', 300), ('Rh345', 600), ('Kul', 600), ('thr-', 150), ('thr+', 150)]
    print(f'chunk 5c lead (a): {len(tasks)} tasks on 4 cores', flush=True)
    results = {}; ok = True; done = 0
    with get_context('fork').Pool(4) as pool:
        its = [pool.apply_async(task, (t,)) for t in tasks]
        for it in its[1:] + its[:1]:            # the long exact Q3 task is submitted first and read last (progress lines keep coming)
            name, good, out, res = it.get()
            done += 1
            for line in out: print(line, flush=True)
            print(f'PROGRESS {done / len(tasks):.2f} {name}', flush=True)
            results.setdefault(name, []).append(res); ok = ok and good
    def say(c, m):
        nonlocal ok
        ok = ok and bool(c); print(('ok   ' if c else 'FAIL ') + m, flush=True)
    drawn = lambda tb: {k: v for k, v in tb.items() if 'outside' not in k}
    r1 = results['R1'][0]; kul = results['Kul'][0]; rh = results['Rh345'][0]; thm = results['thr-'][0]
    q3 = results.get('Q3', results.get('Q3-probe'))[0]
    say(kul['counts']['regions'] == 45 and rh['counts']['regions'] == 45 and q3['counts']['regions'] == 45,
        f'positive control (known counts, sri-yantra study): Kulaichev, Rh345 and Q3 have 45 regions ({kul["counts"]["regions"]}, {rh["counts"]["regions"]}, {q3["counts"]["regions"]})')
    say(thm['counts']['regions'] == 43 and thm['counts']['region_sides'] == {3: 43} and thm['pattern'] == r1['pattern'],
        f'control (rhombus threshold): just below u* the rhombus yantra has 43 regions, all triangles, and the crossing pattern of R1 = DICTO Yantra')
    same45 = kul['pattern'] == rh['pattern'] == q3['pattern']
    if 'table' in q3: same45 = same45 and drawn(kul['table']) == drawn(rh['table']) == drawn(q3['table'])
    if not PILOT:
        thp = results['thr+'][0]; same45 = same45 and thp['pattern'] == kul['pattern']
    say(same45, 'Kulaichev, Rh345' + ('' if PILOT else ', the rhombus yantra just above u*') + ' and Q3 have the same crossing pattern '
        '(every face with its triangles and side lines' + (', every drawn point with type, m, k)' if 'table' in q3 else ')') +
        ': the exact Q3 results carry over as structure')
    a, b = set(r1['pattern']), set(kul['pattern'])
    def fmt(fc): return f't{"".join(map(str, fc[0]))} [' + ' '.join(f't{t}{"b" if s == 0 else "l"}' for t, s in fc[1]) + ']'
    print(f'43 -> 45: faces only in the DICTO pattern (R1): {len(a - b)}: ' + '; '.join(fmt(f) for f in sorted(a - b)), flush=True)
    print(f'43 -> 45: faces only in the 45 pattern (Kulaichev): {len(b - a)}: ' + '; '.join(fmt(f) for f in sorted(b - a)), flush=True)
    if 'table' in kul and 'table' in r1:
        keys = sorted(set(drawn(r1['table'])) | set(drawn(kul['table'])))
        for k in keys:
            x, y = r1['table'].get(k, 0), kul['table'].get(k, 0)
            if x != y: print(f'43 -> 45: point class {k}: {x} -> {y}', flush=True)
        print(f'43 -> 45: degree of N {r1["degN"]} -> {kul["degN"]}; nonempty intersections by size {r1["nI"]} -> {kul["nI"]}; '
              f'sandhi residues {r1["residues"].get("sandhi")} -> {kul["residues"].get("sandhi")}; '
              f'centre Omega_Y R1 {QFstr(r1["centre"][1]):.6g}, Kulaichev {QFstr(kul["centre"][1]):.6g}, Rh345 {QFstr(rh["centre"][1]):.6g}'
              + (f', Q3 {float(QFstr(q3["centre"][1])):.6g}' if 'centre' in q3 else ''), flush=True)
    for nm in ('Rh345', 'Kul'):
        g = results[nm]
        if len(g) == 2:
            import mpmath as mp
            mp.mp.dps = 320
            x, y = [mp.mpf(v) for v in g[0]['fp']], [mp.mpf(v) for v in g[1]['fp']]
            dev = max(abs(p - q) / abs(q) for p, q in zip(x, y))
            ra = [mp.mpf(r[3]) for r in g[0]['rows'] if r[3]]; rb = [mp.mpf(r[3]) for r in g[1]['rows'] if r[3]]
            dev2 = max(abs(p - q) for p, q in zip(ra, rb)) if len(ra) == len(rb) else mp.mpf(1)
            st = g[0]['table'] == g[1]['table'] and g[0]['pattern'] == g[1]['pattern']
            say(dev < mp.mpf(10) ** -200 and dev2 < mp.mpf(10) ** -200 and st,
                f'{nm} at 300 and 600 digits: same pattern and point table; values agree to {mp.nstr(dev, 3)}, residues to {mp.nstr(dev2, 3)}')
    json.dump({k: [{kk: vv for kk, vv in r.items() if kk not in ('pattern', 'rows')} for r in v] for k, v in results.items()},
              open(os.path.join(HERE, '..', 'data', 'yantra-regions45-pilot.json' if PILOT else 'yantra-regions45.json'), 'w'), indent=1, default=str)
    print(f'total {time.time() - t0:.0f} s', flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL: see the FAIL lines above', flush=True)


def QFstr(s):     # float of a stored 'a + b*sqrt(D)' string
    import mpmath as mp
    if 'sqrt' not in s: return float(Fr(s)) if '/' in s or s.lstrip('-').isdigit() else float(mp.mpf(s))
    a, rest = s.split(' + ', 1); bb, D = rest.split('*sqrt(')
    with mp.workdps(60):
        f = lambda q: mp.mpf(Fr(q).numerator) / Fr(q).denominator
        return float(f(a) + f(bb) * mp.sqrt(f(D.rstrip(')'))))


if __name__ == '__main__':
    main()
