"""Vertex ledger at a truncated-icosahedron vertex v of C1 (exact, basis pi, alpha, beta; independence proved earlier).
The vertex figure of a piece at v is a spherical polygon; its area (solid angle) is  sum of corner angles - (n-2) pi  (Girard).
Pieces at v: C1 seen from a TI vertex (4 corners: hh, hp, hp, ss), the apex cone of a dodecahedron centre pyramid (5 corners of 2pi/3),
and unknown K pieces.  Also the orientation ledger of the three pyramids around one ss edge (apex end A, base end v)."""
import json, math
from fractions import Fraction as F
import sympy as sp
al=sp.atan((1+sp.sqrt(5))/2); be=sp.acos(1/sp.sqrt(6)); pi=sp.pi
hh=3*pi/2-2*be; hp=3*pi/4-al+be; sd=2*pi/3
corners_C1=[hh, hp+al, hp+al, sd]              # interior dihedrals of C1 at the four edges through v
area_C1=sp.simplify(sum(corners_C1)-2*pi)
ext=[2*pi-x for x in corners_C1]; area_ext=sp.simplify(sum(ext)-2*pi)
apex=sp.simplify(5*sd-3*pi)
out={}
def pr(s): print(s,flush=True)
pr(f"C1 vertex cone at a TI vertex: corners (deg) {[round(float(sp.N(x*180/pi)),4) for x in corners_C1]}, solid angle = {area_C1} (5pi/3: {sp.simplify(area_C1-5*pi/3)==0})")
pr(f"exterior polygon X (what C1 leaves at v): corners {[round(float(sp.N(x*180/pi)),4) for x in ext]}, solid angle = {area_ext} (7pi/3: {sp.simplify(area_ext-7*pi/3)==0})")
pr(f"apex cone of a dodecahedron centre pyramid: {apex}")
ok_all=sp.simplify(area_C1-5*pi/3)==0 and sp.simplify(area_ext-7*pi/3)==0 and sp.simplify(apex-pi/3)==0
# ss ring: three pyramids around the ss edge A-v; k of them have their base end at v (C1 cone 5pi/3 there), 3-k have apex at v (pi/3)
rows=[]
for k in range(4):
    atv=F(5,3)*k+F(1,3)*(3-k); atA=F(1,3)*k+F(5,3)*(3-k)
    rows.append(dict(k=k,at_v=str(atv)+"pi",left_at_v=str(4-atv)+"pi",at_A=str(atA)+"pi",left_at_A=str(4-atA)+"pi",possible=bool(atv<=4 and atA<=4)))
    pr(f"k={k} pyramids with base end at v: C1/apex cones at v {atv} pi (left {4-atv} pi), at A {atA} pi (left {4-atA} pi) -> {'possible' if atv<=4 and atA<=4 else 'impossible (cones overlap)'}")
out=dict(C1_cone="5pi/3",exterior="7pi/3",apex_cone="pi/3",ss_orientations=rows,
 demands_at_v={"hh":"T+T = 2pi - hh","hp":"B+Q","hp2":"B+Q"})
json.dump(out,open('data/scutoid.json','w'),indent=1)
pr("FINAL ok" if ok_all else "FINAL FAIL")
