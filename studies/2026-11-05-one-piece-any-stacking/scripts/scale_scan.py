"""Route (a): rescale the Culik (x3 / x1/2) and Kari (x2 / x2/3) maps by a; count tiles, per-piece states (pair split), n=s=0 tiles."""
from fractions import Fraction as Fr
from math import floor
def tiles(q,lo,hi):
    T=set()
    for den in (97,101,103,107,211,307):
        for a in range(int(lo*den),int(hi*den)+1):
            x=Fr(a,den)
            if not(lo<=x<=hi): continue
            for k in range(1,300):
                n=floor(k*x)-floor((k-1)*x); s=floor(k*q*x)-floor((k-1)*q*x)
                w=q*floor((k-1)*x)-floor((k-1)*q*x); e=q*floor(k*x)-floor(k*q*x)
                T.add((n,s,w,e))
    return T
fam={'Culik x3 [a,2a] / x1/2 [2a,6a]':lambda a:[(Fr(3),a,2*a),(Fr(1,2),2*a,6*a)],
     'Kari x2 [a,2a] / x2/3 [2a,4a]':lambda a:[(Fr(2),a,2*a),(Fr(2,3),2*a,4*a)]}
for name,f in fam.items():
    print(name)
    for a in (Fr(1,4),Fr(1,3),Fr(2,5),Fr(1,2),Fr(3,5),Fr(2,3),Fr(3,4),Fr(1)):
        row=[]; worst=0; tot=0; zz=0
        for q,lo,hi in f(a):
            T=tiles(q,lo,hi); D={(n,w) for n,s,w,e in T}; U={(q*n+w,s) for n,s,w,e in T}
            tot+=len(T); worst=max(worst,len(D),len(U)); zz+=sum(1 for t in T if t[0]==0 and t[1]==0)
            row.append(f"x{q}:{len(T)}t D{len(D)} U{len(U)}")
        print(f"  a={a}: total {tot}, max per piece {worst}, n=s=0 tiles {zz} | "+'; '.join(row))
