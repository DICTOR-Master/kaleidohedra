# Dictosphere, CLEO sphere, Icosahedral Cleo, wheels counting, breathing limit (Fable review for DICTO, 2026-10-14).
# DICTO · dictospheres.com
import numpy as np, itertools, math
from scipy.spatial import ConvexHull, SphericalVoronoi
phi=(1+5**.5)/2; deg=180/math.pi
def ang(u,v): return math.acos(np.clip(np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v),-1,1))*deg
print("== dictosphere")
P=[np.array(v,float) for v in itertools.product((1,-1),repeat=3)]
Q=[s*np.eye(3)[i] for i in range(3) for s in (1,-1)]
pts=np.array([p/np.linalg.norm(p) for p in P+Q])
sv=SphericalVoronoi(pts); sv.sort_vertices_of_regions()
reg=sv.regions[0]; V=sv.vertices[reg]   # a triangle port's region
arcs=[ang(V[i],V[(i+1)%len(V)]) for i in range(len(V))]
print("triangle region corners",len(V),"arc lengths (deg)",np.round(arcs,4))
a=sorted(set(np.round(arcs,6))); print("arc ratio short/long",a[0]/a[-1])
R=8.4/(109.4712206/deg); print("radius from 8.4 cm tape over 109.47 deg:",R)
print("sphere arcs cm",[x/deg*R for x in a])
s=3**.5; long=2**.5*(s-1); short=2**.5*(2-s); print("flat tangent solid sides (inradius 1)",long,short,"ratio",short/long,"cm",long*R,short*R)
# Voronoi = central projection of the tangent solid: vertex directions of tangent solid
# tangent solid vertex on triangle face (1,1,1)/sqrt3 between faces x=1 and two triangles: solve
A=np.array([[1,0,0],[1,1,1],[1,1,-1]],float); b=np.array([1,s,s]); x=np.linalg.solve(A,b)
print("tangent-solid corner direction vs Voronoi corner (min angle, deg):",min(ang(x,v) for v in sv.vertices))
# port gaps with 3 cm ports
for nm,th in [("tri-tri",math.acos(1/3)*deg),("sq-sq",90)]:
    print(nm,"centre arc",th/deg*R,"rim-to-rim along surface (3 cm ports)",th/deg*R-3, "chord",2*R*math.sin(th/2/deg))
print("areas on tangent solid: square",long**2,"hexagon",3**.5/4*((long+2*short)**2-3*short**2))
print("\n== CLEO sphere")
a=1/phi; Vid=(45+17*5**.5)/6*a**3
pent_area=0.25*math.sqrt(5*(5+2*5**.5))*a*a; Rp=a/(2*math.sin(math.pi/5)); hp=math.sqrt(1-Rp**2)
Vpp=pent_area*hp/3; Vcleo=(5**.5-1)/24
print("icosidodecahedron(1/phi) volume",Vid,"(11sqrt5-5)/6",(11*5**.5-5)/6)
print("pent pyramid",Vpp,"sqrt5/12",5**.5/12,"| 20 CLEO+12 pp",20*Vcleo+12*Vpp, "| penta-cleo",Vpp/5,"sqrt5/60",5**.5/60)
# CLEO solid angle: spherical equilateral triangle with side 36 deg
t=math.pi/5; c=math.cos(t); A_=math.acos((c-c*c)/(1-c*c)); E=3*A_-math.pi
print("CLEO solid-angle fraction x20:",20*E/(4*math.pi))
print("icosahedron neighbour-vertex angle",math.acos(1/5**.5)*deg)
# Icosahedral Cleo: centre + icosahedron face, icosahedron circumradius = pentagon-centre distance hp
I=np.array([p for s_ in itertools.product((1,-1),repeat=2) for p in [(0,s_[0],s_[1]*phi),(s_[0],s_[1]*phi,0),(s_[1]*phi,0,s_[0])]],float)
I*=hp/np.linalg.norm(I[0]); e=min(np.linalg.norm(I[0]-w) for w in I[1:])
print("pentagon-centre radius",hp,"icosahedron edge",e,"2/sqrt5",2/5**.5)
H=ConvexHull(I); print("icosahedron volume",H.volume,"20 central pyramids = same by construction")
# dihedrals of the central pyramid
f=H.simplices[0]; T=I[f]; O=np.zeros(3)
def dihedral(p,q,a,b):  # dihedral along edge pq between faces pqa,pqb
    e=q-p; e/=np.linalg.norm(e); u=a-p; u-=(u@e)*e; v=b-p; v-=(v@e)*e; return ang(u,v)
print("side-edge dihedral",dihedral(O,T[0],T[1],T[2]),"base-edge dihedral",dihedral(T[0],T[1],O,T[2]))
sols=[(i,j,k) for i in range(6) for j in range(1,6) for k in range(3) if abs(i*72+j*69.0948+k*180-360)<0.5]
print("combinations a*72+b*69.09+c*180=360 with b>=1:",sols)
# CLEO's outer corner vs the cut plane
print("icosahedron face-plane distance",hp*0.7946544723,"icosidodecahedron corners at radius 1 -> cut off")
print("\n== wheels: n planes, each with m spoke-lines, pairwise meeting in distinct spoke-lines => n-1 <= m")
for m,name in [(2,"square wheels: 3 (octahedron)"),(3,"hexagonal: 4 (cuboctahedron)"),(4,"octagonal: 5 ?"),(5,"decagonal: 6 (icosidodecahedron)")]:
    print(m, "max", m+1, name)
