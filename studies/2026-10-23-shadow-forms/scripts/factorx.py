# DICTO's 'factor x': Koca's truncated octahedron T(x) = orbit of (1+x, x, 0) (all permutations, signs). Pair T(x) at the points of
# Lℤ³ with T(1/x) at the cube centres, scaled so both reach the cube faces' midplanes (square at distance L/2). Point test for many x.
import numpy as np, itertools
from scipy.spatial import ConvexHull
def T(x,s): return np.array(sorted({tuple(sg[k]*perm[k]*s for k in range(3)) for perm in itertools.permutations((1+x,x,0)) for sg in itertools.product((1,-1),repeat=3)}))
L=2.0; rs=np.random.default_rng(4); P=rs.random((300000,3))*L
inside=lambda Q,E:(Q@E[:,:3].T+E[:,3]<=1e-9).all(1)
for x in [0.3,0.5,1/((1+5**.5)/2),0.8,1.0,1.25,(1+5**.5)/2,2.0,3.0]:
    A=T(x,L/(2*(1+x))); B=T(1/x,L/(2*(1+1/x))); EA,EB=ConvexHull(A).equations,ConvexHull(B).equations
    tot=np.zeros(len(P),int)
    for c in itertools.product(range(-1,3),repeat=3):
        o=np.array(c)*L; tot+=inside(P-o,EA); tot+=inside(P-o-L/2,EB)
    va,vb=ConvexHull(A).volume,ConvexHull(B).volume
    print('x=%.4f: T(x) vol %.4f + T(1/x) vol %.4f = %.4f (cell %.1f)  uncovered %d doubled %d  corners %d/%d'%(x,va,vb,va+vb,L**3,(tot==0).sum(),(tot>1).sum(),len(ConvexHull(A).vertices),len(ConvexHull(B).vertices)))
