# Sphere as the perfect value (DICTO 18 Nov 2026: "the computation if it's of a sphere as perfect value").
# For each die: IQ = 36 pi V^2 / S^3 (sphere 1), roundness r/R (sphere 1), landing isotropy:
# Q4, Q6 of the face normals weighted by solid angle (sphere: 0; Steinhardt-Nelson-Ronchetti 1983).
# Note (DICTO 18 Nov): "sphere as perfect value" was meant for the shape language; here it is the die chapter's comparison table.
# Exact where sympy can (closed forms); hull check in floats. Labels: exact / computed.
import itertools, json, math, os, sys
import numpy as np
from scipy.spatial import ConvexHull
from scipy.special import sph_harm_y
import sympy as sp
phi=(1+5**.5)/2
def perms_signs(t,cyc=False,even=False):
    out=set()
    P=[(0,1,2),(1,2,0),(2,0,1)] if cyc else list(itertools.permutations(range(3)))
    for p in P:
        for s in itertools.product([1,-1],repeat=3):
            v=tuple(s[i]*t[p[i]] for i in range(3)); out.add(tuple(round(x,12) for x in v))
    return np.array(sorted(out),float)
def faces(pts):
    h=ConvexHull(pts); planes={}
    for eq in h.equations:
        k=tuple(np.round(eq,9)); planes[k]=eq
    F=[]
    for eq in planes.values():
        n=eq[:3]; d=-eq[3]; idx=[i for i,p in enumerate(pts) if abs(p@n-d)<1e-9]
        P=pts[idx]; c=P.mean(0); u=P[0]-c; u/=np.linalg.norm(u); w=np.cross(n,u)
        P=P[np.argsort([math.atan2((q-c)@w,(q-c)@u) for q in P])]
        F.append((n,d,P))
    return h,F
def solid_angle(P):  # polygon P seen from origin: fan of triangles (Van Oosterom-Strackee)
    c=P.mean(0); tot=0
    for i in range(len(P)):
        a,b=P[i],P[(i+1)%len(P)]; tri=[c,a,b]; A,B,C=[x/np.linalg.norm(x) for x in tri]
        num=abs(A@np.cross(B,C)); den=1+A@B+B@C+C@A; tot+=2*math.atan2(num,den)
    return tot
def Ql(dirs,w,l):
    th=np.arccos(np.clip(dirs[:,2],-1,1)); ph=np.arctan2(dirs[:,1],dirs[:,0])
    q=[np.sum(w*sph_harm_y(l,m,th,ph))/np.sum(w) for m in range(-l,l+1)]
    return math.sqrt(4*math.pi/(2*l+1)*sum(abs(x)**2 for x in q))
T=math.tan(math.pi/14)*math.tan(2*math.pi/7); muf=1+math.sqrt(2*T); bf=muf-1
DIES=[("dodecahedron (d12)", np.vstack([perms_signs((1,1,1)),perms_signs((0,1/phi,phi),cyc=True)])),
 ("icosahedron (d20)", perms_signs((0,1,phi),cyc=True)),
 ("cube (d6)", perms_signs((1,1,1))),
 ("tetrahedron (d4)", np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)),
 ("octahedron (d8)", perms_signs((1,0,0))),
 ("rhombic dodecahedron (d12)", np.vstack([perms_signs((1,1,1)),perms_signs((2,0,0))])),
 ("fair 14-face die", perms_signs((1,bf,0))),
 ("truncated octahedron (unfair 14)", perms_signs((0,1,2))),
 ("truncated cube (unfair 14)", perms_signs((1,1,math.sqrt(2)-1))),
 ("cube-octahedron line best IQ, mu=sqrt3", perms_signs((1,math.sqrt(3)-1,0)))]
log=[]; rows=[]; ok=True
def say(s): print(s); log.append(s)
for name,pts in DIES:
    h,F=faces(pts); V=h.volume; S=h.area; IQ=36*math.pi*V**2/S**3
    r=min(d for n,d,P in F); R=max(np.linalg.norm(pts,axis=1)); 
    om=np.array([solid_angle(P) for n,d,P in F]); N=np.array([n for n,d,P in F])
    spread=(om.max()-om.min())/(4*math.pi/len(F))
    q4,q6=Ql(N,om,4),Ql(N,om,6)
    rows.append(dict(die=name,faces=len(F),IQ=IQ,r_over_R=r/R,solid_angle_sum_check=om.sum()/(4*math.pi),fairness_spread=spread,Q4=q4,Q6=q6))
    say(f"{name:40s} F={len(F):2d} IQ={IQ:.6f} r/R={r/R:.6f} sumOmega/4pi={om.sum()/(4*math.pi):.12f} spread={spread:.2e} Q4={q4:.4f} Q6={q6:.4f}")
    ok&=abs(om.sum()-4*math.pi)<1e-9
