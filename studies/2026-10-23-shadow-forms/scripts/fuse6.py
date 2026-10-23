# Shadow forms, step 6: two-piece fills by giving each AXE to one of its two neighbours.
# AXE vertices 0,1 = an edge shared by two icosahedra (lattice points); vertices 2,3 = a short edge shared by two Unborns (body centres).
# Rule: each AXE goes to the neighbour with the smaller coordinate sum. Check: every piece gets exactly 6, then a point test.
import numpy as np, json, itertools
from scipy.spatial import ConvexHull
phi=(1+5**.5)/2; h=phi/2
ico=np.array([p for s1 in (1,-1) for s2 in (1,-1) for p in [(0,s1*.5,s2*phi/2),(s1*.5,s2*phi/2,0),(s2*phi/2,0,s1*.5)]])
H=np.array(json.load(open('/home/dicto/k-mix/studies/2026-10-10-icosa-networks-2/data/sc-star-H-unit.json'))['vertices'])
cube=np.array([(h+a,h+b,h+c) for a in (-.5,.5) for b in (-.5,.5) for c in (-.5,.5)]); D=np.vstack([H,cube])
axe=np.array([(-.5,h,0),(.5,h,0),(0,h+.5/phi,h),(0,h-.5/phi,h)])
axes={}
for perm in [(0,1,2),(1,2,0),(2,0,1)]:
    for sg in itertools.product((1,-1),repeat=3):
        V=axe[:,perm]*np.array(sg); c=V.mean(0); k=tuple(np.round(np.mod(c,phi),5))
        if k not in axes: axes[k]=V-(c-np.mod(c,phi))
cellA=list(axes.values()); assert len(cellA)==6
vol=lambda V:ConvexHull(V).volume
print('volumes: ico %.5f  Unborn %.5f  AXE %.5f  dodeca %.5f'%(vol(ico),vol(H),vol(cellA[0]),vol(D)))
def owners(V):
    m1=(V[0]+V[1])/2; m2=(V[2]+V[3])/2
    # two icosahedra across edge 0-1: lattice points at distance h from m1
    I=[np.round(m1/phi+s*u/2)*phi for u in np.eye(3) for s in (1,-1)]; I=[p for p in I if abs(np.linalg.norm(p-m1)-h)<1e-6 and np.allclose(np.round(p/phi),p/phi)]
    U=[(np.floor(m2/phi+s*u/2)+.5)*phi for u in np.eye(3) for s in (1,-1)]; U=[p for p in U if abs(np.linalg.norm(p-m2)-h)<1e-6]
    uniq=lambda L:list({tuple(np.round(p,6)):p for p in L}.values())
    return uniq(I),uniq(U)
I,U=owners(cellA[0]); print('one AXE: icosahedra at',[tuple(np.round(p/phi,2)) for p in I],' Unborns at',[tuple(np.round(p/phi,2)) for p in U])
# all AXE in a 5^3 block of cells, assign, count per owner
allA=[V+np.array(c)*phi for c in itertools.product(range(-2,3),repeat=3) for V in cellA]
for kind in ['ico','unborn']:
    cnt={}
    for V in allA:
        I,U=owners(V); L=I if kind=='ico' else U; assert len(L)==2
        o=min(L,key=lambda p:p.sum()); cnt.setdefault(tuple(np.round(o/phi*2)),[]).append(V)
    inner={k:v for k,v in cnt.items() if all(-2<=x/2<=1 for x in k)}
    print(kind,'AXE per piece (inner):',sorted(set(len(v) for v in inner.values())))
    # shape of the merged piece around the origin owner
    o=(0,0,0) if kind=='ico' else (1,1,1); base=ico if kind=='ico' else H+0  # H is in cell frame with centre (h,h,h)
    Vs=cnt[o]; c0=np.array(o)/2*phi; allV=np.vstack([base]+Vs)
    hv=vol(allV); pv=vol(base)+sum(vol(V) for V in Vs)
    ax=np.linalg.svd(allV-allV.mean(0))[1]
    print('  piece: volume %.5f, hull %.5f, fill %.1f%%, convex %s, AXE directions from centre:'%(pv,hv,100*pv/hv,abs(pv-hv)<1e-9),
          sorted(set(tuple(np.round((V.mean(0)-c0)/np.linalg.norm(V.mean(0)-c0),2)) for V in Vs))[:6])
    json.dump({'base':base.tolist(),'axes':[V.tolist() for V in Vs]},open(f'twopiece-{kind}.json','w'))
# point test: pieces (ico + its AXE) and Unborn; then the twin (Unborn + its AXE) and ico
rs=np.random.default_rng(5); N=400000; P=rs.random((N,3))*3*phi
EI,EH=ConvexHull(ico).equations,ConvexHull(H).equations
inside=lambda Q,E:(Q@E[:,:3].T+E[:,3]<=1e-12).all(1)
tot=np.zeros(N,int)
for c in itertools.product(range(-1,5),repeat=3):
    o=np.array(c)*phi; tot+=inside(P-o,EI); tot+=inside(P-o,EH)
for V in [V+np.array(c)*phi for c in itertools.product(range(-1,5),repeat=3) for V in cellA]:
    tot+=inside(P,ConvexHull(V).equations)
print('point test of the whole network (ico + Unborn + AXE, each AXE counted once): uncovered %d doubled %d'%((tot==0).sum(),(tot>1).sum()))
