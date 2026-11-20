"""Exact relation between the 600-cell and 5-cell dihedral angles.
cos(pi/3 + arccos(-1/4)) = (1/2)(-1/4) - (sqrt3/2)(sqrt15/4) = -1/8 - sqrt45/8 = -(1+3 sqrt5)/8,
and pi/3 + arccos(-1/4) lies in (0, pi) (it is 164.48 deg), so
theta_600 = pi/3 + arccos(-1/4) = pi/3 + pi - arccos(1/4) = 4pi/3 - theta_5.
Hence theta_600 = -theta_5 modulo Q*pi: the two nonzero invariants point in opposite directions
of the same line R (x) [theta_5]. D(5-cell) = A5 (x) [theta_5], D(600-cell) = -A600 (x) [theta_5]
with A5, A600 > 0 (total 2-face areas), so D(5-cell) != D(600-cell) at every scale
(their difference is (A5 + A600) (x) [theta_5] != 0 because [theta_5] != 0 in R/Q pi)."""
import math
t5=math.acos(1/4); t600=math.acos(-(1+3*math.sqrt(5))/8)
print("theta_600 =", t600, " 4pi/3 - theta_5 =", 4*math.pi/3 - t5, " diff", t600-(4*math.pi/3-t5))
print("sqrt3*sqrt15 = sqrt45 = 3 sqrt5:", math.sqrt(3)*math.sqrt(15), 3*math.sqrt(5))
print("FINAL ok" if abs(t600-(4*math.pi/3-t5))<1e-12 else "FINAL MISMATCH")
