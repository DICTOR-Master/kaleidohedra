# Ring 1 of #49 (DICTO 10-22): the Polyhedral Stretching Theorem for the other four Platonic solids (edge 1).
# For each: random unit stretches (equilateral? belt sizes), special directions, and three / four caps.
import numpy as np, itertools, math
from collections import Counter
import mixes3 as M, pieces_figure as PF
phi=M.phi
def scale1(V):
    V=np.array(V,float); d=min(np.linalg.norm(a-b) for a,b in itertools.combinations(V,2)); return V/d
cyc=lambda v:[v,(v[1],v[2],v[0]),(v[2],v[0],v[1])]
SOL={'tetrahedron':scale1([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]),
     'cube':scale1(list(itertools.product((-1,1),repeat=3))),
     'octahedron':scale1([s*e for e in np.eye(3) for s in (1,-1)]),
     'icosahedron':scale1([p for a in (1,-1) for b in (phi,-phi) for p in cyc((0,a,b))])}
def kinds(V):
    F=PF.hull_faces(V); E=[np.linalg.norm(np.array(f[i])-np.array(f[(i+1)%len(f)])) for f in F for i in range(len(f))]
    return Counter(len(f) for f in F),len(F),min(E),max(E)
fmt=lambda c:' + '.join(f"{v}×{ {3:'triangle',4:'quad',5:'pentagon',6:'hexagon',7:'heptagon',8:'octagon'}.get(k,str(k)+'-gon')}" for k,v in sorted(c.items()))
rs=np.random.default_rng(3)
for name,V in SOL.items():
    print('==',name)
    seen=Counter(); bad=0
    for _ in range(1000):
        u=rs.normal(size=3); u/=np.linalg.norm(u); c,n,mn,mx=kinds(np.vstack([V,V+u]))
        if abs(mn-1)>1e-9 or abs(mx-1)>1e-9: bad+=1
        seen[fmt(c)]+=1
    print('   random stretches: 1000, not equilateral:',bad,'| face sets:',dict(seen.most_common(3)))
    dirs={'(1,0,0)':(1,0,0),'(1,1,0)':(1,1,0),'(1,1,1)':(1,1,1)}
    if name=='icosahedron': dirs['five-fold (0,1,φ)']=(0,1,phi)
    for dn,u in dirs.items():
        u=np.array(u,float); u/=np.linalg.norm(u); c,n,mn,mx=kinds(np.vstack([V,V+u]))
        print(f'   along {dn}: {n} faces = {fmt(c)}; edges {mn:.3f}..{mx:.3f}')
    for cn,pts in (('three caps',[(0,0,0),(1,1,0),(1,0,1)]),('four caps',[(0,0,0),(1,1,0),(1,0,1),(0,1,1)])):
        P=[np.array(p,float)/2**.5 for p in pts]
        c,n,mn,mx=kinds(np.vstack([V+p for p in P])); print(f'   {cn}: {n} faces = {fmt(c)}; edges {mn:.3f}..{mx:.3f}')
