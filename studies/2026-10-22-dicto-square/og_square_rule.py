# The DICTO square's neighbour rule on the OG: in the square, side-by-side cells always hold letters that are
# neighbours in the cycle D-I-C-T-O-D (D next to I or O, never C or T). Neighbouring hexagons on the OG are the
# consecutive hexagons round a star (30 pairs). How many pairs can follow the rule at best?
import json, random, numpy as np
G=json.load(open('og-geometry.json')); V=np.array(G['v']); H=[f for f in G['f'] if len(f)==6]
C=np.array([V[f].mean(0) for f in H]); C/=np.linalg.norm(C,axis=1)[:,None]; Dd=C@C.T
E=[(i,j) for i in range(20) for j in range(i+1,20) if abs(Dd[i,j]-Dd[0][np.argsort(-Dd[0])[1]])<1e-6]
print('neighbour pairs', len(E))
good=lambda L,i,j: (L[i]-L[j])%5 in (1,4)
best=0; random.seed(1); bestL=None
for run in range(4000):
    L=[random.randrange(5) for _ in range(20)]
    for it in range(400):
        i=random.randrange(20); old=L[i]; s0=sum(good(L,a,b) for a,b in E)
        L[i]=random.randrange(5); s1=sum(good(L,a,b) for a,b in E)
        if s1<s0 and random.random()>0.05: L[i]=old
    s=sum(good(L,a,b) for a,b in E)
    if s>best: best=s; bestL=L[:]
print('best pairs following the rule:', best, 'of', len(E))
print('letters used:', {c:bestL.count(k) for k,c in enumerate('DICTO')})
# a proof bound: each of the 12 rings of five is an odd cycle; following the rule all round it would need DICTO
# in order round that star (shown impossible for all 12 at once in og_star_letters.py); each pair lies in 2 rings.
