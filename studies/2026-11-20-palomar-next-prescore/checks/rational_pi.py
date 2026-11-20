"""If theta is a rational multiple of pi, 2cos(theta) is an algebraic integer (a sum of two
roots of unity). 5-cell: 2cos = 1/2, rational and not an integer -> theta/pi irrational.
600-cell: x = 2cos = -(1+3*sqrt5)/4 is a root of 4x^2+2x-11 (irreducible over Q since sqrt5
is irrational; check: (4x+1)^2 = 45 -> 16x^2+8x-44 = 0). Leading coefficient 4 after removing
the content 4 from 16x^2+8x-44 -> primitive polynomial 4x^2+2x-11 is not monic -> not an
algebraic integer -> theta/pi irrational. The other four angles are pi/2, 2pi/3, 2pi/3, 4pi/5."""
import math
x=-(1+3*math.sqrt(5))/4
print("600-cell: 4x^2+2x-11 at x=2cos(theta):", 4*x*x+2*x-11)
print("600-cell: x vs 2cos(dihedral):", x, 2*math.cos(math.acos(-(1+3*math.sqrt(5))/8)))
from math import gcd
print("content of 16x^2+8x-44:", gcd(gcd(16,8),44), "-> primitive 4x^2+2x-11, leading coeff 4 != 1: not an algebraic integer")
print("5-cell: 2cos = 1/2 not an integer: not an algebraic integer")
ok = abs(4*x*x+2*x-11) < 1e-12 and abs(x - 2*math.cos(math.acos(-(1+3*math.sqrt(5))/8))) < 1e-12 \
     and gcd(gcd(16,8),44) == 4 and 16//4 != 1 and (2*0.25) != round(2*0.25)
print("FINAL ok" if ok else "FINAL FAIL: algebraic-integer test did not go through")
