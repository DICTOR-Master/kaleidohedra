import sys; sys.path.insert(0,'.')
import numpy as np
from n_slabs import narc, SITE, H
from scipy.spatial import ConvexHull
P=narc(SITE['A'],H,0,'C'); c=SITE['A']
def faces(V):
    h=ConvexHull(V); eq=np.round(h.equations,6); fs={}
    for s,e in zip(h.simplices,eq): fs.setdefault(tuple(e),set()).update(s)
    return [len(v) for v in fs.values()], len(V)
print('N faces', sorted(faces(P)[0]))
mids=[p for p in P if abs(p[2]-H/2)<1e-9]
for name,d in [('through a mid corner',mids[0][:2]-c),('between mid corners',None)]:
    if d is None:
        a=np.arctan2(*(mids[0][:2]-c)[::-1])+np.pi/3; d=np.array([np.cos(a),np.sin(a)])
    n=np.array([-d[1],d[0],0.0]); n/=np.linalg.norm(n)
    pts=[p for p in P if (p-np.r_[c,0])@n>=-1e-9]
    # add edge intersections with the plane
    h=ConvexHull(P)
    for s in h.simplices:
        for i in range(3):
            a_,b_=P[s[i]],P[s[(i+1)%3]]; fa=(a_-np.r_[c,0])@n; fb=(b_-np.r_[c,0])@n
            if fa*fb<-1e-12: pts.append(a_+(b_-a_)*fa/(fa-fb))
    V=np.unique(np.round(np.array(pts),9),axis=0)
    f,nv=faces(V); print(name,': half faces',len(f),sorted(f),'corners',nv,'vol',ConvexHull(V).volume)
