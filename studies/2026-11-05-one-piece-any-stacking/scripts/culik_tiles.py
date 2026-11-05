"""Culik's variant of Kari's method (1996, 13 Wang tiles): x -> 3x on [1/3, 2/3], x -> x/2 on (2/3, 2]. Count the q-tagged tile set,
its digits, carries and whether rows also run right-to-left with the same tiles (needed in turned slabs)."""
from fractions import Fraction as Fr
from math import floor
def tiles(spec):
    T=set()
    for q,lo,hi in spec:
        for den in (97,101,103,107,211,307,401):
            for a in range(int(lo*den),int(hi*den)+1):
                x=Fr(a,den)
                if not(lo<=x<=hi): continue
                for k in range(1,500):
                    n=floor(k*x)-floor((k-1)*x); s=floor(k*q*x)-floor((k-1)*q*x)
                    w=q*floor((k-1)*x)-floor((k-1)*q*x); e=q*floor(k*x)-floor(k*q*x)
                    T.add((q,n,s,w,e))
    return T
def rev_ok(T,spec):
    g=lambda q,x,i:q*floor(i*x)-floor(i*q*x); out={}
    for q,lo,hi in spec:
        cs=sorted({t[3] for t in T if t[0]==q}|{t[4] for t in T if t[0]==q}); good=[]
        for K in {a+b for a in cs for b in cs}:
            ok=True
            for den in (97,101,103,211):
                for a in range(int(lo*den),int(hi*den)+1):
                    x=Fr(a,den)
                    if not(lo<=x<=hi): continue
                    for i in range(1,300):
                        n=floor(i*x)-floor((i-1)*x); s=floor(i*q*x)-floor((i-1)*q*x)
                        if (q,n,s,K-g(q,x,i),K-g(q,x,i-1)) not in T: ok=False; break
                    if not ok: break
                if not ok: break
            if ok: good.append(str(K))
        out[str(q)]=good
    return out
for name,spec in (('Kari',((Fr(2),Fr(1,2),Fr(1)),(Fr(2,3),Fr(1),Fr(2)))),('Culik',((Fr(3),Fr(1,3),Fr(2,3)),(Fr(1,2),Fr(2,3),Fr(2))))):
    T=tiles(spec)
    by={str(q):sum(1 for t in T if t[0]==q) for q,_,_ in spec}
    print(name,'tiles',len(T),by,'digits n',sorted({t[1] for t in T}),'s',sorted({t[2] for t in T}),'reversed rows K:',rev_ok(T,spec))
