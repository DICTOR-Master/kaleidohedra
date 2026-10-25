# Hidden bonds (DICTO 2026-10-25, "hiding in plain sight?!"): along every 3D weight walk of the relay census, find the MEANING POINTS
# where the two kinds' piece volumes stand in a special ratio (1 = equal, the Delian kind; 2, 3, 4 and inverses = doubling, tripling,
# quadrupling (DICTO: 'another rhythm of volume expansion, tripling etc.'); phi^±1, phi^±2 = golden; 1 + sqrt 2 = silver), and describe the cells there; also describe the untested census stops (hcp holes at 5/24 and -11/24, C15 at -5).
# Floats (scipy) on the census's exact site sets (networks.py, Cartesian via the metric G); candidates only, exact proof later.
import sys, numpy as np, itertools, json
sys.path.insert(0, '../2026-10-25-relay-census/scripts')
from networks import NETS
from scipy.spatial import HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog
PHI=(1+5**.5)/2
def setup(net):
    G=np.array(net['G'],float); L=np.linalg.cholesky(G)                       # x_cart = L^T x
    T=[np.array(t,float) for t in net['T']]; M=[(k,np.array(p,float)) for k,p in net['motif']]
    sites=[]
    rng=range(-2,3)
    for n in itertools.product(rng,repeat=3):
        shift=sum(c*t for c,t in zip(n,T))
        for k,p in M: sites.append((k,(L.T@(p+shift))))
    return sites,M,L
def w(net,kind,lam): c=net['w'][kind]; return float(c[0])+float(c[1])*lam
def cell(net,sites,kind,p,lam):
    H=[]; wp=w(net,kind,lam)
    for k,q in sites:
        d=q-p
        if np.allclose(d,0) or d@d>12*max(1,np.abs(p).max()+1): continue
        H.append(np.r_[2*d,-(q@q-p@p-w(net,k,lam)+wp)])
    H=np.array(H); A,b=H[:,:3],-H[:,3]; n=np.linalg.norm(A,axis=1)
    r=linprog([0,0,0,-1],A_ub=np.c_[A,n],b_ub=b,bounds=[(None,None)]*3+[(0,None)])
    if r.status!=0 or r.x[3]<1e-7: return None
    V=HalfspaceIntersection(H,r.x[:3]).intersections; V=np.unique(np.round(V,9),axis=0)
    return V,ConvexHull(V)
def describe(V,h):
    eq=np.round(h.equations,7); F={}
    for s,e in zip(h.simplices,eq): F.setdefault(tuple(e),set()).update(s)
    F=list(F.values()); E=set()
    for a,b in itertools.combinations(range(len(F)),2):
        sh=F[a]&F[b]
        if len(sh)==2: E.add(tuple(sorted(sh)))
    sz={}
    for f in F: sz[len(f)]=sz.get(len(f),0)+1
    L=sorted({round(float(np.linalg.norm(V[i]-V[j])),5) for i,j in E})
    return dict(corners=len(V),faces=dict(sorted(sz.items())),edge_lengths=len(L),volume=round(float(h.volume),6))
SILVER=1+2**.5
targets={'1':1,'2':2,'1/2':.5,'3':3,'1/3':1/3,'4':4,'1/4':.25,'phi':PHI,'1/phi':1/PHI,'phi^2':PHI**2,'1/phi^2':PHI**-2,'silver':SILVER,'1/silver':1/SILVER}
out={}
for key in ['bcc','delian','nacl','zincblende','hcpholes','a15','c15']:
    if key not in NETS: continue
    net=NETS[key]; sites,M,L=setup(net); A,B=net['A'],net['B']
    pa=next(L.T@p for k,p in M if k==A); pb=next(L.T@p for k,p in M if k==B)
    lams=np.linspace(-15,15,1201); ratio=[]
    for lam in lams:
        ca=cell(net,sites,A,pa,lam); cb=cell(net,sites,B,pb,lam)
        ratio.append(None if (ca is None or cb is None) else ca[1].volume/cb[1].volume)
    res=[]
    for name,tv in targets.items():
        for i in range(len(lams)-1):
            r0,r1=ratio[i],ratio[i+1]
            if r0 is None or r1 is None: continue
            if (r0-tv)*(r1-tv)<=0 and r0!=r1:
                lo,hi=lams[i],lams[i+1]
                for _ in range(40):
                    mid=(lo+hi)/2; ca=cell(net,sites,A,pa,mid); cb=cell(net,sites,B,pb,mid)
                    rm=ca[1].volume/cb[1].volume
                    (lo,hi)=(mid,hi) if (r0-tv)*(rm-tv)>0 else (lo,mid)
                lam=(lo+hi)/2; ca=cell(net,sites,A,pa,lam); cb=cell(net,sites,B,pb,lam)
                res.append(dict(ratio=name,lam=round(lam,8),A=describe(*ca),B=describe(*cb)))
    out[key]=res
    print(f"== {key} ({net['name']}): {A}/{B} volume ratio")
    for r in res: print(f"  {r['ratio']:>8s} at lam={r['lam']:+.6f}  {A}: {r['A']}  |  {B}: {r['B']}")
print('== untested census stops')
for key,lam in [('hcpholes',5/24),('hcpholes',-11/24),('c15',-5)]:
    net=NETS[key]; sites,M,L=setup(net)
    for k in dict.fromkeys(kk for kk,_ in M):
        p=next(L.T@pp for kk,pp in M if kk==k); c=cell(net,sites,k,p,lam)
        print(f"  {key} lam={lam:+.4f} {k}: {describe(*c) if c else 'point (vanished)'}")
json.dump(out,open('hidden_bonds.json','w'),indent=1)
