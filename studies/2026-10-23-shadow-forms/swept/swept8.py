# Route A, step 5: the gaps of the swept-piece lattice packing. Voxelise one lattice cell (periodic), mark points outside every
# swept piece, label connected gap pieces (with wrap-around), and report per-cell count, volumes and how convex each one is.
import numpy as np, itertools, json
from scipy import ndimage
from scipy.spatial import ConvexHull
exec(open('swept1.py').read().split('# period:')[0])
L=json.load(open('swept-best-lattice.json')); B=np.array(L['basis']); det=abs(np.linalg.det(B))
n=int(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else 72
g=(np.arange(n)+0.5)/n; F=np.stack(np.meshgrid(g,g,g,indexing='ij'),-1).reshape(-1,3); X=F@B
cov=np.zeros(len(X),bool)
for c in itertools.product(range(-2,3),repeat=3):
    o=np.array(c)@B; cov|=inside(X-o,ES)
gap=(~cov).reshape(n,n,n)
lab,k=ndimage.label(gap)
# merge labels across the periodic boundary
par=list(range(k+1))
def f(i):
    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
    return i
for ax in range(3):
    a=np.take(lab,0,axis=ax); b=np.take(lab,n-1,axis=ax)
    for x,y in zip(a.ravel(),b.ravel()):
        if x and y: par[f(x)]=f(y)
roots=np.array([f(i) for i in range(k+1)]); lab=roots[lab]
ids=[r for r in np.unique(lab) if r and (lab==r).sum()>=max(40,int(4e-4*n**3))]  # drop voxel specks at piece boundaries
vox=det/n**3
print('packing density %.4f; gap %.4f of space; %d real gap pieces per lattice cell (specks dropped: %.5f of space)'%(cov.mean(),gap.mean(),len(ids),gap.mean()-sum((lab==r).sum() for r in ids)/n**3))
out=[]
for r in ids:
    m=(lab==r).ravel(); v=m.sum()*vox
    P=X[m]
    # unwrap: shift points to be near the first point (periodic)
    fr=F[m]; fr=fr-np.round(fr-fr[0]); P=fr@B
    try: hv=ConvexHull(P).volume
    except Exception: hv=float('nan')
    out.append((v,hv)); print('  gap piece: volume %.4f (%.2f%% of a swept piece), fills %.1f%% of its hull'%(v,100*v/hS.volume,100*v/hv))
json.dump(out,open('swept-gaps.json','w'))
