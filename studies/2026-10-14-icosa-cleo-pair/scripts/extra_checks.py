"""(1) base-corner parallelepiped middle piece is congruent to A (distance-matrix
match under a vertex permutation + orientation), (2) the 20 rhombohedra round the
centre: shared vs outer faces (rhombic hexecontahedron check)."""
import numpy as np, itertools, json
phi=(1+5**.5)/2; V=[]
for a in (1,-1):
    for b in (phi,-phi): V+=[(0,a,b),(a,b,0),(b,0,a)]
V=np.array(V)/5**.5; E=2/5**.5
F20=[f for f in itertools.combinations(range(12),3) if all(abs(np.linalg.norm(V[p]-V[q])-E)<1e-9 for p,q in itertools.combinations(f,2))]
u,v,w=V[list(F20[0])]
A=np.array([u,v,w,u+v,v+w,w+u]); B=np.array([np.zeros(3),v,w,v-u,w-u,v+w-u])
D=lambda X:np.linalg.norm(X[:,None]-X[None],axis=2)
match=[p for p in itertools.permutations(range(6)) if np.allclose(D(A),D(B[list(p)]))]
# rigid map from A to B[p]
p=match[0]; X=A-A.mean(0); Y=B[list(p)]-B[list(p)].mean(0)
U,S,Wt=np.linalg.svd(X.T@Y); Rm=(U@Wt).T
out={"perms_matching_distances":len(match),"rigid_fit_residual":float(np.abs(X@Rm.T-Y).max()),"det":float(np.linalg.det(Rm))}
faces={}
for f in F20:
    a,b,c=V[list(f)]; o=np.zeros(3)
    for P,Q,Rr in ((a,b,c),(b,c,a),(c,a,b)):
        for quad in ([o,P,P+Q,Q],[Rr,Rr+P,Rr+P+Q,Rr+Q]):
            k=tuple(sorted(tuple(np.round(x,7)) for x in quad)); faces[k]=faces.get(k,0)+1
out["faces_shared"]=sum(n==2 for n in faces.values()); out["faces_outer"]=sum(n==1 for n in faces.values())
out["outer_vertex_radii"]=sorted(set(round(float(np.linalg.norm(x)),6) for k,n in faces.items() if n==1 for x in k))
print(json.dumps(out,indent=1))
