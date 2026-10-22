# Cut-and-paste nets for #49 (DICTO 10-22): unfold each solid flat (a spanning tree of its faces, tried many ways until
# no two faces overlap), put glue tabs on the cut edges, and draw an A4 sheet: solid cut lines, dashed fold lines,
# faces lightly tinted (pentagons violet, rhombi lilac, triangles gold), title, scale and the DICTO mark.
import math, itertools, random, numpy as np
from PIL import Image, ImageDraw, ImageFont
import mixes3 as M, pieces_figure as PF
phi=M.phi; DOD=M.DOD
def solid(points):
    V=np.vstack([DOD+np.array(p) for p in points]); F=[np.array(f) for f in PF.hull_faces(V)]
    return F
def key(p): return tuple(np.round(p,6))
def adjacency(F):
    edges={}
    for i,f in enumerate(F):
        for a in range(len(f)):
            e=frozenset((key(f[a]),key(f[(a+1)%len(f)]))); edges.setdefault(e,[]).append((i,a))
    adj={i:[] for i in range(len(F))}
    for e,l in edges.items():
        if len(l)==2: (i,a),(j,b)=l; adj[i].append((j,a,b)); adj[j].append((i,b,a))
    return adj
def to2d(f):
    c=f.mean(0); n=np.cross(f[1]-f[0],f[2]-f[0]); n/=np.linalg.norm(n)
    if n@c<0: n=-n
    u=f[1]-f[0]; u/=np.linalg.norm(u); w=np.cross(n,u)
    return np.array([[(p-f[0])@u,(p-f[0])@w] for p in f])
def place(P,A,B,side):
    # rigid 2D motion taking polygon P's edge (P[i],P[i+1]) onto segment A->B reversed, keeping P on the given side
    return P
def unfold(F,adj,order_seed):
    rnd=random.Random(order_seed); n=len(F); root=rnd.randrange(n)
    pos={root:to2d(F[root])}; parent={root:None}; queue=[root]; tree=set()
    while queue:
        i=queue.pop(rnd.randrange(len(queue)) if rnd.random()<0.5 else 0)
        nb=adj[i][:]; rnd.shuffle(nb)
        for j,a,b in nb:
            if j in pos: continue
            # edge a of face i == edge b of face j (opposite direction)
            Pi=pos[i]; A=Pi[a]; B=Pi[(a+1)%len(Pi)]
            Q=to2d(F[j]); qa=Q[b]; qb=Q[(b+1)%len(Q)]
            # map qb->A, qa->B
            ang=math.atan2(*(B-A)[::-1])-math.atan2(*(qa-qb)[::-1]); R=np.array([[math.cos(ang),-math.sin(ang)],[math.sin(ang),math.cos(ang)]])
            Q2=(Q-qb)@R.T+A
            # make sure Q2 lies on the other side of the edge from face i
            e=B-A; nrm=np.array([-e[1],e[0]])
            if (Q2.mean(0)-A)@nrm*((Pi.mean(0)-A)@nrm)>0:
                Q2=np.array([A+(p-A)-2*((p-A)@nrm)/(nrm@nrm)*nrm for p in Q2])   # reflect across the edge
            pos[j]=Q2; tree.add(frozenset((i,j))); queue.append(j)
    return pos,tree
def overlap(P,Q):
    for poly in (P,Q):
        for a in range(len(poly)):
            e=poly[(a+1)%len(poly)]-poly[a]; nrm=np.array([-e[1],e[0]])
            p=P@nrm; q=Q@nrm
            if p.max()<=q.min()+1e-7 or q.max()<=p.min()+1e-7: return False
    return True
def good_net(F,tries=4000):
    """among non-overlapping unfoldings, keep the one where the most cut edges get a glue tab (then the most compact)"""
    adj=adjacency(F); best=None
    for s in range(tries):
        pos,tree=unfold(F,adj,s)
        polys=list(pos.values())
        if any(overlap(polys[i],polys[j]) for i,j in itertools.combinations(range(len(polys)),2)): continue
        nt=len(tabs(F,pos,tree,adj)); ext=np.ptp(np.vstack(polys),axis=0); score=(nt,-ext[0]*ext[1])
        if best is None or score>best[0]: best=(score,pos,tree,adj)
    return best
def tabs(F,pos,tree,adj):
    """one trapezoid glue tab per cut edge, on one of its two faces, avoiding overlaps"""
    T=[]; done=set(); polys=list(pos.values())
    for i in pos:
        for j,a,b in adj[i]:
            pair=frozenset((i,j))
            if pair in tree or pair in done: continue
            done.add(pair)
            for (k,c) in ((i,a),(j,b)):
                P=pos[k]; A=P[c]; B=P[(c+1)%len(P)]; e=B-A; L=np.linalg.norm(e); nrm=np.array([-e[1],e[0]])/L
                if (P.mean(0)-A)@nrm>0: nrm=-nrm
                h=0.13; tab=np.array([A+e*0.02,B-e*0.02,B-e*0.22+nrm*h,A+e*0.22+nrm*h])
                if all(not overlap(tab,q) for q in polys) and all(not overlap(tab,t) for t in T): T.append(tab); break
    return T
