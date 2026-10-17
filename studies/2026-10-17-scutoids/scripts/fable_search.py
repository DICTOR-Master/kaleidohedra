# Fable 2026-10-17: two-colourings T/B of the triangular lattice (cell centres of the hexagonal honeycomb),
# periodic on a sublattice, such that every T cell has exactly one T-T edge whose two flanking cells are B,
# and every B cell has exactly one B-B edge whose two flanking cells are T. Exact combinatorics (integers).
import itertools, sys
NB = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
def edges_dirs(): return [(1,0),(0,1),(-1,1)]  # each undirected edge once
def flanks(d):
    # common neighbours of 0 and d
    return [n for n in NB if (n[0]-d[0],n[1]-d[1]) in NB]
def run(a,b,d):
    # sublattice basis (a,0),(b,d); reps i in [0,a), j in [0,d)
    def red(i,j):
        q=j//d; j-=q*d; i-=q*b; return (i%a, j)
    cells=[(i,j) for j in range(d) for i in range(a)]; n=len(cells); idx={c:k for k,c in enumerate(cells)}
    E=[]
    for c in cells:
        for dd in edges_dirs():
            o=red(c[0]+dd[0],c[1]+dd[1]); f=[red(c[0]+x,c[1]+y) for x,y in flanks(dd)]
            E.append((idx[c],idx[o],idx[f[0]],idx[f[1]]))
    res=[]
    for bits in itertools.product((0,1),repeat=n):
        if bits[0]!=1 or sum(bits)*2!=n: continue
        cnt=[0]*n; ok=True
        for (p,q,r,s) in E:
            if p==q: ok=False;break
            if bits[p]==bits[q] and bits[r]!=bits[p] and bits[s]!=bits[p]:
                cnt[p]+=1; cnt[q]+=1
        if ok and all(c==1 for c in cnt): res.append(bits)
    return res
out=[]
for n in range(2,int(sys.argv[1])+1):
    for a in range(1,n+1):
        if n%a: continue
        d=n//a
        for b in range(a):
            r=run(a,b,d)
            if r: out.append((n,a,b,d,len(r),r[0])); print(n,a,b,d,len(r),r[0],flush=True)
