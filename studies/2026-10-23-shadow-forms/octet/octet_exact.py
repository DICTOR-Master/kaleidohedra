# Octet family, exact (rational arithmetic, no floats in any test): for rational t the cut planes are rational, so every corner is.
# For each t: tetrahedron piece and octahedron piece as exact polytopes (all triples of planes, keep points inside all), their
# corner/face counts and exact volumes; check 8 T + 4 O = 8 (cube of side 2), and the identities at t = 1/3 (octet) and the ends.
from fractions import Fraction as Fr
from itertools import combinations, product
import math
O = [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]
Tc = [tuple(Fr(a,2) for a in p) for p in product((1,3),repeat=3)]
def sites(R=1):
    S=[]
    for c in product(range(-R,R+1),repeat=3):
        o=tuple(2*x for x in c)
        S+=[('O',tuple(Fr(p[i]+o[i]) for i in range(3))) for p in O]+[('T',tuple(p[i]+o[i] for i in range(3))) for p in Tc]
    return S
S=sites()
dot=lambda a,b:sum(x*y for x,y in zip(a,b)); sub=lambda a,b:tuple(x-y for x,y in zip(a,b))
def det3(m): return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
def solve(A,b):
    D=det3(A)
    if D==0: return None
    out=[]
    for k in range(3):
        M=[list(r) for r in A]
        for i in range(3): M[i][k]=b[i]
        out.append(det3(M)/D)
    return tuple(out)
d2=Fr(3,4)
def cell(kind,c,t):
    w={'O':Fr(0),'T':d2*(2*t-1)}
    H=[]
    for k2,c2 in S:
        if c2==c: continue
        n=sub(c2,c)
        if dot(n,n)>4: continue
        H.append((n,(dot(c2,c2)-dot(c,c)-w[k2]+w[kind])/2))
    P=set()
    for (n1,b1),(n2,b2),(n3,b3) in combinations(H,3):
        p=solve([n1,n2,n3],[b1,b2,b3])
        if p is not None and all(dot(n,p)<=b for n,b in H): P.add(p)
    P=list(P)
    faces=[]
    for n,b in H:
        on=[p for p in P if dot(n,p)==b]
        if len(on)>=3: faces.append((n,b,on))
    return P,faces
def volume(P,faces,c):
    v=Fr(0)
    for n,b,on in faces:
        cen=[sum(float(p[k]) for p in on)/len(on) for k in range(3)]
        u=[float(on[0][k])-cen[k] for k in range(3)]; nf=[float(x) for x in n]
        w=[nf[1]*u[2]-nf[2]*u[1],nf[2]*u[0]-nf[0]*u[2],nf[0]*u[1]-nf[1]*u[0]]
        on=sorted(on,key=lambda p:math.atan2(sum((float(p[k])-cen[k])*w[k] for k in range(3)),sum((float(p[k])-cen[k])*u[k] for k in range(3))))
        for j in range(1,len(on)-1):
            v+=abs(det3([sub(on[0],c),sub(on[j],c),sub(on[j+1],c)]))
    return v/6
fails=0
def check(lab,ok):
    global fails; fails+=not ok; print(('PASS ' if ok else 'FAIL ')+lab)
for t in [Fr(1,10),Fr(1,5),Fr(1,3),Fr(1,2),Fr(4,5),Fr(9,10)]:
    PT,FT=cell('T',Tc[0],t); PO,FO=cell('O',tuple(Fr(x) for x in O[0]),t)
    vT=volume(PT,FT,Tc[0]); vO=volume(PO,FO,tuple(Fr(x) for x in O[0]))
    ft=sorted(len(f[2]) for f in FT); fo=sorted(len(f[2]) for f in FO)
    check(f't = {t}: tetra piece {len(PT)} corners, faces {dict((k,ft.count(k)) for k in set(ft))}, volume {vT}; octa piece {len(PO)} corners, faces {dict((k,fo.count(k)) for k in set(fo))}, volume {vO}; 8 T + 4 O = {8*vT+4*vO} (cube of side 2: 8)', 8*vT+4*vO==8)
    if t==Fr(1,3): check('t = 1/3 is the octet: regular tetrahedron (volume 1/3) and regular octahedron (volume 4/3), edge √2', vT==Fr(1,3) and vO==Fr(4,3) and len(PT)==4 and len(PO)==6)
    if t<Fr(1,3): check(f'  t < 1/3: tetra piece is the tetrahedron scaled by 3t (volume (3t)^3/3 = {(3*t)**3/3})', vT==(3*t)**3/3 and len(PT)==4)
    if t>Fr(1,3): check(f'  t > 1/3: octa piece is the octahedron scaled by (3/2)(1 - t) (volume {Fr(4,3)*(Fr(3,2)*(1-t))**3})', vO==Fr(4,3)*(Fr(3,2)*(1-t))**3 and len(PO)==6)
print('ALL PASS' if fails==0 else f'{fails} FAIL')
