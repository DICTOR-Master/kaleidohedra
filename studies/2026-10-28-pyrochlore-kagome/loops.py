# Loops of the tetrahedron network (= rings of the atom net) on any stacking: non-backtracking closed walks per atom,
# tr(B^L)/atoms (Hashimoto matrix B), L up to 20. Cycles of length L enter at L first; stackings that differ only in long loops
# have equal Pauling-type loop corrections up to that order. In-plane cell N=8 so no wrap-around loop shorter than ~13.
import numpy as np
exec(open('pyro_counts.py').read().split('def analyse')[0].replace('N=6','N=8'))
def nb_walks(seq,Lmax=20):
    seq=seq*(-(-12//len(seq))); P,cell,bond=build(seq); M=len(P)
    D=np.linalg.norm(mic(P[:,None,:]-P[None,:,:],cell),axis=2); nb=[list(np.where(np.abs(D[i]-bond)<1e-6)[0]) for i in range(M)]
    E=[(i,j) for i in range(M) for j in nb[i]]; idx={e:k for k,e in enumerate(E)}
    B=np.zeros((len(E),len(E)))
    for (i,j),k in idx.items():
        for l in nb[j]:
            if l!=i: B[k,idx[(j,l)]]=1
    out=[]; X=np.eye(len(E))
    for L in range(1,Lmax+1):
        X=X@B; out.append(np.trace(X)/M)
    return out
res={}
for name,seq in [('3C','ABC'),('2H','AB'),('4H','ABAC'),('6H','ABCACB')]:
    res[name]=nb_walks(seq); print(name,'done',flush=True)
H={'3C':0,'6H':1/3,'4H':1/2,'2H':1}
for L in range(6,21,2):
    v={k:res[k][L-1] for k in res}; span=v['2H']-v['3C']
    lin=' '.join(f"{k} {v[k]:.1f}" for k in ('3C','6H','4H','2H'))
    dev='' if abs(span)<1e-9 else '  law check: '+', '.join(f"{k} off {(v[k]-(v['3C']+span*H[k]))/span*100:+.1f}%" for k in ('6H','4H'))
    print(f'L={L:2d}: {lin}{dev}')
