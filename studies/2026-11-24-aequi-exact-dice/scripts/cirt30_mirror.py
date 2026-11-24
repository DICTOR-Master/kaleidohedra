# Aequus CIRT-30, T 26 (orbits C6 + I12 + RT24/12a): an exact proof, by a mirror, that
#   6 Om(C6 face) - 12 Om(RT24/12a face) = -4pi/5, i.e. 2 Om(RT24/12a) - Om(C6) = 4pi/30,
# on the whole half-line d(C6) = d(RT24/12a) = 1, d(I12) = t >= t0 = (7/4)/sqrt3; hence the fair die has d(C6) = d(RT24/12a).
# Solid angle of face i = area of the cell {x : p_i.x >= p_j.x for all j} on the unit sphere, p_i = (unit normal)/(depth).
# All tests below are exact in Q(sqrt5) (I12 points p = q/r with q = (0, 1/phi, phi) cyclic, |q| = sqrt3, depth t = r/sqrt3),
# except the solid-angle values used for the intermediate value step (arb ball arithmetic, rigorous).
import sys
from fractions import Fraction as Q
from qsqrt5 import *
from flint import arb, ctx
ctx.prec = 200
def pr(*a): print(*a, flush=True)
ONE = K(1); Z = K(0); H = K(Q(1, 2))
C6 = cyc_signs((ONE, Z, Z))
I12q = cyc_signs((Z, IPHI, PHI))                                   # |q|^2 = 3
RT24 = [scl(H, v) for v in cyc_signs((ONE, PHI, IPHI))]           # unit
def prodsign(v):
    s = 1
    for x in v: s *= (1 if x.sign() > 0 else -1)
    return s
# the die's RT24/12 orbit is the half containing (phi, 1/phi, 1)/2 (record 504: representative (phi, 1/phi, 1))
rep = scl(H, vec(PHI, IPHI, ONE)); RA = [v for v in RT24 if prodsign(v) == prodsign(rep)]; RB = [v for v in RT24 if prodsign(v) != prodsign(rep)]
assert rep in RA and len(RA) == 12 and len(RB) == 12
for v in RT24 + C6: assert dot(v, v) == ONE
for q in I12q: assert dot(q, q) == K(3)
# frame rotation group T: cyclic permutations x sign changes with product +1
TG = []
for k in range(3):
    for s in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]:
        TG.append(lambda v, k=k, s=s: tuple(K(s[i]) * v[(i + k) % 3] for i in range(3)))
for orb in (C6, I12q, RA, RB):
    for g in TG: assert all(g(v) in orb for v in orb)
pr('orbits: C6 %d, I12 %d, RT24/12a %d, RT24/12b (absent) %d; all T-invariant' % (len(C6), len(I12q), len(RA), len(RB)))
b = vec(-1, -1, -1)                                                 # an O8 axis whose three nearest RT24 are in RT24/12b
def cosb2(v):                                                       # sign of v.b and (v.b)^2 / (|v|^2 |b|^2)
    d = dot(v, b); return d.sign(), d * d / (dot(v, v) * K(3))
def near(L, c2): return [v for v in L if cosb2(v)[0] > 0 and (cosb2(v)[1] - c2).sign() > 0]
TRIP = near(I12q, K(Q(1, 2)))                                       # the I12 within 45 deg of b
RBT = near(RB, K(Q(3, 4)))                                          # RT24/12b within 30 deg
MC = [v for v in C6 if dot(v, b).sign() > 0]; MRA = [v for v in RA if cosb2(v)[0] > 0 and cosb2(v)[1] == K(Q(1, 3))]
assert len(TRIP) == 3 and len(RBT) == 3 and len(MC) == 3 and len(MRA) == 3
pr('around b = -(1,1,1): I12 triple %d, RT24/12b triple %d, C6 %d and RT24/12a %d at 54.74 deg' % (len(TRIP), len(RBT), len(MC), len(MRA)))
# a mirror of Ih through b: normal = an RT24 direction orthogonal to b
NS = [v for v in RT24 if dot(v, b) == Z]
def refl(n): return lambda v: sub(v, scl(K(2) * dot(n, v), n))   # |n| = 1
sig = None
for n in NS:
    s = refl(n)
    if all(s(v) in TRIP for v in TRIP) and all(s(v) in MRA for v in MC) and all(s(v) in MC for v in MRA) and all(s(v) in RBT for v in RBT):
        sig = s; sn = n; break
assert sig is not None
pr('mirror sigma (unit normal %s, orthogonal to b): permutes the I12 triple and the RT24/12b triple, swaps C6 <-> RT24/12a near b' % (sn,))
MCR = MC + MRA
# start polygon: triangle around b, every generator within 88 deg of b (pointed cone, contains cap(b, 86 deg))
START = [vec(-41, 19, 19), vec(19, -41, 19), vec(19, 19, -41)]
if dot(cross(sub(START[1], START[0]), sub(START[2], START[0])), b).sign() < 0: START = START[::-1]
r0 = K(Q(7, 4)); r1 = K(Q(176, 100))
def Ipts(r): return [scl(ONE / r, q) for q in I12q]
ALLCR = C6 + RA
def W_pieces(r):
    """E_I = {x : a triple member beats every point of TRIP + MCR}, E_R = same with RBT; each split by the MCR diagram"""
    I = [scl(ONE / r, q) for q in TRIP]
    EI, ER = [], []
    for k in range(3):
        base = region(START, 0, [I[k]] + I + MCR, range(1, 10))
        for m in range(6):
            pc = region(base, m, MCR, range(6))
            if pc: EI.append((k, m, pc))
        base = region(START, 0, [RBT[k]] + RBT + MCR, range(1, 10))
        for m in range(6):
            pc = region(base, m, MCR, range(6))
            if pc: ER.append((k, m, pc))
    return EI, ER
