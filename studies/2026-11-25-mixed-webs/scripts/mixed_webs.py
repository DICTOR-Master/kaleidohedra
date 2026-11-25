# DICTO · Do the Vacuus and Resonus planes of cells in a NON-lattice tiling join into a web? (25 Nov 2026)  With Claude (Anthropic).
# Exact (Fractions). Planes are affine: n·x = t with n a covector; incidence needs no metric.
# A family (one normal n up to scale) is the set of central planes n·x = n·c of the cells that carry n in their Vacuus (or Resonus).
# The family CONTINUES when every one of its planes that meets the interior of any cell (min_v n·v < t < max_v n·v) is that cell's own
# central plane (the cell carries n and n·c = t); otherwise it BREAKS (the cell is cut by a plane it does not own).
# Tilings: (1) tetrahedral-octahedral honeycomb (vertices D3, edge sqrt2); (2) trapezo-rhombic dodecahedra = Voronoi cells of hcp,
# in lattice coordinates with the rational Gram matrix (a1,a2 unit at 60 degrees, a3 vertical of length sqrt(8/3)).
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
import sys
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def prim(n):
    from math import lcm
    L=lcm(*[F(x).denominator for x in n]); m=[int(F(x)*L) for x in n]
    g=0
    for x in m: g=gcd(g,abs(x))
    m=[x//g for x in m]
    k=next(x for x in m if x!=0)
    return tuple(-x for x in m) if k<0 else tuple(m)
def hull_faces(V):
    out={}
    for i,j,k in combinations(range(len(V)),3):
        N=cross(sub(V[j],V[i]),sub(V[k],V[i]))
        if N==(0,0,0): continue
        s=[dot(N,sub(v,V[i])) for v in V]
        if all(x<=0 for x in s) or all(x>=0 for x in s):
            on=frozenset(m for m in range(len(V)) if s[m]==0); out[on]=N
    return out
def cell(c,V):
    Fc=hull_faces(V); E=set()
    for on in Fc:
        for a,b in combinations(sorted(on),2):
            # a,b form an edge if no other face-pair... edge = intersection of two faces with 2 points
            pass
    for f1,f2 in combinations(Fc,2):
        I=f1&f2
        if len(I)==2: E.add(tuple(sorted(I)))
    vac=set(); res=set()
    for a,b in E:
        n=cross(sub(V[a],c),sub(V[b],c))
        if n!=(0,0,0): vac.add(prim(n))
    for on,N in Fc.items(): res.add(prim(N))
    return dict(c=c,V=V,vac=vac,res=res,nF=len(Fc),nE=len(E))
def meets(C,n,t):
    # the plane n.x = t meets the interior of the cell (convex: one part; stella: any part, or along an internal face)
    for P in C.get('parts',[C['V']]):
        vals=[dot(n,v) for v in P]
        if min(vals)<t<max(vals): return True
    for (N,val) in C.get('inner',[]):
        if N==n and t==val: return True
    return False
def test(cells, kind, centre_box):
    fams={}
    for C in cells:
        for n in C[kind]: fams.setdefault(n,set()).add(dot(n,C['c']))
    rep={}
    for n,ts in sorted(fams.items()):
        breaks=[]
        for C in cells:
            if not centre_box(C['c']): continue
            for t in ts:
                if meets(C,n,t) and not (n in C[kind] and dot(n,C['c'])==t):
                    breaks.append((C['c'],t)); break
            if breaks: break
        rep[n]=breaks
    return rep
def report(name,cells,box):
    print('==',name)
    kinds={}
    for C in cells:
        if box(C['c']): kinds.setdefault((len(C['V']),C['nF'],C['nE']),0); kinds[(len(C['V']),C['nF'],C['nE'])]+=1
    print('  cells checked (corners, faces, edges): count', kinds)
    for kind,lab in (('vac','Vacuus'),('res','Resonus'),('both','Vacuus and Resonus together')):
        if kind=='both':
            for C in cells: C['both']=C['vac']|C['res']
        r=test(cells,kind,box)
        ok=[n for n,b in r.items() if not b]; bad={n:b[0] for n,b in r.items() if b}
        print(f'  {lab}: {len(r)} normal families; continue {len(ok)}: {ok}')
        for n,(c,t) in bad.items(): print(f'     breaks {n}: plane n.x={t} cuts the cell at {c}')
    return

# ---------- (1) tetrahedral-octahedral honeycomb ----------
R=3; cells=[]
for c in product(range(-R,R+1),repeat=3):
    if sum(c)%2==1:   # octahedral holes of D3
        cells.append(cell(tuple(F(x) for x in c),[tuple(F(c[i]+(s if i==k else 0)) for i in range(3)) for k in range(3) for s in (1,-1)]))
for c in product(range(-R,R),repeat=3):
    t=tuple(F(x)+F(1,2) for x in c)
    V=[v for v in (tuple(t[i]+s[i] for i in range(3)) for s in product((F(1,2),F(-1,2)),repeat=3)) if sum(v)%2==0]
    cells.append(cell(t,V))
box=lambda c: all(abs(x)<=1 for x in c)
oc=[C for C in cells if len(C['V'])==6][0]; te=[C for C in cells if len(C['V'])==4][0]
print('octahedron: Vacuus',sorted(oc['vac']),'Resonus',sorted(oc['res']))
print('tetrahedron: Vacuus',sorted(te['vac']),'Resonus',sorted(te['res']))
report('tetrahedral-octahedral honeycomb',cells,box)
# volume check of the patch: octahedron volume 4/3, tetrahedron 1/3 (edge sqrt2); per unit cube 1/2 oct + 2 tet... (density check)
nO=sum(1 for C in cells if len(C['V'])==6 and box(C['c'])); nT=sum(1 for C in cells if len(C['V'])==4 and box(C['c']))
print('  ratio tetrahedra:octahedra in the box', nT, nO)

# ---------- (2) trapezo-rhombic dodecahedra (hcp Voronoi) ----------
G=((F(1),F(1,2),F(0)),(F(1,2),F(1),F(0)),(F(0),F(0),F(8,3)))
def g(a,b): return sum(a[i]*G[i][j]*b[j] for i in range(3) for j in range(3))
def hcp(R):
    P=[]
    for i,j,k in product(range(-R,R+1),repeat=3):
        P.append((F(i),F(j),F(k))); P.append((F(i)+F(1,3),F(j)+F(1,3),F(k)+F(1,2)))
    return P
pts=hcp(3)
def voronoi(p):
    nb=sorted([q for q in pts if q!=p], key=lambda q:g(sub(q,p),sub(q,p)))[:30]
    # bisector: covector m=G(q-p): m.x = (g(q,q)-g(p,p))/2
    H=[(tuple(sum(G[i][j]*(q[j]-p[j]) for j in range(3)) for i in range(3)),(g(q,q)-g(p,p))/2) for q in nb]
    V=set()
    for (a,x),(b,y),(c,z) in combinations(H,3):
        M=[list(a),list(b),list(c)]; r=[x,y,z]
        det=dot(a,cross(b,c))
        if det==0: continue
        # Cramer
        def rep(col):
            Mc=[[ (r[i] if j==col else M[i][j]) for j in range(3)] for i in range(3)]
            return dot(Mc[0],cross(Mc[1],Mc[2]))
        X=tuple(rep(k)/det for k in range(3))
        if all(dot(m,X)<=s for m,s in H): V.add(X)
    return sorted(V)
cellsT=[]
for p in pts:
    if all(abs(x)<=2 for x in p): cellsT.append(cell(p,voronoi(p)))
c0=[C for C in cellsT if C['c']==(0,0,0)][0]
print('TRD at the origin: corners',len(c0['V']),'faces',c0['nF'],'edges',c0['nE'])
print('  Vacuus normals',len(c0['vac']),sorted(c0['vac']))
print('  Resonus normals',len(c0['res']),sorted(c0['res']))
boxT=lambda c: all(abs(x)<=1 for x in c)
report('trapezo-rhombic dodecahedra (hcp)',cellsT,boxT)

# ---------- (3) stellae octangulae + octahedra ----------
def octV(c): return [tuple(F(c[i]+(s if i==k else 0)) for i in range(3)) for k in range(3) for s in (1,-1)]
def tetV(t): return [v for v in (tuple(t[i]+s[i] for i in range(3)) for s in product((F(1,2),F(-1,2)),repeat=3)) if sum(v)%2==0]
cellsS=[]; owner={}
for c in product(range(-5,6),repeat=3):
    if sum(c)%2!=1: continue
    c=tuple(F(x) for x in c)
    if (c[0]%2,c[1]%2,c[2]%2)==(1,0,0):
        tets=[tuple(c[i]+s[i] for i in range(3)) for s in product((F(1,2),F(-1,2)),repeat=3)]
        for t in tets: owner.setdefault(t,[]).append(c)
        # the two big tetrahedra: corners c + 2*(outer tet apexes)
        big1=[tuple(c[i]+2*s[i] for i in range(3)) for s in product((F(1,2),F(-1,2)),repeat=3) if (s[0]*s[1]*s[2])>0]
        big2=[tuple(c[i]+2*s[i] for i in range(3)) for s in product((F(1,2),F(-1,2)),repeat=3) if (s[0]*s[1]*s[2])<0]
        A=cell(c,big1); B=cell(c,big2); O=cell(c,octV(c))
        C=dict(c=c,V=big1+big2,parts=[octV(c)]+[tetV(t) for t in tets],
               inner=[(prim(N),dot(prim(N),octV(c)[[i for i in range(6) if i in on][0]])) for on,N in hull_faces(octV(c)).items()],
               vac=A['vac']|B['vac'], vac_in=A['vac']|B['vac']|O['vac'], res=A['res']|B['res'],nF=24,nE=36)
        cellsS.append(C)
    else:
        O=cell(c,octV(c)); O['vac_in']=O['vac']; cellsS.append(O)
box3=lambda c: all(abs(x)<=2 for x in c)
cov=[len(v) for t,v in owner.items() if all(abs(x)<=3 for x in t)]
COVER_OK=set(cov)=={1}
print('stella tiling: every tetrahedron in |x|<=3 owned by exactly one stella:', set(cov)=={1}, 'tetrahedra', len(cov))
st=[C for C in cellsS if 'parts' in C][0]
print('stella: Vacuus (outer edges)',sorted(st['vac']),' with inner edges',sorted(st['vac_in']),' Resonus',sorted(st['res']))
report('stellae octangulae + octahedra (Vacuus from outer edges)',cellsS,box3)
for C in cellsS: C['vac']=C['vac_in']
print('-- same tiling, Vacuus including the inner edges:')
r=test(cellsS,'vac',box3); print('  ', {n:('continues' if not b else 'breaks at '+str(b[0])) for n,b in r.items()})
# ---------- control: the cube tiling (lattice-webs study: Vacuus and Resonus continue) and the rhombic dodecahedron ----------
cc=[cell(tuple(F(x) for x in c),[tuple(F(c[i])+s[i] for i in range(3)) for s in product((F(1,2),F(-1,2)),repeat=3)]) for c in product(range(-3,4),repeat=3)]
report('CONTROL cube tiling',cc,lambda c: all(abs(x)<=1 for x in c))
rdV=lambda c:[tuple(F(c[i]+(s if i==k else 0)) for i in range(3)) for k in range(3) for s in (1,-1)]+[tuple(F(c[i])+s[i] for i in range(3)) for s in product((F(1,2),F(-1,2)),repeat=3)]
cr=[cell(tuple(F(x) for x in c),rdV(c)) for c in product(range(-3,4),repeat=3) if sum(c)%2==0]
report('CONTROL rhombic dodecahedron tiling',cr,lambda c: all(abs(x)<=1 for x in c))
ok_cube=all(not b for k in ('vac','res') for b in test(cc,k,lambda c: all(abs(x)<=1 for x in c)).values())
ok_rd=all(not b for k in ('vac','res') for b in test(cr,k,lambda c: all(abs(x)<=1 for x in c)).values())
print('CONTROLS cube', ok_cube, 'rhombic dodecahedron', ok_rd, 'stella cover', COVER_OK)
print('FINAL ok' if (ok_cube and ok_rd and COVER_OK) else 'FINAL FAIL (a control or the stella cover failed)')
