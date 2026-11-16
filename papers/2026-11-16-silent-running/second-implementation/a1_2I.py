"""Referee check 1: 2I, sigma, twisted classes, Tables 1-2, Main theorem, Prop 3, Prop 5, ordinary classes."""
import sys, itertools, time
from fractions import Fraction as Fr
from q5lib import *
t0=time.time()
KMAX=60
G=icosians(); n=len(G); assert n==120
idx={qkey(q):i for i,q in enumerate(G)}
mul=[[idx[qkey(qmul(G[i],G[j]))] for j in range(n)] for i in range(n)]
print('2I closed under multiplication: OK (120 elements)')
e=idx[qkey((ONE,ZERO,ZERO,ZERO))]; neg=[idx[qkey(tuple(-x for x in q))] for q in G]
inv=[idx[qkey(qconj(q))] for q in G]
def sig(q): w,x,y,z=q; return (w.bar(),-x.bar(),z.bar(),y.bar())
try:
    s=[idx[qkey(sig(q))] for q in G]
except KeyError: print('FAIL sigma does not map 2I to 2I'); sys.exit()
assert sorted(s)==list(range(n))
assert all(s[mul[i][j]]==mul[s[i]][s[j]] for i in range(n) for j in range(n)); print('sigma is an automorphism of 2I (all 14400 pairs): OK')
print('sigma involution:', all(s[s[i]]==i for i in range(n)))
inner=[g for g in range(n) if all(mul[mul[g][a]][inv[g]]==s[a] for a in range(n))]
print('sigma inner? conjugators found:',len(inner))
print('fixed subgroup order of sigma:', sum(1 for i in range(n) if s[i]==i))
gal_ok=all(qkey(tuple(x.bar() for x in q)) in idx for q in G); print('coordinatewise Galois conjugation preserves 2I:',gal_ok)
c=[q[0] for q in G]
def tclass(x0,tw): return sorted(set(mul[mul[a][x0]][inv[tw[a]]] for a in range(n)))
def classes(tw):
    seen=set(); out=[]
    for x in range(n):
        if x not in seen:
            C=tclass(x,tw); out.append(C); seen.update(C)
    return out
TC=classes(s); print('twisted class sizes:',[len(C) for C in TC])
ident=list(range(n)); OC=classes(ident); print('ordinary class sizes and Re:',[(len(C),c[C[0]]) for C in OC])
def antip(C): return sorted(neg[x] for x in C)
for i,C in enumerate(TC):
    a=antip(C); j=[k for k,D in enumerate(TC) if D==a][0]
    print(f' twisted class {i}: size {len(C)}, contains 1: {e in C}, antipode class {j}')
Uc=[cheb_U(KMAX,c[g]) for g in range(n)]
chi={'1':[ONE]*n,'2':[2*c[g] for g in range(n)],'3':[Uc[g][2] for g in range(n)],'4s':[Uc[g][3] for g in range(n)],'5':[Uc[g][4] for g in range(n)],'6':[Uc[g][5] for g in range(n)]}
chi["2'"]=[x.bar() for x in chi['2']]; chi["3'"]=[x.bar() for x in chi['3']]
chi['4']=[chi['2'][g]*chi["2'"][g] for g in range(n)]
names=['1','2',"2'",'3',"3'",'4','4s','5','6']
def ip(u,v):
    t=ZERO
    for g in range(n): t=t+u[g]*v[g]
    return t/n
okorth=all(ip(chi[a],chi[b])==(1 if a==b else 0) for a in names for b in names); print('nine characters orthonormal:',okorth)
for a in names:
    tw=[chi[a][s[g]] for g in range(n)]
    print(f'  {a} o sigma =',[b for b in names if ip(tw,chi[b])==1])
mult={}
for k in range(0,KMAX+1):
    vk=[Uc[g][k] for g in range(n)]
    m={a:ip(vk,chi[a]) for a in names}
    assert all(v.b==0 and v.a.denominator==1 for v in m.values())
    mult[k]={a:int(m[a].a) for a in names if m[a].a!=0}
