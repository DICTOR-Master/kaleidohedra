"""Ring-system test: C1 (basis coefficient pair (pi,beta)) or C2 (pair (pi,alpha)) + ONE flat-faced scutoid kind S, rings by exact integer arithmetic.
Angles are vectors (p,b) = p*pi + b*X, X = beta (C1) or alpha (C2); pi and X independent (proved in packet-leads-tiling), so a ring closes iff
sum p = 2 (or 1 on a face) and sum b = 0.  S parallel faces meet each side plane at t=(p,b) on top and pi-t=(1-p,-b) at the bottom.
Part A: which S edge kinds the reflex and hex-hex (or decagon) rings force.  Part B: lateral edges (between side planes) from the closure of the
side-plane azimuths: with side-plane tilt delta (cos delta = c) and sign eps=+-1, lateral dihedral phi between neighbours obeys
 -cos(phi) = (1-c^2) cos(D) + eps_i eps_j c^2,  sum of azimuth steps D = 2 pi (convex polygon section).  Search small k, phi rational multiples of pi."""
import itertools, json, sys
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 50
def pr(s): print(s, flush=True)
def rings_with(kinds, target_kind, caps=None):
    """all nonneg integer ring multisets containing target_kind with sum (2,0) or (1,0)"""
    names=list(kinds); sols=[]
    def rec(i,cur,p,b,cnt):
        if p>2: return
        if i==len(names):
            if b==0 and p in (1,2) and cnt.get(target_kind,0)>0: sols.append((p,dict((k,v) for k,v in cnt.items() if v)))
            return
        k=names[i]; v=kinds[k]; n=0
        while p+n*v[0]<=2 and n<=6:
            cnt[k]=n; rec(i+1,cur,p+n*v[0],b+n*v[1],cnt); n+=1
        cnt[k]=0
    rec(0,None,F(0),F(0),{})
    return sols
CASES={
 'C1':dict(X='beta',h=(F(3,2),F(-2)),r=(F(3,4),F(1)),s=(F(2,3),F(0)),delta=('3pi/4 - beta'),
           c2=(3-mp.sqrt(5))/6, T=(F(1,4),F(1)),B=(F(3,4),F(-1))),
 'C2':dict(X='alpha',h=(F(0),F(2)),r=(F(3,2),F(-1)),s=(F(2,5),F(0)),delta='alpha',
           c2=(5-mp.sqrt(5))/10, T=(F(1),F(-1)),B=(F(0),F(1))),
}
out={}
for nm,C in CASES.items():
    pr(f"==== {nm} (X = {C['X']})")
    base={'h':C['h'],'r':C['r'],'s':C['s']}
    # Part A: general S: what edge vectors can complement the reflex ring / h ring?  Candidates: all (p,b) with p in k/12 and b in -2..2, 0<angle<pi
    # first the forced facts
    hv,rv=C['h'],C['r']
    pr(f"reflex ring needs S+rational complement of ({2-rv[0]},{-rv[1]}); h ring needs ({2-hv[0]},{-hv[1]})")
    pr("  single convex complement of the reflex edge: "+str((2-rv[0],-rv[1]))+f"; hh complement is over pi in angle, so >= 2 S edges (b total {-hv[1]})")
    T,B=C['T'],C['B']
    pr(f"minimal S pair: top {T} / bottom {B} (sum {T[0]+B[0]},{T[1]+B[1]} = (1,0), a side plane)")
    # rational remainder in the reflex ring, with only {r, B, rational laterals, s}: remainder = 2 - r - B
    rem=2-rv[0]-B[0]; pr(f"ring r + B leaves rational remainder {rem} pi; hh ring h + 2T: p-sum {hv[0]+2*T[0]}, b-sum {hv[1]+2*T[1]}")
    out[nm]=dict(remainder_in_reflex_ring=str(rem))
    # Part B: S with k side planes, tilt delta all eps combos
    c2=C['c2']; one=1-c2
    import math
    def Dstep(phi,e,f=False):
        v=(-mp.cos(mp.pi*phi)-e*c2)/one
        if not -1<=v<=1: return None
        return float(mp.acos(v)) if f else mp.acos(v)
    fr3=sorted({F(j,n) for n in range(2,13) for j in range(1,n)})
    fr4=sorted({F(j,n) for n in range(2,9) for j in range(1,n)})
    tab={(f,e):Dstep(f,e,True) for f in fr3 for e in (1,-1)}
    tabm={(f,e):Dstep(f,e) for f in fr3 for e in (1,-1)}
    hits=[]
    for k in (3,4):
        for phis in itertools.product(fr3 if k==3 else fr4,repeat=k):
            for es in itertools.product((1,-1),repeat=k-1):
                es=(1,)+es
                ok=True; tot=0
                for i in range(k):
                    e=es[i]*es[(i+1)%k]; d=tab[(phis[i],e)]
                    if d is None: ok=False;break
                    tot+=d
                if not ok or abs(tot-2*math.pi)>1e-9: continue
                tot=sum(tabm[(phis[i],es[i]*es[(i+1)%k])] for i in range(k))
                if abs(tot-2*mp.pi)>mp.mpf(10)**-25: continue
                hits.append((k,phis,es))
    pr(f"closed side-plane polygons with rational lateral dihedrals (k<=4, denominators<=12): {len(hits)} (up to cyclic order repeats)")
    good=[]
    seen=set()
    for k,phis,es in hits:
        key=(k,tuple(sorted(phis)))
        if key in seen: continue
        seen.add(key)
        kinds=dict(base); kinds['T']=T; kinds['B']=B
        for j,f in enumerate(sorted(set(phis))): kinds[f'L{f}']=(f,F(0))
        need=['h','r','s','T','B']+[k_ for k_ in kinds if k_.startswith('L')]
        allok=True; rr={}
        for kd in need:
            s=rings_with(kinds,kd)
            if not s: allok=False; break
            rr[kd]=s[0]
        if allok: good.append((k,sorted(set(phis)),rr))
    pr(f"  distinct S candidates: {len(seen)};  those where EVERY edge kind (h,r,s,T,B and each lateral) lies in a closing ring: {len(good)}")
    for k,ph,rr in good[:6]:
        pr(f"   k={k} laterals {[str(x)+'pi' for x in ph]}  rings: "+'; '.join(f"{kd}:{r[1]}" for kd,r in rr.items() if kd in ('r','h')))
    out[nm].update(candidates=len(seen),feasible=len(good),examples=[(k,[str(x) for x in ph]) for k,ph,_ in good[:6]],
                   all_hits=[(k,[str(x) for x in ph]) for k,ph,_ in [(h[0],h[1],0) for h in hits][:12]])
    # the unique 'regular' frustum
    pr("  regular frustum k sides, tilt delta, lateral phi: "+', '.join(f"k={k}: {mp.nstr(mp.acos(-((1-c2)*mp.cos(2*mp.pi/k)+c2))*180/mp.pi,8)} deg" for k in (3,4,5,6)))
json.dump(out,open('data/rings.json','w'),indent=1)
pr("FINAL ok" if all(v["feasible"]>0 for v in out.values()) else "FINAL FAIL")
