"""The skeleton of the 4D permutohedron as a web of bonds (DICTO 11 Nov: "B the skeleton as a web of bonds"). Corners = the 120 orderings
of 1..5; a bond = swapping two neighbouring VALUES (k, k+1) = an edge. Exact counts: bonds per corner, bond directions, distance from one
ordering = number of out-of-order pairs, shortest routes from 12345 to 54321, the web's small rings (squares, hexagons) = its 2-faces,
descents per corner = the sweep's h-vector (#104)."""
import itertools
from collections import Counter, deque
from functools import lru_cache
n=5; V=list(itertools.permutations(range(1,n+1))); idx={v:i for i,v in enumerate(V)}
def bonds(p):
    out=[]
    for k in range(1,n):
        q=tuple(k+1 if x==k else k if x==k+1 else x for x in p); out.append(q)
    return out
deg=Counter(len(bonds(p)) for p in V); E={frozenset((p,q)) for p in V for q in bonds(p)}
dirs=Counter(tuple(sorted(abs(a-b) for a,b in zip(*sorted(e)) if a!=b)) for e in E)
dirv=Counter(tuple(a-b for a,b in zip(*sorted(e))) for e in E)
inv=lambda p: sum(1 for i in range(n) for j in range(i+1,n) if p[i]>p[j])
src=tuple(range(1,n+1)); dist={src:0}; Q=deque([src])
while Q:
    p=Q.popleft()
    for q in bonds(p):
        if q not in dist: dist[q]=dist[p]+1; Q.append(q)
ok=all(dist[p]==inv(p) for p in V)
@lru_cache(None)
def routes(p):
    if p==src: return 1
    return sum(routes(q) for q in bonds(p) if dist[q]==dist[p]-1)
desc=Counter(sum(1 for i in range(n-1) if p[i]>p[i+1]) for p in V)
print(f'corners {len(V)}, bonds {len(E)}, bonds per corner {dict(deg)}, distinct bond directions {len(dirv)//1}')
print(f'distance from 12345 = number of out-of-order pairs: {"PASS" if ok else "FAIL"}; corners at distance 0..10: {[Counter(dist.values())[k] for k in range(11)]}')
print(f'shortest routes 12345 -> 54321 (10 bonds): {routes(tuple(range(n,0,-1)))}')
print(f'corners by descents (= h-vector of the sweep): {[desc[k] for k in range(n)]}')
print('FINAL ok' if ok and len(E)==240 else 'FINAL FAIL')
