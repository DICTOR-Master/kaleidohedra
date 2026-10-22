# The space BETWEEN the two dodecahedra (DICTO): the convex hull of the pair minus the two dodecahedra.
# Volume by sampling; drawn as glass by ray marching (opacity from the length of each sight line inside the void),
# over the two dodecahedra.
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
import mixes3 as M, pieces_figure as PF
phi=M.phi
D1=M.DOD.copy(); D2=M.DOD+np.array([phi,phi,0])
def H(V): h=ConvexHull(V); return h.equations[:,:3],h.equations[:,3]
HU=H(np.vstack([D1,D2])); H1=H(D1); H2=H(D2)
inside=lambda X,P: np.all(X@P[0].T+P[1]<-1e-9,axis=1)
void=lambda X: inside(X,HU)&~inside(X,H1)&~inside(X,H2)
rs=np.random.default_rng(0); lo=np.vstack([D1,D2]).min(0); hi=np.vstack([D1,D2]).max(0)
X=rs.uniform(lo,hi,(600000,3)); f=void(X).mean(); vol=f*np.prod(hi-lo)
print('void volume', round(vol,4), ' hull', round(ConvexHull(np.vstack([D1,D2])).volume,4), ' dodecahedron', round(ConvexHull(D1).volume,4))
# connected pieces of the void on a grid
from scipy import ndimage
n=90; g=[np.linspace(lo[i],hi[i],n) for i in range(3)]; G=np.stack(np.meshgrid(*g,indexing='ij'),-1).reshape(-1,3)
lab,k=ndimage.label(void(G).reshape(n,n,n)); sizes=np.bincount(lab.ravel())[1:]; print('void pieces', k, 'sizes', sorted(sizes,reverse=True)[:6])
def view(Rv,px=560,steps=220):
    PF.Rv=Rv; c=np.vstack([D1,D2]).mean(0); scale=px*0.17
    T=PF.orient(PF.tri(PF.hull_faces(D1)))+PF.orient(PF.tri(PF.hull_faces(D2)))
    base=np.array(PF.render([t-c for t in T],(138,92,196),px,scale)).astype(float)
    # rays along -z of the view frame
    ys,xs=np.mgrid[0:px,0:px]; u=(xs+0.5-px/2)/scale; v=-(ys+0.5-px/2)/scale
    R=3.0; acc=np.zeros(px*px)
    for zz in np.linspace(R,-R,steps):
        P=np.stack([u.ravel(),v.ravel(),np.full(px*px,zz)],1)@Rv + c      # back to world
        acc+=void(P)
    acc=acc.reshape(px,px)*(2*R/steps)
    a=np.clip(acc/1.2,0,1)[...,None]*0.85; glass=np.array([150,205,235.])
    out=base*(1-a)+glass*a
    return Image.fromarray(out.astype(np.uint8))
V=[('along the shared edge',PF.rot((1,0,0),0)),('side on',PF.rot((1,0,0),-math.pi/2)@PF.rot((0,0,1),math.pi/4)),('oblique',PF.rot((1,0,0),-0.9)@PF.rot((0,0,1),0.5))]
px=560; fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
sheet=Image.new('RGB',(3*px,px+56),PF.GROUND); d=ImageDraw.Draw(sheet)
for i,(name,R) in enumerate(V):
    sheet.paste(view(R,px),(i*px,0)); d.text((i*px+px/2,px+12),name,font=fnt,fill=(233,224,208),anchor='mt')
sheet.save('hourglass-between.png'); print('ok')
