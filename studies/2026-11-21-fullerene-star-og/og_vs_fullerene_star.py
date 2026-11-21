"""Exact (Q(sqrt5)) comparison: DICTO Ogdoecontahedron (OG, paper #31) vs Fullerene Star (C1 = truncated icosahedron + regular-dodecahedron
centre pyramid on each pentagon, all edges equal). Common frame: truncated icosahedron (TI) of edge 2, same 20 hexagon planes."""
from fractions import Fraction as Fr
import itertools, math, sys
class Q:
    __slots__=('a','b')
    def __init__(s,a=0,b=0): s.a=Fr(a); s.b=Fr(b)
    def _c(o): return o if isinstance(o,Q) else Q(o)
    def __add__(s,o): o=Q._c(o); return Q(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __sub__(s,o): o=Q._c(o); return Q(s.a-o.a,s.b-o.b)
    def __rsub__(s,o): return Q._c(o)-s
    def __neg__(s): return Q(-s.a,-s.b)
    def __mul__(s,o): o=Q._c(o); return Q(s.a*o.a+5*s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s): n=s.a*s.a-5*s.b*s.b; return Q(s.a/n,-s.b/n)
    def __truediv__(s,o): return s*Q._c(o).inv()
    def __eq__(s,o): o=Q._c(o); return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def f(s): return float(s.a)+float(s.b)*5**.5
    def sign(s):
        a,b=s.a,s.b
        if b==0: return (a>0)-(a<0)
        if a==0: return (b>0)-(b<0)
        if a>0 and b>0: return 1
        if a<0 and b<0: return -1
        # opposite signs: compare a^2 with 5b^2
        d=a*a-5*b*b
        return (1 if a>0 else -1) if d>0 else (-1 if a>0 else 1)
    def __repr__(s): return f"({s.a}+{s.b}r5)"
def qsqrt(x):
    """sqrt of x in Q(sqrt5) if it exists else None"""
    if x.sign()<0: return None
    n=x.a*x.a-5*x.b*x.b
    # norm must be a rational square
    from math import isqrt
    if n<0: return None
    nn,nd=n.numerator,n.denominator
    if isqrt(nn)**2!=nn or isqrt(nd)**2!=nd: return None
    r=Fr(isqrt(nn),isqrt(nd))
    for sg in (1,-1):
        for t in ((x.a+sg*r)/2,):
            # (u+v r5)^2=x : u^2+5v^2=a, 2uv=b ; u^2 = t'
            pass
    for sg in (1,-1):
        u2=(x.a+sg*r)/2
        if u2<0: continue
        num,den=u2.numerator,u2.denominator
        if isqrt(num)**2!=num or isqrt(den)**2!=den: continue
        u=Fr(isqrt(num),isqrt(den))
        if u==0:
            v2=x.a/5; 
            nn2,dd2=v2.numerator,v2.denominator
            if v2<0 or isqrt(nn2)**2!=nn2 or isqrt(dd2)**2!=dd2: continue
            c=Q(0,Fr(isqrt(nn2),isqrt(dd2)))
        else: c=Q(u,x.b/(2*u))
        if c*c==x: return c
    return None
R5=Q(0,1); PHI=Q(Fr(1,2),Fr(1,2)); ONE=Q(1)
def dot(u,v): return u[0]*v[0]+u[1]*v[1]+u[2]*v[2]
def sub(u,v): return tuple(x-y for x,y in zip(u,v))
def addv(u,v): return tuple(x+y for x,y in zip(u,v))
def smul(k,u): return tuple(k*x for x in u)
def cross(u,v): return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
def solve3(N,d):
    """N rows (3 normals), rhs d; Cramer. None if singular."""
    D=dot(N[0],cross(N[1],N[2]))
    if D==0: return None
    c12=cross(N[1],N[2]); c20=cross(N[2],N[0]); c01=cross(N[0],N[1])
    return tuple((d[0]*c12[i]+d[1]*c20[i]+d[2]*c01[i])/D for i in range(3))
def ang(u,v): return math.degrees(math.acos(dot(u,v).f()/math.sqrt(dot(u,u).f()*dot(v,v).f())))
out=[]; ok=True
def pr(s=""): print(s,flush=True); out.append(s)
def chk(name,c):
    global ok
    pr(f"  [{'ok' if c else 'FAIL'}] {name}"); ok=ok and bool(c)
# ---------- TI, edge 2 (even permutations of the standard coordinates)
p=PHI
base=[(0,1,3*p),(1,2+p,2*p),(p,2,2*p+1)]
def evenperm(v): return [(v[0],v[1],v[2]),(v[1],v[2],v[0]),(v[2],v[0],v[1])]
TI=set()
for b in base:
    for w in evenperm([Q._c(x) for x in b]):
        for sg in itertools.product((1,-1),repeat=3):
            TI.add(tuple(w[i]*sg[i] for i in range(3)))
TI=sorted(TI,key=lambda v:tuple(x.f() for x in v)); chk("TI has 60 vertices",len(TI)==60)
E2=[(i,j) for i in range(60) for j in range(i+1,60) if dot(sub(TI[i],TI[j]),sub(TI[i],TI[j]))==Q(4)]
chk("TI has 90 edges of length 2 (exact)",len(E2)==90)
ax5=[]; ax3=[]
for s in (1,-1):
    for t in (1,-1):
        for cyc in range(3):
            v=(Q(0),Q(s),Q(t)*p); ax5.append(tuple(v[(i-cyc)%3] for i in range(3)))
for sg in itertools.product((1,-1),repeat=3): ax3.append(tuple(Q(x) for x in sg))
for s in (1,-1):
    for t in (1,-1):
        for cyc in range(3):
            v=(Q(0),Q(s)*p,Q(t)*p.inv()); ax3.append(tuple(v[(i-cyc)%3] for i in range(3)))
chk("12 five-fold and 20 three-fold axes",len(ax5)==12 and len(ax3)==20)
def facev(n):
    d=max(dot(n,v).f() for v in TI); return [i for i,v in enumerate(TI) if abs(dot(n,v).f()-d)<1e-9], [dot(n,TI[i]) for i in range(60) if abs(dot(n,TI[i]).f()-d)<1e-9][0]
pent=[facev(n) for n in ax5]; hexs=[facev(n) for n in ax3]
chk("pentagons have 5 vertices, hexagons 6",all(len(x[0])==5 for x in pent) and all(len(x[0])==6 for x in hexs))
chk("all 12 pentagon planes at one offset (exact)",len({x[1] for x in pent})==1)
dH=hexs[0][1]
# hexagon planes: normal ax3[k] (unnormalised, |n|^2 = nn), offset dH_k = n.v
hexplanes=[(ax3[k],hexs[k][1]) for k in range(20)]
nn3=[dot(n,n) for n in ax3]; chk("3-fold axis vectors (+-1,+-1,+-1) and (0,phi,1/phi) have equal length^2 = 3",all(x==Q(3) for x in nn3))
# so hexagon planes n.x = dh with same |n|: equal distance
chk("hexagon plane offsets all equal",all(h[1]==dH for h in hexplanes))
dHn=dH  # n.x<=dH with |n|^2=3 -> distance dH/sqrt3
# ---------- OG: polar of TI in its midsphere (planes v.x<=rm2), cut at the hexagon planes
mid=(TI[E2[0][0]][0]+TI[E2[0][1]][0],)  # placeholder
m=addv(TI[E2[0][0]],TI[E2[0][1]]); rm2=dot(m,m)*Fr(1,4)
chk("TI midsphere: all 90 edge midpoints at one radius^2 (exact)",all(dot(addv(TI[i],TI[j]),addv(TI[i],TI[j]))*Fr(1,4)==rm2 for i,j in E2))
og_planes=[(TI[i],rm2) for i in range(60)]+hexplanes   # n.x <= d
def vertices(planes):
    P=len(planes); Nf=[[float(c.f()) for c in n] for n,d in planes]; Df=[d.f() for n,d in planes]
    import numpy as np
    A=np.array(Nf); B=np.array(Df); found={}
    for i,j,k in itertools.combinations(range(P),3):
        M=A[[i,j,k]]
        if abs(np.linalg.det(M))<1e-9: continue
        x=np.linalg.solve(M,B[[i,j,k]])
        if np.all(A@x<=B+1e-7):
            key=tuple(np.round(x,6))
            if key not in found: found[key]=(i,j,k)
    res=[]
    for key,(i,j,k) in found.items():
        x=solve3([planes[i][0],planes[j][0],planes[k][0]],[planes[i][1],planes[j][1],planes[k][1]])
        assert all((planes[t][1]-dot(planes[t][0],x)).sign()>=0 for t in range(P)),"corner outside (exact)"
        res.append(x)
    return res
OGv=vertices(og_planes)
def lattice(V,faces):
    """faces: list of vertex-index tuples (unordered). returns edges (pairs of vertices lying in exactly 2 common faces)."""
    inc={}
    for fi,f in enumerate(faces):
        for v in f: inc.setdefault(v,set()).add(fi)
    E=[(a,b) for a in range(len(V)) for b in range(a+1,len(V)) if len(inc[a]&inc[b])>=2]
    return E,inc
pr("== OG (pentakis dodecahedron = polar of TI in its midsphere, cut at TI's 20 hexagon planes)")
chk("OG has 102 corners (exact)",len(OGv)==102)
OGf=[]
for n,d in og_planes:
    f=tuple(i for i,x in enumerate(OGv) if dot(n,x)==d)
    if len(f)>=3: OGf.append(f)
chk("OG has 80 faces",len(OGf)==80)
sz=sorted(len(f) for f in OGf); chk("60 quadrilaterals (kites) + 20 hexagons",sz.count(4)==60 and sz.count(6)==20)
OGe,OGinc=lattice(OGv,OGf); chk("OG has 180 edges, Euler 102-180+80=2",len(OGe)==180 and 102-len(OGe)+80==2)
val=sorted(len(OGinc[v]) for v in range(len(OGv))); chk("valences 12 x5, 30 x4, 60 x3",(val.count(5),val.count(4),val.count(3))==(12,30,60))
kind=lambda f:'H' if len(f)==6 else 'K'
adj={}
for a,b in OGe:
    fs=sorted(OGinc[a]&OGinc[b]); k="-".join(sorted(kind(OGf[x]) for x in fs)); adj[k]=adj.get(k,0)+1
pr(f"  OG edge types (faces on each side): {adj}")
chk("OG: no hexagon-hexagon edge (hexagons meet only at the 30 four-valent corners)",adj.get('H-H',0)==0)
hexOG=[i for i,f in enumerate(OGf) if len(f)==6]
# hexagon regular? side^2 equal and kites
def d2(u,v): w=sub(u,v); return dot(w,w)
e2set={}
for a,b in OGe: e2set.setdefault(d2(OGv[a],OGv[b]),0); e2set[d2(OGv[a],OGv[b])]+=1
pr(f"  OG edge length^2 classes: {[(repr(k),v) for k,v in e2set.items()]}")
chk("OG: two edge lengths, 120 + 60",sorted(e2set.values())==[60,120])
rad=sorted(set(dot(v,v) for v in OGv),key=lambda q:q.f()); pr(f"  OG corner radius^2 classes: {[(repr(r),sum(1 for v in OGv if dot(v,v)==r)) for r in rad]}")
chk("OG: 90 corners on one sphere, 12 on another",sorted(sum(1 for v in OGv if dot(v,v)==r) for r in rad)==[12,90])
# ---------- pentakis parameters in the common frame
a5=ax5[0]; a5sq=dot(a5,a5)
def apex_of_plane_family(planes_through_axis):
    pass
# OG: apex = 12 five-fold corners (radius class with 12); B radius: kite plane meets 3-fold axis
OGapex=[v for v in OGv if sum(1 for f in OGf if True and False)==0 and len(OGinc[OGv.index(v)])==5]
Aog=OGapex[0]
# FS: pyramid apex over a TI pentagon
pi,pd=pent[0]; cen=smul(Q(Fr(1,5)),tuple(sum((TI[i][c] for i in pi),Q(0)) for c in range(3)))
chk("pentagon centroid is parallel to the 5-fold axis",cross(cen,ax5[0])==(Q(0),Q(0),Q(0)))
rp2=dot(cen,cen)
ri2=(Q(25)+11*R5)/10    # dodecahedron edge 2: inradius^2 = a^2 (25+11 sqrt5)/40
Rc2=3*PHI*PHI          # circumradius^2 = 3 phi^2 (a=2: (a sqrt3 phi/2)^2)
pc2=(Q(5)+R5)*Fr(2,5)  # pentagon circumradius^2, a=2: 4(5+sqrt5)/10
chk("regular dodecahedron(edge 2): inradius^2 + pentagon circumradius^2 = circumradius^2 (exact)",ri2+pc2==Rc2)
# pentagon of TI really has circumradius^2 pc2
chk("TI pentagon circumradius^2 = 2(5+sqrt5)/5 (exact)",all(d2(TI[i],cen)==pc2 for i in pi))
ratio2=ri2/rp2; r=qsqrt(ratio2); pr(f"  ri^2/|centre|^2 = {ratio2!r}; sqrt in Q(sqrt5): {r!r}")
chk("apex height ratio ri/|centre| lies in Q(sqrt5)",r is not None)
Afs=addv(cen,smul(r,cen))
chk("FS: apex to each pentagon vertex = R (circumradius) and = pyramid side edge; (R^2 exact)",all(d2(Afs,TI[i])==Rc2 for i in pi))
# FS faces
FSv=list(TI)+[None]*12
Aps=[]
for k in range(12):
    pi_,_=pent[k]; c=smul(Q(Fr(1,5)),tuple(sum((TI[i][t] for i in pi_),Q(0)) for t in range(3)))
    Aps.append(addv(c,smul(r,c)))
FSv=list(TI)+Aps
FSf=[]
for k in range(12):
    pi_,_=pent[k]
    for i,j in E2:
        if i in pi_ and j in pi_: FSf.append((i,j,60+k))
for k in range(20): FSf.append(tuple(hexs[k][0]))
FSe,FSinc=lattice(FSv,FSf)
pr("== Fullerene Star (TI + regular-dodecahedron centre pyramid on each pentagon, same TI, same hexagon planes)")
chk("FS: 72 corners, 80 faces (60 triangles + 20 hexagons)",len(FSv)==72 and len(FSf)==80 and sorted(len(f) for f in FSf).count(3)==60)
chk("FS: 150 edges, Euler 72-150+80=2",len(FSe)==150 and 72-len(FSe)+80==2)
e2f={}
for a,b in FSe: e2f[d2(FSv[a],FSv[b])]=e2f.get(d2(FSv[a],FSv[b]),0)+1
pr(f"  FS edge length^2 classes: {[(repr(k),v) for k,v in e2f.items()]}")
adj2={}
for a,b in FSe:
    fs=sorted(FSinc[a]&FSinc[b]); k="-".join(sorted('H' if len(FSf[x])==6 else 'T' for x in fs)); adj2[k]=adj2.get(k,0)+1
pr(f"  FS edge types: {adj2}")
val2=sorted(len(FSinc[v]) for v in range(72)); pr(f"  FS valences: 5-valent {val2.count(5)}, 4-valent {val2.count(4)}, 3-valent {val2.count(3)}")
# ---------- comparison of the face lattices
pr("== Comparison")
same=(len(OGv),len(OGe),len(OGf))==(len(FSv),len(FSe),len(FSf))
pr(f"  OG (V,E,F)=({len(OGv)},{len(OGe)},{len(OGf)}) ; FS (V,E,F)=({len(FSv)},{len(FSe)},{len(FSf)}) ; same combinatorial type: {same}")
chk("FS is NOT combinatorially the OG (72 vs 102 corners; triangles vs kites; hexagons share edges in FS, only corners in OG)",not same)
# ---------- one-parameter family G(H): fixed TI vertices (hexagon frame), pyramids of apex height H
# triangle plane through p,q and apex at height t*|cen| above the centre; base angle theta_b between pentagon plane and triangle
pe=[(i,j) for i,j in E2 if i in pent[0][0] and j in pent[0][0]][0]; P_,Q_=TI[pe[0]],TI[pe[1]]
mid=smul(Q(Fr(1,2)),addv(P_,Q_)); inr2=d2(cen,mid)  # pentagon inradius^2 (apothem)
chk("pentagon apothem^2 = (a/2)^2 tan^2(54deg) = (5+2sqrt5)/... (float check)",abs(math.sqrt(inr2.f())-math.tan(math.radians(54)))<1e-12)
apothem=math.sqrt(inr2.f()); Hfs=math.sqrt(ri2.f())
pr(f"  pentagon apothem {apothem:.6f}; FS pyramid height (dodecahedron inradius) {Hfs:.6f}")
# interior dihedral at hexagon-triangle edge = (pentagon-hexagon dihedral of TI) + base angle of pyramid
def dih_TI_ph():
    nh=ax3[0]
    for k in range(20):
        if set(pent[0][0])&set(hexs[k][0])>={pe[0],pe[1]}: nh=ax3[k]; break
    return 180-ang(ax5[0],nh)
phdih=dih_TI_ph()
def base_angle(H): return math.degrees(math.atan(H/apothem))
pr(f"  TI pentagon-hexagon dihedral {phdih:.4f}")
Hc=apothem*math.tan(math.radians(180-phdih))
fs_dih=phdih+base_angle(Hfs)
pr(f"  FS hexagon-triangle interior dihedral = {phdih:.4f} + {base_angle(Hfs):.4f} = {fs_dih:.4f}  (reflex if > 180)")
pr(f"  Family G(H): TI + pyramid of apex height H over each pentagon; hexagon-triangle dihedral {phdih:.4f}+atan(H/{apothem:.4f}); convex iff H <= H_c = {Hc:.6f} (triangle coplanar with its hexagon); FS has H = {Hfs:.6f} = {Hfs/Hc:.4f} H_c")
chk("FS lies outside the convex range of G (H_fs > H_c)",Hfs>Hc)
# H_c exact: triangle in the hexagon plane => apex = intersection of hexagon plane with the 5-fold axis
nh=None
for k in range(20):
    if set(pent[0][0])&set(hexs[k][0])>={pe[0],pe[1]}: nh=k;break
n=ax3[nh]; d=hexs[nh][1]
t=d/dot(n,cen); Ac=smul(t,cen); 
chk("H_c exact: hexagon plane meets the 5-fold axis at t*centre, t in Q(sqrt5)",dot(n,Ac)==d)
Hc_exact=(t-1); pr(f"  apex at H_c is {t!r} x pentagon centre, i.e. height {(Hc_exact.f()*math.sqrt(rp2.f())):.6f}")
chk("float H_c equals exact H_c",abs(Hc_exact.f()*math.sqrt(rp2.f())-Hc)<1e-9)
# ---------- pentakis parameters of both, in TI frame (hex planes n.x=d, |n|^2=3)
def pentakis_params(plane_n,plane_d):
    """apex = plane meets 5-fold axis; B = plane meets 3-fold axis through a vertex of the hexagon"""
    ax=ax5[0]; t=plane_d/dot(plane_n,ax); A=smul(t,ax)
    return A
# OG kite plane at apex 5-fold: planes v.x=rm2 with v a TI vertex of pentagon 0
vv=TI[pent[0][0][0]]; tOG=rm2/dot(vv,ax5[0]); A_OG=smul(tOG,ax5[0])
chk("OG apex = plane v.x=rm2 meets the 5-fold axis, and is one of the 12 five-valent OG corners (exact)",any(A_OG==x for x in OGv))
pr(f"  OG apex radius^2 = {dot(A_OG,A_OG)!r} ({math.sqrt(dot(A_OG,A_OG).f()):.6f}); in OG corner classes: {dot(A_OG,A_OG) in [dot(v,v) for v in OGv]}")
pr(f"  FS apex radius^2 = {dot(Afs,Afs)!r} ({math.sqrt(dot(Afs,Afs).f()):.6f})")
dfs=math.sqrt(dHn.f()/math.sqrt(3)) if False else dHn.f()/math.sqrt(3)
pr(f"  hexagon plane distance from centre (common): {dfs:.6f}")
# B radius: the kite/triangle plane through its normal meets the 3-fold axis
def planeThroughAxis(Npl,dpl,axis):
    t=dpl/dot(Npl,axis); return smul(t,axis)
# OG plane facing the hexagon-adjacent triangle: plane v.x=rm2 for v adjacent; B via ax3 direction
# pick the TI vertex v of hexagon 0 (on both a hex and a pentagon): its plane meets the hexagon axis
hex0=hexs[0][0]; v0=TI[hex0[0]]; B_OG=planeThroughAxis(v0,rm2,ax3[0])
pr(f"  OG pentakis vertex B on the 3-fold axis of hexagon 0 at radius {math.sqrt(dot(B_OG,B_OG).f()):.6f}; hexagon plane at {dfs:.6f} (cut depth {math.sqrt(dot(B_OG,B_OG).f())-dfs:.6f})")
# FS: triangle planes through the three points A, P, Q for a triangle adjacent to hexagon 0
for (i,j,ap) in FSf[:60]:
    if i in hex0 and j in hex0:
        Nt=cross(sub(TI[i],Afs if False else Aps[ap-60]),sub(TI[j],Aps[ap-60])); dt=dot(Nt,TI[i])
        if dt.sign()<0: Nt=smul(Q(-1),Nt); dt=-dt
        B_FS=planeThroughAxis(Nt,dt,ax3[0]); break
pr(f"  FS triangle plane meets the 3-fold axis of its hexagon at radius {math.sqrt(dot(B_FS,B_FS).f()):.6f} (hexagon plane {dfs:.6f}, {'beyond' if math.sqrt(dot(B_FS,B_FS).f())>dfs else 'below'} it)")
pr(f"  OG: apex/hexplane = {math.sqrt(dot(A_OG,A_OG).f())/dfs:.6f}; B/hexplane = {math.sqrt(dot(B_OG,B_OG).f())/dfs:.6f}")
pr(f"  FS: apex/hexplane = {math.sqrt(dot(Afs,Afs).f())/dfs:.6f}; B/hexplane = {math.sqrt(dot(B_FS,B_FS).f())/dfs:.6f}")
# ---------- dihedral at hexagon-face edges (interior), both
def interior_dihedral(solid_V,solid_f,fa,fb,edge):
    """interior dihedral between faces fa,fb along edge; centre-origin-based outward normals; non-convex handled via normal orientation and edge convexity test"""
    def outn(f):
        pts=[solid_V[i] for i in f[:3]]; N=cross(sub(pts[1],pts[0]),sub(pts[2],pts[0]))
        if dot(N,pts[0]).sign()<0: N=smul(Q(-1),N)
        return N,dot(N,pts[0])
    Na,da=outn(fa); Nb,db=outn(fb)
    return Na,Nb
# OG: hex-kite dihedral
e=None
for a,b in OGe:
    fs=sorted(OGinc[a]&OGinc[b])
    if len(fs)==2 and sorted(len(OGf[x]) for x in fs)==[4,6]: e=(a,b,fs); break
a,b,fs=e; hf=[x for x in fs if len(OGf[x])==6][0]; kf=[x for x in fs if len(OGf[x])==4][0]
def normal_out(V,f):
    pts=[V[i] for i in f[:3]]
    # take three non-collinear
    for t in itertools.combinations(f,3):
        N=cross(sub(V[t[1]],V[t[0]]),sub(V[t[2]],V[t[0]]))
        if N!=(Q(0),Q(0),Q(0)): break
    if dot(N,V[t[0]]).sign()<0: N=smul(Q(-1),N)
    return N
Nh=normal_out(OGv,OGf[hf]); Nk=normal_out(OGv,OGf[kf])
cosOG=dot(Nh,Nk); dihOG=180-ang(Nh,Nk)
pr(f"  OG hexagon-kite interior dihedral (convex solid) = {dihOG:.6f} deg; cos(theta_ext)^2 = {(dot(Nh,Nk)*dot(Nh,Nk)/(dot(Nh,Nh)*dot(Nk,Nk)))!r}")
# FS hexagon-triangle
for a,b in FSe:
    fs=sorted(FSinc[a]&FSinc[b])
    if sorted(len(FSf[x]) for x in fs)==[3,6]: break
hf=[x for x in fs if len(FSf[x])==6][0]; tf=[x for x in fs if len(FSf[x])==3][0]
Nh=normal_out(FSv,FSf[hf]); Nt=normal_out(FSv,FSf[tf])
ext=ang(Nh,Nt)   # angle between outward normals (hexagon outward, triangle outward)
# signed: edge is convex if the triangle's third vertex lies below the hexagon plane (inside)
third=[v for v in FSf[tf] if v not in (a,b)][0]
convex=(dot(Nh,FSv[third])-dot(Nh,FSv[a])).sign()<0
dihFS=180-ext if convex else 180+ext
pr(f"  FS hexagon-triangle interior dihedral = {dihFS:.6f} deg ({'convex' if convex else 'reflex'}); outward-normal angle {ext:.6f}; cos^2 = {(dot(Nh,Nt)*dot(Nh,Nt)/(dot(Nh,Nh)*dot(Nt,Nt)))!r}")
chk("FS dihedral equals TI pent-hex dihedral + atan(H/apothem) (float, 1e-9)",abs(dihFS-fs_dih)<1e-9)
chk("OG dihedral convex (<180), FS reflex (>180)",dihOG<180 and dihFS>180)
# ---------- OG family: is FS inside G? Which cut family reaches FS-type?
pr("== Link")
pr("  Both solids are made from the same 20 hexagon planes of the TI frame. The OG is a pentakis dodecahedron whose 20 six-fold corners are cut at those planes so that neighbouring hexagons touch only at the 30 edge-midpoint corners (kites).")
pr("  The Fullerene Star's 60 triangle planes also form a pentakis dodecahedron, but its six-fold corners lie BELOW the hexagon planes (B/hexplane < 1), so no cut occurs: the FS is TI + 12 pyramids (union), reflex at all 60 hexagon-triangle edges; the OG has B/hexplane > 1 (cut).")
chk("OG pentakis six-fold corners above the hexagon planes (cut), FS below",math.sqrt(dot(B_OG,B_OG).f())>dfs>math.sqrt(dot(B_FS,B_FS).f()))
chk("FS corner count 72 differs from every corner count in the OG family of #39 (OG 102; up 92,180,212,270; down 80,132,140,162)",72 not in (102,92,180,212,270,80,132,140,162))
pr("FINAL ok" if ok else "FINAL FAIL")
open('og_vs_fullerene_star.log','w').write("\n".join(out)+"\n")
