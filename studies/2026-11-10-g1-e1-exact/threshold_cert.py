"""Certified threshold theorem (DICTO 10 Nov 2026: 'prove the threshold curve'). Region R = [U0, U1] x [V0, V1] of the two-slope
family with (b) and (c) (u = slope of t7, v = slope of t3). Claim: on R the odd regions are 43 (all triangles) on one side of the
curve C = 0 and 45 (41 triangles, 4 four-sided) on the other, where C = det(t4 right leg, t5 base, t6 right leg); the curve meets
each line u = const of R at most once. Proof by certified computation, box by box (side 'h'):
 (1) S from condition (c) (quadratic G, larger root), t from the closing relation H1 (natural coordinates, (b) by construction)
     by interval Newton: one solution in the box, for every (u, v) of the box;
 (2) every coordinate, every line, every triple determinant enclosed by the centred form f(c) + grad f(box) . [-r, r]
     (forward differentiation in u and v through the whole construction, implicit for t);
 (3) admissibility: bases strictly ordered, half-widths > 0, apex on the correct side (strict);
 (4) every triple of the 27 lines other than the 115 identities (84 triples of parallel bases; the 31 Huet conditions,
     identities by Theorem 1) either has a determinant of fixed sign on the box, or does not meet on all three drawn segments;
     the 6 threshold triples (t4's leg with two of t5's base, t5's leg, t6's leg; and mirrors) are excused only where
     dC/dv has a fixed sign on the box (monotone: one crossing per column);
 (5) the region counts at one point on each side are certified elsewhere (the DICTO Yantra: 43; Kulaichev's yantra: 45).
The arrangement of the 27 drawn segments changes only at such events, so (1)-(5) give the claim.
usage: python -u threshold_cert.py U0 U1 V0 V1 h   (prints a heartbeat, FINAL ok / FINAL FAIL)"""
import sys, io, contextlib, itertools, time, json, os
sys.path.insert(0, '.')
import mpmath as mp
from mpmath import iv
mp.mp.dps = 34; iv.dps = 34
T0 = time.time(); say = lambda *a: print(f'[{time.time()-T0:7.1f} s]', *a, flush=True)
with contextlib.redirect_stdout(io.StringIO()):
    import natural as N
