"""Per-piece state counts for the Culik set + 'no two adjacent n=0 in x1/2 rows', split over a pair:
D (down) shows n, takes carry w and the flag z_in (left tile had n=0); passes m=qn+w and z=(n==0) to U.
U (up) takes (m,z), shows s, gives carry e and the flag z on to the next D. Counts are over pairs realised in real rows (Beatty, many x)."""
from fractions import Fraction as Fr
from math import floor
def rows(q,lo,hi):
    out=set()
    for den in (97,101,103,107,211,307):
        for a in range(int(lo*den),int(hi*den)+1):
            x=Fr(a,den)
            if not(lo<=x<=hi): continue
            prevz=None
            for k in range(1,400):
                n=floor(k*x)-floor((k-1)*x); s=floor(k*q*x)-floor((k-1)*q*x)
                w=q*floor((k-1)*x)-floor((k-1)*q*x); e=q*floor(k*x)-floor(k*q*x)
                if prevz is not None: out.add((n,s,w,e,prevz))
                prevz=int(n==0)
    return out
for q,lo,hi in ((Fr(3),Fr(1,3),Fr(2,3)),(Fr(1,2),Fr(2,3),Fr(2))):
    R=rows(q,lo,hi)
    flag = q==Fr(1,2)
    D={(n,w,z) if flag else (n,w) for n,s,w,e,z in R}
    U={(q*n+w,int(n==0),s) if flag else (q*n+w,s) for n,s,w,e,z in R}
    print(f"x{q}: tile uses {len(R)}; D states {len(D)} {sorted(D)}; U states {len(U)}")
