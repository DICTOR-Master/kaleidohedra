# Volumes of the connectors: closed forms (derived by hand with phi^2 = phi + 1) checked against direct
# computation (convex hulls; Monte Carlo for the non-convex caps) to the precision shown.
import numpy as np, itertools
from scipy.spatial import ConvexHull
phi=(1+5**.5)/2; r2=2**.5; L=phi**2/r2
ICO=np.array([p for a in (1,-1) for b in (phi,-phi) for p in [(0,a,b),(a,b,0),(b,0,a)]])/2
import mixes3 as M
vD=ConvexHull(M.DOD).volume; vI=ConvexHull(ICO).volume
roof=ConvexHull(M.ROOF[(2,1)]).volume
rows=[('icosahedron, edge 1','5φ²/6',5*phi**2/6,vI),
('dodecahedron, edge 1','2 + 7φ/2',2+3.5*phi,vD),
("Euclid's roof",'(1 + 3φ/2)/6',(1+1.5*phi)/6,roof),
('P, half octahedron','√2/6',r2/6,ConvexHull(np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1]])/r2).volume),
('Q, tetrahedron face pyramid','√2/48',r2/48,(r2/12)/4),
("Q', Q at size L = φ²/√2","φ⁶/96",phi**6/96,(r2/12)*L**3/4),
('A, one Admiral Cap','φ/12',phi/12,((r2/3)*L**3-vI)/6),
('S, Dogstar','φ/2',phi/2,phi**3-6*roof),
('X, cube of edge φ minus a roof','φ³ − (1 + 3φ/2)/6',phi**3-(1+1.5*phi)/6,phi**3-roof),
('Y, cube of edge φ plus a roof','φ³ + (1 + 3φ/2)/6',phi**3+(1+1.5*phi)/6,phi**3+roof)]
for name,form,closed,direct in rows:
    assert abs(closed-direct)<1e-9, name
    print(f'{name:34s} {form:22s} {closed:.10f}  (direct {direct:.10f})')
print('the six Admiral Caps together and the Dogstar both have volume φ/2 =',phi/2)
