# High-precision check (120 digits, Python decimal) of the angle relations of the three words.
# Only square roots are used: cos and sin of each angle are nested radicals, and the relations are checked
# through cos and sin of the sums (addition formulas), together with double-precision values for the ranges.
from decimal import Decimal as D, getcontext
import math
getcontext().prec = 120
s5 = D(5).sqrt()
r = (3*(10-2*s5)).sqrt()
ca, sa = s5/5, (1-(s5/5)**2).sqrt()
cb = (3-s5)/r; sb = (1-cb*cb).sqrt()
cg = s5/3; sg = (1-cg*cg).sqrt()
ce = (s5+1)/r; se = (1-ce*ce).sqrt()
def add(c1,s1,c2,s2): return c1*c2-s1*s2, s1*c2+c1*s2
c2b,s2b = add(cb,sb,cb,sb)
c,s = add(ca,sa,c2b,s2b)          # alpha + 2 beta
c,s = add(c,s,cg,-sg)             # - gamma
print("cos(alpha+2beta-gamma)+1 =", c+1); print("sin(alpha+2beta-gamma)   =", s)
c,s = add(cb,sb,cg,-sg)           # beta - gamma
print("cos(beta-gamma)-cos(eps) =", c-ce); print("sin(beta-gamma)-sin(eps) =", s-se)
c,s = add(ca,sa,cb,sb); c,s = add(c,s,ce,se)
print("cos(alpha+beta+eps)+1    =", c+1); print("sin(alpha+beta+eps)      =", s)
print("exact forms: sin beta - 4/r =", sb-4/r, "; sin eps - (2 sqrt5 - 2)/r =", se-(2*s5-2)/r, "; sin alpha - 2 sqrt5/5 =", sa-2*s5/5, "; sin gamma - 2/3 =", sg-D(2)/3)
al,be,ga,ep = (math.degrees(math.acos(float(x))) for x in (ca,cb,cg,ce))
print("degrees: alpha %.10f beta %.10f gamma %.10f eps %.10f" % (al,be,ga,ep))
print("alpha+2beta-gamma = %.10f, beta-gamma-eps = %.3e, alpha+beta+eps = %.10f" % (al+2*be-ga, be-ga-ep, al+be+ep))
