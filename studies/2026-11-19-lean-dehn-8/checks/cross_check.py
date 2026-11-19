#!/usr/bin/env python3
"""Lean study 8 (Dehn canon): exact checks before the Lean proof that arccos(1/3), alpha, beta are
independent modulo pi, and of the facts the Lean proof uses.

theta = arccos(1/3), alpha = arccos(1/sqrt5), beta = arccos((3 - sqrt5)/R), R^2 = 3(10 - 2 sqrt5).
Exact arithmetic only (fractions), except block 6 (floating-point sanity) and block 7 (a search, floating).
"""
from fractions import Fraction as F
import math

out = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); out.append(s)

# ---- Q(sqrt5) as pairs (a, b) = a + b sqrt5 ----
def m5(x, y): return (x[0]*y[0] + 5*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def a5(x, y): return (x[0]+y[0], x[1]+y[1])
def s5(x, y): return (x[0]-y[0], x[1]-y[1])
def n5(x): return (-x[0], -x[1])
def inv5(x):
    d = x[0]*x[0] - 5*x[1]*x[1]
    return (x[0]/d, -x[1]/d)
def f5(x): return float(x[0]) + float(x[1])*math.sqrt(5)

# ---- block 1: theta. cos theta = 1/3 in Q, sin theta = (2/3) sqrt2 in Q sqrt2 ----
# represent cos(n theta) = c (rational), sin(n theta) = s * sqrt2 (s rational)
c1, s1 = F(1, 3), F(2, 3)
say("1. theta: cos = 1/3, sin = (2/3)sqrt2; cos^2 + sin^2 =", c1*c1 + 2*s1*s1)
c, s = F(1), F(0)
ok = True
th = math.acos(1/3)
for n in range(1, 61):
    # cos((n)θ) = cos((n-1)θ)cosθ - sin((n-1)θ)sinθ ; sin = sin cos + cos sin
    c, s = c*c1 - 2*s*s1, s*c1 + c*s1
    if c*c + 2*s*s != 1: ok = False
    if abs(float(c) - math.cos(n*th)) > 1e-9 or abs(float(s)*math.sqrt(2) - math.sin(n*th)) > 1e-9: ok = False
    if n == 2: say("   n = 2: cos 2theta =", c, ", sin 2theta =", s, "* sqrt2")
say("   n = 1..60: cos(n theta) in Q, sin(n theta) in Q*sqrt2, cos^2 + sin^2 = 1 exactly, floats agree:", ok)
say("   step used in Lean: cos((n+1)θ) = a/3 - (4/3) b, sin((n+1)θ) = (b/3 + 2a/3) sqrt2, if cos nθ = a, sin nθ = b sqrt2")

# ---- block 2: 2 alpha and 2 beta in Q(sqrt5) ----
ca, sa = (F(-3, 5), F(0)), (F(4, 5), F(0))
say("2. 2alpha: cos = -3/5, sin = 4/5 (= 2 sin a cos a = 2 (2sqrt5/5)(sqrt5/5) = 20/25); cos^2+sin^2 =",
    a5(m5(ca, ca), m5(sa, sa)))
cb = (F(-10, 30), F(-8, 30))
sb = (F(10, 15), F(-2, 15))
say("   2beta: cos = -(10 + 8sqrt5)/30, sin = (10 - 2sqrt5)/15; cos^2+sin^2 =", a5(m5(cb, cb), m5(sb, sb)))
# sin 2beta = 2 sin b cos b = 2 * (4/R) * ((3 - sqrt5)/R) = 8 (3 - sqrt5) / R^2, R^2 = 30 - 6 sqrt5
R2 = (F(30), F(-6))
s2b = m5((F(24), F(-8)), inv5(R2))
say("   8(3 - sqrt5)/R^2 =", s2b, "equals (10 - 2sqrt5)/15:", s2b == sb)
cosb2 = m5(m5((F(3), F(-1)), (F(3), F(-1))), inv5(R2))
say("   cos 2beta = 2cos^2 beta - 1 =", s5(m5((F(2), F(0)), cosb2), (F(1), F(0))), "(study 6 value -(10+8sqrt5)/30)")
al = math.acos(1/math.sqrt(5)); be = math.acos((3 - math.sqrt(5))/math.sqrt(3*(10 - 2*math.sqrt(5))))
say("   floats: cos 2a", math.cos(2*al), f5(ca), "; sin 2a", math.sin(2*al), f5(sa))
say("   floats: cos 2b", math.cos(2*be), f5(cb), "; sin 2b", math.sin(2*be), f5(sb))

# ---- block 3: closure. cos, sin of Q*2alpha + R*2beta lie in Q(sqrt5) ----
def powang(c0, s0, n):
    c, s = (F(1), F(0)), (F(0), F(0))
    cc, ss = c0, (s0 if n >= 0 else n5(s0))
    for _ in range(abs(n)):
        c, s = s5(m5(c, cc), m5(s, ss)), a5(m5(s, cc), m5(c, ss))
    return c, s
ok = True
for Q in range(-12, 13):
    cq, sq = powang(ca, sa, Q)
    for Rr in range(-12, 13):
        cr, sr = powang(cb, sb, Rr)
        cs, ss = s5(m5(cq, cr), m5(sq, sr)), a5(m5(sq, cr), m5(cq, sr))
        if a5(m5(cs, cs), m5(ss, ss)) != (F(1), F(0)): ok = False
        x = Q*2*al + Rr*2*be
        if abs(f5(cs) - math.cos(x)) > 1e-8 or abs(f5(ss) - math.sin(x)) > 1e-8: ok = False
say("3. |Q|, |R| <= 12: cos, sin of Q*2alpha + R*2beta computed in Q(sqrt5), modulus 1 exactly, floats agree:", ok)

# ---- block 4: the separation lemma b sqrt2 = c + d sqrt5 => b = 0 ----
say("4. (b sqrt2 - d sqrt5)^2 = 2b^2 + 5d^2 - 2bd sqrt10, so bd != 0 would make sqrt10 rational;",
    "if d = 0 then b sqrt2 = c forces b = 0. 10 is not a square:", all(k*k != 10 for k in range(11)))

# ---- block 5: the hinted valuation route, checked on paper (not used in Lean) ----
# Z[sqrt-2]: (x, y) = x + y sqrt-2
def mm2(p, q): return (p[0]*q[0] - 2*p[1]*q[1], p[0]*q[1] + p[1]*q[0])
p1 = (1, -1)  # 1 - sqrt-2
p4 = mm2(mm2(p1, p1), mm2(p1, p1))
say("5. (1 - sqrt-2)^4 =", p4, "= -7 + 4 sqrt-2, so e^{2i theta} = (1 - sqrt-2)^2/(1 + sqrt-2)^2:",
    "valuation -2 and +2 at the two primes 1 +- sqrt-2 above 3 (3 = (1+sqrt-2)(1-sqrt-2))")
# Z[i]: (1 + 2i)^2
say("   (1 + 2i)^2 = -3 + 4i, so e^{2i alpha} = (1+2i)/(1-2i): valuations +-1 at the primes above 5 only")
# 15 e^{2i beta} = -(5 + 4 sqrt5) + (10 - 2 sqrt5) i; its norm to Q(sqrt5) is 225
w = (F(-5), F(-4)); v = (F(10), F(-2))
say("   |15 e^{2i beta}|^2 =", a5(m5(w, w), m5(v, v)), "(= 225): e^{2i beta} lives above 3 and 5 in Q(sqrt5, i)")
say("   Route not used: Q(sqrt-2) and Q(sqrt5, i) have intersection Q (the quadratic subfields of Q(sqrt5, i)",
    "are Q(sqrt5), Q(i), Q(sqrt-5)), which the Lean proof uses in the form: sqrt2 is not in Q(sqrt5).")

# ---- block 6: floats of the three angles ----
say("6. floats: theta =", th, "alpha =", al, "beta =", be, "(degrees", math.degrees(th), math.degrees(al), math.degrees(be), ")")

# ---- block 7: floating sanity search for small relations p theta + q alpha + r beta = k pi ----
best = None
B = 40
for p in range(0, B+1):
    for q in range(-B, B+1):
        for r in range(-B, B+1):
            if p == 0 and q == 0 and r == 0: continue
            x = (p*th + q*al + r*be) / math.pi
            d = abs(x - round(x))
            if best is None or d < best[0]: best = (d, p, q, r)
say("7. float sanity: over 0 <= p <= 40, |q|, |r| <= 40, not all 0, the closest (p theta + q alpha + r beta)/pi",
    "comes to an integer is", "%.3e" % best[0], "at (p, q, r) =", best[1:], "(no exact relation; floats only)")

open(__file__.replace(".py", ".out"), "w").write("\n".join(out) + "\n")
