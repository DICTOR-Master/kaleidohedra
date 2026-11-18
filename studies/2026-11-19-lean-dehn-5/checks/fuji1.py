import json,sys
exec(open('q5.py').read())
d=json.loads(sys.stdin.read()) if False else None
V=[[-0.809016994, -0.809016994, -0.809016994], [-0.809016994, -0.809016994, -1.809016994], [-1.618033989, -0.5, -1.309016994], [-0.5, -1.309016994, -1.618033989], [-1.809016994, -0.809016994, -0.809016994], [-0.809016994, -1.809016994, -0.809016994], [-1.309016994, -1.618033989, -0.5]]
F=[[0, 1, 2], [0, 3, 1], [0, 2, 4], [0, 5, 3], [0, 6, 5], [0, 4, 6], [3, 5, 6, 4, 2, 1]]
P=[[snap(c) for c in v] for v in V]
print("P",P)
cen=[sum((p[i] for p in P),Q(0))/7 for i in range(3)]
N=[];B=[]
for f in F:
    n=cross(sub(P[f[1]],P[f[0]]),sub(P[f[2]],P[f[0]]))
    if (dot(n,cen)-dot(n,P[f[0]])).sign()>0: n=[-c for c in n]
    N.append(n);B.append(dot(n,P[f[0]]))
    print("face",f,"n",n,"b",dot(n,P[f[0]]),[ (dot(n,p)-dot(n,P[f[0]])).sign() for p in P])
for i in range(7):
  for j in range(i+1,7):
    X=dot(N[i],N[i]);Y=dot(N[j],N[j]);dd=-dot(N[i],N[j])
    com=[k for k in range(7) if k in F[i] and k in F[j]]
    c=dd.f()/math.sqrt(X.f()*Y.f())
    print(i,j,"common",com,"X",X,"Y",Y,"d",dd,"angle",math.degrees(math.acos(c)), "len", math.sqrt(sum((P[com[0]][t]-P[com[1]][t]).f()**2 for t in range(3))) if len(com)==2 else None)
for t in itertools.combinations(range(7),3):
    D=det(*[N[i] for i in t])
    if D==0: print("dependent triple",t)
