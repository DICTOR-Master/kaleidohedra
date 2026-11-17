# Exact: with c = cos(2pi/7), the fair die's b^2 = 2T equals 1/c^2 - 2. Consequences:
#  (1) the 12 square-hexagon Vacuus plates have unit normals (c, c, b c) up to symmetry: each makes angle 2pi/7 with two cube axes;
#  (2) roundness r/R = 1/sqrt(1+b^2) = cot(2pi/7) = tan(3pi/14).
import sympy as sp
c=sp.cos(2*sp.pi/7); x=sp.symbols('x')
T=sp.tan(sp.pi/14)*sp.tan(2*sp.pi/7)
ok=True
mc=sp.minimal_polynomial(c,x); print('min poly of c:',mc); ok&= sp.expand(mc-(8*x**3+4*x**2-4*x-1))==0
# T = 9 - 4c - 16c^2 (gods-dice, sympy to_number_field): check numerically to 60 digits and by min poly
d=sp.N(T-(9-4*c-16*c**2),60); print('T - (9-4c-16c^2) =',d); ok&=abs(d)<1e-55
# identity 2T = 1/c^2 - 2  <=>  c^2 (2(9-4c-16c^2)+2) - 1 = 0 modulo 8c^3+4c^2-4c-1
r=sp.rem(sp.expand(x**2*(2*(9-4*x-16*x**2)+2)-1), 8*x**3+4*x**2-4*x-1, x); print('remainder:',r); ok&= r==0
b2=2*(9-4*c-16*c**2)
n=sp.Matrix([1,1,sp.sqrt(b2)]); n=n/sp.sqrt(2+b2)
print('normal . x-axis =',sp.N(n[0],30),' cos(2pi/7) =',sp.N(c,30)); ok&=abs(sp.N(n[0]-c,60))<1e-55
rR=1/sp.sqrt(1+b2); print('r/R =',sp.N(rR,30),' cot(2pi/7) =',sp.N(sp.cot(2*sp.pi/7),30),' tan(3pi/14) =',sp.N(sp.tan(3*sp.pi/14),30))
ok&=abs(sp.N(rR-sp.cot(2*sp.pi/7),60))<1e-55
# control: a wrong angle must fail
ok&=abs(sp.N(n[0]-sp.cos(sp.pi/7),30))>1e-3
print('FINAL ok' if ok else 'FINAL FAIL')
