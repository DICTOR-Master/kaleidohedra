# The golden split t = 1/φ: are both padded pieces exactly convex? Their corners and faces; volumes; point test of the 2-piece fill.
import numpy as np, itertools, json
from collections import Counter
src=open('axesplit1.py').read().split('uc=np.array')[0]; exec(src)
uc=np.array([h,h,h])
def piece(t,base,c):
    P=[base+c]
    for V in allA:
        if np.linalg.norm(V.mean(0)-c)>1.6: continue
        for f in touching(V,c,base):
            p=(1-t)*(V[0]+V[1])/2+t*(V[2]+V[3])/2; cone=np.vstack([V[list(f)],p])
            if abs(np.linalg.det(cone[:3]-cone[3]))/6>1e-12: P.append(cone)
    pv=vol(P[0])+sum(abs(np.linalg.det(Q[:3]-Q[3]))/6 for Q in P[1:]); return P,pv
def describe(V):
    hl=ConvexHull(V); planes=[]
    for e in hl.equations:
        if not any(np.allclose(e,q,atol=1e-7) for q in planes): planes.append(e)
    corners=[v for v in V if sum(abs(v@q[:3]+q[3])<1e-7 for q in planes)>=3]
    C=np.unique(np.round(corners,9),axis=0)
    fk=Counter()
    for q in planes:
        on=C[np.abs(C@q[:3]+q[3])<1e-7]; c=on.mean(0)
        # order around the face and record side lengths
        n=q[:3]; u=on[0]-c; u/=np.linalg.norm(u); w=np.cross(n,u)
        on=on[np.argsort(np.arctan2((on-c)@w,(on-c)@u))]
        L=tuple(sorted(np.round([np.linalg.norm(on[i]-on[i-1]) for i in range(len(on))],5)))
        fk[(len(on),L)]+=1
    return len(C),len(planes),fk,hl.volume
T=1/phi
for t in [T-1e-4,T,T+1e-4]:
    a=piece(t,ico,np.zeros(3)); b=piece(t,H-uc,uc)
    print('t=%.7f  ico+: fill-1 = %.2e   Unborn+: fill-1 = %.2e'%(t,a[1]/vol(np.vstack(a[0]))-1,b[1]/vol(np.vstack(b[0]))-1))
for name,(P,pv) in [('padded icosahedron',piece(T,ico,np.zeros(3))),('padded Unborn',piece(T,H-uc,uc))]:
    n,f,fk,hv=describe(np.vstack(P))
    print(name,': corners',n,' faces',f,' volume %.6f (hull %.6f)'%(pv,hv)); [print('   ',k,'x',v) for k,v in sorted(fk.items())]
    json.dump(np.unique(np.round(np.vstack(P),9),axis=0).tolist(),open('golden-'+name.split()[1]+'.json','w'))
print('cell volume φ³ = %.6f'%phi**3)