print('Table 2:'); 
for k in range(1,25): print('  V_%d ='%k,' + '.join((str(v)+'*' if v>1 else '')+a for a,v in mult[k].items()))
print('multiplicities nondecreasing k->k+12 (k<=48):',all(mult[k+12].get(a,0)>=mult[k].get(a,0) for k in range(0,KMAX-11) for a in names))
dim={'1':1,'2':2,"2'":2,'3':3,"3'":3,'4':4,'4s':4,'5':5,'6':6}
print('Twisted character products chi~(Oi)*chi~(Oj) (J^2=1 normalisation), rows=irreps:')
tprod={}
for a in names:
    M=[[None]*len(TC) for _ in TC]
    for i,Ci in enumerate(TC):
        for j,Cj in enumerate(TC):
            t=ZERO
            for x in Ci:
                for y in Cj: t=t+chi[a][mul[x][y]]
            M[i][j]=t*dim[a]/(len(Ci)*len(Cj))
    tprod[a]=M
    print(f'  {a}:'); 
    for i in range(len(TC)): print('      ',M[i])
def order(g):
    k=1; h=g
    while h!=e: h=mul[h][g]; k+=1
    return k
for i,C in enumerate(TC):
    x=C[0]; print(f'  class {i}: order of (x sigma)^2 = x*sigma(x) in 2I: {order(mul[x][s[x]])}  => order of x.sigma = {2*order(mul[x][s[x]])}')
def tone_sig(C,kmax=KMAX):
    cnt={}
    for x in C:
        for y in C:
            g=mul[inv[x]][y]; cnt[g]=cnt.get(g,0)+1
    T=[]
    for k in range(1,kmax+1):
        t=ZERO
        for g,m in cnt.items(): t=t+Uc[g][k]*m
        T.append(t/(len(C)**2*(k+1)))
    return T
print('Direct exact signatures of the twisted classes, k<=%d:'%KMAX)
odd=set(range(1,KMAX+1,2))
def show(sg): return sg if len(sg)<12 else ('all odd + '+str(sorted(set(sg)-odd)) if odd<=set(sg) else sg)
for i,C in enumerate(TC):
    T=tone_sig(C); sg=[k+1 for k,t in enumerate(T) if t.iszero()]
    rat=all(t.b==0 for t in T); nonneg=all(float(t)>=-1e-30 for t in T)
    print(f'  class {i} size {len(C)}: silent {show(sg)}  tones rational: {rat} nonneg: {nonneg} T1..T8={[str(t) for t in T[:8]]}')
    stable=['1','4','5','4s','6']
    pred=[k for k in range(1,KMAX+1) if all(tprod[a][i][i].iszero() for a in mult[k] if a in stable)]
    print('     Theorem-1 prediction equals direct:',pred==sg)
def perms5(v):
    S={}
    for p in itertools.permutations(v): S[tuple(x.key() for x in p)]=p
    return list(S.values())
def centre(P):
    out=[]
    for p in P:
        m=sum(p,ZERO)/5; out.append(tuple(x-m for x in p))
    return out
p2=PHI*PHI
X=centre(perms5((p2,p2,p2,PHI,ZERO))); F=centre(perms5((p2,p2,ONE,ONE,ZERO))); R=centre(perms5((PHI,-PHI,ZERO,ZERO,ZERO)))
mX=[tuple(-x for x in p) for p in X]; mF=[tuple(-x for x in p) for p in F]
def dot(p,q):
    t=ZERO
    for a,b in zip(p,q): t=t+a*b
    return t
print('sizes X,F,R:',len(X),len(F),len(R),' norms^2:',dot(X[0],X[0]),dot(F[0],F[0]),dot(R[0],R[0]))
ALL=X+mX+F+mF+R; lab=['X']*20+['-X']*20+['F']*30+['-F']*30+['R']*20
r2=dot(X[0],X[0])
GA=[[ (dot(p,q)/r2).key() for q in ALL] for p in ALL]
GB=[[ c[mul[inv[x]][y]].key() for y in range(n)] for x in range(n)]
print('all 120 R^5 points distinct:',len(set(tuple(x.key() for x in p) for p in ALL))==120)
tcl={}
for i,C in enumerate(TC):
    for x in C: tcl[x]=i
sys.setrecursionlimit(10000)
def iso(GA,GB,nA,cons=None,count=False):
    mp=[None]*nA; used=set(); res=[0]; found=[None]
    def rec(d):
        if d==nA:
            res[0]+=1
            if found[0] is None: found[0]=mp[:]
            return not count
        i=d
        for j in range(len(GB)):
            if j in used: continue
            if cons and not cons(i,j): continue
            if GA[i][i]!=GB[j][j]: continue
            ok=True
            for p in range(d):
                if GA[p][i]!=GB[mp[p]][j]: ok=False;break
            if ok:
                mp[i]=j; used.add(j)
                if rec(d+1): return True
                used.discard(j); mp[i]=None
        return False
    rec(0); return found[0],res[0]
