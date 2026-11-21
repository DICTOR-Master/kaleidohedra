"""Solids of the amber-cell sweep with their 5-fold axes on the six vectors of tiling.py.  The sweep only fixes the T_h axes; a solid
whose vertex set is not invariant under this I_h (built in ammann_cell.py) is reflected in the plane y = z (swap y, z; face cycles
reversed to keep their orientation); the result is checked to be I_h-invariant (exact)."""
from solids import build as _build
def key(v): return tuple(x.key() for x in v)
def aligned(name, IH, act):
    C = _build(name)
    def inv(C): ks = {key(v) for v in C["V"]}; return all(key(act(g, v)) in ks for g in IH for v in C["V"])
    if inv(C): C["aligned"] = "as built"; return C
    sw = lambda v: [v[0], v[2], v[1]]
    D = dict(V=[sw(v) for v in C["V"]], faces=[(list(reversed(f)), k) for f, k in C["faces"]], planes=[(sw(n), c) for n, c in C["planes"]], name=name)
    assert inv(D), f"{name}: not I_h-invariant in either orientation"
    D["aligned"] = "reflected y<->z"; return D
