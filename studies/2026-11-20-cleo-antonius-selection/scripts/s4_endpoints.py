"""Step 4 (exact elimination + certified balls): the two ends of the traditional-form window, exactly.
Both ends are the same event (s2_events.py): t4's right leg passes through t5's corner, where t5's base and t6's right leg meet
(the corner touch (5,5,6)); C = det3(t4 right leg, t5 base, t6 right leg) = 0.  By #103 Theorem 5 the counts depend only on c = uv,
so the event is solved on the rhombus member u = v = sqrt(c).
 (1) Exact (Sage/Singular over Q, PARI): with v = u, R1 = Res_S(G, H1), R2 = Res_S(G, C); A, B = the irreducible factors of R1, R2
     that vanish at the event (every other factor certified nonzero there by ball arithmetic, so dropping it loses nothing);
     E = Res_t(A, B), factored over Q.
 (2) Certified (python-flint/Arb): for each event, the Krawczyk test proves that G = H1 = C = 0 (v = u) has exactly one solution in
     a box of radius 2^-300 around the 60-digit point; every factor of E except one is nonzero on the box's u (ball evaluation);
     that factor must be #103's f180 (Proposition 13, inputs/threshold-minpoly-u.txt) and must have exactly one real root in the
     box's u-interval (PARI polsturm on a rational interval containing it).
 (3) c = u^2: g90(c) = f180(sqrt c) (f180 is even); irreducibility of f180 and g90 (PARI), and rational isolating intervals of the
     two window ends as roots of g90 (polsturm = 1 on each).
 Also: is 2/phi^3 = 2 sqrt5 - 4 a root of g90 (no: it is not even of degree 90), and the real roots of g90 in (0, 1).
FINAL ok iff (1)-(3) all pass for both events."""
import sys, os, json, time
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); D = lambda *p: os.path.join(ROOT, *p)
sys.path.insert(0, HERE)
import mpmath as mp
mp.mp.dps = 160
import yfam as Y
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
import cypari2
pari = cypari2.Pari(); pari.allocatemem(int(4e9))
import flint
from flint import arb, fmpq, arb_mat
flint.ctx.prec = 1200

R3 = PolynomialRing(QQ, 'u,t,S'); U, T, S = R3.gens()
def load(name):
    f = R3(0)
    for e, c in Y.POL[name]: f += ZZ(c) * U ** (e[0] + e[1]) * T ** e[2] * S ** e[3]
    return f
G, H1, C = load('G'), load('H1'), load('C')
say('v = u: G, H1, C degrees (u, t, S):', [[f.degree(g) for g in (U, T, S)] for f in (G, H1, C)], 'terms', [len(f.monomials()) for f in (G, H1, C)])

# ---- event points (60 digits) from s2's events, t and S from the member
ev = [e for e in json.load(open(D('data', 'events.json')))['events'] if e['below']['odd'] != e['above']['odd']]
pts = []
for e in ev:
    u = mp.mpf(e['u']); y = Y.members(u, u); assert len(y) == 1
    y = y[0]
    with mp.workdps(160):                                # polish (u, t, S) on G = H1 = C = 0 (v = u) to 140 digits
        F = lambda uu, tt, SS: [Y.peval(n, uu, uu, tt, SS)[0] for n in ('G', 'H1', 'C')]
        u, tt, SS = mp.findroot(F, (u, y['t'], y['S']), tol=mp.mpf(10) ** -280)
    y = dict(t=tt, S=SS)
    pts.append((u, y['t'], y['S'], e))
    say(f"event c = {e['c'][:22]}: u = {mp.nstr(u, 25)}, t = {mp.nstr(y['t'], 25)}, S = {mp.nstr(y['S'], 25)}; {e['below']['odd']} -> {e['above']['odd']}")
assert len(pts) == 2

def ball(x, rad): return arb(fmpq(int(mp.floor(x * mp.mpf(2) ** 460)), 2 ** 460), rad)
def ev_sage(f, X):                                       # f in Q[u,t,S] at balls X
    tot = arb(0)
    for e, c in f.dict().items():
        tot += arb(fmpq(int(c.numerator()), int(c.denominator()))) * X[0] ** e[0] * X[1] ** e[1] * X[2] ** e[2]
    return tot
def nonzero(f, X): return not ev_sage(f, X).contains(0)

# ---- (2a) Krawczyk boxes
J = [[f.derivative(g) for g in (U, T, S)] for f in (G, H1, C)]
def krawczyk(p, rad):
    X = [ball(x, rad) for x in p[:3]]; y = [arb(x.mid()) for x in X]
    Fy = arb_mat([[ev_sage(f, y)] for f in (G, H1, C)])
    Jy = arb_mat([[ev_sage(J[i][j], y) for j in range(3)] for i in range(3)]).mid(); Yi = Jy.inv().mid()
    JX = arb_mat([[ev_sage(J[i][j], X) for j in range(3)] for i in range(3)])
    M = arb_mat([[1 if i == j else 0 for j in range(3)] for i in range(3)]) - Yi * JX
    K = arb_mat([[y[i]] for i in range(3)]) - Yi * Fy + M * arb_mat([[X[i] - y[i]] for i in range(3)])
    return all(X[i].contains_interior(K[i, 0]) for i in range(3)), X, [K[i, 0] for i in range(3)]
boxes = []
for p in pts:
    ok, X, K = krawczyk(p, arb(2) ** -300)
    say('Krawczyk (exactly one solution of G = H1 = C = 0 in the box of radius 2^-300):', ok, '; u enclosed to radius', K[0].rad())
    boxes.append((ok, X, K))

