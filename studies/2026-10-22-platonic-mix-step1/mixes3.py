# All 31 mixes of the five Platonic solids (edge 1) fill space: one uniform construction, checked.
# Space is cut by horizontal planes into slabs, one slab per "world" in the mix, stacked bottom to top:
#   D  dodecahedra (Euclid: cube of edge phi + 6 roofs) on alternate cubes of a cubic lattice of edge phi, Dogstars S
#      in the other cubes (#42); a boundary layer of cubes on each side, X = cube minus the roof that pokes in from
#      a dodecahedron, Y = cube plus the roof that a Dogstar is missing, makes the slab's faces flat;
#   C  cubes (edge 1);
#   TO the octet (edge 1), its octahedra cut into half octahedra P at both faces; an octahedron not in the mix is
#      2 P, a tetrahedron not in the mix 4 Q (face pyramids);
#   I  icosahedra in Pacioli's position in octahedra of edge L = phi^2/sqrt2, the rest of each octahedron DICTO's six
#      Admiral Caps A; a large octet between two of its (111) layer planes, its tetrahedra as 4 Q' each.
# With one world only, that world fills space by itself (the slab is simply made thick; the check uses a slab).
# Check: random points in a box crossing every slab; pieces as signed sums of convex parts (Dogstar = cube - 6 roofs,
# X = cube - roof, Y = cube + roof); every point must have total 1; dodecahedra must not overlap.
import itertools, numpy as np
from mixes import planes
phi=(1+5**.5)/2; s=2**-0.5; L=phi**2/2**.5
# ---- convex parts as (sign, normals, offsets)
def part(V,sign=1,kind=None):
    n,o=planes(np.asarray(V,float)); return (sign,n,o,kind)
# dodecahedron of edge 1 = cube [-phi/2,phi/2]^3 + 6 roofs
h=phi/2
CUBE=np.array(list(itertools.product((-h,h),repeat=3)))
def roof(axis,sg):
    # roof on the face axis=sg*h: the face's 4 corners and the ridge (two corners of the dodecahedron)
    face=[c for c in CUBE if np.isclose(c[axis],sg*h)]
    a1,a2=[(axis+1)%3,(axis+2)%3]
    # Euclid's orientation for the standard dodecahedron: ridge along a1 for axis 0 cyclic pattern (0,±1/2,±phi^2/2)
    r=[]
    for t in (0.5,-0.5):
        p=np.zeros(3); p[axis]=sg*phi**2/2; p[(axis+1)%3]=0; p[(axis+2)%3]=0
        # vertices (0, ±1/2, ±phi^2/2) cyclic: for axis z the ridge is along y; axis x ridge along z; axis y ridge along x
        p[(axis+2)%3]=t
        r.append(p)
    return np.array(face+r)
DOD=np.vstack([CUBE]+[roof(a,sg)[4:] for a in range(3) for sg in (1,-1)])
dd=[np.linalg.norm(a-b) for a,b in itertools.combinations(DOD,2)]; assert abs(min(dd)-1)<1e-9 and len(DOD)==20
from scipy.spatial import ConvexHull
assert abs(ConvexHull(DOD).volume-(15+7*5**.5)/4)<1e-9          # the dodecahedron of edge 1
ROOF={(a,sg):roof(a,sg) for a in range(3) for sg in (1,-1)}
def D_world(z0,layers=3,R=2):
    """Slab z0 <= z <= z0 + layers*phi of cubes of edge phi. Middle layers: dodecahedra D (i+j+k even) and Dogstars S.
    Outer layers: X = cube minus the roof poking in from the dodecahedron next to it; Y = cube plus the roof that pokes
    into the Dogstar next to it (so every Dogstar keeps all six roofs out and no bare cube of edge phi appears)."""
    P=[]; dods=[]
    cell=lambda i,j,k: np.array([i*phi,j*phi,z0+k*phi+h])
    mid=lambda k: 0<k<layers-1
    isD=lambda i,j,k: mid(k) and (i+j+k)%2==0
    for i,j,k in itertools.product(range(-R,R+1),range(-R,R+1),range(layers)):
        c=cell(i,j,k)
        if isD(i,j,k): P.append(part(DOD+c,1,'D')); dods.append(c); continue
        if mid(k):                                   # Dogstar: cube minus the six roofs poking in
            P.append(part(CUBE+c,1,'S'))
            for (a,sg),Rf in ROOF.items():
                d=np.zeros(3,int); d[a]=sg; n=(i+d[0],j+d[1],k+d[2])
                if isD(*n) or not mid(n[2]): P.append(part(ROOF[(a,-sg)]+cell(*n),-1))
        else:                                        # boundary layer
            sg=1 if k==0 else -1; n=(i,j,k+sg)       # the middle neighbour
            if layers<3 or not mid(n[2]): P.append(part(CUBE+c,1,'?')); continue
            if isD(*n): P.append(part(CUBE+c,1,'X')); P.append(part(ROOF[(2,-sg)]+cell(*n),-1))
            else:       P.append(part(CUBE+c,1,'Y')); P.append(part(ROOF[(2,sg)]+c,1))
    return P,dods
