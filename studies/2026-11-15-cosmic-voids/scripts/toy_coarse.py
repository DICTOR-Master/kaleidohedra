"""Fixed-step sampling of the toy foam, measured exactly as the void basins are: frames every dt (no halving) through the shared logger,
then the share of SEEN contact changes that come alone (a logger 'contact gained'/'contact lost' event), against the seen contact
changes per cell per step. Gives the curve a one-at-a-time process traces when sampled coarsely. Usage: toy_coarse.py OUT N mode A"""
import sys, os, json, re
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toy_foam import Foam, foam_N, tiling, EL
out, N, mode, A = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
f = Foam(N, mode, 1.0, 0.5, A, 1); foam_N[0] = N
dt0 = 0.005; ts = np.arange(0, 1 + 1e-12, dt0)
frames = []
for i, t in enumerate(ts):
    frames.append(tiling(float(t), f.state(t)))
    print(f'PROGRESS {0.8 * (i + 1) / len(ts):.3f} frame {i + 1}/{len(ts)}', flush=True)
res = []
for k in (1, 2, 4, 8, 16, 32):
    fr = frames[::k]; alone = seen = 0; ncell = []
    for X, Y in zip(fr, fr[1:]):
        for e in EL.classify(X, Y):
            b, d, l, g = map(int, re.findall(r'\d+', e['pattern'])); seen += l + g
            if e['type'] in ('contact gained', 'contact lost'): alone += l + g
        ncell.append(len(Y.cells))
    res.append(dict(dt=dt0 * k, steps=len(fr) - 1, seen_contact_changes=seen, alone_share=alone / seen if seen else None,
                    seen_per_cell_per_step=seen / np.mean(ncell) / (len(fr) - 1)))
    print(res[-1], flush=True)
json.dump(dict(N=N, mode=mode, A=A, rows=res), open(out, 'w'), indent=1)
ok = all(r['alone_share'] is not None for r in res); sys.exit(0 if ok else 1)
