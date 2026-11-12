# inspect_surv.py (13 Nov 2026): structure of the keyed-RD survivors' tiling problems: viable orientations after arc consistency,
# partners per (orientation, direction), and whether the fit relation is deterministic (one partner each way).
# usage: inspect_surv.py <deep48 json files, comma-separated>
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__)); J = sys.argv[1]
sys.argv = ['hunt.py', 'none']; exec(open(os.path.join(here, 'hunt.py')).read().split('# ---------------------------------------------------------------- modes')[0])
S = []
for f in J.split(','): S += [H for H, v in json.load(open(f)) if v == 'SURVIVOR']
rows = []
for H in S:
    H = np.array(H); F = fit_table(H); v = arc(F); st = np.nonzero(v)[0]
    deg = F[np.ix_(st, range(12), st)].sum(2)                 # partners per (state, direction) among viable states
    stab = int((H[ACTINV] == H[None, :]).all(1).sum()); flat = int((H == 0).sum())
    rows.append((len(st), int(deg.min()), int(deg.max()), float(deg.mean()), stab, flat))
from collections import Counter
print('survivors', len(S)); print('viable states:', Counter(r[0] for r in rows)); print('partners min/max:', Counter((r[1], r[2]) for r in rows))
print('mean partners:', sorted(Counter(round(r[3], 2) for r in rows).items())); print('symmetry order:', Counter(r[4] for r in rows)); print('flat points:', Counter(r[5] for r in rows))
print('FINAL ok' if len(rows) == len(S) else 'FINAL FAIL: not every survivor inspected')
