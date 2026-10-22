# The diagonally stretched dodecahedron (DICTO 10-22; sibling of F11): the dodecahedron (edge 1) swept along the
# face diagonal (phi, phi, 0) of Euclid's cube: 12 regular pentagons and a belt of 10 parallelograms.
# Pentagons violet, parallelograms lilac, gold edges; three views.
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont
import mixes3 as M, pieces_figure as PF
phi=M.phi; V=np.vstack([M.DOD, M.DOD+np.array([phi,phi,0])]); V=V-V.mean(0)
F=PF.hull_faces(V)
def draw(Rv,px=620):
    PF.Rv=Rv; img=None
    pent=PF.orient(PF.tri([f for f in F if len(f)==5])) if False else None
    T5=[t for f in F if len(f)==5 for t in PF.tri([f])]; T4=[t for f in F if len(f)==4 for t in PF.tri([f])]
    # render all faces together with per-face colour: draw twice and merge by depth via one call per colour on a shared buffer
    allT=T5+T4; cols=[(138,92,196)]*len(T5)+[(196,170,232)]*len(T4)
    # depth-buffer render with per-triangle colours (reuse PF.render internals)
    scale=px*0.15
    T=[t@Rv.T for t in allT]; c=np.mean(np.vstack(T),0)
    imgA=np.zeros((px,px,3)); imgA[:]=PF.GROUND; Z=np.full((px,px),-1e9)
    for t,col in zip(T,cols):
        n=np.cross(t[1]-t[0],t[2]-t[0]); n/=np.linalg.norm(n)
        if n[2]<=0: continue
        b=0.2+0.8*max(0,n@PF.light)**1.1; sh=np.array(col)*b
        P=(t-c)[:,:2]*scale*np.array([1,-1])+px/2; zz=(t-c)[:,2]
        x0,y0=np.floor(P.min(0)).astype(int); x1,y1=np.ceil(P.max(0)).astype(int)
        x0,y0=max(x0,0),max(y0,0); x1,y1=min(x1,px-1),min(y1,px-1)
        X,Y=np.meshgrid(np.arange(x0,x1+1)+0.5,np.arange(y0,y1+1)+0.5)
        (ax,ay),(bx,by),(cx,cy)=P; det=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(det)<1e-12: continue
        l1=((by-cy)*(X-cx)+(cx-bx)*(Y-cy))/det; l2=((cy-ay)*(X-cx)+(ax-cx)*(Y-cy))/det; l3=1-l1-l2
        m=(l1>=-1e-9)&(l2>=-1e-9)&(l3>=-1e-9); z=l1*zz[0]+l2*zz[1]+l3*zz[2]
        sub=Z[y0:y1+1,x0:x1+1]; up=m&(z>sub); sub[up]=z[up]; imgA[y0:y1+1,x0:x1+1][up]=sh
    out=Image.fromarray(imgA.astype(np.uint8)); d=ImageDraw.Draw(out)
    for f in F:   # gold outlines of front faces
        f=np.array(f)@Rv.T; n=np.cross(f[1]-f[0],f[2]-f[0])
        if n[2]<=0: continue
        P=[tuple((p-c)[:2]*scale*np.array([1,-1])+px/2) for p in f]; d.line(P+[P[0]],fill=PF.GOLD,width=3)
    return out
views=[('along the long edge',PF.rot((0,0,1),-math.pi/4)@np.eye(3)),('end on (decagon)',PF.rot((1,0,0),-math.pi/2)@PF.rot((0,0,1),math.pi/4)),('oblique',PF.rot((1,0,0),-0.95)@PF.rot((0,0,1),0.35))]
px=620; fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
sheet=Image.new('RGB',(3*px,px+56),PF.GROUND); d=ImageDraw.Draw(sheet)
for i,(n,R) in enumerate(views): sheet.paste(draw(R,px),(i*px,0)); d.text((i*px+px/2,px+12),n,font=fnt,fill=(233,224,208),anchor='mt')
sheet.save('swept-dodecahedron.png'); print('ok', len(F),'faces')
