"""Exact decision for Aequus CIRT-30, T 26 (orbits C6 + I12 + RT24/12a): its C6 and RT24/12a depths are EXACTLY equal.

Certificate (PARI via cypari2 for exact algebra, python-flint arb for rigorous enclosures):
 1. Candidate die: C6 and RT24/12a planes at unit depth 1, I12 planes at depth x/sqrt3, x the real root near 1.758 of
    q(x) = 16x^4 - 40x^3 - 100x^2 + 130x + 145 (q was found by an integer relation on the 60-digit depth; it is used only as a candidate).
    With unnormalised normals u (C6 (1,0,0), I12 (0,1/phi,phi) of norm sqrt3, RT (1/phi,1,phi) of norm 2) the planes are u.v = 1, x, 2,
    so every vertex lies in K = Q(sqrt5, x).
 2. Its 44 vertices: incidences from a 50-digit computation, then each vertex verified exactly (zero in K on its planes) and strictly
    inside every other plane (arb enclosure excluding 0).  So the face lattice is exact.
 3. Solid angle of a face cone (spherical polygon v_1..v_n): Omega = sum phi_k - (n-2) pi, phi_k the interior angle at v_k;
    with m_k = v_k x v_k+1: cos phi_k = alpha_k/(|m_k-1||m_k|), sin phi_k = s_k/(|m_k-1||m_k|), alpha_k = -m_k-1.m_k,
    s_k = sqrt(G_k), G_k = |m_k-1|^2 |m_k|^2 - alpha_k^2 (all in K).  So cos Omega = (-1)^n Re prod(alpha_k + i s_k) / M, M = prod |m_k|^2.
 4. beta = cos Omega - cos(2 pi/15).  Eliminating the s_k (resultants with s^2 - G), gamma = cos(2pi/15) (its minimal polynomial) and
    then x and sqrt5 (resultants) gives P in Q[B] with P(beta) = 0.  Write P = B^k Q, Q(0) != 0.  A nonzero root of Q has
    |root| >= |q_0|/(|q_0| + max|q_i|) (Cauchy).  The arb enclosure of |beta| lies below that bound, so beta = 0; and Omega lies in (0, pi)
    (arb), so Omega = 2 pi/15 = 4 pi/30 exactly.  Done for one C6 face and one RT24/12a face; the 12 I12 faces then have 4 pi/30 as well
    (the 30 cones fill the sphere: 6 + 12 + 12 faces).
 5. So the candidate is a fair die with face normals of CIRT-30.  The fair die of an orbit set is unique up to scale (Alexandrov's
    uniqueness for given normals and curvatures; the search found exactly one), so the fair CIRT-30 is this die: C6 and RT24/12a at exactly
    equal depth, I12 at depth x/sqrt3 (an algebraic number of degree <= 4)."""
import itertools, json, os, sys
import mpmath as mp
import flint
from flint import arb, fmpz_poly, fmpq
from cypari2 import Pari
pari = Pari(); pari.allocatemem(4 * 10**9, silent=True) if hasattr(pari, "allocatemem") else None
mp.mp.dps = 50; flint.ctx.prec = 4000
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import classify as C
def pr(*a): print(*a, flush=True)

D = json.load(open(os.path.join(HERE, "../src/dice.json"))); e = D["dice"][83]
assert e.get("name") == "Aequus CIRT-30, T 26"
ED = C.exact_dirs(D["dirs"])
QX = "16*x^4-40*x^3-100*x^2+130*x+145"
pari("w"); pari("x")
VH = {nm: pari(f'varhigher("{nm}")') for nm in ["B", "g", "s0", "s1", "s2", "s3", "s4", "s5", "s6"]}
def K(a, b=0, xc=0):
    return pari(f"Mod(Mod({a}+({b})*w,w^2-5)+Mod({xc},w^2-5)*x,{QX})")
