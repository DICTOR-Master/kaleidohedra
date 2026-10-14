# Can 5 octagonal wheels (great circles) meet pairwise in distinct spokes, every crossing 45 deg apart round each circle?
# Random-start least squares over 5 plane normals. Also re-finds 4 hexagonal (60 deg) and 6 decagonal (36 deg) as controls.
# Fable review for DICTO, 2026-10-14. DICTO · dictospheres.com
import numpy as np, math
from scipy.optimize import least_squares
rng=np.random.default_rng(1)
def resid(x,n,step):
    N=x.reshape(n,3); N=N/np.linalg.norm(N,axis=1)[:,None]; out=[]
    for i in range(n):
        a=N[i]; e1=np.cross(a,[0.3,0.5,0.8]); e1/=np.linalg.norm(e1); e2=np.cross(a,e1)
        th=[]
        for j in range(n):
            if j==i: continue
            l=np.cross(a,N[j]); th.append(math.atan2(l@e2,l@e1)%math.pi)
        th=np.sort(th); d=np.diff(np.r_[th,th[0]+math.pi])
        out+=list(d-step)
    return np.array(out)
for n,step in [(4,math.pi/3),(6,math.pi/5),(5,math.pi/4)]:
    best=1e9
    for t in range(300):
        r=least_squares(resid,rng.normal(size=3*n),args=(n,step))
        best=min(best,np.max(np.abs(r.fun)))
    print(f"{n} circles, crossings every {step*180/math.pi:.0f} deg: best max error {best*180/math.pi:.4f} deg")
