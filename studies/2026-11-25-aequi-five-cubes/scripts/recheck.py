# Copy from study 2026-11-20-aequi-two-placements; only edit (study 2026-11-25): the log-depth box half-width BOX (env, default 1.5 as before).
# Re-search the orbit sets whose first search found no fair die: 2048 Sobol starts (seed 2) plus the centre, maxfev
# 200·m, same box and acceptance as solve.py; also reports the singular values of the fairness Jacobian at each
# solution (finite differences, step 1e-6). Writes a record per set (same format as solve.py) to out.jsonl.
# usage: recheck.py classes.json sol1.jsonl [sol2.jsonl ...] NPROC out.jsonl
import json, sys, numpy as np
from multiprocessing import Pool
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from groups import DIRS
from solve import face_omegas, record
from scipy.optimize import root
from scipy.stats import qmc
import os; BOX = float(os.environ.get('BOX', 1.5))   # study 2026-11-25
cls = json.load(open(sys.argv[1])); npr = int(sys.argv[-2]); out = sys.argv[-1]
todo = []
for f in sys.argv[2:-2]:
    for L in open(f):
        r = json.loads(L)
        if not r['sols']: todo.append((r['cls'], r['m'], tuple(r['subset'])))
def setup(ci, S):
    orbs = cls[ci]['orbits']; idx = [j for i in S for j in orbs[i]]; Nrm = DIRS[idx]; N = len(idx)
    sizes = [len(orbs[i]) for i in S]; m = len(S); T = 4 * np.pi / N; cut = np.cumsum([0] + sizes)
    def F(x):
        if not np.all(np.isfinite(x)) or np.abs(x).max() > BOX: return np.full(m - 1, 10.0) + np.abs(np.nan_to_num(x, nan=9.0)).max()
        try: om = face_omegas(Nrm, np.repeat(np.exp(np.r_[0.0, x]), sizes))
        except Exception: return np.full(m - 1, 10.0)
        return np.array([om[cut[k]:cut[k + 1]].mean() - T for k in range(1, m)])
    def allfaces(x): return face_omegas(Nrm, np.repeat(np.exp(np.r_[0.0, x]), sizes)) - T
    return F, allfaces, m
def one(args):
    ci, S, x0 = args
    F, allfaces, m = setup(ci, S)
    try: r = root(F, x0, method='hybr', options=dict(xtol=1e-14, maxfev=200 * m))
    except Exception: return None
    x = r.x
    if not np.all(np.isfinite(x)) or np.abs(x).max() > 2 * BOX: return None
    try: om = allfaces(x)
    except Exception: return None
    return list(x) if np.abs(om).max() < 1e-10 else None
if __name__ == '__main__':
    lo, hi = np.log(0.65), np.log(1.7)
    with Pool(npr) as pool, open(out, 'w') as fo:
        for ci, m, S in todo:
            st = [list(lo + (hi - lo) * s) for s in qmc.Sobol(m - 1, seed=2).random(2048)] + [[0.0] * (m - 1)]
            xs = [x for x in pool.map(one, [(ci, S, x0) for x0 in st]) if x is not None]
            rec = record(cls[ci]['orbits'], S, xs); rec.update(cls=ci, group=cls[ci]['name'], m=m, nstarts=len(st), recheck=True)
            F, allfaces, _ = setup(ci, S)
            for s in rec['sols']:
                x = np.log(s[1:]); J = np.array([(F(x + 1e-6 * e) - F(x - 1e-6 * e)) / 2e-6 for e in np.eye(m - 1)]).T
                print('  solution', np.round(s, 10).tolist(), 'Jacobian singular values', np.linalg.svd(J, compute_uv=False).round(8).tolist())
            print('class', ci, cls[ci]['name'], 'm', m, 'set', S, 'fams', rec['fams'], 'starts', len(st), 'converged', len(xs), 'distinct', len(rec['sols']), flush=True)
            fo.write(json.dumps(rec) + '\n')
    print('FINAL ok' if todo else 'FINAL FAIL: nothing to re-search', flush=True)   # study 2026-11-25: conditional
