# Control for loops.py: coordination sequences (graph shells) of the same networks must DIFFER between 3C and 2H (known:
# diamond 4,12,24,42,64,92; lonsdaleite 4,12,25,44,67,96), proving the identical loop counts are not a code artefact.
import numpy as np
exec(open('pyro_counts.py').read().split('def analyse')[0].replace('N=6','N=8'))
for name,seq in [('3C','ABC'),('2H','AB'),('4H','ABAC')]:
    seq2=seq*(-(-12//len(seq))); P,cell,bond=build(seq2); M=len(P)
    D=np.linalg.norm(mic(P[:,None,:]-P[None,:,:],cell),axis=2); nb=[list(np.where(np.abs(D[i]-bond)<1e-6)[0]) for i in range(M)]
    tot=np.zeros(6)
    for s0 in range(M):
        seen={s0}; front=[s0]
        for k in range(6):
            nxt=set(w for v in front for w in nb[v] if w not in seen); seen|=nxt; front=list(nxt); tot[k]+=len(nxt)
    print(name,'coordination sequence (mean per atom):',[round(x/M,3) for x in tot])
