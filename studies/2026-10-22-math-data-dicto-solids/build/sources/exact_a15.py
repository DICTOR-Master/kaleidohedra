# Exact power cells of A15 (cubic cell edge 2; Si at 000, 111; Cr at the six face-chain sites) at lambda = w_Si - w_Cr = 3/4.
# Rational arithmetic (Fraction): every corner = intersection of three bisector planes satisfying all others. Checks: corner/face/edge
# counts, edge lengths^2, volumes, 2*V_Si + 6*V_Cr = 8, corners of the Si cell = which sites.
from fractions import Fraction as F
import itertools
lam=F(3,4)
Si=[(0,0,0),(1,1,1)]; Cr=[(F(1,2),0,1),(F(3,2),0,1),(1,F(1,2),0),(1,F(3,2),0),(0,1,F(1,2)),(0,1,F(3,2))]
sites=[]
for t in itertools.product(range(-2,3),repeat=3):
    T=[2*c for c in t]
    sites+=[(tuple(F(T[i])+s[i] for i in range(3)),lam,'Si') for s in Si]+[(tuple(F(T[i])+c[i] for i in range(3)),F(0),'Cr') for c in Cr]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def det3(m): return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
def solve(A,b):
    D=det3(A)
    if D==0: return None
    out=[]
    for k in range(3):
        M=[list(r) for r in A]
        for i in range(3): M[i][k]=b[i]
        out.append(det3(M)/D)
    return tuple(out)
def cell(p,wp,R2=6):
    P=[]
    for q,wq,_ in sites:
        d=sub(q,p)
        if d==(0,0,0) or dot(d,d)>R2: continue
        P.append((tuple(2*x for x in d), dot(q,q)-dot(p,p)-wq+wp))   # 2d.x <= c
    V=set()
    for a,b,c in itertools.combinations(P,3):
        x=solve([a[0],b[0],c[0]],[a[1],b[1],c[1]])
        if x is None: continue
        if all(dot(n,x)<=r for n,r in P): V.add(x)
    V=list(V)
    faces=[]
    for n,r in P:
        on=[v for v in V if dot(n,v)==r]
        if len(on)>=3: faces.append((n,on))
    return V,faces
def stats(name,V,faces):
    E=set()
    for (n1,f1),(n2,f2) in itertools.combinations(faces,2):
        sh=set(f1)&set(f2)
        if len(sh)==2: E.add(frozenset(sh))
    L2=sorted({dot(sub(*tuple(e)),sub(*tuple(e))) for e in E})
    # volume: sum over faces of cone from centroid
    c=tuple(sum(v[i] for v in V)/len(V) for i in range(3))
    vol=F(0)
    for n,f in faces:
        # order face points around face centroid using a fan by angle is not rational; use triangle fan via convex sorting with cross products
        fc=tuple(sum(v[i] for v in f)/len(f) for i in range(3))
        pts=list(f)
        # sort by comparator using cross product sign relative to normal
        import functools
        def cmp(a,b):
            u=sub(a,fc); w=sub(b,fc)
            cr=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
            s=dot(cr,n)
            return -1 if s>0 else (1 if s<0 else 0)
        # half-plane split to make comparator transitive
        ref=sub(pts[0],fc)
        def half(a):
            u=sub(a,fc); cr=(ref[1]*u[2]-ref[2]*u[1],ref[2]*u[0]-ref[0]*u[2],ref[0]*u[1]-ref[1]*u[0]); s=dot(cr,n)
            return 0 if (s>0 or (s==0 and dot(u,ref)>0)) else 1
        pts.sort(key=functools.cmp_to_key(lambda a,b: (half(a)-half(b)) or cmp(a,b)))
        for i in range(1,len(pts)-1):
            a,b,d=sub(pts[0],c),sub(pts[i],c),sub(pts[i+1],c)
            vol+=abs(det3([a,b,d]))/6
    print(name,'corners',len(V),'faces',len(faces),'face sizes',sorted(len(f) for n,f in faces),'edges',len(E),'edge^2',L2,'volume',vol)
    return vol
V,f=cell(Si[0],lam); vs=stats('Si (Goliath)',V,f)
cs={v for v in V}; crs={q for q,w,k in sites if k=='Cr'}
print('  Si corners that are Cr sites:',len(cs&crs),'of',len(V))
V2,f2=cell(Cr[0],F(0)); vc=stats('Cr (David)',V2,f2)
print('  David corners:',sorted(V2))
print('2*V_Si + 6*V_Cr =',2*vs+6*vc,'(cube of edge 2 = 8):', 2*vs+6*vc==8)
# Goliath's corners vs Jessen's vertex set (0, ±1/2, ±1) and its cyclic permutations
J=set()
for a,b in itertools.product([F(1,2),F(-1,2)],[F(1),F(-1)]):
    for v in [(0,a,b),(b,0,a),(a,b,0)]: J.add(tuple(F(x) for x in v))
print('Goliath corners = Jessen set (0,±1/2,±1) cyclic:', set(V)==J)