ZERO = K(0)
def kq(z): return K(str(z.a), str(z.b))     # Q(sqrt5) element of classify.Q -> K
XK = K(0, 0, 1)
# rigorous enclosures of x and sqrt5
roots = [r for r, m in fmpz_poly([145, 130, -100, -40, 16]).complex_roots()]
xr = [r.real for r in roots if abs(float(r.imag.mid())) < 1e-30 and abs(float(r.real.mid()) - 1.7579) < 1e-3]
assert len(xr) == 1; XR = xr[0]; S5 = arb(5).sqrt()
def ev(z):
    """arb enclosure of a K element at (x = XR, w = +sqrt5)"""
    P = pari.lift(pari.lift(z)); tot = arb(0)
    dx = int(pari.poldegree(P, "x")) if P != 0 else 0
    for i in range(dx + 1):
        cx = pari.polcoef(P, i, "x")
        dw = int(pari.poldegree(cx, "w")) if cx != 0 else 0
        for j in range(dw + 1):
            c = pari.polcoef(cx, j, "w")
            if c != 0:
                n, d = int(pari.numerator(c)), int(pari.denominator(c))
                tot += arb(fmpq(n, d)) * XR**i * S5**j
    return tot
orbs = [D["groups"]["T"][oi]["dirs"] for oi in e["o"]]
CONST = [K(1), XK, K(2)]                        # C6, I12, RT24/12a
P = [(ED[i][0], CONST[k], k) for k, ob in enumerate(orbs) for i in ob]
# numeric incidences (50 digits)
xm = mp.mpf(str(XR.mid().str(60, radius=False)))
def fl(z): return mp.mpf(z.a.numerator)/z.a.denominator + mp.mpf(z.b.numerator)/z.b.denominator*mp.sqrt(5)
Pm = [([fl(c) for c in u], [mp.mpf(1), xm, mp.mpf(2)][k]) for u, c_, k in P]
def cr(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
cand = {}
for a, b, c in itertools.combinations(range(len(P)), 3):
    A_, B_, C_ = Pm[a][0], Pm[b][0], Pm[c][0]
    bc, ca, ab = cr(B_, C_), cr(C_, A_), cr(A_, B_); det = sum(A_[t]*bc[t] for t in range(3))
    if abs(det) < 1e-20: continue
    v = [(Pm[a][1]*bc[t] + Pm[b][1]*ca[t] + Pm[c][1]*ab[t])/det for t in range(3)]
    s = [sum(Pm[j][0][t]*v[t] for t in range(3)) - Pm[j][1] for j in range(len(P))]
    if max(s) < 1e-30:
        inc = frozenset(j for j in range(len(P)) if abs(s[j]) < 1e-30)
        cand.setdefault(inc, (a, b, c, v))
pr(f"candidate vertices {len(cand)} (record corners {e['c']})")
V = []
for inc, (a, b, c, vm) in cand.items():
    ua, ub, uc = [[kq(z) for z in P[t][0]] for t in (a, b, c)]
    bc, ca, ab = cr(ub, uc), cr(uc, ua), cr(ua, ub); det = ua[0]*bc[0] + ua[1]*bc[1] + ua[2]*bc[2]
    v = [(P[a][1]*bc[t] + P[b][1]*ca[t] + P[c][1]*ab[t])/det for t in range(3)]
    for j in range(len(P)):
        u = [kq(z) for z in P[j][0]]; val = u[0]*v[0] + u[1]*v[1] + u[2]*v[2] - P[j][1]
        if j in inc: assert val == ZERO, "vertex on its planes (exact)"
        else: assert ev(val) < 0, "strictly inside (arb)"
    V.append((v, inc, vm))
assert len(V) == e["c"]
pr(f"vertices {len(V)}: each exactly on its planes and strictly inside the others")
# cos(2 pi/15): minimal polynomial from the cyclotomic polynomial
GAM = pari("polresultant(polcyclo(15,z), 2*gg*z - z^2 - 1, z)")   # in the ordinary variable gg
gam_r = (arb.pi() * 2 / 15).cos()

def certify(j, name):
    n_ = [kq(z) for z in P[j][0]]
    F = [(v, vm) for v, inc, vm in V if j in inc]
    nm_ = [fl(z) for z in P[j][0]]
    cen = [sum(f[1][t] for f in F)/len(F) for t in range(3)]; u0 = [F[0][1][t] - cen[t] for t in range(3)]; w0 = cr(nm_, u0)
    F.sort(key=lambda f: mp.atan2(sum((f[1][t]-cen[t])*w0[t] for t in range(3)), sum((f[1][t]-cen[t])*u0[t] for t in range(3))))
    v = [f[0] for f in F]; n = len(v)
    def dot(p, q): return p[0]*q[0] + p[1]*q[1] + p[2]*q[2]
    m = [cr(v[k], v[(k+1) % n]) for k in range(n)]
    alpha = [-dot(m[k-1], m[k]) for k in range(n)]
    G = [dot(m[k-1], m[k-1])*dot(m[k], m[k]) - alpha[k]*alpha[k] for k in range(n)]
    Mk = ZERO + 1
    for k in range(n): Mk = Mk*dot(m[k], m[k])
    sym = []
    gi = []
    for k in range(n):
        hit = [t for t, g_ in enumerate(sym) if g_ == G[k]]
        if hit: gi.append(hit[0])
        else: sym.append(G[k]); gi.append(len(sym) - 1)
    # product of (alpha_k + i s_gi[k]) as {frozenset S: (re, im)}, s^2 reduced to G
    prod = {frozenset(): (ZERO + 1, ZERO)}
    for k in range(n):
        g_ = gi[k]; new = {}
        for S, (re, im) in prod.items():
            def add(T, a, b):
                r0, i0 = new.get(T, (ZERO, ZERO)); new[T] = (r0 + a, i0 + b)
            add(S, alpha[k]*re, alpha[k]*im)
            if g_ in S: add(S - {g_}, -sym[g_]*im, sym[g_]*re)
            else: add(S | {g_}, -im, re)
        prod = new
    sgn = 1 if n % 2 == 0 else -1
    # rigorous value
    sr = [ev(g_).sqrt() for g_ in sym]
    reval = arb(0)
    for S, (re, im) in prod.items():
        t = ev(re)
        for q in S: t *= sr[q]
        reval += t
    cosO = sgn*reval/ev(Mk); beta = cosO - gam_r
    Om = cosO.acos()
    # annihilating polynomial: F = sgn*Re - M*(B + g)
    expr = pari(0)
    for S, (re, im) in prod.items():
        t = re
        for q in S: t = t * VH[f"s{q}"]
        expr = expr + t
    F = sgn*expr - Mk*(VH["B"] + VH["g"])
    for q in range(len(sym)):
        F = pari.polresultant(F, VH[f"s{q}"]**2 - sym[q], VH[f"s{q}"])
    gpol = pari.subst(GAM, pari("gg"), VH["g"])
    F = pari.polresultant(F, gpol, VH["g"])
    F = pari.lift(pari.lift(F))
    F = pari.polresultant(F, pari(QX), "x")
    F = pari.polresultant(F, pari("w^2-5"), "w")
    Pb = pari.subst(F, VH["B"], "y")
    deg = int(pari.poldegree(Pb, "y")); co = [pari.polcoef(Pb, i, "y") for i in range(deg + 1)]
    kz = 0
    while co[kz] == 0: kz += 1
    q0 = abs(co[kz]); qmax = max(abs(c) for c in co[kz+1:]) if deg > kz else 0
    bound = arb(fmpq(int(pari.numerator(q0)), int(pari.denominator(q0)))) / (arb(fmpq(int(pari.numerator(q0)), int(pari.denominator(q0)))) + arb(fmpq(int(pari.numerator(qmax)), int(pari.denominator(qmax)))))
    ok = kz >= 1 and bool(abs(beta) < bound) and bool(Om > 0) and bool(Om < arb.pi())
    pr(f"{name}: {n}-gon, {len(sym)} distinct G; P(B) degree {deg}, B^{kz} divides it; |beta| < {abs(beta).upper().str(5)}; "
       f"nonzero-root bound {bound.lower().str(5)}; Omega = {Om.str(15)}; 4pi/30 = {(4*arb.pi()/30).str(15)}  -> Omega = 4pi/30 exactly: {ok}")
    return ok
okC = certify([t for t in range(len(P)) if P[t][2] == 0][0], "C6 face"); pr("PROGRESS 0.5 C6 face done")
okR = certify([t for t in range(len(P)) if P[t][2] == 2][0], "RT24/12a face")
pr("FINAL ok: CIRT-30's C6 and RT24/12a depths are exactly equal (fair die = this algebraic die)" if okC and okR else "FINAL FAIL")
