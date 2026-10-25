# Technical description of each piece kind of the gnomon steps (DICTO 2026-10-25): face types, corner degrees, distinct edge lengths,
# a family name (pyramid / bipyramid / frustum / prismatoid / wedge / polyhedron), and the nearest classical solid it departs from.
import json, numpy as np, itertools
from scipy.spatial import ConvexHull
d=json.load(open('pieces.json'))
def faces(P):
    h=ConvexHull(P); out={}
    for s,e in zip(h.simplices,h.equations): out.setdefault(tuple(np.round(e,7)),set()).update(s)
    return [sorted(v) for v in out.values()]
def describe(P):
    P=np.array(P); F=faces(P); sizes=sorted(len(f) for f in F)
    E=set()
    for a,b in itertools.combinations(range(len(F)),2):
        sh=set(F[a])&set(F[b])
        if len(sh)==2: E.add(tuple(sorted(sh)))
    L=sorted({round(float(np.linalg.norm(P[i]-P[j])),5) for i,j in E})
    deg={}
    for i,j in E: deg[i]=deg.get(i,0)+1; deg[j]=deg.get(j,0)+1
    cnt={s:sizes.count(s) for s in sorted(set(sizes))}; nF=len(F); big=[s for s in cnt if s>4]
    if nF==4: fam='tetrahedron'
    elif sizes.count(3)==nF-1: fam=f'{max(sizes)}-gonal pyramid'
    elif set(sizes)=={3} and nF in (6,10) and max(deg.values())==nF//2: fam=f'{nF//2}-gonal bipyramid'
    elif set(sizes)=={3}: fam=f'deltahedron-like ({nF} triangles)'
    else:
        top=[f for f in F if len(f)==max(sizes)]
        if len(top)==2 and all(s==4 for s in sizes if s!=max(sizes)): fam=f'{max(sizes)}-gonal frustum/prismatoid'
        else: fam='polyhedron'
    return dict(corners=len(P),faces=nF,face_types=cnt,edges=len(E),edge_lengths=len(L),fam=fam)
rows=[]
for k,st in enumerate(d['steps'],1):
    for kind in st['kinds']:
        r=describe(kind['pieces'][0]); rows.append((k,st['from'],st['to'],kind['label'],len(kind['pieces']),r))
for k,a,b,lab,n,r in rows:
    print(f"step {k:2d} {a} -> {b}: {lab} x{n}: {r['fam']}; {r['corners']} corners, faces {r['face_types']}, {r['edges']} edges in {r['edge_lengths']} lengths")
