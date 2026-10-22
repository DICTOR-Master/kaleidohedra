# The telescoping (spyglass) paper model of DICTO's stretched dodecahedron (DICTO 10-22).
# Three parts slide: cap A (6 pentagons) with 10 flaps (inner layer), a loose middle ring of 10 belt faces, and cap B
# with 10 flaps (outer layer). Belt face i is the strip spanned by rim edge e_i (length 1) and the slide direction u
# (face diagonal of Euclid's cube). Flaps and ring are 1 long, so the model runs from short (1) to about 2.7 > long
# (phi*sqrt2 = 2.288). Inner layer scaled by (1 - d), outer by (1 + d), d = 1.2 %, so they nest. Two slider loops hold
# ring and cap-B flaps together on two opposite faces. Marks: 'long' on cap A's flaps and on the ring.
import math, itertools, random, numpy as np
from PIL import Image, ImageDraw, ImageFont
import mixes3 as M, pieces_figure as PF
from nets import adjacency, to2d, overlap, key
phi=M.phi; DOD=M.DOD; u=np.array([1,1,0])/2**.5; LONG=phi*2**.5; d=0.012
F=[np.array(f) for f in PF.hull_faces(DOD)]
nrm=lambda f:(lambda n:n if n@f.mean(0)>0 else -n)(np.cross(f[1]-f[0],f[2]-f[0])/np.linalg.norm(np.cross(f[1]-f[0],f[2]-f[0])))
capA=[i for i,f in enumerate(F) if nrm(f)@u<0]; capB=[i for i,f in enumerate(F) if nrm(f)@u>0]
assert len(capA)==6 and len(capB)==6
# rim: edges shared by a capA face and a capB face, in cyclic order
adj=adjacency(F)
rim=[(i,a) for i in capA for j,a,b in adj[i] if j in capB]
assert len(rim)==10
def cap_net(cap,sign,scale,seed):
    rnd=random.Random(seed); sub={i:[(j,a,b) for j,a,b in adj[i] if j in cap] for i in cap}
    root=rnd.choice(cap); pos={root:to2d(F[root])}; q=[root]
    while q:
        i=q.pop(rnd.randrange(len(q))); nb=sub[i][:]; rnd.shuffle(nb)
        for j,a,b in nb:
            if j in pos: continue
            Pi=pos[i]; A=Pi[a]; B=Pi[(a+1)%len(Pi)]; Q=to2d(F[j]); qa=Q[b]; qb=Q[(b+1)%len(Q)]
            ang=math.atan2(*(B-A)[::-1])-math.atan2(*(qa-qb)[::-1]); R=np.array([[math.cos(ang),-math.sin(ang)],[math.sin(ang),math.cos(ang)]])
            Q2=(Q-qb)@R.T+A; e=B-A; n2=np.array([-e[1],e[0]])
            if (Q2.mean(0)-A)@n2*((Pi.mean(0)-A)@n2)>0: Q2=np.array([A+(p-A)-2*((p-A)@n2)/(n2@n2)*n2 for p in Q2])
            pos[j]=Q2; q.append(j)
    flaps=[]
    for i in cap:
        for j,a,b in adj[i]:
            if j in cap: continue
            f3=F[i]; A3,B3=f3[a],f3[(a+1)%len(f3)]; e3=(B3-A3); e3/=np.linalg.norm(e3)
            P=pos[i]; A,B=P[a],P[(a+1)%len(P)]; e2=(B-A)/np.linalg.norm(B-A); n2=np.array([-e2[1],e2[0]])
            if (P.mean(0)-A)@n2>0: n2=-n2
            w=sign*u; along=w@e3; perp=np.linalg.norm(w-along*e3)
            v=along*e2+perp*n2                       # the slide direction, laid flat in the flap's plane
            flaps.append((np.array([A,B,B+v,A+v]),A,B,v))
    polys=list(pos.values())+[f[0] for f in flaps]
    ok=all(not overlap(polys[x],polys[y]) for x,y in itertools.combinations(range(len(polys)),2))
    return ok,{k:p*scale for k,p in pos.items()},[(f[0]*scale,f[1]*scale,f[2]*scale,f[3]*scale) for f in flaps]
