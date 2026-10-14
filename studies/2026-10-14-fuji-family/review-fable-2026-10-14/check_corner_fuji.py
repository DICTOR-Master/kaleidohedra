# Cube corner over the dictosphere's triangles (Fable review for DICTO, 2026-10-14).
# Solid: polyhedron A (faces at distance 1) intersected with polyhedron B (faces at distance s). The pyramid from A's corner over a
# B-face hexagon has equal side edges by symmetry; find s where its long faces (in A's face planes) are equilateral.
# DICTO · dictospheres.com
import numpy as np, itertools, math
from scipy.optimize import brentq
from scipy.spatial import HalfspaceIntersection
phi=(1+5**.5)/2
def solid(NA,NB,s):
    hs=[list(n)+[-1] for n in NA]+[list(n)+[-s] for n in NB]
    return HalfspaceIntersection(np.array(hs),np.zeros(3)).intersections
def test(NA,NB,cornerA,nB,s):
    X=np.unique(np.round(solid(NA,NB,s),9),axis=0)
    H=X[np.abs(X@nB-s)<1e-7]            # hexagon on face nB
    c=H.mean(0); o=np.argsort([math.atan2(*( (p-c)@np.c_[np.cross(nB,[0,0.3,1]),np.cross(nB,np.cross(nB,[0,0.3,1]))]).T[::-1]) for p in H]); H=H[o]
    sides=[np.linalg.norm(H[i]-H[(i+1)%6]) for i in range(6)]
    edges=[np.linalg.norm(cornerA-p) for p in H]
    return max(sides), min(sides), np.mean(edges), np.std(edges)
# cube + octahedron
NA=[s*np.eye(3)[i] for i in range(3) for s in (1,-1)]
NB=[np.array(v)/3**.5 for v in itertools.product((1,-1),repeat=3)]
f=lambda s: (lambda t: t[0]-t[2])(test(NA,NB,np.array([1,1,1.]),NB[0],s))
s=brentq(f,0.9,1.1); L,S,E,sd=test(NA,NB,np.array([1,1,1.]),NB[0],s)
print("cube/octahedron: equilateral long faces at s =",s,"(tangent solid s = 1 means equal distances; sqrt3/sqrt3 normalised)")
print("  r =",S/L,"(sqrt3-1)/2 =",(3**.5-1)/2,"side-edge spread",sd)
# algebra: hexagon on x+y+z = S (S = s*sqrt3) has long side sqrt2 (S-1) in the face x = 1; apex (1,1,1) to the corner (1, S-1, 0)
# is sqrt((2-S)^2 + 1). Equal when 2(S-1)^2 = (2-S)^2 + 1, i.e. S^2 = 3: exactly the equal-depth solid.
S=3**.5; print("algebra check:",2*(S-1)**2,(2-S)**2+1)
