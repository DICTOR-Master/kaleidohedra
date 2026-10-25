# Keying rule test on the Delian bond (DICTO 2026-10-25): move a triangular cap from Samson (tetrahedron-site piece) into Delilah
# (octahedron-site piece) through one shared triangle. Cap = pyramid on the triangle scaled by s about the face centre, apex at depth
# d*(inradius of Samson toward its centre). The web is unchanged iff the cap meets Samson's boundary ONLY in its base (base strictly
# inside the shared face, apex strictly inside Samson): then no other face is touched. Exact (sympy). Output: the allowed (s, d) region
# boundary along s, and keyed volumes/areas at sample keys. Pieces from krp-core delian-bond.js formulas (tetPiece, t >= 1/3), cube side 2.
import sympy as sp, itertools
t=1-sp.Rational(2,3)*2**sp.Rational(-1,3)          # the Delian bond
a=sp.Rational(3,2)*(1-t)
k=sp.Matrix([0,0,0]); q=k+sp.Matrix([sp.Rational(1,2)]*3)
C=[sp.Matrix([x,y,z]) for x in (0,1) for y in (0,1) for z in (0,1)]
odd=lambda p: (sum(p)%2)==1
even=[c for c in C if not odd(c)]; octs=[c for c in C if odd(c)]
P=even+[o+a*(v-o) for o in octs for v in even if (v-o).norm()<1.0001]   # Samson's corners (tetPiece, t >= 1/3)
P=[sp.nsimplify(sp.simplify(p)) for p in P]
# faces of Samson: hull via planes through triples with all points on one side
def plane(a,b,c):
    n=(b-a).cross(c-a); return n, n.dot(a)
faces={}
for A,B,Cc in itertools.combinations(range(len(P)),3):
    n,d0=plane(P[A],P[B],P[Cc])
    if n.norm()==0: continue
    s=[sp.simplify(n.dot(p)-d0) for p in P]
    if all(v<=0 for v in s) or all(v>=0 for v in s):
        on=tuple(sorted(i for i,v in enumerate(s) if v==0))
        faces[on]=(n if all(v<=0 for v in s) else -n)
tri=[f for f in faces if len(f)==3]
print('Samson: corners',len(P),'faces',len(faces),'triangles (oct-tet faces)',len(tri))
F=tri[0]; A_,B_,C_=[P[i] for i in F]
cen=(A_+B_+C_)/3; n=faces[F]; n=n/sp.sqrt(n.dot(n))       # outward unit normal of that face
# Samson's inradius-like depth toward q along -n: distance from face plane to the centre q
depth_q=sp.simplify(n.dot(cen-q))
print('distance face -> Samson centre:', sp.nsimplify(depth_q), float(depth_q))
def ok(s,d):
    base=[cen+s*(v-cen) for v in (A_,B_,C_)]; apex=cen-d*depth_q*n
    # apex strictly inside Samson: strictly behind every face plane
    inside=all(sp.simplify(faces[f].dot(apex)-faces[f].dot(P[f[0]]))<0 for f in faces)
    return inside and 0<s<1
print('s, largest d (of the way to the centre) with the cap inside Samson:')
for s in [sp.Rational(1,4),sp.Rational(1,2),sp.Rational(3,4)]:
    lo,hi=sp.Rational(0),sp.Rational(1)
    for _ in range(30):
        mid=(lo+hi)/2
        (lo,hi)=(mid,hi) if ok(s,mid) else (lo,mid)
    print(' s =',s,' d_max ≈',float(lo))
# sample key: s = 1/2, d = 1/2
s,d=sp.Rational(1,2),sp.Rational(1,2)
base=[cen+s*(v-cen) for v in (A_,B_,C_)]; apex=cen-d*depth_q*n
capV=sp.simplify(abs((base[1]-base[0]).cross(base[2]-base[0]).dot(apex-base[0]))/6)
print('sample key s=1/2, d=1/2: inside =',ok(s,d),' cap volume =',sp.nsimplify(capV),float(capV))
print('RESULT: web unchanged for every key inside the region above (cap touches only the shared triangle).')
