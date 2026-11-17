# shape kernel shim (stage 1 proper): a + b*phi now comes from the kernel (kernel/field.py, NF over GOLDEN), with the original's float.
from kernel.field import NF as _NF, GOLDEN as _GOLDEN


class Q(_NF):
    """a + b*phi, a, b Fractions (kernel element)"""
    __slots__ = (); FLOAT = 'golden'
    def __init__(s, a, b=0): _NF.__init__(s, [a, b], _GOLDEN)
