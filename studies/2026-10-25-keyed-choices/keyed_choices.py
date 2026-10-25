# Keyed choices A and B for two pairs (DICTO 2026-10-25). Key = cap moved from the bigger piece into the smaller one through every
# shared triangle (as the golden keyed pair moves its Tricaps out of the Icosaxes):
#   A: cap = cone over the shared triangle's mid-triangle (edge midpoints) with apex at the bigger piece's centre (deepest key).
#   B: cap = tooth over the same mid-triangle, height = sqrt(2/3) x its mean edge (a tetrahedral tooth).
# Pairs: Delian bond (Samson = tet piece -> Delilah = oct piece) and David & Goliath (Goliath -> David). manifold3d booleans;
# matplotlib renders; checks: volumes conserved, keyed pieces watertight. Output: keyed_choices.png, keyed_choices.txt.
import numpy as np, itertools, manifold3d as m3, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
def hull(P): return m3.Manifold.hull_points([list(map(float,p)) for p in P])
def tri_faces(P,c):
    """triangular faces of the convex hull of P (as point triples), with outward normals"""
    from scipy.spatial import ConvexHull
    h=ConvexHull(P); out={}
    for s,e in zip(h.simplices,h.equations):
        key=tuple(np.round(e,9)); out.setdefault(key,set()).update(s)
    return [(P[sorted(v)],np.array(k[:3])) for k,v in out.items() if len(v)==3]
KS={'Delian bond':1.0,'David & Goliath':0.8}
cur=['Delian bond']
def mid(T):
    M=np.array([(T[0]+T[1])/2,(T[1]+T[2])/2,(T[2]+T[0])/2]); c=M.mean(0); return c+KS[cur[0]]*(M-c)
def cap(T,apex): return hull(np.vstack([mid(T),[apex]]))
def keyed(big_P,big_c,small_P,small_c,neigh_big_centres,option,shared_big,shared_small):
    big=hull(big_P); small=hull(small_P)
    for T,n,cen in shared_big:      # caps leaving the big piece through its shared triangles
        M=mid(T); h=np.sqrt(2/3)*np.mean([np.linalg.norm(M[i]-M[(i+1)%3]) for i in range(3)])
        apex= big_c if option=='A' else M.mean(0)-h*n
        big=big-cap(T,apex)
    for T,n,bc in shared_small:     # caps arriving in the small piece through its shared triangles (apex on the big side)
        M=mid(T); h=np.sqrt(2/3)*np.mean([np.linalg.norm(M[i]-M[(i+1)%3]) for i in range(3)])
        apex= bc if option=='A' else M.mean(0)+h*n
        small=small+hull(np.vstack([M-1e-6*n,[apex]]))
    return big,small
out=[]; panels=[]
# ---- Delian bond (cube side 2 units; krp-core tetPiece/octPiece, t >= 1/3) ----
t=1-(2/3)*2**(-1/3); a=1.5*(1-t)
C=[np.array([x,y,z],float) for x in (0,1) for y in (0,1) for z in (0,1)]
even=[c for c in C if sum(c)%2==0]; octs=[c for c in C if sum(c)%2==1]
samP=np.array(even+[o+a*(v-o) for o in octs for v in even if np.linalg.norm(v-o)<1.0001]); samC=np.array([.5,.5,.5])
dc=np.array([1.,0,0]); delP=np.array([dc+s*a*e for e in np.eye(3) for s in (1,-1)])
sam_tris=[(T,n,None) for T,n in tri_faces(samP,samC)]
del_tris=[]
for T,n in tri_faces(delP,dc):
    bc=dc+0.5*np.sign(np.round(n,6)); del_tris.append((T,n,bc))   # neighbouring Samson centre across this face
V0=(hull(samP).volume(),hull(delP).volume())
# ---- David & Goliath (A15, cube edge 2) ----
J=[]
for a_,b in itertools.product([.5,-.5],[1.,-1.]):
    J+= [[0,a_,b],[b,0,a_],[a_,b,0]]
