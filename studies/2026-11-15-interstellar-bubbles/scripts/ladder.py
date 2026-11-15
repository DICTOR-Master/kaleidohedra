"""Foam ladder census: one rung -> tiling sequence -> shared event logger at time steps 1, 2, 4 -> results JSON.
Usage: python ladder.py RUNG OUT.json [key=value ...]
RUNG: dry2d (rung 1), wet2d (rung 2), dry3d (rung 3), births2d (rung 4), ism2d (rung 5, toy).
Prints PROGRESS <fraction> lines and LADDER_OK / LADDER_FAIL at the end."""
import sys, os, json, time, hashlib
import numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
LOGGER = os.path.join(HERE, '..', '..', '2026-11-15-event-logger', 'scripts')
sys.path.insert(0, LOGGER); sys.path.insert(0, HERE)
import eventlog as EL
import tiles, potts, ism_toy
from scipy import ndimage as ndi

rung, out = sys.argv[1], sys.argv[2]
P = dict(a.split('=', 1) for a in sys.argv[3:])
g = lambda k, d: type(d)(P.get(k, d))
seed = g('seed', 1); rng = np.random.default_rng(seed)
t_start = time.time()


def frame2d(lab, t, parents=None, heirs=None):
    G = tiles.graph(lab)
    T = tiles.to_tiling(EL.Tiling, lab, G, t, parents, heirs)
    jdeg = Counter(len(c) for c, _ in G['junctions'])
    ncell = len(T.cells)
    stat = dict(t=t, cells=ncell, euler=tiles.torus_euler(ncell, G), loops=G['loops'], odd=G['odd'],
                junction_degrees={str(k): v for k, v in jdeg.items()},
                mean_neighbours=float(np.mean([len(T.nb[c]) for c in T.cells])) if ncell else 0.0)
    return T, stat


def frame3d(lab, t):
    C = tiles.graph3(lab)
    T = tiles.to_tiling3(EL.Tiling, lab, C, t)
    stat = dict(t=t, cells=len(T.cells), mean_neighbours=float(np.mean([len(T.nb[c]) for c in T.cells])))
    return T, stat


def wet_to_tiling(lab):
    """Tiling rule for a wet foam: every liquid pixel (label 0) joins the nearest bubble (periodic Euclidean distance)."""
    pad = 32
    t = np.pad(lab, pad, mode='wrap')
    _, ind = ndi.distance_transform_edt(t == 0, return_indices=True)
    full = t[tuple(ind)]
    sl = tuple(slice(pad, pad + n) for n in lab.shape)
    return full[sl]


