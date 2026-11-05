"""Do Kari's 14 tiles also tile rows read right-to-left (carry entering from the east), as turned Narcissus layers need?
Forward tile (q,n,s,w,e): q*n + w = s + e, w = in (from west), e = out (to east). A piece turned 180 deg about the vertical
takes its in-carry from the east. Reversed row: in at i is c'(i+1), out is c'(i), with c'(i) = K - g(i), g(i) = q*floor(i x) - floor(i q x)."""
from fractions import Fraction as Fr
from math import floor
import json
T={(q,n,s,w,e) for (q,n,s,w,e) in json.load(open('kari-tiles.json'))} if False else None
T=set()
for q,lo,hi in ((Fr(2),Fr(1,2),Fr(1)),(Fr(2,3),Fr(1),Fr(2))):
    for den in (97,101,103,107,211,307):
        for a in range(int(lo*den),int(hi*den)+1):
            x=Fr(a,den)
            if not(lo<=x<=hi): continue
            for k in range(1,400):
                n=floor(k*x)-floor((k-1)*x); s=floor(k*q*x)-floor((k-1)*q*x)
                w=q*floor((k-1)*x)-floor((k-1)*q*x); e=q*floor(k*x)-floor(k*q*x)
                T.add((q,n,s,w,e))
print('forward tiles',len(T))
g=lambda q,x,i: q*floor(i*x)-floor(i*q*x)
for q,lo,hi in ((Fr(2),Fr(1,2),Fr(1)),(Fr(2,3),Fr(1),Fr(2))):
    carries=sorted({t[3] for t in T if t[0]==q}|{t[4] for t in T if t[0]==q})
    okK=[]
    for K in [c1+c2 for c1 in carries for c2 in carries]:
        bad=0; tot=0
        for den in (97,101,103,211):
            for a in range(int(lo*den),int(hi*den)+1):
                x=Fr(a,den)
                if not(lo<=x<=hi): continue
                for i in range(1,300):
                    n=floor(i*x)-floor((i-1)*x); s=floor(i*q*x)-floor((i-1)*q*x)
                    # tile at column i: forward uses w=g(i-1), e=g(i). Reversed: in = K-g(i), out = K-g(i-1)
                    tup=(q,n,s,K-g(q,x,i),K-g(q,x,i-1)); tot+=1
                    if tup not in T: bad+=1
        if bad==0: okK.append(K)
    print('q',q,'carries',[str(c) for c in carries],'reversed rows with the SAME 14 tiles for K =',sorted(set(str(k) for k in okK)) or 'none')
    if not okK:
        need=set()
        for den in (97,101,103,211):
            for a in range(int(lo*den),int(hi*den)+1):
                x=Fr(a,den)
                if not(lo<=x<=hi): continue
                K=min(carries)+max(carries)
                for i in range(1,300):
                    n=floor(i*x)-floor((i-1)*x); s=floor(i*q*x)-floor((i-1)*q*x)
                    need.add((q,n,s,K-g(q,x,i),K-g(q,x,i-1)))
        print('   extra tiles needed (K = min+max):',sorted((str(t[0]),t[1],t[2],str(t[3]),str(t[4])) for t in need-T))
