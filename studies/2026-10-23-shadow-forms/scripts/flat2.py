# Flat top and bottom, step 2: cut the network into flat layers, then search for ONE unit piece per layer cell
# (each part of the layer goes to one unit; translation in x,y) with the fewest protrusions (highest fill of its convex hull).
# Layers: A = icosahedron equator to equator (z 0..φ), B = icosahedron equator to Unborn middle (0..φ/2), C = Unborn middle to middle (φ/2..3φ/2).
import numpy as np, itertools, json
exec(open('fuse6.py').read().split('vol=lambda')[0])
def hullvol(V):
    try: return ConvexHull(V).volume
    except Exception: return 0.0
def clip(V,z0,z1):
    P=[v for v in V]
    for a,b in itertools.combinations(V,2):
        for t in (z0,z1):
            if (a[2]-t)*(b[2]-t)<0: s=(t-a[2])/(b[2]-a[2]); P.append(a+s*(b-a))
    P=np.array([p for p in P if z0-1e-9<=p[2]<=z1+1e-9])
    return P if len(P)>=4 and hullvol(P)>1e-7 else None
base=[]
for c in itertools.product(range(-2,3),range(-2,3),range(-2,3)):
    o=np.array(c)*phi
    base+=[('icosahedron',ico+o),('Unborn',H+o)]+[('AXE',V+o) for V in cellA]
def layer(z0,z1):
    parts={}
    for n,V in base:
        if V[:,2].max()<=z0+1e-9 or V[:,2].min()>=z1-1e-9: continue
        P=clip(V,z0,z1)
        if P is None: continue
        c=P.mean(0); cl=np.floor(c[:2]/phi+1e-6); k=(n,)+tuple(np.round(c[:2]-cl*phi,4))+(round(c[2],4),)
        if k not in parts: parts[k]=(n,P-np.array([cl[0]*phi,cl[1]*phi,0]))
    return list(parts.values())
SH=[np.array([i,j,0])*phi for i in (-1,0,1) for j in (-1,0,1)]
def fill(parts,sh):
    allV=np.vstack([P+SH[s] for (n,P),s in zip(parts,sh)])
    return sum(hullvol(P) for n,P in parts)/hullvol(allV)
rng=np.random.default_rng(1)
out={}
for name,(z0,z1) in {'A icosahedron equator to equator':(0,phi),'B icosahedron equator to Unborn middle':(0,phi/2),'C Unborn middle to middle':(phi/2,1.5*phi)}.items():
    parts=layer(z0,z1); tot=sum(hullvol(P) for n,P in parts)
    assert abs(tot-phi**2*(z1-z0))<1e-6, (tot,phi**2*(z1-z0))
    print(name,': %d parts per cell, volume %.5f (cell %.5f):'%(len(parts),tot,phi**2*(z1-z0)),
          {n:sum(1 for m,_ in parts if m==n) for n in ('icosahedron','Unborn','AXE')})
    best=(0,None)
    for r in range(120):
        if r<2:  # compact start: each part as close as possible to the Unborn (r=0) or to the icosahedron part (r=1)
            ref=[P for n,P in parts if n==('Unborn' if r==0 else 'icosahedron')][0].mean(0)
            sh=[int(np.argmin([np.linalg.norm(P.mean(0)+SH[s]-ref) for s in range(9)])) for n,P in parts]
        else: sh=list(rng.integers(0,9,len(parts)))
        f=fill(parts,sh); improved=True
        while improved:
            improved=False
            for i in range(len(parts)):
                for s in range(9):
                    if s==sh[i]: continue
                    t=sh.copy(); t[i]=s; g=fill(parts,t)
                    if g>f+1e-9: f,sh,improved=g,t,True
        if f>best[0]: best=(f,sh)
    f,sh=best; U=[(n,(P+SH[s]).tolist()) for (n,P),s in zip(parts,sh)]
    allV=np.vstack([np.array(P) for n,P in U]); ext=allV.max(0)-allV.min(0)
    print('   best unit: fill %.1f%% of its hull; size %.3f x %.3f x %.3f'%(100*f,*ext))
    out[name]={'fill':f,'z':[z0,z1],'unit':U}
json.dump(out,open('flat2-units.json','w'))