def C_world(z0,layers=1,R=3):
    return [part(np.array(list(itertools.product((0,1),repeat=3)),float)+np.array([i,j,z0+k]),1,'C')
            for i,j,k in itertools.product(range(-R,R+1),range(-R,R+1),range(layers))]
def TO_world(z0,mix,K=2,R=4):
    """edge-1 octet between z0 and z0 + K s; octahedra centred on the two faces become half octahedra P"""
    P=[]
    for x,y,z in itertools.product(range(-R,R+1),range(-R,R+1),range(0,K+1)):
        c=np.array([x,y,z])*s+np.array([0,0,z0])
        if (x+y+z)%2:
            V=[c+d*s for d in np.vstack([np.eye(3),-np.eye(3)])]; eq=[v for v in V if abs(v[2]-c[2])<1e-9]
            up,dn=eq+[c+np.array([0,0,s])],eq+[c-np.array([0,0,s])]
            if z==0: P.append(part(up,1,'P'))
            elif z==K: P.append(part(dn,1,'P'))
            elif 'O' in mix: P.append(part(V,1,'O'))
            else: P.append(part(up,1,'P')); P.append(part(dn,1,'P'))
        if z==K: continue
        cs=[np.array([x+i,y+j,z+k]) for i in (0,1) for j in (0,1) for k in (0,1)]
        ev=[q*s+np.array([0,0,z0]) for q in cs if q.sum()%2==0]
        if 'T' in mix: P.append(part(ev,1,'T'))
        else:
            g=np.mean(ev,0)
            for f in itertools.combinations(ev,3): P.append(part(list(f)+[g],1,'Q'))
    return P
from mixes2 import octet_pieces, RZ
def I_world(z0,layers=1,R=4):
    """large octet (edge L) between (111) layer planes z0 and z0 + layers*L*sqrt(2/3); octahedron = icosahedron + caps"""
    P=[]; top=z0+layers*L*(2/3)**.5
    for k,V,c in octet_pieces(L,R):
        V=np.array(V)@RZ.T+np.array([0,0,z0]); m=V[:,2].mean()
        if not (z0<m<top): continue
        if k=='O': P.append(part(V,1,'I+A'))
        else:
            g=V.mean(0)
            for f in itertools.combinations(V,3): P.append(part(list(f)+[g],1,"Q'"))
    return P,top
def build(mix):
    P=[]; z=0.0; dods=[]
    if 'D' in mix:
        q,dods=D_world(z); P+=q; z+=3*phi
    if 'C' in mix: P+=C_world(z); z+=1
    if mix&{'T','O'}: P+=TO_world(z,mix); z+=2*s
    if 'I' in mix:
        q,z=I_world(z); P+=q
    return P,z,dods
def check(mix,N=40000):
    P,top,dods=build(mix)
    rs=np.random.default_rng(3); X=np.column_stack([rs.uniform(-1.3,1.3,N),rs.uniform(-1.3,1.3,N),rs.uniform(0.001,top-0.001,N)])
    tot=np.zeros(N); nd=np.zeros(N,int); kinds=set()
    for sg,n,o,k in P:
        inside=np.all(X@n.T<o-1e-9,axis=1); tot+=sg*inside
        if k: kinds.add(k)
        if k=='D': nd+=inside
    return sorted(kinds),int((np.abs(tot-1)>1e-9).sum()),int((nd>1).sum()),round(top,3)
if __name__=='__main__':
    names='DICTO'
    for r in range(1,6):
        for m in itertools.combinations(names,r):
            k,bad,ov,top=check(set(m))
            print(''.join(m).ljust(6),'slab height',str(top).ljust(7),'pieces',k,'| not covered once:',bad,'| D overlaps:',ov)
