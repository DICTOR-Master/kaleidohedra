"""Step 3b foundation: Narcissus-only slabs, one straight/turned bit per interface.
Slab = layer of N between two planes (down-N on X balls, up-N on Y balls, mid corners over Z holes).
Next slab = mirror of the slab in its top plane (STRAIGHT), optionally then turned 60 deg about a hexagon centre (TURNED).
Check: random words -> every sample point lies in exactly one N; all-S = hcp h-tiling, all-T = Covenant pairs."""
import numpy as np, sys, itertools
from scipy.spatial import ConvexHull
r3=np.sqrt(3); H=np.sqrt(2/3); s=1/r3
a1=np.array([1,0.]); a2=np.array([.5,r3/2])
SITE={'A':np.zeros(2),'B':(a1+a2)/3,'C':2*(a1+a2)/3}
def coset(p):
    # which of A,B,C a planar point belongs to (mod lattice)
    M=np.array([a1,a2]).T; c=np.linalg.solve(M,p); f=c-np.floor(c+1e-9)
    for k,v in SITE.items():
        g=np.linalg.solve(M,v); d=(f-g); d-=np.round(d)
        if np.allclose(d,0,atol=1e-7): return k
    return None
DIRS=[s*np.array([np.cos(np.pi/3*k+np.pi/6),np.sin(np.pi/3*k+np.pi/6)]) for k in range(6)]
def narc(c,zh,za,Z):
    """hexagon centred c at height zh, apex below/above at za; mid corners over the Z-type hexagon corners"""
    hexv=[c+d for d in DIRS]; zm=(zh+za)/2
    P=[np.r_[v,zh] for v in hexv]+[np.r_[v,zm] for v in hexv if coset(v)==Z]+[np.r_[c,za]]
    assert len(P)==10, len(P)
    return np.array(P)
def slab(n=4):
    X,Y,Z='A','B','C'; out=[]
    for i,j in itertools.product(range(-n,n+1),repeat=2):
        L=i*a1+j*a2
        out.append(('down',narc(L+SITE[X],H,0,Z)))
        out.append(('up',narc(L+SITE[Y],0,H,Z)))
    return out
def apply(P,k,turn,c0):
    Q=P.copy(); Q[:,2]=2*(k+1)*H-Q[:,2]   # mirror in plane z=(k+1)H
    if turn:
        t=np.pi/3; R=np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
        Q[:,:2]=(Q[:,:2]-c0)@R.T+c0
    return Q
def build(word,n=4):
    S=slab(n); layers=[[p for _,p in S]]
    c0=SITE['A']  # a hexagon centre of the top plane of slab 0 (down-N centred on X=A)
    for k,b in enumerate(word):
        prev=layers[-1]
        # hexagon centre on the current top plane: any down-N hexagon centre of the previous layer
        layers.append([apply(P,k,b=='T',c0) for P in prev])
        # next interface: hexagon centres on plane (k+2)H -> pick one from new layer (corners at z=(k+2)H... centre = mean of 6 hex corners)
        top=[P for P in layers[-1] if np.sum(np.isclose(P[:,2],(k+2)*H))==6]
        cs=[P[np.isclose(P[:,2],(k+2)*H)][:,:2].mean(0) for P in top]
        c0=min(cs,key=lambda c:np.linalg.norm(c))   # hexagon centre nearest the axis, so turns stay inside the patch
    return [P for L in layers for P in L]
def check(word,N=20000,seed=1):
    Ps=build(word); hulls=[ConvexHull(P) for P in Ps]
    rng=np.random.default_rng(seed)
    pts=np.c_[rng.uniform(-1.5,1.5,(N,2)),rng.uniform(0.01,(len(word)+1)*H-0.01,N)]
    cnt=np.zeros(N,int)
    for h in hulls:
        cnt+=(h.equations[:,:3]@pts.T+h.equations[:,3:4]<=1e-12).all(0)
    vol=np.mean([h.volume for h in hulls])
    return (cnt==1).mean(), cnt.min(), cnt.max(), vol
if __name__=='__main__':
    rng=np.random.default_rng(7)
    words=['SSSSS','TTTTT','STSTT','TTSST']+[''.join(rng.choice(['S','T'],6)) for _ in range(6)]
    for w in words:
        f,lo,hi,v=check(w)
        print(f'{w:8s} exactly-once {f:.6f} min {lo} max {hi} N volume {v:.6f} (sqrt2/4={np.sqrt(2)/4:.6f})',flush=True)
    print('FINAL ok')
