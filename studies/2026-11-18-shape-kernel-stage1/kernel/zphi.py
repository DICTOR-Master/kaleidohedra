"""Z[phi] (and Q(phi)) as plain pairs (x, y) = x + y phi: the function names of zsurf.py (GET study, 2 copies), computed by the kernel.

zsurf.py works on tuples of Python ints in hot loops, so these functions keep that form: ints in, ints out (Fractions in, Fractions
out), no objects.  The sign is the kernel's exact quadratic rule (exact.qsign) on x + y phi = (2x + y + y sqrt5) / 2; the product is
the golden product phi^2 = phi + 1.  tests/test_fields.py checks every function against the general field element NF over GOLDEN."""
from .exact import qsign

__all__ = ['zadd', 'zsub', 'zmul', 'zneg', 'zsign', 'zfloat', 'zconj', 'znorm']


def zadd(u, v): return (u[0] + v[0], u[1] + v[1])
def zsub(u, v): return (u[0] - v[0], u[1] - v[1])
def zmul(u, v): return (u[0] * v[0] + u[1] * v[1], u[0] * v[1] + u[1] * v[0] + u[1] * v[1])
def zneg(u): return (-u[0], -u[1])
def zsign(u):
    """exact sign of x + y*phi = (2x + y + y*sqrt5)/2"""
    x, y = u; return qsign(2 * x + y, y, 5)
def zfloat(u): return u[0] + u[1] * (1 + 5 ** 0.5) / 2
def zconj(u):
    """Galois twin: phi -> 1 - phi = -1/phi, so x + y phi -> (x + y) - y phi"""
    return (u[0] + u[1], -u[1])
def znorm(u):
    """field norm (x + y phi)(x + y phi') = x^2 + x y - y^2"""
    return u[0] * u[0] + u[0] * u[1] - u[1] * u[1]
