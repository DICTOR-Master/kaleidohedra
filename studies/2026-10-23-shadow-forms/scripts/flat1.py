# Flat top and bottom: for lattice plane directions, find heights where a plane cuts no piece (all pieces touch it only on faces/edges).
import numpy as np, itertools
exec(open('fuse6.py').read().split('vol=lambda')[0])
pieces=[]
for c in itertools.product(range(-2,3),repeat=3):
    o=np.array(c)*phi
    pieces+= [('ico',ico+o),('Unborn',H+o)]+[('AXE',V+o) for V in cellA]+[('Tricap?',None)]*0
for n in [(0,0,1),(1,1,0),(1,1,1),(0,1,phi),(1,phi,0)]:
    n=np.array(n,float); n/=np.linalg.norm(n)
    hs=sorted(set(np.round(np.concatenate([V@n for _,V in pieces]),6)))
    period=None
    free=[]
    for t in np.linspace(0,phi*np.abs(n).max()*2,4001):
        cut=[k for k,V in pieces if (V@n).min()<t-1e-7 and (V@n).max()>t+1e-7 and np.linalg.norm(V.mean(0))<2*phi]
        if not cut: free.append(round(t,4))
    cutsets={}
    for t in [0,phi/4,phi/2]:
        cutsets[round(t,3)]=sorted(set(k for k,V in pieces if (V@n).min()<t-1e-7 and (V@n).max()>t+1e-7 and np.linalg.norm(V.mean(0))<2*phi))
    print('normal',np.round(n,3),'uncut heights:',free[:5] or 'none','| cut at 0, φ/4, φ/2:',cutsets)