i20=[i for i,C in enumerate(TC) if len(C)==20 and antip(C)!=C]; i30=[i for i,C in enumerate(TC) if len(C)==30]; iR=[i for i,C in enumerate(TC) if len(C)==20 and antip(C)==C]
print('antipodal 20-class index:',iR,' non-antipodal 20-classes:',i20,' 30-classes:',i30)
for f30 in i30:
    target={'X':i20[0],'-X':i20[1],'F':f30,'-F':[j for j in i30 if j!=f30][0],'R':iR[0]}
    m,cnt=iso(GA,GB,120,cons=lambda i,j:tcl[j]==target[lab[i]])
    print(f'  Gram isomorphism of 120-point R^5 configuration onto 2I with X->class {i20[0]}, F->class {f30}, R->class {iR[0]}:', 'FOUND' if m else 'none')
def tone_sig_pts(P,kmax=KMAX):
    r=dot(P[0],P[0]); cnt={}
    for p in P:
        for q in P:
            k=(dot(p,q)/r).key(); cnt[k]=cnt.get(k,0)+1
    Us={k:cheb_U(kmax,Q5(*k)) for k in cnt}
    T=[]
    for d in range(1,kmax+1):
        t=ZERO
        for k,m in cnt.items(): t=t+Us[k][d]*m
        T.append(t/(len(P)**2*(d+1)))
    return T
for nm,P in (('X',X),('-X',mX),('F',F),('-F',mF),('R',R)):
    T=tone_sig_pts(P); sg=[k+1 for k,t in enumerate(T) if t.iszero()]
    print(f'  {nm} from R^5 coordinates, k<={KMAX}: silent', show(sg))
for nm,P in (('X',X),('F',F),('R',R)):
    r=dot(P[0],P[0]); Gm=[[ (dot(p,q)/r).key() for q in P] for p in P]
    m,cnt=iso(Gm,Gm,len(P),count=True)
    print(f'  |Aut(Gram {nm})| =',cnt)
for nm,v in (('(3,3,3,2,0)',(3,3,3,2,0)),('(1.7,1.7,1.7,0.6,0)',(Fr(17,10),Fr(17,10),Fr(17,10),Fr(6,10),0)),('(2,2,1,1,0)',(2,2,1,1,0)),('(3,3,2,2,0)',(3,3,2,2,0)),('(1,1,1,0,0)',(1,1,1,0,0))):
    P=centre(perms5(tuple(Q5(x) for x in v))); T=tone_sig_pts(P,30)
    print(f'  control perms of {nm} ({len(P)} pts): silent k<=30:',[k+1 for k,t in enumerate(T) if t.iszero()])
pF=F[0]; print('p3 at (phi^2,phi^2,1,1,0) centred:',sum((x*x*x for x in pF),ZERO), ' p3 at X:',sum((x*x*x for x in X[0]),ZERO))
print('Ordinary classes signatures k<=%d:'%KMAX)
for C in OC:
    if len(C)<2: continue
    T=tone_sig(C); sg=[k+1 for k,t in enumerate(T) if t.iszero()]
    chebz=[k for k in range(1,KMAX+1) if Uc[C[0]][k].iszero()]
    print(f'  size {len(C)} Re={c[C[0]]} order {order(C[0])}: silent',show(sg), '| Chebyshev zeros U_k(Re)=0:',chebz[:12])
print('Prop 5 class pairs:')
C12=[C for C in OC if len(C)==12]
def union_sig(Cs,kmax=KMAX):
    S=sorted(set().union(*Cs)); T=tone_sig(S,kmax); return len(S),show([k+1 for k,t in enumerate(T) if t.iszero()])
for C in C12:
    sC=sorted(s[x] for x in C); msC=antip(sC); mC=antip(C)
    print(f'  C Re={c[C[0]]} (order {order(C[0])}); sigmaC Re={c[sC[0]]}; C u -sigmaC:',union_sig([C,msC]),' C u -C:',union_sig([C,mC]),' C u sigmaC:',union_sig([C,sC]))
print('all 6 pairs of 12-point classes:')
for A,B in itertools.combinations(C12,2):
    print(f'   Re {c[A[0]]} + Re {c[B[0]]}:',union_sig([A,B]))
print('V_15 =',mult[15],' V_13 =',mult[13],' V_17 =',mult[17],' V_19 =',mult[19],' V_14 =',mult[14],' V_18=',mult[18])
print('time',time.time()-t0); print('FINAL done')
