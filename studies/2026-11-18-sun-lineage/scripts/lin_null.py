"""Moving Poisson-Voronoi null WITH births and deaths, lineage net change (README.md, section "Null with births and deaths").

Extends moving.py of studies/2026-11-15-tissue-null-models (independent Gaussian seed steps, Delaunay contacts via nulllib.edge_keys):
seeds move in 10 s steps whose variance follows the Sun's survivor D^2(tau) of one setting (linear between (0, 0) and its six
tau points); each 10 s, Poisson numbers of deaths (uniform among alive seeds; heir = nearest remaining alive seed) and births
(uniform position; parent = nearest alive seed) at the census rates of persistent merges and splits of that setting. Lineages:
anc(new) = anc(parent); anc(heir) gains anc(dead). Counted at tau = 80 ... 640 s with lineage_lib.lineage_counts, and the
survivor count of the parent study (survivor pairs lost + made) / survivors for comparison.
Variants: main; V1 (births = deaths = -ln(s320)/320 s, s320 = Sun survivor share at tau 320 s); V2 (split births: daughter at
parent + 0.25 l, parent uniform among alive); calib (zero rates, D^2 linear to 1.0, outputs at D = 0.1 ... 1.0).
Usage: lin_null.py TAG|calib VARIANT OUT.json [N] [REPS] [setting_index]"""
import sys, os, json, time
import numpy as np
import scipy.sparse as sp
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-15-tissue-null-models', 'scripts'))
sys.path.insert(0, HERE)
from nulllib import edge_keys
from lineage_lib import lineage_counts

TAG, VAR, OUT = sys.argv[1:4]
N = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
REPS = int(sys.argv[5]) if len(sys.argv) > 5 else 4
IDX = int(sys.argv[6]) if len(sys.argv) > 6 else 0
PARENT = os.path.join(HERE, '..', '..', '2026-11-18-sun-net-change', 'results', 'summary.json')
CENSUS = os.path.join(HERE, '..', '..', '2026-11-15-sun-granulation', 'results', 'census')
TAUF = ['8', '16', '24', '32', '48', '64']
DT = 10.0
ell = N ** -0.5

if TAG == 'calib':
    DOUT = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]
    knots_t, knots_D2 = [0.0, 640.0], [0.0, 1.0]
    outs = [640.0 * d * d for d in DOUT]
    beta = delta = 0.0
    grid = sorted(set(outs) | {0.0})            # no events: jump straight between outputs
    info = {}
else:
    S = json.load(open(PARENT))['sun'][TAG]['1']
    knots_t = [0.0] + [S[tf]['tau'] for tf in TAUF]; knots_D2 = [0.0] + [S[tf]['D'] ** 2 for tf in TAUF]
    outs = [S[tf]['tau'] for tf in TAUF]
    r = json.load(open(f'{CENSUS}/{TAG}.json'))['steps']['1']['rate_per_cell_per_min']
    if VAR == 'V1':
        beta = delta = -np.log(S['32']['surv_frac']) / S['32']['tau']
    else:
        beta, delta = r['splits_persistent'] / 60.0, r['merges_persistent'] / 60.0
    grid = [DT * k for k in range(int(round(max(outs) / DT)) + 1)]
    info = dict(sun_D={tf: S[tf]['D'] for tf in TAUF}, sun_surv_frac={tf: S[tf]['surv_frac'] for tf in TAUF},
                census_rates_per_min=dict(splits_persistent=r['splits_persistent'], merges_persistent=r['merges_persistent']))
D2 = lambda t: float(np.interp(t, knots_t, knots_D2))


