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
POSE={'D':G,'I':G,'C':G@rot((0,0,1),0.35),'T':rot((0,0,1),0.5)@rot((1,-1,0),0.62),'O':G@rot((0,0,1),0.3)}
GROUND=(20,15,11); GOLD=(214,168,74); PURPLE=(150,118,200)
TONE={'D':GOLD,'I':PURPLE,'C':(232,200,120),'T':(190,160,230),'O':(176,128,58)}
N=1800; SS=2; W=N*SS
view=rot((1,0,0),-0.62)          # tilt the board towards the viewer
light=np.array([-0.4,0.55,0.75]); light/=np.linalg.norm(light)
img=Image.new('RGB',(W,W),GROUND); d=ImageDraw.Draw(img)
# fit the board and its letters to the canvas
B=np.array([[x,y,z] for x in (-2.95,2.6) for y in (-2.6,2.95) for z in (-0.44,0.44)])@view.T
sc=0.9*W/max(np.ptp(B[:,0]),np.ptp(B[:,1])); ox=W/2-sc*(B[:,0].max()+B[:,0].min())/2; oy=W/2+sc*(B[:,1].max()+B[:,1].min())/2
items=[]
for i in range(5):
    for j in range(5):
        k=M[i][j]; V,F=SOL[k]; R=POSE[k]
        pos=np.array([j-2,2-i,0.0])
        Vw=(V@R.T)*0.44+pos; Vv=Vw@view.T
        items.append((Vv[:,2].mean(),k,Vv,[(n@R.T@view.T,idx) for n,idx in F]))
for _,k,Vv,F in sorted(items,key=lambda t:t[0]):
    for n,idx in sorted(F,key=lambda f:Vv[f[1]][:,2].mean()):
        if n[2]<=1e-9: continue
        b=0.45+0.55*max(0,n@light)
        col=tuple(int(c*b+GROUND[m]*(1-b)*0.2) for m,c in enumerate(TONE[k]))
        pts=[(ox+Vv[q,0]*sc, oy-Vv[q,1]*sc) for q in idx]
        d.polygon(pts,fill=col); d.line(pts+[pts[0]],fill=(250,232,190),width=2*SS)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',int(0.034*W))
for j in range(5):   # letters along the top and down the left, in board perspective
    p=np.array([j-2,2.78,0])@view.T; d.text((ox+p[0]*sc, oy-p[1]*sc),WORD[j],font=f,fill=GOLD,anchor='mm')
    p=np.array([-2.78,2-j,0])@view.T; d.text((ox+p[0]*sc, oy-p[1]*sc),WORD[j],font=f,fill=GOLD,anchor='mm')
img=img.resize((N,N),Image.LANCZOS); img.save('dicto-square.png'); print('ok')
