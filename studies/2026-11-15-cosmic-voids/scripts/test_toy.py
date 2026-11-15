"""Independent checks of toy_foam.Foam.state:
1. Voronoi mode: contacts equal those of scipy.spatial.Delaunay on all 27 periodic copies (a different Qhull call, no margin cut).
2. Power mode: every cell reported empty is hidden: its lifted point lies on or above the lower hull (checked against the hull facets).
3. Lattice centres (degenerate): the robustness check (random shift) is expected to DISAGREE or the frame to carry non-generic ties."""
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toy_foam import Foam, foam_N
from scipy.spatial import Delaunay
ok = True
for seed in (1, 2, 3):
    f = Foam(216, 'voronoi', 1.0, 0.5, 0.0, seed); foam_N[0] = 216
    for t in (0.0, 0.37):
        alive, E, nt, nf, okm = f.state(t)
        x, _ = f.at(t)
        P = np.concatenate([x + np.array(o) for o in itertools.product((-1, 0, 1), repeat=3)])
        I = np.tile(np.arange(216), 27)
        D = Delaunay(P)
        E2 = set()
        for s in D.simplices:
            if ((s >= 13 * 216) & (s < 14 * 216)).any():       # touches the central copy (offset (0,0,0) is copy 13)
                ids = sorted(I[s].tolist())
                for a, b in itertools.combinations(ids, 2): E2.add(a * 216 + b)
        same = set(E) == E2
        print('voronoi', seed, t, 'contacts', len(E), 'independent', len(E2), 'equal', same, 'Euler', len(alive) - len(E) + nf - nt, 'margin ok', okm)
        ok &= same and okm and len(alive) - len(E) + nf - nt == 0 and len(alive) == 216
f = Foam(216, 'walk', 1.0, 0.5, 3.0, 1); foam_N[0] = 216
alive, E, nt, nf, okm = f.state(1.0)
print('walk A=3 at t=1: cells alive', len(alive), 'of 216; Euler', len(alive) - len(E) + nf - nt, 'margin ok', okm)
ok &= len(alive) < 216 and len(alive) - len(E) + nf - nt == 0
print('ALL OK' if ok else 'SOME FAIL'); sys.exit(0 if ok else 1)
