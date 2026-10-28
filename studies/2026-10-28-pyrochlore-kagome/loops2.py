# Robust version of loops.py: closed non-backtracking walks per atom, counted only from the atoms of one vertical column
# (one in-plane cell, all layers of the period), on a large in-plane cell (N=36) and many repeated periods (>= 36 layers),
# so no walk of length <= 34 can wrap around the cell. Sparse propagation; L up to 34.
import numpy as np, sys
from scipy.sparse import csr_matrix
a1=np.array([1,0,0.]); a2=np.array([.5,3**.5/2,0]); SH={'A':0,'B':1,'C':2}; s=1/np.sqrt(2)
N=36; LMAX=34
def run(seq):
    p=len(seq); rep=-(-36//p); seq=seq*rep; n=len(seq); bond=np.sqrt(3/8)*s; dz=4/3*bond
    # atoms indexed (k,i,j,u): layer k, cell i,j, u=0 lower/1 upper; neighbours by rule instead of distances (exact):
    # u=0 atom at (k,i,j) bonds up to (k,i,j,1) and down to the 3 upper atoms of layer k-1 around it; u=1 bonds to 3 lower atoms of k+1.
    def offs(lo,hi):   # in-plane shifts (di,dj) so that lower atom of the next layer at (i-di,j-dj) is a bond from upper atom (i,j)
        r=[]
        for di in range(-2,3):
            for dj in range(-2,3):
                d=((-di)*a1+(-dj)*a2+(hi-lo)*(a1+a2)/3)*s
                if abs(np.hypot(d[0],d[1])-s/np.sqrt(3))<1e-9: r.append((di,dj))
        assert len(r)==3,(lo,hi,r); return r
    off={(lo,hi):offs(lo,hi) for lo in range(3) for hi in range(3) if lo!=hi}
    def idx(k,i,j,u): return ((k%n)*N*N+(i%N)*N+(j%N))*2+u
    def pos(k,i,j,u): return (i*a1+j*a2+SH[seq[k%n]]*(a1+a2)/3)*s+np.array([0,0,k*dz+u*bond])
    M=n*N*N*2; nb=[[] for _ in range(M)]
    for k in range(n):
        lo,hi=SH[seq[k]],SH[seq[(k+1)%n]]
        for i in range(N):
            for j in range(N):
                a=idx(k,i,j,0); b=idx(k,i,j,1); nb[a].append(b); nb[b].append(a)
                for di,dj in off[(lo,hi)]:
                    c=idx(k+1,i-di,j-dj,0)    # lower atom of layer k+1 near upper atom (k,i,j)
                    nb[b].append(c); nb[c].append(b)
    # geometric check on a sample
    for k in range(min(n,4)):
        for v in [idx(k,3,4,1)]:
            for w in nb[v]:
                kk=(w//2)//(N*N); r=(w//2)%(N*N); ii,jj=r//N,r%N; u=w%2
                if kk<k: kk+=n
                d=np.linalg.norm(pos(kk,ii,jj,u)-pos(k,3,4,1)); 
                if abs(d-bond)>1e-6:
                    # try wrapped images in plane
                    best=min(np.linalg.norm(pos(kk,ii+x*N,jj+y*N,u)-pos(k,3,4,1)) for x in (-1,0,1) for y in (-1,0,1))
                    assert abs(best-bond)<1e-6,(seq[k],seq[(k+1)%n],d)
    assert all(len(x)==4 for x in nb)
    E=[(v,w) for v in range(M) for w in nb[v]]; eid={e:t for t,e in enumerate(E)}
    rows=[];cols=[]
    for (v,w),t in eid.items():
        for x in nb[w]:
            if x!=v: rows.append(t); cols.append(eid[(w,x)])
    B=csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(E),len(E))).T.tocsr()   # column-propagation
    start=[eid[(v,w)] for k in range(p) for u in (0,1) for v in [idx(k,0,0,u)] for w in nb[v]]
    X=np.zeros((len(E),len(start))); X[start,range(len(start))]=1
    out=[]
    for L in range(1,LMAX+1):
        X=B@X; out.append(sum(X[start[c],c] for c in range(len(start)))/(2*p))
    return out
res={}
for name,seq in [('3C','ABC'),('2H','AB'),('4H','ABAC'),('6H','ABCACB'),('9R','ABABCBCAC')]:
    res[name]=run(seq); print(name,'done',flush=True)
for L in range(6,LMAX+1,2):
    print(f'L={L:2d}: '+'  '.join(f'{k} {res[k][L-1]:.0f}' for k in res)+('   all equal' if len({round(res[k][L-1],6) for k in res})==1 else '   DIFFER'))
