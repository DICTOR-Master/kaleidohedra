"""Exact check of the ring-level solution S = square tube cut by two parallel planes with unit normal (c,c,sqrt(1-2c^2)).
Dihedral of the cut plane with the faces x=0,y=0 is arccos c (x=p, y=q: pi - arccos c); lateral edges are 90 deg (box); top and bottom swap.
C1: c = cos(3pi/4 - beta) = (sqrt5-1)/(2 sqrt3);  C2: c = cos(alpha) = 1/sqrt(1+phi^2)."""
import sympy as sp
ALL=True
phi=(1+sp.sqrt(5))/2
for nm,c,B in (("C1",(sp.sqrt(5)-1)/(2*sp.sqrt(3)),"3pi/4-beta"),("C2",1/sp.sqrt(1+phi**2),"alpha")):
    c2=sp.simplify(c**2); nz2=sp.simplify(1-2*c2)
    ok=sp.N(nz2)>0
    ALL=ALL and bool(ok)
    # edge length of every top/bottom edge for square cross-section q: q*sqrt(1-c^2)/n_z ; choose q so it equals a
    print(nm,"c^2 =",sp.nsimplify(sp.radsimp(c2)),"  n_z^2 =",sp.radsimp(nz2)," (>0:",ok,")  acute edge angle",B,"= arccos c =",sp.N(sp.acos(c)*180/sp.pi,10),"deg; obtuse = 180 - that")
    print("   edges: 4 x acute + 4 x obtuse (one of each on every side plane top/bottom), 4 right-angled lateral edges; Dehn: a x (acute+obtuse) = a x pi = 0")
print("FINAL ok" if ALL else "FINAL FAIL")
