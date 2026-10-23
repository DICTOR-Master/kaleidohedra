# Flat top and bottom, step 4: units with TURNED copies. The layer is tiled by a group G = <T', g>: T' an index-2 sublattice of the
# cell translations, g = a network symmetry (sign flips of x, y and, for the thick layers, z about the layer's middle) followed by a
# one-cell slide not in T'. G has the same density as the cell lattice, so a unit = one part from each G-orbit (volume = one cell).
# Groups that send some part onto itself are skipped (that part would have to be halved). Search: max fill of the unit's hull.
import numpy as np, itertools, json
exec(open('flat2.py').read().split('rng=np.random')[0])
LAY={'A':(0,phi),'B':(0,phi/2),'C':(phi/2,1.5*phi)}
SUB={'x even':lambda a,b:a%2==0,'y even':lambda a,b:b%2==0,'checker':lambda a,b:(a+b)%2==0}
rng=np.random.default_rng(3); results=[]
for L,(z0,z1) in LAY.items():
    reps=layer(z0,z1); W=range(-4,5)
    allp=[(n,P+np.array([a*phi,b*phi,0])) for n,P in reps for a in W for b in W]
    key=lambda n,P:(n,)+tuple(np.round(P.mean(0),4))
    idx={key(n,P):i for i,(n,P) in enumerate(allp)}
    zs=[1,-1] if L in 'AC' else [1]
    for s in itertools.product((1,-1),(1,-1),zs):
        if s==(1,1,1): continue
        for tn,(ta,tb) in {'(1,0)':(1,0),'(0,1)':(0,1),'(1,1)':(1,1)}.items():
            for sn,sub in SUB.items():
                if sub(ta,tb): continue
                if not sub(2*ta*(s[0]==1),2*tb*(s[1]==1)): pass
                off=np.array([ta*phi,tb*phi,(z0+z1) if s[2]==-1 else 0])
                g=lambda P:P*np.array(s)+off
                Tp=[(a,b) for a in range(-4,5) for b in range(-4,5) if sub(a,b)]
                # g^2 must lie in T' (else the group is bigger than intended)
                g2=g(g(np.zeros((1,3))))[0]; a2,b2=np.round(g2[:2]/phi).astype(int)
                if abs(g2[2])>1e-9 or not sub(a2,b2): continue
                # free action: no part sent onto itself by g followed by any T' slide
                fixed=False
                for n,P in reps:
                    for a,b in Tp:
                        if key(n,g(P)+np.array([a*phi,b*phi,0]))==key(n,P): fixed=True
                if fixed: continue
                # orbits by union-find
                par=list(range(len(allp)))
                def f(i):
                    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
                    return i
                for i,(n,P) in enumerate(allp):
                    for Q in [g(P)]+[P+np.array([a*phi,b*phi,0]) for a,b in [(2,0),(0,2),(1,1),(1,-1),(0,1),(1,0)] if sub(a,b)]:
                        j=idx.get(key(n,Q))
                        if j is not None: par[f(i)]=f(j)
                orb={}
                for i,(n,P) in enumerate(allp):
                    if np.linalg.norm(P.mean(0)[:2]-phi/2)<1.6*phi: orb.setdefault(f(i),[]).append(i)
                if len(orb)!=len(reps): print('  skip',L,s,tn,sn,'orbits',len(orb)); continue
                C=list(orb.values())
                def fill(ch):
                    V=np.vstack([allp[C[k][c]][1] for k,c in enumerate(ch)])
                    return sum(hullvol(allp[C[k][c]][1]) for k,c in enumerate(ch))/hullvol(V)
                best=(0,None)
                for r in range(30):
                    if r==0: ch=[int(np.argmin([np.linalg.norm(allp[i][1].mean(0)[:2]-phi/2) for i in c])) for c in C]
                    else: ch=[int(rng.integers(len(c))) for c in C]
                    fv=fill(ch); imp=True
                    while imp:
                        imp=False
                        for k in range(len(C)):
                            for c in range(len(C[k])):
                                if c==ch[k]: continue
                                t=ch.copy(); t[k]=c; gv=fill(t)
                                if gv>fv+1e-9: fv,ch,imp=gv,t,True
                    if fv>best[0]: best=(fv,ch)
                fv,ch=best
                U=[(allp[C[k][c]][0],allp[C[k][c]][1].tolist()) for k,c in enumerate(ch)]
                results.append(dict(layer=L,z=[z0,z1],flip=s,slide=tn,sub=sn,fill=fv,unit=U,off=off.tolist()))
                print('%s flip %s slide %s keep %s: fill %.1f%%'%(L,s,tn,sn,100*fv),flush=True)
results.sort(key=lambda r:-r['fill'])
json.dump(results,open('flat4-units.json','w'))
print('BEST:',[(r['layer'],r['flip'],r['slide'],r['sub'],round(100*r['fill'],1)) for r in results[:6]])
