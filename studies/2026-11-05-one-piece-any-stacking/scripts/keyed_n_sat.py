"""Step 3b check on real geometry: 17 keyed Narcissus (14 Kari tile pieces + 3 relays) in Narcissus-only slab stackings.
Every site's N is placed by a PROPER rigid motion of one reference N (found by matching corners); face keys follow the motion;
contacts are the actual face-to-face pairs. For each stacking word (S = straight, T = turned) we ask SAT whether a keyed tiling
of a finite box exists. Keys:
  tile piece t=(q,n,s,w,e): hexagon = digit n + 3 bumps (q=2: at the hexagon corners NOT over mid corners; q=2/3: at those over mid corners);
     quad Q0 = output digit s; quads Q1,Q2 = 'p'; triangle at azimuth 0 = carry out e, at 180 = carry in w; other triangles 'side'.
  relay d: hexagon = digit d + 3 holes at the corners over its mid corners; one quad = digit d (receiver); two quads 'r'; triangles 'rt'.
Heartbeat per word; final line always."""
import sys, time, itertools, json
import numpy as np
from fractions import Fraction as Fr
from math import floor
from scipy.spatial import ConvexHull
from pysat.solvers import Cadical153
sys.path.insert(0, __file__.rsplit('/',1)[0])
from n_slabs import build, H
t0=time.time()
def hb(m): print(f"HEARTBEAT {time.time()-t0:.0f}s {m}", flush=True)
# ---- Kari tiles (exact)
T=set()
for q,lo,hi in ((Fr(2),Fr(1,2),Fr(1)),(Fr(2,3),Fr(1),Fr(2))):
    for den in (97,101,103,107,211,307):
        for a in range(int(lo*den),int(hi*den)+1):
            x=Fr(a,den)
            if not(lo<=x<=hi): continue
            for k in range(1,400):
                n=floor(k*x)-floor((k-1)*x); s=floor(k*q*x)-floor((k-1)*q*x)
                w=q*floor((k-1)*x)-floor((k-1)*q*x); e=q*floor(k*x)-floor(k*q*x)
                T.add((q,n,s,w,e))
T=sorted(T); assert len(T)==14
# ---- geometry helpers
def faces(P):
    h=ConvexHull(P); F={}
    for eq,sp in zip(h.equations,h.simplices): F.setdefault(tuple(np.round(eq,7)),set()).update(sp)
    return [(np.array(k[:3]),k[3],sorted(v)) for k,v in F.items()]
def az(n): return (round(np.degrees(np.arctan2(n[1],n[0])))%360)
def sites(word,n):
    out=[]
    for P in build(word,n):
        k=int(np.floor(P[:,2].mean()/H+1e-9)); down=np.isclose(P[9,2],P[:,2].min())
        out.append(dict(P=P,k=k,down=bool(down),c=P[:6,:2].mean(0)))
    return out
REF=None
RELAX=set()
FORCE_ROLES=False
def ref_labels(P):
    """label the reference N's faces; returns list of (label, normal, vertex idx)"""
    L=[]
    for nrm,d,idx in faces(P):
        if len(idx)==6: L.append(('H',nrm,idx))
        elif len(idx)==4: L.append(('Q',nrm,idx))
        else: L.append(('T',nrm,idx))
    qs=sorted([f for f in L if f[0]=='Q'],key=lambda f:az(f[1])); ts=[f for f in L if f[0]=='T']
    lab={}
    for i,f in enumerate(qs): lab[('Q',az(f[1]))]=f'Q{i}'
    for f in ts: lab[('T',az(f[1]))]=f'T{az(f[1])}'
    return L,lab
