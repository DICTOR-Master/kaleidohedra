# --- shape kernel shim (stage 1 proper): K = Q(sqrt5) now comes from the kernel (kernel/exact.py, Quad), with the original's printed form and hash.
from kernel.exact import Quad as _Quad


class K(_Quad):
    __slots__ = (); D = 5; STYLE = '(a+br5)always'; HASH_PAIR = True
    sym = _Quad.sympy
