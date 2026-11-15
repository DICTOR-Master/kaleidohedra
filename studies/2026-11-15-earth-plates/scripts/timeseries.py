"""Event time series, a reorganisation test and neighbour-number distributions for finished Earth runs (One tissue, three scales,
Section 1, second round; DICTO 15 Nov 2026). Post-processing of results/frames_MODEL_RULE_L0.jsonl and results/events_MODEL_RULE_L0.json
written by earth_mesh.py; the rules are stated in README section 7 before any run.
  * classes: persistent swaps (two-sided k = 5 Myr, swaps.py, including swaps joined through four-fold meetings), splits, merges,
    births, deaths; an event between frames t0 and t0 - 1 has age t0 - 0.5;
  * bins of 5 and 10 Myr over the model's span;
  * reorganisation test: statistic = events (persistent swaps + splits + merges + births) with age in W = [98,108) U [45,55) Ma within
    0-230 Ma; null = circular shift of the event series by a whole number of Myr uniform in 0..229; 10 000 shifts, seed 20261115;
    one-sided p = share of shifts with count >= observed. Same test for persistent swaps alone and (exploratory) for [20,26) Ma;
  * neighbour numbers per frame: sides n (boundaries per cell, counted per boundary) and distinct neighbours; mean against 6 - 12/F;
    variance mu2, share of three-sided cells and the largest n against Poisson-Voronoi on the sphere with the same F (uniform random
    points, Voronoi cells = vertex degrees of the convex hull; NPV maps per F, seed fixed).
Usage: python timeseries.py RESULTS_DIR OUT.json MODEL_RULE [MODEL_RULE ...]"""
import sys, os, json, math
from collections import Counter, defaultdict
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts')); sys.path.insert(0, HERE)
from eventlog import Tiling
from swaps import swap_list, persistent

W = [(98, 108), (45, 55)]
W_EXPL = [(20, 26)]
TEST_SPAN = (0, 230)
NSHIFT, SEED, NPV = 10000, 20261115, 2000
CLASSES = ('pswap', 'split', 'merge', 'birth', 'death')

def events(fr, rows, k=5):
    sw = swap_list(fr, rows); out = []
    for s in sw:
        if persistent(fr, [s], k)[0]: out.append(('pswap', fr[s['iA']].t - 0.5))
    for r in rows:
        if r['type'] in ('split', 'merge', 'birth', 'death'): out.append((r['type'], r['t0'] - 0.5))
    return out, len(sw)

