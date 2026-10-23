# Step 2: what does one swept piece (D at 0 + D at (φ,φ,0)) collide with? Other dodecahedra of the #42 grid, by offset.
import numpy as np, itertools
exec(open('swept1.py').read().split('# period:')[0])
rs=np.random.default_rng(3); N=300000
lo=S.min(0); hi=S.max(0); P=lo+rs.random((N,3))*(hi-lo); P=P[inside(P,ES)]
own=inside(P,ED)|inside(P-sweep,ED); bridge=P[~own]
print('swept piece sample points: %d, of which in its own two dodecahedra %.3f, bridge %.3f'%(len(P),own.mean(),1-own.mean()))
hits={}
for a,b,c in itertools.product(range(-2,4),repeat=3):
    if (a+b+c)%2 or (a,b,c) in [(0,0,0),(1,1,0)]: continue
    f=inside(P-np.array([a,b,c])*phi,ED).mean()
    if f>0: hits[(a,b,c)]=f
print('overlap with other dodecahedra (fraction of the swept piece):',{k:round(v,4) for k,v in sorted(hits.items(),key=lambda x:-x[1])})
# the bridge (swept piece minus its two dodecahedra): is it inside the Dogstar cells (odd cells)?
cells=np.round(bridge/phi).astype(int); odd=(cells.sum(1)%2!=0)
print('bridge volume 4.736 lies in odd (Dogstar) cells: %.3f; in even cells: %.3f'%(odd.mean(),1-odd.mean()))
from collections import Counter; print('bridge by cell:',Counter(map(tuple,cells)).most_common(6))
