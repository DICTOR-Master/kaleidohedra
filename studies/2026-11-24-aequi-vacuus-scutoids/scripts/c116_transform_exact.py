"""EXACT certificate for DICTO's Hollow-straw transformation C116 -> Minana #377 (27 Nov 2026; DICTO: "make the transformation exact").
With Claude (Anthropic). Construction as c116_transform.py: planes a . x = 1; a_k(lam) = a_k + lam (m_sigma(k) - a_k), lam in [0, 1];
P(lam) = {x : a_k(lam) . x <= 1 for all 60 k}. Numbers: exact Q(sqrt5) (Fractions). Inputs made exact:
  Minana #377: its planes exactly as the study's exact work uses them (directions in Q(sqrt5); depths = rational stand-ins of the fair
  depths, |error| < 1e-15; aequus_solid.py MODE stand); the layer scale s as a rational (denominator <= 1e9);
  C116: its own shape in the floating-resin placement, each plane vector rounded to rationals (denominator <= 1e9).
Certificate, all exact:
  (A) at lam = 0 the polytope has C116's face pattern, at lam = 1 Minana #377's (under the pairing): every corner on exactly three
      planes and strictly inside all others, the corners close into a sphere (each face one cycle, V - E + F = 2);
  (B) a corner (planes k, a, b) at lam is x(lam) = N(lam)/det(lam), N quadratic, det cubic; it stays a corner while every other plane c
      keeps f_c = a_c(lam) . N - det on the strict side. The pattern can change only at a root of some f_c (four planes through one
      point). All roots in (0, 1] are isolated exactly (norm to Q[lam], Sturm/isolating intervals, sign change of f itself). Between
      events the pattern is constant (proved by the root isolation); each event is crossed at a rational lam and the new state is
      verified exactly as in (A);
  (C) NESTING: on each corner's whole lifetime, every plane p through it moves outward there: (m_p - a_p) . x(lam) < 0 (quadratic over
      det, no root on the lifetime, sign checked) -> P(lam) grows, so the straws (regions swept by each face) do not overlap and fill
      the shell exactly; det has no root on any lifetime (corners never degenerate);
  (D) the events are exactly the 18 swaps of the floating-resin floor, one swap each (lost pair and gained pair on four faces).
FINAL ok iff (A)-(D) hold."""
import os, sys, json, itertools, time
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
from scipy.spatial import HalfspaceIntersection
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
from resin import Q
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
t0 = time.time()
def pr(*a): print(*a, flush=True)
R = json.load(open(os.path.join(ROOT, 'data/cells/stand/amber_c116-layer0float_layer_6-5_cen.json')))
sig = {int(k): int(v) for k, v in json.load(open(os.path.join(ROOT, 'data/c116/onefloor_float.json')))['pairing'].items()}
inv = {v: k for k, v in sig.items()}
C116f = json.load(open(os.path.join(ROOT, 'data/c116/pairing.json')))['faces']
FL = json.load(open(os.path.join(ROOT, 'data/c116/onefloor_float.json')))['swaps']
floor = {(tuple(sorted(g)), tuple(sorted(l))) for g, l in FL if l}
S = A.build("aequus-377"); sR = Fr(float(R['s'])).limit_denominator(10 ** 9)
M = [[x / (c * Q(sR)) for x in u] for u, c in S['planes']]                       # Minana planes, a . x = 1, exact Q(sqrt5)
CV = np.array(R['solid_V']); CF = R['solid_faces']; AK = []
for f in CF:
    X = CV[f]; c0 = X.mean(0); n = np.linalg.svd(X - c0)[2][2]; n = n if n @ c0 > 0 else -n
    AK.append([Q(Fr(float(x)).limit_denominator(10 ** 9)) for x in n / (n @ c0)])
Mk = [M[sig[k]] for k in range(60)]
Dk = [[Mk[k][i] - AK[k][i] for i in range(3)] for k in range(60)]
# ---- polynomials in lam with Q(sqrt5) coefficients: list of Q, low degree first
def padd(p, q): n = max(len(p), len(q)); return [(p[i] if i < len(p) else Q(0)) + (q[i] if i < len(q) else Q(0)) for i in range(n)]
def pneg(p): return [-c for c in p]
def pmul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): out[i + j] = out[i + j] + a * b
    return out
def peval(p, lam):
    v = Q(0)
    for c in reversed(p): v = v * Q(lam) + c
    return v
