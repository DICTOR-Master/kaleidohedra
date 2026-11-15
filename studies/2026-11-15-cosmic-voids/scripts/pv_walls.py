"""Reference for the neighbour rule: periodic Poisson-Voronoi cells (tracer_zones.voronoi_periodic: Qhull Delaunay with periodic copies), mean neighbours when a face counts only if its area is
at least eps * Vbar^(2/3) (Vbar = mean cell volume), for the eps list of basin_events. eps = 0 must give 48 pi^2 / 35 + 2 = 15.535
(Meijering 1953). Usage: pv_walls.py OUT N seeds"""
import sys, json
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from basin_events import EPS_LIST
from tracer_zones import voronoi_periodic
out, N, S = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rows = []
for s in range(S):
    pos = np.random.default_rng(1000 + s).random((N, 3))
    V, qi, pj, w = voronoi_periodic(pos, 1.0, margin=3.0 * N ** (-1 / 3))
    a = w[qi < pj] / (1.0 / N) ** (2 / 3)
    rows.append([2 * np.count_nonzero(a >= e) / N for e in EPS_LIST])
    print(f'PROGRESS {(s + 1) / S:.3f} seed {s} eps0 {rows[-1][0]:.4f} volsum {V.sum():.12f}', flush=True)
r = np.array(rows)
res = dict(N=N, seeds=S, eps_list=list(EPS_LIST), mean=list(r.mean(0)), sem=list(r.std(0, ddof=1) / np.sqrt(S)), meijering=48 * np.pi ** 2 / 35 + 2)
json.dump(res, open(out, 'w'), indent=1); print(res)
ok = abs(res['mean'][0] - res['meijering']) < 4 * res['sem'][0] + 0.01
sys.exit(0 if ok else 1)
