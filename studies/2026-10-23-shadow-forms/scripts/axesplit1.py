# AXE polar split: a point p inside each AXE cones it into 4 pyramids, one on each face; each pyramid joins the piece across that face
# (faces with the long edge 0-1 lie on icosahedra, faces with the short edge 2-3 on Unborns). The AXE vanishes: two pieces remain,
# icosahedron+12 pyramids and Unborn+12 pyramids. p moves along the AXE's axis from the long-edge midpoint (t=0) to the short-edge midpoint (t=1).
import numpy as np, itertools
exec(open('fuse6.py').read().split('vol=lambda')[0])
from scipy.spatial import ConvexHull
vol=lambda V:ConvexHull(V).volume
allA=[V+np.array(c)*phi for c in itertools.product(range(-2,3),repeat=3) for V in cellA]
def touching(V,c,base):  # faces of AXE V lying on the piece base+c
    E=ConvexHull(base+c).equations; out=[]
    for f in itertools.combinations(range(4),3):
        F=V[list(f)]
        if all(np.isclose(E[:,:3]@x+E[:,3],0,atol=1e-7).any() for x in F) and np.isclose((E[:,:3]@F.T+E[:,3][:,None]).max(0),0,atol=1e-7).all(): out.append(f)
    return out
uc=np.array([h,h,h])
import sys
for t in [float(x) for x in sys.argv[1:]]:
    row=[]
    for name,base,c in [('icosahedron',ico,np.zeros(3)),('Unborn',H-uc,uc)]:
        P=[base+c]; add=0
        for V in allA:
            if np.linalg.norm(V.mean(0)-c)>1.6: continue
            fs=touching(V,c,base)
            for f in fs:
                p=(1-t)*(V[0]+V[1])/2+t*(V[2]+V[3])/2
                cone=np.vstack([V[list(f)],p]); 
                if abs(np.linalg.det(cone[:3]-cone[3]))/6>1e-9: P.append(cone); add+=1
        Vall=np.vstack(P); pv=vol(P[0])+sum(abs(np.linalg.det(Q[:3]-Q[3]))/6 for Q in P[1:]); hv=vol(Vall)
        row.append('%s +%d pyramids: vol %.4f fill %.1f%%'%(name,add,pv,100*pv/hv))
    print('t=%.4f  '%t+'  |  '.join(row),flush=True)