row = lambda k: [[AK[k][i], Dk[k][i]] for i in range(3)]          # a_k(lam) as 3 linear polys
def vcross(u, v): return [padd(pmul(u[1], v[2]), pneg(pmul(u[2], v[1]))), padd(pmul(u[2], v[0]), pneg(pmul(u[0], v[2]))), padd(pmul(u[0], v[1]), pneg(pmul(u[1], v[0])))]
def vdot(u, v): return padd(padd(pmul(u[0], v[0]), pmul(u[1], v[1])), pmul(u[2], v[2]))
lam = sp.Symbol('lam')
def norm_poly(p):    # A^2 - 5 B^2 for p = A + B sqrt5, as a sympy Poly over QQ
    Apol = sp.Poly([sp.Rational(c.a.numerator, c.a.denominator) for c in reversed(p)], lam, domain='QQ')
    Bpol = sp.Poly([sp.Rational(c.b.numerator, c.b.denominator) for c in reversed(p)], lam, domain='QQ')
    return Apol ** 2 - 5 * Bpol ** 2
def roots_in(p, lo, hi):
    """exact sign-change roots of p in the open interval (lo, hi): list of isolating rational intervals (a, b) with sign(p(a)) != sign(p(b))"""
    N = norm_poly(p)
    if N.is_zero: raise ValueError('identically zero polynomial')
    if N.count_roots(sp.Rational(lo.numerator, lo.denominator), sp.Rational(hi.numerator, hi.denominator)) == 0: return []
    out = []
    for (a, b), m in N.intervals(inf=sp.Rational(lo.numerator, lo.denominator), sup=sp.Rational(hi.numerator, hi.denominator)):
        a, b = Fr(int(sp.numer(a)), int(sp.denom(a))), Fr(int(sp.numer(b)), int(sp.denom(b)))
        if a == b:            # rational root of the norm: is it a root of p?
            if peval(p, a).sign() == 0 and lo < a < hi: out.append((a, a))
            continue
        sa, sb = peval(p, a).sign(), peval(p, b).sign()
        if sa != sb and lo < b and a < hi: out.append((max(a, lo), min(b, hi)))
    return out
def refine(p, a, b, w):
    while b - a > w:
        m = (a + b) / 2; sm = peval(p, m).sign()
        if sm == 0: return m, m
        if sm == peval(p, a).sign(): a = m
        else: b = m
    return a, b
