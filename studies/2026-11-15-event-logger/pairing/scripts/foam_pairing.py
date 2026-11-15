"""Foam ladder rung 1 (dry 2D froth, cellular Potts) with the pairing rules of ../../scripts/pairing.py.
The simulation is the dry2d branch of studies/2026-11-15-interstellar-bubbles/scripts/ladder.py, copied unchanged in substance
(same potts.py and tiles.py, imported from there; same parameters and seeds as the pilot runs r1_dry2d_s1 / _s2), with two
additions: every frame is saved (JSON lines, gzip) with its boundary lengths (pixel edges per touching pair), and the census
applies the rules at sampling steps 1, 2, 4 and 8 MCS.
Usage: python foam_pairing.py OUT_PREFIX seed=1 [mcs=1500 T=0.3 L=256 N=2000]
Time unit: MCS (Monte Carlo sweeps). Rule sets fixed before the run (see README pairing section)."""
import sys, os, json, gzip, time
import numpy as np
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
LOGGER = os.path.join(HERE, '..', '..', 'scripts')
FOAM = os.path.join(HERE, '..', '..', '..', '2026-11-15-interstellar-bubbles', 'scripts')
sys.path.insert(0, LOGGER); sys.path.insert(0, FOAM)
import eventlog as EL, pairing as PR
import tiles, potts

out = sys.argv[1]
P_ = dict(a.split('=', 1) for a in sys.argv[2:])
g = lambda k, d: type(d)(P_.get(k, d))
seed = g('seed', 1); rng = np.random.default_rng(seed)
L, N, Tm, mcs, burn = g('L', 256), g('N', 2000), g('T', 0.3), g('mcs', 1500), g('burn', 20)
RULES = [(0, 0, 0), (8, 8, 0), (16, 16, 0), (8, 8, 2), (32, 32, 0)]   # (W MCS, P MCS, tol pixel edges): main = (8, 8, 0); (32, 32, 0) added after the pilot
STEPS = [1, 2, 4, 8]
t0 = time.time()
fpath = out + '_frames.jsonl.gz'
if not os.path.exists(fpath):
    lab = potts.voronoi_labels((L, L), N, rng)
    sim = potts.Potts(lab, T=Tm, Jbl=None, rng=rng, nmax=N + 1 + 20000)
    total = burn + mcs; moved_total = 0
    with gzip.open(fpath + '.part', 'wt') as f:
        for step in range(total):
            sim.sweep()
            if step >= burn:
                sim.lab, moved = tiles.clean_fragments(sim.lab); moved_total += moved
                G = tiles.graph(sim.lab)
                T = tiles.to_tiling(EL.Tiling, sim.lab, G, step)
                d = json.loads(T.to_json())
                d['lengths'] = {f'{a}|{b}': [int(v)] for (a, b), v in G['contacts'].items()}
                d['torus_euler'] = int(tiles.torus_euler(len(T.cells), G)); d['loops'] = int(G['loops'])
                f.write(json.dumps(d) + '\n')
            if step % max(1, total // 50) == 0:
                print(f'PROGRESS {0.6 * step / total:.3f} sim mcs {step} cells {len(np.unique(sim.lab))}', flush=True)
    os.replace(fpath + '.part', fpath)
    print(f'simulated in {time.time() - t0:.0f} s; fragment pixels moved {moved_total}', flush=True)

lines = [l for l in gzip.open(fpath, 'rt') if l.strip()]
frames, lens = [], []
for l in lines:
    d = json.loads(l)
    frames.append(EL.Tiling.from_json(l))
    lens.append({tuple(sorted(p.split('|'))): v for p, v in d['lengths'].items()})
euler_fail = sum(json.loads(l)['torus_euler'] != json.loads(l)['loops'] for l in lines)
res = dict(params=dict(seed=seed, L=L, N=N, T=Tm, mcs=mcs, burn=burn), frames=len(frames), rules_fixed_in_advance=RULES,
           euler_fail_islands_allowed=euler_fail, cells_first_last=[len(frames[0].cells), len(frames[-1].cells)], steps={})
ns = len(STEPS) * len(set(r[2] for r in RULES)); k = 0
for s in STEPS:
    fr, ln = frames[::s], lens[::s]
    van, app = PR.vanished_appeared(fr)
    res['steps'][s] = dict(cells_vanished=van, cells_appeared=app, rules={})
    for tol in sorted(set(r[2] for r in RULES)):
        data = PR.collect(fr, tol=tol, lengths=ln)
        for Wr, Pr, tr in RULES:
            if tr != tol: continue
            _, sm = PR.apply_rules(data, Wr, Pr, units='MCS (tol: pixel edges)')
            sm['swaps_per_vanished'] = sm['swaps'] / van if van else None
            res['steps'][s]['rules'][f'W={Wr} P={Pr} tol={tr}'] = sm
        k += 1; print(f'PROGRESS {0.6 + 0.4 * k / ns:.3f} census step {s} tol {tol}', flush=True)
res['seconds'] = round(time.time() - t0, 1)
json.dump(res, open(out + '.json', 'w'), indent=1, default=str)
print('swaps per vanished cell (rows: rule; columns: step ' + ' / '.join(map(str, STEPS)) + ')')
for Wr, Pr, tr in RULES:
    key = f'W={Wr} P={Pr} tol={tr}'
    print(key, ' / '.join(f"{res['steps'][s]['rules'][key]['swaps_per_vanished']:.3f}" for s in STEPS),
          ' swaps', ' / '.join(str(res['steps'][s]['rules'][key]['swaps']) for s in STEPS),
          ' halves left', ' / '.join(str(res['steps'][s]['rules'][key]['halves_left_lost'] + res['steps'][s]['rules'][key]['halves_left_gained']) for s in STEPS))
ok = all(r['balance_failures'] == 0 for st in res['steps'].values() for r in st['rules'].values()) and len(frames) > 10
print('FOAM_OK' if ok else 'FOAM_FAIL')
