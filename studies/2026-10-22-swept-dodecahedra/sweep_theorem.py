# #49 Swept Dodecahedra (DICTO's idea): the regular dodecahedron (edge 1) swept along a segment of length 1.
# Checks: (1) for random directions, every edge of the hull is 1 (equilateral) and the faces are the dodecahedron's
# pentagons, stretched to hexagons where a face is parallel to the sweep, plus one parallelogram (rhombus) per
# silhouette edge; (2) the special directions: cube axis (F11), face diagonal, body diagonal, five-fold axis.
import numpy as np, math
from collections import Counter
from scipy.spatial import ConvexHull
import mixes3 as M, pieces_figure as PF
phi=M.phi; DOD=M.DOD
def faces(V): return PF.hull_faces(V)
def summary(u,s=1.0):
    u=np.array(u,float); u/=np.linalg.norm(u); F=faces(np.vstack([DOD,DOD+s*u]))
    E=[np.linalg.norm(np.array(f[i])-np.array(f[(i+1)%len(f)])) for f in F for i in range(len(f))]
    return Counter(len(f) for f in F), min(E), max(E), len(F)
rs=np.random.default_rng(7); bad=0; kinds=Counter()
for _ in range(2000):
    c,mn,mx,n=summary(rs.normal(size=3))
    if abs(mn-1)>1e-9 or abs(mx-1)>1e-9: bad+=1
    kinds[tuple(sorted(c.items()))]+=1
print('random directions: 2000, not equilateral:',bad)
print('face types seen (n-gon: count) -> how often:'); [print('  ',k,'x',v) for k,v in kinds.most_common()]
for name,u in [('cube axis (F11)',(1,0,0)),('face diagonal',(1,1,0)),('body diagonal (three-fold)',(1,1,1)),('five-fold axis',(0,1,phi)),('edge midpoint (two-fold, not cube axis)',(phi, 1/phi, 1))]:
    c,mn,mx,n=summary(u); print(f'{name}: {n} faces {dict(sorted(c.items()))}, edges {mn:.6f}..{mx:.6f}')
