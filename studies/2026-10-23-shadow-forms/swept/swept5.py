# Route A, step 3: stretch #42's lattice only across the sweep (two independent factors, z and z×sweep); find the densest valid.
import numpy as np
exec(open('swept4.py').read().split('fams={')[0])
best=None
for az in np.linspace(0,1.2,25):
    mk=lambda aw:B0@(np.eye(3)+az*np.outer(z,z)+aw*np.outer(w,w)).T
    aw=smallest(mk,0,2.5)
    if aw is None: continue
    dens=vK/abs(np.linalg.det(mk(aw)))
    if best is None or dens>best[0]: best=(dens,az,aw)
    print('z factor %.3f  across factor %.4f  density %.4f'%(1+az,1+aw,dens),flush=True)
print('BEST density %.4f at z %.3f, across %.4f'%(best[0],1+best[1],1+best[2]))
