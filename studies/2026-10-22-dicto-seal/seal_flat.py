# DICTO seal, flat: Penrose kites and darts (P2) round a five-dart star, clipped to the seal circle, with DICTO's five marks on the five arms.
import cmath, math
from PIL import Image, ImageDraw
import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'p2b.py')).read())
T=star()
for _ in range(4): T=deflate(T)
# star arms: axis direction of the darts at the centre
arms=sorted({round(math.degrees(cmath.phase(v))%360,3) for t,P,Q,R in T if t=='D' and abs(Q)<1e-9 for v in [P]}|
            {round(math.degrees(cmath.phase(P))%360,3) for t,P,Q,R in T if t=='D' and abs(P)<1e-9 for v in [Q]})
cen=[(t,P,Q,R) for t,P,Q,R in T if min(abs(P),abs(Q),abs(R))<1e-9]
axisdirs=sorted({round(math.degrees(cmath.phase(P if abs(Q)<1e-9 else Q))%360,2) for t,P,Q,R in cen})
rot=math.radians(90-axisdirs[0]+36)   # star points sit between dart axes
T=[(t,P*cmath.exp(1j*rot),Q*cmath.exp(1j*rot),R*cmath.exp(1j*rot)) for t,P,Q,R in T]
RAD=0.93                      # seal radius in tiling units
N=1600; SS=3; W=N*SS; s=W/2/RAD*0.94; c0=W/2
xy=lambda z:(c0+z.real*s, c0-z.imag*s)
GROUND=(20,15,11); GOLD=(214,168,74); KITE=(70,52,30); DART=(74,50,104); PURPLE=(169,139,214)
img=Image.new('RGB',(W,W),GROUND); d=ImageDraw.Draw(img)
# fill whole tiles (pairs) by filling halves; edges drawn except the axis
for t,X,Y,Z in T:
    if min(abs(X),abs(Y),abs(Z))>RAD*1.05: continue
    centre=t=='D' and min(abs(X),abs(Y),abs(Z))<1e-9
    d.polygon([xy(X),xy(Y),xy(Z)],fill=PURPLE if centre else (KITE if t=='K' else DART))
lw=max(2,int(4.5*SS))
for t,X,Y,Z in T:
    if min(abs(X),abs(Y),abs(Z))>RAD*1.05: continue
    for a,b in ((Y,Z),(Z,X)):   # X-Y is the axis
        d.line([xy(a),xy(b)],fill=GOLD,width=lw)
# clip to circle
mask=Image.new('L',(W,W),0); ImageDraw.Draw(mask).ellipse([c0-RAD*s,c0-RAD*s,c0+RAD*s,c0+RAD*s],fill=255)
out=Image.new('RGB',(W,W),GROUND); out.paste(img,(0,0),mask); d=ImageDraw.Draw(out)
ring=lambda r,w: d.ellipse([c0-r,c0-r,c0+r,c0+r],outline=GOLD,width=w)
ring(RAD*s,int(9*SS))
# the five marks, on the five arms, as in DICTO's seal (top, then clockwise)
mr=RAD*s*0.205; MR=RAD*s*0.60; w=int(7*SS)
def mark(k,ang):
    x=c0+MR*math.cos(ang); y=c0-MR*math.sin(ang)
    bb=[x-mr,y-mr,x+mr,y+mr]
    if k in (1,3,4): d.ellipse([x-mr*1.12,y-mr*1.12,x+mr*1.12,y+mr*1.12],fill=GROUND)
    def openarc(gap):
        d.arc(bb,start=gap+60,end=gap+300,fill=GROUND,width=int(w*1.8))
        d.arc(bb,start=gap+60,end=gap+300,fill=GOLD,width=w)
    if k==0: openarc(180)                                             # top: arc open to the left
    if k==1:                                                          # right: circle with lens
        d.ellipse(bb,outline=GOLD,width=w)
        p,q=(x-mr*.72,y+mr*.62),(x+mr*.95,y-mr*.3)
        for sgn in (1,-1):
            pts=[]
            for i in range(41):
                u=i/40; mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2; nx,ny=-(q[1]-p[1]),(q[0]-p[0])
                bow=sgn*0.22*math.sin(math.pi*u)
                pts.append((p[0]+(q[0]-p[0])*u+nx*bow, p[1]+(q[1]-p[1])*u+ny*bow))
            d.line(pts,fill=GOLD,width=w)
    if k==2: openarc(135)                                             # lower right: arc open to the lower left
    if k==3:                                                          # lower left: circle with four-point star
        d.ellipse(bb,outline=GOLD,width=w)
        pts=[]
        for i in range(8):
            r=mr*(0.78 if i%2==0 else 0.26); a=math.radians(-30+45*i)
            pts.append((x+r*math.cos(a), y-r*math.sin(a)))
        d.line(pts+[pts[0]],fill=GOLD,width=w,joint='curve')
    if k==4:                                                          # left: circle with dot
        d.ellipse(bb,outline=GOLD,width=w); r=mr*0.17; d.ellipse([x-r,y-r,x+r,y+r],fill=GOLD)
for k in range(5): mark(k, math.radians(90-72*k))
out=out.resize((N,N),Image.LANCZOS); out.save('seal-flat.png')
kites=sum(t=='K' for t,*_ in T)//2; print('done', len(T), axisdirs[:5])
