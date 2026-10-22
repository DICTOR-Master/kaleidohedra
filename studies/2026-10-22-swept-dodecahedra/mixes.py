# Step 1 of DICTO's idea "any mix of the Platonic solids fills space" (2026-10-22): the 7 mixes of the cube C,
# tetrahedron T and octahedron O, all at edge 1, with connector pieces allowed and no face-to-face condition.
#
# Construction. The octet (T + O, edge 1): vertices at the fcc points s(x,y,z), x+y+z even, s = 1/sqrt2;
# octahedra centred at the odd points; a tetrahedron on the 4 even corners of every small cube of side s.
# The plane z = 0 is tiled exactly by the square equators (edge 1) of the octahedra centred in it, so cutting the
# octet there leaves square pyramids P (half octahedra), and edge-1 cubes below meet those squares exactly.
# Connectors (both cut from the solids themselves): P = half octahedron (square pyramid), Q = face pyramid of the
# tetrahedron (a quarter tetrahedron, as in #44). An octahedron not in the mix is split into 2 P, a tetrahedron
# into 4 Q. Check: random points in a box are each covered by exactly one piece (interiors), and every solid
# of the mix (and no other) appears.
import itertools, numpy as np, sys
s=2**-0.5
def planes(V):
    V=np.array(V,float); c=V.mean(0); P=[]
    for a,b,d in itertools.combinations(range(len(V)),3):
        n=np.cross(V[b]-V[a],V[d]-V[a]); L=np.linalg.norm(n)
        if L<1e-9: continue
        n=n/L; o=n@V[a]
        if n@c>o: n,o=-n,-o
        if np.all(V@n<=o+1e-9) and not any(np.allclose(n,q[0]) and abs(o-q[1])<1e-9 for q in P): P.append((n,o))
    return np.array([q[0] for q in P]),np.array([q[1] for q in P])
def build(mix,R=4):
    out=[]   # (kind, vertices)
    rng=range(-R,R+1)
    octa=lambda c:[c+d*s for d in np.vstack([np.eye(3),-np.eye(3)])]
    seam='C' in mix and mix!={'C'}
    if mix=={'C'}:
        for i,j,k in itertools.product(rng,rng,rng):
            out.append(('C',[np.array([i,j,k])+np.array(v) for v in itertools.product((0,1),repeat=3)]))
        return out
    for x,y,z in itertools.product(rng,rng,rng):
        if seam and z<0: continue
        c=np.array([x,y,z])*s
        if (x+y+z)%2:                                    # octahedron centre
            V=octa(c); eq=[v for v in V if abs(v[2]-c[2])<1e-9]; top=c+np.array([0,0,s]); bot=c-np.array([0,0,s])
            if seam and z==0: out.append(('P',eq+[top]))
            elif 'O' in mix: out.append(('O',V))
            else: out.append(('P',eq+[top])); out.append(('P',eq+[bot]))
        # tetrahedron in the small cube with lowest corner (x,y,z)
        cs=[np.array([x+i,y+j,z+k]) for i in (0,1) for j in (0,1) for k in (0,1)]
        ev=[q*s for q in cs if q.sum()%2==0]
        if 'T' in mix: out.append(('T',ev))
        else:
            g=np.mean(ev,0)
            for f in itertools.combinations(ev,3): out.append(('Q',list(f)+[g]))
    if seam:   # cubes below z = 0, on the squares of the seam (a square lattice turned 45 degrees)
        u=np.array([s,s,0]); v=np.array([s,-s,0]); w=np.array([0,0,1.0])   # the seam squares: corners at the even points of z = 0
        for i,j,k in itertools.product(range(-2*R,2*R+1),range(-2*R,2*R+1),range(-R,0)):
            o=i*u+j*v+k*w
            out.append(('C',[o+a*u+b*v+c_*w for a in (0,1) for b in (0,1) for c_ in (0,1)]))
    return out
def check(mix,N=40000,seed=1):
    pcs=build(mix); kinds=sorted({k for k,_ in pcs})
    PL=[(k,*planes(V)) for k,V in pcs]
    rs=np.random.default_rng(seed); X=rs.uniform(-1.6,1.6,(N,3))
    cnt=np.zeros(N,int)
    for k,n,o in PL:
        cnt+=np.all(X@n.T<o-1e-7,axis=1)
    bad=(cnt!=1).sum()
    # points on boundaries (within 1e-7) are measure zero; count ones
    return kinds,bad
if __name__=='__main__':
    for m in [{'C'},{'T'},{'O'},{'T','O'},{'C','T'},{'C','O'},{'C','T','O'}]:
        kinds,bad=check(m)
        print(''.join(sorted(m)).ljust(4),'pieces used:',kinds,'| points not covered exactly once:',bad)