# controls: classical IQ values
ctl={"cube (d6)":math.pi/6,"octahedron (d8)":math.pi/(3*math.sqrt(3)),"tetrahedron (d4)":math.pi/(6*math.sqrt(3))}
for k,v in ctl.items():
    g=[r for r in rows if r['die']==k][0]['IQ']; say(f"control IQ {k}: {g:.12f} vs {v:.12f}"); ok&=abs(g-v)<1e-10
fd=[r for r in rows if r['die']=='fair 14-face die'][0]; ok&=fd['fairness_spread']<1e-10
# exact: fair die IQ and r/R minimal polynomials
b=sp.symbols('b',positive=True); x=sp.symbols('x')
pb=sp.Poly(b**6-18*b**4-4*b**2+8,b)   # minimal polynomial of b_f (fair-die-full step 1)
mu=1+b
V=sp.Rational(8)-sp.Rational(4,3)*(mu-1)**3*0  # placeholder replaced below
# volume of S(mu) on chamber I: cube minus 8 corner tetrahedra cut by |x|+|y|+|z|<=mu: corner simplex leg (3-mu)
V=sp.Rational(4,3)*mu**3-4*(mu-1)**3   # octahedron(mu) minus 6 caps beyond |x|>1, each 2(mu-1)^3/3
# area: 6 squares (side sqrt2*b) + 8 hexagons = equilateral triangle side sqrt2*(3-mu... ) computed as triangle minus 3 corners
sq=2*b**2
tri_side=sp.sqrt(2)*(3-1)  # hexagon lies in plane x+y+z=mu inside cube: big triangle with corners (mu,0,0)...
# hexagon = triangle side mu*sqrt2 minus 3 corner triangles of side (mu-1)*sqrt2
hexa=sp.sqrt(3)/4*(2*mu**2-3*2*(mu-1)**2)
S=6*sq+8*hexa
IQe=36*sp.pi*V**2/S**3
val=float(IQe.subs(b,bf)); say(f"exact-form IQ at b_f = {val:.12f} (hull {fd['IQ']:.12f})"); ok&=abs(val-fd['IQ'])<1e-10
# IQ/pi is algebraic: minimal polynomial via resultant
y=sp.symbols('y')
num=sp.expand(36*V**2); den=sp.expand(S**3)
# S contains sqrt3: S = A + sqrt3*B ; IQ/pi = num/S^3. eliminate sqrt3 and b
s3=sp.symbols('s3')
den2=sp.expand((6*sq+8*sp.Rational(1,4)*s3*(2*mu**2-6*(mu-1)**2))**3)
R1=sp.resultant(sp.expand(y*den2-num),pb.as_expr(),b)
R2=sp.resultant(R1,s3**2-3,s3)
fac=sp.factor_list(sp.Poly(R2,y))[1]
target=val/math.pi
best=min(fac,key=lambda f:abs(sp.Poly(f[0],y).eval(target)) if True else 0)
mp=sp.Poly(best[0],y); roots=[complex(r) for r in mp.nroots(n=30)]
hit=min(abs(r-target) for r in roots)
say(f"IQ/pi minimal polynomial degree {mp.degree()}: {mp.as_expr()}  (root error {hit:.1e})"); ok&=hit<1e-12
# r/R = 1/sqrt(1+b^2): (r/R)^2 = 1/(1+b^2)
R3=sp.resultant(sp.expand(y*(1+b**2)-1),pb.as_expr(),b); f3=sp.factor_list(sp.Poly(R3,y))[1]
t3=fd['r_over_R']**2; m3=min(f3,key=lambda f:abs(sp.Poly(f[0],y).eval(t3)))[0]
say(f"(r/R)^2 minimal polynomial: {sp.Poly(m3,y).as_expr()}")
os.makedirs('../data',exist_ok=True)
json.dump(dict(rows=rows,IQ_over_pi_minpoly=str(mp.as_expr()),rR2_minpoly=str(sp.Poly(m3,y).as_expr())),open('../data/sphere-score.json','w'),indent=1)
say("FINAL ok" if ok else "FINAL FAIL")
open('../data/sphere-score.log','w').write("\n".join(log)+"\n")