def le_on(poly, q, S):
    """q.x <= max_{s in S} s.x on poly (exact): refine poly by the S diagram, compare at the generators"""
    for i in range(len(S)):
        pc = region(poly, i, S, range(len(S)))
        if pc and not all((dot(S[i], v) - dot(q, v)).sign() >= 0 for v in pc): return False
    return True
ok = True
EI, ER = W_pieces(r0)
pr('W_b at t0 = (7/4)/sqrt3: E_I pieces %d, E_R pieces %d' % (len(EI), len(ER)))
I0 = Ipts(r0); TRIP0 = [scl(ONE / r0, q) for q in TRIP]
otherCR = [v for v in ALLCR if v not in MCR]; otherI = [p for p, q in zip(I0, I12q) if q not in TRIP]; otherRB = [v for v in RB if v not in RBT]
a1 = a2 = a3 = True
for (k, m, pc) in EI + ER:
    # (A1) every other C6/RT24a point loses to p_m, the MCR maximum on the piece
    a1 &= all(all((dot(MCR[m], v) - dot(q, v)).sign() >= 0 for v in pc) for q in otherCR)
    # (A2) every other I12 point at t0 loses to max(triple at t0, MCR)
    a2 &= all(le_on(pc, q, TRIP0 + MCR) for q in otherI)
    # (A3) every other RT24/12b point loses to max(RBT, MCR)
    a3 &= all(le_on(pc, q, RBT + MCR) for q in otherRB)
pr('on W_b: (A1) other C6/RT24a dominated:', a1, ' (A2) other I12 dominated:', a2, ' (A3) other RT24b dominated:', a3)
ok &= a1 and a2 and a3
# caps: E_I inside cap(b, 60 deg), E_R inside cap(b, 45 deg); 60 + 45 < 109.47 = angle between two axes of the T-orbit of b
capI = all(cosb2(v)[0] > 0 and (cosb2(v)[1] - K(Q(1, 4))).sign() >= 0 for (_, _, pc) in EI for v in pc)
capR = all(cosb2(v)[0] > 0 and (cosb2(v)[1] - K(Q(1, 2))).sign() >= 0 for (_, _, pc) in ER for v in pc)
orbit_b = {tuple(g(b)) for g in TG}
okb = len(orbit_b) == 4 and all(dot(c, c2) == K(-1) for c in orbit_b for c2 in orbit_b if c != c2)
pr('E_I in cap(b, 60 deg):', capI, ' E_R in cap(b, 45 deg):', capR, ' 4 axes T.b pairwise at arccos(-1/3) = 109.47 deg:', okb)
cover = {tuple(g(q)) for g in TG for q in TRIP} == set(map(tuple, I12q)) and {tuple(g(q)) for g in TG for q in RBT} == set(map(tuple, RB))
pr('T-images of the two triples cover all 12 I12 and all 12 RT24/12b:', cover)
ok &= capI and capR and cover and okb
# ---------- solid angles, rigorous (arb), for the intermediate value step and as a check ----------
def arbv(v):
    s5 = arb(5).sqrt(); return [arb(x.a.numerator) / x.a.denominator + arb(x.b.numerator) / x.b.denominator * s5 for x in v]
def area(poly):
    P = [arbv(v) for v in poly]; tot = arb(0)
    def d3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
    def dt(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    for i in range(1, len(P) - 1):     # Van Oosterom-Strackee fan (convex polygon)
        a, bb, c = P[0], P[i], P[i + 1]
        la, lb, lc = dt(a, a).sqrt(), dt(bb, bb).sqrt(), dt(c, c).sqrt()
        num = abs(d3(a, bb, c)); den = la * lb * lc + dt(a, bb) * lc + dt(a, c) * lb + dt(bb, c) * la
        tot += 2 * arb.atan2(num, den)
    return tot
OCTS = []
for s0 in (1, -1):
    for s1 in (1, -1):
        for s2 in (1, -1):
            o = [vec(s0, 0, 0), vec(0, s1, 0), vec(0, 0, s2)]
            if dot(cross(sub(o[1], o[0]), sub(o[2], o[0])), add(add(o[0], o[1]), o[2])).sign() < 0: o = o[::-1]
            OCTS.append(o)
def cellarea(P, k):
    tot = arb(0)
    for o in OCTS:
        pc = region(o, k, P, range(len(P)))
        if pc: tot += area(pc)
    return tot
T30 = 4 * arb.pi() / 30
ivt0 = ivt1 = False
for r in (r0, r1, K(Q(1758, 1000)), K(Q(2))):
    P = C6 + Ipts(r) + RA
    oc, oi, orr = cellarea(P, 0), cellarea(P, 6), cellarea(P, 18)
    pr('t = %s/sqrt3: Om_I - 4pi/30 = %s ; 2 Om_RA - Om_C - 4pi/30 = %s ; 6 Om_C + 12 Om_I + 12 Om_RA - 4pi = %s' % (
        float(r), (oi - T30).str(6), (2 * orr - oc - T30).str(6), (6 * oc + 12 * oi + 12 * orr - 4 * arb.pi()).str(6)))
    if r == r0: ivt0 = bool(oi > T30)
    if r == r1: ivt1 = bool(oi < T30)
pr('Om_I(t0) > 4pi/30:', ivt0, '  Om_I(t1) < 4pi/30 (t1 = 1.76/sqrt3):', ivt1)
ok &= ivt0 and ivt1
pr('FINAL ok' if ok else 'FINAL FAIL')
