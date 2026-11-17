"""Null curve: net change of contacts per cell after an rms displacement D (in spacings), periodic 2D Poisson-Voronoi.

Each of N seeds in the unit torus is moved by an independent Gaussian displacement of rms length D * l (l = N^(-1/2)); contacts
(Delaunay edges) at the start and the end are compared exactly as in studies/2026-11-15-tissue-null-models/scripts/moving.py:
net per cell = (net_lost + net_made) / N, share of contacts changed = net_lost / 3N. Net uses only the two end configurations,
so straight-line motion with Gaussian velocities and Brownian motion (both Gaussian at the end) give the same curve.
Check: D = 1.0 reproduces the null study's 3.600 +- 0.006 within 0.02.
Usage: null_net.py OUT.json [N] [REPS]"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '2026-11-15-tissue-null-models', 'scripts'))
from nulllib import edge_keys

OUT = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 20000; REPS = int(sys.argv[3]) if len(sys.argv) > 3 else 4
DS = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.70, 1.00]
t0 = time.time(); ell = N ** -0.5
rows = []
for r in range(REPS):
    rng = np.random.default_rng(18000 + r)
    P = rng.random((N, 2)); E0 = edge_keys(P); G = rng.normal(size=(N, 2))
    for D in DS:
        E1 = edge_keys((P + G * D * ell / np.sqrt(2)) % 1.0)
        lost = int(np.setdiff1d(E0, E1, assume_unique=True).size); made = int(np.setdiff1d(E1, E0, assume_unique=True).size)
        rows.append(dict(rep=r, D=D, N=N, contacts=int(E0.size), lost=lost, made=made))
    print(f'PROGRESS rep {r + 1}/{REPS} {time.time() - t0:.0f} s', flush=True)
summ = {}
for D in DS:
    rs = [x for x in rows if x['D'] == D]
    net = np.array([(x['lost'] + x['made']) / x['N'] for x in rs]); sh = np.array([x['lost'] / x['contacts'] for x in rs])
    summ[str(D)] = dict(net_per_cell=float(net.mean()), err=float(net.std(ddof=1) / np.sqrt(len(net))),
                        share_changed=float(sh.mean()), share_err=float(sh.std(ddof=1) / np.sqrt(len(sh))))
    print('NULL', D, summ[str(D)], flush=True)
ok = abs(summ['1.0']['net_per_cell'] - 3.600) <= 0.02 and all(x['contacts'] == 3 * N for x in rows)
json.dump(dict(N=N, reps=REPS, rows=rows, summary=summ, wall_s=time.time() - t0,
               check_reproduces_3600=bool(abs(summ['1.0']['net_per_cell'] - 3.600) <= 0.02)), open(OUT, 'w'), indent=1)
print('FINAL ok' if ok else 'FINAL FAIL (3.600 not reproduced or contacts != 3N)', flush=True)
