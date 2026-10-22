# The DICTO Ogdoecontahedron seen along a five-fold axis (as Figure 1(c) of paper #31), no colours: stone facets with
# gold edges, and D-I-C-T-O V-cut in platinum leaf into the five hexagons round the centre, carved in each facet's
# own plane so the letters foreshorten with the facet.
import os, json, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
here=os.path.dirname(os.path.abspath(__file__))
G=json.load(open(os.path.join(here,'og-geometry.json'))); V0=np.array(G['v']); F=G['f']
LINE=os.environ.get('LINE','0')=='1'      # gold line drawing: edges and letter outlines only, transparent ground
assert len(F)==80 and sum(len(f)==6 for f in F)==20
def rot(ax,a):
    ax=np.array(ax,float); ax/=np.linalg.norm(ax); K=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+math.sin(a)*K+(1-math.cos(a))*K@K
def align(u,v):
    u=np.array(u,float)/np.linalg.norm(u); v=np.array(v,float)/np.linalg.norm(v); ax=np.cross(u,v)
    if np.linalg.norm(ax)<1e-12: return np.eye(3)
    return rot(ax,math.acos(np.clip(u@v,-1,1)))
# five-fold axis: a corner where five kites meet
deg={}
for f in F:
    if len(f)==4:
        for q in f: deg[q]=deg.get(q,0)+1
apex=max(deg,key=lambda q:(deg[q],V0[q]@np.array([0.1,0.2,1])))
assert deg[apex]==5
R0=align(V0[apex],(0,0,1)); V=V0@R0.T
hexes=[f for f in F if len(f)==6]
ring=sorted([f for f in hexes if V[f][:,2].mean()>0.25*np.abs(V[:,2]).max()], key=lambda f:-V[f][:,2].mean())[:5]
assert len(ring)==5
c0=V[ring[0]].mean(0); spin=math.atan2(c0[0],c0[1])     # turn so the first hexagon sits at the top
V=V@rot((0,0,1),spin).T
TILT=rot((1,0,0),-0.12)                                # a slight tilt, as in the figure
V=V@TILT.T
AXIS=np.array([0,0,1.0])@TILT.T                         # the five-fold axis through the centre star
# each hexagon lies round three stars; its own star is the one of those three that faces the viewer most
# (for the five round the centre, the centre star); its letter lines up with that star (DICTO)
STARS=[V[q]/np.linalg.norm(V[q]) for q in deg if deg[q]==5]
OWN={}
for f in [f for f in F if len(f)==6]:
    c=V[f].mean(0)/np.linalg.norm(V[f].mean(0)); three=sorted(STARS,key=lambda a:-(a@c))[:3]
    OWN[tuple(f)]=max(three,key=lambda a:a[2])
ring_c={tuple(f):V[f].mean(0) for f in ring}
order=sorted(ring,key=lambda f:(math.atan2(ring_c[tuple(f)][0],ring_c[tuple(f)][1])+0.6)%(2*math.pi))   # clockwise from the top
RINGLET={tuple(f):ch for f,ch in zip(order,'DICTO')}
# every hexagon lettered like the DICTO square: the 20 hexagons fall into the five tetrahedra of the compound of five
# (hexagon centres pairwise at cos = -1/3); each tetrahedron takes the letter of its hexagon in the centre ring,
# so no two neighbouring hexagons share a letter and each letter appears four times.
import itertools
Nh=np.array([V[f].mean(0) for f in hexes]); Nh/=np.linalg.norm(Nh,axis=1)[:,None]; Dd=Nh@Nh.T
tets=[c for c in itertools.combinations(range(20),4) if all(abs(Dd[a,b]+1/3)<1e-6 for a,b in itertools.combinations(c,2))]
cover=[cv for cv in itertools.combinations(tets,5) if len(set(sum(cv,())))==20][0]   # one of the two (mirror) compounds
LET={}
for t in cover:
    ch=[RINGLET[tuple(hexes[i])] for i in t if tuple(hexes[i]) in RINGLET]; assert len(ch)==1
    for i in t: LET[tuple(hexes[i])]=ch[0]
assert len(LET)==20
GROUND=tuple(int(x) for x in os.environ.get('BG','20,15,11').split(',')); GOLD=(222,178,80); STONE=(150,141,128)
PLAT={'platinum':(214,218,224),'titanium':(92,95,104)}[os.environ.get('KITE','platinum')]   # kite finish (DICTO: try dark titanium)
import os as _os
TINT=_os.environ.get('TINT','1')=='1'   # DICTO: each lettered hexagon in its element colour, the kite stars in platinum
ELEM={'T':(205,62,40),'O':(232,200,82),'I':(58,112,205),'C':(72,142,72),'D':(138,92,196)}
light=np.array([-0.45,0.55,0.7]); light/=np.linalg.norm(light)
FONT=os.path.join(here,'Cinzel.ttf')
def carve_tile(ch,px):
    f=ImageFont.truetype(FONT,int(px*0.78)); f.set_variation_by_name('Bold')
    m=Image.new('L',(px,px),0); ImageDraw.Draw(m).text((px/2,px/2),ch,font=f,fill=255,anchor='mm')
    x0,y0,x1,y1=m.getbbox(); m=m.transform(m.size,Image.AFFINE,(1,0,(x0+x1)/2-px/2,0,1,(y0+y1)/2-px/2))   # centre the letter's ink
    M=np.array(m)/255.0; ins=M>0.5
    dist=ndimage.gaussian_filter(ndimage.distance_transform_edt(ins),0.8)
    gy,gx=np.gradient(dist); return M,gx,gy