golP=np.array(J); golC=np.zeros(3)
davP=np.array([[0,-.5,1],[0,.5,1],[1,0,.5],[1,0,1.5]]); davC=np.array([.5,0,1])
dav_tris=[]
for T,n in tri_faces(davP,davC):
    # the Goliath across this face: Si sites 2Z^3 and 2Z^3+(1,1,1); pick the one nearest the face centre on the outer side
    cands=[np.array(p,float) for p in itertools.product(range(-2,4),repeat=3) if (all(v%2==0 for v in p) or all(v%2==1 for v in p))]
    fc=T.mean(0); bc=min([c for c in cands if np.dot(c-fc,n)>0],key=lambda c:np.linalg.norm(c-fc)); dav_tris.append((T,n,bc))
gol_tris=[]
for T,n in tri_faces(golP,golC):
    e=sorted(np.linalg.norm(T[i]-T[(i+1)%3]) for i in range(3))
    if abs(e[0]-e[2])>1e-9: gol_tris.append((T,n,None))           # the 12 isosceles faces = shared with Davids
W0=(hull(golP).volume(),hull(davP).volume())
for name,(bP,bC,sP,sC,btris,stris,V,labels) in {'Delian bond':(samP,samC,delP,dc,sam_tris,del_tris,V0,('Samson','Delilah')),
        'David & Goliath':(golP,golC,davP,davC,gol_tris,dav_tris,W0,('Goliath','David'))}.items():
    cur[0]=name
    for opt in 'AB':
        big,small=keyed(bP,bC,sP,sC,None,opt,btris,stris)
        dv_big=V[0]-big.volume(); dv_small=small.volume()-V[1]
        n_caps_big=len(btris); n_caps_small=len(stris)
        out.append(f"{name} {opt}: {labels[0]} {V[0]:.5f} -> {big.volume():.5f} ({n_caps_big} sockets), {labels[1]} {V[1]:.5f} -> {small.volume():.5f} ({n_caps_small} teeth); "
                   f"per-cap {dv_big/n_caps_big:.5f} out vs {dv_small/n_caps_small:.5f} in; genus {big.genus()},{small.genus()}")
        panels.append((f"{name} — {opt}",big,small,labels))
fig=plt.figure(figsize=(16,8.6),dpi=150)
for i,(title,big,small,labels) in enumerate(panels):
    for j,(piece,lab,col) in enumerate(((big,labels[0],'#e2b04a'),(small,labels[1],'#6d8fd4'))):
        ax=fig.add_subplot(2,4,2*i+j+1,projection='3d'); mesh=piece.to_mesh(); V=np.array(mesh.vert_properties)[:,:3]; Fc=np.array(mesh.tri_verts)
        pc=Poly3DCollection(V[Fc],facecolor=col,edgecolor=(0,0,0,0.25),linewidths=0.2); ax.add_collection3d(pc)
        lo,hi=V.min(0),V.max(0); c=(lo+hi)/2; r=(hi-lo).max()/2
        ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r,c[2]+r); ax.set_axis_off(); ax.view_init(22,35)
        ax.set_title(f"{title}: {lab}",fontsize=9)
fig.text(0.99,0.01,'DICTO',ha='right',fontsize=10,color='#b8962e',weight='bold')
fig.suptitle('Keyed choices. A: cone to the big piece\'s centre on each shared triangle\'s mid-triangle. B: tetrahedral tooth on the same mid-triangle.',fontsize=10)
plt.tight_layout(); plt.savefig('keyed_choices.png')
# export the two valid choices for Blender: Delian A, David & Goliath B (big and small piece each)
import trimesh
for title,big,small,labels in panels:
    if title.endswith('A') and 'Delian' in title or title.endswith('B') and 'Goliath' in title:
        for piece,lab in ((big,labels[0]),(small,labels[1])):
            m=piece.to_mesh(); V=np.array(m.vert_properties)[:,:3]; c=V.mean(0)
            trimesh.Trimesh(V-c,np.array(m.tri_verts)).export(f'keyed-{lab}.obj')
            half=piece.trim_by_plane([0,1,0],float(c[1])).to_mesh()
            trimesh.Trimesh(np.array(half.vert_properties)[:,:3]-c,np.array(half.tri_verts)).export(f'keyed-{lab}-half.obj'); open('keyed_choices.txt','w').write('\n'.join(out)+'\n'); print('\n'.join(out))
