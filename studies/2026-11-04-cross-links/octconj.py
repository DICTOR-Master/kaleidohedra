# min over v of inradius(conv(O v))/|v|, O = chiral octahedral rotation group (24)
import numpy as np, itertools
from scipy.spatial import ConvexHull
G=[]
for p in itertools.permutations(range(3)):
    for s in itertools.product([1,-1],repeat=3):
        M=np.zeros((3,3))
        for i in range(3): M[i,p[i]]=s[i]
        if abs(np.linalg.det(M)-1)<1e-9: G.append(M)
G=np.array(G); assert len(G)==24
def ratio(v):
    v=v/np.linalg.norm(v); P=G@v; h=ConvexHull(P)
    return (-h.equations[:,3]).min()
rng=np.random.default_rng(1); best=(9,None)
for _ in range(200000):
    v=rng.normal(size=3); r=ratio(v)
    if r<best[0]: best=(r,v/np.linalg.norm(v))
print('min ratio',best, '1/sqrt3=',1/np.sqrt(3))
for v in ([1,0,0],[1,1,1],[1,1,0]): print(v,ratio(np.array(v,float)))
