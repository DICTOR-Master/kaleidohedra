"""Aim 1, step 5a (DICTO 10 Nov 2026; checks 16 Nov 2026): the icosahedral line at TILE level, not only projection data.
Scheme at x: lattice Z^6, physical map P(x) (step 4), internal map Q_x = P(-1/x) (rows orthogonal to those of P(x): P(x) Q_x^T = 0),
strip direction E(x) = row space of P(x), window W_x = Q_x([-1/2,1/2]^6) (canonical: de Bruijn 1981, Duneau-Katz 1985, Elser 1986,
Katz-Duneau 1986 for the icosahedral case). Lifted vertex set L(x, w) = { n in Z^6 : Q_x n in W_x + w }; x = F(n+1)/F(n) a cubic
approximant (crystal), x = phi the icosahedral quasicrystal.
Claims checked here:
 (1) symbolic, all x > 0: P(x) A = (2x+1) P(g(x)) (step 4) AND Q_g(x) A = k(x) Q_x with k(x) = -x/(3x+2) (k(phi) = -phi^-3);
     hence A L(x, w) = { m : Q_g m in k W_x + k w }: the inflated crystal at x is the model set of the strip of g(x) with window k W_x.
     Periods: P(g)A - s(x)P(x) vanishes on E(x), s(x) = (2x+1)(1+g^2)/(1+x^2), so the period lattice of T(g(x)) is s(x) times that of
     T(x) (s(phi) = phi^3); vertices move by a bounded phason displacement, zero only at phi.
 (2) symbolic, all x > 0: |k(x)| W_x is contained in W_g(x) (support functions at all 15 facet normals of W_g, exact sign analysis),
     so A L(x, w) is a subset of L(g(x), k w): every vertex of the inflated crystal at x is a vertex of the crystal at g(x).
     |k| W_x is a homothetic copy of W_g(x) only at x = phi.
 (3) exact enumeration for the pairs 1/1 -> 5/3, 2/1 -> 8/5, 3/2 -> 13/8: vertices and the 20 tile types per period, inclusion of the
     inflated vertex set, density = |k|^3 vol W_x / vol W_g, tile counts = volume x x^-3 / covolume (Pluecker duality), total tile volume =
     cell volume, period lattices similar with ratio s(x).
 Controls: positive: the turn x -> 1/x (found here: x P(1/x) = R P(x) S, S a signed permutation) maps L(2) ONTO L(1/2) exactly;
 negative: A does not carry the strip of x to the strip of h(x) (one Fibonacci hop) nor of g(g(x)): a period of T(x) leaves it.
usage: python3 ico_tiles.py [pairs]   (pairs default: 1,3/2,2,5/3,1/2)"""
import sys, itertools, time
from fractions import Fraction as Fr
import sympy as sp
T0 = time.time()
def prog(msg): print(f'PROGRESS [{time.time()-T0:7.1f}s] {msg}', flush=True)
x = sp.symbols('x', positive=True); phi = (1 + sp.sqrt(5)) / 2
def P(t): return sp.Matrix([[1, -1, 0, 0, t, -t], [t, t, 1, -1, 0, 0], [0, 0, t, t, 1, 1]])
def Q(t): return P(-1 / t)
A = sp.Matrix([[2, 1, 1, -1, 1, -1], [1, 2, 1, -1, -1, 1], [1, 1, 2, 1, 1, 1], [-1, -1, 1, 2, 1, 1], [1, -1, 1, 1, 2, -1], [-1, 1, 1, 1, -1, 2]])
def g(t): return (3 * t + 2) / (2 * t + 1)
def h(t): return 1 + 1 / t
k = -x / (3 * x + 2); s = (2 * x + 1) * (1 + g(x) ** 2) / (1 + x ** 2)
OK = {}
Z36 = sp.zeros(3, 6); Z33 = sp.zeros(3, 3)
OK['P Q^T = 0'] = sp.simplify(P(x) * Q(x).T) == Z33
OK['A symmetric, det -1'] = A == A.T and A.det() == -1
OK['P(x) A = (2x+1) P(g)'] = sp.simplify(P(x) * A - (2 * x + 1) * P(g(x))) == Z36
OK['Q_g A = k Q_x'] = sp.simplify(Q(g(x)) * A - k * Q(x)) == Z36
OK['phason part vanishes on E(x)'] = sp.simplify((P(g(x)) * A - s * P(x)) * P(x).T) == Z33
OK['k(phi) = -phi^-3, s(phi) = phi^3'] = sp.simplify(k.subs(x, phi) + phi ** -3) == 0 and sp.simplify(s.subs(x, phi) - phi ** 3) == 0
OK['phason part nonzero off phi'] = sp.simplify((P(g(x)) * A - s * P(x)).subs(x, 2)) != Z36
prog('(1) symbolic hop identities: ' + str(all(OK.values())))
# the turn x -> 1/x: find R, S with x P(1/x) = R P(x) S
R = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]]); RP = R * P(x); M = sp.expand(x * P(1 / x)); S = sp.zeros(6, 6)
for j in range(6):
    for i in range(6):
        for sg in (1, -1):
            if sp.simplify(M[:, j] - sg * RP[:, i]) == sp.zeros(3, 1): S[i, j] = sg
