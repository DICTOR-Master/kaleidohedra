"""Validation (b): a Voronoi tiling of the sphere with slowly moving seeds (mode voronoi) and its weighted form, the spherical power
diagram with slowly changing weights (mode power), logged by eventlog.py at several time steps.
Construction: cell i is the face of the polyhedron {x : n_i . x <= h_i} (n_i the seed on the unit sphere, h_i <= 1 its weight; h = 1
gives the Voronoi tiling), projected from the centre onto the sphere. Its combinatorics are those of the convex hull of the points
n_i / h_i (polar duality): hull vertices = cells present, hull edges = boundaries, hull triangles = junctions (all triple when generic).
Independent check: the hull's triangles are the weighted Delaunay triangulation (#52); between frames its change is a list of flips,
split into groups of edge-sharing triangles and classified directly from the triangles removed / added in each group: 2-2 (= swap), 1-3 (= birth), 3-1 (= death), anything else = several at once.
Usage: python voronoi_sphere.py MODE N SEED TMAX DT [DT ...]  -> voronoi_MODE_N_SEED.json"""
import numpy as np, sys, json, os
from collections import Counter
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eventlog import from_triangles, run_stream
MODE, N, SEED, TMAX, DTS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), [float(x) for x in sys.argv[5:]]
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
    """Flips between two triangulations, split into local groups: removed and added triangles that share an edge (directly or
    through others) form one group; each group is classified by (removed, added). Independent of eventlog.py."""
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
out = dict(mode=MODE, N=N, seed=SEED, tmax=TMAX, runs={})
K = len(DTS)
for kk, dt in enumerate(DTS):
    ts = np.round(np.arange(0, TMAX + dt / 2, dt), 12)
    fl = Counter(); prevT = [None]; first = last = None
    def gen():
        for i, t in enumerate(ts):
            tr = tris(t)
            if prevT[0] is not None:
                for q in flips(prevT[0], tr):
                    fl[{(2, 2): 'flip 2-2', (1, 3): 'flip 1-3', (3, 1): 'flip 3-1'}.get(q, f'several at one place {q}')] += 1
            prevT[0] = tr
            if i % 2000 == 0: print(f'PROGRESS {(kk + i / len(ts)) / K:.3f} dt {dt} frame {i}/{len(ts)}', flush=True)
            yield from_triangles(tr, float(t))
    frames = gen()
    _, summ = run_stream(frames)
    agree = (summ['counts'].get('swap', 0) == fl['flip 2-2'] and summ['counts'].get('birth', 0) == fl['flip 1-3'] and
             summ['counts'].get('death', 0) == fl['flip 3-1'])
    only = set(summ['counts']) <= {'swap', 'birth', 'death'}
    neg = summ['neg_control_caught']
    T0, T1 = from_triangles(tris(ts[0])), from_triangles(tris(ts[-1]))
    out['runs'][str(dt)] = dict(frames=len(ts), cells_first=len(T0.cells), cells_last=len(T1.cells), logger=summ,
                               flips=dict(fl), logger_equals_flips=agree, only_swap_birth_death=only, neg_control_caught=neg)
    print(f'dt {dt}: {len(ts)} frames, cells {len(T0.cells)} -> {len(T1.cells)}; logger {summ["counts"]} ok {summ["ok"]}; '
          f'flips {dict(fl)}; agree {agree}; only swap/birth/death {only}; NEG caught {neg}', flush=True)
json.dump(out, open(f'voronoi_{MODE}_{N}_{SEED}.json', 'w'), indent=1)
print('PROGRESS 1.000 done', flush=True)
