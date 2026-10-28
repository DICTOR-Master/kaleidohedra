# Exact check: hexagonal perovskites ABX3 as stacked AX3 close-packed layers (A on a 2x2 sublattice of each layer).
# B goes in octahedral holes bounded only by X. Count, per B, neighbours sharing a face (3 X) and a corner (1 X).
import itertools, numpy as np
a1=np.array([1,0.]); a2=np.array([.5,3**.5/2]); SH={'A':0,'B':1,'C':2}
def pos(letter,i,j): return i*a1+j*a2+SH[letter]*(a1+a2)/3
N=4                                               # in-plane supercell N x N (A sublattice 2x2)
def layer_sites(letter,off):                       # off in {(0,0),(1,0),(0,1),(1,1)}: which 2x2 coset holds A
    return [(pos(letter,i,j),'A' if (i%2,j%2)==off else 'X') for i in range(N) for j in range(N)]
def wrap(d):                                       # minimal image in the N x N cell
    M=np.array([a1,a2]).T*N; f=np.linalg.solve(M,d); f-=np.round(f); return M@f
def gap_Bs(seq,offs,k):                            # B sites in the gap above layer k (holes bounded by 6 X)
    n=len(seq); lo=layer_sites(seq[k],offs[k]); hi=layer_sites(seq[(k+1)%n],offs[(k+1)%n])
    t=({'A','B','C'}-{seq[k],seq[(k+1)%n]}).pop(); out=[]
    for i in range(N):
        for j in range(N):
            p=pos(t,i,j)
            nb=[(kk,idx) for kk,lay in ((k,lo),((k+1)%n,hi)) for idx,(q,el) in enumerate(lay) if np.linalg.norm(wrap(q-p))<0.6]
            if all(lay_el=='X' for lay_el in [(lo if kk==k else hi)[idx][1] for kk,idx in nb]): out.append((k,frozenset(nb)))
    return out
def analyse(seq):                                  # depth-first over A offsets, each gap must hold exactly N*N/4 B
    n=len(seq); O=[(0,0),(1,0),(0,1),(1,1)]
    def dfs(offs):
        k=len(offs)-1
        if k>=1 and len(gap_Bs(seq,offs+[None]*(n-len(offs)),k-1))!=N*N//4: return None
        if len(offs)==n:
            if len(gap_Bs(seq,offs,n-1))!=N*N//4: return None
            return offs
        for o in O:
            r=dfs(offs+[o])
            if r: return r
    offs=dfs([(0,0)])
    if not offs: return None
    Bs=[b for k in range(n) for b in gap_Bs(seq,offs,k)]
    face=corner=0
    for x,y in itertools.combinations(Bs,2):
        s=len(x[1]&y[1]); face+=s==3; corner+=s==1
    return 2*face/len(Bs), 2*corner/len(Bs)
def h_of(seq):
    n=len(seq); return sum(seq[i-1]==seq[(i+1)%n] for i in range(n))/n
for name,seq in [('3C','ABC'),('2H','AB'),('4H','ABAC'),('6H','ABCACB'),('9R','ABABCBCAC')]:
    r=analyse(seq*(1 if len(seq)>=6 else -(-6//len(seq)))); h=h_of(seq)   # repeat short cells: no period aliasing
    print(f'{name}: h = {h:.3f}  per B: face-sharing {r[0]:.3f} (2h = {2*h:.3f}), corner-sharing {r[1]:.3f} (6(1-h) = {6*(1-h):.3f})' if r else f'{name}: no B arrangement found')