# ---- (1) exact elimination, keeping only factors that may vanish at an event (the others are certified nonzero on its box)
R1 = G.resultant(H1, S); say('R1 = Res_S(G, H1) degrees (u, t)', R1.degree(U), R1.degree(T))
R2 = G.resultant(C, S); say('R2 = Res_S(G, C) degrees (u, t)', R2.degree(U), R2.degree(T))
def keep(R, name):
    out = []
    for f, m in R.factor():
        if f.degree() == 0: continue
        z = [not nonzero(f, b[2] if b[0] else b[1]) for b in boxes]
        say(f'   {name} factor degrees (u, t) = ({f.degree(U)}, {f.degree(T)})^{m}: may vanish at the events: {z}')
        if any(z): out.append((f, z))
    return out
A = keep(R1, 'R1'); B = keep(R2, 'R2')
f180 = pari(open(D('inputs', 'threshold-minpoly-u.txt')).read().strip())
ok_ev = []
for k, (okk, X, K) in enumerate(boxes):
    a = [f for f, z in A if z[k]]; b = [f for f, z in B if z[k]]
    say(f'event {k}: kept factors of R1 {[(f.degree(U), f.degree(T)) for f in a]}, of R2 {[(f.degree(U), f.degree(T)) for f in b]}')
    Ub = K[0]; found = []; others_nonzero = True
    for fa in a:
        for fb in b:
            if fa.degree(T) == 0 or fb.degree(T) == 0:
                Es = [fa if fa.degree(T) == 0 else fb]
            else:
                t1 = time.time(); Es = [pari(str(fa)).polresultant(pari(str(fb)), 't')]; say(f'   Res_t: degree {pari.poldegree(Es[0], "u")} ({time.time() - t1:.1f} s)')
            for E in Es:
                Fq = pari.factor(pari(str(E)))
                for i in range(len(Fq[0])):
                    q = Fq[0][i]
                    if pari.poldegree(q, 'u') == 0: continue
                    coeffs = [int(x) for x in pari.Vecrev(q)]
                    val = sum(arb(c) * Ub ** j for j, c in enumerate(coeffs))
                    if val.contains(0):
                        found.append(q); say(f'   factor of degree {pari.poldegree(q, "u")} may vanish on the u-ball')
    is180 = len(found) >= 1 and all(pari.poldegree(q, 'u') == 180 and q * pari.pollead(f180) == f180 * pari.pollead(q) for q in found)
    # exactly one real root of f180 in a rational interval holding the u-ball
    lo = fmpq(int(mp.floor(mp.mpf(Ub.mid().str(60, radius=False)) * 10 ** 40)) - 1, 10 ** 40); hi = lo + fmpq(3, 10 ** 40)
    ns = int(pari.polsturm(f180, [pari(f'{lo.p}/{lo.q}'), pari(f'{hi.p}/{hi.q}')]))
    inside = (Ub.lower() > arb(lo)) and (Ub.upper() < arb(hi))
    say(f'event {k}: the only factor of E that can vanish there is f180: {is180}; f180 has {ns} root(s) in [{lo}, {hi}] (holds the u-ball: {bool(inside)})')
    ok_ev.append(okk and is180 and ns == 1 and bool(inside))

# ---- (3) c = u^2
ff = pari.Vecrev(f180); assert all(ff[j] == 0 for j in range(1, 181, 2)), 'f180 not even'
g90 = pari.Pol(pari.Vec([ff[j] for j in range(180, -1, -2)]), 'c')
irr = bool(pari.polisirreducible(f180)) and bool(pari.polisirreducible(g90))
rr = pari.polrootsreal(g90); roots01 = [mp.mpf(str(r)) for r in rr if 0 < float(r) < 1]
say('f180 and g90 irreducible over Q:', irr, '; g90 degree', pari.poldegree(g90), ', real roots', len(rr), ', in (0, 1):', [mp.nstr(r, 12) for r in roots01])
cint = []
for k, (u, t, Sv, e) in enumerate(pts):
    cc = u * u; lo = mp.floor(cc * 10 ** 40) - 1; hi = lo + 3
    n = int(pari.polsturm(g90, [pari(f'{int(lo)}/10^40'), pari(f'{int(hi)}/10^40')]))
    cint.append((f'{int(lo)}/10^40', f'{int(hi)}/10^40', n)); say(f'window end {k}: c = {mp.nstr(cc, 45)}; g90 roots in [{int(lo)}, {int(hi)}]*10^-40: {n}')
two_phi3 = 2 * mp.sqrt(5) - 4
say('g90 at 2/phi^3 (nonzero expected):', mp.nstr(mp.polyval([mp.mpf(str(x)) for x in pari.Vec(g90)], two_phi3), 5))
json.dump(dict(g90=str(g90), window=[mp.nstr(p[0] ** 2, 60) for p in pts], u=[mp.nstr(p[0], 60) for p in pts], c_intervals=cint,
               g90_roots_01=[mp.nstr(r, 40) for r in roots01]), open(D('data', 'window-exact.json'), 'w'), indent=1)
open(D('data', 'g90-c.txt'), 'w').write(str(g90) + '\n')
ok = all(ok_ev) and irr and all(n == 1 for _, _, n in cint)
print('FINAL ok' if ok else f'FINAL FAIL: events {ok_ev}, irreducible {irr}, isolation {[n for _, _, n in cint]}')