# ---- exact state at rational lam: corners (sets of 3 planes) verified exactly
def planes_at(l): return [[AK[k][i] + Dk[k][i] * Q(l) for i in range(3)] for k in range(60)]
def state(l):
    Af = np.array([[float(AK[k][i]) + float(Dk[k][i]) * float(l) for i in range(3)] for k in range(60)])
    P = HalfspaceIntersection(np.hstack([Af, -np.ones((60, 1))]), np.zeros(3)).intersections
    labs = set()
    for p in P:
        t = np.argsort(np.abs(Af @ p - 1))[:3]; labs.add(frozenset(int(i) for i in t))
    PL = planes_at(l); ok = True
    from resin import det3
    for L in labs:
        k, a, b = sorted(L); dd = det3(PL[k], PL[a], PL[b])
        if dd.sign() == 0: ok = False; continue
        # x = (r_a x r_b + r_b x r_k + r_k x r_a) / det
        def cr(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        Nn = [x + y + z for x, y, z in zip(cr(PL[a], PL[b]), cr(PL[b], PL[k]), cr(PL[k], PL[a]))]
        for c in range(60):
            if c in L: continue
            if ((sum((PL[c][i] * Nn[i] for i in range(3)), Q(0)) - dd) * Q(dd.sign())).sign() >= 0: ok = False
    # closed sphere: faces as cycles, Euler
    E = {}
    for L1, L2 in itertools.combinations(labs, 2):
        if len(L1 & L2) == 2: E.setdefault(frozenset(L1 & L2), []).append((L1, L2))
    deg = {L: 0 for L in labs}
    for e, lst in E.items():
        for L1, L2 in lst: deg[L1] += 1; deg[L2] += 1
    ok &= all(len(lst) == 1 for lst in E.values()) and all(d == 3 for d in deg.values())
    faces_present = {k for L in labs for k in L}
    ok &= len(faces_present) == 60 and len(labs) - len(E) + 60 == 2
    pairs = {tuple(sorted(e)) for e in E}
    return labs, pairs, ok
def pairs_of(fl):
    at = {}
    for k, F in enumerate(fl):
        for v in F: at.setdefault(v, set()).add(k)
    return {(a, b) for S_ in at.values() for a in S_ for b in S_ if a < b}
want0 = pairs_of(C116f); want1 = {tuple(sorted((inv[a], inv[b]))) for a, b in pairs_of([vs for vs, kk in S['faces']])}
# ---- corner polynomials
cache = {}
def corner_polys(L):
    if L in cache: return cache[L]
    k, a, b = sorted(L); rk, ra, rb = row(k), row(a), row(b)
    Nv = [padd(padd(x, y), z) for x, y, z in zip(vcross(ra, rb), vcross(rb, rk), vcross(rk, ra))]
    det = vdot(rk, vcross(ra, rb)); cache[L] = (Nv, det); return Nv, det
lam0 = Fr(0); labs, pairs, ok0 = state(lam0)
pr('(A) lam = 0: corners', len(labs), 'exact and closed:', ok0, '; pattern = C116 under the pairing:', pairs == want0)
okA = ok0 and pairs == want0
born = {L: lam0 for L in labs}; events = []; okC = True; okdet = True; step = 0
while True:
    step += 1
    # earliest event after lam0: roots of f_c for every corner and plane, grouped by the 4-plane set
    cands = []
    for L in labs:
        Nv, det = corner_polys(L)
        if roots_in(det, lam0, Fr(1)): okdet = False
        for c in range(60):
            if c in L: continue
            f = padd(vdot(row(c), Nv), pneg(det))
            for a_, b_ in roots_in(f, lam0, Fr(1)): cands.append((a_, b_, frozenset(L | {c}), f))
    if not cands:
        lam1 = Fr(1); break
    # refine until the earliest group is separated from all others
    w = Fr(1, 10 ** 6)
    while True:
        cands = [(*refine(f, a_, b_, w), F4, f) for a_, b_, F4, f in cands]
        first = min(cands, key=lambda z: z[1]); grp = {z[2] for z in cands if z[0] <= first[1]}
        if len(grp) == 1: break
        w /= 1000
        if w < Fr(1, 10 ** 40): pr('  two different four-plane sets meet at the same lam (to 1e-40):', [sorted(g) for g in grp]); break
    F4 = first[2]; hi = max(z[1] for z in cands if z[2] == F4)
    nxt = min((z[0] for z in cands if z[2] != F4), default=Fr(1))
    lam1 = (hi + nxt) / 2 if nxt < 1 else (hi + 1) / 2
    labs1, pairs1, ok1 = state(lam1)
    lost, gained = sorted(pairs - pairs1), sorted(pairs1 - pairs)
    sw = len(lost) == 1 and len(gained) == 1 and (tuple(gained[0]), tuple(lost[0])) in floor and set(lost[0]) | set(gained[0]) == set(F4)
    events.append(dict(lam_lo=str(first[0]), lam_hi=str(hi), lam=float(hi), planes=sorted(F4), lost=lost, gained=gained, one_floor_swap=sw, state_ok=ok1))
    pr(f'  event {len(events)}: lam in [{float(first[0]):.12f}, {float(hi):.12f}] planes {sorted(F4)} lost {lost} gained {gained} '
       f'floor swap {sw}; state after exact and closed: {ok1}  ({time.time() - t0:.0f} s)')
    # (C) nesting on the lifetimes of the corners that die here
    for L in labs - labs1:
        Nv, det = corner_polys(L); sdet = peval(det, (born[L] + first[0]) / 2).sign()
        for p in L:
            g = vdot([[Dk[p][i]] for i in range(3)], Nv)
            if roots_in(g, born[L], hi) or (peval(g, (born[L] + first[0]) / 2) * Q(sdet)).sign() >= 0: okC = False; pr('  NOT growing: corner', sorted(L), 'plane', p)
    for L in labs1 - labs: born[L] = hi
    labs, pairs, lam0 = labs1, pairs1, lam1
    if step > 60: pr('too many events'); break
labsE, pairsE, okE = state(Fr(1))
for L in labsE:        # nesting on the lifetimes of the corners alive at the end
    Nv, det = corner_polys(L); sdet = peval(det, (born[L] + 1) / 2).sign()
    for p in L:
        g = vdot([[Dk[p][i]] for i in range(3)], Nv)
        if roots_in(g, born[L], Fr(1)) or (peval(g, (born[L] + 1) / 2) * Q(sdet)).sign() >= 0: okC = False; pr('  NOT growing: corner', sorted(L), 'plane', p)
okAend = okE and pairsE == want1
pr('(A) lam = 1: corners', len(labsE), 'exact and closed:', okE, '; pattern = Minana #377 under the pairing:', pairsE == want1)
pr('(B) events:', len(events), '; every state between events exact and closed:', all(e['state_ok'] for e in events), '; no corner degenerates (det):', okdet)
pr('(C) nested (every plane moves outward at every corner over its whole life):', okC)
okD = len(events) == 18 and all(e['one_floor_swap'] for e in events) and len({(tuple(e['gained'][0]), tuple(e['lost'][0])) for e in events}) == 18
pr('(D) exactly the 18 floor swaps, one per event:', okD)
json.dump(dict(scale=str(sR), events=events, A=[okA, okAend], C=okC, D=okD, det=okdet), open(os.path.join(ROOT, 'data/c116/transform_exact.json'), 'w'))
good = okA and okAend and okC and okD and okdet and all(e['state_ok'] for e in events)
pr('RESULT:', "DICTO's Hollow-straw transformation is EXACT (C116 own shape, rounded to 1e-9; Minana with its 15-digit depth stand-ins)" if good else 'NOT certified: see above')
pr('FINAL ok' if good else 'FINAL FAIL')
