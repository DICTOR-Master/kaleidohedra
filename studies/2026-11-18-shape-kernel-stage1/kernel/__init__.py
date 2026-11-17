"""Shape kernel, stage 1: exact numbers.  exact.Quad = a + b sqrt d; field.NF = an element of Q(t) for a real algebraic t with an
isolating interval (cubic and radical fields, the golden basis); field.MQ = Q(sqrt p, sqrt q); pairs = the Q(sqrt5) Fraction-pair
API; zphi = the Z[phi] integer-pair API; vec = exact vectors."""
from .exact import *          # noqa
from .field import NumberField, NF, MQ, GOLDEN, pure_field, sturm_count, poly_gcd, NF_STYLES, NF_FLOATS, MQ_STYLES   # noqa
from . import exact, pairs, vec, field, zphi
