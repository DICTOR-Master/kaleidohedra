# --- shape kernel shim (stage 1 proper): K = Q(k^(1/n)) in the basis 1, r, ..., r^(n-1) now comes from the kernel (kernel/field.py, NF
# over pure_field(k, n)); n and k stay class settings as in the original, and the sign is exact (the original read it from floats).
from kernel.field import NF as _NF, pure_field as _pure


class K(_NF):
    __slots__ = (); n = 2; k = 2; STYLE = 'r^i'; FLOAT = 'r^i'
    def __init__(s, c): _NF.__init__(s, c, _pure(K.k, K.n))
    @staticmethod
    def of(x): return x if isinstance(x, K) else K(x)
