"""Depth-box certification for the amber cells (24 Nov 2026).

Every number the amber construction computes is a rational function of the die's depths D_1..D_m (one per face orbit; the directions are
fixed exact vectors in Q(phi)^3).  HQ carries two things through the unchanged amber code:
  q = the exact value (in Q(sqrt5)) at the box centre c (rational depths, |c - fair| tiny), and
  z = an arb ball enclosing the value for EVERY depth vector in the box B = prod [c_k - r, c_k + r].
Each sign test made by the code is logged.  A nonzero sign at the centre is accepted only if the ball excludes 0: then that sign is the
same over all of B (certified).  A zero at the centre is recorded as a zero test.
A second run of the same code in exact arithmetic at a random rational depth vector p in B (64-bit random offsets) must make the same
sequence of sign tests with the same results; so every zero test of the centre run also vanishes at p.  Each zero test is a
rational function of the depths that is either identically zero on B or vanishes at p only with probability <= deg/2^64
(Schwartz-Zippel); this part is a randomised identity test, not a deterministic proof, and is stated so.
If both hold, the code takes the same path for every depth vector in B, so the combinatorics it outputs (pieces, side counts, kinds,
Y vertices, convexity) is constant on B."""
import hashlib
from fractions import Fraction as Fr
import flint
from flint import arb, fmpq
import resin
flint.ctx.prec = 600
S5 = arb(5).sqrt()
_ORIG_SIGN = resin.Q.sign
LOG = bytearray(); STATS = {"tests": 0, "zero": 0, "certified": 0, "uncertified": 0}
def _ball(a, b): return arb(fmpq(a.numerator, a.denominator)) + arb(fmpq(b.numerator, b.denominator))*S5

def logged_sign(s):
    v = _ORIG_SIGN(s); LOG.append(v + 1); STATS["tests"] += 1
    if v == 0: STATS["zero"] += 1
    return v

class HQ(resin.Q):
    __slots__ = ("z",)
    def __init__(s, a=0, b=0, z=None):
        resin.Q.__init__(s, a, b); s.z = z if z is not None else _ball(s.a, s.b)
    @staticmethod
    def lift(o):
        if isinstance(o, HQ): return o
        if isinstance(o, resin.Q): return HQ(o.a, o.b)
        return HQ(o)
    def __add__(s, o): o = HQ.lift(o); return HQ(s.a + o.a, s.b + o.b, s.z + o.z)
    __radd__ = __add__
    def __neg__(s): return HQ(-s.a, -s.b, -s.z)
    def __sub__(s, o): o = HQ.lift(o); return HQ(s.a - o.a, s.b - o.b, s.z - o.z)
    def __rsub__(s, o): return HQ.lift(o) - s
    def __mul__(s, o): o = HQ.lift(o); return HQ(s.a*o.a + 5*s.b*o.b, s.a*o.b + s.b*o.a, s.z*o.z)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = HQ.lift(o); n = o.a*o.a - 5*o.b*o.b
        return HQ((s.a*o.a - 5*s.b*o.b)/n, (s.b*o.a - s.a*o.b)/n, s.z/o.z)
    def __rtruediv__(s, o): return HQ.lift(o) / s
    def sign(s):
        v = _ORIG_SIGN(s); LOG.append(v + 1); STATS["tests"] += 1
        if v == 0: STATS["zero"] += 1
        elif (v > 0 and s.z > 0) or (v < 0 and s.z < 0): STATS["certified"] += 1
        else: STATS["uncertified"] += 1
        return v

def install_logging(): resin.Q.sign = logged_sign
def digest(): return hashlib.sha256(bytes(LOG)).hexdigest()
def report(pr):
    const = STATS['tests'] - STATS['zero'] - STATS['certified'] - STATS['uncertified']
    pr(f"SIGNS: tests {STATS['tests']}, zero at the point {STATS['zero']}, nonzero certified over the box {STATS['certified']}, nonzero depth-free (constants) {const}, "
       f"nonzero NOT certified {STATS['uncertified']}; sequence sha256 {digest()}")
