from fractions import Fraction as Fr
import math, itertools
S5 = math.sqrt(5)
class Q:
    __slots__=('a','b')
    def __init__(s,a=0,b=0): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o): o=Qc(o); return Q(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return Q(-s.a,-s.b)
    def __sub__(s,o): return s+(-Qc(o))
    def __rsub__(s,o): return Qc(o)-s
    def __mul__(s,o): o=Qc(o); return Q(s.a*o.a+5*s.b*o.b, s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s):
        d=s.a*s.a-5*s.b*s.b; return Q(s.a/d,-s.b/d)
    def __truediv__(s,o): return s*Qc(o).inv()
    def __eq__(s,o): o=Qc(o); return s.a==o.a and s.b==o.b
    def __hash__(s): return hash((s.a,s.b))
    def f(s): return float(s.a)+float(s.b)*S5
    def sign(s):
        # exact sign of a+b sqrt5
        a,b=s.a,s.b
        if b==0: return (a>0)-(a<0)
        if a==0: return (b>0)-(b<0)
        if a>0 and b>0: return 1
        if a<0 and b<0: return -1
        c=(a*a>5*b*b)
        if a>0: return 1 if c else -1
        return -1 if c else 1
    def __repr__(s):
        if s.b==0: return str(s.a)
        if s.a==0: return f"{s.b}r5"
        return f"({s.a}{'+' if s.b>0 else ''}{s.b}r5)"
    def lean(s):
        def fr(x):
            return f"{x.numerator}" if x.denominator==1 else f"({x.numerator} / {x.denominator})"
        def frp(x): # positive
            return fr(x)
        a,b=s.a,s.b
        if b==0:
            return fr(a) if a>=0 else f"(-{fr(-a)})" if a.denominator==1 else f"(-{fr(-a)})"
        bt = "√5" if abs(b)==1 else f"{fr(abs(b))} * √5"
        if a==0:
            return bt if b>0 else f"(-({bt}))" if abs(b)!=1 else "(-√5)"
        at = fr(a) if a>0 else f"-{fr(-a)}"
        return f"({at} {'+' if b>0 else '-'} {bt})"
def Qc(o): return o if isinstance(o,Q) else Q(o)
def snap(x):
    best=None
    for b4 in range(-8,9):
        b=Fr(b4,4); a=x-float(b)*S5; a4=round(a*4)
        if abs(a-a4/4)<1e-7:
            c=(abs(a4)+abs(b4),Q(Fr(a4,4),b))
            if best is None or c[0]<best[0]: best=c
    assert best, x
    return best[1]
def dot(u,v): return u[0]*v[0]+u[1]*v[1]+u[2]*v[2]
def sub(u,v): return [u[i]-v[i] for i in range(3)]
def cross(u,v): return [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
def det(a,b,c): return dot(a,cross(b,c))
def solve3(rows,rhs):
    # rows: 3 vectors as rows; solve M x = rhs
    D=det(*rows)
    if D==0: return None
    cols=[[rows[r][c] for r in range(3)] for c in range(3)]
    out=[]
    for k in range(3):
        cc=[cols[c] if c!=k else rhs for c in range(3)]
        out.append(det(*cc)/D)   # det of transpose same
    return out
