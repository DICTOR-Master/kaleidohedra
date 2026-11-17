# shape kernel shim (stage 1 proper): the number classes QF, KC, AlgField and RF now come from the kernel (kernel/exact.py Quad,
# kernel/field.py NF and NumberField), with the dataset's printed forms, hashes, floats and decimals; the rest of exactlib.py is unchanged.
from kernel.exact import Quad as _Quad
from kernel.field import NF as _NF, NumberField as AlgField, pure_field as _pure


class QF(_Quad):
    """a + b*sqrt(d), a, b rational (kernel element)"""
    __slots__ = (); D = 5; STYLE = 'parsable'; HASH_PAIR = True


class KC(_NF):
    """a + b*r + c*r^2 with r = k^(1/3) (kernel element; sign exact by interval refinement, equal to the sign of the norm)"""
    __slots__ = (); STYLE = 'kc'; FLOAT = 'kc'; DEC = 'kc'; MP = 'kc'
    def __init__(s, a=0, b=0, c=0, k=2): _NF.__init__(s, [a, b, c], _pure(k, 3))
    @property
    def d(s): return ('cbrt', s.F.pure[0])


class RF(_NF):
    """an element of an AlgField (kernel element)"""
    __slots__ = (); STYLE = 'rf'
