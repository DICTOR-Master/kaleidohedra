# Shadow forms, step 1 (DICTO 2026-10-23, fusions first): in the simple cubic icosahedron lattice (edge 1, spacing phi), every pair of
# pieces that share a face, and whether their union is one convex solid (hull volume = sum of volumes). Pieces: icosahedron, Unborn,
# dodecahedron, Lotus Jewel (non-convex: skipped as a whole, used via Tricaps), Tricap, AXE.
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
# Tricaps: corners of the dodecahedron = cube corner + its 3 neighbouring H vertices (the dodecahedron's vertex figure)
def tricaps():
    out=[]
    for c in cube:
        d=np.linalg.norm(H-c,axis=1); nb=H[np.argsort(d)[:3]]; out.append(np.vstack([c,nb]))
    return out
TR=tricaps()
assert all(abs(ConvexHull(t).volume-(3-5**.5)/24)<1e-9 for t in TR), [ConvexHull(t).volume for t in TR]
def pieces(network):
    P=[]
    for sh in itertools.product((-1,0,1),repeat=3):
        o=np.array(sh)*phi
        if network in ('icoUnborn','four'):
            if network=='icoUnborn': P.append(('icosahedron',ico+o))
            P.append(('Unborn',H+o))
        if network in ('jewelDodeca',): P.append(('dodecahedron',D+o))
        if network=='four': P+= [('Tricap',t+o) for t in TR]
        P+=[('AXE',V+o) for V in axes.values()]
    return P
def faces(V):
    hl=ConvexHull(V); F={}
    for s,e in zip(hl.simplices,hl.equations): F.setdefault(tuple(np.round(e,6)),set()).update(s)
    return [(np.array(k[:3]),k[3],V[list(f)]) for k,f in F.items()]
def share_face(A,B):
    for na,da,Pa in faces(A):
        for nb,db,Pb in faces(B):
            if np.allclose(na,-nb,atol=1e-6) and abs(da+db)<1e-6:
                # common area: points of each face polygon inside the other plane's polygon -> use 2D hull intersection approx via shared vertices
                sa={tuple(np.round(p,5)) for p in Pa}; sb={tuple(np.round(p,5)) for p in Pb}
                if len(sa&sb)>=3: return True
    return False
def sig(V):
    hl=ConvexHull(V); e=sorted({round(float(np.linalg.norm(V[i]-V[j])),4) for s in hl.simplices for i,j in itertools.combinations(s,2)})
    nf=len({tuple(np.round(q,6)) for q in hl.equations}); return (len(hl.vertices),nf,round(hl.volume,6))
import sys
for net in ['icoUnborn','four']:
    P=pieces(net); centre=[i for i,(n,V) in enumerate(P) if np.linalg.norm(V.mean(0)-np.array([h,h,h]))<1.6]
    found={}
    for i in centre:
        for j in range(len(P)):
            if j<=i and j in centre: continue
            ni,Vi=P[i]; nj,Vj=P[j]
            if np.linalg.norm(Vi.mean(0)-Vj.mean(0))>2.2: continue
            if not share_face(Vi,Vj): continue
            U=np.vstack([Vi,Vj]); hv=ConvexHull(U).volume; s=ConvexHull(Vi).volume+ConvexHull(Vj).volume
            key=(tuple(sorted([ni,nj])), abs(hv-s)<1e-7)
            if key not in found: found[key]=(sig(U) if abs(hv-s)<1e-7 else None, hv, s)
    print('==',net)
    for (pair,convex),(sg,hv,s) in sorted(found.items()):
        print('  %-28s convex=%-5s'%(' + '.join(pair),convex), ('verts/faces/vol %s'%(sg,)) if convex else 'hull %.4f > sum %.4f'%(hv,s))
