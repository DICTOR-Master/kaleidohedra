import itertools, numpy as np
from scipy.spatial import ConvexHull
phi=(1+5**0.5)/2
B=np.linalg.svd(np.eye(5)-np.ones((5,5))/5)[0][:,:4]   # basis of x1+..+x5=0
def pts(seed):
    P=np.array(sorted(set(itertools.permutations(seed))),float); P-=P.mean(1,keepdims=True); return P@B
def vacuus(seed,name):
    X=pts(seed); h=ConvexHull(X)
    fac={}
    for s,eq in zip(h.simplices,h.equations):
        k=tuple(np.round(eq,7)); fac.setdefault(k,set()).update(s)
    F=list(fac.values()); ridges=set()
    for a,b in itertools.combinations(F,2):
        I=sorted(a&b)
        if len(I)>=3:
            M=X[I]-X[I].mean(0)
            if np.linalg.matrix_rank(M,1e-7)==2: ridges.add(tuple(I))
    planes=set()
    for r in ridges:
        V=X[list(r)]
        if np.linalg.matrix_rank(V,1e-7)!=3: planes.add(('notcentral',r)); continue
        n=np.linalg.svd(V)[2][-1]; n=n/np.linalg.norm(n)
        if n[np.argmax(abs(n))]<0: n=-n
        planes.add(tuple(np.round(n,6)))
    nc=sum(1 for p in planes if p[0]=='notcentral')
    print(f"{name}: points {len(X)}, facets {len(F)}, ridges {len(ridges)}, central hyperplanes {len(planes)-nc}, ridges not spanning a hyperplane with the centre {nc}")
vacuus((1,2,3,4,5),"CONTROL permutohedron n=5 (#105: 150 ridges -> 65)")
vacuus((phi**2,phi**2,phi**2,phi,0),"golden 20-set")
vacuus((phi**2,phi**2,1,1,0),"golden 30-set")