OK['turn: x P(1/x) = R P(x) S, S signed permutation'] = sp.simplify(x * P(1 / x) - R * P(x) * S) == Z36 and all(sum(abs(S[i, j]) for j in range(6)) == 1 for i in range(6))
OK['turn on internal maps: Q_(1/x) = -x R Q_x S'] = sp.simplify(Q(1 / x) + x * R * Q(x) * S) == Z36
prog(f'(1b) turn x -> 1/x, S = {S.tolist()}: {OK["turn: x P(1/x) = R P(x) S, S signed permutation"] and OK["turn on internal maps: Q_(1/x) = -x R Q_x S"]}')

# (2) window containment |k| W_x in W_g for all x > 0
def gens(t): Qt = Q(t); return [Qt[:, l] for l in range(6)]
def hsupp(u, G): return sum(sp.Abs(u.dot(v)) for v in G) / 2
Gx, Gg = gens(x), gens(g(x))
pairs15 = list(itertools.combinations(range(6), 2))
def lam_max_at(val):      # exact largest lambda with lambda |k| W_x in W_g at x = val
    Gx_, Gg_ = gens(val), gens(g(val)); kk = abs(k.subs(x, val)); best = None
    for i, j in pairs15:
        u = Gg_[i].cross(Gg_[j])
        if u == sp.zeros(3, 1): continue
        r = sp.nsimplify(sp.simplify(hsupp(u, Gg_) / (kk * hsupp(u, Gx_))))
        best = r if best is None or sp.N(r - best) < 0 else best
    return sp.simplify(best)
def containment_all_x(factor):
    """exact: is factor*|k| W_x inside W_g(x) for every x > 0? sign analysis of the 15 support-function inequalities."""
    cont_ok = True; tight = []
    for i, j in pairs15:
        u = sp.simplify(Gg[i].cross(Gg[j]))
        terms_g = [sp.together(u.dot(v)) for v in Gg]; terms_x = [sp.together(u.dot(v)) for v in Gx]
        crit = set()
        for e in terms_g + terms_x:
            num = sp.numer(sp.together(e))
            if num != 0:
                for r in sp.Poly(num, x).real_roots():
                    if r > 0: crit.add(r)
        crit = sorted(crit, key=lambda r: sp.N(r, 30))
        pts = [sp.Integer(0)] + crit
        samples = [(pts[m] + pts[m + 1]) / 2 for m in range(len(pts) - 1)] + [pts[-1] + 1]
        bounds = list(zip(pts, pts[1:] + [sp.oo]))
        for smp, (lo, hi) in zip(samples, bounds):
            sg = lambda e: sp.sign(e.subs(x, smp))
            Fexpr = sum(sg(e) * e for e in terms_g) / 2 - factor * (-k) * sum(sg(e) * e for e in terms_x) / 2   # -k = |k| > 0
            Fexpr = sp.together(sp.simplify(Fexpr))
            num, den = sp.fraction(Fexpr)
            if num == 0: tight.append(((i, j), 'identically equal on', (lo, hi))); continue
            inside = lambda r: sp.N(r, 30) > sp.N(lo, 30) and (hi == sp.oo or sp.N(r, 30) < sp.N(hi, 30))
            roots_in = [r for r in sp.Poly(num, x).real_roots() if inside(r)]
            dens_in = [r for r in sp.Poly(den, x).real_roots() if inside(r)]
            if Fexpr.subs(x, smp) < 0 or dens_in: cont_ok = False
            for r in roots_in:      # a root inside the interval: F may only touch 0 there
                eps = sp.Rational(1, 10 ** 6); ev = lambda t: Fexpr.subs(x, t)
                if sp.N(ev(r - eps), 30) < 0 or sp.N(ev(r + eps), 30) < 0: cont_ok = False
                tight.append(((i, j), 'touches at x =', sp.N(r, 12)))
    return cont_ok, tight
