"""Exploration for the Lean derivation (step 2): sizes of every construction quantity as a reduced fraction in (u, t, S) and in
(u, tau, rho), and the factors of the denominators."""
from sage.all__sagemath_singular import QQ, PolynomialRing
R3 = PolynomialRing(QQ, 'u,t,S'); u, t, S = R3.gens(); Fr = R3.fraction_field(); u, t, S = Fr(u), Fr(t), Fr(S); one = Fr(1)
v = u; P = v**2/(1+v**2); R = one/(1+u**2); w3 = v/(1+v**2); w7 = u/(1+u**2)
b1 = t**2/(1+t**2); w1 = t/(1+t**2)
xW = w7*P/R; xX = xW*(S-R)/(S-P); k9 = xX/(R-P); w9 = k9*(S-P); k3 = w3/(1-P); xZ = k3*(1-R)
c138 = w1*(R-b1) - xZ*(P-b1); Q = (w1*P*(R-b1) - xZ*b1*(P-b1))/c138
m1 = w1/(Q-b1); b8 = (k3+k9*P)/(k3+k9); xF = k9*(Q-P); w6 = xW*(S-Q)/(S-P); k7 = w7/R
b2 = m1*Q/(m1+k7); c4 = xF/(b8-Q); c8 = xZ/(R-b1); b4 = (c4*b8+c8*b1)/(c4+c8)
b5 = (m1*Q+k9*P)/(m1+k9); w5 = w6*(b5-b2)/(Q-b2)
names = dict(P=P,R=R,w3=w3,w7=w7,b1=b1,w1=w1,xW=xW,xX=xX,k9=k9,w9=w9,k3=k3,xZ=xZ,c138=c138,Q=Q,m1=m1,b8=b8,xF=xF,w6=w6,k7=k7,b2=b2,c4=c4,c8=c8,b4=b4,b5=b5,w5=w5,
  w2=xW*(S-b2)/(S-P), w4=xF*(b8-b4)/(b8-Q), w8=xZ*(b8-b1)/(R-b1))
for k, q in names.items():
    n, d = q.numerator(), q.denominator()
    print(k, len(n.monomials()), n.degree(), '/', len(d.monomials()), d.degree(), '| den factors:', [(str(f)[:40], m) for f, m in d.factor()][:8])
