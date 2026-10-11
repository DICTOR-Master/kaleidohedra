import itertools, numpy as np
from scipy.spatial import ConvexHull
P=(1+5**.5)/2
def cyc(v):
    out=set()
    for s in itertools.product(*[(-1,1) if x else (1,) for x in v]):
        w=[a*b for a,b in zip(v,s)]
        for k in range(3): out.add(tuple(np.round(np.roll(w,k),12)))
    return np.array(sorted(out),float)
def uniqfaces(V):
    E=[]
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e-q)<1e-6 for q in E): E.append(e)
    return np.array(E)
I=cyc((0,1,P))
F=uniqfaces(I); D=np.array([-f[:3]/f[3] for f in F])
EI=[(a,b) for a,b in itertools.combinations(range(12),2) if abs(np.linalg.norm(I[a]-I[b])-2)<1e-9]
ID=np.array([(I[a]+I[b])/2 for a,b in EI])
dmin=min(np.linalg.norm(D[0]-w) for w in D[1:])
ED=[(a,b) for a,b in itertools.combinations(range(20),2) if abs(np.linalg.norm(D[a]-D[b])-dmin)<1e-9]
md=lambda V,E: np.linalg.norm((V[E[0][0]]+V[E[0][1]])/2)
Ds=D*md(I,EI)/md(D,ED)
MD=np.array([(Ds[a]+Ds[b])/2 for a,b in ED])
print('icosahedron + dodecahedron in dual position:')
print('  their 30 edge pairs cross at the same points:', all(np.min(np.linalg.norm(MD-m,axis=1))<1e-9 for m in ID))
print('  those 30 points form an icosidodecahedron:', len(ID)==30 and len(uniqfaces(ID))==32)
print('  convex hull of both:', len(uniqfaces(np.vstack([I,Ds]))), 'faces (rhombic triacontahedron has 30)')
row=Ds[np.abs(Ds[:,0])<1e-9][0]; print('  dodecahedron non-cube corners on rectangles with ratio', round(max(abs(row[1:]))/min(abs(row[1:])),6), '(phi^2 =',round(P**2,6),')')
