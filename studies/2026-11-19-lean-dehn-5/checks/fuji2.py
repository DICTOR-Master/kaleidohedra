exec(open('q5.py').read())
r5=Q(0,1)
h=Fr(1,2); q=Fr(1,4)
P=[[Q(-q,-q)]*3,[Q(-q,-q),Q(-q,-q),Q(-5*q,-q)],[Q(-h,-h),Q(-h),Q(-3*q,-q)],[Q(-h),Q(-3*q,-q),Q(-h,-h)],
   [Q(-5*q,-q),Q(-q,-q),Q(-q,-q)],[Q(-q,-q),Q(-5*q,-q),Q(-q,-q)],[Q(-3*q,-q),Q(-h,-h),Q(-h)]]
a=Q(-1,1); c=Q(1,1); z=Q(0); t=Q(2)
N=[[a,c,z],[t,a,z],[z,t,a],[c,z,a],[a,z,t],[z,a,c],[Q(-1)]*3]
B=[Q(-Fr(5,2),-h),Q(-Fr(3,2),-h),Q(-Fr(3,2),-h),Q(-Fr(5,2),-h),Q(-Fr(3,2),-h),Q(-Fr(5,2),-h),Q(Fr(7,4),Fr(3,4))]
S=[[B[m]-dot(N[m],P[k]) for k in range(7)] for m in range(7)]
print("slack");
for m in range(7): print(m,S[m],[s.sign() for s in S[m]])
assert all(s.sign()>=0 for row in S for s in row)
E=[(0,1,0,1),(0,2,0,2),(3,1,0,3),(5,2,0,4),(3,4,0,5),(5,4,0,6),(6,0,1,2),(6,3,3,5),(6,5,4,6),(1,6,1,3),(2,6,2,4),(4,6,5,6)]
for (i,j,k,l) in E:
    assert S[i][k]==0 and S[i][l]==0 and S[j][k]==0 and S[j][l]==0
    d2=sum(((P[k][x]-P[l][x])*(P[k][x]-P[l][x]) for x in range(3)),Q(0))
    print("edge",i,j,k,l,"len2",d2,"gram",dot(N[i],N[i]),dot(N[j],N[j]),dot(N[i],N[j]))
    for m in range(7):
        if m not in (i,j): assert S[m][k].sign()>0 or S[m][l].sign()>0
epairs={frozenset((i,j)):e for e,(i,j,k,l) in enumerate(E)}
out=[]
for i in range(7):
  for j in range(i+1,7):
    fs=frozenset((i,j))
    if fs in epairs:
        e=epairs[fs]; _,_,k,l=E[e]
        cs=[cc for cc in range(7) if cc not in (i,j) and S[cc][l]==0 and S[cc][k].sign()>0 and det(N[i],N[j],N[cc])!=0]
        cps=[cc for cc in range(7) if cc not in (i,j) and S[cc][k]==0 and S[cc][l].sign()>0]
        cc=cs[0]; cp=cps[0]
        print("EDGE",i,j,"e",e,"k,l",k,l,"c",cc,"c'",cp,"det",det(N[i],N[j],N[cc]))
    else:
        found=None
        for cc in range(6):
          if cc in (i,j) or det(N[i],N[j],N[cc])==0: continue
          for cp in range(6):
            if cp in (i,j,cc): continue
            # N[cc] = a N[i] + a' N[j] - mu N[cp]
            M=[[N[i][r],N[j][r],N[cp][r]] for r in range(3)]
            sol=solve3(M,N[cc])
            if sol is None: continue
            # solve3 solves rows*x = rhs with Cramer on columns; verify
            ok=all(sum((M[r][s]*sol[s] for s in range(3)),Q(0))==N[cc][r] for r in range(3))
            assert ok
            mu=-sol[2]
            if mu.sign()>0:
                found=(cc,cp,mu,sol[0],sol[1]); break
          if found: break
        print("NONEDGE",i,j,found,"det",det(N[i],N[j],N[found[0]]))
# bounds
for k in range(3):
  for sg in (1,-1):
    tgt=[Q(sg if r==k else 0) for r in range(3)]
    best=None
    for tri in itertools.combinations(range(7),3):
        M=[[N[m][r] for m in tri] for r in range(3)]
        if det(*M)==0: continue
        sol=solve3(M,tgt)
        if all(s.sign()>=0 for s in sol):
            U=sum((sol[t]*B[tri[t]] for t in range(3)),Q(0))
            cplx=sum(abs(s.a.denominator)+abs(s.b.denominator)+abs(s.a.numerator)+abs(s.b.numerator) for s in sol)
            if best is None or cplx<best[0]: best=(cplx,tri,sol,U)
    print("BOUND",k,sg,best[1],best[2],"U",best[3],best[3].f())
