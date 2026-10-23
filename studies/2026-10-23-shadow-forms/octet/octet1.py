# DICTO 10-23: 'can we do something similar with tetrahedron, octahedron, cube?' The octet (regular tetrahedra + octahedra, edge √2,
# vertices on the fcc lattice of a cube of side 2) split like the golden split: every tetrahedron and octahedron is a union of cones
# from its centre over its faces; each shared face's double cone (tetra centre -> face <- octa centre) is cut by a plane parallel to
# the face at fraction t from the tetra centre. t = 1/3 gives back the octet; t = 0 gives the octahedra everything, t = 1 the tetrahedra.
# Computed as a power diagram (weights make the cut planes), so every piece is convex.
import numpy as np, itertools, sys, json
from scipy.spatial import ConvexHull, HalfspaceIntersection
O=[np.array(p,float) for p in [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]]          # octahedron centres per cube (octahedral holes)
Tc=[np.array(p,float)/2 for p in itertools.product((1,3),repeat=3)]         # tetrahedron centres (1/2,1/2,1/2)+...
d=np.sqrt(3)/2
def sites(R=2):
    S=[]
    for c in itertools.product(range(-R,R+1),repeat=3):
        o=np.array(c)*2.0
        S+=[('O',p+o) for p in O]+[('T',p+o) for p in Tc]
    return S
S=sites()
def cell(kind,c,t):
    w={'O':0.0,'T':d*d*(2*t-1)}
    hs=[]
    for k2,c2 in S:
        if np.allclose(c2,c) or np.linalg.norm(c2-c)>2.2: continue
        n=c2-c; off=(np.dot(c2,c2)-np.dot(c,c)-w[k2]+w[kind])/2   # p·n <= off
        hs.append(np.r_[n,-off])
    hs=np.array(hs)
    try:
        hi=HalfspaceIntersection(hs,c.copy()); V=hi.intersections
        V=V[ConvexHull(V).vertices]; return V
    except Exception: return None
def describe(V):
    h=ConvexHull(V); N=[]
    for e in h.equations:
        if not any(np.dot(e[:3],q[:3])>1-1e-7 for q in N): N.append(e)
    from collections import Counter
    fk=Counter(int((np.abs(V@q[:3]+q[3])<1e-7).sum()) for q in N)
    E=sorted(set(np.round([np.linalg.norm(a-b) for a,b in itertools.combinations(V,2)],4)))
    return len(V),len(N),dict(sorted(fk.items())),h.volume
ts=[float(a) for a in sys.argv[1:]] or [0.02,0.1,0.2,0.3,1/3,0.4,0.5,0.6,0.7,0.8,0.9,0.98]
for t in ts:
    row=[]
    for kind,c in [('T',Tc[0]),('O',O[0])]:
        V=cell(kind,c,t)
        if V is None or len(V)<4: row.append('%s: none'%kind); continue
        n,f,fk,vol=describe(V); row.append('%s: %d corners, %d faces %s, vol %.4f'%(kind,n,f,fk,vol))
    print('t=%.4f  '%t+'  |  '.join(row),flush=True)
