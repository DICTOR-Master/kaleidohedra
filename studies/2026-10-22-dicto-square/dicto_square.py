# The DICTO square (DICTO's idea, 2026-10-22): a 5x5 word square like SATOR AREPO, built from the five Platonic
# solids of DICTO's emblem key, D-I-C-T-O = Dodecahedron, Icosahedron, Cube, Tetrahedron, Octahedron.
# Cyclic Latin square: row i, column j holds letter (i+j) mod 5, so DICTO reads across the top and down the left,
# every solid appears once in each row and column, and each solid runs in one diagonal stripe.
# Solids sit on a square lattice (spacing 1), each scaled to the same circumsphere (radius 0.44).
import itertools, math, numpy as np
from scipy.spatial import ConvexHull
from PIL import Image, ImageDraw, ImageFont
phi=(1+5**.5)/2
def cyc(v): return [v,(v[1],v[2],v[0]),(v[2],v[0],v[1])]
S={}
S['T']=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
S['C']=list(itertools.product((-1,1),repeat=3))
S['O']=[tuple(s*(i==k) for k in range(3)) for i in range(3) for s in (1,-1)]
S['I']=[p for a in (1,-1) for b in (phi,-phi) for p in cyc((0,a,b))]
S['D']=list(itertools.product((-1,1),repeat=3))+[p for a in (1/phi,-1/phi) for b in (phi,-phi) for p in cyc((0,a,b))]
assert [len(S[k]) for k in 'DICTO']==[20,12,8,4,6]
def faces(V):
    V=np.array(V,float); V=V/np.linalg.norm(V,axis=1).max()
    h=ConvexHull(V); F={}
    for s,eq in zip(h.simplices,h.equations):
        F.setdefault(tuple(np.round(eq,6)),set()).update(s)
    out=[]
    for eq,idx in F.items():
        n=np.array(eq[:3]); idx=list(idx); c=V[idx].mean(0)
        u=V[idx[0]]-c; u/=np.linalg.norm(u); w=np.cross(n,u)
        idx.sort(key=lambda i: math.atan2((V[i]-c)@w,(V[i]-c)@u)); out.append((n,idx))
    return V,out
SOL={k:faces(v) for k,v in S.items()}
assert [len(SOL[k][1]) for k in 'DICTO']==[12,20,6,4,8]
WORD='DICTO'; M=[[WORD[(i+j)%5] for j in range(5)] for i in range(5)]
assert M[0]==list(WORD) and [r[0] for r in M]==list(WORD)
assert all(len(set(r))==5 for r in M) and all(len({M[i][j] for i in range(5)})==5 for j in range(5))
# turn each solid to a pleasing pose (same for all copies of a solid)
def rot(ax,a):
    ax=np.array(ax,float); ax/=np.linalg.norm(ax); K=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+math.sin(a)*K+(1-math.cos(a))*K@K
G=rot((1,0.55,0.15),0.85)   # one general pose shows three or more faces of every solid
def align(u,v):   # rotation taking direction u to direction v
    u=np.array(u,float)/np.linalg.norm(u); v=np.array(v,float)/np.linalg.norm(v); ax=np.cross(u,v)
    return rot(ax,math.acos(np.clip(u@v,-1,1)))
POSE={'D':G,'I':G,'C':rot((1,0,0),-0.5)@rot((0,1,0),0.62),
      'T':align((1,1,1),(-0.18,0.32,0.93))@rot((1,1,1),0.0),     # a corner towards the viewer: three faces show
      'O':align((1,1,1),(0.3,0.38,0.875))@rot((1,1,1),0.2)}    # nearly face-on: a hexagonal outline
GROUND=(20,15,11); GOLD=(214,168,74)
# Plato's elements (Timaeus): fire tetrahedron, air octahedron, water icosahedron, earth cube; the dodecahedron for the whole (aether)
TONE={'T':(205,62,40),'O':(232,200,82),'I':(58,112,205),'C':(72,142,72),'D':(138,92,196)}
N=1800; SS=2; W=N*SS
view=np.eye(3)                   # straight-on view: true grid squares
light=np.array([-0.4,0.55,0.75]); light/=np.linalg.norm(light)
img=Image.new('RGB',(W,W),GROUND); d=ImageDraw.Draw(img)
# fit the board and its letters to the canvas
B=np.array([[x,y,z] for x in (-2.5,2.5) for y in (-2.5,2.5) for z in (-0.5,0.5)])@view.T
sc=0.9*W/max(np.ptp(B[:,0]),np.ptp(B[:,1])); ox=W/2-sc*(B[:,0].max()+B[:,0].min())/2; oy=W/2+sc*(B[:,1].max()+B[:,1].min())/2
P=lambda x,y,z: (lambda v:(ox+v[0]*sc, oy-v[1]*sc))(np.array([x,y,z])@view.T)
for t in range(6):
    d.line([P(t-2.5,-2.5,-0.5),P(t-2.5,2.5,-0.5)],fill=GOLD,width=3*SS); d.line([P(-2.5,t-2.5,-0.5),P(2.5,t-2.5,-0.5)],fill=GOLD,width=3*SS)
