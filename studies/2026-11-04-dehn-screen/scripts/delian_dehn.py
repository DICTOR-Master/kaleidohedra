import sys, itertools, numpy as np
sys.argv = sys.argv[:1] + ['x', '8', '300']
exec(open('scripts/dehn.py').read().split("if __name__")[0])
from scipy.spatial import HalfspaceIntersection
RD = [np.array(p, float) for p in {tuple(s*v for s, v in zip(sg, q)) for q in itertools.permutations((1, 1, 0)) for sg in itertools.product((1, -1), repeat=3)}]
for t in (0.0, 0.05, 1/9, 0.2, 0.3):
    Hs = [[*n, -1.0] for n in RD] + [[*s, -1.5*(1 - t)] for s in itertools.product((1., -1.), repeat=3)]
    P = HalfspaceIntersection(np.array(Hs), np.zeros(3)).intersections
    X, F = hull_faces(np.unique(np.round(P, 10), axis=0)); r = dehn(X, F)
    print(f"t={t:.4f} corners {len(X)} zero={r['dehn_zero']} {r['coefficient_sums_over_maxL']}")
