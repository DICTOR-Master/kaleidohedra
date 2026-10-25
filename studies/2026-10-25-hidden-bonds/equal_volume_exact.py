# Exact equal-volume points (hidden-bonds follow-up, 2026-10-25): for the gyrated octet (hcp holes), the Delian octet (control)
# and C15, find the weight where the two kinds' pieces have equal volume, exactly (census engine, sympy), and describe the pieces
# there. Each orbit (site of the motif) is reported separately, since the hcp tetrahedral holes form two orbits.
import sys
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, '../2026-10-25-relay-census/scripts')
from engine import Net, Cell, LAM, cell_volume
from networks import NETS
RUNS = [('delian', Fr(-1, 50)), ('hcpholes', Fr(1, 300)), ('c15', Fr(-5, 8))]   # samples next to the float roots
for key, l0 in RUNS:
    spec = NETS[key]; net = Net(spec['name'], spec['G'], spec['T'], spec['motif'], spec['w']); D2 = Fr(spec['D2'])
    cells = [Cell(net, i, (l0,), D2) for i in range(len(net.motif))]
    lo = max([c.interval()[0] for c in cells if c.interval()[0] is not None], default=None)
    hi = min([c.interval()[1] for c in cells if c.interval()[1] is not None], default=None)
    V = [cell_volume(c, c.faces()) for c in cells]
    A, B = spec['A'], spec['B']
    vA = [v for c, v in zip(cells, V) if c.kind == A]; vB = [v for c, v in zip(cells, V) if c.kind == B]
    print(f"== {key}: open interval ({lo}, {hi}) around {l0}")
    for c, v in zip(cells, V):
        F = c.faces(); sz = {}
        for pts in F.values(): sz[len(pts)] = sz.get(len(pts), 0) + 1
        print(f"  site {c.i} {c.kind}: corners {len(c.corners)}, faces {dict(sorted(sz.items()))}, volume {sp.factor(v)}")
    roots = [r for r in sp.solve(sp.Eq(vA[0], vB[0]), LAM) if r.is_real and (lo is None or r > lo) and (hi is None or r < hi)]
    for r in roots:
        print(f"  EQUAL VOLUME ({A} site {cells[[c.kind for c in cells].index(A)].i} = {B}) at lam = {sp.nsimplify(r)} = {float(r):.10f}")
        print(f"    volumes there: " + ", ".join(f"site {c.i} {c.kind} {sp.nsimplify(sp.simplify(v.subs(LAM, r)))}" for c, v in zip(cells, V)))
        same = len({sp.simplify(v.subs(LAM, r)) for v in V}) == 1
        print(f"    all sites equal: {same}")
    if not roots: print("  no equal-volume root inside this interval")
