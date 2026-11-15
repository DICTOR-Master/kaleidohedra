"""Exact Dehn invariant on a {0,1,t} family of Wythoff polyhedra.
Dehn(t) = 1 (x) X + t (x) Y,  X = sum over edge classes of length 2 of 2*count*theta, Y likewise for length 2t.
Angles are reduced in a Q-basis of their span modulo pi:
  A3, B3: every dihedral angle is p*pi + q*beta, beta = arctan(1/sqrt2) (cos 2beta = 1/3); found by search, PROVED by sympy
          (minimal polynomial of cos(theta) - cos(p pi + q beta) is x); beta/pi irrational (2cos 2beta = 2/3 is not an algebraic integer).
  H3: Q-relations among the distinct angles and pi by PSLQ (80 digits), each relation re-checked at 300 digits; completeness NOT proved.
Zero set: if t irrational, need X = Y = 0; if t rational, X + tY = 0 in the basis. So zeros are rational t (or the whole family)."""
import mpmath as mp
from fractions import Fraction as Fr
import sympy as sp

def beta_decompose(theta, cos2, cos_sign, D):
    """theta (mp) -> (p, q) with theta = p*pi + q*beta, exact proof by sympy; None if not of that form"""
    mp.mp.dps = 60
    beta = mp.atan(1/mp.sqrt(2))
    for q in range(-8, 9):
        x = (theta - q*beta)/mp.pi
        p = Fr(str(mp.nstr(x, 40))).limit_denominator(120)
        if abs(x - mp.mpf(p.numerator)/p.denominator) < mp.mpf(10)**-40:
            # exact proof
            a, b = cos2
            cexact = cos_sign*sp.sqrt(sp.Rational(a) + sp.Rational(b)*sp.sqrt(D))
            B = sp.atan(1/sp.sqrt(2))
            rhs = sp.expand_trig(sp.cos(sp.Rational(p.numerator, p.denominator)*sp.pi + q*B))
            rhs = sp.cos(sp.Rational(p.numerator, p.denominator)*sp.pi + q*B)
            diff = sp.nsimplify(0) + (cexact - sp.expand(sp.expand_trig(rhs.rewrite(sp.cos))))
            xx = sp.Symbol('x')
            try:
                mpol = sp.minimal_polynomial(sp.simplify(cexact - rhs.expand(trig=True)), xx)
                proved = (mpol == xx)
            except Exception:
                proved = False
            return (p, q, proved)
    return None

def pslq_basis(thetas):
    """greedy Q-basis of span(thetas) mod pi; returns basis indices and for each theta its rational coordinates (+ pi part)"""
    mp.mp.dps = 80
    basis = []   # list of mp values
    coords = []
    for th in thetas:
        vec = [th] + basis + [mp.pi]
        rel = mp.pslq(vec, maxcoeff=10**5, maxsteps=10**6)
        if rel is not None and rel[0] != 0:
            mp.mp.dps = 300
            # re-check at 300 digits with recomputed values is done by caller (angles recomputed); here check residual
            co = [Fr(-r, rel[0]) for r in rel[1:-1]]
            coords.append(co + [0]*0)
            mp.mp.dps = 80
        else:
            basis.append(th); coords.append(None)
    # rebuild coordinates against the final basis
    out = []
    bi = 0; idx = []
    nb = len(basis); full = []
    j = 0
    for th, co in zip(thetas, coords):
        if co is None:
            v = [Fr(0)]*nb; v[j] = Fr(1); j += 1; full.append(v)
        else:
            v = list(co) + [Fr(0)]*(nb - len(co)); full.append(v)
    return nb, full
