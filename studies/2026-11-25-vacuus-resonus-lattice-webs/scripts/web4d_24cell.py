# Lead 4 (exact): the 24-cell as the Voronoi cell of D4 = {x in Z^4 : sum even}.
# Checks: (a) Vacuus (hyperplanes through the centre and each 2-face) = Resonus (centre, parallel to facets) = the 12 root hyperplanes;
# (b) Theorem 0 data k = 2h/d per family; (c) web = {r.x in Z}, the affine D4 (D~4) arrangement; regions per cell = |W(D4)| = 192.
from fractions import Fraction as F
from itertools import permutations, product, combinations
def dot(u,v): return sum(a*b for a,b in zip(u,v))
V=set()
for p in set(permutations((1,0,0,0))):
    for s in (1,-1): V.add(tuple(s*x for x in p))
for s in product((F(1,2),F(-1,2)),repeat=4): V.add(s)
V=sorted(V); assert len(V)==24
roots=sorted({tuple(v) for v in (tuple(a*(i==k)+b*(j==k) for k in range(4)) for i,j in combinations(range(4),2) for a in (1,-1) for b in (1,-1))})
assert len(roots)==24
# cell = {x : |r.x| <= 1 for all roots}; every vertex on the boundary, max r.x over vertices = 1 (half-width h=1)
assert all(max(abs(dot(r,v)) for r in roots)==1 for v in V)
h=max(dot(roots[0],v) for v in V); assert h==1
E=[(a,b) for a,b in combinations(V,2) if dot([x-y for x,y in zip(a,b)],[x-y for x,y in zip(a,b)])==1]
T=[t for t in combinations(V,3) if all(((t[i],t[j]) in E or (t[j],t[i]) in E) for i,j in ((0,1),(0,2),(1,2)))]
# 2-faces: triangles lying in a facet r.x=1
T=[t for t in T if any(all(dot(r,v)==1 for v in t) for r in roots)]
print("vertices",len(V),"edges",len(E),"2-faces",len(T))
def null(rows):
    # exact 1-dim nullspace of three independent vectors in Q^4
    M=[list(map(F,r)) for r in rows]; piv=[]; r0=0
    for c in range(4):
        p=next((i for i in range(r0,len(M)) if M[i][c]!=0),None)
        if p is None: continue
        M[r0],M[p]=M[p],M[r0]; M[r0]=[x/M[r0][c] for x in M[r0]]
        for i in range(len(M)):
            if i!=r0 and M[i][c]!=0: M[i]=[a-M[i][c]*b for a,b in zip(M[i],M[r0])]
        piv.append(c); r0+=1
    free=[c for c in range(4) if c not in piv]; assert len(free)==1
    n=[F(0)]*4; n[free[0]]=F(1)
    for i,c in enumerate(piv): n[c]=-M[i][free[0]]
    return n
def canon(n):
    k=next(x for x in n if x!=0); m=[F(x)/F(k) for x in n]
    from math import lcm
    L=lcm(*[x.denominator for x in m]); return tuple(int(x*L) for x in m)
vac={canon(null(t)) for t in T}
res={canon(r) for r in roots}
print("Vacuus hyperplanes",len(vac),"Resonus hyperplanes",len(res),"equal",vac==res)
# layer spacing d along r: r.D4 = Z (values r.t, t in D4); gcd over generators
gens=[r for r in roots]  # roots generate D4
d=0
from math import gcd
for r in roots:
    vals={dot(r,t) for t in gens}; g=0
    for x in vals: g=gcd(g,int(x))
    assert g==1
print("each family: h =",h,"d = 1 -> k = 2h/d =",2*h,"(<= 2: continues, Theorem 0)")
# web = {r.x = c : c in Z} = affine D4 arrangement; inside one cell only r.x=0 cuts the interior (|r.x|<1), r.x=+-1 are facets.
# regions per cell = chambers of the 12 central hyperplanes = |W(D4)|: count sign vectors at exact generic points of the cell
import random; random.seed(1); seen=set()
for _ in range(200000):
    x=[F(random.randint(-999,999),1000) for _ in range(4)]
    if max(abs(dot(r,x)) for r in roots)>=1 or any(dot(r,x)==0 for r in roots): continue
    seen.add(tuple(dot(r,x)>0 for r in sorted(res)))
print("regions found in one cell",len(seen),"(|W(D4)| = 192; cell volume 2 = covolume of D4 -> one alcove each)")
