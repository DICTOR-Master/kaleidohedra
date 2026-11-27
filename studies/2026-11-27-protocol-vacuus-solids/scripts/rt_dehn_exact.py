"""EXACT Dehn invariant of the rhombic triacontahedron's special Vacuus-Solid (s = 3 - sqrt5; walls on the face planes of the RT
scaled by 1/phi). DICTO 27 Nov: "do the exact Dehn check of the RT member". With Claude (Anthropic). Sector build: one pit (one rhombus
face) carries every edge type; the symmetry group (order 120, edge- and face-transitive RT) copies it to all 30 pits (control done in
protocol.py: copied walls = direct walls). Edge types of the excavated solid: knife edges (the RT's 60 edges, between two pits),
pit edges from the tip to the 5-fold corners (60) and to the 3-fold corners (60). Dehn = sum over edges of length (x) material angle,
in R (x) R/Q pi. Each material angle is tested EXACTLY for being a rational multiple of pi: cos^2 of the angle, an exact algebraic
number, is compared (equal minimal polynomials, then numerically identified) with cos^2(p pi / q), q <= 120. If all three are rational
multiples of pi, every term vanishes and the Dehn invariant is exactly zero. Controls: the plain RT (dihedral 4 pi/5: zero) and the
excavated dodecahedron (nonzero by the screen) must come out as known."""
import os, sys, itertools
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, '../..')
src = open(os.path.join(ST, '2026-11-25-partial-vacuus/scripts/exact_check.py')).read(); exec(src[:src.index('fails = 0')])
r5 = sp.sqrt(5)
def S(x): return sp.nsimplify(x.a) + sp.nsimplify(x.b) * r5 if hasattr(x, 'a') else sp.nsimplify(x)
def vec(v): return tuple(v)
def rational_pi(c2, sign):
    """is the angle with cos^2 = c2 (exact) and sign(cos) = sign a rational multiple of pi? Candidate p/q (q <= 120) from the float
    value; then proved EXACTLY: the minimal polynomial of c2 equals that of cos^2(p pi/q) and the two agree numerically (so they are
    the same root). Returns p/q, or None (no candidate: not a rational multiple of pi with q <= 120, numerically)."""
    import math
    val = math.acos(math.copysign(math.sqrt(float(c2)), sign) if sign else 0.0) / math.pi
    best = None
    for q in range(1, 121):
        p = round(val * q)
        if abs(val - p / q) < 1e-11: best = (p, q); break
    if best is None: return None
    p, q = best; x = sp.Symbol('x')
    if sp.minimal_polynomial(c2, x) == sp.minimal_polynomial(sp.nsimplify(sp.cos(sp.pi * p / q) ** 2), x): return sp.Rational(p, q)
    return None
def kdot(u, w): return u[0] * w[0] + u[1] * w[1] + u[2] * w[2]
def ksub(u, w): return tuple(a - b for a, b in zip(u, w))
def kscl(t, u): return tuple(t * a for a in u)
def angle_info(u, w):
    """angle between vectors u, w (exact in Q(sqrt5)): cos^2 as a sympy number a + b sqrt5, and the sign of cos"""
    d = kdot(u, w); c2 = (d * d) / (kdot(u, u) * kdot(w, w)); sg = d.sign()
    return sp.Rational(c2.a.numerator, c2.a.denominator) + sp.Rational(c2.b.numerator, c2.b.denominator) * r5, sg
def perp(v, e): return ksub(v, kscl(kdot(v, e) / kdot(e, e), e))
def excavated(Pn, s, r=5):
    VP = body(Pn, r); FP = faces(VP); V = [vec(v) for v in VP]
    idx, N, d = FP[0]; tip = kscl(s * d / kdot(N, N), N)
    out = []
    # pit edges of face 0: tip -> corner w, walls (tip, a, w) and (tip, w, b); pyramid angle beta, material angle 2 pi - beta
    n = len(idx); seen = {}
    for t in range(n):
        a, w, b = V[idx[t - 1]], V[idx[t]], V[idx[(t + 1) % n]]; e = ksub(w, tip)
        c2, sg = angle_info(perp(ksub(a, tip), e), perp(ksub(b, tip), e)); L2 = kdot(e, e)
        deg = sum(1 for (jdx, _, _) in FP if idx[t] in jdx)
        out.append(('pit edge to a %d-fold corner' % deg, L2, c2, sg, 'material = 2 pi - pyramid angle'))
    # knife edge: face 0 and its neighbour g across edge (u, v)
    u_i, v_i = idx[0], idx[1]; g = next(k for k, (jdx, _, _) in enumerate(FP) if k != 0 and u_i in jdx and v_i in jdx)
    jdx, Ng, dg = FP[g]; tip_g = kscl(s * dg / kdot(Ng, Ng), Ng)
    u, v = V[u_i], V[v_i]; e = ksub(v, u)
    c2, sg = angle_info(perp(ksub(tip, u), e), perp(ksub(tip_g, u), e)); L2 = kdot(e, e)
    out.append(('knife edge (an edge of P)', L2, c2, sg, 'material = wedge between the two walls'))
    return out
def report(name, rows):
    allrat = True
    print(name, flush=True)
    for kind, L2, c2, sg, note in rows:
        q = rational_pi(c2, sg); allrat &= q is not None
        ang = sp.acos(sp.sign(sg) * sp.sqrt(c2)) if sg != 0 else sp.pi / 2
        print(f'  {kind}: length^2 = {L2}; angle {float(ang) * 180 / 3.141592653589793:.6f} deg, cos^2 = {c2}; '
              f'rational multiple of pi: {"yes, " + str(q) + " pi" if q is not None else "NO"} ({note})', flush=True)
    return allrat
# control 1: the plain RT, dihedral 4 pi / 5 (all edges alike)
VP = body('rhombic triacontahedron', 5); FP = faces(VP)
N0, N1 = tuple(FP[0][1]), tuple(next(F for F in FP[1:] if FP[0][0][0] in F[0] and FP[0][0][1] in F[0])[1])
c2, sg = angle_info(N0, N1)        # angle between outward normals = pi - dihedral
q = rational_pi(c2, sg); ctl1 = q is not None and sp.simplify(1 - q) == sp.Rational(4, 5)
print('control: rhombic triacontahedron dihedral = pi -', q, 'pi -> 4 pi/5:', ctl1, flush=True)
# control 2: the excavated dodecahedron must NOT be all-rational
ctl2 = not report('control: excavated dodecahedron (s = 5 - 2 sqrt5)', excavated('dodecahedron', K(5, -2, 5)))
print('control: excavated dodecahedron has an angle that is not a rational multiple of pi:', ctl2, flush=True)
zero = report('RHOMBIC TRIACONTAHEDRON special member (s = 3 - sqrt5)', excavated('rhombic triacontahedron', K(3, -1, 5)))
print('RESULT: every material angle is a rational multiple of pi, so every term L (x) angle vanishes in R (x) R/Q pi: the Dehn invariant is EXACTLY ZERO' if zero
      else 'RESULT: not every angle is a rational multiple of pi; zero would need a relation between the terms (not settled here)', flush=True)
print('FINAL ok' if ctl1 and ctl2 else 'FINAL FAIL (control)')
