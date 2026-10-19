import json, numpy as np, manifold3d as m3, math
H='/home/dicto/dbt-exact/2026-10-19-og-gyrated-octet/'
fq=lambda s:(lambda a,b: float(eval(a))+float(eval(b))*5**.5)(*s.split('|'))
DB=np.array([[fq(c) for c in v] for v in json.load(open(H+'dbt-exact.json'))['V']])
D=json.load(open(H+'../2026-10-18-ocd-octet/data/step1-ocd-exact.json')); R=fq(D['R'])
hull=lambda P: m3.Manifold.hull_points(np.asarray(P,float))
dbt=hull(DB); OCT=np.array([[s*R if k==j else 0 for j in range(3)] for k in range(3) for s in (1,-1)]); octa=hull(OCT)
sp=octa-dbt; parts=sorted([p for p in sp.decompose()], key=lambda p:-p.volume())
print('octahedron - DBT', round(sp.volume(),6), 'parts', len(parts), [round(p.volume(),6) for p in parts[:8]])
# where the DBT meets each octahedron edge: sample along the edge, distance to DBT surface via inside test on tiny cubes
from scipy.spatial import ConvexHull
h=ConvexHull(DB); E=h.equations
inside=lambda x: np.max(E[:,:3]@x+E[:,3])
for a,b in [((R,0,0),(0,R,0)),((R,0,0),(0,0,R)),((0,R,0),(0,0,R)),((R,0,0),(0,-R,0))]:
    a=np.array(a);b=np.array(b); ts=np.linspace(0,1,20001); d=[inside(a+(b-a)*t) for t in ts]; i=int(np.argmin(d))
    print('edge',a.round(3),b.round(3),'closest t',round(ts[i],4),'gap',round(d[i],6),'plane sum',round((a+(b-a)*ts[i]).sum()/R,3))
for p in parts[:1]:
    print('largest part sphericity', round(math.pi**(1/3)*(6*p.volume())**(2/3)/p.surface_area(),3))
