# Route A: lattice packings of the swept piece K = D + [0, s], s = (φ, φ, 0). A lattice packs K iff no non-zero lattice vector
# lies in the interior of K − K = 2D + [−s, s]. Search: sublattices of #42's dodecahedron lattice Λ0 (fcc of cells, step φ) of
# index 2..4, then keep the valid ones and their density vol(K)/det.
import numpy as np, itertools
exec(open('swept1.py').read().split('# period:')[0])
E2=ConvexHull(2*D).equations
def in_diff(l, tol=1e-9):          # l in interior of 2D + [-s, s]?
    for u in np.linspace(-1,1,801):
        q=l-u*sweep
        if (q@E2[:,:3].T+E2[:,3] < -tol).all(): return True
    return False
B0=np.array([[1,1,0],[1,0,1],[0,1,1]],float)*phi        # fcc basis of the even cells
vK=hS.volume; det0=abs(np.linalg.det(B0))
def short_vectors(B,R=3):
    return [np.array(c)@B for c in itertools.product(range(-R,R+1),repeat=3) if any(c)]
seen=set(); res=[]
for n in (2,3,4):
    # Hermite normal forms of index n
    for a in range(1,n+1):
        if n%a: continue
        for d in range(1,n//a+1):
            if (n//a)%d: continue
            f=n//(a*d)
            for b in range(d):
                for c in range(f):
                    for e in range(f):
                        H=np.array([[a,0,0],[b,d,0],[c,e,f]],float); B=H@B0
                        key=tuple(np.round(np.sort(np.abs(np.linalg.eigvalsh(B@B.T))),6))
                        ok=not any(in_diff(l) for l in short_vectors(B,2) if np.linalg.norm(l)<2*np.linalg.norm(S.max(0)-S.min(0)))
                        if ok: res.append((vK/(n*det0),n,H.astype(int).tolist()))
res.sort(key=lambda r:-r[0])
print('valid sublattice packings found:',len(res))
for r in res[:6]: print('  density %.4f  index %d  HNF %s'%r)
