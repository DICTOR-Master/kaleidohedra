# More caps for #49 (DICTO 10-22): every Platonic solid P (edge 1) placed at the corners of every Platonic solid Q (edge 1)
# and wrapped (the convex hull = Minkowski sum P ⊕ Q). Standard frames (the Euclid-cube frame of #47 and ring1.py),
# then Q turned 90° about z where edges run parallel. Prints face counts and the edge range (equal-edged when 1..1).
import numpy as np
import itertools, math
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
ALL=dict(SOL); ALL['dodecahedron']=scale1(M.DOD)
N={'tetrahedron':4,'cube':8,'octahedron':6,'icosahedron':12,'dodecahedron':20}
Rz=np.array([[0,-1,0],[1,0,0],[0,0,1.]])
for p,P in ALL.items():
    for q,Q in ALL.items():
        for tag,QQ in (('',Q),(' (turned)',Q@Rz.T)):
            c,n,mn,mx=kinds(np.vstack([P+v for v in QQ]))
            print(f'{p} at the {N[q]} corners of a{"n" if q[0] in "aeio" else ""} {q}{tag}: {n} faces = {fmt(c)}; edges {mn:.3f}..{mx:.3f}{"  EQUAL" if abs(mn-1)<1e-9 and abs(mx-1)<1e-9 else ""}')
            if abs(mx-1)<1e-9 and abs(mn-1)<1e-9: break
# the cube's edges run along the icosahedron's and dodecahedron's in the Euclid-cube frame: turn the cube instead
def rot(ax,a):
    ax=np.array(ax,float)/np.linalg.norm(ax); K=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
    return np.eye(3)+math.sin(a)*K+(1-math.cos(a))*K@K
print('-- cube turned against the icosahedron and dodecahedron')
for q in ('icosahedron','dodecahedron'):
    for tag,R in (('45° about a cube axis',rot((0,0,1),math.pi/4)),('60° about a body diagonal',rot((1,1,1),math.pi/3)),('the five-fold-compatible turn (cube of the compound of five)',rot((0,1,M.phi),2*math.pi/5))):
        c,n,mn,mx=kinds(np.vstack([ALL['cube']@R.T+v for v in ALL[q]]))
        print(f'cube turned {tag} at the corners of a{"n" if q[0]=="i" else ""} {q}: {n} faces = {fmt(c)}; edges {mn:.3f}..{mx:.3f}{"  EQUAL" if abs(mn-1)<1e-9 and abs(mx-1)<1e-9 else ""}')
