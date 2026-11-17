# Vacuus plates of the fair die (#110 definitions, centre O = origin) and which lie on the cube's walls (Oh mirrors;
# the cube's cross walls are its coordinate planes, already mirrors). Exact: corners in Z[b], plate normals = cross products.
import itertools, sympy as sp
b=sp.symbols("b",positive=True)  # b_f = 0.75658..., root of b^6-18b^4-4b^2+8 (fair-die-full step 1)
V=set()
for p in itertools.permutations([1,b,0]):
    for s in itertools.product([1,-1],repeat=3): V.add(tuple(sp.expand(s[i]*p[i]) for i in range(3)))
V=[sp.Matrix(v) for v in V]; R2=float((1+b**2).subs(b,0.7565821359)); el2=2*0.7565821359**2; e22=2*(1-0.7565821359)**2
num=lambda e: float(e.subs(b,0.7565821359450421))
E=[]
for i in range(len(V)):
    for j in range(i+1,len(V)):
        d=num((V[i]-V[j]).dot(V[i]-V[j]))
        if abs(d-el2)<1e-9 or abs(d-e22)<1e-9:
            # edge iff midpoint is on boundary and segment is an edge: check by the two known edge lengths and adjacency in perms
            E.append((i,j,'sq-hex' if abs(d-el2)<1e-9 else 'hex-hex'))
# keep true edges: endpoints share a face plane; faces x_k=+-1 and +-x+-y+-z=mu
def onface(v,n,h): return abs(num(n.dot(v))-h)<1e-9
mu=1+0.7565821359450421
F=[(sp.Matrix([1 if k==m else 0 for k in range(3)])*s,1) for m in range(3) for s in (1,-1)]+[(sp.Matrix(s),mu) for s in itertools.product([1,-1],repeat=3)]
E=[e for e in E if sum(onface(V[e[0]],n,h) and onface(V[e[1]],n,h) for n,h in F)==2]
print('edges',len(E),{k:sum(1 for e in E if e[2]==k) for k in ('sq-hex','hex-hex')})
planes={}
for i,j,k in E:
    n=V[i].cross(V[j]); n=n/sp.sqrt(n.dot(n)); n=sp.simplify(n)
    key=tuple(round(abs(num(c)),9) for c in n)  # up to sign: normalise sign
    nn=[num(c) for c in n]; s=next(x for x in nn if abs(x)>1e-12); key=tuple(round(x/abs(s)*(1 if s>0 else -1)*abs(s),9) for x in nn)
    planes.setdefault(key,[]).append(k)
mir=[(1,0,0),(0,1,0),(0,0,1)]+[(1,s,0) for s in (1,-1)]+[(1,0,s) for s in (1,-1)]+[(0,1,s) for s in (1,-1)]
import math
def onwall(n): return any(abs(abs(sum(a*c for a,c in zip(n,m)))/math.sqrt(sum(c*c for c in m))-1)<1e-9 for m in mir)
w=sum(1 for k in planes if onwall(k))
print('plates',len(planes),'edges per plate',sorted(set(len(v) for v in planes.values())),'on cube walls',w)
for k,v in planes.items(): print(k,v,'WALL' if onwall(k) else '')
ok=len(E)==36 and len(planes)==15 and w==3
print('FINAL ok' if ok else 'FINAL FAIL')
