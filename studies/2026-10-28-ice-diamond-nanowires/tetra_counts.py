# Exact counts on tetrahedral networks (diamond family) built on any close-packed stacking (DICTO 10-28).
# Each layer letter carries a bilayer: atom at the layer site and a partner straight above at bond length (wurtzite/zinc-blende).
import numpy as np, itertools
a1=np.array([1,0,0.]); a2=np.array([.5,3**.5/2,0]); SH={'A':0,'B':1,'C':2}
b=np.sqrt(3/8)                                   # bond length for in-plane nn distance 1/sqrt(2)... set via ideal tetrahedra
s=1/np.sqrt(2)                                   # in-plane spacing of the close-packed layer
def build(seq,N=4):
    n=len(seq); bond=np.sqrt(3/8)*s; dz=4/3*bond  # ideal: layer spacing c/n = (4/3) bond
    P=[]
    for k,L in enumerate(seq):
        for i in range(N):
            for j in range(N):
                xy=(i*a1+j*a2+SH[L]*(a1+a2)/3)*s
                z=k*dz; P.append(xy+[0,0,z]); P.append(xy+[0,0,z+bond])
    cell=np.array([a1*s*N,a2*s*N,[0,0,n*dz]]); return np.array(P),cell,bond
def dists(P,cell):
    inv=np.linalg.inv(cell.T); D=P[:,None,:]-P[None,:,:]; f=D@inv.T; f-=np.round(f); return np.linalg.norm(f@cell,axis=2)
def analyse(seq):
    rep=-(-6//len(seq)); seq=seq*rep; P,cell,bond=build(seq); D=dists(P,cell); n=len(P)
    nn=(np.abs(D-bond)<1e-6)
    assert all(nn.sum(1)==4)
    # classify 3rd-neighbour paths i-j-k-l (dihedral about j-k): eclipsed vs staggered, per bond j-k count eclipsed bonds
    ecl=0; tot=0; d3=[]
    for j in range(n):
        for k in np.where(nn[j])[0]:
            if k<j: continue
            tot+=1
            I=[i for i in np.where(nn[j])[0] if i!=k]; L=[l for l in np.where(nn[k])[0] if l!=j]
            ds=sorted(round(D[i,l],6) for i in I for l in L); d3+=ds
            ecl+= min(ds)<1.75*bond              # eclipsed: some i-l pair at 5/3 bond (staggered: 1.915 bond)
    h=sum(seq[i-1]==seq[(i+1)%len(seq)] for i in range(len(seq)))/len(seq)
    short=sum(1 for x in d3 if x<1.75*bond)/n
    return h, ecl/n, tot/n, short, sorted(set(d3))
for name,seq in [('3C diamond','ABC'),('2H lonsdaleite','AB'),('4H','ABAC'),('6H','ABCACB'),('9R','ABABCBCAC'),('15R','ABCACBCABACABCB')]:
    h,e,t,sh,ds=analyse(seq)
    print(f'{name:15s} h = {h:.3f}  bonds/atom {t:.2f}  eclipsed bonds/atom {e:.3f} (h/2 = {h/2:.3f})  short 3rd-nb pairs/atom {sh:.3f}  3rd-nb distances in bonds {[round(x/0.4330127,4) for x in ds]}')
