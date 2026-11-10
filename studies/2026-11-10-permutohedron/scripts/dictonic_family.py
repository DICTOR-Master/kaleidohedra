import itertools, sympy as sp
from collections import Counter
t=(1+sp.sqrt(5))/2
def fp(P):
    d=Counter(sp.radsimp(sp.expand(sum((a-b)**2 for a,b in zip(p,q)))) for p,q in itertools.combinations(P,2))
    m=min(d, key=lambda k: float(k)); return sorted(((sp.radsimp(sp.expand(k/m)),v) for k,v in d.items()), key=lambda z: float(z[0]))
def T(x):
    s=set()
    for p in itertools.permutations((1+x,x,0)):
        for sg in itertools.product((1,-1),repeat=3): s.add(tuple(sp.expand(a*b) for a,b in zip(p,sg)))
    return list(s)
for x,vals in [(t,(-t**3,-1,1,t**3)),(sp.Integer(1),(-3,-1,1,3)),(sp.Rational(1,2),(-2,-1,1,2))]:
    P=[tuple(sp.expand(v) for v in p) for p in itertools.permutations(vals)]
    a=fp(T(x)); b=fp(P)
    print(x, len(T(x)), 'same shape:', len(a)==len(b) and all(sp.simplify(k1-k2)==0 and v1==v2 for (k1,v1),(k2,v2) in zip(a,b)))
