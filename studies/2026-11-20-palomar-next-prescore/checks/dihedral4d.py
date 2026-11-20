"""Dihedral angles of the six regular convex 4-polytopes, from coordinates.
Dihedral angle at a ridge = pi - (angle between outward normals of the two cells),
and the outward cell normals are the vertices of the dual, so the angle between
adjacent cell normals is the nearest-neighbour central angle of the dual's vertices.
Light: at most 600 points. Also checks theta/pi rationality by the algebraic-integer test."""
import itertools, math
import numpy as np
phi=(1+5**.5)/2
def evenperms(v):
    out=set()
    for p in itertools.permutations(range(4)):
        inv=sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j])
        if inv%2==0: out.add(tuple(v[i] for i in p))
    return out
def signs(v):
    out=set()
    for s in itertools.product([1,-1],repeat=4):
        out.add(tuple(a*b for a,b in zip(s,v)))
    return out
def v600():
    pts=set()
    for s in signs((1,1,1,1)): pts.add(tuple(x/2 for x in s))
    for p in itertools.permutations((1,0,0,0)):
        for s in signs(p): pts.add(s)
    for p in evenperms((phi/2,.5,1/(2*phi),0)):
        for s in signs(p): pts.add(tuple(round(x,12) for x in s))
    return np.array(sorted(pts))
def v16():
    return np.array([s for p in set(itertools.permutations((1,0,0,0))) for s in signs(p)])
def v8():
    return np.array(sorted(signs((1,1,1,1))))
def v24():
    return np.array(sorted({s for p in set(itertools.permutations((1,1,0,0))) for s in signs(p)}))
def v5():
    a=np.eye(5)-0.2; # 5 points in a hyperplane of R^5
    q,_=np.linalg.qr(np.ones((5,1)),mode='complete'); B=q[:,1:]
    return a@B
def v120():
    # 120-cell vertices = centres of the 600 tetrahedral cells of the 600-cell
    V=v600(); G=V@V.T; n=len(V)
    nn=np.isclose(G,np.max(G-2*np.eye(n),axis=1)[:,None])
    cells=set()
    for i in range(n):
        nb=[j for j in range(n) if nn[i,j]]
        for a,b,c in itertools.combinations(nb,3):
            if nn[a,b] and nn[a,c] and nn[b,c]: cells.add(tuple(sorted((i,a,b,c))))
    assert len(cells)==600, len(cells)
    C=np.array([V[list(c)].mean(0) for c in cells]); return C
def minangle(D):
    D=D/np.linalg.norm(D,axis=1)[:,None]; G=np.clip(D@D.T,-1,1); np.fill_diagonal(G,-2)
    return math.acos(G.max())
cases=[('5-cell',v5,'arccos(1/4)',math.acos(1/4)),
       ('tesseract (8-cell)',v16,'pi/2',math.pi/2),
       ('16-cell',v8,'2pi/3',2*math.pi/3),
       ('24-cell',v24,'2pi/3',2*math.pi/3),
       ('120-cell',v600,'4pi/5',4*math.pi/5),
       ('600-cell',v120,'arccos(-(1+3sqrt5)/8)',math.acos(-(1+3*5**.5)/8))]
ok=True
for name,dual,expr,val in cases:
    th=math.pi-minangle(dual())
    good=abs(th-val)<1e-9; ok&=good
    print(f"{name:20s} dihedral {math.degrees(th):10.6f} deg  expected {expr} = {math.degrees(val):10.6f}  {'ok' if good else 'MISMATCH'}")
print("FINAL ok" if ok else "FINAL MISMATCH")
