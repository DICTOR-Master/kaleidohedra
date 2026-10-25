# Power cells of the two strongest #53 stops (floats, cross-check only): A15 at lambda = 3/4, NaCl at lambda = 4 - 2*sqrt(3).
import numpy as np, itertools, json
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection, ConvexHull
def cell(p, wp, sites, R=4.0):
    H=[]
    for q,wq in sites:
        d=np.array(q)-np.array(p)
        if np.allclose(d,0) or np.linalg.norm(d)>R: continue
        # |x-p|^2 - wp <= |x-q|^2 - wq  <=>  2 d.x <= |q|^2-|p|^2 - wq + wp
        H.append(np.r_[2*d, -(np.dot(q,q)-np.dot(p,p)-wq+wp)])
    H=np.array(H); A=H[:,:3]; b=-H[:,3]
    n=np.linalg.norm(A,axis=1)
    r=linprog([0,0,0,-1],A_ub=np.c_[A,n],b_ub=b,bounds=[(None,None)]*3+[(0,None)])
    c=r.x[:3]
    hs=HalfspaceIntersection(H,c); V=hs.intersections
    V=np.unique(np.round(V,10),axis=0); hull=ConvexHull(V)
    return V,hull
def describe(V,hull,name):
    E=set()
    # merge coplanar triangles into faces
    eqs=np.round(hull.equations,8); faces={}
    for s,e in zip(hull.simplices,eqs): faces.setdefault(tuple(e),set()).update(s)
    deg={i:0 for i in range(len(V))}
    for f in faces.values():
        pts=list(f); 
        for i in pts: deg[i]+=1
    # edges: pairs sharing two faces
    fl=[set(f) for f in faces.values()]
    for a,b in itertools.combinations(range(len(fl)),2):
        sh=fl[a]&fl[b]
        if len(sh)==2: E.add(tuple(sorted(sh)))
    L=sorted(round(float(np.linalg.norm(V[i]-V[j])),6) for i,j in E)
    sizes=sorted(len(f) for f in faces.values())
    return dict(name=name,corners=len(V),faces=len(faces),face_sizes=sizes,edges=len(E),edge_lengths=sorted(set(L)),
                volume=round(float(hull.volume),8),corner_degrees=sorted(deg.values()))
out=[]
# A15, cubic cell edge 2
Si=[(0,0,0),(1,1,1)]; Cr=[(.5,0,1),(1.5,0,1),(1,.5,0),(1,1.5,0),(0,1,.5),(0,1,1.5)]
lam=0.75
sites=[]
for t in itertools.product(range(-3,4),repeat=3):
    T=2*np.array(t)
    sites+= [(tuple(T+s),lam) for s in Si]+[(tuple(T+c),0.0) for c in Cr]
for p,w,nm in [(Si[0],lam,'A15 Si cell at 3/4'),(Cr[0],0.0,'A15 Cr cell at 3/4')]:
    V,h=cell(p,w,sites); out.append(describe(V,h,nm))
# NaCl: fcc of edge-2 cube, Na at even-sum integer points, Cl at odd-sum points; lambda = w_Na - w_Cl
lam=4-2*np.sqrt(3); sites=[]
for x,y,z in itertools.product(range(-4,5),repeat=3):
    sites.append(((x,y,z), lam if (x+y+z)%2==0 else 0.0))
for p,w,nm in [((0,0,0),lam,'NaCl Na cell at 4-2r3'),((1,0,0),0.0,'NaCl Cl cell at 4-2r3')]:
    V,h=cell(p,w,sites); out.append(describe(V,h,nm))
print(json.dumps(out,indent=1))
