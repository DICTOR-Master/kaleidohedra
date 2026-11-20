"""Place the slanted rhombic prisms S (C1 case: all 12 edges length 1, Gram of generators (phi^-2,phi^-2,phi^-4)) around one C1.
C1 = truncated icosahedron (edge 1) + dodecahedron centre pyramid on each pentagon.  Slots: each hexagon-hexagon edge takes wedges T,T
(110.905 deg each); each pentagon-hexagon (reflex) edge takes wedges B (69.095) and Q (90) in either order.  A placement maps one S edge
onto the C1 edge, with the S wedge occupying the required angular interval and its first face flush with the C1 face (mirror images allowed).
Interior overlap test: exact separating-axis test for convex polytopes (float64, tolerance 1e-9; every margin is either >= 1e-3 or <= 1e-12).
Run: python place.py   (writes data/place.json)"""
import itertools, json, math, sys
import numpy as np
from scipy.spatial import ConvexHull
phi=(1+5**.5)/2; EPS=1e-9
def pr(s): print(s,flush=True)
class Poly:
    def __init__(s,V):
        s.V=np.array(V,float); h=ConvexHull(s.V,qhull_options='Qt')
        N=[]
        for e in h.equations:
            n=e[:3]
            if not any(np.linalg.norm(n-m)<1e-7 for m in N): N.append(n)
        s.N=np.array(N)
        E=set()
        for t in h.simplices:
            for i,j in ((0,1),(1,2),(0,2)):
                d=s.V[t[i]]-s.V[t[j]]; d=d/np.linalg.norm(d)
                if d[np.argmax(abs(d))]<0: d=-d
                if not any(np.linalg.norm(d-m)<1e-7 for m in E): E.add(tuple(d))
        s.E=np.array(sorted(E)); s.vol=h.volume; s.c=s.V.mean(0)
    def key(s): return tuple(sorted(map(tuple,np.round(s.V,6))))
def sep(A,B):
    """largest separation along any candidate axis (>=-1e-9 means interiors disjoint)"""
    axes=list(A.N)+list(B.N)
    for a in A.E:
        for b in B.E:
            x=np.cross(a,b); n=np.linalg.norm(x)
            if n>1e-9: axes.append(x/n)
    best=-1e9
    for ax in axes:
        pa=A.V@ax; pb=B.V@ax
        best=max(best,pb.min()-pa.max(),pa.min()-pb.max())
    return best
def inside(P,pts,tol=1e-12):
    ok=np.ones(len(pts),bool)
    h=ConvexHull(P.V,qhull_options='Qt')
    for e in h.equations: ok&=(pts@e[:3]+e[3]<=tol)
    return ok
# ---------- C1
cyc=lambda t:[(t[0],t[1],t[2]),(t[2],t[0],t[1]),(t[1],t[2],t[0])]
base=[(0,1,3*phi),(1,2+phi,2*phi),(phi,2,2*phi+1)]
VS=set()
for b in base:
    for sg in itertools.product([1,-1],repeat=3):
        t=tuple(sg[i]*b[i] for i in range(3))
        for c in cyc(t): VS.add(tuple(np.round(np.array(c)/2,9)))
TV=np.array(sorted(VS)); assert len(TV)==60
D=np.linalg.norm(TV[:,None]-TV[None],axis=2)
assert abs(np.sort(D[0])[1]-1)<1e-9
pent_dirs=[np.array(d) for d in {tuple(np.round(np.array(c)/np.linalg.norm(c),9)) for t in itertools.product([1,-1],repeat=2) for c in cyc((0,t[0],t[1]*phi))}]
assert len(pent_dirs)==12
_h={}
for a_,b_,c_ in itertools.combinations(pent_dirs,3):
    if all(abs(x@y-1/5**.5)<1e-6 for x,y in ((a_,b_),(b_,c_),(a_,c_))):
        n_=a_+b_+c_; n_=n_/np.linalg.norm(n_); _h[tuple(np.round(n_,9))]=n_
