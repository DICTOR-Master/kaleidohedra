"""Common scale for a solid in both golden rhombohedra: S0 = max(s0 prolate, s0 oblate), s0 = smallest s with the solid inside the mould
(exact).  All 20 orientations checked to give the same two values.  Prints 'solid a b' with S0 = a + b sqrt5 (for AMBER_S) and both s0."""
import sys, itertools
from ammann_cell import shell, dot, Q, IH, act
from aligned import aligned
from tiling import TRIPLES, tvol, absq
vP = max((absq(tvol(A)) for A in TRIPLES), key=float)
for solid in sys.argv[1:]:
    C = aligned(solid, IH, act); V = C["V"]; s0 = {}
    for A in TRIPLES:
        k = "P" if (absq(tvol(A)) - vP).sign() == 0 else "O"
        m = None
        for n, c in shell("".join(map(str, A)), Q(1)):
            for v in V:
                r = dot(n, v)/c
                if m is None or (r - m).sign() > 0: m = r
        s0.setdefault(k, set()).add(m.key())
    assert all(len(x) == 1 for x in s0.values()), "same s0 in all orientations of a type"
    sP, sO = Q(*next(iter(s0["P"]))), Q(*next(iter(s0["O"])))
    S = sP if (sP - sO).sign() >= 0 else sO
    print(solid, S.a, S.b, f"s0P={sP}={float(sP):.6f} s0O={sO}={float(sO):.6f} S0={'P' if S is sP else 'O'} orientation={C['aligned']}")