items=[]
for i in range(5):
    for j in range(5):
        k=M[i][j]; V,F=SOL[k]; R=POSE[k]
        pos=np.array([j-2,2-i,0.0])
        Vw=(V@R.T)*0.44+pos; Vv=Vw@view.T
        items.append((Vv[:,2].mean(),k,Vv,[(n@R.T@view.T,idx) for n,idx in F]))
CEN={}
for _,k,Vv,F in sorted(items,key=lambda t:t[0]):
    vis=[Vv[idx][:,:2].mean(0) for n,idx in F if n[2]>1e-9]; CEN[tuple(np.round(Vv.mean(0)[:2],3))]=np.mean(vis,0)   # letter on the visible body
    for n,idx in sorted(F,key=lambda f:Vv[f[1]][:,2].mean()):
        if n[2]<=1e-9: continue
        b=0.45+0.55*max(0,n@light)
        col=tuple(int(c*b+GROUND[m]*(1-b)*0.2) for m,c in enumerate(TONE[k]))
        pts=[(ox+Vv[q,0]*sc, oy-Vv[q,1]*sc) for q in idx]
        d.polygon(pts,fill=col); d.line(pts+[pts[0]],fill=(250,232,190),width=2*SS)
# Roman (Trajan-style) initials V-cut into each form, the groove gilded with platinum leaf:
# the groove depth is the distance to the letter's edge, so the two walls meet in a ridge-free V along the stroke's middle;
# light from the upper left lights one wall and leaves the other in shadow.
from scipy import ndimage
f=ImageFont.truetype('Cinzel.ttf',int(0.075*W)); f.set_variation_by_name('Bold')
Lc=np.array([-0.55,0.6,0.58]); Lc/=np.linalg.norm(Lc)
def carved(ch):
    box=int(0.12*W); m=Image.new('L',(box,box),0); ImageDraw.Draw(m).text((box/2,box/2),ch,font=f,fill=255,anchor='mm')
    M=np.array(m)/255.0; ins=M>0.5
    dist=ndimage.distance_transform_edt(ins); dist=ndimage.gaussian_filter(dist,0.8)
    gy,gx=np.gradient(dist); k=1.6                          # wall slope of the V
    n=np.dstack([gx*k, -gy*k, np.ones_like(dist)])   # depth = -dist: a groove; n/=np.linalg.norm(n,axis=2,keepdims=True)
    lam=np.clip(n@Lc,0,1)
    h=n@(Lc+np.array([0,0,1.0])); h=np.clip(h/np.linalg.norm(Lc+[0,0,1.0]),0,1)**40
    dark=np.array([70,74,82.]); lite=np.array([226,229,235.]); spec=np.array([255,255,255.])
    rgb=dark+(lite-dark)*lam[...,None]**1.3; rgb=rgb+(spec-rgb)*h[...,None]*0.8
    # a thin cast shadow just inside the lit-side edge (the block's lip shades the groove)
    sh=ndimage.shift(ins.astype(float),(-2*SS*0.6,2*SS*0.6),order=1)
    rgb*= (1-0.35*np.clip(ins-sh,0,1))[...,None]
    tile=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)); mask=Image.fromarray((ndimage.gaussian_filter(M,0.6)*255).astype(np.uint8))
    return tile,mask,box
CARVE={ch:carved(ch) for ch in 'DICTO'}
for i in range(5):
    for j in range(5):
        p=CEN[tuple(np.round(np.array([j-2,2-i,0.0])[:2],3))]; tile,mask,box=CARVE[M[i][j]]
        img.paste(tile,(int(ox+p[0]*sc-box/2),int(oy-p[1]*sc-box/2)),mask)
img=img.resize((N,N),Image.LANCZOS); img.save('dicto-square.png'); print('ok')