cont_ok, tight = containment_all_x(1)
OK['NEG: 5|k| W_x inside W_g(x) for every x > 0 must FAIL'] = not containment_all_x(5)[0]
OK['|k| W_x inside W_g(x) for every x > 0'] = cont_ok
prog(f'(2) window containment for all x > 0 (15 facet normals, exact sign analysis): {cont_ok}; touching: {tight[:6]}; NEG factor 5 fails: {OK["NEG: 5|k| W_x inside W_g(x) for every x > 0 must FAIL"]}')
# homothety only at phi: generator (1, w, 0) direction fixes w; W_x generators have w = -1/x, W_g has w = -1/g(x)
OK['homothetic only at phi'] = sp.solve(sp.Eq(-1 / x, -1 / g(x)), x) == [phi] or sp.simplify(sp.solve(sp.Eq(-1 / x, -1 / g(x)), x)[0] - phi) == 0
lm = {}
for val in (sp.Rational(1, 100), sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2), sp.Integer(2), sp.Rational(5, 3), sp.Integer(100), phi):
    lm[val] = lam_max_at(val)
prog('(2b) largest lambda with lambda |k| W_x in W_g: ' + ', '.join(f'x = {v}: {sp.nsimplify(lv)} = {sp.N(lv, 8)}' for v, lv in lm.items()))
OK['lambda_max(phi) = phi^3'] = sp.simplify(lm[phi] - phi ** 3) == 0
OK['lambda_max >= 1 at the approximants'] = all(lv >= 1 for v, lv in lm.items() if v != phi)