def find_cap(cap,sign,scale):
    for s in range(3000):
        ok,pos,fl=cap_net(cap,sign,scale,s)
        if ok: return pos,fl
    raise SystemExit('no cap net')
def ring_net(scale):
    """the 10 belt faces as two rows of five; each strip starts where the previous one ends (u vertical);
    a glue tab on the right end of each row joins it to the next row's first face"""
    E=[(F[i][a],F[i][(a+1)%5]) for i,a in rim]
    cyc=[E[0]]; rest=E[1:]
    while rest:
        last=cyc[-1][1]
        for k,(p,q) in enumerate(rest):
            if np.allclose(p,last): cyc.append((p,q)); rest.pop(k); break
            if np.allclose(q,last): cyc.append((q,p)); rest.pop(k); break
    strips=[]; tabs=[]
    for row in range(2):
        x=0.0; y=0.0; start=len(strips)
        for p,q in cyc[row*5:row*5+5]:
            e=q-p; h=e@u; wdt=np.linalg.norm(e-h*u)
            strips.append(np.array([[x,y],[x+wdt,y+h],[x+wdt,y+h+1],[x,y+1]])*scale); x+=wdt; y+=h
        tabs.append(np.array([[x,y],[x+0.2,y+0.15],[x+0.2,y+0.85],[x,y+1]])*scale)
        if row==1:   # move the second row clear below the first
            top2=max(p[1] for r in strips[start:]+tabs[-1:] for p in r); low1=min(p[1] for r in strips[:start]+tabs[:1] for p in r)
            dy=low1-top2-0.3*scale
            for r in strips[start:]: r[:,1]+=dy
            tabs[-1][:,1]+=dy
    return strips,tabs
def draw(fname,title,parts,marks,notes,fixed=None):
    dpi=200; W,H=int(21/2.54*dpi),int(29.7/2.54*dpi)
    allp=np.vstack([p for poly,kind in parts for p in poly]); lo=allp.min(0); ext=np.ptp(allp,axis=0)
    s=min((W*0.86)/ext[0],(H*0.70)/ext[1]) if fixed is None else fixed
    off=np.array([(W-ext[0]*s)/2,0.17*H]); tr=lambda p:tuple(off+(np.array(p)-lo)*s)
    img=Image.new('RGB',(W,H),'white'); dr=ImageDraw.Draw(img)
    col={'pent':(206,186,236),'flap':(226,214,244),'ring':(226,214,244),'tab':(236,236,236),'loop':(250,236,190)}
    for poly,kind in parts: dr.polygon([tr(p) for p in poly],fill=col[kind])
    segs={}
    for poly,kind in parts:
        for i in range(len(poly)):
            a,b=poly[i],poly[(i+1)%len(poly)]; k=tuple(sorted([tuple(np.round(a,4)),tuple(np.round(b,4))]))
            segs.setdefault(k,[]).append(kind)
    for (a,b),kinds in segs.items():
        pa,pb=np.array(tr(a)),np.array(tr(b))
        if len(kinds)>1:
            L=np.linalg.norm(pb-pa); n=max(2,int(L/12))
            for m in range(0,n,2): dr.line([tuple(pa+(pb-pa)*m/n),tuple(pa+(pb-pa)*min(m+1,n)/n)],fill=(70,70,70),width=2)
        else: dr.line([tuple(pa),tuple(pb)],fill=(0,0,0),width=3)
    for a,b,label in marks:
        dr.line([tr(a),tr(b)],fill=(200,60,40),width=3)
    f1=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',int(0.017*H)); f2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(0.0125*H))
    dr.text((W*0.06,H*0.03),title,font=f1,fill=(40,30,20))
    for k,t in enumerate(notes): dr.text((W*0.06,H*0.065+k*H*0.02),t,font=f2,fill=(60,60,60))
    dr.text((W*0.06,H*0.955),'DICTO · dictospheres.com · The Stretching Theorem (#49) · telescoping model · CC BY-SA 4.0',font=f2,fill=(110,110,110))
    img.save(fname,resolution=dpi); return s
