# Figure: the stack for the mix of all five solids, slabs drawn apart. Shown: the solids and the convex connectors
# P; the large octet's face pyramids Q' and the non-convex connectors (Dogstars S, boundary pieces X and Y, Admiral Caps A) are left out so the solids
# show. Element colours: dodecahedron violet, icosahedron blue, cube green, tetrahedron red, octahedron yellow.
import math, numpy as np, itertools
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull
import mixes3 as M
from mixes2 import octet_pieces, RZ
phi=M.phi; s=M.s; L=M.L
pieces=[]   # (kind, vertices)
GAP=0.9; z=0.0
for c in M.D_world(0)[1]:
    if abs(c[0])<2 and abs(c[1])<2: pieces.append(('D',M.DOD+c))
z=3*phi+GAP
for i,j in itertools.product(range(-2,2),range(-2,2)):
    pieces.append(('C',np.array(list(itertools.product((0,1),repeat=3)),float)+np.array([i,j,z])))
z+=1+GAP
for sg,n,o,k in M.TO_world(z,{'T','O'}):
    pass
# rebuild T/O slab pieces with vertices (TO_world stores planes only)
K=2
for x,y,zz in itertools.product(range(-3,4),range(-3,4),range(0,K+1)):
    c=np.array([x,y,zz])*s+np.array([0,0,z])
    if (x+y+zz)%2:
        V=[c+d*s for d in np.vstack([np.eye(3),-np.eye(3)])]; eq=[v for v in V if abs(v[2]-c[2])<1e-9]
        if zz==0: pieces.append(('P',np.array(eq+[c+np.array([0,0,s])])))
        elif zz==K: pieces.append(('P',np.array(eq+[c-np.array([0,0,s])])))
        else: pieces.append(('O',np.array(V)))
    if zz<K:
        cs=[np.array([x+i,y+j,zz+k]) for i in (0,1) for j in (0,1) for k in (0,1)]
        pieces.append(('T',np.array([q*s+np.array([0,0,z]) for q in cs if q.sum()%2==0])))
z+=2*s+GAP
ICO=np.array([p for a in (1,-1) for b in (phi,-phi) for p in [(0,a,b),(a,b,0),(b,0,a)]])/2
for k,V,c in octet_pieces(L,3):
    V=np.array(V)@RZ.T+np.array([0,0,z]); m=V[:,2].mean()
    if not (z<m<z+L*(2/3)**.5): continue
    if k=='O': pieces.append(('I',ICO@RZ.T+V.mean(0)))

BOX=2.0
pieces=[(k,V) for k,V in pieces if abs(V.mean(0)[0])<BOX and abs(V.mean(0)[1])<BOX]
def rot(ax,a):
    ax=np.array(ax,float); ax/=np.linalg.norm(ax); Kx=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+math.sin(a)*Kx+(1-math.cos(a))*Kx@Kx
Rv=rot((1,0,0),-1.2)@rot((0,0,1),0.45)
COL={'D':(138,92,196),'I':(58,112,205),'C':(72,142,72),'T':(205,62,40),'O':(232,200,82),'P':(240,222,160),"Q'":(150,170,215)}
GROUND=(20,15,11); GOLD=(222,178,80); light=np.array([-0.4,0.5,0.77]); light/=np.linalg.norm(light)
allv=np.vstack([V@Rv.T for _,V in pieces]); N=1500; SS=2
Wd=N*SS; Ht=int(Wd*np.ptp(allv[:,1])/np.ptp(allv[:,0])*1.04)
img=Image.new('RGB',(Wd,Ht),GROUND); d=ImageDraw.Draw(img); sc=0.96*Wd/np.ptp(allv[:,0])
cx=(allv[:,0].max()+allv[:,0].min())/2; cy=(allv[:,1].max()+allv[:,1].min())/2
Pt=lambda p:(Wd/2+(p[0]-cx)*sc, Ht/2-(p[1]-cy)*sc)
items=[]
for k,V in pieces:
    Vv=V@Rv.T; h=ConvexHull(Vv); F={}
    for simp,eq in zip(h.simplices,h.equations): F.setdefault(tuple(np.round(eq,6)),set()).update(simp)
    items.append((Vv[:,2].mean(),k,Vv,F))
for _,k,Vv,F in sorted(items,key=lambda t:t[0]):
    for eq,idx in F.items():
        n=np.array(eq[:3])
        if n[2]<=1e-9: continue
        idx=list(idx); c=Vv[idx].mean(0); u=Vv[idx[0]]-c; w=np.cross(n,u)
        idx.sort(key=lambda i: math.atan2((Vv[i]-c)@w,(Vv[i]-c)@u))
        b=0.35+0.65*max(0,n@light); col=tuple(int(x*b) for x in COL[k])
        pts=[Pt(Vv[i]) for i in idx]; d.polygon(pts,fill=col); d.line(pts+[pts[0]],fill=GOLD,width=2*SS)
img.resize((N,int(Ht/SS)),Image.LANCZOS).save('stack-dicto.png'); print('ok',len(pieces))
