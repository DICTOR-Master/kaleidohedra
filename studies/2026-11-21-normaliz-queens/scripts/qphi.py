"""Exact numbers p + q*phi in Q(phi) = Q(sqrt5), phi^2 = phi + 1; parser for Normaliz/e-antic strings (generator a = phi).
Used only to CHECK Normaliz output independently (exact signs, incidences); Normaliz does the hulls."""
from fractions import Fraction as Fr
import re


class QP:
    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p = Fr(p); self.q = Fr(q)

    def __add__(s, o): o = cv(o); return QP(s.p + o.p, s.q + o.q)
    __radd__ = __add__
    def __neg__(s): return QP(-s.p, -s.q)
    def __sub__(s, o): o = cv(o); return QP(s.p - o.p, s.q - o.q)
    def __rsub__(s, o): return cv(o) - s
    def __mul__(s, o):
        o = cv(o)  # (p+qa)(r+sa) = pr + (ps+qr)a + qs(a+1)
        return QP(s.p * o.p + s.q * o.q, s.p * o.q + s.q * o.p + s.q * o.q)
    __rmul__ = __mul__
    def conj(s): return QP(s.p + s.q, -s.q)          # phi -> 1 - phi
    def norm(s): x = s * s.conj(); assert x.q == 0; return x.p
    def inv(s): n = s.norm(); c = s.conj(); return QP(c.p / n, c.q / n)
    def __truediv__(s, o): return s * cv(o).inv()
    def __rtruediv__(s, o): return cv(o) * s.inv()
    def __eq__(s, o): o = cv(o); return s.p == o.p and s.q == o.q
    def __hash__(s): return hash((s.p, s.q))
    def sign(s):
        # s = u + v*sqrt5 with u = p + q/2, v = q/2
        u = s.p + s.q / 2; v = s.q / 2
        su = (u > 0) - (u < 0); sv = (v > 0) - (v < 0)
        if su == sv or sv == 0: return su
        if su == 0: return sv
        d = u * u - 5 * v * v
        return su if d > 0 else (sv if d < 0 else 0)
    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __float__(s): return float(s.p) + float(s.q) * 1.6180339887498949
    def s5(s):
        """as a + b*sqrt5"""
        u = s.p + s.q / 2; v = s.q / 2
        if v == 0: return str(u)
        if u == 0: return f"{v}√5"
        return f"{u} {'+' if v > 0 else '-'} {abs(v)}√5"
    def nz(s):
        """Normaliz/e-antic string in the generator a"""
        if s.q == 0: return str(s.p)
        t = f"{s.q}*a"
        if s.p: t += ("+" if s.p > 0 else "") + str(s.p)
        return t
    __repr__ = s5


def cv(x): return x if isinstance(x, QP) else QP(x)


PHI = QP(0, 1); IPHI = QP(-1, 1); SQRT5 = QP(-1, 2); ONE = QP(1); ZERO = QP(0)

_tok = re.compile(r"([+-]?)\s*([0-9]+(?:/[0-9]+)?)?\s*(\*?\s*a(?:\^([0-9]+))?)?")


def parse(st):
    """parse e-antic output such as '2/5*a-6/5', '-a+1', 'a', '(1/2*a+1)'"""
    st = st.strip().replace(" ", "").strip("()")
    if st in ("0", ""): return QP(0)
    res = QP(0); pos = 0
    while pos < len(st):
        m = _tok.match(st, pos)
        if not m or m.end() == pos: raise ValueError("cannot parse " + st)
        sg, num, apart, pw = m.groups()
        c = Fr(num) if num else Fr(1)
        if sg == "-": c = -c
        if apart:
            k = int(pw) if pw else 1
            term = QP(c)
            for _ in range(k): term = term * PHI
        else:
            term = QP(c)
        res = res + term; pos = m.end()
    return res


def dot(u, v):
    s = QP(0)
    for x, y in zip(u, v): s = s + x * y
    return s


NF = ["a^2-a-1", "a", "1.618+/-0.01"]