def one(rep):
    rng = np.random.default_rng(18100 + 10 * IDX + rep)
    cap = N * 4
    pos = np.zeros((cap, 2)); pos[:N] = rng.random((N, 2))
    disp = np.zeros((N, 2))                        # unwrapped displacement of start seeds
    alive = np.zeros(cap, bool); alive[:N] = True; n = N
    anc = [{i} for i in range(N)] + [None] * (cap - N)
    E0 = edge_keys(pos[:N]); assert E0.size == 3 * N
    rows = []
    for j in range(1, len(grid)):
        t0, t1 = grid[j - 1], grid[j]
        al = np.nonzero(alive[:n])[0]
        var = max(D2(t1) - D2(t0), 0.0)
        step = rng.normal(size=(len(al), 2)) * np.sqrt(var / 2) * ell
        pos[al] = (pos[al] + step) % 1.0
        st = al[al < N]; disp[st] += step[al < N]
        if delta > 0 or beta > 0:
            nd = rng.poisson(delta * len(al) * (t1 - t0))
            if nd:
                dead = rng.choice(al, size=min(nd, len(al) - 1), replace=False)
                alive[dead] = False
                rem = np.nonzero(alive[:n])[0]
                _, h = cKDTree(pos[rem], boxsize=1.0).query(pos[dead] % 1.0)
                for d, hh in zip(dead, rem[h]):
                    anc[hh] = anc[hh] | anc[d]; anc[d] = None
            al = np.nonzero(alive[:n])[0]
            nb = rng.poisson(beta * len(al) * (t1 - t0))
            if nb:
                assert n + nb <= cap
                if VAR == 'V2':
                    par = rng.choice(al, size=nb)
                    th = rng.random(nb) * 2 * np.pi
                    newp = (pos[par] + 0.25 * ell * np.stack([np.cos(th), np.sin(th)], 1)) % 1.0
                else:
                    newp = rng.random((nb, 2))
                    _, h = cKDTree(pos[al], boxsize=1.0).query(newp); par = al[h]
                pos[n:n + nb] = newp; alive[n:n + nb] = True
                for k, p in enumerate(par): anc[n + k] = set(anc[p])
                n += nb
        for o in outs:
            if abs(o - t1) < 1e-9:
                al = np.nonzero(alive[:n])[0]
                E1 = edge_keys(pos[al] % 1.0); m = len(al)
                c3 = E1.size == 3 * m
                ec, ed = E1 // m, E1 % m
                rr = np.concatenate([np.full(len(anc[a]), i) for i, a in enumerate(al)])
                cc = np.concatenate([np.fromiter(anc[a], np.int64) for a in al])
                M = sp.csr_matrix((np.ones(len(rr), np.int64), (rr, cc)), shape=(m, N))
                ok_links = bool((np.asarray(M.sum(0)).ravel() > 0).all() and (np.asarray(M.sum(1)).ravel() > 0).all())
                lc = lineage_counts(E0, N, ec, ed, m, M)
                # survivor count of the parent (start seeds alive at the end; indices < N keep their identity)
                sv = al[al < N]; svs = np.zeros(N, bool); svs[sv] = True
                a0, b0 = E0 // N, E0 % N; E0s = E0[svs[a0] & svs[b0]]
                ga, gb = al[ec], al[ed]; k1 = (ga < N) & (gb < N) & svs[np.minimum(ga, N - 1)] & svs[np.minimum(gb, N - 1)]
                E1s = np.unique(np.minimum(ga[k1], gb[k1]).astype(np.int64) * N + np.maximum(ga[k1], gb[k1]))
                sl = int(np.setdiff1d(E0s, E1s, assume_unique=True).size); sm = int(np.setdiff1d(E1s, E0s, assume_unique=True).size)
                # plain count over the start seeds' labels (equals lineage when nobody is born or dies)
                plain = None
                if m == N and np.array_equal(al, np.arange(N)):
                    plain = int(np.setdiff1d(E0, E1, assume_unique=True).size + np.setdiff1d(E1, E0, assume_unique=True).size)
                D = float(np.sqrt((disp[sv] ** 2).sum(1).mean()) / ell) if len(sv) else float('nan')
                rows.append(dict(rep=rep, tau=o, D_target=float(np.sqrt(D2(o))), D=D, N0=N, alive=int(m), surv=int(len(sv)),
                                 contacts_3n=bool(c3), links_ok=ok_links, lin_lost=lc['lost'], lin_made=lc['made'],
                                 lin_pairs=lc['pairs'], fused=lc['fused'], lin_size=lc['size'], surv_lost=sl, surv_made=sm,
                                 E0s=int(E0s.size), plain=plain, contacts=int(E1.size)))
    return rows


if __name__ == '__main__':
    t0 = time.time(); rows = []
    for rep in range(REPS):
        rows += one(rep)
        print(f'PROGRESS rep {rep + 1}/{REPS} {time.time() - t0:.0f} s', flush=True)
    summ = {}
    for o in outs:
        rs = [x for x in rows if abs(x['tau'] - o) < 1e-9]
        lin = np.array([(x['lin_lost'] + x['lin_made']) / x['N0'] for x in rs])
        sur = np.array([(x['surv_lost'] + x['surv_made']) / max(1, x['surv']) for x in rs])
        summ[f'{o:g}'] = dict(tau=o, D_target=rs[0]['D_target'], D=float(np.mean([x['D'] for x in rs])),
                              lin_net=float(lin.mean()), lin_err=float(lin.std(ddof=1) / np.sqrt(len(lin))) if len(lin) > 1 else None,
                              surv_net=float(sur.mean()), surv_frac=float(np.mean([x['surv'] / x['N0'] for x in rs])),
                              lin_share_lost=float(np.mean([x['lin_lost'] / (3 * x['N0']) for x in rs])),
                              lin_size=float(np.mean([x['lin_size'] / x['N0'] for x in rs])),
                              fused_per_cell=float(np.mean([x['fused'] / x['N0'] for x in rs])))
        print('NULL', TAG, VAR, f'tau {o:g}', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in summ[f'{o:g}'].items()}, flush=True)
    # deviation recorded in README: 3N + 1 in a few configurations (a cocircular quad triangulated differently in two periodic copies)
    checks = dict(contacts_3n_within_1=all(abs(x['contacts'] - 3 * x['alive']) <= 1 for x in rows), links=all(x['links_ok'] for x in rows))
    n_exact = sum(x['contacts_3n'] for x in rows); print(f'CONTACTS exactly 3N in {n_exact} of {len(rows)} configurations', flush=True)
    if TAG == 'calib':
        checks['lineage_equals_plain'] = all(x['plain'] is not None and x['plain'] == x['lin_lost'] + x['lin_made'] for x in rows)
        checks['D1_reproduces_3600'] = abs(summ[f'{640.0:g}']['lin_net'] - 3.600) <= 0.02
    json.dump(dict(tag=TAG, variant=VAR, N=N, reps=REPS, beta_per_s=beta, delta_per_s=delta, info=info, rows=rows, summary=summ,
                   checks=checks, n_exact_3n=n_exact, wall_s=time.time() - t0), open(OUT, 'w'), indent=1)
    print('CHECKS', checks, flush=True)
    print('FINAL ok' if all(checks.values()) else 'FINAL FAIL (' + ', '.join(k for k, v in checks.items() if not v) + ')', flush=True)
