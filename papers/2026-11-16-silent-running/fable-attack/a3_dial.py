"""Referee check 3 (v2, integer arithmetic): the dial on the two edge circles of the A5 action, exact, k<=30.
C3: v=(1,1,1,s,-3-s); C2: v=(1,1,s,s,-2-2s).  P_k(s) = sum_{g in A5} N^k U_k(<v,gv>/N), N=|v|^2; T_k(orbit of v)=0 <=> P_k(s)=0.
Real roots counted by Sturm sequences built with primitive pseudo-remainders (positive scalings only)."""
import itertools, time, sys
from math import gcd
from functools import reduce
t0=time.time()
def trim(a):
    a=list(a)
    while a and a[-1]==0: a.pop()
    return a
def padd(a,b):
    n=max(len(a),len(b)); return [ (a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(n)]
def pscale(a,c): return [x*c for x in a]
def pmul(a,b):
    if not a or not b: return []
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]+=x*y
    return r
def prim(a):
    a=trim(a)
    if not a: return a
    c=reduce(gcd,a,0); return [x//c for x in a]     # c>0 (gcd seeded with 0): sign preserved
def prem(a,b):
    """pseudo-remainder times a POSITIVE constant, primitive"""
    a=trim(a); b=trim(b); lb=b[-1]
    while len(a)>=len(b):
        la=a[-1]; s=len(a)-len(b)
        # a <- |lb|*a - sign(lb)*la*x^s*b   (multiplying a by |lb|>0)
        a=[x*abs(lb) for x in a]
        f=la*(1 if lb>0 else -1)
        for i,y in enumerate(b): a[s+i]-=f*y
        a=trim(a)
        if not a: break
    return prim(a)
def pgcd(a,b):
    a=prim(a); b=prim(b)
    while b:
        a,b=b,prem(a,b)
    if a and a[-1]<0: a=[-x for x in a]
    return a
def pder(a): return [a[i]*i for i in range(1,len(a))]
def pdiv_exact(a,b):
    """a/b for integer polys if exact (b monic or divides), else None"""
    a=trim(a); b=trim(b); q=[0]*max(1,len(a)-len(b)+1)
    while a and len(a)>=len(b):
        if a[-1]%b[-1]: return None
        c=a[-1]//b[-1]; s=len(a)-len(b); q[s]=c
        for i,y in enumerate(b): a[s+i]-=c*y
        a=trim(a)
    return None if a else trim(q)
def squarefree(p):
    p=prim(p); g=pgcd(p,pder(p))
    if len(g)<=1: return p
    # divide p by g over Q: scale
    from fractions import Fraction as Fr
    a=[Fr(x) for x in p]; q=[Fr(0)]*(len(a)-len(g)+1)
    while a and len(a)>=len(g):
        c=a[-1]/g[-1]; s=len(a)-len(g); q[s]=c
        for i,y in enumerate(g): a[s+i]-=c*y
        while a and a[-1]==0: a.pop()
    assert not a
    den=reduce(lambda x,y:x*y//gcd(x,y),[c.denominator for c in q]); r=[int(c*den) for c in q]
    return prim(r)
def sturm_count(p):
    p=trim(p)
    if len(p)<=1: return 0
    p=squarefree(p); seq=[p,prim(pder(p))]
    while len(seq[-1])>1:
        r=prem(seq[-2],seq[-1])
        if not r: break
        seq.append([-x for x in r])
    def sc(vals):
        v=[x for x in vals if x!=0]; return sum(1 for i in range(len(v)-1) if (v[i]>0)!=(v[i+1]>0))
    minf=[c[-1]*(-1)**(len(c)-1) for c in seq]; pinf=[c[-1] for c in seq]
    return sc(minf)-sc(pinf)
# self-test of Sturm
assert sturm_count([-2,0,1])==2 and sturm_count([1,0,1])==0 and sturm_count(pmul([-6,11,-6,1],[1,0,1]))==3 and sturm_count(pmul([1,3,1],[1,3,1]))==2
def even(p): return sum(1 for i in range(5) for j in range(i+1,5) if p[i]>p[j])%2==0
A5=[p for p in itertools.permutations(range(5)) if even(p)]
KM=30
U=[[1],[0,2]]
for j in range(1,KM): U.append(padd([0]+pscale(U[j],2),pscale(U[j-1],-1)))
def build(v):
    N=[]
    for p in v: N=padd(N,pmul(p,p))
    qs={}
    for g in A5:
        q=[]
        for i in range(5): q=padd(q,pmul(v[i],v[g[i]]))
        key=tuple(trim(q)); qs[key]=qs.get(key,0)+1
    Np=[[1]]
    for i in range(KM): Np.append(pmul(Np[-1],N))
    qp={}
    for key in qs:
        L=[[1]]
        for i in range(KM): L.append(pmul(L[-1],list(key)))
        qp[key]=L
    P={}
    for k in range(1,KM+1):
        tot=[]
        for key,m in qs.items():
            for j in range(k%2,k+1,2):
                if U[k][j]: tot=padd(tot,pscale(pmul(qp[key][j],Np[k-j]),U[k][j]*m))
        P[k]=trim(tot)
    return N,P
s=[0,1]
circles={'C3 (1,1,1,s,-3-s)':[[1],[1],[1],s,[-3,-1]], 'C2 (1,1,s,s,-2-2s)':[[1],[1],s,s,[-2,-2]]}
gold=[1,3,1]
for name,v in circles.items():
    print('==',name); sys.stdout.flush()
    N,P=build(v)
    known=[gold]+([[1,1]] if name.startswith('C2') else [])
    rest={}; info={}
    for k in range(1,KM+1):
        p=P[k]
        if not p: print(f' k={k}: identically zero (forced)'); continue
        deg=len(p)-1; R=prim(p); mult=[]
        for f in known:
            m=0
            while True:
                q=pdiv_exact(R,f)
                if q is None: break
                R=q; m+=1
            mult.append(m)
        # also strip powers of N (no real roots) is unnecessary
        nreal=sturm_count(R)
        rest[k]=R; info[k]=(mult,nreal)
        print(f' k={k}: deg {deg} of {2*k} (root at infinity: {deg<2*k}); mult of s^2+3s+1: {mult[0]}'+(f'; of (s+1): {mult[1]}' if len(mult)>1 else '')+f'; other distinct real roots: {nreal}'); sys.stdout.flush()
    ks=[k for k in rest if info[k][1]>0]
    print(' degrees with other real silences:',ks)
    for a,b in itertools.combinations(ks,2):
        g=pgcd(rest[a],rest[b]); c=sturm_count(g) if len(g)>1 else 0
        if c: print(f'   COMMON real roots of degrees {a},{b}: {c}')
    print('  (no COMMON line = no other base point on this chart is silent in two of these degrees)')
    # rational roots of the remaining parts for the degrees with real roots: test all p/q with |p|,|q|<=60
    from fractions import Fraction as Fr
    cand=sorted(set(Fr(a,b) for a in range(-60,61) for b in range(1,61)))
    for k in ks:
        hits=[str(x) for x in cand if sum(c*x**i for i,c in enumerate(rest[k]))==0]
        print(f'   k={k}: rational roots with height<=60:',hits)
    sys.stdout.flush()
print('time',time.time()-t0); print('FINAL done')