# (3) exact enumeration
def col_hnf(Mi):
    M = [row[:] for row in Mi]; n = len(M[0]); U = [[int(i == j) for j in range(n)] for i in range(n)]
    def colop(c, d, q):       # col_c -= q col_d
        for r in range(len(M)): M[r][c] -= q * M[r][d]
        for r in range(n): U[r][c] -= q * U[r][d]
    def swap(c, d):
        for r in range(len(M)): M[r][c], M[r][d] = M[r][d], M[r][c]
        for r in range(n): U[r][c], U[r][d] = U[r][d], U[r][c]
    for r in range(len(M)):
        while True:
            nz = [c for c in range(r, n) if M[r][c] != 0]
            c0 = min(nz, key=lambda c: abs(M[r][c])); swap(r, c0)
            done = True
            for c in range(r + 1, n):
                if M[r][c]: colop(c, r, M[r][c] // M[r][r]); done = done and M[r][c] == 0
            if all(M[r][c] == 0 for c in range(r + 1, n)): break
        if M[r][r] < 0:
            for rr in range(len(M)): M[rr][r] = -M[rr][r]
            for rr in range(n): U[rr][r] = -U[rr][r]
    return M, U
def det3(m): return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def dot(a, b): return sum(p * q for p, q in zip(a, b))
def Pr(t): return [[1, -1, 0, 0, t, -t], [t, t, 1, -1, 0, 0], [0, 0, t, t, 1, 1]]
def apply(Mx, v): return [sum(Mx[r][c] * v[c] for c in range(len(v))) for r in range(len(Mx))]
TRIPLES = list(itertools.combinations(range(6), 3))
class Scheme:
    """canonical tiling at rational x, internal coordinates scaled by a = numerator of x (generators integer)."""
    def __init__(self, xv, w):
        self.x = Fr(xv); self.a = self.x.numerator
        Qs = [[int(self.a * e) for e in row] for row in Pr(-1 / self.x)]          # a Q_x, integer 3 x 6
        self.Qs = Qs; self.G = [[Qs[r][l] for r in range(3)] for l in range(6)]
        self.B, self.U = col_hnf(Qs)
        self.periods = [[self.U[r][c] for r in range(6)] for c in range(3, 6)]
        assert all(apply(Qs, t) == [0, 0, 0] for t in self.periods)
        self.covol = abs(self.B[0][0] * self.B[1][1] * self.B[2][2])
        self.w = [self.a * c for c in w]                                          # scaled shift
        self.normals = []
        for i, j in itertools.combinations(range(6), 2):
            u = cross(self.G[i], self.G[j])
            if any(u): self.normals.append((u, Fr(sum(abs(dot(u, v)) for v in self.G), 2)))
        self.volW = sum(abs(det3([self.G[i], self.G[j], self.G[l]])) for i, j, l in TRIPLES)
    def inside(self, z, generic_check=True):
        for u, hh in self.normals:
            d = abs(dot(u, z) - dot(u, self.w))
            if d == hh: raise ValueError('non-generic shift: lattice point on the window boundary')
            if d > hh: return False
        return True
    def enumerate(self):
        B = self.B; ext = [sum(abs(self.G[l][r]) for l in range(6)) / 2 + abs(self.w[r]) + 1 for r in range(3)]
        out = []
        import math
        lo0, hi0 = math.floor(-ext[0]), math.ceil(ext[0])
        for c0 in range(lo0 // B[0][0] - 1, hi0 // B[0][0] + 2):
            z0 = B[0][0] * c0
            if not -ext[0] <= z0 <= ext[0]: continue
            b1 = B[1][0] * c0
            for c1 in range(math.floor((-ext[1] - b1) / B[1][1]) - 1, math.ceil((ext[1] - b1) / B[1][1]) + 2):
                z1 = b1 + B[1][1] * c1
                if not -ext[1] <= z1 <= ext[1]: continue
                b2 = B[2][0] * c0 + B[2][1] * c1
                for c2 in range(math.floor((-ext[2] - b2) / B[2][2]) - 1, math.ceil((ext[2] - b2) / B[2][2]) + 2):
                    z2 = b2 + B[2][2] * c2
                    if not -ext[2] <= z2 <= ext[2]: continue
                    z = [z0, z1, z2]
                    if self.inside(z): out.append((tuple(z), (c0, c1, c2)))
        self.pts = out; return out
    def lift(self, c):
        return [sum(self.U[r][m] * c[m] for m in range(3)) for r in range(6)]
    def tile_counts(self):
        """tile of type I at vertex n (Oguey-Duneau-Katz): Q(n + e_I/2) - w in Q([-1/2,1/2]^(I^c)) (half-open)."""
        cnt = {}
        for I in TRIPLES:
            Ic = [l for l in range(6) if l not in I]; Mc = [self.G[l] for l in Ic]   # columns
            Mt = [[Mc[cc][r] for cc in range(3)] for r in range(3)]; D = det3(Mt)
            if D == 0: cnt[I] = 0; continue
            # inverse via adjugate
            inv = [[Fr(0)] * 3 for _ in range(3)]
            for r in range(3):
                for cc in range(3):
                    minor = [[Mt[rr][c2] for c2 in range(3) if c2 != r] for rr in range(3) if rr != cc]
                    inv[r][cc] = Fr((-1) ** (r + cc) * (minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0]), D)
            half = [Fr(sum(self.G[i][r] for i in I), 2) for r in range(3)]
            n_ = 0
            for z, _ in self.pts:
                v = [z[r] + half[r] - self.w[r] for r in range(3)]
                co = [sum(inv[r][cc] * v[cc] for cc in range(3)) for r in range(3)]
                if all(Fr(-1, 2) <= cf < Fr(1, 2) for cf in co): n_ += 1
            cnt[I] = n_
        return cnt
    def tile_vol(self, I):
        Pm = Pr(self.x); return abs(det3([[Pm[r][i] for r in range(3)] for i in I]))
    def cell_vol(self):
        Pm = Pr(self.x); return abs(det3([apply(Pm, t) for t in self.periods]))

def run_pair(xv, w):
    xv = Fr(xv); gv = Fr(3 * xv + 2, 2 * xv + 1); kv = -xv / (3 * xv + 2); sv = (2 * xv + 1) * (1 + gv * gv) / (1 + xv * xv)
    S1 = Scheme(xv, w); S2 = Scheme(gv, [kv * c for c in w])
    I1 = S1.enumerate(); I2 = S2.enumerate(); set2 = set(z for z, _ in I2)
    prog(f'pair {xv} -> {gv}: vertices per period {len(I1)} and {len(I2)}')
    res = {}
    res['vertex count = vol W / covol (x)'] = Fr(len(I1)) == Fr(S1.volW, S1.covol)
    res['vertex count = vol W / covol (g)'] = Fr(len(I2)) == Fr(S2.volW, S2.covol)
    Ag = [[int(A[r, c]) for c in range(6)] for r in range(6)]
    Qg = [[S2.a * e for e in row] for row in Pr(-1 / gv)]
    imgs = set(); all_in = True
    for z, c in I1:
        n = S1.lift(c); assert apply(S1.Qs, n) == list(z)
        m = apply(Ag, n); zg = tuple(apply(Qg, m))
        assert all(Fr(v).denominator == 1 for v in zg)
        zg = tuple(int(v) for v in zg); imgs.add(zg); all_in &= zg in set2
    res['A L(x) inside L(g(x))'] = all_in
    res['A injective mod periods'] = len(imgs) == len(I1)
    dens = Fr(len(I1), len(I2)); want = abs(kv) ** 3 * Fr(S1.volW, S1.a ** 3) / Fr(S2.volW, S2.a ** 3)
    res['density = |k|^3 vol W_x / vol W_g'] = dens == want
    res['L(g(x)) strictly larger (no equality)'] = len(I2) > len(I1)
    # periods: A maps the period lattice of x onto that of g, physical ratio s(x)
    Pg = Pr(gv); Px = Pr(xv)
    APer = [apply(Ag, t) for t in S1.periods]
    res['A periods(x) are periods of g'] = all(apply(S2.Qs, t) == [0, 0, 0] for t in APer)
    res['physical periods scale by s(x)'] = all(apply(Pg, t2) == [sv * v for v in apply(Px, t1)] for t1, t2 in zip(S1.periods, APer))
    res['cell volume ratio s^3 (A onto all periods of g)'] = S2.cell_vol() == sv ** 3 * S1.cell_vol()
    # tiles
    for S_, lab in ((S1, 'x'), (S2, 'g')):
        cnt = S_.tile_counts()
        res[f'tile counts = |det Q_(I^c)| / covol ({lab})'] = all(Fr(cnt[I]) == Fr(abs(det3([S_.G[l] for l in range(6) if l not in I])), S_.covol) for I in TRIPLES)
        res[f'tile count proportional to tile volume ({lab})'] = len(set(Fr(cnt[I]) / S_.tile_vol(I) for I in TRIPLES if S_.tile_vol(I) != 0)) == 1 and all(cnt[I] == 0 for I in TRIPLES if S_.tile_vol(I) == 0)
        res[f'total tile volume = cell volume ({lab})'] = sum(cnt[I] * S_.tile_vol(I) for I in TRIPLES) == S_.cell_vol()
        cls = {}
        for I in TRIPLES: cls[S_.tile_vol(I)] = cls.get(S_.tile_vol(I), 0) + cnt[I]
        prog(f'   tiles of T({S_.x}) per period by volume class {{volume: count}}: {dict(sorted(cls.items()))}; total {sum(cnt.values())}')
    # negative controls: A does not carry the strip of x to the strip of h(x) or of g(g(x))
    for lab, yv in (('h(x)', 1 + 1 / xv), ('g(g(x))', Fr(3 * gv + 2, 2 * gv + 1))):
        Qy = Pr(-1 / yv)
        res[f'NEG: A periods(x) leave the strip of {lab}'] = any(apply(Qy, t) != [0, 0, 0] for t in APer)
    for kk, v in res.items(): print(f'   {kk}: {v}')
    return all(res.values()), len(I1), len(I2)

def turn_control(xv, w):
    xv = Fr(xv); S1 = Scheme(xv, w); yv = 1 / xv
    Rm = [[0, 1, 0], [1, 0, 0], [0, 0, 1]]
    # Q_(1/x) S^-1 = -x R Q_x, so S^-1 L(x, w) = L(1/x, -x R w)
    w2 = [-xv * c for c in apply(Rm, w)]
    S2 = Scheme(yv, w2); I1 = S1.enumerate(); I2 = S2.enumerate()
    imgs = set()
    for z, _ in I1:
        zi = [Fr(c, S1.a) for c in z]; zy = [-xv * c for c in apply(Rm, zi)]
        imgs.add(tuple(int(S2.a * c) for c in zy))
    ok = imgs == set(z for z, _ in I2)
    prog(f'POSITIVE CONTROL turn: L(1/x) is the mirror image of L(x) at x = {xv}: {len(I1)} = {len(I2)} vertices, sets equal: {ok}')
    return ok

w0 = [Fr(1, 97), Fr(2, 131), Fr(-3, 173)]
xs = [Fr(a) for a in (sys.argv[1].split(',') if len(sys.argv) > 1 else ['1', '3/2', '2', '5/3', '1/2'])]
OK['POSITIVE turn control'] = turn_control(2, w0)
rows = []
for xv in xs:
    ok, n1, n2 = run_pair(xv, w0); OK[f'pair {xv}'] = ok; rows.append((xv, n1, n2))
for kk, v in OK.items(): print(f'CHECK {kk}: {v}')
print('FINAL ok' if all(OK.values()) else 'FINAL FAIL')
