"""The chain of T with the depth s as a SYMBOL, in FLINT: every corner coordinate is an element of Q(sqrt5)(s) stored as
(A + B sqrt5) / E with A, B, E in Q[s] (fmpq_poly) and gcd(A, B, E) = 1 over Q.  This form is canonical up to a constant:
any rational denominator of N/D is a multiple of lcm(D, conj D), so dividing out the rational gcd reaches the smallest one.
Usage: python sym.py <cube|dodeca> <s0 as p/q> <steps> <lo> <hi>
At the sample s0 the type of every step is read in floating point; each corner is then solved in Q(sqrt5)(s) and
 * every tight incidence must vanish IDENTICALLY in s (else s0 itself is a wall: stop);
 * the walls are the real roots, in (lo, hi), of the free-slack numerators and of the corner determinants: roots of the norm
   A^2 - 5B^2 (FLINT factor + certified root isolation), kept only where A + B sqrt5 itself vanishes (arb: the conjugate
   A - B sqrt5 certified nonzero there); the HOP is the pair of walls nearest to s0;
 * closure: step k equals step j scaled IDENTICALLY in s (every cross product zero in Q(sqrt5)(s), one common ratio).
Then, on the whole hop, the type is fixed and the closure identity holds: the regime is proved on that open interval."""
import sys, time, itertools
import numpy as np
from flint import fmpq, fmpz, arb, fmpq_poly, fmpz_poly, ctx
import fw

ONEP = fmpq_poly([1]); ZEROP = fmpq_poly([])
class RF:
    __slots__ = ('A', 'B', 'E')
    def __init__(z, A, B=None, E=None, red=True):
        z.A = A; z.B = ZEROP if B is None else B; z.E = ONEP if E is None else E
        if red: z._red()
    def _red(z):
        if z.A.is_zero() and z.B.is_zero(): z.E = ONEP; return
        g = z.E.gcd(z.A) if z.B.is_zero() else z.E.gcd(z.A.gcd(z.B)) if not z.A.is_zero() else z.E.gcd(z.B)
        if g.degree() > 0: z.A, z.B, z.E = z.A / g, z.B / g, z.E / g     # exact division
        lc = z.E.leading_coefficient()
        if lc != 1: z.A, z.B, z.E = z.A / lc, z.B / lc, z.E / lc
    def _c(z, o): return o if isinstance(o, RF) else RF(fmpq_poly([o]))
    def __add__(z, o):
        o = z._c(o)
        if z.E == o.E: return RF(z.A + o.A, z.B + o.B, z.E)
        return RF(z.A * o.E + o.A * z.E, z.B * o.E + o.B * z.E, z.E * o.E)
    __radd__ = __add__
    def __neg__(z): return RF(-z.A, -z.B, z.E, red=False)
    def __sub__(z, o): return z + (-z._c(o))
    def __rsub__(z, o): return z._c(o) - z
    def __mul__(z, o):
        o = z._c(o)
        return RF(z.A * o.A + 5 * z.B * o.B, z.A * o.B + z.B * o.A, z.E * o.E)
    __rmul__ = __mul__
    def __truediv__(z, o):
        o = z._c(o); n = o.A * o.A - 5 * o.B * o.B
        assert not n.is_zero(), 'division by zero in Q(sqrt5)(s)'
        return z * RF(o.E * o.A, -o.E * o.B, n)
    def is_zero(z): return z.A.is_zero() and z.B.is_zero()
    def at(z, s):       # arb value
        r5 = arb(5).sqrt()
        return (ev(z.A, s) + ev(z.B, s) * r5) / ev(z.E, s)
def ev(P, x):
    v = arb(0)
    for c in reversed(P.coeffs()): v = v * x + arb(c)
    return v

def const(a, b): return RF(fmpq_poly([a]), fmpq_poly([b]) if b != 0 else None)
S = RF(fmpq_poly([0, 1]))
def start(kind):
    return [(tuple(const(*x) for x in n), const(*p) + const(*q) * S) for n, (p, q) in fw.spec(kind)]

kind, s0 = sys.argv[1], fmpq(*map(int, sys.argv[2].split('/')))
N = int(sys.argv[3]); lo, hi = (fmpq(*map(int, x.split('/'))) for x in sys.argv[4:6])
t0 = time.time()
def log(*x): print(f'[{time.time() - t0:6.1f}s]', *x, flush=True)
types, Vf = fw.float_chain(kind, float(s0), N)

