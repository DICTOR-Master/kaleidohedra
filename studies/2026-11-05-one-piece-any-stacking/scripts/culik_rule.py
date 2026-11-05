"""Route (a)(i) v2: keep all tiles, forbid two adjacent n=0 in x1/2 rows.
Route (a)(i): Culik-type set (x3 on [1/3,2/3], x1/2 on [2/3,2]) WITHOUT the all-zero tile.
Does it still tile big squares (free boundary)? Tori (periodic) must stay UNSAT. HEARTBEAT + FINAL lines."""
import sys,time
from fractions import Fraction as Fr
from math import floor
from pysat.solvers import Cadical153
from pysat.card import CardEnc
t0=time.time()
def hb(m): print(f"HEARTBEAT {time.time()-t0:.0f}s {m}",flush=True)
def tiles(q,lo,hi):
    T=set()
    for den in (97,101,103,107,211,307):
        for a in range(int(lo*den),int(hi*den)+1):
            x=Fr(a,den)
            if not(lo<=x<=hi): continue
            for k in range(1,400):
                n=floor(k*x)-floor((k-1)*x); s=floor(k*q*x)-floor((k-1)*q*x)
                w=q*floor((k-1)*x)-floor((k-1)*q*x); e=q*floor(k*x)-floor(k*q*x)
                T.add((q,n,s,w,e))
    return T
T=sorted(tiles(Fr(3),Fr(1,3),Fr(2,3))|tiles(Fr(1,2),Fr(2,3),Fr(2)))
print('all tiles',len(T)); Z=[t for t in T if t[1:]==(0,0,0,0)]; print('zero tiles',Z)
RULE=True  # no two horizontally adjacent x1/2 tiles with n=0 (true rows have x>=2/3)
for q in (Fr(3),Fr(1,2)):
    ts=[t for t in T if t[0]==q]
    print(f' x{q}: tiles {len(ts)}, down (n,w) {len({(t[1],t[3]) for t in ts})}, up (qn+w,s) {len({(q*t[1]+t[3],t[2]) for t in ts})}')
def solve(R,C,torus):
    v=lambda r,c,i: 1+(r*C+c)*len(T)+i
    S=Cadical153(); top=R*C*len(T)
    for r in range(R):
        for c in range(C):
            S.add_clause([v(r,c,i) for i in range(len(T))])
            for i in range(len(T)):
                for j in range(i+1,len(T)): S.add_clause([-v(r,c,i),-v(r,c,j)])
            for dr,dc in ((0,1),(1,0)):
                r2,c2=r+dr,c+dc
                if torus: r2%=R; c2%=C
                elif r2>=R or c2>=C: continue
                for i,a in enumerate(T):
                    ok=[v(r2,c2,j) for j,b in enumerate(T) if (dc==1 and a[0]==b[0] and a[4]==b[3] and not(RULE and a[0]==Fr(1,2) and a[1]==0 and b[1]==0)) or (dr==1 and a[2]==b[1])]
                    S.add_clause([-v(r,c,i)]+ok)
    return S.solve()
for R,C in [(2,2),(3,3),(4,4),(6,6),(2,6),(3,4),(6,4)]:
    hb(f'torus {R}x{C}: {"SAT" if solve(R,C,True) else "UNSAT"}')
ok=True
for N in (8,16,24,32,48,64):
    r=solve(N,N,False); hb(f'square {N}x{N} free boundary: {"SAT" if r else "UNSAT"}'); ok&=r
    if not r: break
print('FINAL', 'OK tiles all squares tested' if ok else 'FAIL a square is UNSAT', f'{time.time()-t0:.0f}s',flush=True)
