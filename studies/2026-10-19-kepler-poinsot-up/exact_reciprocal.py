# EXACT: the inward pieces are the golden reciprocals of the other star's points (DICTO 2026-10-19, "opposite structures", PiTet's principle).
# For a pyramid on a regular face: (height / face circumradius)^2, in Q(sqrt5).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '2026-10-19-five-fold-octet'))
exec(open(os.path.join(HERE, 'exact_kp.py')).read().split('def shell(')[0])
from exact_shells import cross
def ratio2(F, apex):
    c = cent(F); n = cross(sub(F[1], F[0]), sub(F[2], F[0])); hn = dot(sub(apex, c), n); h2 = hn * hn / dot(n, n); r2 = dot(sub(F[0], c), sub(F[0], c)); return h2 / r2
phi = PHI
p2 = PHI * PHI; p4 = p2 * p2
F0, tip0 = gsd[0]; print('great-star spike   (h/r)^2 =', ratio2(F0, tip0), ' phi^4 =', phi, ratio2(F0, tip0) == p4)
F1, tip1 = ssd[0]; print('small-star spire   (h/r)^2 =', ratio2(F1, tip1), ' phi^2 =', p2, ratio2(F1, tip1) == p2)
HD1_ = hullH(D1); o, i = HD1_['F'][0]; F = [HD1_['C'][j] for j in o]; n, d = HD1_['H'][i]; c = max(I, key=lambda v: dot(n, v).f())
print('great-shell cap     (h/r)^2 =', ratio2(F, c), ' phi^-2 =', Q5(1) / p2, ratio2(F, c) == Q5(1) / p2)
HI2 = hullH(I2); o, i = HI2['F'][0]; F = [HI2['C'][j] for j in o]; n, d = HI2['H'][i]; c = max(D1, key=lambda v: dot(n, v).f())
print('small-shell inward  (h/r)^2 =', ratio2(F, c), ' phi^-4 =', Q5(1) / phi, ratio2(F, c) == Q5(1) / p4)
