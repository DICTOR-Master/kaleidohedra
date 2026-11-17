# --- shape kernel shim (stage 1 proper): the field K = Q(sqrt2, sqrt5) and its printed form kstr now come from the kernel
# (kernel/field.py, MQ); _s2sign is no longer needed (the kernel decides signs exactly by interval refinement).
from kernel.field import MQ as _MQ, MQ_STYLES as _MQS


class K(_MQ):
    """a + b sqrt2 + c sqrt5 + d sqrt10 (kernel element; cubes_lib's printed form and hash)"""
    __slots__ = (); RADS = (2, 5); STYLE = 'roots'


def kstr(x): return _MQS['roots'](x)