hex_dirs=list(_h.values())
assert len(hex_dirs)==20
def face_of(n):
    d=TV@n; return np.where(d>d.max()-1e-7)[0]
rin=phi**2/(2*math.sqrt(3-phi))
faces=[]   # (kind, vertex idx, centre, outward normal, apex)
for n in pent_dirs:
    ix=face_of(n); assert len(ix)==5; ct=TV[ix].mean(0); faces.append(('P',ix,ct,n,ct+rin*n))
for n in hex_dirs:
    ix=face_of(n); assert len(ix)==6; faces.append(('H',ix,TV[ix].mean(0),n,None))
TI=Poly(TV); pyr=[Poly(np.vstack([TV[f[1]],f[4]])) for f in faces if f[0]=='P']
C1pieces=[TI]+pyr
pr(f"C1: TI vol {TI.vol:.6f}, pyramid vol {pyr[0].vol:.6f}, total {TI.vol+12*pyr[0].vol:.6f}")
# ---------- S
c=(5**.5-1)/(2*3**.5); nz=math.sqrt(1-2*c*c); s_=math.sqrt(1-c*c); w=nz/s_
SV={}
for ix,iy,iz in itertools.product((0,1),repeat=3):
    x,y=ix*w,iy*w; SV[(ix,iy,iz)]=np.array([x,y,(-c*x-c*y)/nz+iz])
S0=Poly(list(SV.values()))
planes=[(np.array([-1,0,0.]),0),(np.array([1,0,0.]),w),(np.array([0,-1,0.]),0),(np.array([0,1,0.]),w),
        (np.array([-c,-c,-nz]),0.0),(np.array([c,c,nz]),nz)]
sedges=[]
for p,q in itertools.combinations(SV,2):
    if sum(a!=b for a,b in zip(p,q))==1 and abs(np.linalg.norm(SV[p]-SV[q])-1)<1e-9: sedges.append((p,q))
assert len(sedges)==12
def fdir(P,Q,n,d0):
    cen=np.mean([SV[k] for k in SV if abs(np.dot(n,SV[k])-d0)<1e-9],axis=0)
    q=(Q-P)/np.linalg.norm(Q-P); v=cen-P; v=v-np.dot(v,q)*q; return v/np.linalg.norm(v)
SE=[]
for p,q in sedges:
    P,Q=SV[p],SV[q]; fs=[(n,d0) for n,d0 in planes if abs(n@P-d0)<1e-9 and abs(n@Q-d0)<1e-9]; assert len(fs)==2
    v1,v2=fdir(P,Q,*fs[0]),fdir(P,Q,*fs[1]); d=math.acos(np.clip(v1@v2,-1,1))
    SE.append((P,Q,v1,v2,d))
degs=sorted(round(math.degrees(e[4]),4) for e in SE); pr("S dihedrals: "+str({x:degs.count(x) for x in set(degs)}))
T=math.pi/4+math.acos(1/math.sqrt(6)); Bn=math.pi-T
def rot(v,u,a): return v*math.cos(a)+np.cross(u,v)*math.sin(a)+u*np.dot(u,v)*(1-math.cos(a))
def placements(A,B,u,e_start,sigma,a0,dwant):
    """all images of S whose edge lies on A-B with wedge [a0,a0+dwant] (angle measured from e_start about u, sense sigma)"""
    out=[]
    for P,Q,v1,v2,d in SE:
        if abs(d-dwant)>1e-9: continue
        for (va,vb) in ((v1,v2),(v2,v1)):
            q=(Q-P)/np.linalg.norm(Q-P); E=np.array([q,va,np.cross(q,va)]).T
            tau=np.sign(np.dot(np.cross(va,vb),q))
            w1=rot(e_start,u,sigma*a0)
            for F1,orig in ((u,A),(-u,B)):
                F2=w1; F3=tau*sigma*np.cross(u,w1)
                Fm=np.array([F1,F2,F3]).T
                M=Fm@E.T
                V=np.array([M@(SV[k]-P)+orig for k in SV])
                out.append(Poly(V))
    return out
