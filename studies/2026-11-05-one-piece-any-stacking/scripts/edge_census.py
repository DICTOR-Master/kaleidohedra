"""DICTO 11-06 double-spiral key, step A: edge and face census of Narcissus in slab stackings.
For the down-N and up-N nearest the axis in slab 1, for each of its 18 edges: the pieces whose surface contains the edge's
midpoint and quarter points (edge valence = pieces meeting along that edge, counting N itself), and for each of its 10 faces:
how many distinct neighbours touch it (area > 0). Words: S S and T S around slab 1 (straight / turned interfaces)."""
import numpy as np, itertools, time
from scipy.spatial import ConvexHull
from n_slabs import build, H
from n_faces import faces, overlap, kind
t0=time.time()
def edges(P):
    h=ConvexHull(P); F=faces(P); E=set()
    for n,d,V in F:
        # polygon order
        c=V.mean(0); u=V[0]-c; u/=np.linalg.norm(u); w=np.cross(n,u)
        order=np.argsort(np.arctan2((V-c)@w,(V-c)@u)); V=V[order]
        for i in range(len(V)):
            a,b=V[i],V[(i+1)%len(V)]
            E.add(tuple(sorted([tuple(np.round(a,7)),tuple(np.round(b,7))])))
    return [(np.array(a),np.array(b)) for a,b in E]
def on_surface(Q,h,x):
    s=h.equations[:,:3]@x+h.equations[:,3]
    return s.max()<=1e-7 and s.max()>=-1e-7
def isdown(P): return np.isclose(P[9,2],P[:,2].min())
for w in ['SS','TS','ST','TT']:
    Ps=build(w,n=3); hs=[ConvexHull(P) for P in Ps]
    zr=lambda P:int(np.floor(P[:,2].mean()/H)); cen=lambda P:P[:,:2].mean(0)
    for role in ['down','up']:
        C=[i for i,P in enumerate(Ps) if zr(P)==1 and isdown(P)==(role=='down')]
        i0=min(C,key=lambda i:np.linalg.norm(cen(Ps[i]))); P0=Ps[i0]
        E=edges(P0); val=[]
        for a,b in E:
            vs=[]
            for t in (0.25,0.5,0.75):
                x=a+t*(b-a); vs.append(sum(on_surface(Q,h,x) for Q,h in zip(Ps,hs)))
            val.append((round(np.linalg.norm(b-a),4),vs))
        F0=faces(P0); fn=[]
        for f in F0:
            nb=sum(1 for j,Q in enumerate(Ps) if j!=i0 and any(overlap(f,g)>1e-9 for g in faces(Q)))
            fn.append((kind(f[2]),nb))
        hist={}
        for L,vs in val: hist.setdefault((L,tuple(vs)),0); hist[(L,tuple(vs))]+=1
        print(f'word {w} slab1 {role}-N: edges {len(E)}; (length, valence at 1/4,1/2,3/4): count ->', dict(sorted(hist.items())), flush=True)
        print(f'   faces (type, neighbours touching):', sorted(fn), flush=True)
print(f'FINAL ok {time.time()-t0:.0f}s')
