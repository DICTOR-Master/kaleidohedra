"""Exact C1, C2 (gluing) from the exact dihedrals of studies/2026-11-21-packet-leads-tiling/data/angles.json,
vectors in the basis (pi, alpha, beta, gamma) with Fractions. Demand = 2pi - theta (ring) and pi - theta (on a face).
Scutoid identity checked: a side plane between two parallel faces gives top theta, bottom pi-theta."""
import json, math
from fractions import Fraction as F
import sympy as sp
al=math.atan((1+5**.5)/2); be=math.acos(6**-.5); ga=math.acos((2/3)**.5)
def deg(v): return (float(v[0])*math.pi+float(v[1])*al+float(v[2])*be+float(v[3])*ga)*180/math.pi
V=lambda p,a,b,g:(F(p),F(a),F(b),F(g))
add=lambda u,v:tuple(x+y for x,y in zip(u,v)); sub=lambda u,v:tuple(x-y for x,y in zip(u,v))
sc=lambda k,u:tuple(F(k)*x for x in u)
PI=V(1,0,0,0)
out={}
def pr(s): print(s,flush=True)
# pieces (exact dihedrals, data/angles.json of packet-leads study)
TI_hh=V(F(3,2),0,-2,0); TI_ph=V(F(3,4),-1,1,0); TI_pent_pyr_base=V(0,1,0,0); D_ss=V(F(2,3),0,0,0)
TD_dd=V(0,2,0,0); TD_td=V(F(3,4),-1,1,0); I_base=V(F(3,4),0,-1,0); I_ss=V(F(2,5),0,0,0)
# length classes: 'a' = common edge, 'R' = centre-to-vertex edge
C1=[("hexagon-hexagon","a",30,TI_hh),("pyramid side-hexagon (reflex)","a",60,add(TI_ph,TI_pent_pyr_base)),("pyramid side-side","R",60,D_ss)]
C2=[("decagon-decagon","a",30,TD_dd),("pyramid side-decagon (reflex)","a",60,add(TD_td,I_base)),("pyramid side-side","R",60,I_ss)]
# face-edge check: pentagon edges of TI (60) each carry TI_ph and the pyramid base angle; triangle edges of TD (60) likewise
def packet(C):
    P={}
    for n,l,c,t in C:
        key=l; cur=P.get(key,(F(0),)*3)
        P[key]=tuple(x+c*y for x,y in zip(cur,t[1:]))
    return P
res={}
for nm,C in (("C1 = truncated icosahedron + dodecahedron centre pyramid on each pentagon (12:1)",C1),("C2 = truncated dodecahedron + icosahedron centre pyramid on each triangle (20:1)",C2)):
    pr("== "+nm)
    P=packet(C); z=all(all(x==0 for x in v) for v in P.values())
    pr(f"packet (alpha,beta,gamma coefficients per length class, pi part is 0 in the tensor): {({k:[str(x) for x in v] for k,v in P.items()})}  zero={z}")
    rows=[]
    for n,l,c,t in C:
        d=deg(t); dem=sub(sc(2,PI),t); onf=sub(PI,t)
        rows.append(dict(edge=n,length=l,count=c,theta=[str(x) for x in t],theta_deg=round(d,4),reflex=d>180,
            ring_demand=[str(x) for x in dem],ring_demand_deg=round(deg(dem),4),
            face_demand=[str(x) for x in onf],face_demand_deg=round(deg(onf),4),face_possible=deg(onf)>0))
        pr(f"{n:32s} x{c:2d} theta=[{','.join(str(x) for x in t)}] {d:8.4f}  ring: [{','.join(str(x) for x in dem)}] {deg(dem):8.4f}  on-face: {deg(onf):8.4f} {'(impossible: reflex)' if deg(onf)<0 else ''}")
    res[nm]=dict(packet_zero=z,rows=rows)
    # beta/alpha balance of demands (must be zero for a zero-packet helper at length a)
    for i,name in ((1,'alpha'),(2,'beta'),(3,'gamma')):
        s=sum(r_c*(2*0-t[i]) for (_,l,r_c,t) in C if l=='a')
        pr(f"  total {name}-coefficient demanded at length-a edges (ring case): {s}")
# scutoid identity: top theta, bottom pi-theta; Dehn term (l_top - l_bot) x theta
th=sp.Symbol('t'); lt,lb=sp.symbols('lt lb')
pr("scutoid side plane between parallel faces: top angle t, bottom pi-t, sum = pi exactly; Dehn term = (lt-lb) x t mod pi: "+str(sp.simplify(lt*th+lb*(sp.pi-th)-(lt-lb)*th-lb*sp.pi)==0))
# demands realisable by convex dihedrals (0<theta<pi)
for nm,t in (("C1 reflex 5pi/4-beta",V(F(5,4),0,-1,0)),("C2 reflex pi/2+alpha",V(F(1,2),1,0,0)),("C1 hex-hex pi/2+2beta (ring, >pi: needs >=2 edges)",V(F(1,2),0,2,0)),("C2 decagon pi/2+... 2pi-2alpha (needs >=2 edges)",V(2,-2,0,0))):
    pr(f"{nm}: {deg(t):.4f} deg, single convex edge possible: {0<deg(t)<180}; partner bottom edge pi-theta: {180-deg(t):.4f}")
json.dump(res,open('data/compounds.json','w'),indent=1)
pr("FINAL ok")
