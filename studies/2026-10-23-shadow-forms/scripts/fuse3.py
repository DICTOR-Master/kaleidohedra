# Shadow forms, step 3 (DICTO 2026-10-23: "go ahead with chunky fusions"): every face-connected cluster of 2 or 3 pieces in the three
# simple-cubic networks, kept when "chunky": the pieces fill >= 85% of the cluster's convex hull, and no hull axis is more than 1.8x
# another. Pieces are disjoint, so a cluster's volume is the sum of its pieces'. Lotus Jewel from the study's own data (non-convex).
import numpy as np, json, itertools, sys
from scipy.spatial import ConvexHull
exec(open('fuse1.py').read().split('def pieces')[0])
J=json.load(open('/home/dicto/k-mix/studies/2026-10-10-icosa-networks-3/data/clawed-icosahedron-unit.json'))
JV=np.array(J['vertices']); JF=J['faces']; JVOL=J['volume']
assert np.linalg.norm(JV.mean(0))<0.2, JV.mean(0)
def convex_piece(name,V):
    hl=ConvexHull(V); F={}
    for s,e in zip(hl.simplices,hl.equations): F.setdefault(tuple(np.round(e,6)),set()).update(s)
    return dict(name=name,V=V,faces=[(np.array(k[:3]),sorted(f)) for k,f in F.items()],vol=hl.volume)
def jewel(o):
    V=JV+o; faces=[]
    for f in JF:
        P=V[f]; n=np.cross(P[1]-P[0],P[2]-P[0]); n/=np.linalg.norm(n)
        if n@(P.mean(0)-V.mean(0))<0: n=-n   # rough outward; dents may flip, only used with opposite-normal test both ways below
        faces.append((n,f))
    return dict(name='Lotus Jewel',V=V,faces=faces,vol=JVOL)
VOL={'AXE':1/12}
def net(kind):
    P=[]
    for sh in itertools.product((-1,0,1),repeat=3):
        o=np.array(sh)*phi
        if kind=='icoUnborn': P+= [convex_piece('icosahedron',ico+o), convex_piece('Unborn',H+o)]
        if kind=='jewelDodeca': P+= [jewel(o), convex_piece('dodecahedron',D+o)]
        if kind=='four': P+= [jewel(o), convex_piece('Unborn',H+o)] + [convex_piece('Tricap',t+o) for t in TR]
        P+= [convex_piece('AXE',V+o) for V in axes.values()]
    return P
key=lambda p:tuple(np.round(p,5))
def touch(a,b):
    vb={key(p) for p in b['V']}
    for na,fa in a['faces']:
        common=[a['V'][i] for i in fa if key(a['V'][i]) in vb]
        if len(common)>=3:
            c=np.array(common); n=np.cross(c[1]-c[0],c[2]-c[0])
            if np.linalg.norm(n)>1e-6:
                for nb,fb in b['faces']:
                    if abs(abs(nb@na)-1)<1e-6 and sum(key(b['V'][i]) in {key(x) for x in common} for i in fb)>=3: return True
    return False
def chunk(ps):
    V=np.vstack([p['V'] for p in ps]); hl=ConvexHull(V); vol=sum(p['vol'] for p in ps); fill=vol/hl.volume
    X=V[hl.vertices]-V[hl.vertices].mean(0); ev=np.sqrt(np.sort(np.linalg.eigvalsh(X.T@X/len(X))))
    return fill, ev[-1]/max(ev[0],1e-9), hl.volume, vol
out={}
for kind in ['icoUnborn','jewelDodeca','four']:
    P=net(kind); C=np.array([p['V'].mean(0) for p in P])
    mid=[i for i in range(len(P)) if np.linalg.norm(C[i]-np.array([h,h,h]))<1.5]
    adj={}
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            if np.linalg.norm(C[i]-C[j])<2.3 and touch(P[i],P[j]) or (np.linalg.norm(C[i]-C[j])<2.3 and touch(P[j],P[i])):
                adj.setdefault(i,set()).add(j); adj.setdefault(j,set()).add(i)
    clusters=set()
    for i in mid:
        for j in adj.get(i,()):
            clusters.add(frozenset((i,j)))
            for k in (adj[i]|adj[j])-{i,j}: clusters.add(frozenset((i,j,k)))
    for cl in clusters:
        ps=[P[i] for i in cl]; fill,el,hv,vol=chunk(ps)
        names=tuple(sorted(p['name'] for p in ps)); sig=(kind,names,round(vol,5),round(hv,5))
        if sig not in out: out[sig]=(fill,el,sorted(cl))
    print(kind,'pieces',len(P),'contacts',sum(len(v) for v in adj.values())//2,'clusters',len(clusters),file=sys.stderr)
rows=sorted(((f,e,s) for s,(f,e,cl) in out.items()),key=lambda r:-r[0])
print('%-12s %-48s %7s %7s %6s %s'%('network','pieces','vol','hull','fill','elong'))
for f,e,s in rows:
    if f>=0.85 and e<=1.8: print('%-12s %-48s %7.4f %7.4f %5.1f%% %.2f  CHUNKY'%(s[0],' + '.join(s[1]),s[2],s[3],100*f,e))
print('--- not chunky (best 8):')
for f,e,s in [r for r in rows if not (r[0]>=0.85 and r[1]<=1.8)][:8]: print('%-12s %-48s %7.4f %7.4f %5.1f%% %.2f'%(s[0],' + '.join(s[1]),s[2],s[3],100*f,e))
json.dump([dict(network=s[0],pieces=s[1],vol=s[2],hull=s[3],fill=f,elong=e) for f,e,s in rows],open('fuse3-results.json','w'),indent=1)
