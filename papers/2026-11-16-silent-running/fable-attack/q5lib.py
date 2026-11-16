"""Exact Q(sqrt5) arithmetic, icosians, Gegenbauer. Pure Python. Independent referee code."""
from fractions import Fraction as Fr
import itertools
class Q5:
    __slots__=('a','b')
    def __init__(s,a=0,b=0): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o):
        if not isinstance(o,Q5): o=Q5(o)
        return Q5(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return Q5(-s.a,-s.b)
    def __sub__(s,o):
        if not isinstance(o,Q5): o=Q5(o)
        return Q5(s.a-o.a,s.b-o.b)
    def __rsub__(s,o): return (-s)+o
    def __mul__(s,o):
        if not isinstance(o,Q5): return Q5(s.a*o,s.b*o)
        return Q5(s.a*o.a+5*s.b*o.b,s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s):
        n=s.a*s.a-5*s.b*s.b
        return Q5(s.a/n,-s.b/n)
    def __truediv__(s,o):
        if not isinstance(o,Q5): return Q5(s.a/o,s.b/o)
        return s*o.inv()
    def bar(s): return Q5(s.a,-s.b)
    def __eq__(s,o):
        if not isinstance(o,Q5): o=Q5(o)
        return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def iszero(s): return s.a==0 and s.b==0
    def __float__(s): return float(s.a)+float(s.b)*5**0.5
    def __repr__(s):
        if s.b==0: return str(s.a)
        return f"({s.a}{'+' if s.b>0 else '-'}{abs(s.b)}r5)"
    def key(s): return (s.a,s.b)
PHI=Q5(Fr(1,2),Fr(1,2)); ONE=Q5(1); ZERO=Q5(0)
def qmul(p,q):
    a,b,c,d=p; e,f,g,h=q
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g, a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)
def qconj(p): return (p[0],-p[1],-p[2],-p[3])
def qkey(p): return tuple(x.key() for x in p)
def even_perms(t):
    out=[]
    for p in itertools.permutations(range(4)):
        inv=sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j])
        if inv%2==0: out.append(tuple(t[p[i]] for i in range(4)))
    return out
def icosians():
    h=Fr(1,2); S=set(); L=[]
    def add(q):
        k=qkey(q)
        if k not in S: S.add(k); L.append(q)
    for i in range(4):
        for s in (1,-1):
            v=[ZERO]*4; v[i]=Q5(s); add(tuple(v))
    for sg in itertools.product((1,-1),repeat=4): add(tuple(Q5(h*s) for s in sg))
    base=(ZERO,Q5(h),PHI.inv()*h,PHI*h)
    for sg in itertools.product((1,-1),repeat=4):
        v=tuple(base[i]*sg[i] for i in range(4))
        for p in even_perms(v): add(p)
    return L
def gegen_norm(kmax,lam,t):
    """Q_k(t)=C_k^lam(t)/C_k^lam(1), k=0..kmax. lam Fraction."""
    Q=[ONE if isinstance(t,Q5) else Fr(1), t]
    for k in range(1,kmax):
        Q.append((2*(k+lam)*(t*Q[k]) - k*Q[k-1])/(k+2*lam))
    return Q
def cheb_U(kmax,t):
    U=[ONE,2*t]
    for k in range(1,kmax): U.append(2*t*U[k]-U[k-1])
    return U
