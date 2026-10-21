# Can the OG's 20 hexagons be lettered so that round EVERY five-kite star (12 of them) the five hexagons read
# D-I-C-T-O clockwise (seen from outside), each star a cyclic shift, like the rows of the DICTO square?
import json, itertools, numpy as np
G=json.load(open('og-geometry.json')); V=np.array(G['v']); F=G['f']
deg={}
for f in F:
    if len(f)==4:
        for q in f: deg[q]=deg.get(q,0)+1
stars=[q for q in deg if deg[q]==5]; assert len(stars)==12
H=[f for f in F if len(f)==6]; C=np.array([V[f].mean(0) for f in H])
rings=[]
for s in stars:
    a=V[s]/np.linalg.norm(V[s]); d=np.linalg.norm(C/np.linalg.norm(C,axis=1)[:,None]-a,axis=1)
    ring=list(np.argsort(d)[:5])
    # clockwise seen from outside (looking along -a)
    e1=np.cross(a,[0.3,0.5,0.8]); e1/=np.linalg.norm(e1); e2=np.cross(a,e1)
    ang=[np.arctan2(C[i]@e2,C[i]@e1) for i in ring]
    ring=[ring[i] for i in np.argsort(ang)[::-1]]       # decreasing angle = clockwise from outside
    rings.append(ring)
assert sorted(sum(rings,[]))==sorted(list(range(20))*3)   # every hexagon round exactly 3 stars
def solve(order):
    sols=[]
    def rec(k,L):
        if k==len(rings): sols.append(dict(L)); return
        r=rings[k]
        for sh in range(5):
            want={r[i]:order[(i+sh)%5] for i in range(5)}
            if all(L.get(h,c)==c for h,c in want.items()):
                L2=dict(L); L2.update(want); rec(k+1,L2)
    rec(0,{}); return sols
cw=solve('DICTO'); print('clockwise D-I-C-T-O round every star:', len(cw), 'letterings')
acw=solve('OTCID'); print('anticlockwise round every star:', len(acw))
# mixed: each star either way
def solve_mixed():
    n=0
    def rec(k,L):
        nonlocal n
        if k==len(rings): n+=1; return
        r=rings[k]
        for order in ('DICTO','OTCID'):
            for sh in range(5):
                want={r[i]:order[(i+sh)%5] for i in range(5)}
                if all(L.get(h,c)==c for h,c in want.items()):
                    L2=dict(L); L2.update(want); rec(k+1,L2)
    rec(0,{}); return n
print('each star D-I-C-T-O one way or the other:', solve_mixed())
# check of the search: letterings where every star merely has all five letters (any order) = 2 compounds x 5! = 240
def solve_any():
    n=0
    def rec(k,L):
        nonlocal n
        if k==len(rings): n+=1; return
        r=rings[k]; fixed={h:L[h] for h in r if h in L}
        free=[h for h in r if h not in L]; left=[c for c in 'DICTO' if c not in fixed.values()]
        if len(set(fixed.values()))<len(fixed): return
        for p in itertools.permutations(left):
            L2=dict(L); L2.update(dict(zip(free,p))); rec(k+1,L2)
    rec(0,{}); return n
print('check, every star has all five letters:', solve_any())
# which orders do occur round the stars in the compound lettering?
sol=[]
def rec(k,L):
    if sol: return
    if k==len(rings): sol.append(L); return
    r=rings[k]; fixed={h:L[h] for h in r if h in L}; free=[h for h in r if h not in L]; left=[c for c in 'DICTO' if c not in fixed.values()]
    if len(set(fixed.values()))<len(fixed): return
    for p in itertools.permutations(left):
        L2=dict(L); L2.update(dict(zip(free,p))); rec(k+1,L2)
rec(0,{})
L=sol[0]
for r in rings:
    w=''.join(L[h] for h in r); i=w.index('D'); print(w[i:]+w[:i], end='  ')
print()