frames, stats, extra = [], [], {}
if rung in ('dry2d', 'wet2d', 'births2d', 'dry3d'):
    d3 = rung == 'dry3d'
    L = g('L', 48 if d3 else 256); N = g('N', 800 if d3 else 2000); Tm = g('T', 0.5 if d3 else 0.3)
    mcs = g('mcs', 400 if d3 else 2000); rec = g('rec', 2); burn = g('burn', 20)
    shape = (L,) * (3 if d3 else 2)
    lab = potts.voronoi_labels(shape, N, rng)
    Jbl = None
    if rung == 'wet2d':
        phi = g('phi', 0.15); Jbl = g('Jbl', 0.6)
        # liquid = pixels near cell boundaries, grown until the liquid fraction reaches phi
        liq = np.zeros(shape, bool)
        for ax in range(2):
            for s in (1, -1): liq |= np.roll(lab, s, ax) != lab
        while liq.mean() < phi: liq = ndi.binary_dilation(liq) | liq
        lab[liq] = 0
    sim = potts.Potts(lab, T=Tm, Jbl=Jbl, rng=rng, nmax=N + 1 + g('nuc_max', 20000))
    if rung == 'wet2d':
        sim.lam[0] = g('lam0', 0.005); sim.target[0] = phi * lab.size
        extra['liquid_fraction'] = []
    next_label = N + 1; births_injected = 0; nuc = []
    total = burn + mcs
    for step in range(total):
        sim.sweep()
        if rung == 'births2d' and step >= burn:
            # gas-fed bubbles: supply grows the target area for t_supply MCS, then stops (lam -> 0, free coarsening)
            for (lb, t0) in nuc:
                age = step - t0
                if age < g('t_supply', 100): sim.target[lb] = g('a0', 28.0) + g('growth', 2.0) * age
                else: sim.lam[lb] = 0.0
            nuc = [(lb, t0) for lb, t0 in nuc if step - t0 < g('t_supply', 100)]
        if step >= burn and (step - burn) % rec == 0:
            protect = 0 if rung == 'wet2d' else None
            sim.lab, moved = tiles.clean_fragments(sim.lab, protect=protect)
            if rung == 'births2d':
                k = rng.poisson(g('nuc_rate', 3.0))
                if k:
                    G = tiles.graph(sim.lab); J = [cs for cs, _ in G['junctions'] if len(cs) == 3]
                    r0 = g('r0', 3.0)
                    for _ in range(min(k, len(J))):
                        # nucleate at a random triple junction (a Plateau border, where bubbles meet)
                        cs = J[rng.integers(len(J))]
                        near = np.ones(shape, bool)
                        for c in cs:
                            mc = sim.lab == c
                            near &= mc | np.roll(mc, 1, 0) | np.roll(mc, -1, 0) | np.roll(mc, 1, 1) | np.roll(mc, -1, 1)
                        pts = np.argwhere(near)
                        if not len(pts): continue
                        cy, cx = pts[0]
                        Y, X = np.ogrid[:L, :L]
                        dy = (Y - cy + L / 2) % L - L / 2; dx = (X - cx + L / 2) % L - L / 2
                        disc = dy ** 2 + dx ** 2 <= r0 ** 2
                        sim.grow(next_label + 1)
                        sim.lab[disc] = next_label; sim.lam[next_label] = g('lam_b', 0.05); sim.target[next_label] = disc.sum()
                        nuc.append((next_label, step)); next_label += 1; births_injected += 1
                    sim.lab, m2 = tiles.clean_fragments(sim.lab); moved += m2
            if d3:
                T, st = frame3d(sim.lab, step)
            else:
                tl = wet_to_tiling(sim.lab) if rung == 'wet2d' else sim.lab
                if rung == 'wet2d':
                    extra['liquid_fraction'].append(float((sim.lab == 0).mean()))
                    tl, m3 = tiles.clean_fragments(tl); moved += m3
                T, st = frame2d(tl, step)
            st['fragment_pixels_moved'] = moved
            frames.append(T); stats.append(st)
        if step % max(1, total // 50) == 0: print(f'PROGRESS {step / total:.3f} {rung} mcs {step} cells {len(np.unique(sim.lab))}', flush=True)
    extra['births_injected'] = births_injected
    params = dict(L=L, N=N, T=Tm, mcs=mcs, rec=rec, burn=burn, seed=seed)
    params.update({k: v for k, v in P.items()})
elif rung == 'ism2d':
    L = g('L', 256); dt = g('dt', 1.0); span = g('span', 60.0); burn = int(g('burn', 30.0) / dt); nfr = int(round(span / dt))
    theta = g('theta', 0.05); amin = g('amin', 4)
    gas = ism_toy.BubbleGas(L=L, rate=g('rate', 8.0), rmed=g('rmed', 5.0), f_cluster=g('fc', 0.2), seed=seed)
    prev, next_id, hotf = None, 1, []
    for k in range(burn + nfr):
        gas.advance(dt)
        if k < burn: continue
        rho, hot = gas.density(); hotf.append(float(hot.mean()))
        raw = ism_toy.cells_from_density(rho, theta, amin, tiles)
        if raw is None: continue
        if prev is None:
            lab = raw; next_id = int(raw.max()) + 1; par = her = None
        else:
            lab, par, her, next_id = tiles.match(prev, raw, next_id)
        lab, moved = tiles.clean_fragments(lab)
        T, st = frame2d(lab, round(k * dt, 6), par, her); st['fragment_pixels_moved'] = moved
        frames.append(T); stats.append(st); prev = lab
        if k % 20 == 0: print(f'PROGRESS {(k - burn) / nfr:.3f} ism2d frame {k} cells {st["cells"]} hot {hotf[-1]:.2f}', flush=True)
    extra['hot_filling_factor_mean'] = float(np.mean(hotf))
    params = dict(L=L, frames=nfr, dt=dt, span=span, burn=burn, theta=theta, amin=amin, seed=seed); params.update(P)
else:
    sys.exit(f'unknown rung {rung}')


def census(fr):
    rows, summ = EL.run(fr)
    died_sides = Counter()
    for A, B in zip(fr, fr[1:]):
        for c in A.cells - B.cells: died_sides[len(A.nb[c])] += 1
    born = sum(len(B.cells - A.cells) for A, B in zip(fr, fr[1:]))
    died = sum(died_sides.values())
    cnt = summ['counts']
    sw = cnt.get('swap', 0) + cnt.get('contact gained', 0) + cnt.get('contact lost', 0)
    # negative control: retype the first cell-changing event as a swap; the balance must catch it
    neg = None
    by = {}
    for r in rows: by.setdefault((r['t0'], r['t1']), []).append(r)
    for A, B in zip(fr, fr[1:]):
        ev = by.get((A.t, B.t), [])
        if any(e['net'] for e in ev):
            bad = [dict(e) for e in ev]; i = next(i for i, e in enumerate(bad) if e['net']); bad[i]['type'] = 'swap'
            neg = not EL.balance(A, B, bad)[0]; break
    return dict(counts=cnt, clump_patterns=dict(Counter(summ['clump_patterns']).most_common(12)),
                n_balance_failures=summ['n_balance_failures'], n_frames_failing_logger=summ['n_frames_failing'],
                cells_vanished=died, cells_appeared=born, vanished_by_sides=dict(sorted(died_sides.items())),
                swaps_or_contact_changes=sw, swaps_per_vanished=(sw / died if died else None),
                swaps_per_appeared=(sw / born if born else None), neg_control_caught=neg)


res = dict(rung=rung, params=params, frames=len(frames), extra=extra,
           logger_md5=hashlib.md5(open(os.path.join(LOGGER, 'eventlog.py'), 'rb').read()).hexdigest())
for k in (1, 2, 4):
    res[f'step{k}'] = census(frames[::k])
    print(f'PROGRESS {0.9 + 0.03 * k:.3f} census step {k}', flush=True)
if stats and 'euler' in stats[0]:
    res['euler_failures'] = sum(s['euler'] != 0 for s in stats)
    # an island cell (closed loop boundary, no junction) adds 1 to V - E + F on the torus; with islands allowed the check is V - E + F = loops
    res['euler_failures_islands_allowed'] = sum(s['euler'] != s['loops'] for s in stats)
    res['island_loops_mean'] = float(np.mean([s['loops'] for s in stats]))
    res['frames_with_nontriple_junctions'] = sum(any(k != '3' for k in s['junction_degrees']) for s in stats)
res['cells_first_last'] = [stats[0]['cells'], stats[-1]['cells']] if stats else None
res['mean_neighbours_first_last'] = [stats[0]['mean_neighbours'], stats[-1]['mean_neighbours']] if stats else None
res['frame_stats_every10'] = stats[::10]
res['seconds'] = round(time.time() - t_start, 1)
json.dump(res, open(out, 'w'), indent=1, default=str)
s1 = res['step1']
ok = s1['n_balance_failures'] == 0 and (s1['neg_control_caught'] in (True, None)) and len(frames) > 10
print(json.dumps({k: res[k] for k in ('rung', 'frames', 'seconds', 'cells_first_last', 'mean_neighbours_first_last')}))
print(json.dumps(dict(step1=s1['counts'], step2=res['step2']['counts'], step4=res['step4']['counts'],
                      vanished_by_sides=s1['vanished_by_sides'], swaps_per_vanished=s1['swaps_per_vanished'],
                      euler_failures=res.get('euler_failures'), euler_fail_islands_ok=res.get('euler_failures_islands_allowed'), balance_failures=s1['n_balance_failures'])))
print('LADDER_OK' if ok else 'LADDER_FAIL')
