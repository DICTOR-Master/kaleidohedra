# Step 2: the 8 mixes that contain the icosahedron I (edge 1), with C, T, O (edge 1).
# The icosahedron sits in Pacioli's position in an octahedron of edge L = phi^2/sqrt2; the rest of that octahedron is
# DICTO's six Admiral Caps (F21, connector A). These octahedra form a large octet of edge L whose tetrahedra are split
# into 4 face pyramids each (connector Q', the tetrahedron face pyramid at size L). The large octet is turned so
# that one of its (111) layer planes is horizontal: above the plane z = H it fills the half-space with whole pieces.
# Below z = H: the step-1 filling of the rest of the mix (edge 1), whose top plane z = H cuts octahedra into half
# octahedra P (as at the cube seam). Faces need not match across z = H (the two lattices differ in size).
# Check: random points each covered by exactly one piece; every solid of the mix, and no other, appears.
import itertools, numpy as np
from mixes import planes
s=2**-0.5; phi=(1+5**.5)/2; L=phi**2/2**.5
def rot_to_z(n):
    n=np.array(n,float); n/=np.linalg.norm(n); z=np.array([0,0,1.0]); ax=np.cross(n,z); c=n@z; S=np.linalg.norm(ax)
    ax/=S; K=np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]]); return np.eye(3)+S*K+(1-c)*K@K
RZ=rot_to_z((1,1,1))
def octet_pieces(scale,R):
    out=[]; rng=range(-R,R+1)
    for x,y,z in itertools.product(rng,rng,rng):
        c=np.array([x,y,z])*s
        if (x+y+z)%2: out.append(('O',[(c+d*s)*scale for d in np.vstack([np.eye(3),-np.eye(3)])],c*scale))
        cs=[np.array([x+i,y+j,z+k]) for i in (0,1) for j in (0,1) for k in (0,1)]
        out.append(('T',[q*s*scale for q in cs if q.sum()%2==0],None))
    return out
def build2(mix,H=0.0,R=4):
    rest=mix-{'I'}; out=[]
    # upper: the large octet (edge L), (111) horizontal, layer plane at z = H
    for k,V,c in octet_pieces(L,R):
        V=np.array(V)@RZ.T+np.array([0,0,H])
        if rest and V[:,2].mean()<H: continue
        if k=='O': out.append(('I+A',V))          # icosahedron + 6 Admiral Caps fill this octahedron exactly
        else:
            g=V.mean(0)
            for f in itertools.combinations(V,3): out.append(("Q'",np.array(list(f)+[g])))
    if not rest: return out
    # lower: step-1 filling of `rest` below z = H (H = 0 here); edge-1 octet or cubes
    rng=range(-R,R+1)
    if rest=={'C'}:
        for i,j,k in itertools.product(rng,rng,range(-R,0)):
            out.append(('C',np.array([[i+a,j+b,k+c_] for a in (0,1) for b in (0,1) for c_ in (0,1)],float)))
        return out
    seam='C' in rest
    for x,y,z in itertools.product(rng,rng,rng):
        if z>0 or (seam and z<0): continue      # octet occupies 0 <= z <= ... below H=0? (see below)
    # place the edge-1 octet slab between z = -K s and z = 0 (top cut), cubes below z = -K s when C is in the mix
    K=2
    for x,y,z in itertools.product(rng,rng,range(-K-1,1)):
        c=np.array([x,y,z])*s
        if (x+y+z)%2:
            V=[c+d*s for d in np.vstack([np.eye(3),-np.eye(3)])]; eq=[v for v in V if abs(v[2]-c[2])<1e-9]
            top=c+np.array([0,0,s]); bot=c-np.array([0,0,s])
            if z==0: out.append(('P',np.array(eq+[bot]))); 
            elif z==-K and seam: out.append(('P',np.array(eq+[top])))
            elif z<-K and seam: pass
            elif 'O' in rest: out.append(('O',np.array(V)))
            else: out.append(('P',np.array(eq+[top]))); out.append(('P',np.array(eq+[bot])))
        if z>=0 or (seam and z<-K): continue
        cs=[np.array([x+i,y+j,z+k]) for i in (0,1) for j in (0,1) for k in (0,1)]
        ev=[q*s for q in cs if q.sum()%2==0]
        if 'T' in rest: out.append(('T',np.array(ev)))
        else:
            g=np.mean(ev,0)
            for f in itertools.combinations(ev,3): out.append(('Q',np.array(list(f)+[g])))
    if not seam:   # no cubes: the edge-1 octet continues all the way down
        for x,y,z in itertools.product(rng,rng,range(-R-3,-K-1)):
            c=np.array([x,y,z])*s
            if (x+y+z)%2:
                V=[c+d*s for d in np.vstack([np.eye(3),-np.eye(3)])]; eq=[v for v in V if abs(v[2]-c[2])<1e-9]
                if 'O' in rest: out.append(('O',np.array(V)))
                else: out.append(('P',np.array(eq+[c+np.array([0,0,s])]))); out.append(('P',np.array(eq+[c-np.array([0,0,s])])))
            cs=[np.array([x+i,y+j,z+k]) for i in (0,1) for j in (0,1) for k in (0,1)]
            ev=[q*s for q in cs if q.sum()%2==0]
            if 'T' in rest: out.append(('T',np.array(ev)))
            else:
                g=np.mean(ev,0)
                for f in itertools.combinations(ev,3): out.append(('Q',np.array(list(f)+[g])))
    else:          # cubes below z = -K s, on the seam squares
        u=np.array([s,s,0]); v=np.array([s,-s,0]); w=np.array([0,0,1.0]); z0=-K*s
        for i,j,k in itertools.product(range(-2*R,2*R+1),range(-2*R,2*R+1),range(-R,0)):
            o=i*u+j*v+(k)*w+np.array([0,0,z0])
            out.append(('C',np.array([o+a*u+b*v+c_*w for a in (0,1) for b in (0,1) for c_ in (0,1)])))
    return out
def check(mix,N=30000):
    pcs=build2(mix); kinds=sorted({k for k,_ in pcs})
    rs=np.random.default_rng(2); X=rs.uniform(-1.5,1.5,(N,3)); cnt=np.zeros(N,int)
    for k,V in pcs:
        V=np.asarray(V); c=V.mean(0)
        if np.abs(c).max()>4: continue
        n,o=planes(V); cnt+=np.all(X@n.T<o-1e-7,axis=1)
    return kinds,(cnt!=1).sum()
if __name__=='__main__':
    for m in [{'I'},{'I','C'},{'I','T'},{'I','O'},{'I','T','O'},{'I','C','T'},{'I','C','O'},{'I','C','T','O'}]:
        k,b=check(m); print(''.join(sorted(m)).ljust(5),'pieces:',k,'| not covered exactly once:',b)
