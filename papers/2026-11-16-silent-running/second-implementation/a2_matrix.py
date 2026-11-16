"""Referee check 2: Sym6 exceptional twist on S^24; W(H3) on S^8; W+(H4) on S^15 with a product-rule test; 2T, 2O rows."""
import sys, itertools, time
from fractions import Fraction as Fr
from q5lib import *
t0=time.time()
# ---------- Sym6 ----------
print('== Sym6, exceptional outer automorphism ==')
P6=list(itertools.permutations(range(6))); pid={p:i for i,p in enumerate(P6)}
def pm(p,q): return tuple(p[q[i]] for i in range(6))   # p after q
def pinv(p):
    r=[0]*6
    for i,x in enumerate(p): r[x]=i
    return tuple(r)
def transp(i,j):
    l=list(range(6)); l[i],l[j]=l[j],l[i]; return tuple(l)
idp=tuple(range(6))
def ctype(p):
    seen=[0]*6; out=[]
    for i in range(6):
        if not seen[i]:
            l=0; j=i
            while not seen[j]: seen[j]=1; j=p[j]; l+=1
            out.append(l)
    return tuple(sorted(out,reverse=True))
triples=[p for p in P6 if ctype(p)==(2,2,2)]; assert len(triples)==15
gens=[transp(i,i+1) for i in range(5)]
def order(p):
    k=1;q=p
    while q!=idp: q=pm(q,p);k+=1
    return k
sol=None
def search(img):
    global sol
    if sol: return
    i=len(img)
    if i==5: sol=img[:]; return
    for t in triples:
        ok=True
        for j,u in enumerate(img):
            o=order(pm(t,u))
            if (i-j==1 and o!=3) or (i-j>1 and o!=2): ok=False;break
        if ok: search(img+[t])
search([])
# extend homomorphism by BFS
xi={idp:idp}; frontier=[idp]
while frontier:
    nf=[]
    for g in frontier:
        for s_,t_ in zip(gens,sol):
            h=pm(g,s_)
            if h not in xi: xi[h]=pm(xi[g],t_); nf.append(h)
    frontier=nf
assert len(xi)==720 and len(set(xi.values()))==720
assert all(xi[pm(g,s_)]==pm(xi[g],t_) for g in P6 for s_,t_ in zip(gens,sol))
print('xi built: bijective homomorphism; transposition ->',ctype(xi[gens[0]]),'; 3-cycle ->',ctype(xi[(1,2,0,3,4,5)]),'; 6-cycle ->',ctype(xi[(1,2,3,4,5,0)]))
def fix(p): return sum(1 for i in range(6) if p[i]==i)
seen=set(); TCS=[]
for x in P6:
    if x in seen: continue
    C={x}; fr=[x]
    while fr:
        nf=[]
        for y in fr:
            for a in gens:
                z=pm(pm(a,y),pinv(xi[a]))
                if z not in C: C.add(z); nf.append(z)
        fr=nf
    TCS.append(sorted(C)); seen|=C
print('twisted class sizes:',sorted(len(C) for C in TCS))
KM=40; lam=Fr(23,2)
for C in TCS:
    x0=C[0]; xi0=pinv(x0); cnt={}
    for y in C:
        v=Fr(fix(pm(xi0,y))-1,5); cnt[v]=cnt.get(v,0)+1
    # homogeneity check: distribution from another base point
    x1=C[-1]; xi1=pinv(x1); cnt1={}
    for y in C:
        v=Fr(fix(pm(xi1,y))-1,5); cnt1[v]=cnt1.get(v,0)+1
    Q={v:gegen_norm(KM,lam,v) for v in cnt}
    T=[sum(Q[v][k]*m for v,m in cnt.items())/len(C) for k in range(1,KM+1)]
    print(f'  class size {len(C)}: inner-product distribution {dict(sorted(cnt.items()))} homogeneous:{cnt==cnt1}; silent k<=40:',[k+1 for k,t in enumerate(T) if t==0],' min nonzero tone %.3e'%min(float(t) for t in T if t!=0))
# Molien of twist group on R^25
def ppow(p,k):
    q=idp
    for _ in range(k): q=pm(q,p)
    return q
a=[Fr(0)]*(KM+1)
cache={}
for g in P6:
    key=(ctype(g),ctype(xi[g]))
    if key not in cache:
        ps=[None]+[ (fix(ppow(g,i))-1)*(fix(ppow(xi[g],i))-1) for i in range(1,KM+1)]
        h=[Fr(1)]
        for k in range(1,KM+1): h.append(sum(ps[i]*h[k-i] for i in range(1,k+1))/k)
        cache[key]=h
    h=cache[key]
    for k in range(KM+1): a[k]+=h[k]
a=[x/720 for x in a]
harm=[a[k]-(a[k-2] if k>=2 else 0) for k in range(KM+1)]
print('invariant harmonics of twist group k=1..12:',[int(x) for x in harm[1:13]],' zero degrees k<=40:',[k for k in range(1,KM+1) if harm[k]==0])
# ---------- 2I based matrix spheres ----------
G=icosians(); n=120; idx={qkey(q):i for i,q in enumerate(G)}
mul=[[idx[qkey(qmul(G[i],G[j]))] for j in range(n)] for i in range(n)]
inv=[idx[qkey(qconj(q))] for q in G]; neg=[idx[qkey(tuple(-x for x in q))] for q in G]
def sig(q): w,x,y,z=q; return (w.bar(),-x.bar(),z.bar(),y.bar())
s=[idx[qkey(sig(q))] for q in G]; c=[q[0] for q in G]
def classes(tw):
    seen=set(); out=[]
    for x in range(n):
        if x not in seen:
            C=sorted(set(mul[mul[a][x]][inv[tw[a]]] for a in range(n))); out.append(C); seen.update(C)
    return out
