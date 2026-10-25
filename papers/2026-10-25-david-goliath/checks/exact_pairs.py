# Exact checks for the David and Goliath paper (2026-10-25): exact arithmetic in Q(sqrt3) (pairs of Fractions a + b*sqrt3).
# (1) A15 at lambda = 3/4: Goliath/David face types by neighbour, and the shift by (1,1,1) onto the classical Cr12 icosahedron / Cr4 tetrahedron.
# (2) Rock salt at lambda = 4 - 2*sqrt3 (Na-Cl distance 1): one edge length, chamfered-cube face vector + cube, volumes.
# (3) Zinc blende at lambda = +1 and -1 (cubic cell edge 4): capped octahedron + regular tetrahedron, edges^2, volumes.
from fractions import Fraction as F
import itertools, functools
class Q:
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): o=o if isinstance(o,Q) else Q(o); return Q(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return Q(-s.a,-s.b)
    def __sub__(s,o): return s+(-(o if isinstance(o,Q) else Q(o)))
    def __rsub__(s,o): return Q(o)-s
    def __mul__(s,o): o=o if isinstance(o,Q) else Q(o); return Q(s.a*o.a+3*s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def __truediv__(s,o):
        o=o if isinstance(o,Q) else Q(o); n=o.a*o.a-3*o.b*o.b; return s*Q(o.a/n,-o.b/n)
    def sign(s):
        a,b=s.a,s.b
        if a>=0 and b>=0: return 0 if (a==0 and b==0) else 1
        if a<=0 and b<=0: return -1
        d=a*a-3*b*b
        return (1 if a>0 else -1) if d>0 else ((1 if b>0 else -1) if d<0 else 0)
    def __eq__(s,o): return (s-o).sign()==0
    def __le__(s,o): return (s-o).sign()<=0
    def __lt__(s,o): return (s-o).sign()<0
    def __hash__(s): return hash((s.a,s.b))
    def __repr__(s): return (str(s.a) if s.b==0 else f'{s.a}{"+" if s.b>=0 else ""}{s.b}*sqrt3')
Z=Q(0)
def dot(u,v): return functools.reduce(lambda x,y:x+y,[x*y for x,y in zip(u,v)],Z)
def sub(u,v): return tuple(x-y for x,y in zip(u,v))
def det3(m): return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
def solve(A,b):
    D=det3(A)
    if D==Z: return None
    out=[]
    for k in range(3):
        M=[list(r) for r in A]
        for i in range(3): M[i][k]=b[i]
        out.append(det3(M)/D)
    return tuple(out)
def cell(p,wp,sites,R2):
    P=[]
    for q,wq,kind in sites:
        d=sub(q,p); dd=dot(d,d)
        if dd==Z or R2<dd: continue
        P.append((tuple(2*x for x in d), dot(q,q)-dot(p,p)-wq+wp, q, kind))
    V=[]
    for a,b,c in itertools.combinations(P,3):
        x=solve([a[0],b[0],c[0]],[a[1],b[1],c[1]])
        if x is None or x in V: continue
        if all(dot(n,x)<=r for n,r,_,_ in P): V.append(x)
    faces=[]
    for n,r,q,kind in P:
        on=[v for v in V if dot(n,v)==r]
        if len(on)>=3: faces.append((n,on,q,kind))
    return V,faces
def order(n,pts):
    fc=tuple(functools.reduce(lambda x,y:x+y,[v[i] for v in pts],Z)/len(pts) for i in range(3)); ref=sub(pts[0],fc)
    def cr(u,w): return (u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
    def half(a):
        u=sub(a,fc); s=dot(cr(ref,u),n); return 0 if (Z<s or (s==Z and Z<dot(u,ref))) else 1
    def cmp(a,b):
        s=dot(cr(sub(a,fc),sub(b,fc)),n).sign(); return -s
    return sorted(pts,key=functools.cmp_to_key(lambda a,b:(half(a)-half(b)) or cmp(a,b)))
def info(V,faces):
    E={}
    for (n1,f1,_,_),(n2,f2,_,_) in itertools.combinations(faces,2):
        sh=[v for v in f1 if v in f2]
        if len(sh)==2: E[frozenset(sh)]=dot(sub(*sh),sub(*sh))
    c=tuple(functools.reduce(lambda x,y:x+y,[v[i] for v in V],Z)/len(V) for i in range(3))
    vol=Z
    for n,f,_,_ in faces:
        pts=order(n,f)
        for i in range(1,len(pts)-1):
            d=det3([sub(pts[0],c),sub(pts[i],c),sub(pts[i+1],c)]); vol=vol+(d if Z<=d else -d)/6
    deg={}
    for e in E:
        for v in e: deg[repr(v)]=deg.get(repr(v),0)+1
    L2=sorted(set(E.values()),key=lambda q:(q.a+q.b*F(17320508,10000000)))
    return dict(corners=len(V),faces=len(faces),face_sizes=sorted(len(f) for _,f,_,_ in faces),edges=len(E),
                edge2={repr(l):sum(1 for x in E.values() if x==l) for l in L2},deg=sorted(deg.values()),vol=vol,E=E)
ok=[]
def check(name,cond): ok.append(cond); print(('PASS ' if cond else 'FAIL ')+name)
Fq=lambda *t: tuple(Q(F(x)) for x in t)
# ---------- (1) A15 ----------
lam=Q(F(3,4))
Si=[(0,0,0),(1,1,1)]; Cr=[(F(1,2),0,1),(F(3,2),0,1),(1,F(1,2),0),(1,F(3,2),0),(0,1,F(1,2)),(0,1,F(3,2))]
sites=[]
for t in itertools.product(range(-2,3),repeat=3):
    sites+=[(Fq(*(2*t[i]+s[i] for i in range(3))),lam,'Si') for s in Si]+[(Fq(*(2*t[i]+c[i] for i in range(3))),Z,'Cr') for c in Cr]
crset={q for q,w,k in sites if k=='Cr'}
G,gf=cell(Fq(0,0,0),lam,sites,Q(6)); gi=info(G,gf)
print('Goliath',{k:v for k,v in gi.items() if k!='E'})
tri=lambda f:sorted([dot(sub(f[i],f[j]),sub(f[i],f[j])) for i,j in [(0,1),(1,2),(0,2)]],key=lambda q:q.a)
byk={}
for n,f,q,k in gf:
    key=(k,repr(dot(q,q)),tuple(repr(x) for x in tri(f))); byk[key]=byk.get(key,0)+1
print(' Goliath faces by neighbour (kind, dist^2, edge^2s):',byk)
check('Goliath: 20 triangles, 12 corners deg 5, 30 edges, vol 7/2',gi['face_sizes']==[3]*20 and gi['deg']==[5]*12 and gi['edges']==30 and gi['vol']==Q(F(7,2)))
check('Goliath edges: 6 of edge^2 1, 24 of edge^2 3/2',gi['edge2']=={'1':6,'3/2':24})
check('Goliath: 12 faces to Cr (edge^2 1,3/2,3/2), 8 faces to Si@3 (equilateral edge^2 3/2)',
      byk=={('Cr','5/4',('1','3/2','3/2')):12,('Si','3',('3/2','3/2','3/2')):8})
J={Fq(*v) for a in (F(1,2),F(-1,2)) for b in (1,-1) for v in [(0,a,b),(b,0,a),(a,b,0)]}
check('Goliath corners = (0, ±1/2, ±1) cyclic (Jessen set, halved)',set(G)==J)
sh=lambda v,d: tuple(x+Q(F(y)) for x,y in zip(v,d))
check('Goliath + (1,1,1): all 12 corners are Cr sites (the Cr12 icosahedron of the Si at (1,1,1))',all(sh(v,(1,1,1)) in crset for v in G))
cr12={q for q in crset if dot(sub(q,Fq(1,1,1)),sub(q,Fq(1,1,1)))==Q(F(5,4))}
check('the Si at (1,1,1) has exactly 12 Cr at dist^2 5/4 and they are Goliath + (1,1,1)',cr12=={sh(v,(1,1,1)) for v in G} and len(cr12)==12)
D,df=cell(Fq(*Cr[0]),Z,sites,Q(6)); di=info(D,df)
print('David',{k:v for k,v in di.items() if k!='E'})
check('David: tetrahedron, vol 1/6, 2 edges of edge^2 1 (opposite) + 4 of 3/2',di['faces']==4 and di['vol']==Q(F(1,6)) and di['edge2']=={'1':2,'3/2':4}
      and all(len(e1&e2)==0 for e1 in di['E'] for e2 in di['E'] if e1!=e2 and di['E'][e1]==Q(1) and di['E'][e2]==Q(1)))
cen=tuple(functools.reduce(lambda x,y:x+y,[v[i] for v in D],Z)/4 for i in range(3))
check('David centroid = its Cr site',cen==Fq(*Cr[0]))
check('David + (1,1,1): 4 corners are Cr sites (a Cr4 tetrahedron)',all(sh(v,(1,1,1)) in crset for v in D))
check('2*7/2 + 6*1/6 = 8 = cube of edge 2',2*gi['vol']+6*di['vol']==Q(8))
# ---------- (2) rock salt ----------
lam=Q(4,-2)  # 4 - 2 sqrt3 = w_Na - w_Cl; Na at even coordinate sum, Cl at odd
sites=[(Fq(x,y,z),lam if (x+y+z)%2==0 else Z,'Na' if (x+y+z)%2==0 else 'Cl') for x,y,z in itertools.product(range(-3,4),repeat=3)]
A,af=cell(Fq(0,0,0),lam,sites,Q(3)); ai=info(A,af)
B,bf=cell(Fq(1,0,0),Z,sites,Q(3)); bi=info(B,bf)
print('rock salt Na',{k:v for k,v in ai.items() if k!='E'}); print('rock salt Cl',{k:v for k,v in bi.items() if k!='E'})
e2=Q(21,-12)  # (2 sqrt3 - 3)^2 = 21 - 12 sqrt3
check('rock salt Na cell: 6 squares + 12 hexagons, 32 corners, 48 edges',ai['face_sizes']==[4]*6+[6]*12 and ai['corners']==32 and ai['edges']==48)
check('rock salt: every edge of both cells has length 2 sqrt3 - 3',set(ai['E'].values())=={e2} and set(bi['E'].values())=={e2})
check('rock salt Cl cell: cube (6 squares)',bi['face_sizes']==[4]*6 and bi['corners']==8)
check('rock salt: Na vol + Cl vol = 2 (cell of edge 2 holds 4 + 4)',ai['vol']+bi['vol']==Q(2))
print(' rock salt volumes: Na',ai['vol'],' Cl',bi['vol'])
# ---------- (3) zinc blende ----------
for lv in (1,-1):
    lam=Q(lv); sites=[]
    for x,y,z in itertools.product(range(-4,5,2),repeat=3):
        if (x+y+z)%4==0:
            sites.append((Fq(x,y,z),lam,'Zn')); sites.append((Fq(x+1,y+1,z+1),Z,'S'))
    A,af=cell(Fq(0,0,0),lam,sites,Q(11)); ai=info(A,af)
    B,bf=cell(Fq(1,1,1),Z,sites,Q(11)); bi=info(B,bf)
    big,small=(ai,bi) if lv==1 else (bi,ai)
    print(f'zinc blende lambda={lv}: big',{k:v for k,v in big.items() if k!='E'},' small',{k:v for k,v in small.items() if k!='E'})
    check(f'zinc blende {lv:+d}: small cell regular tetrahedron, edge^2 8, vol 8/3',small['faces']==4 and small['edge2']=={'8':6} and small['vol']==Q(F(8,3)))
    check(f'zinc blende {lv:+d}: big cell 16 triangles, corners deg 3 x4 + 6 x6, edges^2 8 (x12) and 3 (x12), vol 40/3',
          big['face_sizes']==[3]*16 and big['deg']==[3]*4+[6]*6 and big['edge2']=={'3':12,'8':12} and big['vol']==Q(F(40,3)))
    check(f'zinc blende {lv:+d}: 4*8/3 + 4*40/3 = 64 = cube of edge 4',4*big['vol']+4*small['vol']==Q(64))
    Vb,ctr,other=(A,(0,0,0),(1,1,1)) if lv==1 else (B,(1,1,1),(0,0,0))   # big cell corners, its site, sign of the small-kind offset
    rel={tuple(x-Q(c) for x,c in zip(v,ctr)) for v in Vb}
    octa={Fq(*v) for v in [(2,0,0),(-2,0,0),(0,2,0),(0,-2,0),(0,0,2),(0,0,-2)]}
    s1={Fq(*v) for v in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]}; s2={tuple(-x for x in v) for v in s1}
    small_dirs=s1 if lv==1 else s2   # directions from the big site to its 4 small-kind neighbours
    check(f'zinc blende {lv:+d}: big cell = octahedron (±2,0,0) perms + 4 cap apices at the 4 empty tetrahedral holes (opposite the small sites)',
          rel==octa|({tuple(-x for x in v) for v in small_dirs}))
print(f'{sum(ok)} PASS, {len(ok)-sum(ok)} FAIL')
