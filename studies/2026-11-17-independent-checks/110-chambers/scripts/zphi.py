"""Exact vectorised arithmetic in Z[phi], phi^2 = phi + 1.  An element a + b*phi is an
int64 pair [..., 2].  Written from scratch for the #110 chamber check."""
import numpy as np

LIM = 2 ** 62

def _chk(*xs):
    for x in xs:
        if x.size and np.abs(x).max() >= 1_500_000_000:
            raise OverflowError('Z[phi] operand too large for safe int64 products')

def mul(x, y):
    _chk(x, y)
    a, b = x[..., 0], x[..., 1]; c, d = y[..., 0], y[..., 1]
    return np.stack([a * c + b * d, a * d + b * c + b * d], -1)

def dot(u, v):          # u, v: [..., 4, 2]
    return mul(u, v).sum(-2)

def neg(x): return -x

def times_phi(x):       # phi*(a + b phi) = b + (a + b) phi
    return np.stack([x[..., 1], x[..., 0] + x[..., 1]], -1)

def sign(x):
    """exact sign of a + b phi = ((2a + b) + b sqrt5)/2"""
    _chk(x)
    p = 2 * x[..., 0] + x[..., 1]; q = x[..., 1]
    assert p.size == 0 or np.abs(p).max() < 2_000_000_000
    sp, sq = np.sign(p), np.sign(q)
    big = np.sign(p * p - 5 * q * q)          # p^2 = 5 q^2 only if p = q = 0
    out = np.where(sp == sq, sp, np.where(sp == 0, sq, np.where(sq == 0, sp, np.where(big > 0, sp, sq))))
    return out.astype(int)

def det3(r0, r1, r2):   # rows [...,3,2] each length-3 Z[phi] vectors
    def m(x, y): return mul(x, y)
    return (m(r0[..., 0, :], m(r1[..., 1, :], r2[..., 2, :]) - m(r1[..., 2, :], r2[..., 1, :]))
            - m(r0[..., 1, :], m(r1[..., 0, :], r2[..., 2, :]) - m(r1[..., 2, :], r2[..., 0, :]))
            + m(r0[..., 2, :], m(r1[..., 0, :], r2[..., 1, :]) - m(r1[..., 1, :], r2[..., 0, :])))

def cross3(u, v, w):
    """generalised cross product in 4D: vector orthogonal to u, v, w (exact)."""
    comps = []
    for i in range(4):
        cols = [j for j in range(4) if j != i]
        d = det3(u[..., cols, :], v[..., cols, :], w[..., cols, :])
        comps.append(d if i % 2 == 0 else -d)
    return np.stack(comps, -2)

def reduce(v):
    """divide a Z[phi]^4 vector (or batch) by the gcd of its 8 integers."""
    flat = v.reshape(v.shape[:-2] + (8,))
    g = np.gcd.reduce(np.abs(flat), axis=-1)
    g = np.where(g == 0, 1, g)
    return v // g[..., None, None]

def canon(v):
    """exact projective canonical key of nonzero vectors v [..., 4, 2]: divide by the first
    nonzero coordinate x_k (in Q(phi)), express as (p_i + q_i phi)/N with N = norm(x_k) > 0,
    reduced by gcd.  Returns int64 array [..., 9] (p0,q0,..,p3,q3,N); +-v give the same key."""
    v = reduce(v)
    nz = np.any(v != 0, axis=-1)                       # [...,4]
    if not np.all(nz.any(-1)):
        raise ValueError('zero vector in canon')
    k = np.argmax(nz, axis=-1)
    xk = np.take_along_axis(v, k[..., None, None].repeat(2, -1), axis=-2)[..., 0, :]
    c, d = xk[..., 0], xk[..., 1]
    N = c * c + c * d - d * d                          # norm, nonzero
    conj = np.stack([c + d, -d], -1)                   # (c + d phi)(c + d - d phi) = N
    num = mul(v, conj[..., None, :])                   # [...,4,2]
    out = np.concatenate([num.reshape(num.shape[:-2] + (8,)), N[..., None]], -1)
    s = np.sign(out[..., 8]); out = out * s[..., None]
    g = np.gcd.reduce(np.abs(out), axis=-1); g = np.where(g == 0, 1, g)
    return out // g[..., None]

def tofloat(x):
    PHI = (1 + 5 ** 0.5) / 2
    return x[..., 0] + PHI * x[..., 1]
