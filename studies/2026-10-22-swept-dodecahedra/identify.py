# Identify the ring-1 stretched shapes: for each, are its faces regular polygons (Johnson/Archimedean candidates),
# squares vs rhombi, and what vertex count; known names where the face data match a known solid exactly.
import numpy as np, itertools, math
from collections import Counter
import mixes3 as M, pieces_figure as PF
exec(open('ring1.py').read().split("fmt=lambda")[0])
def face_info(V):
    F=[np.array(f) for f in PF.hull_faces(V)]; out=Counter(); allreg=True
    for f in F:
        n=len(f); ang=[math.degrees(math.acos(np.clip((f[i-1]-f[i])@(f[(i+1)%n]-f[i])/np.linalg.norm(f[i-1]-f[i])/np.linalg.norm(f[(i+1)%n]-f[i]),-1,1))) for i in range(n)]
        reg=max(ang)-min(ang)<1e-6
        nm={3:'triangle',4:'square' if reg else 'rhombus',5:'regular pentagon' if reg else 'pentagon',6:'regular hexagon' if reg else 'hexagon',7:'heptagon',8:'octagon'}[n]
        out[nm]+=1; allreg&=reg
    nv=len({tuple(np.round(p,6)) for f in F for p in f}); return out,allreg,nv,len(F)
KNOWN={ (('square',6),('triangle',8)):'cuboctahedron (Archimedean)', (('regular hexagon',4),('triangle',4)):'truncated tetrahedron (Archimedean)',
        (('regular hexagon',2),('square',6)):'hexagonal prism', (('square',3),('triangle',2)):'triangular prism', (('square',6),):'cube (box)'}
cases=[]
for name,V in SOL.items():
    dirs={'(1,0,0)':(1,0,0),'(1,1,0)':(1,1,0),'(1,1,1)':(1,1,1)}
    if name=='icosahedron': dirs['five-fold']=(0,1,phi)
    for dn,u in dirs.items():
        u=np.array(u,float); u/=np.linalg.norm(u); cases.append((name,'stretched along '+dn,np.vstack([V,V+u])))
    for cn,pts in (('three caps',[(0,0,0),(1,1,0),(1,0,1)]),('four caps',[(0,0,0),(1,1,0),(1,0,1),(0,1,1)])):
        cases.append((name,cn,np.vstack([V+np.array(p,float)/2**.5 for p in pts])))
for name,how,V in cases:
    info,allreg,nv,nf=face_info(V); k=tuple(sorted(info.items()))
    tag=KNOWN.get(k,'regular-faced: check Johnson list' if allreg else 'not regular-faced (rhombi/irregular): not Johnson or Archimedean')
    print(f'{name:12s} {how:24s} V={nv:3d} F={nf:3d} {dict(info)}  -> {tag}')
