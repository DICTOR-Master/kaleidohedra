"""Where two of the five central truncated octahedra (slices x_i = 3, the middle value) cross: the 4D permutohedron cut by the central
plane x_i = x_j = 3. The plane meets no corner or edge, so the polygon's corners are where it pierces 2-faces. Exact (fractions);
membership by majorization (x lies in the permutohedron iff sum 0 and every k largest entries sum to at most the k largest values)."""
import itertools
from fractions import Fraction as F
vals=[-2,-1,0,1,2]
def inside(x):
    s=sorted(x,reverse=True); return sum(x)==0 and all(sum(s[:k])<=sum(sorted(vals,reverse=True)[:k]) for k in range(1,5))
V=[tuple(x-3 for x in p) for p in itertools.permutations(range(1,6))]
# every 2-face as 3 affine-independent corners spanning its plane (hexagon: values k..k+2 permuted; square: two swaps)
idx=set(V); faces=set()
for p in V:
    for k in (-2,-1,0):
        pos=[i for i in range(5) if p[i] in (k,k+1,k+2)]
        pts=[]
        for perm in itertools.permutations((k,k+1,k+2)):
            q=list(p)
            for t,i in enumerate(pos): q[i]=perm[t]
            pts.append(tuple(q))
        faces.add(frozenset(pts))
    for a,b in itertools.combinations(range(-2,2),2):
        if b<=a+1: continue
        pts=[]
        for s1,s2 in itertools.product((0,1),repeat=2):
            q=list(p)
            if s1: q=[a+1 if x==a else a if x==a+1 else x for x in q]
            if s2: q=[b+1 if x==b else b if x==b+1 else x for x in q]
            pts.append(tuple(q))
        faces.add(frozenset(pts))
I,J=0,1; hits=set()
for f in faces:
    f=sorted(f); o=f[0]; d1=[y-x for x,y in zip(o,f[1])]
    d2=next([y-x for x,y in zip(o,g)] for g in f[2:] if any(a*b2!=a2*b for a,b,a2,b2 in [(d1[0],d1[1],0,0)]) or True)
    # pick d2 independent of d1
    for g in f[2:]:
        d2=[y-x for x,y in zip(o,g)]
        if any(d1[r]*d2[s]-d1[s]*d2[r] for r in range(5) for s in range(5)): break
    # solve o + s d1 + t d2 with coordinates I, J zero
    A=[[F(d1[I]),F(d2[I])],[F(d1[J]),F(d2[J])]]; bb=[F(-o[I]),F(-o[J])]
    det=A[0][0]*A[1][1]-A[0][1]*A[1][0]
    if det==0: continue
    s=(bb[0]*A[1][1]-A[0][1]*bb[1])/det; t=(A[0][0]*bb[1]-bb[0]*A[1][0])/det
    x=tuple(F(a)+s*b+t*c for a,b,c in zip(o,d1,d2))
    if inside(x): hits.add(x)
P=sorted(hits); print('corners of the crossing polygon:',len(P),[tuple(int(v) if v.denominator==1 else str(v) for v in p) for p in P])
import math
c=lambda p:(float(p[2]-p[3])/math.sqrt(2), float(p[2]+p[3]-2*p[4])/math.sqrt(6))
Q=sorted(P,key=lambda p:math.atan2(c(p)[1],c(p)[0]))
print('sides^2:',[str(sum((x-y)**2 for x,y in zip(Q[k],Q[(k+1)%len(Q)]))) for k in range(len(Q))],' radius^2:',sorted(set(str(sum(v*v for v in p)) for p in P)))
# the polygon must be the whole section: test a ring of points just outside each side midpoint
out=[tuple(F(11,10)*(a+b)/2 for a,b in zip(Q[k],Q[(k+1)%len(Q)])) for k in range(len(Q))]
print('PASS section closed' if not any(inside(x) for x in out) and all(inside(tuple(F(9,10)*(a+b)/2 for a,b in zip(Q[k],Q[(k+1)%len(Q)]))) for k in range(len(Q))) else 'FAIL')
