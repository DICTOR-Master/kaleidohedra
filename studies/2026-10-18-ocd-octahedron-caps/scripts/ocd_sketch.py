# DICTO 2026-10-17: Admiral Cap analog -- the OCD in the regular octahedron of its 8 joint hexagons: z=0 section, top view, the cap at +z, the golden key on a joint hexagon. -> data/ocd-octa-sketch.json
import sys, io, os, contextlib, itertools, json, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
PD='/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here=os.getcwd(); os.chdir(PD)
sys.argv=['polar.py','data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()): exec(open('scripts/polar.py').read())
os.chdir(here)
St=dict(rev); V=np.array([[x.f() for x in v] for v in St['dual of the Hecatodihedron']])
h=ConvexHull(V); eq=np.unique(np.round(h.equations,10),axis=0)
hexn=[e for e in eq if np.sum(np.abs(V@e[:3]+e[3])<1e-7)==6]
c3=[e for e in hexn if np.allclose(np.abs(e[:3]),1/3**.5,atol=1e-9)]
R=-c3[0][3]*3**.5
out={'R':R}
# A: section z=0
def sect2d(H):  # H rows a,b,c,d -> 2D halfspaces in x,y (z=0)
    A=np.c_[H[:,0],H[:,1],H[:,3]]; hs=HalfspaceIntersection(A,np.zeros(2)); P=hs.intersections
    c=P.mean(0); return P[np.argsort(np.arctan2(P[:,1]-c[1],P[:,0]-c[0]))].tolist()
out['ocd_z0']=sect2d(eq)
# B: projection along z of OCD faces facing +z (visible), and silhouette
faces=[]
for e in eq:
    idx=np.where(np.abs(V@e[:3]+e[3])<1e-7)[0]; P=V[idx]; c=P.mean(0); n=e[:3]
    u=P[0]-c; u/=np.linalg.norm(u); w=np.cross(n,u); ang=np.arctan2((P-c)@w,(P-c)@u); P=P[np.argsort(ang)]
    if n[2]>1e-9: faces.append({'k':len(idx),'p':P[:,:2].tolist(),'nz':float(n[2])})
out['top']=faces
# cap volumes: cap at +z = shell points with z>=|x|,|y|
rng=np.random.default_rng(2); P=rng.uniform(-R,R,(3000000,3)); P=P[np.abs(P).sum(1)<=R]
octV=4/3*R**3; inO=np.all(P@eq[:,:3].T+eq[:,3]<=0,axis=1); G=P[~inO]
cap=G[(G[:,2]>=np.abs(G[:,0]))&(G[:,2]>=np.abs(G[:,1]))]
out['shell_frac']=len(G)/len(P); out['cap_vol']=len(cap)/len(P)*octV; out['ocd_vol']=h.volume; out['oct_vol']=octV
# is a cap one piece? voxel label
n=120; g=np.linspace(-R,R,n); X,Y,Z=np.meshgrid(g,g,g,indexing='ij'); Q=np.c_[X.ravel(),Y.ravel(),Z.ravel()]
m=(np.abs(Q).sum(1)<=R*0.999)&~np.all(Q@eq[:,:3].T+eq[:,3]<=0,axis=1)&(Q[:,2]>=np.abs(Q[:,0]))&(Q[:,2]>=np.abs(Q[:,1]))
from scipy import ndimage
lab,k=ndimage.label(m.reshape(n,n,n)); s=np.bincount(lab.ravel())[1:]; out['cap_components']=int((s>20).sum())
# does the cap touch OCD? fraction of OCD surface under cap: OCD faces whose centre has z>=|x|,|y|
cnt={}
for e in eq:
    idx=np.where(np.abs(V@e[:3]+e[3])<1e-7)[0]; c=V[idx].mean(0)
    if c[2]>=abs(c[0])-1e-9 and c[2]>=abs(c[1])-1e-9: cnt[len(idx)]=cnt.get(len(idx),0)+1
out['cap_faces_under']=cnt
# C: joint hexagon on (1,1,1)
e=c3[[i for i in range(len(c3)) if np.all(c3[i][:3]>0)][0]]
idx=np.where(np.abs(V@e[:3]+e[3])<1e-7)[0]; P=V[idx]; c=P.mean(0); nn=e[:3]
p=(1+5**.5)/2; two=[np.roll([p,1,1/p],k)/2 for k in range(3)]
two+=[np.roll([p,1/p,1],k)/2 for k in range(3)]  # both cyclic orders (frame-dependent)
kind=['two' if any(np.allclose(np.abs(q)/np.linalg.norm(q),t,atol=1e-6) for t in two) else 'side' for q in P]
u=np.array([1,-1,0])/2**.5; w=np.cross(nn,u); X2=np.c_[(P-c)@u,(P-c)@w]; o=np.argsort(np.arctan2(X2[:,1],X2[:,0]))
out['hex']=X2[o].tolist(); out['hexkind']=[kind[i] for i in o]; s_=np.linalg.norm(X2[0]-X2[1]) if True else 0
sides=[np.linalg.norm(X2[o][i]-X2[o][(i+1)%6]) for i in range(6)]; out['hex_edge']=float(np.mean(sides)); out['hex_edge_spread']=float(np.ptp(sides))
out['key_h']=out['hex_edge']/2*np.tan(np.radians(20.905157)); 
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','ocd-octa-sketch.json'),'w'))
print({k:v for k,v in out.items() if k not in('ocd_z0','top','hex')})
