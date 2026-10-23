# Golden split check: faces of both padded pieces by merging hull facets with the same normal; then a point test of the
# two-piece fill using the convex hulls only (padded icosahedra at lattice points, padded Unborns at body centres).
import numpy as np, json, itertools
from scipy.spatial import ConvexHull
from collections import Counter
phi=(1+5**.5)/2; h=phi/2
for nm in ['icosahedron','Unborn']:
    V=np.array(json.load(open('golden-%s.json'%nm))); hl=ConvexHull(V); V=V[hl.vertices]; hl=ConvexHull(V)
    N=[]
    for e in hl.equations:
        if not any(np.dot(e[:3],n[:3])>1-1e-6 for n in N): N.append(e)
    fk=Counter()
    for q in N:
        on=V[np.abs(V@q[:3]+q[3])<1e-6]; c=on.mean(0); u=on[0]-c; u/=np.linalg.norm(u); w=np.cross(q[:3],u)
        on=on[np.argsort(np.arctan2((on-c)@w,(on-c)@u))]
        fk[(len(on),tuple(np.round([np.linalg.norm(on[i]-on[i-1]) for i in range(len(on))],4)))]+=1
    print(nm,'+ pyramids: corners',len(V),'faces',len(N),'edges',len(V)+len(N)-2); [print('   ',k,'x',v) for k,v in fk.items()]
    globals()['E_'+nm]=hl.equations
rs=np.random.default_rng(9); P=rs.random((500000,3))*2*phi
inside=lambda Q,E:(Q@E[:,:3].T+E[:,3]<=1e-9).all(1)
tot=np.zeros(len(P),int)
for c in itertools.product(range(-1,4),repeat=3):
    o=np.array(c)*phi; tot+=inside(P-o,E_icosahedron); tot+=inside(P-o,E_Unborn)
print('point test (500k points): uncovered %d, doubled %d'%((tot==0).sum(),(tot>1).sum()))