def uniq(L):
    seen={};
    for p in L: seen.setdefault(p.key(),p)
    return list(seen.values())
# ---------- C1 edges
ti_edges=[(i,j) for i in range(60) for j in range(i+1,60) if abs(D[i,j]-1)<1e-9]
assert len(ti_edges)==90
def fdirC(A,B,face):
    kind,ix,ct,n,apex=face; q=(B-A)/np.linalg.norm(B-A); v=ct-A; v=v-v@q*q; return v/np.linalg.norm(v)
rings=[]
for i,j in ti_edges:
    A,B=TV[i],TV[j]; u=(B-A)/1.0; ff=[f for f in faces if i in f[1] and j in f[1]]; assert len(ff)==2
    ff.sort(key=lambda f:f[0]!='H')   # hexagon first
    f1,f2=ff
    e1=fdirC(A,B,f1)
    if f2[0]=='H': e2=fdirC(A,B,f2); kind='hh'
    else:
        v=f2[4]-A; v=v-v@u*u; e2=v/np.linalg.norm(v); kind='hp'
    ang=math.acos(np.clip(e1@e2,-1,1)) # angle of C1 surface faces' wedge measured the short way
    # interior wedge of C1 = angle from f1 to f2 through the solid; exterior = 2pi - interior. Solid lies below: use centre direction
    # decide sense: rotate e1 about u by +t until e2: the exterior sense is the one not passing through the solid (solid contains the origin side)
    inward=-(A+B)/2; inward=inward-inward@u*u
    best=None
    for sg in (1,-1):
        # angle from e1 to e2 in sense sg (0..2pi)
        a=math.atan2(sg*np.dot(np.cross(e1,e2),u),e1@e2)%(2*math.pi)
        mid=rot(e1,u,sg*a/2)
        solid=mid@inward>0   # the arc contains the origin direction -> this arc is the solid side
        if not solid: best=(sg,a)
    sg,ext=best
    rings.append(dict(i=i,j=j,kind=kind,A=A,B=B,u=u,e1=e1,sigma=sg,ext=ext))
for k in ('hh','hp'):
    L=[r for r in rings if r['kind']==k]; pr(f"{k}: {len(L)} edges, exterior angle {math.degrees(L[0]['ext']):.4f} (should be {math.degrees(2*math.pi-(3*math.pi/2-2*math.acos(1/math.sqrt(6)))) if k=='hh' else math.degrees(5*math.pi/4-math.acos(1/math.sqrt(6))):.4f})")
# ---------- local placements
cand={}; stats={'hh':[],'hp':[]}
for idx,r in enumerate(rings):
    A,B,u,e1,sg=r['A'],r['B'],r['u'],r['e1'],r['sigma']; opts=[]
    seqs=[(('T',T),('T',T))] if r['kind']=='hh' else [(('B',Bn),('Q',math.pi/2)),(('Q',math.pi/2),('B',Bn))]
    for seq in seqs:
        a0=0; wedges=[]
        for nm,d in seq:
            P=uniq(placements(A,B,u,e1,sg,a0,d)); wedges.append(P); a0+=d
        # filter: no overlap with C1 pieces
        free=[[p for p in W if all(sep(p,C)>-EPS for C in C1pieces)] for W in wedges]
        pairs=[(p,q) for p in free[0] for q in free[1] if sep(p,q)>-EPS]
        opts+=[(seq[0][0]+seq[1][0],p,q) for p,q in pairs]
        stats[r['kind']].append((seq[0][0]+seq[1][0],[len(W) for W in wedges],[len(W) for W in free],len(pairs)))
    cand[idx]=opts
