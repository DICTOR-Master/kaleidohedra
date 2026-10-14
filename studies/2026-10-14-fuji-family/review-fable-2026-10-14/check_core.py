# Independent re-derivation of the FUJI-family paper's load-bearing numbers (Fable review for DICTO, 2026-10-14).
# Built from coordinates only; does not import the study scripts. DICTO · dictospheres.com
import numpy as np, itertools, math
phi=(1+5**.5)/2; deg=180/math.pi
def ang(u,v): return math.acos(np.clip(np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v),-1,1))*deg
def fuji(r):
    # hexagon: big triangle side 1+2r, corners cut by r; walk sides 1,r,1,r,... turning 60 deg
    P=[np.zeros(2)]; d=0
    for i in range(5):
        P.append(P[-1]+(1 if i%2==0 else r)*np.array([math.cos(d),math.sin(d)])); d+=math.pi/3
    P=np.array(P); P-=P.mean(0)
    R=np.linalg.norm(P,axis=1); h=math.sqrt(1-R[0]**2)
    B=np.c_[P,np.zeros(6)]; A=np.array([0,0,h])
    def base_angle(i):  # angle between base and face on side i..i+1
        a,b=B[i],B[(i+1)%6]; m=(a+b)/2; return ang(A-m, m - (m@np.array([0,0,1]))*0 - 0) if False else math.atan2(h, np.linalg.norm(m[:2]))*deg
    area=0.5*abs(sum(P[i,0]*P[(i+1)%6,1]-P[(i+1)%6,0]*P[i,1] for i in range(6)))
    return dict(R2=R.std(), h=h, L=base_angle(0), S=base_angle(1), V=area*h/3, sides=[round(float(np.linalg.norm(B[i]-B[(i+1)%6])),9) for i in range(6)])
print("== FUJI(r) formulas vs coordinates")
for r in [0,0.25,0.5,1/phi,(3**.5-1)/2,0.8,0.99]:
    f=fuji(r)
    hf=math.sqrt((2-r-r*r)/3); Lf=math.acos((1+2*r)/3)*deg; Sf=math.acos(math.sqrt((2+r)/(3*(2-r))))*deg; Vf=3**.5/12*(1+4*r+r*r)*hf
    print(f"r={r:.4f} h {f['h']:.6f}/{hf:.6f} L {f['L']:.4f}/{Lf:.4f} S {f['S']:.4f}/{Sf:.4f} V {f['V']:.6f}/{Vf:.6f} concyclic-spread {f['R2']:.1e}")
print("FUJI(r) base + 3 unit triangles on long sides = triangle of side 2+r; at r=1/phi:",2+1/phi,"phi^2=",phi**2)
print("\n== antiprism dihedral (triangle-triangle at side edge) from coordinates")
for n in range(3,13):
    t=math.pi/n; c=math.cos(t); R=1/(2*math.sin(t)); h=math.sqrt((1+2*c)/(8*(1+c)))
    T=lambda k:np.array([R*math.cos(2*k*t),R*math.sin(2*k*t),h]); Bt=lambda k:np.array([R*math.cos((2*k+1)*t),R*math.sin((2*k+1)*t),-h])
    assert abs(np.linalg.norm(T(0)-Bt(0))-1)<1e-12
    M=(T(0)+Bt(0))/2; e=Bt(0)-T(0); e/=np.linalg.norm(e)
    u=T(1)-M; u-=(u@e)*e; v=Bt(-1)-M; v-=(v@e)*e
    D=ang(u,v); r=(-3*math.cos(D/deg)-1)/2
    print(f"n={n:2d} D={D:.4f} formula {math.acos((1-4*c)/3)*deg:.4f}  r={r:.12f} 2cos(pi/n)-1={2*c-1:.12f}")
print("\n== face-plane members")
for name,cD in [("icosahedron",-5**.5/3),("cuboctahedron tri-sq",-1/3**.5),("rhombicuboct tri-sq",-(2/3)**.5),("octahedron",-1/3)]:
    print(name,(-3*cD-1)/2)
print("(sqrt3-1)/2",(3**.5-1)/2,"(sqrt6-1)/2",(6**.5-1)/2)
print("cuboct member height^2",(2-(3**.5-1)/2-((3**.5-1)/2)**2)/3,"1/2 ->",1/2**.5)
print("\n== Odom: extend unit triangle sides by e at both ends")
for e in [1,phi,1/phi,0.3]:
    V=[np.array([math.cos(a),math.sin(a)])/3**.5 for a in (math.pi/2,math.pi/2+2*math.pi/3,math.pi/2+4*math.pi/3)]
    pts=[]
    for i in range(3):
        a,b=V[i],V[(i+1)%3]; u=(b-a)/np.linalg.norm(b-a); pts+= [a-e*u, b+e*u]
    pts=np.array(pts); c=pts.mean(0); o=np.argsort(np.arctan2(*(pts-c).T[::-1])); pts=pts[o]
    s=[np.linalg.norm(pts[i]-pts[(i+1)%6]) for i in range(6)]
    angs=[ang(pts[i-1]-pts[i],pts[(i+1)%6]-pts[i]) for i in range(6)]
    print(f"e={e:.4f} sides {np.round(s,6)} angles {np.round(angs,4)} r={min(s)/max(s):.6f} e/(1+e)={e/(1+e):.6f}")
print("\n== k-families: flat limit r = (sqrt3 tan(pi/k)-1)cos(pi/k) = 2 sin(pi/k - pi/6)")
for k in range(3,8):
    t=math.pi/k; print(k,(3**.5*math.tan(t)-1)*math.cos(t), 2*math.sin(t-math.pi/6))
