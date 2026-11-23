"""The three permutahedra as amber-cell cores (24 Nov 2026), exact in Q(sqrt5), T_h axes on the cube axes, built with the hull of the
amber-cell sweep (solids.py: every face plane checked exactly).
- truncated_octahedron: all permutations of (0, +-1, +-2) (uniform, edge sqrt2; the A3 permutahedron).
- B3_permutahedron_123: all permutations of (+-1, +-2, +-3): the B3 permutahedron through a rational point (the uniform truncated
  cuboctahedron needs sqrt2, outside the code's field Q(sqrt5); same faces and symmetry, rectangles and non-regular hexagons/octagons).
- truncated_icosidodecahedron: the uniform one, edge 2/phi: even permutations of (+-1/phi, +-1/phi, +-(3+phi)), (+-2/phi, +-phi, +-(1+2phi)),
  (+-1/phi, +-phi^2, +-(-1+3phi)), (+-(2phi-1), +-2, +-(2+phi)), (+-phi, +-3, +-2phi)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../2026-11-21-amber-cell-sweep/scripts"))
from solids import orbit, hull, KIND, Q, PHI, dot, vsub
K = dict(KIND); K[8] = "oct"
COUNTS = {"truncated_octahedron": (24, 14), "B3_permutahedron_123": (48, 26), "truncated_icosidodecahedron": (120, 62)}
def build(name):
    if name == "truncated_octahedron":
        P = orbit([(0, 1, 2), (0, 2, 1)])
    elif name == "B3_permutahedron_123":
        P = orbit([(1, 2, 3), (1, 3, 2)])
    elif name == "truncated_icosidodecahedron":
        ip = PHI - 1
        P = orbit([(ip, ip, 3 + PHI), (2 * ip, PHI, 1 + 2 * PHI), (ip, PHI + 1, 3 * PHI - 1), (2 * PHI - 1, Q(2), 2 + PHI), (PHI, Q(3), 2 * PHI)])
    else:
        raise SystemExit("unknown solid " + name)
    S = hull(P, K); S["name"] = name
    assert (len(S["V"]), len(S["faces"])) == COUNTS[name], (name, len(S["V"]), len(S["faces"]))
    if name != "B3_permutahedron_123":
        L = set()
        for f, k in S["faces"]:
            for i in range(len(f)):
                d = vsub(S["V"][f[i]], S["V"][f[(i + 1) % len(f)]]); L.add(dot(d, d).key())
        assert len(L) == 1, "uniform: all edges equal"
    return S
if __name__ == "__main__":
    from collections import Counter
    for nm in COUNTS:
        S = build(nm); print(nm, len(S["V"]), "vertices", dict(Counter(k for f, k in S["faces"])), "ok")