for k in ('hh','hp'):
    n=[len(cand[i]) for i,r in enumerate(rings) if r['kind']==k]
    pr(f"{k}: edges {len(n)}; surviving ring placements per edge: min {min(n)} max {max(n)}; sample stats {stats[k][0]}")
res={'hh_survivors':sorted(set(len(cand[i]) for i,r in enumerate(rings) if r['kind']=='hh')),
     'hp_survivors':sorted(set(len(cand[i]) for i,r in enumerate(rings) if r['kind']=='hp')),'stats_hh':stats['hh'][0],'stats_hp':stats['hp'][:2]}
dead=[i for i in cand if not cand[i]]
if dead:
    r=rings[dead[0]]; pr(f"CONTRADICTION: {len(dead)} edges have no wedge placement free of C1 overlap, e.g. a {r['kind']} edge")
    # diagnose first wedge: which pieces overlap
    A,B,u,e1,sg=r['A'],r['B'],r['u'],r['e1'],r['sigma']
    for nm,d,a0 in ([('T',T,0),('T',T,T)] if r['kind']=='hh' else [('B',Bn,0),('Q',math.pi/2,0),('Q',math.pi/2,Bn),('B',Bn,math.pi/2)]):
        P=uniq(placements(A,B,u,e1,sg,a0,d)); ov=[min(sep(p,C) for C in C1pieces) for p in P]
        pr(f"   wedge {nm} at {math.degrees(a0):.2f} deg: {len(P)} placements, best C1 separation {max(ov):.6f}, overlap depths {sorted(round(x,4) for x in ov)}")
    res['contradiction']=True
else: res['contradiction']=False

# ---------- global stage: arc consistency over the 90 edge slots, then backtracking
import time; t0=time.time()
ids={}; plist=[]
def pid(p):
    k=p.key()
    if k not in ids: ids[k]=len(plist); plist.append(p)
    return ids[k]
dom={i:[(o,pid(p),pid(q)) for o,p,q in cand[i]] for i in cand}
pr(f"unique S placements: {len(plist)}")
sepc={}
def ok(a,b):
    if a==b: return True
    k=(a,b) if a<b else (b,a)
    if k not in sepc:
        pa,pb=plist[a],plist[b]
        sepc[k]=True if np.linalg.norm(pa.c-pb.c)>2.6 else sep(pa,pb)>-EPS
    return sepc[k]
mid={i:(rings[i]['A']+rings[i]['B'])/2 for i in cand}
nbr={i:[j for j in cand if j!=i and np.linalg.norm(mid[i]-mid[j])<4.2] for i in cand}
compc={}
def comp(i,a,j,b):
    k=(i,a,j,b)
    if k not in compc: compc[k]=all(ok(x,y) for x in a[1:] for y in b[1:])
    return compc[k]
# ---- diagnosis: one pair of neighbouring ring slots at a time (no iteration): which neighbour kills every placement of a slot?
diag={}
for i in dom:
    for j in nbr[i]:
        if j<i: continue
        okA=[a for a in dom[i] if any(comp(i,a,j,b) for b in dom[j])]
        okB=[b for b in dom[j] if any(comp(i,a,j,b) for a in dom[i])]
        if not okA or not okB:
            sh=len({rings[i]['i'],rings[i]['j']}&{rings[j]['i'],rings[j]['j']})
            key=(rings[i]['kind'],rings[j]['kind'],'shared vertex' if sh else 'no shared vertex')
            diag.setdefault(key,[]).append((i,j))
for k,v in diag.items(): pr(f"pair of slots with NO mutually compatible placements: {k}: {len(v)} pairs, first {v[0]}")
res['pair_contradictions']={str(k):len(v) for k,v in diag.items()}
if diag:
    (i,j)=list(diag.values())[0][0]
    best=max((min(sep(plist[x],plist[y]) for x in a[1:] for y in b[1:] if x!=y) if any(x!=y for x in a[1:] for y in b[1:]) else 1) for a in dom[i] for b in dom[j])
    pr(f"for that pair the best achievable worst-case separation over all placements = {best:.6f} (negative = forced interior overlap)")
    res['best_separation_first_bad_pair']=best
