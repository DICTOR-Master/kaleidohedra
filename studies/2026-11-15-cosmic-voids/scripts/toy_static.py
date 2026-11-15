"""Mean contacts per cell of the periodic Poisson-Voronoi foam against 48π²/35 + 2 = 15.535 (Meijering 1953), by box size N
(single frames, 4 seeds each; Euler and margin checks). Usage: toy_static.py OUT.json"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toy_foam import Foam, foam_N
rows = []; Ns = (512, 1000, 4096, 8000); ok = True
for i, N in enumerate(Ns):
    d = []
    for seed in (1, 2, 3, 4):
        f = Foam(N, 'voronoi', 1.0, 0.5, 0.0, seed); foam_N[0] = N
        alive, E, nt, nf, okm = f.state(0.0)
        ok &= okm and len(alive) - len(E) + nf - nt == 0 and len(alive) == N
        d.append(2 * len(E) / N)
    rows.append(dict(N=N, mean=float(np.mean(d)), sd_of_mean=float(np.std(d, ddof=1) / 2), seeds=d)); print(rows[-1], flush=True)
    print(f'PROGRESS {(i + 1) / len(Ns):.2f} N={N}', flush=True)
json.dump(dict(target=48 * np.pi ** 2 / 35 + 2, rows=rows), open(sys.argv[1], 'w'), indent=1)
sys.exit(0 if ok else 1)
