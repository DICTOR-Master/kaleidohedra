# Figure: the seam of mix C + T + O. Cubes (green, earth) below z = 0; above, the octet's tetrahedra (red, fire),
# octahedra (yellow, air) and the half octahedra P (pale gold) on the seam. The octet is lifted a little to show
# the seam's squares. Element colours as in the DICTO square; gold edges; dark ground.
import math, numpy as np, itertools
from PIL import Image, ImageDraw
from mixes import build, planes
from scipy.spatial import ConvexHull
pcs=build({'C','T','O'},R=3)
LIFT=0.22; BOX=1.45
sel=[]
for k,V in pcs:
    V=np.array(V,float); c=V.mean(0)
    if abs(c[0])>BOX or abs(c[1])>BOX or c[2]<-1.05 or c[2]>1.1: continue
    if k=='C' and c[2]<-1.05: continue
    if c[2]>0: V=V+np.array([0,0,LIFT])
    sel.append((k,V))
def rot(ax,a):
    ax=np.array(ax,float); ax/=np.linalg.norm(ax); K=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+math.sin(a)*K+(1-math.cos(a))*K@K
Rv=rot((1,0,0),-1.05)@rot((0,0,1),0.5)          # look down at the seam from the side and above
COL={'C':(72,142,72),'T':(205,62,40),'O':(232,200,82),'P':(240,222,160)}
GROUND=(20,15,11); GOLD=(222,178,80)
light=np.array([-0.4,0.5,0.77]); light/=np.linalg.norm(light)
N=1600; SS=2; W=N*SS; img=Image.new('RGB',(W,int(W*0.82)),GROUND); d=ImageDraw.Draw(img)
allv=np.vstack([V@Rv.T for _,V in sel]); sc=0.92*W/np.ptp(allv[:,0]); cx=(allv[:,0].max()+allv[:,0].min())/2; cy=(allv[:,1].max()+allv[:,1].min())/2
P=lambda p:(W/2+(p[0]-cx)*sc, img.height/2-(p[1]-cy)*sc)
items=[]
for k,V in sel:
    Vv=V@Rv.T; h=ConvexHull(Vv); faces={}
    for simp,eq in zip(h.simplices,h.equations): faces.setdefault(tuple(np.round(eq,6)),set()).update(simp)
    items.append((Vv[:,2].mean(),k,Vv,faces))
for _,k,Vv,faces in sorted(items,key=lambda t:t[0]):
    for eq,idx in faces.items():
        n=np.array(eq[:3])
        if n[2]<=1e-9: continue
        idx=list(idx); c=Vv[idx].mean(0); u=Vv[idx[0]]-c; w=np.cross(n,u)
        idx.sort(key=lambda i: math.atan2((Vv[i]-c)@w,(Vv[i]-c)@u))
        b=0.35+0.65*max(0,n@light); col=tuple(int(x*b) for x in COL[k])
        pts=[P(Vv[i]) for i in idx]; d.polygon(pts,fill=col); d.line(pts+[pts[0]],fill=GOLD,width=2*SS)
img.resize((N,int(N*0.82)),Image.LANCZOS).save('seam-cto.png'); print('ok',len(sel))
