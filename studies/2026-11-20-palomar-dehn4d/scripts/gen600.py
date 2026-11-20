import itertools, json, math
def mul(x,y): return (x[0]*y[0]+x[1]*y[1], x[0]*y[1]+x[1]*y[0]+x[1]*y[1])
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def neg(x): return (-x[0],-x[1])
PHI=(1+5**.5)/2
def val(x): return x[0]+x[1]*PHI
def dot(u,v):
    r=(0,0)
    for a,b in zip(u,v): r=add(r,mul(a,b))
    return r
def vadd(u,v): return tuple(add(a,b) for a,b in zip(u,v))
def vsub(u,v): return tuple(sub(a,b) for a,b in zip(u,v))
def vscale(c,u): return tuple(mul(c,a) for a in u)
perms=list(itertools.permutations(range(4)))
def parity(p): return sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j])%2
orders=[p for p in perms if parity(p)==0]+[p for p in perms if parity(p)==1]
Z=(0,0);one=(1,0);two=(2,0);phi=(0,1);iphi=(-1,1);iphi2=(2,-1);phi2=(1,1);s5=(-1,2)
bases=[(24,(Z,Z,two,two)),(24,(one,one,one,s5)),(24,(iphi2,phi,phi,phi)),(24,(iphi,iphi,iphi,phi2)),
       (12,(Z,iphi2,one,phi2)),(12,(Z,iphi,phi,s5)),(12,(iphi,one,phi,two))]
def orbit(n,z):
    out=[]
    for s_ in orders[:n]:
        for s in range(16):
            out.append(tuple(neg(z[s_[i]]) if (s>>i)&1 else z[s_[i]] for i in range(4)))
    return out
full=[]
for n,z in bases: full+=orbit(n,z)
L=[]; seen=set()
for v in full:
    if v not in seen: seen.add(v); L.append(v)
assert len(L)==600 and all(dot(v,v)==(8,0) for v in L)
# vertices of P: directions = 600-cell vertices of norm 2 (cell120Z style), scaled: v = w*(2-phi)/2
W=set()
for z in [(two,Z,Z,Z)]:
    for p in perms:
        for s in range(16): W.add(tuple(neg(z[p[i]]) if (s>>i)&1 else z[p[i]] for i in range(4)))
for s in range(16): W.add(tuple(neg(one) if (s>>i)&1 else one for i in range(4)))
for p in orders[12:]:
    z=(phi,one,iphi,Z)
    for s in range(16): W.add(tuple(neg(z[p[i]]) if (s>>i)&1 else z[p[i]] for i in range(4)))
W=sorted(W); assert len(W)==120, len(W)
V=[vscale((2,-1),w) for w in W]   # v = (1/2) * gvec(V[i])
vals=set(); act=[[] for _ in L]
for j,v in enumerate(V):
    for k,a in enumerate(L):
        d=dot(a,v); vals.add(d)
        assert val(d)<=2+1e-9
        if d==(2,0): act[k].append(j)
print("vertex dot values", sorted(vals, key=val))
assert all(len(x)==4 for x in act)
facets=[frozenset(x) for x in act]
recs=[]
cvals=set()
for k in range(600):
    vs=act[k]; nbrs=[]
    for i in vs:
        others=frozenset(vs)-{i}
        cand=[k2 for k2 in range(600) if k2!=k and others<=facets[k2]]
        assert len(cand)==1
        nbrs.append(cand[0])
        cvals.add(dot(L[cand[0]],V[i]))
        assert dot(L[k],L[cand[0]])==(-2,6)
    s=((0,0),(0,0),(0,0),(0,0))
    for q in nbrs: s=vadd(s,L[q])
    recs.append((vs,nbrs,s))
print("c values (2c):", cvals)
c2=list(cvals)[0]
# check 2*sum = (6 + 2c) a_p
for k,(vs,nbrs,s) in enumerate(recs):
    assert vscale((2,0),s)==vscale(add((6,0),c2),L[k]), k
print("sum identity ok; 6+2c =", add((6,0),c2), "c =", val(c2)/2)
# patch: record 0, neighbour index 0 opposite vertex vs[0]; triangle = vs[1],vs[2],vs[3]
vs,nbrs,_=recs[0]; p=0; q=nbrs[0]; t=[V[i] for i in vs[1:]]
g6=vadd(vadd(t[0],t[1]),t[2])    # g = (1/6) gvec g6
e1=vsub(t[1],t[0])               # e1 = (1/2) gvec e1
e2=vsub(vsub(vscale((2,0),t[2]),t[0]),t[1])
print("p,q",p,q,"g6",g6,"e1",e1,"e2",e2)
print("e1.e2",dot(e1,e2),"|e1|^2*4",dot(e1,e1),val(dot(e1,e1))/4,"|e2|^2*4",dot(e2,e2),val(dot(e2,e2))/4)
gv=sorted({dot(a,g6) for a in L}, key=val); print("g dot values (x6):", [(d,round(val(d),4)) for d in gv])
print("p,q at g:", dot(L[p],g6), dot(L[q],g6), "ap.e1",dot(L[p],e1),dot(L[p],e2),dot(L[q],e1),dot(L[q],e2))
json.dump(dict(full=full,L=L,V=V,recs=[(r[0],r[1]) for r in recs],orders=orders,c2=c2,g6=g6,e1=e1,e2=e2,p=p,q=q,vals=sorted(vals,key=val),gvals=gv),open('/tmp/gen600.json','w'))