seen = {}            # primitive norm polynomial -> its real roots in (lo, hi), as (fmpz_poly factor, acb root)
def walls_of(x, note):
    """genuine real roots in (lo, hi) of the numerator A + B sqrt5 of x"""
    if x.B.is_zero(): P = x.A
    else: P = x.A * x.A - 5 * x.B * x.B
    if P.degree() < 1: return []
    Pz = P.numer(); c = int(Pz.content()) * (1 if Pz.leading_coefficient() > 0 else -1)
    Pz = fmpz_poly([int(x) // c for x in Pz.coeffs()])
    key = tuple(int(c) for c in Pz.coeffs())
    if key not in seen:
        out = []
        for g, m in Pz.factor()[1]:
            if g.degree() < 1: continue
            for r, mult in g.complex_roots():
                if r.imag.contains(0) and not (r.real < arb(lo)) and not (r.real > arb(hi)):
                    out.append((g, r.real))
        seen[key] = out
    res = []
    ctx.prec = 300
    for g, rr in seen[key]:
        if x.B.is_zero(): res.append((g, rr)); continue
        # refine the root ball, then test which of A +- B sqrt5 vanishes there
        for rt, mult in g.complex_roots():
            if rt.real.overlaps(rr) and rt.imag.contains(0):
                rb = rt.real
        conj = ev(x.A, rb) - ev(x.B, rb) * arb(5).sqrt(); own = ev(x.A, rb) + ev(x.B, rb) * arb(5).sqrt()
        if not conj.contains(0): res.append((g, rb))
        elif not own.contains(0): pass
        else:
            gq = fmpq_poly(g.coeffs())
            if (x.A % gq).is_zero() and (x.B % gq).is_zero(): res.append((g, rb))     # g divides both parts: A + B sqrt5 vanishes
            else: raise RuntimeError(f'cannot decide which conjugate vanishes ({note})')
    return res

planes = start(kind); hist = []; HOP = [None, None]; closed = None
def upd(g, r):
    v = r.mid()
    if v < arb(s0):
        if HOP[0] is None or v > HOP[0][1].mid(): HOP[0] = (g, r)
    elif v > arb(s0):
        if HOP[1] is None or v < HOP[1][1].mid(): HOP[1] = (g, r)
    else: raise RuntimeError('s0 is a wall')
for k in range(N + 1):
    typ = types[k]; V = []
    for j, (tri, T) in enumerate(typ):
        A = [planes[i][0] for i in tri]; b = [planes[i][1] for i in tri]; D = fw.det3(*A)
        for g, r in walls_of(D, 'determinant'): upd(g, r)
        V.append(tuple(fw.det3(*[tuple(b[rr] if kk == col else A[rr][kk] for kk in range(3)) for rr in range(3)]) / D for col in range(3)))
    deg = max(max(x.A.degree(), x.B.degree(), x.E.degree()) for v in V for x in v)
    nfree = 0
    for j, (tri, T) in enumerate(typ):
        Ts = set(T)
        for i in range(len(planes)):
            sl = fw.slack(planes, V[j], i)
            if i in Ts:
                assert sl.is_zero(), f'step {k}: incidence holds only at the sample: s0 is a wall'
            else:
                nfree += 1
                for g, r in walls_of(sl, 'slack'): upd(g, r)
    kinds = fw.kinds_of(typ, len(planes))
    lo_s = '-' if HOP[0] is None else HOP[0][1].mid().str(12); hi_s = '-' if HOP[1] is None else HOP[1][1].mid().str(12)
    log(f'step {k}: {len(V)} corners, kinds {dict(kinds)}; incidences identical in s; {nfree} free slacks; largest degree {deg}; '
        f'hop so far ({lo_s}, {hi_s})')
    for j, (Vj, kj) in enumerate(hist):
        if len(Vj) != len(V) or kj != kinds: continue
        a = np.array(Vf[j]); a /= np.linalg.norm(a, axis=1)[:, None]
        b = np.array(Vf[k]); b /= np.linalg.norm(b, axis=1)[:, None]
        g = None; ok = True
        for vi, v in enumerate(V):
            m = int(np.argmin(np.linalg.norm(a - b[vi], axis=1))); u = Vj[m]
            if not all(x.is_zero() for x in fw.cross(u, v)): ok = False; break
            r = fw.dot(v, v) / fw.dot(u, u)
            if g is None: g = r
            elif not (r - g).is_zero(): ok = False; break
        if ok: closed = (j, k, g); break
    if closed: break
    hist.append((V, kinds))
    if k < N: planes = [(v, fw.dot(v, v)) for v in V]

def show(w):
    if w is None: return 'none in the window'
    g, r = w
    return f'root of {g} in {r.str(25)}'
log(f'HOP of the type around s0 = {s0}: low end {show(HOP[0])}; high end {show(HOP[1])}')
if closed:
    j, k, g = closed
    gs = 'constant ' + str(g.A[0] / g.E[0]) + (f' + ({g.B[0] / g.E[0]}) sqrt5' if not g.B.is_zero() else '') if g.A.degree() < 1 and g.B.degree() < 1 and g.E.degree() < 1 else f'varies with s (degree {max(g.A.degree(), g.B.degree(), g.E.degree())}); at s0 {g.at(arb(s0)).str(12)}'
    log(f'CLOSURE IDENTITY: step {k} = step {j} scaled for every s on the hop; period {k - j}, entered at step {j}; squared radius gain {gs}')
print('FINAL ok' if closed else 'FINAL FAIL: no closure identity within the steps run')
