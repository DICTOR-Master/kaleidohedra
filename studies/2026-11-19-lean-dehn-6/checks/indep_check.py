# Exact check of the hand argument for the independence of alpha and beta modulo pi.
# Numbers a + b*sqrt5 are pairs of Fractions; complex numbers x + y*i are pairs of such pairs.
# No floating point except the last sanity block.
from fractions import Fraction as F
import math

def q(a, b=0): return (F(a), F(b))
def qadd(x, y): return (x[0] + y[0], x[1] + y[1])
def qsub(x, y): return (x[0] - y[0], x[1] - y[1])
def qmul(x, y): return (x[0]*y[0] + 5*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def qinv(x):
    n = x[0]*x[0] - 5*x[1]*x[1]
    return (x[0]/n, -x[1]/n)
def cmul(u, v): return (qsub(qmul(u[0], v[0]), qmul(u[1], v[1])), qadd(qmul(u[0], v[1]), qmul(u[1], v[0])))
def cconj(u): return (u[0], qsub(q(0), u[1]))
ONE = (q(1), q(0))

# 1. cos^2 beta, with cos beta = (3 - sqrt5)/r, sin beta = 4/r, r^2 = 3(10 - 2 sqrt5)
r2 = q(30, -6)
cos2 = qmul(qmul(q(3, -1), q(3, -1)), qinv(r2))
assert cos2 == (F(1, 3), F(-2, 15))
print("cos^2 beta = 1/3 - 2 sqrt5/15: ok")
cos2b = qsub(qmul(q(2), cos2), q(1))                # cos 2 beta
sin2b = qmul(qmul(q(8), q(3, -1)), qinv(r2))        # 2 sin beta cos beta
assert cos2b == (F(-5, 15), F(-4, 15)) and sin2b == (F(10, 15), F(-2, 15))
print("e^{2i beta} = (-(5 + 4 sqrt5) + (10 - 2 sqrt5) i)/15: ok")
z = (cos2b, sin2b)
assert cmul(z, cconj(z)) == ONE
print("|e^{2i beta}| = 1, so its field norm to Q is 1: norms of e^{2i beta} itself do not separate")
w = (q(F(-3, 5)), q(F(4, 5)))
assert cmul(w, cconj(w)) == ONE
print("e^{2i alpha} = (-3 + 4i)/5, modulus 1: ok")

# 2. c_n = 15^n (z^n + conj z^n) = 2 * 15^n cos(2 n beta): the integer recurrence used in Lean
def cB(N):
    out = [(2, 0), (-10, -8)]
    while len(out) <= N:
        (a, b), (a0, b0) = out[-1], out[-2]
        out.append((-10*a - 40*b - 225*a0, -8*a - 10*b - 225*b0))
    return out
def dA(N):
    out = [2, -6]
    while len(out) <= N:
        out.append(-6*out[-1] - 25*out[-2])
    return out
N = 60
cb, da = cB(N), dA(N)
zn, wn = ONE, ONE
for n in range(N + 1):
    tr = qadd(zn[0], zn[0])                          # z^n + conj z^n = 2 Re z^n
    assert (tr[0] * 15**n, tr[1] * 15**n) == (F(cb[n][0]), F(cb[n][1])), n
    tw = qadd(wn[0], wn[0])
    assert tw[1] == 0 and tw[0] * 5**n == da[n], n
    zn, wn = cmul(zn, z), cmul(wn, w)
print("2*15^n cos(2 n beta) = a_n + b_n sqrt5 and 2*5^n cos(2 n alpha) = d_n (integers), n = 0..%d: ok" % N)

# 3. the invariant: a_n^2 - 5 b_n^2 is not divisible by 3 for n >= 1
M = 2000
cb = cB(M)
res = set()
for n in range(1, M + 1):
    a, b = cb[n]
    nn = a*a - 5*b*b
    assert nn % 3 != 0, n
    res.add(nn % 3)
    if n >= 2:
        a1, b1 = cb[n-1]
        assert (nn + 220*(a1*a1 - 5*b1*b1)) % 225 == 0
print("3 does not divide a_n^2 - 5 b_n^2 for n = 1..%d (residues seen: %s); step N_(n+1) = -220 N_n mod 225: ok" % (M, sorted(res)))
print("a_1^2 - 5 b_1^2 =", cb[1][0]**2 - 5*cb[1][1]**2)

# 4. the consequence: 5^k (a_j + b_j sqrt5) = 15^j d_k has no solution with j >= 1 (small range, exact)
da = dA(60)
for j in range(1, 61):
    for k in range(0, 61):
        a, b = cb[j]
        assert not (5**k * b == 0 and 5**k * a == 15**j * da[k])
print("no j in 1..60, k in 0..60 with cos(2 j beta) = cos(2 k alpha): ok")

# 5. floating sanity only
al = math.acos(1/math.sqrt(5)); be = math.acos((3 - math.sqrt(5))/math.sqrt(3*(10 - 2*math.sqrt(5))))
for n in range(0, 6):
    a, b = cb[n]
    assert abs(2*15**n*math.cos(2*n*be) - (a + b*math.sqrt(5))) < 1e-6 * 15**n
    assert abs(2*5**n*math.cos(2*n*al) - da[n]) < 1e-6 * 5**n
print("floating sanity n = 0..5: ok; alpha = %.6f deg, beta = %.6f deg" % (math.degrees(al), math.degrees(be)))
