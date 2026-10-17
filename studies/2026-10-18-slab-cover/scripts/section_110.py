# DICTO 2026-10-18: 2D cut through the RT envelopes on the bcc (110)-type plane (slab axis + a nearest-neighbour axis). -> data/section-110-float.json
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data'))
import json,itertools,numpy as np
from scipy.spatial import ConvexHull
S=json.load(open('scene-float.json'));V=np.array(S['rt']['v']);E=ConvexHull(V).equations
G=json.load(open('../../2026-10-16-ocd-pyrochlore/data/gbpc-geom-exact.json'));S5=5**.5
f=lambda s:(lambda a,b:float(eval(a))+float(eval(b))*S5)(*s.split('|'))
L=np.array([[f(x) for x in v] for v in G['LB']])
lat=[np.array(c)@L for c in itertools.product(range(-3,4),repeat=3)]
lat=[t for t in lat if np.linalg.norm(t)<3.2]
nb=[t for t in lat if 0<np.linalg.norm(t)<1.75]
slab=[t for t in nb if abs(np.linalg.norm(t)-1.4383)<1e-3]; near=[t for t in nb if abs(np.linalg.norm(t)-1.2456)<1e-3]
o=slab[0]; u=o/np.linalg.norm(o)
# nearest neighbour p making the plane: pick p coplanar-most-symmetric (largest component perpendicular to u)
p=max(near,key=lambda t:np.linalg.norm(t-(t@u)*u)); w=p-(p@u)*u; w/=np.linalg.norm(w); nrm=np.cross(u,w)
print('angle o,p',np.degrees(np.arccos(u@p/np.linalg.norm(p))))
def section(halfspaces,shift):  # polygon of {x: n.x+d<=0} ∩ plane, in (u,w) coords
    poly=[np.array(c) for c in [(-4,-4),(4,-4),(4,4),(-4,4)]]
    for e in halfspaces:
        n3=e[:3]; d=e[3]+n3@(-shift)   # body translated by shift: n.(x-shift)+d<=0
        a=np.array([n3@u,n3@w]); out=[]
        for i in range(len(poly)):
            A,B=poly[i],poly[(i+1)%len(poly)];da,db=a@A+d,a@B+d
            if da<=0: out.append(A)
            if da*db<0: out.append(A+(B-A)*da/(da-db))
        poly=out
        if len(poly)<3: return None
    return poly
rts=[(t,section(E,t)) for t in lat]; rts=[(t,p_) for t,p_ in rts if p_]
tiles=[]
for t in S['tiles']:
    P=np.array(t['v']);h=ConvexHull(P);sec=section(h.equations,np.zeros(3))
    if sec: tiles.append((t['k'],sec))
print('rts',len(rts),'tile sections',len(tiles))
json.dump(dict(rts=[dict(c=[float(t@u),float(t@w)],p=np.round(p_,5).tolist()) for t,p_ in rts],
  tiles=[dict(k=k,p=np.round(p_,5).tolist()) for k,p_ in tiles],
  slabdir=[float(o@u),float(o@w)],near=[float(p@u),float(p@w)]),open('section-110-float.json','w'))
