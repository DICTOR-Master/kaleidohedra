# shape kernel counterpart of the golden-basis Q5 of echo_lib.py and qlib.py (used by the differential test): a + b phi over GOLDEN.
from kernel.field import NF as _NF, GOLDEN as _GOLDEN


class Q5(_NF):
    __slots__ = (); FLOAT = 'golden'; STYLE = '(a+-bphi)'
    def __init__(s, a=0, b=0): _NF.__init__(s, [a, b], _GOLDEN)
