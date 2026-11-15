"""Control 1 of the pairing rules: moving seeds on the sphere (Voronoi and power diagram), where every swap is known exactly from
the Delaunay flips. The counts with the rules (fixed W, P in the system's time unit) must equal the counts without them, at every step.
The seed motion (state, tris) and the flip reference are copied unchanged from ../../scripts/voronoi_sphere.py (validation (b)).
Usage: python sphere_control.py MODE N SEED TMAX OUT.json DT [DT ...]"""
import numpy as np, sys, json, os, time
from collections import Counter
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from eventlog import from_triangles
import pairing as PR
MODE, N, SEED, TMAX, OUT, DTS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], [float(x) for x in sys.argv[6:]]
RULES = [(0.0, 0.0), (2e-4, 2e-4), (1e-3, 1e-3)]        # (W, P) fixed before the run; time unit of the seed motion
# ---- copied unchanged from voronoi_sphere.py ----
rng = np.random.default_rng(SEED)
n0 = rng.normal(size=(N, 3)); A = rng.normal(size=(N, 3)) * 0.25; W = rng.uniform(1, 3, size=(N, 3)); PH = rng.uniform(0, 6.3, size=(N, 3))
amp = rng.uniform(0, 0.2, size=N) if MODE == 'power' else np.zeros(N); om = rng.uniform(1, 4, size=N); ph = rng.uniform(0, 6.3, size=N)
def state(t):
    n = n0 + A * np.sin(W * t + PH); n /= np.linalg.norm(n, axis=1)[:, None]
    h = 1 - amp * (1 + np.sin(om * t + ph)) / 2
    return n / h[:, None]
def tris(t):
    hull = ConvexHull(state(t)); return [tuple(sorted(map(int, s))) for s in hull.simplices]
def flips(T0, T1):
    r, a = set(T0) - set(T1), set(T1) - set(T0)
    tri = [('r', x) for x in r] + [('a', x) for x in a]
    edges = lambda x: {(x[0], x[1]), (x[0], x[2]), (x[1], x[2])}
    par = list(range(len(tri)))
    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for i in range(len(tri)):
        for j in range(i + 1, len(tri)):
            if edges(tri[i][1]) & edges(tri[j][1]): par[f(i)] = f(j)
    g = Counter()
    for i, (k, _) in enumerate(tri): g[(f(i), k)] += 1
    roots = {f(i) for i in range(len(tri))}
    return [(g[(q, 'r')], g[(q, 'a')]) for q in roots]
# ---- end of copied part ----
t0 = time.time(); out = dict(mode=MODE, N=N, seed=SEED, tmax=TMAX, rules=RULES, runs={})
K = len(DTS)
for kk, dt in enumerate(DTS):
    ts = np.round(np.arange(0, TMAX + dt / 2, dt), 12); fl = Counter(); prevT = [None]
    def gen():
        for i, t in enumerate(ts):
            tr = tris(t)
            if prevT[0] is not None:
                for q in flips(prevT[0], tr): fl[{(2, 2): 'flip 2-2', (1, 3): 'flip 1-3', (3, 1): 'flip 3-1'}.get(q, f'several {q}')] += 1
            prevT[0] = tr
            if i % 2000 == 0: print(f'PROGRESS {(kk + i / len(ts)) / K:.3f} dt {dt} frame {i}/{len(ts)}', flush=True)
            yield from_triangles(tr, float(t))
    data = PR.collect(gen())
    res = {}
    for Wr, Pr in RULES:
        _, s = PR.apply_rules(data, Wr, Pr, units='seed-motion time')
        res[f'W={Wr} P={Pr}'] = s
    raw = res['W=0.0 P=0.0']['raw_counts'].get('swap', 0)
    same = all(r['swaps'] == raw == fl['flip 2-2'] for r in res.values())
    out['runs'][str(dt)] = dict(frames=len(ts), flips=dict(fl), logger_swaps=raw, rules=res, identical_with_and_without=same)
    print(f'dt {dt}: flips {dict(fl)}; logger swaps {raw}; with rules ' +
          ', '.join(f'{k}: {v["swaps"]} (paired {v["swaps_paired"]}, cancelled {v["swaps_cancelled_flicker"]})' for k, v in res.items()) +
          f'; identical {same}', flush=True)
out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(OUT, 'w'), indent=1, default=str)
# the main rule set (2e-4) must give identical counts; the wide set (1e-3) is reported, a difference there is a finding, not a fault
main_ok = all(r['rules']['W=0.0002 P=0.0002']['swaps'] == r['logger_swaps'] == r['flips'].get('flip 2-2', 0) for r in out['runs'].values())
print('SPHERE_OK' if main_ok else 'SPHERE_FAIL')