sv=[v for k,v in diag.items() if k[2]=='shared vertex']
if sv:
    i,j=sv[0][0]
    best=max(min(sep(plist[x],plist[y]) for x in a[1:] for y in b[1:] if x!=y) for a in dom[i] for b in dom[j])
    pr(f"adjacent slots at one TI vertex: {rings[i]['kind']} edge {i} and {rings[j]['kind']} edge {j}: best worst-case separation over all {len(dom[i])*len(dom[j])} placement pairs = {best:.6f}")
    res['best_separation_adjacent_pair']=best
# arc consistency
changed=True; rounds=0
while changed and time.time()-t0<200:
    changed=False; rounds+=1
    for i in dom:
        keep=[a for a in dom[i] if all(any(comp(i,a,j,b) for b in dom[j]) for j in nbr[i])]
        if len(keep)<len(dom[i]): dom[i]=keep; changed=True
        if not keep: break
    if any(not dom[i] for i in dom): break
sizes={k:sorted(set(len(dom[i]) for i,r in enumerate(rings) if r['kind']==k)) for k in ('hh','hp')}
pr(f"arc consistency: {rounds} rounds, domain sizes {sizes}, time {time.time()-t0:.0f}s")
res['domains_after_AC']=sizes
empty=[i for i in dom if not dom[i]]
if empty:
    res['contradiction']=True; res['contradiction_edge']=rings[empty[0]]['kind']
    i=empty[0]; pr(f"CONTRADICTION: edge slot {rings[i]['kind']} (index {i}) has no placement compatible with its neighbours' placements")
else:
    sol={}
    order=sorted(dom,key=lambda i:len(dom[i]))
    def bt(k):
        if time.time()-t0>240: raise TimeoutError
        if k==len(order): return True
        i=order[k]
        for a in dom[i]:
            if all(comp(i,a,j,sol[j]) for j in nbr[i] if j in sol):
                sol[i]=a
                if bt(k+1): return True
                del sol[i]
        return False
    try: found=bt(0)
    except TimeoutError: found=None
    pr(f"backtracking: {'solution found' if found else ('no solution' if found is False else 'timed out')}")
    res['solution']=found
    if found:
        used={pid_ for a in sol.values() for pid_ in a[1:]}; pr(f"distinct S pieces used around this C1: {len(used)}")
        res['S_pieces']=len(used)
        pieces=[plist[i] for i in used]
        # overlaps among all chosen S and vertex neighbourhood coverage
        bad=0
        for x,y in itertools.combinations(used,2):
            if not ok(x,y): bad+=1
        pr(f"overlapping pairs among chosen S: {bad}")
        rng=np.random.default_rng(1); worst=0; gaps=0
        for v in TV:
            d=rng.normal(size=(3000,3)); d/=np.linalg.norm(d,axis=1)[:,None]; pts=v+0.05*d
            cnt=sum(inside(P,pts).astype(int) for P in C1pieces+pieces)
            gaps+=int((cnt==0).sum()); worst=max(worst,int((cnt>1).sum()))
        pr(f"vertex neighbourhoods (60 TI vertices x 3000 samples, radius 0.05): uncovered {gaps}, multiply covered {worst}")
        res['vertex_uncovered']=gaps; res['vertex_multi']=worst
        allv=np.vstack([TV]+[P.V for P in pieces]+[f[4][None] for f in faces if f[0]=='P'])
        H=ConvexHull(allv); res['hull_volume']=H.volume; res['sumvol']=TI.vol+12*pyr[0].vol+sum(p.vol for p in pieces)
        pr(f"convex hull volume {H.volume:.4f} vs C1 + S volume {res['sumvol']:.4f}")
json.dump(res,open('data/place.json','w'),indent=1,default=str)
pr("FINAL ok" if 'pair_contradictions' in res else "FINAL FAIL")