def sheet(name,F,pos,tree,adj,fname,cm_per_unit):
    dpi=200; W,H=int(21/2.54*dpi),int(29.7/2.54*dpi); s=cm_per_unit/2.54*dpi
    T=tabs(F,pos,tree,adj); allp=np.vstack(list(pos.values())+T); lo=allp.min(0); ext=np.ptp(allp,axis=0)
    if ext[0]>ext[1]:   # landscape-wise: rotate 90 degrees to fit the page
        R=np.array([[0,-1],[1,0]]); pos={k:v@R.T for k,v in pos.items()}; T=[t@R.T for t in T]
        allp=np.vstack(list(pos.values())+T); lo=allp.min(0); ext=np.ptp(allp,axis=0)
    fit=min((W-2*0.12*W)/(ext[0]*s),(H-0.25*H)/(ext[1]*s)); s*=min(1,fit)
    off=np.array([(W-ext[0]*s)/2,0.12*H])
    tr=lambda p:tuple(off+(p-lo)*s)
    img=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(img)
    col={3:(244,226,160),4:(226,214,244),5:(206,186,236),6:(215,225,245),7:(215,225,245)}
    for t in T: d.polygon([tr(p) for p in t],fill=(238,238,238),outline=(90,90,90))
    for k,P in pos.items(): d.polygon([tr(p) for p in P],fill=col.get(len(P),(230,230,230)))
    # edges: fold (shared, in tree) dashed; cut solid
    drawn=set()
    for i,P in pos.items():
        for a in range(len(P)):
            A,B=P[a],P[(a+1)%len(P)]; kk=frozenset((key(np.r_[A,0]),key(np.r_[B,0])))
            if kk in drawn: continue
            drawn.add(kk)
            fold=any(frozenset((i,j)) in tree and a==aa for j,aa,bb in adj[i])
            pa,pb=np.array(tr(A)),np.array(tr(B))
            if fold:
                L=np.linalg.norm(pb-pa); n=int(L/14)
                for m in range(0,n,2): d.line([tuple(pa+(pb-pa)*m/n),tuple(pa+(pb-pa)*min(m+1,n)/n)],fill=(60,60,60),width=2)
            else: d.line([tuple(pa),tuple(pb)],fill=(0,0,0),width=3)
    f1=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',int(0.017*H)); f2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',int(0.013*H))
    d.text((W*0.06,H*0.03),name,font=f1,fill=(40,30,20))
    d.text((W*0.06,H*0.062),'Cut on the solid lines, fold on the dashed lines, glue the grey tabs.',font=f2,fill=(60,60,60))
    d.text((W*0.06,H*0.082),'Join the few edges without a tab with tape. Edge = %.1f cm.'%(s/dpi*2.54),font=f2,fill=(60,60,60))
    d.text((W*0.06,H*0.955),'DICTO · dictospheres.com · The Stretching Theorem (#49) · CC BY-SA 4.0',font=f2,fill=(110,110,110))
    img.save(fname,resolution=dpi); return len(T), sum(1 for i in pos for j,a,b in adj[i] if frozenset((i,j)) not in tree)//2
if __name__=='__main__':
    u=np.array([1,1,0])/2**.5
    S={'Short stretched dodecahedron (12 pentagons, 10 rhombi)':[(0,0,0),tuple(u)],
       'Three-cap dodecahedron (12 pentagons, 15 rhombi, 2 triangles)':[(0,0,0),(1/2**.5,1/2**.5,0),(1/2**.5,0,1/2**.5)],
       'Four-cap dodecahedron (12 pentagons, 18 rhombi, 4 triangles)':[(0,0,0),(1/2**.5,1/2**.5,0),(1/2**.5,0,1/2**.5),(0,1/2**.5,1/2**.5)],
       'Long stretched dodecahedron, to the next one (12 pentagons, 10 long faces)':[(0,0,0),(phi,phi,0)],
       "DICTO's F11 stretched dodecahedron, square version (8 pentagons, 4 hexagons, 2 squares)":[(0,0,0),(2/phi,0,0)]}
    pages=[]
    for i,(name,pts) in enumerate(S.items()):
        F=solid(pts); b=good_net(F,1200)
        if b is None: print(name,'NO NET FOUND'); continue
        fn=f'net-{i+1}.png'; nt,ncut=sheet(name,F,b[1],b[2],b[3],fn,3.2); pages.append(fn); print(name,'faces',len(F),'tabs',nt,'of',ncut,'cut edges ->',fn)
    ims=[Image.open(p).convert('RGB') for p in pages]
    if ims: ims[0].save('swept-dodecahedra-nets.pdf',save_all=True,append_images=ims[1:],resolution=200); print('pdf ok')