def render(img,cx,cy,rad,SS=2):
    d=ImageDraw.Draw(img); s=rad/np.abs(V[:,:2]).max()*0.98
    P=lambda p:(cx+p[0]*s, cy-p[1]*s)
    for f in sorted(F,key=lambda f:V[f][:,2].mean()):
        n=np.cross(V[f[1]]-V[f[0]],V[f[2]]-V[f[0]]); n/=np.linalg.norm(n)
        if n@V[f].mean(0)<0: n=-n
        if n[2]<=1e-9: continue
        base=STONE
        if TINT and tuple(f) in LET: base=ELEM[LET[tuple(f)]]
        elif TINT and len(f)==4: base=PLAT
        b=0.35+0.65*max(0,n@light); col=tuple(int(c*b) for c in base)
        if TINT and len(f)==4:   # platinum: a soft sheen towards the light
            hv=light+np.array([0,0,1.0]); sp=max(0,n@(hv/np.linalg.norm(hv)))**30
            col=tuple(int(c+(255-c)*0.6*sp) for c in col)
        pts=[P(V[q]) for q in f]
        if LINE: d.line(pts+[pts[0]],fill=GOLD+(255,),width=LW,joint='curve')
        else: d.polygon(pts,fill=col); d.line(pts+[pts[0]],fill=GOLD,width=2*SS)
        if tuple(f) in LET:
            # facet frame: U to the right on screen, Vv up on screen, both in the facet's plane
            # letters set in a circle round the centre of the star (DICTO): each letter's upright points away
            # from the five-fold axis through the star's centre, tops outward, like letters round a coin
            c=V[f].mean(0); ax_=OWN[tuple(f)]; rad=c-ax_*(c@ax_); Vv=rad-n*(rad@n); Vv/=np.linalg.norm(Vv); U=np.cross(Vv,n)
            r=np.linalg.norm(V[f]-c,axis=1).min()            # inradius-ish
            px=int(2*r*s*1.2); M,gx,gy=carve_tile(LET[tuple(f)],px)
            hx,hy=r*0.6,r*0.92                                   # elongated Trajan forms: tall and narrow
            gx=gx*(hy/hx)
            k=1.6; nl=np.dstack([gx*k,-gy*k,np.ones_like(gx)]); nl/=np.linalg.norm(nl,axis=2,keepdims=True)
            nw=nl[...,0:1]*U+nl[...,1:2]*Vv+nl[...,2:3]*n           # groove normals in the world
            lam=np.clip(nw@light,0,1); hv=light+np.array([0,0,1.0]); h=np.clip(nw@(hv/np.linalg.norm(hv)),0,1)**40
            dark=np.array([70,74,82.]); lite=np.array([226,229,235.])
            rgb=dark+(lite-dark)*lam[...,None]**1.3; rgb=rgb+(255-rgb)*h[...,None]*0.8
            tile=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8)); mask=Image.fromarray((ndimage.gaussian_filter(M,0.6)*255).astype(np.uint8))
            if LINE:   # the letter as a gold outline
                ins=M>0.5; ring=ins & ~ndimage.binary_erosion(ins,iterations=max(1,int(px*0.07)))
                tile=Image.new('RGB',(px,px),GOLD); mask=Image.fromarray((ndimage.gaussian_filter(ring.astype(float),0.7)*255).astype(np.uint8))
            # affine map tile (px x px, side 2*r*1.6 in the facet) onto the screen
            corner=lambda a,b_: P(c+U*(a*hx)+Vv*(b_*hy))
            (x0,y0),(x1,y1),(x2,y2)=corner(-1,1),corner(1,1),corner(-1,-1)
            # screen = A*(tx,ty) + o ; PIL needs inverse
            A=np.array([[(x1-x0)/px,(x2-x0)/px],[(y1-y0)/px,(y2-y0)/px]]); Ai=np.linalg.inv(A)
            box=(int(min(x0,x1,x2,x1+x2-x0))-2,int(min(y0,y1,y2,y1+y2-y0))-2,int(max(x0,x1,x2,x1+x2-x0))+2,int(max(y0,y1,y2,y1+y2-y0))+2)
            w,hh=box[2]-box[0],box[3]-box[1]
            o=np.array([x0-box[0],y0-box[1]])
            coef=(Ai[0,0],Ai[0,1],-(Ai[0]@o),Ai[1,0],Ai[1,1],-(Ai[1]@o))
            t2=tile.transform((w,hh),Image.AFFINE,coef,resample=Image.BICUBIC); m2=mask.transform((w,hh),Image.AFFINE,coef,resample=Image.BICUBIC)
            img.paste(t2,box[:2],m2)
if __name__=='__main__':
    if LINE:
        N=600; SS=2; W=N*SS; LW=int(0.012*W); img=Image.new('RGBA',(W,W),(0,0,0,0))
        render(img,W/2,W/2,0.46*W,SS); img.resize((N,N),Image.LANCZOS).save(os.path.join(here,'og-line.png'))
    else:
        N=1400; SS=2; W=N*SS; img=Image.new('RGB',(W,W),GROUND)
        render(img,W/2,W/2,0.46*W,SS); img.resize((N,N),Image.LANCZOS).save(os.path.join(here,'og-letters%s.png'%('' if TINT else '-stone'))); print('ok')