def bins(ev, lo, hi, width):
    edges = list(range(lo, hi + width, width)); out = {c: [0] * (len(edges) - 1) for c in CLASSES}
    for c, a in ev:
        i = int((a - lo) // width)
        if 0 <= i < len(edges) - 1: out[c][i] += 1
    return dict(edges=edges, counts=out)

def in_w(a, wins): return any(lo <= a < hi for lo, hi in wins)

def shift_test(ages, wins, span, rng):
    lo, hi = span; L = hi - lo
    a = np.array([x for x in ages if lo <= x < hi])
    if len(a) == 0: return dict(n=0)
    win = np.zeros(L, bool)
    for wl, wh in wins: win[max(wl, lo) - lo:min(wh, hi) - lo] = True
    obs = int(win[(np.floor(a) - lo).astype(int)].sum())
    u = rng.integers(0, L, NSHIFT)
    idx = ((np.floor(a)[None, :] - lo + u[:, None]) % L).astype(int)
    null = win[idx].sum(1)
    wlen = int(win.sum()); rate_in = obs / wlen; rate_out = (len(a) - obs) / (L - wlen)
    return dict(n=int(len(a)), in_window=obs, expected=round(len(a) * wlen / L, 2), rate_ratio=round(rate_in / rate_out, 3) if rate_out else None,
                p=round(float(np.mean(null >= obs)), 4), null_mean=round(float(null.mean()), 2), null_q95=float(np.quantile(null, 0.95)))

def sides(T):
    c = Counter()
    for a, b in T.segments: c[a] += 1; c[b] += 1
    return np.array([c[x] for x in sorted(T.cells)]), np.array([len(T.nb[x]) for x in sorted(T.cells)])

PV = {}
def pv(F, rng):
    if F in PV: return PV[F]
    mu2, f3, nmax, mean = [], [], [], []
    for _ in range(NPV):
        X = rng.normal(size=(F, 3)); X /= np.linalg.norm(X, axis=1)[:, None]
        h = ConvexHull(X); deg = np.zeros(F, int)
        E = set()
        for s in h.simplices:
            for i, j in ((s[0], s[1]), (s[1], s[2]), (s[0], s[2])): E.add((min(i, j), max(i, j)))
        for i, j in E: deg[i] += 1; deg[j] += 1
        mean.append(deg.mean()); mu2.append(deg.var()); f3.append(np.mean(deg == 3)); nmax.append(deg.max())
    PV[F] = dict(mean=float(np.mean(mean)), mu2=float(np.mean(mu2)), mu2_sd=float(np.std(mu2)), f3=float(np.mean(f3)),
                 nmax_q99=float(np.quantile(nmax, 0.99)), nmax_mean=float(np.mean(nmax)))
    return PV[F]

def one(d, mr, rng):
    lines = open(os.path.join(d, f'frames_{mr}_L0.jsonl')).read().splitlines()
    fr = [Tiling.from_json(l) for l in lines]
    rows = json.load(open(os.path.join(d, f'events_{mr}_L0.json')))
    ev, nsw = events(fr, rows)
    ts = [T.t for T in fr]; lo, hi = min(ts), max(ts)
    tot = Counter(c for c, a in ev)
    span = (max(lo, TEST_SPAN[0]), min(hi, TEST_SPAN[1]))             # event ages t0 - 0.5 lie in [lo, hi)
    tests = None
    if span[1] - span[0] >= 99 and span[0] <= 45:                 # spans: 0-230 Ma, or the model's record if shorter (README 7, amended)
        main = [a for c, a in ev if c in ('pswap', 'split', 'merge', 'birth')]
        tests = dict(span=list(span), combined=shift_test(main, W, span, rng), pswap=shift_test([a for c, a in ev if c == 'pswap'], W, span, rng),
                     combined_100only=shift_test(main, W[:1], span, rng), combined_50only=shift_test(main, W[1:], span, rng),
                     exploratory_20_26=shift_test(main, W_EXPL, span, rng))
    nf = []
    for T in fr:
        n, k = sides(T); F = len(T.cells); p = pv(F, rng) if F >= 4 else None
        nf.append(dict(t=T.t, F=F, loops=T.loops, components=T.components, mean=round(float(n.mean()), 4), euler_mean=round(6 - 12 / F, 4),
                       mu2=round(float(n.var()), 3), f3=round(float(np.mean(n == 3)), 3), nmax=int(n.max()), nmin=int(n.min()),
                       nb_mean=round(float(k.mean()), 3), nb_mu2=round(float(k.var()), 3), hist=dict(Counter(map(int, n))),
                       pv_mu2=round(p['mu2'], 3) if p else None, pv_f3=round(p['f3'], 3) if p else None, pv_nmax_q99=p['nmax_q99'] if p else None))
    clean = [x for x in nf if not x['loops'] and x['components'] == 1]
    return dict(model=mr, span=[lo, hi], frames=len(fr), swaps_all=nsw, totals=dict(tot), events=[[c, a] for c, a in ev],
                bins10=bins(ev, lo, hi, 10), bins5=bins(ev, lo, hi, 5), tests=tests,
                neighbours=dict(frames=nf, euler_mean_exact=sum(abs(x['mean'] - x['euler_mean']) < 1e-3 for x in clean), clean_frames=len(clean),
                                mu2_ratio_min=min(x['mu2'] / x['pv_mu2'] for x in nf if x['pv_mu2']),
                                mu2_ratio_median=float(np.median([x['mu2'] / x['pv_mu2'] for x in nf if x['pv_mu2']])),
                                f3_ratio_median=float(np.median([x['f3'] / x['pv_f3'] for x in nf if x['pv_f3']])),
                                nmax_above_q99=sum(x['nmax'] > x['pv_nmax_q99'] for x in nf if x['pv_nmax_q99'] is not None)))

if __name__ == '__main__':
    d, out, mrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    rng = np.random.default_rng(SEED); res = []
    for i, mr in enumerate(mrs):
        r = one(d, mr, rng); res.append(r)
        t = r['tests']
        print(f'PROGRESS {(i + 1) / len(mrs):.3f} {mr}: totals {r["totals"]}; test {t["combined"] if t else "-"}; '
              f'Euler-exact {r["neighbours"]["euler_mean_exact"]}/{r["neighbours"]["clean_frames"]}; mu2 ratio min {r["neighbours"]["mu2_ratio_min"]:.2f}', flush=True)
    json.dump(dict(rules=dict(W=W, W_exploratory=W_EXPL, span=TEST_SPAN, shifts=NSHIFT, seed=SEED, pv_maps_per_F=NPV), runs=res), open(out, 'w'))
    print('FINAL ok' if all(r['neighbours']['clean_frames'] == 0 or r['neighbours']['euler_mean_exact'] == r['neighbours']['clean_frames'] for r in res)
          else 'FINAL FAIL Euler mean check', flush=True)
