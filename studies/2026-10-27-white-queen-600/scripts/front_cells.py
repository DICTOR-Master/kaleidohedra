import json, numpy as np, sys
D=json.load(open(sys.argv[1])); V=np.array(D['vertices']); C=D['cells']
phi=(1+5**.5)/2
def num(q): return float(eval(q[0]))+float(eval(q[1]))*5**.5
for k,d in D['directions'].items():
    u=np.array([num(x) for x in d['d_exact']]); u/=np.linalg.norm(u)
    # orthonormal basis of complement
    Q,_=np.linalg.qr(np.column_stack([u,np.eye(4)])); B=Q[:,1:4]
    P=V@B
    front=back=side=0; shapes=set(); vol=0
    for c in C:
        n=V[c].mean(0); s=n@u   # outward normal of a cell of a regular polytope ~ its centre
        if abs(s)<1e-9: side+=1; continue
        if s>0:
            front+=1
            p=P[c]; vol+=abs(np.linalg.det(p[1:]-p[0]))/6
            L=sorted(round(float(np.linalg.norm(p[i]-p[j])),6) for i in range(4) for j in range(i+1,4)); shapes.add(tuple(L))
        else: back+=1
    from scipy.spatial import ConvexHull
    hv=ConvexHull(P).volume
    print(f"{k}: front {front}, back {back}, side (flat) {side}; front cells cover volume {vol:.6f} vs hull {hv:.6f}; distinct front tetra shapes {len(shapes)}")
