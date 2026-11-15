"""Values at the yantra of the factors of the scaled corner-t5 test."""
import json, os
from sage.all__sagemath_singular import QQ, PolynomialRing, RealField
R = RealField(200)
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
J = json.load(open(os.path.join(HERE, 'data', 'lean-deriv.json'))); kb = json.load(open(os.path.join(HERE, 'data', 'lean-kbox.json')))
Q = int(kb['Xs']['Q']); c = [R(int(n)) / Q for n in kb['Xs']['centre_num']]
u, tau, rho = c; t = u * tau; S = (1 + rho * (1 - u) * u**2) / (1 + u**2)
P3 = PolynomialRing(QQ, 'u,t,S')
def ev(p): return sum(R(QQ(cc)) * u**e[0] * t**e[1] * S**e[2] for e, cc in p)
V = [ev(r['N']) / ev(r['D']) for r in J['table']]
b5, Qv, b2, w6, w5 = V[20], V[12], V[17], V[16], V[21]
print('A=b5(1-b5)', b5 * (1 - b5), 'B=(Q-b2)^2', (Qv - b2)**2, 'C=w6^2', w6**2, 'D=(b5-b2)^2', (b5 - b2)**2)
print('q5 =', b5 * (1 - b5) - w5**2, ' b5-b2', b5 - b2, 'Q-b2', Qv - b2, 'w6', w6, 'w5', w5)
