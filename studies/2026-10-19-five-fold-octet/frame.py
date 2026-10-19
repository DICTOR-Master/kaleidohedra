import itertools, json, numpy as np
from scipy.spatial import ConvexHull
PHI=(1+5**.5)/2; hv=lambda P: ConvexHull(np.asarray(P)).volume
I=np.array([s for a in [(0,1,PHI),(1,PHI,0),(PHI,0,1)] for s in itertools.product(*[(x,-x) if x else (0,) for x in a])],float)/2
u5=I/np.linalg.norm(I,axis=1)[:,None]
D=np.array([I[f].mean(0) for f in ConvexHull(I).simplices]); D*=PHI**2/3**.5/np.linalg.norm(D[0]); u3=D/np.linalg.norm(D,axis=1)[:,None]
E=[(i,j) for i,j in itertools.combinations(range(12),2) if abs(np.linalg.norm(I[i]-I[j])-1)<1e-9]
ID=np.array([I[i]+I[j] for i,j in E]); ID*=np.linalg.norm(D[0])/(ID[np.argsort(-(ID@u3[0]))[:3]].mean(0)@u3[0])
r=np.linalg.norm(ID[0]); n2=ID/r; u2=n2; t5=r/np.max(n2@u5[0]); t3=r/np.max(n2@u3[0])
O=np.array(json.load(open('ocd-vertices.json'))); R=np.linalg.norm(O,axis=1); far=O[np.abs(R-R.max())<1e-7]/R.max()
a=far[0]; b=far[np.argsort(np.linalg.norm(far-a,axis=1))[1]]; x=u5[0]; y=u5[np.argsort(np.linalg.norm(u5-x,axis=1))[1]]
O=O@(np.array([x,y,np.cross(x,y)]).T@np.linalg.inv(np.array([a,b,np.cross(a,b)]).T)).T*3*PHI/2
def planes(V):
    q=[]
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e,w,atol=1e-7) for w in q): q.append(e)
    q=np.array(q); return q[:,:3],-q[:,3]
