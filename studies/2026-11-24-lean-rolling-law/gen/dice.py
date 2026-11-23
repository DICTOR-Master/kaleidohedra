#!/usr/bin/env python3
"""Exact geometry of the three fair dice (A3, B3, H3) -> Lean data.

Numbers are in Q(sqrt5), stored as pairs (a, b) = a + b*sqrt5 with integer a, b
after scaling.  For each group G (exact 3x3 matrices) and a generic point u:
  * face normals n_x = g_x u (one face per group element; the permutahedron's vertices),
  * die vertices V: the orbits of three axis vectors (one orbit per vertex type),
  * heights c_k = max_x n_x . V for V of type k (same for the whole orbit),
so the die = { y : n_x . y <= 1 for all x } has vertices V / c_k.
Vertex type k is the corner where edges of the other two types meet, with
valence 2*m(i,j) (Mathlib's matrices).  The roll r_i x = the face sharing with x
the two vertices of types other than i.  Faces are numbered breadth-first from
the face of u.  Data only: every property is re-checked by the Lean kernel."""
from fractions import Fraction as F
import sys, os, itertools
class Q:
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=F(a); s.b=F(b)
    def __add__(s,o): return Q(s.a+o.a,s.b+o.b)
    def __sub__(s,o): return Q(s.a-o.a,s.b-o.b)
    def __mul__(s,o): return Q(s.a*o.a+5*s.b*o.b, s.a*o.b+s.b*o.a)
    def __neg__(s): return Q(-s.a,-s.b)
    def key(s): return (s.a,s.b)
    def __eq__(s,o): return s.key()==o.key()
    def __hash__(s): return hash(s.key())
    def f(s): return float(s.a)+float(s.b)*5**.5
    def ge0(s):
        a,b=s.a,s.b
        if a>=0 and b>=0: return True
        if a<=0 and b<=0: return a==0 and b==0
        return a*a>=5*b*b if a>0 else 5*b*b>=a*a
def le(x,y): return (y-x).ge0()
H=F(1,2); PHI=Q(H,H); IPHI=Q(-H,H)   # phi, 1/phi
Z,O=Q(0),Q(1)
def mm(A,B): return tuple(tuple(sum((A[r][k]*B[k][c] for k in range(3)),Q(0)) for c in range(3)) for r in range(3))
def mv(A,v): return tuple(sum((A[r][k]*v[k] for k in range(3)),Q(0)) for r in range(3))
def dot(u,v): return sum((u[k]*v[k] for k in range(3)),Q(0))
def mkey(A): return tuple(x.key() for r in A for x in r)
def closure(gens):
    I=tuple(tuple(O if r==c else Z for c in range(3)) for r in range(3))
    els={mkey(I):I}; fr=[I]
    while fr:
        nf=[]
        for A in fr:
            for g in gens:
                B=mm(A,g); k=mkey(B)
                if k not in els: els[k]=B; nf.append(B)
        fr=nf
    return list(els.values())
def perm(p,s=(1,1,1)): return tuple(tuple(Q(s[r]) if c==p[r] else Z for c in range(3)) for r in range(3))
cyc=perm((1,2,0)); swp=perm((1,0,2)); neg=lambda s: perm((0,1,2),s)
half=lambda x: x*Q(H)
M5=((Q(H),-(PHI*Q(H)),IPHI*Q(H)),(PHI*Q(H),IPHI*Q(H),-Q(H)),(IPHI*Q(H),Q(H),PHI*Q(H)))
def V(*xs): return tuple(x if isinstance(x,Q) else Q(x) for x in xs)
GROUPS={
 # name: (generators, u, axis vector per vertex type 0,1,2, m01, m12, m02)
 'A3': ([cyc,swp,neg((-1,-1,1))], V(5,2,1), [V(1,1,1),V(1,0,0),V(-1,-1,-1)], (3,3,2)),
 'B3': ([cyc,swp,neg((-1,1,1))], V(5,2,1), [V(1,0,0),V(1,1,0),V(1,1,1)], (3,4,2)),
 'H3': ([cyc,neg((-1,1,1)),M5], V(7,2,1), [V(0,PHI,1),V(0,0,1),V(1,1,1)], (3,5,2)),
}
def lcd_scale(vecs):
    import math
    den=1
    for v in vecs:
        for x in v: den=math.lcm(den,x.a.denominator,x.b.denominator)
    return [tuple(Q(x.a*den,x.b*den) for x in v) for v in vecs]
def lean_q(x): 
    assert x.a.denominator==1 and x.b.denominator==1
    return f"⟨{x.a},{x.b}⟩"