def motions(R0,V):
    """proper rigid motions g with g(R0) = V as corner sets; corner order: 6 hexagon, 3 mid, apex"""
    out=[]
    cR=R0[:6].mean(0); cV=V[:6].mean(0)
    for perm in itertools.permutations(range(6,9)):
        A=np.vstack([R0[9],cR]+[R0[i] for i in range(6,9)]); B=np.vstack([V[9],cV]+[V[i] for i in perm])
        ma,mb=A.mean(0),B.mean(0); U,S,Wt=np.linalg.svd((A-ma).T@(B-mb)); Rm=(U@Wt).T
        if np.linalg.det(Rm)<0: continue
        G=(R0-ma)@Rm.T+mb
        if all(np.min(np.linalg.norm(V-g,axis=1))<1e-6 for g in G): out.append((Rm,ma,mb))
    return out
def run(word,W,D,n=4):
    S0=sites(word,n)
    # reference = down N of slab 0 nearest the axis
    ref=min([s for s in S0 if s['k']==0 and s['down']],key=lambda s:np.linalg.norm(s['c']))
    R0=ref['P']; L0,lab=ref_labels(R0)
    over=[i for i in range(6) if any(np.allclose(R0[i,:2],R0[j,:2]) for j in range(6,9))]   # hexagon corners over mid corners
    betw=[i for i in range(6) if i not in over]
    tri_az=sorted({az(f[1]) for f in L0 if f[0]=='T'}); OUT,IN=tri_az[0],(tri_az[0]+180)%360
    assert IN in tri_az
    # box
    box=[s for s in S0 if abs(s['c'][0])<=W/2+1e-9 and -1e-9<=s['c'][1]<=D*np.sqrt(3)/2-1e-9+0.5]
    # pieces: 14 tiles then 3 relays; each = dict face-label -> key, plus hexagon corner set
    pieces=[]
    for t in T:
        q,nn,ss,ww,ee=t
        keys={'H':('Hd',nn),'Q0':('S',ss),'Q1':('p',),'Q2':('p',)}
        for a in tri_az: keys[f'T{a}']=('side',)
        keys[f'T{OUT}']=('out',str(q),str(ee)); keys[f'T{IN}']=('in',str(q),str(ww))
        pieces.append(dict(name=f'tile{t}',keys=keys,corners=(betw if q==2 else over),kind='tile'))
    for d in (0,1,2):
        keys={'H':('Hr',d),'Q0':('D',d),'Q1':('r',),'Q2':('r',)}
        for a in tri_az: keys[f'T{a}']=('rt',)
        pieces.append(dict(name=f'relay{d}',keys=keys,corners=over,kind='relay'))
    # placements per site: motion -> map world face (by normal) -> ref label
    for s in box:
        s['pl']=[]
        for Rm,ma,mb in motions(R0,s['P']):
            fm={}
            for lbl,nrm,idx in L0:
                key='H' if lbl=='H' else lab[(lbl,az(nrm))]
                fm[tuple(np.round(Rm@nrm,5))]=key
            s['pl'].append((Rm,ma,mb,fm))
        assert len(s['pl'])==3, len(s['pl'])
    # contacts: pairs of sites sharing a face (opposite normals, same plane, close centroids)
    def wf(s):
        return [(nrm,d,s['P'][idx].mean(0)) for nrm,d,idx in faces(s['P'])]
    for s in box: s['F']=wf(s)
    con=[]
    for i,a in enumerate(box):
        for j in range(i+1,len(box)):
            b=box[j]
            if np.linalg.norm(a['P'].mean(0)-b['P'].mean(0))>1.6: continue
            for na,da,ca in a['F']:
                for nb,db,cb in b['F']:
                    if np.allclose(na,-nb,atol=1e-6) and abs(da+db)<1e-6 and np.linalg.norm(ca-cb)<1e-6:   # true face-to-face: same centroid (coplanar faces at other heights excluded)
                        con.append((i,j,tuple(np.round(na,5)),tuple(np.round(nb,5))))
    # compatibility
    def comp(ka,kb,a_pl,b_pl,pa,pb,ia,ib):
        A,B=ka[0],kb[0]
        if A in RELAX or B in RELAX: return True
        if {A,B}=={'Hd','Hr'}:
            if ka[1]!=kb[1]: return False
            # bumps of the tile piece must sit on the holes of the relay (world positions)
            (ta,tpl,ti),(ra,rpl,ri)=((pa,a_pl,ia),(pb,b_pl,ib)) if A=='Hd' else ((pb,b_pl,ib),(pa,a_pl,ia))
            g=lambda pl,idx: [(pl[0]@(R0[c]-pl[1]))+pl[2] for c in idx]
            X=g(tpl,ta['corners']); Y=g(rpl,ra['corners'])
            return all(min(np.linalg.norm(x-y) for y in Y)<1e-6 for x in X)
        if {A,B}=={'S','D'}: return ka[1]==kb[1]
        if {A,B}=={'p','r'}: return True
        if {A,B}=={'out','in'}: return ka[1]==kb[1] and ka[2]==kb[2]
        if A==B=='side' or A==B=='rt': return True
        return False
    Sv=Cadical153(); var={}
    def v(k):
        if k not in var: var[k]=len(var)+1
        return var[k]
    for si,s in enumerate(box):
        xs=[v((si,p,r)) for p in range(len(pieces)) for r in range(3)]
        Sv.add_clause(xs)
        for a,b in itertools.combinations(xs,2): Sv.add_clause([-a,-b])
    if FORCE_ROLES:
        for si,s in enumerate(box):
            for p in range(len(pieces)):
                if (pieces[p]['kind']=='relay')==s['down']:
                    for r in range(3): Sv.add_clause([-v((si,p,r))])
    for i,j,na,nb in con:
        for p in range(len(pieces)):
            for r in range(3):
                ka=pieces[p]['keys'][box[i]['pl'][r][3][na]]
                ok=[v((j,p2,r2)) for p2 in range(len(pieces)) for r2 in range(3)
                    if comp(ka,pieces[p2]['keys'][box[j]['pl'][r2][3][nb]],box[i]['pl'][r],box[j]['pl'][r2],pieces[p],pieces[p2],i,j)]
                Sv.add_clause([-v((i,p,r))]+ok)
    sat=Sv.solve()
    info=dict(word=word,sites=len(box),contacts=len(con),sat=sat)
    if sat:
        m=set(x for x in Sv.get_model() if x>0)
        per=[]
        for k in range(len(word)+1):
            cnt={}
            for si,s in enumerate(box):
                if s['k']!=k: continue
                for p in range(len(pieces)):
                    for r in range(3):
                        if v((si,p,r)) in m: cnt.setdefault(('down' if s['down'] else 'up')+':'+pieces[p]['kind']+('' if pieces[p]['kind']=='relay' else ':x'+str(T[p][0])),0); cnt[('down' if s['down'] else 'up')+':'+pieces[p]['kind']+('' if pieces[p]['kind']=='relay' else ':x'+str(T[p][0]))]+=1
            per.append(cnt)
        info['layers']=per
    return info
if __name__=='__main__':
    W=float(sys.argv[1]) if len(sys.argv)>1 else 6; D=int(sys.argv[2]) if len(sys.argv)>2 else 2; m=int(sys.argv[3]) if len(sys.argv)>3 else 3
    words=sys.argv[4].split(',') if len(sys.argv)>4 else [''.join(w) for w in itertools.product('ST',repeat=m)]
    res=[]
    for w in words:
        r=run(w,W,D); res.append(r); hb(f"word {w}: sites {r['sites']} contacts {r['contacts']} -> {'SAT' if r['sat'] else 'UNSAT'}")
        if r['sat'] and len(words)<=4: print('  layers:',r['layers'],flush=True)
    json.dump(res,open(f'keyed_n_W{W}_D{D}_m{m}.json','w'),default=str)
    print(f"FINAL ok words={len(res)} sat={sum(r['sat'] for r in res)} {time.time()-t0:.0f}s",flush=True)
