"""Aim 2, chunk 5c (12 Nov 2026): canonical forms of the 43 regions of the flat DICTO Yantra. Method and checks: ../README.md.
Exact for the lemmas (sympy, symbolic slopes) and for the rational yantra R1 (Fractions, grid lemma); the DICTO Yantra (GF1, degree 160)
at 300 and 600 digits (u isolated exactly by a sign change of its degree-160 polynomial; Q, S by Newton).
Usage: python -u yantra_regions.py [pilot]"""
import sys, os, json, math, re, time, itertools
from fractions import Fraction as Fr
from multiprocessing import get_context

PILOT = sys.argv[1:] == ['pilot']
HERE = os.path.dirname(os.path.abspath(__file__))
SRI = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-08-sri-yantra'))
sys.path.insert(0, os.path.join(SRI, 'scripts'))
GRID = 26                                   # N has degree <= 24 (checked); 26 x 26 grid proves degree <= 25 identities


# ---------------------------------------------------------------- number context
class Ctx:
    def __init__(self, dps=None):
        self.exact = dps is None
        self.dps = dps
        if not self.exact:
            import mpmath as mp
            mp.mp.dps = dps
            self.mp = mp
            self.eps = mp.mpf(10) ** (-(2 * dps // 3))
            self.merge = mp.mpf(10) ** (-(dps // 2))

    def c(self, q):
        q = Fr(q)
        return q if self.exact else self.mp.mpf(q.numerator) / q.denominator

    def zero(self, x, scale=1):
        return x == 0 if self.exact else abs(x) <= self.eps * scale

    def sgn(self, x, scale=1):
        return 0 if self.zero(x, scale) else (1 if x > 0 else -1)

    def le(self, x, y):          # x <= y up to tolerance
        return x <= y if self.exact else x <= y + self.eps

    def f(self, x):
        return float(x)


def det2(a, b):
    return a[0] * b[1] - a[1] * b[0]


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


# ---------------------------------------------------------------- forms of convex polygons (vertices CCW)
def vertex_form(V, X, flip=None):
    """Omega = sum_v det(a_prev, a_next)/(l_prev l_next); l_i(X) = det(v_{i+1} - v_i, X - v_i) >= 0 inside (CCW)."""
    n = len(V); ls = []; As = []
    for i in range(n):
        p, q = V[i], V[(i + 1) % n]
        e = sub(q, p)
        a = (-e[1], e[0])
        if flip == i: a = (-a[0], -a[1])
        As.append(a); ls.append(det2(e, sub(X, p)))
    return sum(det2(As[i - 1], As[i]) / (ls[i - 1] * ls[i]) for i in range(n))


def tri_form(a, b, c, X):
    D = det2(sub(b, a), sub(c, a))
    d0 = det2(sub(b, X), sub(c, X)); d1 = det2(sub(X, a), sub(c, a)); d2 = det2(sub(b, a), sub(X, a))
    return (1 if D > 0 else -1) * D * D / (d0 * d1 * d2)


def fan_form(V, X):
    return sum(tri_form(V[0], V[i], V[i + 1], X) for i in range(1, len(V) - 1))


def polar_area2(V, X):
    """2! * area of the polar of (P - X), X inside P."""
    n = len(V); W = []
    for i in range(n):
        p, q = V[i], V[(i + 1) % n]
        e = sub(q, p); a = (-e[1], e[0]); l = det2(e, sub(X, p))
        W.append((-a[0] / l, -a[1] / l))
    A = sum(det2(W[i], W[(i + 1) % n]) for i in range(n)) / 2
    return 2 * abs(A)


def area2(V):
    return sum(det2(V[i], V[(i + 1) % len(V)]) for i in range(len(V)))


def centroid(V):
    n = len(V)
    return (sum(v[0] for v in V) / n, sum(v[1] for v in V) / n)


# ---------------------------------------------------------------- yantra data
def load_r1(K, shift=None):
    e = json.load(open(os.path.join(SRI, 'data', 'quadratic-examples.json')))['R1']
    g = lambda d: {int(k): Fr(v['a']) for k, v in d.items()}
    b, w, a = g(e['b']), g(e['w']), g(e['apex'])
    if shift: b[shift[0]] += shift[1]
    return {i: (K.c(b[i]), K.c(w[i]), K.c(a[i])) for i in range(1, 10)}


def parse_poly(path):
    txt = open(path).read().replace(' ', '').replace('\n', '')
    coef = {}
    for sgn, c, var, e in re.findall(r'([+-]?)(\d*)\*?(u?)(?:\^(\d+))?', txt):
        if not c and not var: continue
        k = (int(e) if e else 1) if var else 0
        v = int(c) if c else 1
        coef[k] = coef.get(k, 0) + (-v if sgn == '-' else v)
    return coef


def poly_sign_at(coef, q):           # exact sign of the integer polynomial at the rational q
    n, d = q.numerator, q.denominator; deg = max(coef)
    s = sum(c * n ** k * d ** (deg - k) for k, c in coef.items())
    return (s > 0) - (s < 0)


def load_gf1(K, log):
    mp = K.mp
    from model import solve, all_conditions, order_ok
    coef = parse_poly(os.path.join(SRI, 'figures', 'dicto-yantra-exact-u.txt'))
    assert max(coef) == 160, 'polynomial degree'
    f = lambda u: sum(c * u ** k for k, c in coef.items())
    fp = lambda u: sum(k * c * u ** (k - 1) for k, c in coef.items() if k)
    u = mp.mpf('0.679318588706774657388650310391')
    for _ in range(60):
        du = f(u) / fp(u); u -= du
        if abs(du) < mp.mpf(10) ** (-(K.dps + 10)): break
    Kd = K.dps - 20
    lo = Fr(int(mp.floor(u * mp.mpf(10) ** Kd)), 10 ** Kd); hi = lo + Fr(1, 10 ** Kd)
    s_lo, s_hi = poly_sign_at(coef, lo), poly_sign_at(coef, hi)
    iso = s_lo * s_hi < 0
    log(f'u isolated exactly by a sign change of the degree-160 polynomial on an interval of width 1e-{Kd}: {"yes" if iso else "NO"}; '
        f'u = {mp.nstr(u, 40)}')
    phi = (1 + mp.sqrt(5)) / 2
    v = 2 / phi ** 3 / u
    yan = lambda Q, S: solve(v ** 2 / (1 + v ** 2), Q, 1 / (1 + u ** 2), S, v / (1 + v ** 2), u / (1 + u ** 2), mp.sqrt, root=1)
    G = lambda Q, S: (lambda t: [t['w'][1] ** 2 + t['b'][1] ** 2 - t['b'][1], t['w'][9] ** 2 + t['b'][9] ** 2 - t['b'][9]])(yan(Q, S))
    gf = json.load(open(os.path.join(SRI, 'figures', 'golden_family.json')))['GF1']
    Q, S = mp.findroot(G, (mp.mpf(gf['b']['6']['a']), mp.mpf(gf['b']['9']['a'])), tol=mp.mpf(10) ** (-(K.dps - 20)), maxsteps=300)
    t = yan(Q, S)
    b, w = t['b'], t['w']
    m1 = w[1] / (Q - b[1]); h = abs(Q - b[5]); hw = m1 * h; r = hw * h / (hw + mp.sqrt(hw ** 2 + h ** 2))
    third = abs(b[5] + (r if Q > b[5] else -r) - mp.mpf(1) / 2)
    worst = max(abs(e) for n, e in all_conditions(t))
    dev40 = max(abs(t['b'][i] - mp.mpf(gf['b'][str(i)]['a'])) for i in range(1, 10))
    lim = mp.mpf(10) ** (-(K.dps - 50))
    ok = iso and third < lim and worst < lim and order_ok(t, lim) and dev40 < mp.mpf(10) ** -38
    log(f'GF1 rebuilt: bindu centring (not imposed) misses by {mp.nstr(third, 3)}; worst Huet condition {mp.nstr(worst, 3)}; '
        f'agrees with the stored 40 digits to {mp.nstr(dev40, 3)}')
    return {i: (t['b'][i], t['w'][i], t['a'][i]) for i in range(1, 10)}, ok


# ---------------------------------------------------------------- arrangement
def sides(Y):
    """27 sides: id 3(i-1)+0 base, +1 left leg (L-A), +2 right leg (R-A); each (P, Q, triangle, kind)."""
    S = []
    for i in range(1, 10):
        b, w, a = Y[i]
        L, R, A = (-w, b), (w, b), (0 * w, a)
        S += [(L, R, i, 'base'), (L, A, i, 'leg'), (R, A, i, 'leg')]
    return S


def line_of(P, Q):          # L(X) = A x + B y + C, zero on the side
    A = P[1] - Q[1]; B = Q[0] - P[0]; C = P[0] * Q[1] - Q[0] * P[1]
    return (A, B, C)


def Lval(l, X):
    return l[0] * X[0] + l[1] * X[1] + l[2]


class Pts:
    def __init__(self, K):
        self.K = K; self.pts = []; self.idx = {}; self.spread = 0

    def id(self, p):
        if self.K.exact:
            if p not in self.idx: self.idx[p] = len(self.pts); self.pts.append(p)
            return self.idx[p]
        for k, q in enumerate(self.pts):
            dd = max(abs(p[0] - q[0]), abs(p[1] - q[1]))
            if dd < self.K.merge:
                self.spread = max(self.spread, dd); return k
        self.pts.append(p); return len(self.pts) - 1


def arrangement(K, Y):
    S = sides(Y)
    lines = [line_of(s[0], s[1]) for s in S]
    # no two sides on one line
    for j, k in itertools.combinations(range(27), 2):
        l1, l2 = lines[j], lines[k]
        sc = max(abs(v) for v in l1) * max(abs(v) for v in l2)
        if K.zero(l1[0] * l2[1] - l1[1] * l2[0], sc) and K.zero(l1[0] * l2[2] - l1[2] * l2[0], sc) and K.zero(l1[1] * l2[2] - l1[2] * l2[1], sc):
            raise RuntimeError(f'sides {j}, {k} on one line')
    P = Pts(K); edges = {}
    for i, s in enumerate(S):
        (x1, y1), (x2, y2) = s[0], s[1]
        cuts = [(K.c(0), s[0]), (K.c(1), s[1])]
        for j, t in enumerate(S):
            if i == j: continue
            (x3, y3), (x4, y4) = t[0], t[1]
            d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
            if K.zero(d, 1): continue
            p = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
            q = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
            if K.le(0, p) and K.le(p, 1) and K.le(0, q) and K.le(q, 1):
                cuts.append((p, (x1 + p * (x2 - x1), y1 + p * (y2 - y1))))
        cuts.sort(key=lambda c: c[0])
        ids = []
        for _, pt in cuts:
            k = P.id(pt)
            if not ids or ids[-1] != k: ids.append(k)
        for k in range(len(ids) - 1):
            edges[(ids[k], ids[k + 1])] = i; edges[(ids[k + 1], ids[k])] = i
    pts = P.pts
    nb = {}
    for (p, q) in edges: nb.setdefault(p, []).append(q)
    fl = lambda p: (K.f(p[0]), K.f(p[1]))
    for p in nb:
        nb[p].sort(key=lambda q: math.atan2(K.f(pts[q][1] - pts[p][1]), K.f(pts[q][0] - pts[p][0])))
    used, faces = set(), []
    for e in edges:
        if e in used: continue
        f = []; cur = e
        while cur not in used:
            used.add(cur); f.append(cur); p, q = cur
            n = nb[q]; k = n.index(p); cur = (q, n[(k - 1) % len(n)])
        faces.append(f)
    out = []
    for f in faces:
        lid = [edges[e] for e in f]
        corners = [pts[f[i][0]] for i in range(len(f)) if lid[i - 1] != lid[i]]
        cl = [lid[i] for i in range(len(f)) if lid[i - 1] != lid[i]]          # edge line leaving each corner
        A2 = area2(corners)
        # an interior point next to the longest walk edge (valid for non-convex faces too): the face lies left of a CCW walk
        e0 = max(f, key=lambda e: K.f((pts[e[1]][0] - pts[e[0]][0]) ** 2 + (pts[e[1]][1] - pts[e[0]][1]) ** 2))
        E0, E1 = pts[e0[0]], pts[e0[1]]; sg = 1 if A2 > 0 else -1; dl = K.c(Fr(1, 10 ** 12))
        Xi = ((E0[0] + E1[0]) / 2 - sg * dl * (E1[1] - E0[1]), (E0[1] + E1[1]) / 2 + sg * dl * (E1[0] - E0[0]))
        out.append({'V': corners, 'lines': cl, 'A2': A2, 'edges': f, 'Xi': Xi})
    signs = [1 if fc['A2'] > 0 else -1 for fc in out]
    outer = [i for i, s in enumerate(signs) if s != max(set(signs), key=signs.count)]
    assert len(outer) == 1, f'outer faces {len(outer)}'
    inner = [fc for i, fc in enumerate(out) if i != outer[0]]
    for fc in inner:                     # make CCW
        if fc['A2'] < 0:
            fc['V'] = fc['V'][::-1]; fc['lines'] = fc['lines'][::-1]; fc['lines'] = fc['lines'][1:] + fc['lines'][:1]; fc['A2'] = -fc['A2']
    # triangles' inside tests
    def inside_tri(i, X):
        idx = [3 * (i - 1), 3 * (i - 1) + 1, 3 * (i - 1) + 2]
        b, w, a = Y[i]; cen = (0 * w, (2 * b + a) / 3)
        return all(K.sgn(Lval(lines[j], X)) * K.sgn(Lval(lines[j], cen)) > 0 for j in idx)
    for fc in inner:
        V = fc['V']; n = len(V)
        fc['convex'] = all(det2(sub(V[(i + 1) % n], V[i]), sub(V[(i + 2) % n], V[(i + 1) % n])) > 0 for i in range(n))
        fc['X'] = centroid(V) if fc['convex'] else fc['Xi']
        fc['tris'] = frozenset(i for i in range(1, 10) if inside_tri(i, fc['Xi']))
        fc['c'] = len(fc['tris'])
    return {'S': S, 'lines': lines, 'pts': pts, 'faces': inner, 'edges': edges, 'spread': P.spread, 'inside_tri': inside_tri}


def triangle_V(Y, i):
    b, w, a = Y[i]
    V = [(-w, b), (w, b), (0 * w, a)]
    return V if area2(V) > 0 else V[::-1]


def clip(K, V, l):
    """intersect CCW convex polygon V with half-plane l(X) >= 0 (l affine triple)."""
    out = []; n = len(V)
    for i in range(n):
        p, q = V[i], V[(i + 1) % n]
        fp, fq = Lval(l, p), Lval(l, q)
        sp_, sq = K.sgn(fp), K.sgn(fq)
        if sp_ >= 0: out.append(p)
        if sp_ * sq < 0:
            t = fp / (fp - fq); out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    # drop duplicates and straight vertices
    W = []
    for p in out:
        if not W or not (K.zero(p[0] - W[-1][0]) and K.zero(p[1] - W[-1][1])): W.append(p)
    if len(W) > 1 and K.zero(W[0][0] - W[-1][0]) and K.zero(W[0][1] - W[-1][1]): W.pop()
    changed = True
    while changed and len(W) >= 3:
        changed = False
        for i in range(len(W)):
            a, b, c = W[i - 1], W[i], W[(i + 1) % len(W)]
            if K.zero(det2(sub(b, a), sub(c, b))):
                W.pop(i); changed = True; break
    return W if len(W) >= 3 and not K.zero(area2(W)) else None


def intersections(K, Y, lines):
    """all nonempty T_I = cap of T_i, i in I (as CCW polygons)."""
    res = {}
    def half(i):
        b, w, a = Y[i]; cen = (0 * w, (2 * b + a) / 3); hs = []
        for j in (3 * (i - 1), 3 * (i - 1) + 1, 3 * (i - 1) + 2):
            l = lines[j]; s = 1 if Lval(l, cen) > 0 else -1
            hs.append((s * l[0], s * l[1], s * l[2]))
        return hs
    H = {i: half(i) for i in range(1, 10)}
    def rec(I, V):
        res[I] = V
        for j in range(max(I) + 1, 10):
            W = V
            for l in H[j]:
                W = clip(K, W, l)
                if W is None: break
            if W is not None: rec(I + (j,), W)
    for i in range(1, 10): rec((i,), triangle_V(Y, i))
    return res


# ---------------------------------------------------------------- polynomial N and its derivatives
def grid(K, lines):
    xs = [K.c(Fr(-56, 100) + Fr(112 * i, 100 * (GRID - 1)) + Fr(1, 7919)) for i in range(GRID)]
    ys = [K.c(Fr(-6, 100) + Fr(112 * j, 100 * (GRID - 1)) + Fr(1, 7907)) for j in range(GRID)]
    for x in xs:
        for y in ys:
            for l in lines:
                if K.zero(Lval(l, (x, y)), 1): raise RuntimeError('grid point on a side line')
    return xs, ys


def inv_vandermonde(K, xs):
    n = len(xs)
    M = [[xs[i] ** k for k in range(n)] + [K.c(1 if r == i else 0) for r in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]; M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                fct = M[r][col]; M[r] = [a - fct * b for a, b in zip(M[r], M[col])]
    return [row[n:] for row in M]          # inverse of V (V[i][k] = xs[i]^k): coef = Vinv @ vals


def interpolate(K, xs, ys, vals):
    """vals[i][j] = N(xs[i], ys[j]) -> coefficients C[a][b] of x^a y^b."""
    Vx, Vy = inv_vandermonde(K, xs), inv_vandermonde(K, ys)
    n = len(xs)
    T = [[sum(Vx[a][i] * vals[i][j] for i in range(n)) for j in range(n)] for a in range(n)]
    return [[sum(Vy[b][j] * T[a][j] for j in range(n)) for b in range(n)] for a in range(n)]


def deriv_at(C, p, al, be, absval=False):
    n = len(C); x, y = p
    px = [x ** k for k in range(n)]; py = [y ** k for k in range(n)]
    if absval: px = [abs(v) for v in px]; py = [abs(v) for v in py]
    s = 0
    for a in range(al, n):
        fa = math.perm(a, al)
        for b in range(be, n):
            c = C[a][b]
            if c == 0: continue
            s += (abs(c) if absval else c) * fa * math.perm(b, be) * px[a - al] * py[b - be]
    return s


# ---------------------------------------------------------------- one yantra, full analysis
def analyse(K, Y, name, log, want_pattern=True):
    ok = True; res = {}
    def check(cond, msg):
        nonlocal ok
        ok = ok and bool(cond); log(('ok   ' if cond else 'FAIL ') + msg)
    A = arrangement(K, Y)
    faces, lines, S = A['faces'], A['lines'], A['S']
    odd = [f for f in faces if f['c'] % 2]; even = [f for f in faces if f['c'] % 2 == 0 and f['c'] > 0]
    outside = [f for f in faces if f['c'] == 0]
    rings = {c: sum(1 for f in odd if f['c'] == c) for c in (1, 3, 5, 7, 9)}
    sides_odd = {}; sides_even = {}
    for f in odd: sides_odd[len(f['V'])] = sides_odd.get(len(f['V']), 0) + 1
    for f in even: sides_even[len(f['V'])] = sides_even.get(len(f['V']), 0) + 1
    log(f'{name}: {len(faces)} bounded faces: {len(odd)} regions (odd), {len(even)} even faces inside the yantra, {len(outside)} outside every triangle')
    log(f'{name}: regions by ring (c = 1,3,5,7,9): {[rings[c] for c in (1, 3, 5, 7, 9)]}; regions by number of sides {dict(sorted(sides_odd.items()))}; '
        f'even faces by sides {dict(sorted(sides_even.items()))}')
    res['counts'] = (len(odd), [rings[c] for c in (1, 3, 5, 7, 9)], dict(sorted(sides_odd.items())), dict(sorted(sides_even.items())), len(outside))
    if not K.exact: log(f'{name}: point merging: largest spread inside one merged point {K.mp.nstr(A["spread"], 3)} (tolerance 1e-{K.dps // 2})')
    nonconvex = [f for f in faces if not f['convex']]
    check(not nonconvex, f'{name}: every face of the arrangement is convex' + (f' ({len(nonconvex)} non-convex: a corner pokes into a face, sides {[len(f["V"]) for f in nonconvex]})' if nonconvex else ''))
    # parity lemma
    by_edge = {}
    for fi, f in enumerate(faces):
        for e in f['edges']: by_edge[e] = fi
    bad_par = 0; odd_odd = 0
    for (p, q), fi in by_edge.items():
        if (q, p) in by_edge:
            c1, c2 = faces[fi]['c'], faces[by_edge[(q, p)]]['c']
            if abs(c1 - c2) != 1:
                bad_par += 1
                if bad_par <= 3: log(f'{name}:   parity exception on side {A["edges"][(p, q)]} (t{S[A["edges"][(p, q)]][2]} {S[A["edges"][(p, q)]][3]}): counts {c1}, {c2}; '
                                     f'faces {sorted(faces[fi]["tris"])} | {sorted(faces[by_edge[(q, p)]]["tris"])}')
            if c1 % 2 and c2 % 2: odd_odd += 1
    check(bad_par == 0 and odd_odd == 0, f'{name}: parity lemma: across every wall the count changes by exactly 1, so no two regions share a wall '
          f'({bad_par} exceptions, {odd_odd} odd-odd walls)')
    # Q1: each face: vertex formula = fan formula (grid lemma), Omega > 0 inside, = 2 polar area
    xs, ys = grid(K, lines)
    GP = [(x, y) for x in xs for y in ys]
    P27 = [math.prod(Lval(l, X) for l in lines) for X in GP]
    vf_ok = True; pos_ok = True; polar_ok = True
    VAL = {}
    for fi, f in enumerate(faces):
        V = f['V']
        vals = [vertex_form(V, X) for X in GP]
        VAL[fi] = vals
        for X, v in zip(GP[::7], vals[::7]):     # the grid lemma for the identity vertex = fan needs every point; done below for regions
            pass
        Xc = f['X']; om = vertex_form(V, Xc)
        if not om > 0: pos_ok = False
        pa = polar_area2(V, Xc)
        if not K.zero(om - pa, abs(om)): polar_ok = False
    for f in odd:
        fi = faces.index(f); V = f['V']
        for X, v in zip(GP, VAL[fi]):
            if not K.zero(v - fan_form(V, X), abs(v) + 1): vf_ok = False; break
    check(vf_ok, f'{name}: each of the {len(odd)} regions: vertex formula = fan triangulation at all {len(GP)} grid points (grid lemma: identity of forms)')
    check(pos_ok and polar_ok, f'{name}: every face: Omega > 0 inside and Omega = 2 * area of the polar at its centroid (chunk-2 bridge)')
    # Q2: faces inside each triangle sum to the triangle
    tri_ok = True
    for i in range(1, 10):
        Vt = triangle_V(Y, i)
        inside = [fi for fi, f in enumerate(faces) if i in f['tris']]
        for g, X in enumerate(GP):
            if not K.zero(sum(VAL[fi][g] for fi in inside) - vertex_form(Vt, X), abs(vertex_form(Vt, X)) + 1): tri_ok = False; break
    check(tri_ok, f'{name}: positive control (known region sum): in each of the nine triangles the faces sum to the triangle\'s form '
          f'(every inner wall cancels), all grid points')
    # whole-yantra form and the valuation identity
    TI = intersections(K, Y, lines)
    nI = {k: sum(1 for I in TI if len(I) == k) for k in range(1, 10)}
    OY = [sum(VAL[faces.index(f)][g] for f in odd) for g in range(len(GP))]
    RHS = [sum((-2) ** (len(I) - 1) * vertex_form(V, X) for I, V in TI.items()) for X in GP]
    val_ok = all(K.zero(a - b, abs(a) + 1) for a, b in zip(OY, RHS))
    check(val_ok, f'{name}: valuation identity: sum of the {len(odd)} regions = sum over I of (-2)^(|I|-1) Omega(cap T_I) '
          f'({len(TI)} nonempty intersections, by size {[nI[k] for k in range(1, 10) if nI[k]]}), all {len(GP)} grid points (grid lemma)')
    plain = [sum(VAL[fi][g] * faces[fi]['c'] for fi in range(len(faces))) for g in range(len(GP))]
    nine = [sum(vertex_form(triangle_V(Y, i), X) for i in range(1, 10)) for X in GP]
    check(all(K.zero(a - b, abs(a) + 1) for a, b in zip(plain, nine)), f'{name}: sum of the nine triangles = sum of faces weighted by c')
    # negative: one region's sign flipped
    f0 = faces.index(odd[0])
    flipped = [a - 2 * VAL[f0][g] for g, a in enumerate(OY)]
    check(not all(K.zero(a - b, abs(a) + 1) for a, b in zip(flipped, RHS)), f'{name}: negative control: one region with its sign flipped breaks the valuation identity')
    Vn = odd[0]['V']; Xt = GP[100]
    check(not K.zero(vertex_form(Vn, Xt, flip=0) - fan_form(Vn, Xt), 1), f'{name}: negative control: one flipped normal breaks vertex = fan')
    # numerator N = Omega_Y * prod of the 27 side lines
    Nvals = [[OY[i * GRID + j] * P27[i * GRID + j] for j in range(GRID)] for i in range(GRID)]
    C = interpolate(K, xs, ys, Nvals)
    cscale = max(abs(C[a][b]) for a in range(GRID) for b in range(GRID))
    top = max((a + b for a in range(GRID) for b in range(GRID) if not K.zero(C[a][b], cscale)), default=-1)
    check(top <= 24, f'{name}: numerator N of the whole-yantra form has degree {top} (bound 24 from 27 lines)')
    res['degN'] = top
    # every side line is a pole: N not zero on it
    poles = 0
    for j, l in enumerate(lines):
        P0, P1 = S[j][0], S[j][1]
        X = (P0[0] + (P1[0] - P0[0]) * K.c(Fr(3, 7)), P0[1] + (P1[1] - P0[1]) * K.c(Fr(3, 7)))
        if not K.zero(deriv_at(C, X, 0, 0), deriv_at(C, X, 0, 0, True)): poles += 1
    check(poles == 27, f'{name}: every one of the 27 sides is a pole line of the whole-yantra form ({poles})')
    # Q3: points where two or more side lines meet
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
    table = {}; residues = {}; marma_pts = []; rows = []
    for p in PP.pts:
        th = [j for j, l in enumerate(lines) if K.zero(Lval(l, p), 1)]
        m = len(th)
        def seg_par(j):
            P0, P1 = S[j][0], S[j][1]
            dx, dy = P1[0] - P0[0], P1[1] - P0[1]
            return ((p[0] - P0[0]) * dx + (p[1] - P0[1]) * dy) / (dx * dx + dy * dy)
        par = {j: seg_par(j) for j in th}
        inner = [j for j in th if not K.le(par[j], 0) and not K.le(1, par[j])]
        onseg = [j for j in th if K.le(0, par[j]) and K.le(par[j], 1)]
        cn = [c for c in corners if K.zero(c[0][0] - p[0]) and K.zero(c[0][1] - p[1])]
        if cn:
            kinds = {c[2] for c in cn}
            touch = [j for j in inner if all(S[j][2] != c[1] for c in cn)]
            if touch:
                typ = ('tip on a base' if 'apex' in kinds and any(S[j][3] == 'base' for j in touch) else
                       'corner touch' if 'base corner' in kinds else 'apex on a side')
            else:
                typ = 'triangle corner'
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
            if any(nz(al, o - al) for al in range(o + 1)):
                k = o; break
        kk = k if k is not None else '>=4'
        r = None
        if m == 2 and k == 0:
            R = math.prod(Lval(lines[j], p) for j in range(27) if j not in th)
            n1, n2 = lines[th[0]][:2], lines[th[1]][:2]
            r = deriv_at(C, p, 0, 0) / (R * det2(n1, n2))
        key = (typ, m, kk)
        table[key] = table.get(key, 0) + 1
        if r is not None:
            rr = round(float(abs(r)), 9)
            residues.setdefault(typ, {}); residues[typ][rr] = residues[typ].get(rr, 0) + 1
        if typ == 'marma': marma_pts.append(p)
        rows.append((typ, tuple(sorted((S[j][2], j % 3) for j in th)), kk, None if r is None else abs(r), (float(p[0]), float(p[1]))))
    for key in sorted(table, key=str):
        log(f'{name}:   {key[0]:24s} lines through it m = {key[1]}, N vanishes to order k = {key[2]}: {table[key]} points')
    for typ, d in residues.items():
        log(f'{name}:   point residue |Res| at {typ}s (m = 2, k = 0): {d}')
    log(f'{name}:   {far} crossings of extended side lines lie beyond the box |x| <= 3, |y - 1/2| <= 3 (not classified)')
    check(all(k != 0 for (t, m, k) in table if 'outside' in t), f'{name}: at every crossing of extended lines off the drawn sides (in the box) N vanishes '
          f'(order >= 1: no point residue, the adjoint zeros)')
    nm = sum(v for (t, m, k), v in table.items() if t == 'marma'); ns = sum(v for (t, m, k), v in table.items() if t == 'sandhi')
    check(nm == 18 and ns == 24, f'{name}: traditional counts: {nm} marmas, {ns} sandhis (18, 24)')
    check(all(k == 2 for (t, m, k) in table if t == 'marma'), f'{name}: at every marma N vanishes to order exactly 2 (the three alternate sectors cancel: no point residue)')
    check(residues.get('sandhi') and set(residues['sandhi']) == {2.0}, f'{name}: at every sandhi the point residue is 2 (the two opposite regions add)')
    res['table'] = {str(k): v for k, v in table.items()}; res['residues'] = {t: {str(a): b for a, b in d.items()} for t, d in residues.items()}
    res['rows'] = rows
    # mis-joined wall control
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
    mid = ((pA[0] + pB[0]) / 2, (pA[1] + pB[1]) / 2)
    nrm = (-(pB[1] - pA[1]), pB[0] - pA[0])
    def expo(fn):
        e1, e2 = K.c(Fr(1, 10 ** 20)), K.c(Fr(1, 10 ** 40))
        v1 = fn((mid[0] + e1 * nrm[0], mid[1] + e1 * nrm[1])); v2 = fn((mid[0] + e2 * nrm[0], mid[1] + e2 * nrm[1]))
        return math.log10(abs(float(v2)) / abs(float(v1))) / 20
    good = expo(lambda X: vertex_form(F['V'], X) + vertex_form(G['V'], X))
    dl = K.c(Fr(1, 1000))
    Gs = [(v[0] + dl * nrm[0], v[1] + dl * nrm[1]) for v in G['V']]
    badj = expo(lambda X: vertex_form(F['V'], X) + vertex_form(Gs, X))
    check(abs(good) < 0.05 and abs(badj - 1) < 0.05, f'{name}: wall control: region + its even neighbour: pole exponent on the shared wall {good:.3f} '
          f'(cancels); neighbour moved 1/1000 off the wall: {badj:.3f} (pole left, negative control)')
    # values for the precision comparison
    tests = [K.c(Fr(1, 9)), K.c(Fr(1, 2)), K.c(Fr(2, 7))]
    res['fp'] = [vertex_form(odd[0]['V'], (tests[0], tests[2]))] + [sum(vertex_form(f['V'], (tests[0], t)) for f in odd) for t in tests]
    bindu = [f for f in odd if f['c'] == 9]
    if bindu:
        X0 = (K.c(0), K.c(Fr(1, 2)))
        res['bindu'] = (vertex_form(bindu[0]['V'], X0), sum(vertex_form(f['V'], X0) for f in odd))
        log(f'{name}: at the circle centre (0, 1/2): Omega(bindu region) = {float(res["bindu"][0]):.12g}, Omega_Y = {float(res["bindu"][1]):.12g}')
    res['pattern'] = sorted((tuple(sorted(f['tris'])), tuple(sorted((S[j][2], j % 3) for j in f['lines']))) for f in faces)
    res['marmas'] = marma_pts
    return ok, res


# ---------------------------------------------------------------- tasks
def task_lemmas(_):
    import sympy as sp
    out = []; ok = True
    def check(c, m):
        nonlocal ok
        ok = ok and bool(c); out.append(('ok   ' if c else 'FAIL ') + m)
    X = sp.symbols('X1 X2'); Xv = sp.Matrix(X)
    def om(ra, rb):
        d = lambda u, v: u[0] * v[1] - u[1] * v[0]
        return d(ra, rb) / (d(ra, X) * d(X, rb))
    for k in (2, 3, 4, 5):
        ps = sp.symbols(f'p1:{k + 1}'); qs = sp.symbols(f'q1:{k + 1}')
        r = [(ps[i], qs[i]) for i in range(k)] + [(-ps[i], -qs[i]) for i in range(k)]
        sec = [om(r[i], r[(i + 1) % (2 * k)]) for i in range(2 * k)]
        s_in = sp.cancel(sp.together(sum(sec[0::2]))); s_out = sp.cancel(sp.together(sum(sec[1::2])))
        if k % 2:
            check(s_in == 0 and s_out == 0, f'lemma: {k} lines through a point, alternate sectors: both sums are 0 (symbolic rays)')
        else:
            half = sp.cancel(sp.together(sum(sec[0:k:2]))) if k > 2 else sec[0]
            check(s_in != 0 and sp.cancel(s_in - 2 * half) == 0, f'lemma: {k} lines through a point, alternate sectors: sum = 2 x (alternate sectors of a half-turn) != 0')
    p = sp.symbols('a1 a2 b1 b2 c1 c2')
    ra, rb, rc = (p[0], p[1]), (p[2], p[3]), (p[4], p[5])
    check(sp.cancel(om(ra, rb) + om(rb, rc) - om(ra, rc)) == 0, 'lemma: sectors add (Pluecker): Omega(a,b) + Omega(b,c) = Omega(a,c)')
    # positive controls: plain triangle and a triangle cut in four
    K = Ctx()
    V = [(Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1))]
    pts = [(Fr(1, 3), Fr(1, 3)), (Fr(2, 9), Fr(5, 11)), (Fr(-3, 7), Fr(9, 4))]
    check(all(vertex_form(V, Xp) == fan_form(V, Xp) == 1 / (Xp[0] * Xp[1] * (1 - Xp[0] - Xp[1])) for Xp in pts), 'positive control: plain triangle: vertex = fan = 1/(xy(1-x-y))')
    check(polar_area2(V, pts[0]) == 27, 'positive control: plain triangle: 2 * polar area at (1/3, 1/3) = 27 = Omega')
    x, y = sp.symbols('x y')
    T = [(sp.Integer(0), sp.Integer(0)), (sp.Integer(3), sp.Integer(1)), (sp.Integer(1), sp.Integer(4))]
    M = [((T[i][0] + T[(i + 1) % 3][0]) / 2, (T[i][1] + T[(i + 1) % 3][1]) / 2) for i in range(3)]
    pieces = [[T[0], M[0], M[2]], [M[0], T[1], M[1]], [M[2], M[1], T[2]], [M[0], M[1], M[2]]]
    s = sum(vertex_form(Pc, (x, y)) for Pc in pieces)
    check(sp.cancel(s - vertex_form(T, (x, y))) == 0, 'positive control: a triangle cut in four by its midlines sums back to the triangle (symbolic)')
    s2 = sum(vertex_form(Pc, (x, y)) for Pc in pieces[:3]) - vertex_form(pieces[3], (x, y))
    check(sp.cancel(s2 - vertex_form(T, (x, y))) != 0, 'negative control: the same with the middle piece subtracted does not sum back')
    return 'lemmas', ok, out, {}


def task_yantra(arg):
    name, dps = arg
    out = []
    log = lambda m: out.append(m)
    K = Ctx(dps)
    t0 = time.time()
    if name == 'R1':
        Y = load_r1(K); ok0 = True
    elif name == 'R1-broken':
        return task_broken()
    else:
        Y, ok0 = load_gf1(K, log)
        log(('ok   ' if ok0 else 'FAIL ') + f'{name}: DICTO Yantra rebuilt from its degree-160 polynomial at {dps} digits')
    ok, res = analyse(K, Y, name, log)
    res['fp'] = [str(v) for v in res['fp']]
    res.pop('marmas', None)
    if 'bindu' in res: res['bindu'] = [str(v) for v in res['bindu']]
    res['rows'] = [(a, b, c, None if d is None else str(d), e) for a, b, c, d, e in res['rows']]
    log(f'{name}: {time.time() - t0:.0f} s')
    return name, ok and ok0, out, res


def task_broken():
    """negative control: R1 with the base of t2 moved 1/1000: the marma (1,2,7) splits."""
    out = []; log = lambda m: out.append(m)
    K = Ctx()
    Y0 = load_r1(K)
    l1 = line_of((Y0[1][1], Y0[1][0]), (0, Y0[1][2])); l7 = line_of((Y0[7][1], Y0[7][0]), (0, Y0[7][2]))
    d = l1[0] * l7[1] - l1[1] * l7[0]
    p0 = ((l1[1] * l7[2] - l1[2] * l7[1]) / d, (l1[2] * l7[0] - l1[0] * l7[2]) / d)
    Y = load_r1(K, shift=(2, Fr(1, 1000)))
    ok, res = analyse(K, Y, 'R1-broken', lambda m: out.append('     [broken figure, not asserted] ' + m))
    P0 = (float(p0[0]), float(p0[1]))
    near = [r for r in res['rows'] if abs(r[4][0] - P0[0]) < 0.01 and abs(r[4][1] - P0[1]) < 0.01]
    for r in near:
        out.append(f'     [broken figure] near the old marma (1,2,7): {r[0]}, sides {r[1]}, k = {r[2]}, |Res| = {None if r[3] is None else float(r[3])}')
    nm = sum(1 for r in res['rows'] if r[0] == 'marma')
    cond = (nm < 18 and len(near) >= 3 and not any(r[0] == 'marma' for r in near)
            and all(r[2] == 0 and r[3] is not None and float(r[3]) > 0.5 for r in near if len(r[1]) == 2 and 'outside' not in r[0]))
    out.append(('ok   ' if cond else 'FAIL ') + f'negative control (broken marma): R1 with t2\'s base moved 1/1000: {nm} marmas left (18 before); '
               f'within 1/100 of the old marma (1,2,7) {len(near)} separate crossings, no triple point, and every two-side crossing there is a '
               f'genuine point pole (k = 0, nonzero residue): the order-2 zero needs exact concurrency')
    return 'R1-broken', cond, out, {}


def main():
    t0 = time.time()
    tasks = [('lemmas', None), ('R1', None), ('GF1', 150 if PILOT else 300)] + ([] if PILOT else [('GF1', 600), ('R1-broken', None)])
    print(f'chunk 5c: {len(tasks)} tasks on 4 cores', flush=True)
    results = {}; ok = True; done = 0
    with get_context('fork').Pool(4) as pool:
        its = [pool.apply_async(task_lemmas if t[0] == 'lemmas' else task_yantra, ((t[0], t[1]),)) for t in tasks]
        for it in its:
            name, good, out, res = it.get()
            done += 1
            for line in out: print(line, flush=True)
            print(f'PROGRESS {done / len(tasks):.2f} {name}', flush=True)
            results.setdefault(name, []).append(res); ok = ok and good
    # R1 and GF1: same crossing pattern?
    r1 = results['R1'][0]; g = results['GF1']
    drawn = lambda tb: {k: v for k, v in tb.items() if not k.startswith("('outside")}
    same = r1['pattern'] == g[0]['pattern'] and drawn(r1['table']) == drawn(g[0]['table'])
    if not same:
        a, b = set(r1['pattern']), set(g[0]['pattern'])
        print(f'  pattern: faces only in R1 {sorted(a - b)[:6]}; only in GF1 {sorted(b - a)[:6]}', flush=True)
        print(f'  point table R1 {r1["table"]}', flush=True)
        print(f'  point table GF1 {g[0]["table"]}', flush=True)
    print(('ok   ' if same else 'FAIL ') + 'R1 and the DICTO Yantra have the same crossing pattern (all 74 faces with their triangles and side lines; '
          'every point on the drawn sides with its type, m and k): the exact R1 results carry over as structure', flush=True)
    ok = ok and same
    if len(g) == 2:
        import mpmath as mp
        mp.mp.dps = 320
        a, b = [mp.mpf(v) for v in g[0]['fp']], [mp.mpf(v) for v in g[1]['fp']]
        dev = max(abs(x - y) / abs(y) for x, y in zip(a, b))
        ra = [mp.mpf(r[3]) for r in g[0]['rows'] if r[3]]; rb = [mp.mpf(r[3]) for r in g[1]['rows'] if r[3]]
        dev2 = max(abs(x - y) for x, y in zip(ra, rb)) if len(ra) == len(rb) else mp.mpf(1)
        st = g[0]['table'] == g[1]['table'] and g[0]['pattern'] == g[1]['pattern']
        c = dev < mp.mpf(10) ** -200 and dev2 < mp.mpf(10) ** -200 and st
        print(('ok   ' if c else 'FAIL ') + f'DICTO Yantra at 300 and 600 digits: same pattern and point table; values agree to {mp.nstr(dev, 3)}, residues to {mp.nstr(dev2, 3)}', flush=True)
        ok = ok and c
    json.dump({k: [{kk: vv for kk, vv in r.items() if kk not in ('pattern', 'rows')} for r in v] for k, v in results.items()},
              open(os.path.join(HERE, '..', 'data', 'yantra-regions-pilot.json' if PILOT else 'yantra-regions.json'), 'w'), indent=1, default=str)
    print(f'total {time.time() - t0:.0f} s', flush=True)
    print('FINAL ok' if ok else 'FINAL FAIL: see the FAIL lines above', flush=True)


if __name__ == '__main__':
    main()
