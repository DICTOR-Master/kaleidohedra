# Route A, step 2: stretch #42's lattice just enough for the swept piece; densest of three simple families.
import numpy as np, itertools
exec(open('swept3.py').read().split('seen=set()')[0])
sh=sweep/np.linalg.norm(sweep); z=np.array([0,0,1.]); w=np.cross(z,sh)
def valid(B):
    L=[l for l in short_vectors(B,2)]
    return not any(in_diff(l) for l in L)
def smallest(make, lo=0, hi=3):
    if not valid(make(hi)): return None
    for _ in range(30):
        m=(lo+hi)/2
        if valid(make(m)): hi=m
        else: lo=m
    return hi
fams={'stretch along the sweep':lambda a:B0@(np.eye(3)+a*np.outer(sh,sh)).T,
      'stretch vertically (z)':lambda a:B0@(np.eye(3)+a*np.outer(z,z)).T,
      'stretch across (z × sweep)':lambda a:B0@(np.eye(3)+a*np.outer(w,w)).T,
      'scale evenly':lambda a:B0*(1+a)}
for name,mk in fams.items():
    a=smallest(mk)
    if a is None: print(name,': no valid lattice up to factor 4'); continue
    B=mk(a); print('%-28s factor %.4f  density %.4f'%(name,1+a,vK/abs(np.linalg.det(B))))
