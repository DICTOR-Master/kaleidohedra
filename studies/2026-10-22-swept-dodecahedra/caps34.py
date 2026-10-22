# DICTO 10-22: three and four caps. Dodecahedra (edge 1) on cubes of the dodecahedron layer whose centres are
# pairwise face-diagonal neighbours (distance phi*sqrt2): three make an equilateral triangle, four a regular
# tetrahedron. Their hull = the dodecahedron swept over that triangle / tetrahedron. Faces counted by kind.
import numpy as np, math
from collections import Counter
from scipy.spatial import ConvexHull
import mixes3 as M, pieces_figure as PF
phi=M.phi
cells={'triangle':[(0,0,0),(1,1,0),(1,0,1)],'tetrahedron':[(0,0,0),(1,1,0),(1,0,1),(0,1,1)]}
def describe(V):
    F=PF.hull_faces(V); c=Counter()
    for f in F:
        f=np.array(f); n=len(f); L=sorted({round(np.linalg.norm(f[i]-f[(i+1)%n]),3) for i in range(n)})
        a=sorted({round(math.degrees(math.acos(np.clip((f[i-1]-f[i])@(f[(i+1)%n]-f[i])/np.linalg.norm(f[i-1]-f[i])/np.linalg.norm(f[(i+1)%n]-f[i]),-1,1)))) for i in range(n)})
        c[(n,tuple(L),tuple(a))]+=1
    return F,c
for name,cs in cells.items():
    for s,label in ((phi*2**.5,'touching corners (spacing φ√2)'),(1.0,'equilateral (spacing 1)')):
        P=[np.array(x,float)*phi for x in cs]; P=[p/np.linalg.norm(P[1]-P[0])*s for p in P]
        V=np.vstack([M.DOD+p for p in P]); F,c=describe(V)
        print(f'{name}, {label}: {len(F)} faces, volume {ConvexHull(V).volume:.4f}')
        for k,v in sorted(c.items()): print('   ',v,'x',k[0],'-gon, edges',k[1],'angles',k[2])
