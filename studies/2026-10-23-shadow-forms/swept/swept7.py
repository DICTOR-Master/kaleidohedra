# Route A, step 4: refine the swept piece's lattice packing (all 9 basis entries free), then measure the gaps.
# Overlap test, exact up to float: K − K = 2D + [−s, s]; λ is inside iff some u in [−1, 1] has λ − u·s strictly inside 2D,
# i.e. for every facet (n, c) of 2D: n·λ − u n·s + c < 0 — an interval in u per facet; intersect them.
import numpy as np, itertools, json
exec(open('swept1.py').read().split('# period:')[0])
E2=ConvexHull(2*D).equations; N2=E2[:,:3]; C2=E2[:,3]; ns=N2@sweep
def inside_diff(l, tol=1e-9):
    a=N2@l+C2              # need a - u*ns < -tol for all facets
    lo,hi=-1.0,1.0
    for ai,ni in zip(a,ns):
        if abs(ni)<1e-12:
            if ai>=-tol: return False
        elif ni>0: lo=max(lo,(ai+tol)/ni)
        else: hi=min(hi,(ai+tol)/ni)
    return lo<hi
COMB=[np.array(c) for c in itertools.product(range(-3,4),repeat=3) if any(c)]
def valid(B): return not any(inside_diff(c@B) for c in COMB)
vK=hS.volume
sh=sweep/np.linalg.norm(sweep); z=np.array([0,0,1.]); w=np.cross(z,sh)
B0=np.array([[1,1,0],[1,0,1],[0,1,1]],float)*phi
def mk(az,aw): return B0@(np.eye(3)+np.outer(sh,sh)+az*np.outer(z,z)+aw*np.outer(w,w)).T
best0=None
for az in np.linspace(0,1.6,33):
    lo,hi=0.0,3.0
    if not valid(mk(az,hi)): continue
    for _ in range(40):
        m=(lo+hi)/2
        if valid(mk(az,m)): hi=m
        else: lo=m
    d=abs(np.linalg.det(mk(az,hi)))
    if best0 is None or d<best0[0]: best0=(d,az,hi)
print('exact-test start: density %.4f at z %.3f across %.4f'%(vK/best0[0],1+best0[1],1+best0[2]),flush=True)
B=mk(best0[1],best0[2]*1.0000001)
assert valid(B), 'start not valid'
rng=np.random.default_rng(7); best=B.copy(); bd=abs(np.linalg.det(B)); step=0.08
for it in range(30000):
    C=best+rng.normal(0,step,(3,3))
    if not valid(C): continue
    d=abs(np.linalg.det(C))
    if d<bd: best,bd=C,d
    if it%3000==2999: step*=0.7; print('iter %d density %.4f'%(it+1,vK/bd),flush=True)
print('BEST density %.5f'%(vK/bd)); print('basis', np.round(best,5).tolist())
json.dump({'basis':best.tolist(),'density':vK/bd},open('swept-best-lattice.json','w'))
