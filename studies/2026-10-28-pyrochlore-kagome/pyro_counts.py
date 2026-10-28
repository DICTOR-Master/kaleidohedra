# Step A (DICTO 10-28): the pyrochlore network on any close-packed stacking, exact counts from coordinates.
# Build the tetrahedral (diamond-family) network as in #73 (tetra_counts.py); pyrochlore sites = bond midpoints; each atom's
# four bond midpoints form one tetrahedron; tetrahedra share corners. Count: kagome vs triangular layers, corner-sharing pairs
# by conformation (staggered = inversion, eclipsed = mirror), and the loops of the tetrahedron graph (= rings of the atom net):
# 6-rings as chair or boat, and 8-rings. These loops are what corrects Pauling's spin-ice entropy.
import numpy as np, itertools, sys
a1=np.array([1,0,0.]); a2=np.array([.5,3**.5/2,0]); SH={'A':0,'B':1,'C':2}; s=1/np.sqrt(2); N=6
def build(seq):
    n=len(seq); bond=np.sqrt(3/8)*s; dz=4/3*bond; P=[]
    for k,L in enumerate(seq):
        for i in range(N):
            for j in range(N):
                xy=(i*a1+j*a2+SH[L]*(a1+a2)/3)*s; P.append(xy+[0,0,k*dz]); P.append(xy+[0,0,k*dz+bond])
    return np.array(P), np.array([a1*s*N,a2*s*N,[0,0,n*dz]]), bond
def mic(d,cell):
    f=d@np.linalg.inv(cell); f-=np.round(f); return f@cell
def analyse(seq):
    seq=seq*(-(-6//len(seq))); n=len(seq); P,cell,bond=build(seq); M=len(P)
    D=np.linalg.norm(mic(P[:,None,:]-P[None,:,:],cell),axis=2); nb=[list(np.where(np.abs(D[i]-bond)<1e-6)[0]) for i in range(M)]
    assert all(len(x)==4 for x in nb)
    h=sum(seq[i-1]==seq[(i+1)%n] for i in range(n))/n
    # pyrochlore sites (bond midpoints): axial bonds give triangular layers, slanted bonds kagome layers
    axial=sum(1 for i in range(M) for j in nb[i] if i<j and abs(abs(mic(P[j]-P[i],cell)[2])-bond)<1e-6)
    bonds=M*2; tri=axial; kag=bonds-axial
    # corner-sharing tetrahedron pairs = bonds; eclipsed if the 3+3 other bonds face each other (third neighbours at 5/3 bond)
    ecl=0
    for i in range(M):
        for j in nb[i]:
            if i<j:
                d=min(np.linalg.norm(mic(P[l]-P[k],cell)) for k in nb[i] if k!=j for l in nb[j] if l!=i)
                ecl+= d<1.75*bond
    # rings (simple cycles) of length 6 and 8 through the atom graph
    def cycles(L):
        found=set()
        for s0 in range(M):
            stack=[(s0,[s0])]
            while stack:
                v,path=stack.pop()
                if len(path)==L:
                    if s0 in nb[v] and path[1]<path[-1]: found.add(tuple(path))
                    continue
                for w in nb[v]:
                    if w>s0 and w not in path: stack.append((w,path+[w]))
        return found
    r6=cycles(6); chair=boat=0
    for c in r6:
        X=np.array([P[c[0]]+mic(P[x]-P[c[0]],cell) for x in c]); X-=X.mean(0)
        nrm=np.linalg.svd(X)[2][2]; z=np.sign(np.round(X@nrm,6))
        if all(z[k]!=z[(k+1)%6] for k in range(6)): chair+=1
        else: boat+=1
    r8=len(cycles(8))
    return dict(h=h, sites_per_atom=bonds/M, triangular_share=tri/bonds, kagome_share=kag/bonds, eclipsed_pairs_per_tetra=ecl/M,
                chair6_per_tetra=chair/M, boat6_per_tetra=boat/M, rings8_per_tetra=r8/M)
for name,seq in [('3C','ABC'),('2H','AB'),('4H','ABAC'),('6H','ABCACB'),('9R','ABABCBCAC')]:
    r=analyse(seq); print(name, {k:round(v,4) for k,v in r.items()}, flush=True)
