from fractions import Fraction as Fr
from math import floor
def tiles(q,lo,hi):
    T=set()
    for den in (97,101,103,107,211):
        for a in range(int(lo*den),int(hi*den)+1):
            x=Fr(a,den)
            if not(lo<=x<=hi): continue
            for k in range(1,300):
                n=floor(k*x)-floor((k-1)*x); s=floor(k*q*x)-floor((k-1)*q*x)
                w=q*floor((k-1)*x)-floor((k-1)*q*x); e=q*floor(k*x)-floor(k*q*x)
                T.add((n,s,w,e))
    return T
def counts(q,lo,hi):
    ts=tiles(q,lo,hi)
    D={(n,w) for n,s,w,e in ts}; U={(q*n+w,s) for n,s,w,e in ts}
    zero=(0,0,0,0) in ts
    return len(ts),len(D),len(U),zero
# Kari-type maps: two branches covering [lo,hi]; product of multipliers never 1 (2^a 3^b)
cands=[("Kari x2 [1/2,1] / x2/3 [1,2]",[(Fr(2),Fr(1,2),Fr(1)),(Fr(2,3),Fr(1),Fr(2))]),
       ("x3 [1/3,2/3] / x1/2 [2/3,2] (Culik-type)",[(Fr(3),Fr(1,3),Fr(2,3)),(Fr(1,2),Fr(2,3),Fr(2))]),
       ("x2 [1,3/2] / x3/4... skip",[]),
       ("x3/2 [2/3,4/3] / x1/2 [4/3,2]",[(Fr(3,2),Fr(2,3),Fr(4,3)),(Fr(1,2),Fr(4/3) if False else Fr(4,3),Fr(2))]),
       ("x2 [1,2] / x1/3 [2,4]",[(Fr(2),Fr(1),Fr(2)),(Fr(1,3),Fr(2),Fr(4))]),
       ("x2 [3/2,3] / x2/3 [3,...]",[]),
       ("x2 [1,3/2] / x2/3 [3/2,3]",[(Fr(2),Fr(1),Fr(3,2)),(Fr(2,3),Fr(3,2),Fr(3))]),
       ("x3/2 [1,2] / x2/3? (=1 cycle) skip",[]),
       ("x4/3 [3/4,3/2]... / x1/2 [3/2,3]",[(Fr(4,3),Fr(3,4),Fr(3,2)),(Fr(1,2),Fr(3,2),Fr(3))]),
]
for name,br in cands:
    if not br: continue
    print(name)
    for q,lo,hi in br:
        t,d,u,z=counts(q,lo,hi); print(f"   x{q} on [{lo},{hi}]: tiles {t}, piece D {d}, piece U {u}, all-zero tile {z}")
