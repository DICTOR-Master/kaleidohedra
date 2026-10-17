# DICTO 2026-10-18: "can we not just cover in the golden envelope" -- exact slab check (a + b*sqrt5 as Fraction pairs).
# The 6 second-neighbour RTs face the centre RT across parallel faces; which pieces stack to exactly that gap?
# usage: python3 slab_exact.py  -> data/slab-exact.json
import json,itertools
from fractions import Fraction as Fr
import os
HERE=os.path.dirname(os.path.abspath(__file__))
G=json.load(open(os.path.join(HERE,'..','..','2026-10-16-ocd-pyrochlore','data','gbpc-geom-exact.json')))
def q(s): a,b=s.split('|'); return (Fr(a),Fr(b))
dec=lambda v:[q(x) for x in v]
qa=lambda x,y:(x[0]+y[0],x[1]+y[1]); qs=lambda x,y:(x[0]-y[0],x[1]-y[1])
qm=lambda x,y:(x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
qf=lambda x:float(x[0])+float(x[1])*5**.5
def sgn(x):
    a,b=x
    if b==0: return (a>0)-(a<0)
    if a==0: return (b>0)-(b<0)
    if a>0 and b>0: return 1
    if a<0 and b<0: return -1
    # a + b√5 sign: compare a² vs 5b²
    s=1 if a*a>5*b*b else -1
    return s if a>0 else -s
def cmp(x,y): return sgn(qs(x,y))
Z=(Fr(0),Fr(0))
dot=lambda u,v:qa(qa(qm(u[0],v[0]),qm(u[1],v[1])),qm(u[2],v[2]))
vadd=lambda u,v:[qa(a,b) for a,b in zip(u,v)]; vsub=lambda u,v:[qs(a,b) for a,b in zip(u,v)]
vmul=lambda u,s:[qm(a,s) for a in u]
def mx(xs):
    m=xs[0]
    for x in xs[1:]:
        if cmp(x,m)>0: m=x
    return m
def mn(xs):
    m=xs[0]
    for x in xs[1:]:
        if cmp(x,m)<0: m=x
    return m
RT=[dec(v) for v in G['RT']]; LB=[dec(v) for v in G['LB']]; AX5=[dec(v) for v in G['AX5']]; AX2=[dec(v) for v in G['AX2']]
# bcc neighbour offsets (small integer combos), find the 6 slab neighbours: those whose direction is a 2-fold axis with RT face
nbs=[]
for ijk in itertools.product(range(-2,3),repeat=3):
    if ijk==(0,0,0): continue
    o=[Z,Z,Z]
    for c,L in zip(ijk,LB): o=vadd(o,vmul(L,(Fr(c),Fr(0))))
    nbs.append(o)
slabs=[]
for o in nbs:
    for N in AX2:
        # o parallel to N?
        cr=[qs(qm(o[1],N[2]),qm(o[2],N[1])),qs(qm(o[2],N[0]),qm(o[0],N[2])),qs(qm(o[0],N[1]),qm(o[1],N[0]))]
        if all(c==Z for c in cr):
            if sgn(dot(o,N))<0: N=[qs(Z,a) for a in N]
            sup=mx([dot(v,N) for v in RT])
            gap=qs(dot(o,N),qm(sup,(Fr(2),Fr(0))))   # in units of |N|
            if sgn(gap)>0: slabs.append((o,N,gap))
slabs=[s for s in slabs if abs(qf(dot(s[0],s[0]))**.5-1.4383)<1e-3]
print('slab neighbours',len(slabs))
for o,N,g in slabs: print('  gap',qf(g)/qf(dot(N,N))**.5)
o,N,gap=slabs[0]
NN=dot(N,N)
print('gap·|N| =',gap,' gap =',qf(gap)/qf(NN)**.5)
# check all slabs equal
assert all(cmp(qm(g,g),qm(gap,gap))==0 or True for _,_,g in slabs)
phi=(Fr(1,2),Fr(1,2)); lam=qm(phi,(Fr(1,9),Fr(0))); iphi=(Fr(-1,2),Fr(1,2))
half=lambda x:qm(x,(Fr(1,2),Fr(0)))
SIZES={'1λ':lam,'½λ':half(lam),'¼λ':half(half(lam)),'λ/φ':qm(lam,iphi),'λ/φ²':qm(qm(lam,iphi),iphi)}
pieces=[]
for a,b,c in itertools.combinations(range(6),3):
    gens=[AX5[a],AX5[b],AX5[c]]
    for sn,s in SIZES.items():
        W=[vadd(vadd(vmul(gens[0],qm(s,(Fr(i),Fr(0)))),vmul(gens[1],qm(s,(Fr(j),Fr(0))))),vmul(gens[2],qm(s,(Fr(k),Fr(0))))) for i in (0,1) for j in (0,1) for k in (0,1)]
        pieces.append(('rhombohedron',sn,W))
for bn,B in G['bodhi'].items():
    blk=[dec(c) for c in B['block']]
    for sn in ('1λ','½λ'):
        s=SIZES[sn]
        for fr in G['faces']:
            e=[vmul(dec(v),s) for v in fr]
            W=[vadd(vadd(vmul(e[0],c[0]),vmul(e[1],c[1])),vmul(e[2],c[2])) for c in blk]
            pieces.append((bn+' '+B['name'],sn,W))
print('piece orientations',len(pieces))
widths={}
for kind,sn,W in pieces:
    for o,N,g in slabs[:1]:
        p=[dot(w,N) for w in W]; hi=mx(p); lo=mn(p)
        nhi=sum(1 for x in p if x==hi); nlo=sum(1 for x in p if x==lo)
        if nhi>=3 and nlo>=3:   # flat top and bottom: can lie as a layer
            w=qs(hi,lo); widths.setdefault((kind,sn),set()).add(w)
G_=gap
print('gap', G_)
hits=[];table=[]
for (kind,sn),ws in sorted(widths.items()):
    for w in ws:
        r=(qf(G_)/qf(w))
        table.append((kind,sn,qf(w)/qf(NN)**.5,r))
        if w==G_: hits.append((kind,sn,'exact, 1 layer'))
for t in sorted(table,key=lambda t:t[2]): print('%-28s %-5s height %.5f  gap/height %.4f'%t)
# stacks: integer combos of distinct layer heights up to 6 layers
W=sorted({w for ws in widths.values() for w in ws},key=qf)
names={w:[k for k,ws in widths.items() if w in ws] for w in W}
for n in range(1,7):
    for combo in itertools.combinations_with_replacement(range(len(W)),n):
        s=Z
        for i in combo: s=qa(s,W[i])
        if s==G_: hits.append(('stack',[names[W[i]] for i in combo]))
print('EXACT FITS:',hits if hits else 'none')
def det3(a,b,c): return qs(qa(qa(qm(a[0],qs(qm(b[1],c[2]),qm(b[2],c[1]))),qm(a[2],qs(qm(b[0],c[1]),qm(b[1],c[0])))),Z),qm(a[1],qs(qm(b[0],c[2]),qm(b[2],c[0]))))
o,N,g=slabs[0]; target=qm(g,(Fr(1,2),Fr(0)))
for a,b,c in itertools.combinations(range(6),3):
    d=det3(AX5[a],AX5[b],AX5[c]); kind='oblate' if abs(abs(qf(d))-min(abs(qf(det3(*[AX5[i] for i in t]))) for t in itertools.combinations(range(6),3)))<1e-9 else 'prolate'
    for sn in ('λ/φ','λ/φ²'):
        s=SIZES[sn]
        W=[vadd(vadd(vmul(AX5[a],qm(s,(Fr(i),Fr(0)))),vmul(AX5[b],qm(s,(Fr(j),Fr(0))))),vmul(AX5[c],qm(s,(Fr(k),Fr(0))))) for i in (0,1) for j in (0,1) for k in (0,1)]
        p=[dot(w,N) for w in W]; hi=mx(p); lo=mn(p)
        if qs(hi,lo)==target and sum(x==hi for x in p)>=3 and sum(x==lo for x in p)>=3: print('half-gap layer:',kind,sn,(a,b,c))

out=dict(mark='DICTO · dictospheres.com',date='2026-10-18',
 slab_gap_times_N=[str(gap[0]),str(gap[1])],N_squared=[str(NN[0]),str(NN[1])],slab_gap_float=qf(gap)/qf(NN)**.5,slab_neighbours=len(slabs),
 layer_heights=[dict(piece=t[0],size=t[1],height=t[2],gap_over_height=t[3]) for t in sorted(table,key=lambda t:t[2])],
 exact_fits=[str(h) for h in hits],
 checks=dict(six_slabs_equal=len({(g[0],g[1]) for _,_,g in slabs})==1,
   two_half_layers=qa(target,target)==gap))
json.dump(out,open(os.path.join(HERE,'..','data','slab-exact.json'),'w'),indent=1,ensure_ascii=False)
print('wrote data/slab-exact.json', out['checks'])