import sympy as sp
from model import solve, det3
u_, v_, t_, S_ = N.u, N.v, N.t, N.S
Hm = [f for f, m in sp.factor_list(N.H)[1] if sp.degree(f, t_) == 10][0]
def pdict(e): return [(tuple(m), (int(c.p), int(c.q))) for m, c in sp.Poly(sp.expand(e), u_, v_, t_, S_).terms()]
H = pdict(Hm); Ht = pdict(sp.diff(Hm, t_)); Htt = pdict(sp.diff(Hm, t_, 2)); Hu = pdict(sp.diff(Hm, u_)); Hv = pdict(sp.diff(Hm, v_)); HS = pdict(sp.diff(Hm, S_))
Gp = sp.Poly(sp.expand(N.G), S_); GA, GB, GC = [pdict(Gp.coeff_monomial(S_**k)) for k in (2, 1, 0)]
Qn_, Qd_ = sp.fraction(sp.factor(N.Q)); QN, QD = pdict(Qn_), pdict(Qd_)
say('polynomials ready: H1 terms', len(H))
class D:
    __slots__ = ('x', 'a', 'b')
    def __init__(s, x, a=0, b=0): s.x = x; s.a = a; s.b = b
    @staticmethod
    def c(o): return o if isinstance(o, D) else D(iv.mpf(o) if not isinstance(o, type(iv.mpf(0))) else o)
    def __add__(s, o): o = D.c(o); return D(s.x + o.x, s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = D.c(o); return D(s.x - o.x, s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return D.c(o) - s
    def __mul__(s, o): o = D.c(o); return D(s.x * o.x, s.a * o.x + s.x * o.a, s.b * o.x + s.x * o.b)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = D.c(o); q = s.x / o.x; return D(q, (s.a - q * o.a) / o.x, (s.b - q * o.b) / o.x)
    def __rtruediv__(s, o): return D.c(o) / s
    def __neg__(s): return D(-s.x, -s.a, -s.b)
    def __pow__(s, k):
        r = D(iv.mpf(1))
        for _ in range(k): r = r * s
        return r
def sqrtD(z): r = iv.sqrt(z.x); return D(r, z.a / (2 * r), z.b / (2 * r))
def peval(P, X):          # X: D values for (u, v, t, S)
    tot = D(iv.mpf(0)); pw = {}
    for mon, (p, q) in P:
        term = D(iv.mpf(p) / q)
        for j, e in enumerate(mon):
            if e:
                key = (j, e)
                if key not in pw: pw[key] = X[j] ** e
                term = term * pw[key]
        tot = tot + term
    return tot
def pevalI(P, X):         # plain intervals
    tot = iv.mpf(0)
    for mon, (p, q) in P:
        term = iv.mpf(p) / q
        for j, e in enumerate(mon):
            if e: term = term * X[j] ** e
        tot = tot + term
    return tot
def build(U, V, tguess):
    """U, V: iv intervals (thin at a centre). Returns (tri of D values, t interval) or raises."""
    u, v = D(U, iv.mpf(1), iv.mpf(0)), D(V, iv.mpf(0), iv.mpf(1))
    zero = D(iv.mpf(0))
    A, B, C = (peval(P, [u, v, zero, zero]) for P in (GA, GB, GC))
    S = (-B + sqrtD(B * B - 4 * A * C)) / (2 * A)
    # point Newton at the centre, then epsilon-inflated interval Newton over the box (unique t for every (u, v) of the box)
    um_, vm_ = mp.mpf(U.mid), mp.mpf(V.mid)
    Sm = iv.mpf(S.x.mid) if S.x.delta == 0 else None
    zc = D(iv.mpf(0)); uc_, vc_ = D(iv.mpf(um_)), D(iv.mpf(vm_))
    Ac, Bc, Cc = (peval(P, [uc_, vc_, zc, zc]).x for P in (GA, GB, GC))
    Sc = (-Bc + iv.sqrt(Bc * Bc - 4 * Ac * Cc)) / (2 * Ac)
    ru0, rv0 = mp.mpf(U.delta) / 2, mp.mpf(V.delta) / 2
    S = D(Sc + S.a * iv.mpf([-ru0, ru0]) + S.b * iv.mpf([-rv0, rv0]), S.a, S.b)   # centred form for S over the box
    m = mp.mpf(tguess)
    for _ in range(80):
        hv = pevalI(H, [iv.mpf(um_), iv.mpf(vm_), iv.mpf(m), Sc]); hd = pevalI(Ht, [iv.mpf(um_), iv.mpf(vm_), iv.mpf(m), Sc])
        dm = mp.mpf(hv.mid) / mp.mpf(hd.mid); m -= dm
        if abs(dm) < mp.mpf(10)**-30: break
    ru_, rv_ = mp.mpf(U.delta) / 2, mp.mpf(V.delta) / 2
    Ru, Rv = iv.mpf([-ru_, ru_]), iv.mpf([-rv_, rv_]); M = iv.mpf(m)
    hc = pevalI(H, [iv.mpf(um_), iv.mpf(vm_), M, Sc]); hd = peval(H, [u, v, D(M), S])
    Hbox = hc + hd.a * Ru + hd.b * Rv                         # H(m; box), centred form
    htc = pevalI(Ht, [iv.mpf(um_), iv.mpf(vm_), M, Sc]); htd = peval(Ht, [u, v, D(M), S])
    for r in [mp.mpf(10)**-k for k in (28, 24, 20, 16, 12, 10, 9, 8, 7, 6, 5, 4)]:
        T = iv.mpf([m - r, m + r])
        Htb = htc + htd.a * Ru + htd.b * Rv + pevalI(Htt, [U, V, T, S.x]) * (T - M)
        if Htb.a <= 0 <= Htb.b: continue
        Nn = M - Hbox / Htb
        if Nn.a > T.a and Nn.b < T.b: T = Nn; break
    else:
        if os.environ.get('DEBUGN') == '1':
            print('DEBUG m', mp.nstr(m, 12), 'Sc', Sc, '\n hc', hc, '\n hd.a', hd.a, '\n hd.b', hd.b, '\n Hbox', Hbox, '\n htc', htc, '\n Htb(last)', Htb, '\n S.x', S.x, 'S.a', S.a, flush=True)
            raise SystemExit('debug stop')
        raise ValueError('interval Newton failed')
    X = [U, V, T, S.x]; ht = pevalI(Ht, X)
    t = D(T, -(pevalI(Hu, X) + pevalI(HS, X) * S.a) / ht, -(pevalI(Hv, X) + pevalI(HS, X) * S.b) / ht)
    Q = peval(QN, [u, v, t, S]) / peval(QD, [u, v, t, S])
    one = D(iv.mpf(1))
    P_ = v * v / (one + v * v); R_ = one / (one + u * u)
    tri = solve(P_, Q, R_, S, v / (one + v * v), u / (one + u * u), None, b1=t * t / (one + t * t))
    for k in ('b', 'w', 'a'):
        for i in tri[k]: tri[k][i] = D.c(tri[k][i])
    return tri, mp.mpf(T.mid)
NAMES = [f'{k}{i}' for i in range(1, 10) for k in 'BRL']
def lines(tri):
    b, w, a = tri['b'], tri['w'], tri['a']; z = D(iv.mpf(0)); L = {}
    for i in range(1, 10):
        L[f'B{i}'] = ((-w[i], b[i]), (w[i], b[i])); L[f'R{i}'] = ((w[i], b[i]), (z, a[i])); L[f'L{i}'] = ((-w[i], b[i]), (z, a[i]))
    return L
TRIPLES = list(itertools.combinations(NAMES, 3))
IDENT = set(); THRESH = {('B5', 'R4', 'R5'), ('B5', 'R4', 'R6'), ('R4', 'R5', 'R6'), ('B5', 'L4', 'L5'), ('B5', 'L4', 'L6'), ('L4', 'L5', 'L6')}
def enclose(fc, fb, ru, rv):   # centred form
    return fc.x + fb.a * iv.mpf([-ru, ru]) + fb.b * iv.mpf([-rv, rv])
def meet_params(L, tr):
    (p1, p2), (q1, q2), (r1, r2) = L[tr[0]], L[tr[1]], L[tr[2]]
    den = (p2[0]-p1[0])*(q2[1]-q1[1]) - (p2[1]-p1[1])*(q2[0]-q1[0])
    lam = ((q1[0]-p1[0])*(q2[1]-q1[1]) - (q1[1]-p1[1])*(q2[0]-q1[0])) / den
    mu = ((q1[0]-p1[0])*(p2[1]-p1[1]) - (q1[1]-p1[1])*(p2[0]-p1[0])) / den
    X0 = p1[0] + lam*(p2[0]-p1[0]); X1 = p1[1] + lam*(p2[1]-p1[1])
    vx, vy = r2[0]-r1[0], r2[1]-r1[1]
    nu = ((X0-r1[0])*vx + (X1-r1[1])*vy) / (vx*vx + vy*vy)
    return lam, mu, nu
U0, U1, V0, V1, h = (mp.mpf(x) for x in sys.argv[1:6]); import os; VERB = os.environ.get('VERBOSE') == '1'
# identities from the centre of the region (exactly zero by Theorem 1 / horizontal bases); checked again in every box
tc0 = mp.mpf('0.1')
uc, vc = (U0+U1)/2, (V0+V1)/2
import rhombus
Qg, Sg = mp.findroot(lambda Q, S: rhombus.extra(rhombus.yantra(uc, vc, Q, S))[:2], (mp.mpf('0.55'), mp.mpf('0.92')))
b1g = rhombus.yantra(uc, vc, Qg, Sg)['b'][1]; tc0 = mp.sqrt(b1g / (1 - b1g))
tri0, _ = build(iv.mpf(uc), iv.mpf(vc), tc0); L0 = lines(tri0)
for tr in TRIPLES:
    d = det3(*(L0[n] for n in tr)).x
    if abs(mp.mpf(d.mid)) < mp.mpf(10)**-25: IDENT.add(tr)
say('identities at the centre:', len(IDENT), '(expected 115 = 84 base triples + 31 Huet)')
if len(IDENT) != 115: raise SystemExit('FINAL FAIL: identity count')
bad = []; boxes = 0; thr_boxes = 0; dCsign = set(); queue = []
nu_ = int((U1 - U0) / h + mp.mpf('0.5')); nv_ = int((V1 - V0) / h + mp.mpf('0.5'))
for i in range(nu_):
    for j in range(nv_):
        queue.append((U0 + i*h, U0 + (i+1)*h, V0 + j*h, V0 + (j+1)*h, 0))
tguess = {}; last = time.time()
while queue:
    a0, a1, c0, c1, depth = queue.pop()
    ru, rv = (a1 - a0) / 2, (c1 - c0) / 2; um, vm = (a0 + a1) / 2, (c0 + c1) / 2
    try:
        g = tguess.get(round(float(um), 2), tc0)
        triC, tm = build(iv.mpf(um), iv.mpf(vm), g); tguess[round(float(um), 2)] = tm
        triB, _ = build(iv.mpf([a0, a1]), iv.mpf([c0, c1]), tm)
    except (ValueError, ZeroDivisionError) as e:
        if depth < 4:
            queue += [(a0, um, c0, vm, depth+1), (um, a1, c0, vm, depth+1), (a0, um, vm, c1, depth+1), (um, a1, vm, c1, depth+1)]; continue
        bad.append((float(a0), float(c0), 'build: ' + str(e))); continue
    LC, LB = lines(triC), lines(triB); ok = True; why = ''
    # admissibility
    bE = {i: enclose(triC['b'][i], triB['b'][i], ru, rv) for i in range(1, 10)}
    wE = {i: enclose(triC['w'][i], triB['w'][i], ru, rv) for i in range(1, 10)}
    aE = {i: enclose(triC['a'][i], triB['a'][i], ru, rv) for i in range(1, 10)}
    for i in range(1, 9):
        if not (bE[i+1] - bE[i]).a > 0: ok, why = False, f'order b{i}'
    for i in range(1, 10):
        if not wE[i].a > 0: ok, why = False, f'w{i}'
        side = (aE[i] - bE[i]) if i <= 5 else (bE[i] - aE[i])
        if i not in (3, 7) and not side.a > 0: ok, why = False, f'apex side t{i}'
    thr_here = False
    if ok:
        for tr in TRIPLES:
            if tr in IDENT: continue
            dE = enclose(det3(*(LC[n] for n in tr)), det3(*(LB[n] for n in tr)), ru, rv)
            if dE.a > 0 or dE.b < 0: continue
            if tr in THRESH: thr_here = True; continue
            try:
                pc, pb = meet_params(LC, tr), meet_params(LB, tr)
                off = False
                for k in range(3):
                    e = enclose(pc[k], pb[k], ru, rv)
                    if e.b < 0 or e.a > 1: off = True; break
            except ZeroDivisionError:
                off = False
            if not off: ok, why = False, 'triple ' + '-'.join(tr); break
    if ok and thr_here:
        Cb = det3(LB['R4'], LB['B5'], LB['R6'])
        if Cb.b.a > 0: dCsign.add(1)
        elif Cb.b.b < 0: dCsign.add(-1)
        else: ok, why = False, 'dC/dv contains 0'
        thr_boxes += 1
    if not ok and VERB: say(f'  box depth {depth} not certified: {why}')
    if not ok:
        if depth < 4:
            queue += [(a0, um, c0, vm, depth+1), (um, a1, c0, vm, depth+1), (a0, um, vm, c1, depth+1), (um, a1, vm, c1, depth+1)]; continue
        bad.append((float(a0), float(c0), why))
    boxes += 1
    if VERB: say(f'box u [{float(a0):.4f},{float(a1):.4f}] v [{float(c0):.4f},{float(c1):.4f}] depth {depth}: ' + ('ok' if ok else 'FAIL ' + why) + (' threshold' if thr_here else ''))
    if time.time() - last > 30: say(f'heartbeat: boxes certified {boxes}, threshold boxes {thr_boxes}, queue {len(queue)}, failures {len(bad)}'); last = time.time()
say(f'boxes certified {boxes}; boxes crossed by the threshold {thr_boxes}; dC/dv sign there {sorted(dCsign)}; failures {len(bad)}')
json.dump({'region': [str(x) for x in (U0, U1, V0, V1)], 'h': str(h), 'boxes': boxes, 'threshold_boxes': thr_boxes, 'dCdv_sign': sorted(dCsign), 'failures': bad[:50]},
          open(f'threshold-cert-{sys.argv[1]}-{sys.argv[2]}-{sys.argv[3]}-{sys.argv[4]}.json', 'w'))
print('FINAL ok' if not bad and len(dCsign) <= 1 else f'FINAL FAIL: {len(bad)} boxes not certified, dC/dv signs {sorted(dCsign)}; first {bad[:3]}')
