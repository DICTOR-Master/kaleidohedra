# DICTO 10-22: rotate (and shift) one cap of the stretched dodecahedron so the belt becomes equilateral triangles?
# A cap = the 6 pentagons on one side of the dodecahedron's silhouette for a direction u; its rim is a skew decagon.
# Join cap A to a moved copy A' by an antiprism band (20 triangles: rim vertex i to rim' i and i+1). All band edges = 1?
import numpy as np, itertools, math
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation as Rot
import mixes3 as M
phi=M.phi; DOD=M.DOD.copy()
E=[(a,b) for a,b in itertools.combinations(range(20),2) if abs(np.linalg.norm(DOD[a]-DOD[b])-1)<1e-9]
def rim(u):
    # silhouette edges: edges between a face facing +u and a face facing -u; order them into a cycle
    from scipy.spatial import ConvexHull
    h=ConvexHull(DOD); faces={}
    for s,eq in zip(h.simplices,h.equations): faces.setdefault(tuple(np.round(eq,6)),set()).update(s)
    F=[(np.array(k[:3]),v) for k,v in faces.items()]
    sil=[e for e in E if len({np.sign(round(n@u,9)) for n,v in F if e[0] in v and e[1] in v})==2]
    cyc=[sil[0][0],sil[0][1]]; rest=sil[1:]
    while rest:
        for e in rest:
            if cyc[-1] in e: nxt=e[1] if e[0]==cyc[-1] else e[0]; cyc.append(nxt); rest.remove(e); break
        else: break
    return np.array([DOD[i] for i in cyc[:-1]])
def best(u,label):
    B=rim(u); n=len(B); c=B.mean(0)
    def res(p):
        R=Rot.from_rotvec(p[:3]).as_matrix(); t=p[3:]
        B2=(B-c)@R.T+c+t
        r=[]
        for i in range(n): r+= [np.linalg.norm(B[i]-B2[i])-1, np.linalg.norm(B[i]-B2[(i+1)%n])-1]
        return r
    bestv=None
    rs=np.random.default_rng(0)
    for k in range(300):
        p0=np.r_[rs.normal(0,0.6,3), u*rs.uniform(0.3,2.5)+rs.normal(0,0.2,3)]
        s=least_squares(res,p0)
        v=np.max(np.abs(s.fun))
        if bestv is None or v<bestv[0]: bestv=(v,s.x)
    print(label,'rim vertices',n,' best worst-edge error',round(bestv[0],6))
    return bestv
u1=np.array([1,1,0])/2**.5
best(u1,'(a) face-diagonal caps:')
u5=np.array([0,1,phi]); u5/=np.linalg.norm(u5)   # a face normal: five-fold axis
v,p=best(u5,'(b) five-fold caps:')
R=Rot.from_rotvec(p[:3]); print('   twist about the axis (deg):', round(math.degrees(np.linalg.norm(p[:3])),3), ' shift along axis:', round(p[3:]@u5,6))
