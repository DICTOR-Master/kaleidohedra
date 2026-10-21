# DICTO emblem, forms iteration (DICTO 2026-10-22): the emblem's gold ring, with each mark replaced by its
# Platonic form (D-I-C-T-O key) carrying its V-cut platinum initial, at the mark's measured place.
# STAR=1 adds, as a variant, five golden Penrose rhombi (the fat 72-degree rhombs) meeting at the centre as a star,
# V-cut and laid with platinum leaf like the initials.
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'dicto_square.py')).read()
exec(src[:src.index("N=1800")])                       # solids, poses, element colours
exec(src[src.index("def align"):src.index("light=np.array")].replace("    return rot(","    return rot(",1)) if 'tet_pose' not in dir() else None
STAR=os.environ.get('STAR','0')=='1'
N=1600; SS=2; W=N*SS; c0=W/2; RR=0.47*W                 # ring radius
GROUND=(20,15,11); GOLD=(222,178,80); EDGE=GOLD
view=np.eye(3); light=np.array([-0.4,0.55,0.75]); light/=np.linalg.norm(light)
# measured from dicto-logo.png: angle of each mark from the centre (degrees), distance 0.625 of the ring radius
PLACE={'D':86.6,'I':19.8,'C':-47.0,'T':-124.7,'O':162.4}; DIST=0.625; FR=0.27   # form circumradius / ring radius
img=Image.new('RGB',(W,W),GROUND); d=ImageDraw.Draw(img)
d.ellipse([c0-RR,c0-RR,c0+RR,c0+RR],outline=GOLD,width=int(0.0115*W))
def pc(P):
    x,y=P[:,0],P[:,1]; c=x*np.roll(y,-1)-np.roll(x,-1)*y; A=c.sum()/2
    return abs(A), np.array([((x+np.roll(x,-1))*c).sum(),((y+np.roll(y,-1))*c).sum()])/(6*A)
sc=RR
for k,ang in PLACE.items():
    V,F=SOL[k]; R=POSE[k]; Vb=(V@R.T)*FR; Fv=[(n@R.T,idx) for n,idx in F]
    ac=[pc(Vb[idx][:,:2]) for n,idx in Fv if n[2]>1e-9]; off=sum(a*c for a,c in ac)/sum(a for a,c in ac)
    pos=np.array([DIST*math.cos(math.radians(ang)),DIST*math.sin(math.radians(ang))])
    Vv=Vb.copy(); Vv[:,:2]+=pos-off
    for n,idx in sorted(Fv,key=lambda f:Vv[f[1]][:,2].mean()):
        if n[2]<=1e-9: continue
        b=0.45+0.55*max(0,n@light); col=tuple(int(c*b+GROUND[m]*(1-b)*0.2) for m,c in enumerate(TONE[k]))
        pts=[(c0+Vv[q,0]*sc, c0-Vv[q,1]*sc) for q in idx]
        d.polygon(pts,fill=col); d.line(pts+[pts[0]],fill=EDGE,width=2*SS)
# carved platinum initials, centred on each form's place
ci=src.index("from scipy import ndimage"); ce=src.index("CARVE={ch")
exec(src[ci:ce].replace("int(0.075*W)","int(0.085*W)").replace("box=int(0.12*W)","box=int(0.13*W)"))
for k,ang in PLACE.items():
    tile,mask,box=carved(k)
    x=c0+DIST*math.cos(math.radians(ang))*sc; y=c0-DIST*math.sin(math.radians(ang))*sc
    img.paste(tile,(int(x-box/2),int(y-box/2)),mask)
if STAR:
    side=0.2*RR; gap=0.012*RR
    m=Image.new('L',(W,W),0); dm=ImageDraw.Draw(m)
    for j in range(5):
        th=math.radians(90+72*j); u=np.exp(1j*(th-math.radians(36))); v=np.exp(1j*(th+math.radians(36)))
        Z=np.array([0,u,u+v,v])*side; cz=Z.mean(); Z=cz+(Z-cz)*(1-gap/side*2.2)   # small gap between rhombi
        dm.polygon([(c0+z.real, c0-z.imag) for z in Z],fill=255)
    M=np.array(m)/255.0; ins=M>0.5
    dist=ndimage.distance_transform_edt(ins); dist=ndimage.gaussian_filter(dist,0.8)
    gy,gx=np.gradient(dist); k=0.9
    n=np.dstack([gx*k, -gy*k, np.ones_like(dist)]); n/=np.linalg.norm(n,axis=2,keepdims=True)
    lam=np.clip(n@Lc,0,1); h=np.clip(n@(Lc+np.array([0,0,1.0]))/np.linalg.norm(Lc+[0,0,1.0]),0,1)**40
    dark=np.array([70,74,82.]); lite=np.array([226,229,235.])
    rgb=dark+(lite-dark)*lam[...,None]**1.3; rgb=rgb+(255-rgb)*h[...,None]*0.8
    img.paste(Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)),(0,0),Image.fromarray((ndimage.gaussian_filter(M,0.6)*255).astype(np.uint8)))
    d=ImageDraw.Draw(img)
    for j in range(5):   # gold edge round each cut
        th=math.radians(90+72*j); u=np.exp(1j*(th-math.radians(36))); v=np.exp(1j*(th+math.radians(36)))
        Z=np.array([0,u,u+v,v])*side; cz=Z.mean(); Z=cz+(Z-cz)*(1-gap/side*2.2)
        P=[(c0+z.real, c0-z.imag) for z in Z]; d.line(P+[P[0]],fill=GOLD,width=2*SS)
img=img.resize((N,N),Image.LANCZOS); img.save('dicto-emblem-forms%s.png'%('-star' if STAR else '')); print('ok')
