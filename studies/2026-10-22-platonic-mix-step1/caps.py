# The icosahedron (edge 1) in Pacioli's position inside the octahedron of edge L = phi^2/sqrt2 (vertices on the
# octahedron's edges at the golden section); the octahedron minus the icosahedron = DICTO's Admiral Caps (F21).
import itertools, numpy as np
from scipy.spatial import ConvexHull
phi=(1+5**.5)/2; L=phi**2/2**.5
ICO=np.array([p for a in (1,-1) for b in (phi,-phi) for p in [(0,a,b),(a,b,0),(b,0,a)]])/2      # edge 1
OCT=np.vstack([np.eye(3),-np.eye(3)])*phi**2/2                                               # edge L
assert np.allclose(np.abs(ICO).sum(1),phi**2/2)            # icosahedron corners on the octahedron's surface
d=[np.linalg.norm(a-b) for a,b in itertools.combinations(ICO,2)]; assert abs(min(d)-1)<1e-12
assert abs(np.linalg.norm(OCT[0]-OCT[1+1])-L)<1e-12
# caps: points of octa \ ico grouped by the nearest octahedron... find components by sampling
rs=np.random.default_rng(0); X=rs.uniform(-1.4,1.4,(400000,3))
inO=np.abs(X).sum(1)<phi**2/2
hi=ConvexHull(ICO); inI=np.all(X@hi.equations[:,:3].T+hi.equations[:,3]<0,axis=1)
G=X[inO&~inI]
# label each gap point by the icosahedron edge-pair it lies over: nearest octahedron edge midpoint
mids=np.array([(a+b)/2 for a,b in itertools.combinations(OCT,2) if abs(np.linalg.norm(a-b)-L)<1e-9])
lab=np.argmin(((G[:,None,:]-mids[None])**2).sum(-1),1)
print('octahedron edges', len(mids), 'gap points by edge', np.bincount(lab,minlength=12))
# by nearest octahedron vertex instead
labv=np.argmin(((G[:,None,:]-OCT[None])**2).sum(-1),1); print('by vertex', np.bincount(labv,minlength=6))
Vo=(2**.5/3)*L**3; Vi=5*phi**2/6   # icosahedron of edge 1 (was /12: wrong); print('V_oct',Vo,'V_ico',Vi,'gap',Vo-Vi,'per cap (6)',(Vo-Vi)/6)
