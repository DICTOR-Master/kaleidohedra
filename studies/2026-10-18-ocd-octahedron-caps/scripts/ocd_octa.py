# DICTO 2026-10-17: does the OCD sit in a regular octahedron (8 joint hexagons on its faces) like the icosahedron + 6 Admiral Caps? fill ratio, five-fold corners vs edges, shell components.
import sys, io, os, contextlib, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
PD='/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here=os.getcwd(); os.chdir(PD)
sys.argv=['polar.py','data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()): exec(open('scripts/polar.py').read())
os.chdir(here)
St=dict(rev); V=np.array([[x.f() for x in v] for v in St['dual of the Hecatodihedron']])
h=ConvexHull(V); eq=np.unique(np.round(h.equations,9),axis=0)
hexn=[e for e in eq if np.sum(np.abs(V@e[:3]+e[3])<1e-7)==6]
print('faces',len(eq),'hexagons',len(hexn))
# hexagon normals along (+-1,+-1,+-1)? check
for e in hexn[:20]: pass
cubeish=[e for e in hexn if np.allclose(np.abs(e[:3]),1/3**.5,atol=1e-9)]
print('hexagons on cube 3-fold axes:',len(cubeish))
dh=-cubeish[0][3]; R=dh*3**.5   # octahedron |x|+|y|+|z|<=R
r=np.linalg.norm(V,axis=1); five=V[r>r.min()+1e-6]
print('five-fold corners',len(five),'|x|+|y|+|z| / R:',np.unique(np.round(np.abs(five).sum(1)/R,6)))
print('all corners max l1/R',np.abs(V).sum(1).max()/R)
vo=h.volume; oct_=4/3*R**3; print('OCD vol',vo,'octa vol',oct_,'ratio',vo/oct_,'octa edge',R*2**.5)
# components of octa minus OCD by sampling
rng=np.random.default_rng(1); P=rng.uniform(-R,R,(400000,3)); P=P[np.abs(P).sum(1)<=R]
inO=np.all(P@eq[:,:3].T+eq[:,3]<=1e-12,axis=1); G=P[~inO]
print('gap frac of octa',len(G)/len(P))
# which octa vertex region: nearest of 6 axis tips, and whether regions meet: test points near octa edges midpoints in gap
mid=np.array([[R/2,R/2,0]]); print('octa edge midpoint inside OCD?',np.all(mid@eq[:,:3].T+eq[:,3]<=0))
# connectivity via voxel flood
n=90; g=np.linspace(-R,R,n); X,Y,Z=np.meshgrid(g,g,g,indexing='ij'); Q=np.c_[X.ravel(),Y.ravel(),Z.ravel()]
m=(np.abs(Q).sum(1)<=R*0.999)&~np.all(Q@eq[:,:3].T+eq[:,3]<=0,axis=1)
from scipy import ndimage
lab,k=ndimage.label(m.reshape(n,n,n)); sizes=np.bincount(lab.ravel())[1:]; print('gap components',k,sorted(sizes)[-8:])