if __name__=='__main__':
    LM=(LONG-1)/2          # for 'long', the ring sits centred: it starts LM from cap A's rim
    posA,flA=find_cap(capA,+1,1-d); posB,flB=find_cap(capB,-1,1+d)
    def cap_parts(pos,fl,markat):
        parts=[(p,'pent') for p in pos.values()]+[(f[0],'flap') for f in fl]; marks=[]
        # glue tabs on the pentagon edges left open on the sheet (each pair of open edges glued once)
        seen={}
        allpolys=[p for p,k in parts]
        for i,P in pos.items():
            for a in range(5):
                A,B=P[a],P[(a+1)%5]; k=tuple(sorted([tuple(np.round(A,4)),tuple(np.round(B,4))]))
                shared=sum(1 for Q in allpolys for c in range(len(Q)) if tuple(sorted([tuple(np.round(Q[c],4)),tuple(np.round(Q[(c+1)%len(Q)],4))]))==k)
                if shared>1: continue
                e3=frozenset((key(F[i][a]),key(F[i][(a+1)%5])))
                if e3 in seen: continue
                seen[e3]=1
                e=B-A; L=np.linalg.norm(e); n2=np.array([-e[1],e[0]])/L
                if (P.mean(0)-A)@n2>0: n2=-n2
                h=0.16*L; t=np.array([A+e*0.02,B-e*0.02,B-e*0.25+n2*h,A+e*0.25+n2*h])
                if any(overlap(t,Q) for Q in allpolys): continue
                parts.append((t,'tab')); allpolys.append(t)
        for poly,A,B,v in fl:
            if markat: t=markat/1.0; marks.append((A+v*t,B+v*t,'long'))
        return parts,marks
    pa,ma=cap_parts(posA,flA,LM); pb,mb=cap_parts(posB,flB,None)
    ring,rtabs=ring_net(1.0); x1=max(p[0] for r in ring for p in r)
    rm=[]
    for st in ring:
        a=st[0]+(st[3]-st[0])*LM; b=st[1]+(st[2]-st[1])*LM; rm.append((a,b,'long'))
    loops=[(np.array([[0,0],[2.4,0],[2.4,0.35],[0,0.35]])+[0.2+2.7*k,min(p[1] for r in ring for p in r)-0.9],'loop') for k in range(2)]
    jobs=[('telescope-1-capA.png','Telescope, part 1: cap A with inner flaps',pa,ma,['Cut, fold the dashed lines, glue the six pentagons into a cap. The 10 flaps stay open: they slide INSIDE the ring.','Red lines on the flaps: where the ring’s edge sits for the LONG shape.']),
          ('telescope-2-ring.png','Telescope, part 2: the middle ring and two slider loops',[(r,'ring') for r in ring]+[(t,'tab') for t in rtabs]+loops,rm,['Join the two rows into one ring: each row’s end tab goes under the other row’s first face.','Red line: where cap B’s flap edges sit for the LONG shape.','Slider loops: wrap each round the ring and a cap-B flap on two opposite faces; glue the loop to itself only.']),
          ('telescope-3-capB.png','Telescope, part 3: cap B with outer flaps',pb,mb,['Cut, fold, glue the six pentagons into a cap. Its 10 flaps slide OVER the ring.','Short: push everything together (all layers overlap). Long: line up both red marks.'])]
    dpi=200; W,H=int(21/2.54*dpi),int(29.7/2.54*dpi)
    S=min(min((W*0.86)/np.ptp(np.vstack([p for poly,k in j[2] for p in poly]),axis=0)[0],(H*0.70)/np.ptp(np.vstack([p for poly,k in j[2] for p in poly]),axis=0)[1]) for j in jobs)
    for fn,t,parts,marks,notes in jobs: draw(fn,t,parts,marks,notes+['Edge = %.1f cm on all three sheets.'%(S/dpi*2.54)],fixed=S)
    sc1=sc2=sc3=S/dpi*2.54
    ims=[Image.open(p).convert('RGB') for p in ('telescope-1-capA.png','telescope-2-ring.png','telescope-3-capB.png')]
    ims[0].save('swept-dodecahedron-telescope.pdf',save_all=True,append_images=ims[1:],resolution=200)
    print('scales (cm per edge):',round(sc1,2),round(sc2,2),round(sc3,2))
