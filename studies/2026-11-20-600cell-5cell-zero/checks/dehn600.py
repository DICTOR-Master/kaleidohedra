"""600-cell + 5-cells with Dehn invariant zero: exact checks in Q(sqrt5).
Exact arithmetic: numbers a+b*sqrt5 with a,b Fractions (class Q5); sympy for closed forms.
Floats only for the symmetry count (matching rounded centroids) and printed sanity values."""
from fractions import Fraction as F
from itertools import combinations, permutations
import math, sympy as sp

class Q5:
    __slots__=("a","b")
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): o=o if isinstance(o,Q5) else Q5(o); return Q5(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return Q5(-s.a,-s.b)
    def __sub__(s,o): return s+(-(o if isinstance(o,Q5) else Q5(o)))
    def __mul__(s,o): o=o if isinstance(o,Q5) else Q5(o); return Q5(s.a*o.a+5*s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s): d=s.a*s.a-5*s.b*s.b; return Q5(s.a/d,-s.b/d)
    def __truediv__(s,o): o=o if isinstance(o,Q5) else Q5(o); return s*o.inv()
    def __eq__(s,o): o=o if isinstance(o,Q5) else Q5(o); return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def f(s): return float(s.a)+float(s.b)*math.sqrt(5)
    def __repr__(s): return f"({s.a}+{s.b}*sqrt5)"

phi=Q5(F(1,2),F(1,2)); iphi=phi-1; h=Q5(F(1,2))
ok=True
def check(name,cond):
    global ok; ok&=bool(cond); print(("PASS " if cond else "FAIL ")+name)

# --- 600-cell vertices: the 120 unit quaternions of the binary icosahedral group
V=set()
for i in range(4):
    for s in (1,-1):
        v=[Q5(0)]*4; v[i]=Q5(s); V.add(tuple(v))
for sg in range(16):
    V.add(tuple(Q5(F(1,2)*(-1 if sg>>k&1 else 1)) for k in range(4)))
even=[p for p in permutations(range(4)) if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2==0]
base=[phi*h,h,iphi*h,Q5(0)]
for p in even:
    for sg in range(8):
        vals=[base[0]*(-1 if sg&1 else 1),base[1]*(-1 if sg&2 else 1),base[2]*(-1 if sg&4 else 1),Q5(0)]
        v=[None]*4
        for k in range(4): v[p[k]]=vals[k]
        V.add(tuple(v))
V=sorted(V,key=lambda v:tuple(x.f() for x in v)); N=len(V); idx={v:i for i,v in enumerate(V)}
dot=lambda u,w: sum((x*y for x,y in zip(u,w)),Q5(0))
check("120 vertices, all on the unit sphere", N==120 and all(dot(v,v)==1 for v in V))
cosE=phi*h  # cos 36 deg = phi/2 : neighbours at distance 1/phi
adj={i:set() for i in range(N)}
for i,j in combinations(range(N),2):
    if dot(V[i],V[j])==cosE: adj[i].add(j); adj[j].add(i)
E=sum(len(s) for s in adj.values())//2
d2=lambda u,w: dot(u,u)+dot(w,w)-2*dot(u,w)
check("720 edges, edge length^2 = 1/phi^2", E==720 and d2(V[0],V[min(adj[0])])==iphi*iphi)
T=[t for t in combinations(range(N),3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
C=[c for c in combinations(range(N),4) if all(c[j] in adj[c[i]] for i in range(4) for j in range(i+1,4))]
check("1200 triangles, 600 tetrahedral facets", len(T)==1200 and len(C)==600)
tri_cells={t:[] for t in T}
for k,c in enumerate(C):
    for t in combinations(c,3): tri_cells[t].append(k)
check("every triangle lies in exactly 2 facets", all(len(x)==2 for x in tri_cells.values()))
cen=[tuple(sum((V[i][k] for i in c),Q5(0)) for k in range(4)) for c in C]
cc=dot(cen[0],cen[0])
cosd=set(-dot(cen[a],cen[b])/cc for a,b in tri_cells.values())
check("one dihedral cosine for the 600-cell, = -(1+3 sqrt5)/8", cosd=={Q5(F(-1,8),F(-3,8))})

# --- closed forms (sympy)
s5=sp.sqrt(5); th5=sp.acos(sp.Rational(1,4)); d600=sp.acos(-(1+3*s5)/8)
check("cos(4pi/3 - theta5) = -(1+3sqrt5)/8 exactly", sp.simplify(sp.expand_trig(sp.cos(4*sp.pi/3-th5))+(1+3*s5)/8)==0)
check("4pi/3 - theta5 in (0,pi), equal to the 600-cell angle numerically", abs(float(4*sp.pi/3-th5)-float(d600))<1e-14 and 0<float(4*sp.pi/3-th5)<math.pi)
print("   theta5 =",float(th5*180/sp.pi),"deg ; 600-cell dihedral =",float(d600*180/sp.pi),"deg")
# theta5/pi irrational: if theta5 = (p/q) pi then 2cos(theta5)=1/2 would be an algebraic integer (sum of roots of unity); it is not.
check("2cos(theta5) = 1/2 is not an algebraic integer (so theta5 is not a rational multiple of pi)", sp.minimal_polynomial(sp.Rational(1,2),sp.Symbol('x')).as_poly().LC()!=1 or False)

a,b,n=sp.symbols('a b n',positive=True)
At=sp.sqrt(3)/4
D600=1200*At*a**2*(-1); D5=10*At*b**2   # coefficients of (area) (x) theta5, modulo Q pi
print("   total ridge area 600-cell:",sp.simplify(1200*At*a**2),"; 5-cell:",sp.simplify(10*At*b**2))
print("   D(600-cell, a) = ",sp.simplify(D600),"(x) theta5 ;  D(5-cell, b) = ",sp.simplify(D5),"(x) theta5   (mod Q pi)")
cond=sp.solve(sp.Eq(D600+n*D5,0),n)[0]
print("   union of one 600-cell and n 5-cells: invariant 0  <=>  n =",cond)
check("equal edges b=a: n = 120 exactly (the only, hence smallest, equal-edge solution)", cond.subs(b,a)==120)
# rational ratios b/a = p/q (lowest terms): n = 120 q^2/p^2 integer <=> p^2 | 120 <=> p in {1,2}
check("rational b/a with integer n: numerator p must divide... p^2|120 only for p=1,2", [p for p in range(1,12) if 120%(p*p)==0]==[1,2])

# --- arrangement: caps (5-cells) on 120 facets. Left multiplication by the 120 vertex quaternions.
def qmul(x,y):
    a1,b1,c1,d1=x; a2,b2,c2,d2=y
    return (a1*a2-b1*b2-c1*c2-d1*d2, a1*b2+b1*a2+c1*d2-d1*c2, a1*c2-b1*d2+c1*a2+d1*b2, a1*d2+b1*c2-c1*b2+d1*a2)
check("vertex set is closed under quaternion product (group 2I)", all(qmul(V[i],V[j]) in idx for i in range(0,N,7) for j in range(N)))
Cset={frozenset(c):k for k,c in enumerate(C)}
orbit_of=[None]*600; orbits=[]
for k,c in enumerate(C):
    if orbit_of[k] is None:
        o=set()
        for g in V:
            o.add(Cset[frozenset(idx[qmul(g,V[i])] for i in c)])
        for m in o: orbit_of[m]=len(orbits)
        orbits.append(sorted(o))
check("left multiplication splits the 600 facets into 5 orbits of 120", sorted(map(len,orbits))==[120]*5)
U=set(orbits[0])
shared=sum(1 for x,y in tri_cells.values() if x in U and y in U)
vcount=[sum(1 for k in U if i in C[k]) for i in range(N)]
print("   orbit 0: ridges shared by two capped facets =",shared,"; capped facets per vertex =",set(vcount))
# capped facets meeting at an edge
ecount={}
for k in U:
    for e in combinations(C[k],2): ecount[e]=ecount.get(e,0)+1
print("   orbit 0: capped facets per edge, distribution:",{m:list(ecount.values()).count(m) for m in set(ecount.values())},"(edges with none: %d)"%(720-len(ecount)))

# --- Dehn invariant of the augmented solid computed directly from its boundary ridges.
# angle = r*pi + c*theta5 ; record (area weight, c); only c survives modulo Q pi.
# 600-cell dihedral = 4/3 pi - theta5 ; 5-cell dihedral = theta5. Area weight 1 = one triangle.
coef=0; kinds={}
for t,(x,y) in tri_cells.items():
    k=(x in U)+(y in U)        # ridge angle = 4pi/3 - theta5 + k theta5
    kinds[k]=kinds.get(k,0)+1; coef+=(-1+k)
coef+=6*len(U)                 # each cap: 6 side ridges (base edge + apex), angle theta5
print("   600-cell ridges by number of adjacent caps:",kinds,"; cap side ridges:",6*len(U))
check("direct boundary sum: invariant of the augmented solid = 0 (x) theta5", coef==0)
check("ridge angles: 4pi/3 (rational multiple of pi) next to one cap; 4pi/3+theta5 between two caps",
      abs((4*math.pi/3-float(th5))+float(th5)-4*math.pi/3)<1e-15 and 2*float(th5)+float(d600)<2*math.pi)
print("   interior angle next to one cap = 240 deg (>180: reflex, so not convex); between two caps =",
      float((2*th5+d600)*180/sp.pi),"deg (<360: caps do not overlap there)")
# non-overlap: each cap = conv(facet, apex) with apex on the ray through the facet centroid, so the cap lies in
# the cone from the centre over its facet; these 600 cones have disjoint interiors (central fan of a convex polytope).
# check apex in its own cone: apex = s*centroid, s>0 -> barycentric coefficients s/4 each > 0 (exact by construction)
# heights (exact, sympy): unit circumradius, edge e=1/phi
e=1/sp.GoldenRatio
rin=sp.sqrt(sp.nsimplify(cc.f()))/4
rin=sp.sqrt(sp.Rational(cc.a)+sp.Rational(cc.b)*s5)/4
hcap=e*sp.sqrt(sp.Rational(5,8))
print("   unit circumradius: inradius =",sp.nsimplify(sp.simplify(rin)),"=",float(rin),"; cap height =",float(hcap),"; apex radius =",float(rin+hcap))
check("apex radius > 1: caps reach outside the circumsphere (star-shaped, spiky)", float(rin+hcap)>1)

# --- volumes (edge a for both kinds)
Vtet=lambda s: s**3/(6*sp.sqrt(2))
V600=sp.nsimplify(sp.simplify(600*Vtet(e)*rin/4*sp.GoldenRatio**4))  # rescale edge 1/phi -> 1
V600=sp.simplify((600*Vtet(e)*rin/4*sp.GoldenRatio**4).rewrite(sp.sqrt))
V5=sp.sqrt(5)/96
check("V(600-cell, edge 1) = (25/4)(2+sqrt5)", sp.simplify(V600-sp.Rational(25,4)*(2+s5))==0)
check("V(5-cell, edge 1) = sqrt5/96 (from height sqrt(5/8))", sp.simplify(Vtet(1)*sp.sqrt(sp.Rational(5,8))/4-V5)==0)
Vtot=sp.simplify(sp.Rational(25,4)*(2+s5)+120*V5)
phis=(1+s5)/2
check("total = (25+15sqrt5)/2 = 5 sqrt5 phi^2", sp.simplify(Vtot-(25+15*s5)/2)==0 and sp.simplify(Vtot-5*s5*phis**2)==0)
cube=sp.root(Vtot,4)
check("cube edge = 5^(3/8) sqrt(phi) a", abs(float(cube)-float(5**sp.Rational(3,8)*sp.sqrt(phis)))<1e-14)
print("   V600 =",float(sp.Rational(25,4)*(2+s5)),"; 120 V5 =",float(120*V5),"; total =",float(Vtot),"; cube edge =",float(cube),"a")
# n=30, b=2a variant
V30=sp.simplify(sp.Rational(25,4)*(2+s5)+30*16*V5)
print("   variant n=30, b=2a: total volume =",V30,"=",float(V30),"; cube edge",float(sp.root(V30,4)),"a")

# --- 3D echo: octahedron + 2 tetrahedra
tt=sp.acos(sp.Rational(1,3))
check("3D: octahedron dihedral = pi - arccos(1/3); oct (12 edges) + 2 tets (6 edges each) -> -12+12 = 0",
      abs(float(sp.acos(-sp.Rational(1,3)))-float(sp.pi-tt))<1e-15)
print("   3D: tet angle + oct angle = pi exactly (faces merge flat: convex union possible);",
      "4D: 5-cell angle + 600-cell angle = 4pi/3 (reflex: never convex)")

# --- symmetry of the chosen union (floats; rotations x -> l x r and reflections x -> l conj(x) r)
import numpy as np
Vf=np.array([[x.f() for x in v] for v in V])
def qm(x,y):
    a1,b1,c1,d1=x.T if x.ndim>1 else x; a2,b2,c2,d2=y.T if y.ndim>1 else y
    return np.stack([a1*a2-b1*b2-c1*c2-d1*d2, a1*b2+b1*a2+c1*d2-d1*c2, a1*c2-b1*d2+c1*a2+d1*b2, a1*d2+b1*c2-c1*b2+d1*a2],-1)
cf=np.array([[x.f() for x in c] for c in cen]); cf/=np.linalg.norm(cf,axis=1)[:,None]
key=lambda P:{tuple(np.round(p,6)+0.0) for p in P}
Uk=key(cf[sorted(U)]); allk=key(cf)
conj=np.array([1,-1,-1,-1.])
rot=refl=0
for l in Vf:
    L=qm(np.broadcast_to(l,cf[sorted(U)].shape),cf[sorted(U)])
    Lc=qm(np.broadcast_to(l,cf[sorted(U)].shape),cf[sorted(U)]*conj)
    for r in Vf:
        if key(qm(L,np.broadcast_to(r,L.shape)))==Uk: rot+=1
        if key(qm(Lc,np.broadcast_to(r,Lc.shape)))==Uk: refl+=1
print("   symmetries of the 600-cell (order 14400) keeping the 120 capped facets: rotations",rot//2,", reflections",refl//2)
check("chosen union keeps a symmetry group of order >= 120", (rot+refl)//2>=120)
print("FINAL ok" if ok else "FINAL MISMATCH")
