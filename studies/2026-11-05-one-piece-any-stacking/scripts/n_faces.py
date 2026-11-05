"""Face-contact map of Narcissus in the slab stacking: for the down-N and up-N at the axis of slab 0,
every neighbour sharing a face (area>0), with face types and the neighbour's role (same slab / slab above / below)."""
import numpy as np
from scipy.spatial import ConvexHull
from n_slabs import build, H
def hull2(X):
    h=ConvexHull(X); return X[h.vertices]   # counter-clockwise
def clip(A,B):
    out=list(A)
    for i in range(len(B)):
        p,q=B[i],B[(i+1)%len(B)]; inp=out; out=[]
        side=lambda x:(q[0]-p[0])*(x[1]-p[1])-(q[1]-p[1])*(x[0]-p[0])
        for j in range(len(inp)):
            a,b=inp[j],inp[(j+1)%len(inp)]; sa,sb=side(a),side(b)
            if sa>=-1e-12: out.append(a)
            if (sa>=-1e-12)!=(sb>=-1e-12): t=sa/(sa-sb); out.append(a+t*(b-a))
        if not out: return 0.
    X=np.array(out); return 0.5*abs(np.dot(X[:,0],np.roll(X[:,1],-1))-np.dot(X[:,1],np.roll(X[:,0],-1)))
def faces(P):
    h=ConvexHull(P); F={}
    for eq,sp in zip(h.equations,h.simplices): F.setdefault(tuple(np.round(eq,7)),set()).update(sp)
    out=[]
    for eq,idx in F.items():
        V=P[sorted(idx)]; n=np.array(eq[:3]); out.append((n,eq[3],V))
    return out
def kind(V): return {3:'tri',4:'quad',6:'hex'}[len(V)]
def overlap(f,g):
    n,d,V=f; m,e,W=g
    if not (np.allclose(n,-m,atol=1e-6) and abs(d+e)<1e-6): return 0
    u=np.cross(n,[1,0,0] if abs(n[0])<.9 else [0,1,0]); u/=np.linalg.norm(u); v=np.cross(n,u)
    return clip(hull2(np.c_[V@u,V@v]),hull2(np.c_[W@u,W@v]))
for w in ['S','T']:
    Ps=build(w+'S',n=3)
    def zr(P): return int(np.floor(P[:,2].mean()/H))
    cen=lambda P:P[:,:2].mean(0)
    for role in ['down','up']:
        # pick the N in slab 1 (middle) nearest the axis with apex below (down) or above (up)
        cand=[P for P in Ps if zr(P)==1 and ((P[:,2].argmin()==9) == (role=='down') or True)]
        def isdown(P): return np.isclose(P[9,2],P[:,2].min())
        C=[P for P in Ps if zr(P)==1 and isdown(P)==(role=='down')]
        P0=min(C,key=lambda P:np.linalg.norm(cen(P)))
        F0=faces(P0); rows=[]
        for Q in Ps:
            if Q is P0: continue
            for f in F0:
                for g in faces(Q):
                    a=overlap(f,g)
                    if a>1e-9: rows.append((kind(f[2]),kind(g[2]),{0:'below',1:'same',2:'above'}[zr(Q)],'down' if isdown(Q) else 'up',round(a,5),tuple(np.round(f[0],3))))
        print(f'word {w}S, slab 1 {role}-N: {len(rows)} contacts')
        for r in sorted(rows): print('  ',r)
