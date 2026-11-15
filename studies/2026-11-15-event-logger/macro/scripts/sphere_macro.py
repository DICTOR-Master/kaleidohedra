"""Control of the macroscopic count: moving seeds on the sphere (Voronoi: no cell ever vanishes, so every swap must be free and the
swap count must equal the logger's and the Delaunay 2-2 flips; power diagram: births and deaths occur and are reported). Seed motion
and flip reference copied unchanged from ../../scripts/voronoi_sphere.py (via ../../pairing/scripts/sphere_control.py).
Rules fixed before the run: W = P = 2e-4 (main pairing rule), tau = 4e-4 (2W), also 2e-4 and 8e-4.
Usage: python sphere_macro.py MODE N SEED TMAX OUT.json DT [DT ...]"""
import numpy as np, sys, json, os, time
from collections import Counter
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from eventlog import from_triangles
import pairing as PR, macro as MA
MODE, N, SEED, TMAX, OUT, DTS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], [float(x) for x in sys.argv[6:]]
WP, TAUS = 2e-4, [4e-4, 2e-4, 8e-4]
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
t0 = time.time(); out = dict(mode=MODE, N=N, seed=SEED, tmax=TMAX, W=WP, P=WP, taus=TAUS, runs={})
K = len(DTS)
for kk, dt in enumerate(DTS):
    ts = np.round(np.arange(0, TMAX + dt / 2, dt), 12); fl = Counter(); prevT = [None]
    def gen(count):                 # frames streamed (regenerated for the second pass) so memory stays small
        for i, t in enumerate(ts):
            tr = tris(t)
            if count and prevT[0] is not None:
                for q in flips(prevT[0], tr): fl[{(2, 2): 'flip 2-2', (1, 3): 'flip 1-3', (3, 1): 'flip 3-1'}.get(q, f'several {q}')] += 1
            prevT[0] = tr
            if i % 2000 == 0: print(f'PROGRESS {(kk + (0.5 if not count else 0) + 0.5 * i / len(ts)) / K:.3f} dt {dt} frame {i}/{len(ts)}', flush=True)
            yield from_triangles(tr, float(t))
    data = PR.collect(gen(True)); _, cev = MA.cell_events(gen(False))
    res = {f'tau={tau}': MA.macro_from(data, cev, WP, WP, tau, units='seed-motion time') for tau in TAUS}
    m = res[f'tau={TAUS[0]}']
    out['runs'][str(dt)] = dict(frames=len(ts), flips=dict(fl), logger_swaps=data['raw'].get('swap', 0), macro=res)
    print(f'dt {dt}: flips {dict(fl)}; logger swaps {data["raw"].get("swap", 0)}; ' + '; '.join(
        f'{k}: swaps {v["swaps"]} free {v["primary"]["free"]} attached {v["primary"]["attached"]} (ring free {v["ring"]["free"]})'
        for k, v in res.items()), flush=True)
out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(OUT, 'w'), indent=1, default=str)
def run_ok(r):
    ms = r['macro'].values()
    ident = all(v[k]['identity_ok'] for v in ms for k in ('primary', 'ring'))
    same = all(v['swaps'] == r['logger_swaps'] == r['flips'].get('flip 2-2', 0) for v in ms)
    allfree = all(v['primary']['free'] == v['swaps'] for v in ms) if MODE == 'voronoi' else True
    return ident and same and allfree
print('SPHERE_MACRO_OK' if all(run_ok(r) for r in out['runs'].values()) else 'SPHERE_MACRO_FAIL')