TC=classes(s); OC=classes(list(range(n)))
def name_t(C):
    if len(C)==30: return 'F'
    return 'R' if sorted(neg[x] for x in C)==C else 'X'
def cosdist(C):
    x0=C[0]; d={}
    for y in C:
        k=c[mul[inv[x0]][y]]; d[k]=d.get(k,0)+1
    return d
def s3sig(C,kmax):
    d=cosdist(C); out=set()
    Us={k:cheb_U(kmax,k) for k in d}
    for k in range(1,kmax+1):
        t=ZERO
        for v,m in d.items(): t=t+Us[v][k]*m
        if t.iszero(): out.add(k)
    return out
print('== W(H3) Galois twist on S^8 (rotation part = 2I/+-1; inner product (4c^2-1)/3) ==')
KM=30
for C in TC:
    d=cosdist(C); dd={}
    for v,m in d.items():
        t=(4*v*v-1)/3; dd[t]=dd.get(t,0)+m
    T=[]
    Q={v:gegen_norm(KM,Fr(7,2),v) for v in dd}
    for k in range(1,KM+1):
        t=ZERO
        for v,m in dd.items(): t=t+Q[v][k]*m
        T.append(t)
    img=len(set(min(x,neg[x]) for x in C))
    print(f'  image of {name_t(C)} in A5: {img} elements; silent k<=30 on S^8:',[k+1 for k,t in enumerate(T) if t.iszero()])
print('== W+(H4) on S^15: classes O1 x O2 mod +-; inner product c1*c2; product-rule test ==')
KM=20
def s15sig(C1,C2):
    d1=cosdist(C1); d2=cosdist(C2); dd={}
    for v,m in d1.items():
        for w,m2 in d2.items():
            t=v*w; dd[t]=dd.get(t,0)+m*m2
    Q={v:gegen_norm(KM,Fr(7),v) for v in dd}
    out=[]
    for k in range(1,KM+1):
        t=ZERO
        for v,m in dd.items(): t=t+Q[v][k]*m
        if t.iszero(): out.append(k)
    return out
def rule(S1,S2):
    out=[]
    for k in range(1,KM+1):
        ok=True
        for j in range(k%2,k+1,2):
            for l in range(k%2,k+1,2):
                if (j,l)==(0,0): continue
                if not ((j in S1) or (l in S2)): ok=False
        if ok: out.append(k)
    return out
def nm_o(C): return f'C{len(C)}(Re={c[C[0]]})'
def short(L):
    od=[k for k in range(1,KM+1,2)]
    return ('all odd + '+str([k for k in L if k%2==0])) if set(od)<=set(L) else str(L)
allok=True
print(' Galois both: twisted x twisted')
for C1 in TC:
    for C2 in TC:
        S1=s3sig(C1,KM); S2=s3sig(C2,KM); d=s15sig(C1,C2); r=rule(S1,S2)
        same = (sorted(neg[x] for x in C1)==C1) or (sorted(neg[x] for x in C2)==C2)
        size=len(C1)*len(C2)//(2 if same else 1)
        allok&=(d==r)
        print(f'   {name_t(C1)}{C1[0]:>3} x {name_t(C2)}{C2[0]:>3}: class size mod+- {size}: direct {short(d)} | product rule {short(r)} | agree {d==r}')
print(' Galois left only: twisted x ordinary')
for C1 in TC:
    for C2 in OC:
        S1=s3sig(C1,KM); S2=s3sig(C2,KM); d=s15sig(C1,C2); r=rule(S1,S2)
        allok&=(d==r)
        print(f'   {name_t(C1)}{C1[0]:>3} x {nm_o(C2)}: |O1||O2|={len(C1)*len(C2)}: direct {short(d)} | product rule {short(r)} | agree {d==r}')
print(' product rule agrees with direct sums on all classes:',allok)
# ---------- 2T, 2O ----------
print('== 2T with outer automorphism (conjugation by (1+i)/sqrt2: (w,x,y,z)->(w,x,-z,y)) ==')
T24=[i for i,q in enumerate(G) if all(x.b==0 for x in q)]; assert len(T24)==24
def sT(i):
    w,x,y,z=G[i]; return idx[qkey((w,x,-z,y))]
tw={i:sT(i) for i in T24}; assert set(tw.values())==set(T24)
assert all(tw[mul[a][b]]==mul[tw[a]][tw[b]] for a in T24 for b in T24)
seen=set()
for x in T24:
    if x in seen: continue
    C=sorted(set(mul[mul[a][x]][inv[tw[a]]] for a in T24)); seen|=set(C)
    print(f'  2T twisted class size {len(C)} (base Re={c[x]}): silent k<=30:',short(sorted(s3sig(C,30))) if len(C)>1 else '-', ' cos distribution',{str(k):v for k,v in cosdist(C).items()})
print('time',time.time()-t0); print('FINAL done')
