# Swept dodecahedra as a space filler, positive search, step 1 (DICTO 10-22 idea; started 10-23).
# Dodecahedra of edge 1 on alternate cells of the cube grid of edge φ (cells (a,b,c), a+b+c even, centre φ(a,b,c)), as in #42.
# Pair every dodecahedron with its diagonal neighbour (a,b,c) <-> (a+1,b+1,c) for a even; replace each pair by the swept dodecahedron
# (hull of the two). Check: swept pieces disjoint? what fraction of space do they fill? what is left?
import numpy as np, itertools
from scipy.spatial import ConvexHull
phi=(1+5**.5)/2
D=np.array([(x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)])*phi/2
D=np.vstack([D]+[np.array([[0,s1*0.5,s2*phi**2/2],[s1*0.5,s2*phi**2/2,0],[s2*phi**2/2,0,s1*0.5]]) for s1 in (1,-1) for s2 in (1,-1)])
assert len(D)==20
e=sorted(set(np.round([np.linalg.norm(a-b) for a,b in itertools.combinations(D,2)],6)))[0]; print('dodecahedron edge',e,'volume %.6f'%ConvexHull(D).volume)
sweep=np.array([phi,phi,0])
S=np.vstack([D,D+sweep]); hS=ConvexHull(S); ES=hS.equations; ED=ConvexHull(D).equations
print('swept piece volume %.6f = 2 dodecahedra %.6f + %.6f'%(hS.volume,2*ConvexHull(D).volume,hS.volume-2*ConvexHull(D).volume))
inside=lambda Q,E:(Q@E[:,:3].T+E[:,3]<=1e-9).all(1)
# period: cells with a even and a+b+c even give the swept pieces; lattice of first members: (2i, j, k) with j+k even
rs=np.random.default_rng(2); N=400000; L=2*phi
P=rs.random((N,3))*np.array([2*phi,2*phi,2*phi])
cnt=np.zeros(N,int); inD=np.zeros(N,int)
for a in range(-3,4):
    for b in range(-3,4):
        for c in range(-3,4):
            if (a+b+c)%2: continue
            o=np.array([a,b,c])*phi
            inD+=inside(P-o,ED)
            if a%2==0: cnt+=inside(P-o,ES)
print('points in 2+ swept pieces: %d   in dodecahedra: %.4f   in swept pieces: %.4f   left over: %.4f'%((cnt>1).sum(),(inD>0).mean(),(cnt>0).mean(),(cnt==0).mean()))
np.save('leftover-pts.npy',P[cnt==0])