out=sys.argv[1]
for name,(gens,u,axes,(m01,m12,m02)) in GROUPS.items():
    G=closure(gens); N=len(G)
    normals=lcd_scale([mv(g,u) for g in G])
    assert len(set(tuple(x.key() for x in n) for n in normals))==N
    verts=[];types=[]
    for k,a in enumerate(axes):
        orb={}
        for g in G:
            w=mv(g,a); orb[tuple(x.key() for x in w)]=w
        orb=lcd_scale(list(orb.values()))
        verts+=orb; types+=[k]*len(orb)
    c=[]
    for k in range(3):
        best=None
        for v,t in zip(verts,types):
            if t!=k: continue
            mx=None
            for n in normals:
                dd=dot(n,v)
                if mx is None or le(mx,dd): mx=dd
            if best is None: best=mx
            assert mx==best
        c.append(best)
    fv=[]
    for n in normals:
        on=[i for i,(v,t) in enumerate(zip(verts,types)) if dot(n,v)==c[t]]
        assert sorted(types[i] for i in on)==[0,1,2], (name,on)
        fv.append(tuple(sorted(on,key=lambda i:types[i])))
    # rolls
    idx={}
    for x,f in enumerate(fv):
        for i in range(3): idx.setdefault((i,tuple(f[k] for k in range(3) if k!=i)),[]).append(x)
    r=[[None]*N for _ in range(3)]
    for (i,_),xs in idx.items():
        assert len(xs)==2; a,b=xs; r[i][a]=b; r[i][b]=a
    # base face = face of u (identity matrix is G[0])
    order=[0]; seen={0:0}; d={0:0}; q=0; word={0:[]}
    while q<len(order):
        x=order[q]; q+=1
        for i in range(3):
            y=r[i][x]
            if y not in seen: seen[y]=len(order); order.append(y); d[y]=d[x]+1; word[y]=word[x]+[i]
    assert len(order)==N
    p=seen
    rt=[[p[r[i][x]] for x in order] for i in range(3)]
    dt=[d[x] for x in order]
    nt=[normals[x] for x in order]
    ft=[fv[x] for x in order]
    wt=[word[x] for x in order]
    # 4 g_x: exact symmetry matrices (scaled by 4 so that entries lie in Z[sqrt5])
    gm=[tuple(tuple(e*Q(4) for e in row) for row in G[x]) for x in order]
    for g in gm:
        for row in g:
            for e in row: assert e.a.denominator==1 and e.b.denominator==1
    nkey={tuple(x.key() for x in n):z for z,n in enumerate(nt)}
    perm=[[nkey[tuple((e*Q(F(1,4))).key() for e in mv(g,n))] for n in nt] for g in gm]
    gkey={tuple(e.key() for row in g for e in row):x for x,g in enumerate(gm)}
    inv=[gkey[tuple(g[c][r].key() for r in range(3) for c in range(3))] for g in gm]
    val=[sum(1 for f in fv if v in f) for v in range(len(verts))]
    exp={0:2*m12,1:2*m02,2:2*m01}
    assert all(val[v]==exp[types[v]] for v in range(len(verts))), (name, set(zip(types,val)))
    L=lambda xs: '['+', '.join(xs)+']'
    with open(os.path.join(out,name+'.lean'),'w') as f:
        f.write(f"""/-
Exact data of the {name} die ({N} faces, {len(verts)} vertices), generated by gen/dice.py.
Numbers `⟨a, b⟩` stand for a + b√5. Faces are numbered breadth-first from face 0.
Data only: every property is checked by the Lean kernel in RollingLaw/Dice.lean
and RollingLaw/Die.lean.
-/
import RollingLaw.Q5

namespace RollingLaw.Data.{name}

set_option maxRecDepth 100000

/-- number of faces -/
def N : Nat := {N}

/-- `rt[i][x]`: the face reached from face `x` by rolling across its edge of type `i`. -/
def rt : List (List Nat) :=
  [{(','+chr(10)+'   ').join(str(row).replace(' ','') for row in rt)}]

/-- `dt[x]`: the number of rolls on a shortest roll from face 0 to face `x`. -/
def dt : List Nat :=
  {str(dt).replace(' ','')}

/-- number of vertices of the die -/
def NV : Nat := {len(verts)}

/-- vertex types (the corner where edges of the other two types meet) -/
def vtype : List Nat :=
  {str(types).replace(' ','')}

/-- vertex directions `V` (the die vertex is `V / c[type]`) -/
def vert : List (List Q5) :=
  {L(L(lean_q(x) for x in v) for v in verts)}

/-- heights `c[k]` -/
def height : List Q5 := {L(lean_q(x) for x in c)}

/-- face normals `n[x]` (the die is `n[x] · y ≤ 1`; these are the permutahedron's vertices) -/
def normal : List (List Q5) :=
  {L(L(lean_q(x) for x in v) for v in nt)}

/-- `fv[x][k]`: the vertex of type `k` of face `x` -/
def fv : List (List Nat) :=
  {str([list(t) for t in ft]).replace(' ','')}

/-- `word[x]`: a shortest roll (edge types) from face 0 to face `x` -/
def word : List (List Nat) :=
  {str(wt).replace(' ','')}

/-- `gm[x]`: 4 × the symmetry matrix (rows) taking face 0 to face `x` -/
def gm : List (List (List Q5)) :=
  {L(L(L(lean_q(e) for e in row) for row in g) for g in gm)}

/-- `inv[x]`: the face whose symmetry is the inverse (= transpose) of that of face `x` -/
def inv : List Nat :=
  {str(inv).replace(' ','')}

/-- `perm[x][z]`: the symmetry of face `x` takes the normal of face `z` to that of face `perm[x][z]` -/
def perm : List (List Nat) :=
  {str(perm).replace(' ','')}

end RollingLaw.Data.{name}
""")
    print(name,N,len(verts),max(dt),[lean_q(x) for x in c])
