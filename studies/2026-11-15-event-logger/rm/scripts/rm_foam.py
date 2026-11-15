"""Foam rung 1 (dry 2D Potts froth) with the Rutenberg-McCurdy count of ../../scripts/rm_count.py at sampling steps 1, 2, 4, 8 MCS.
The saved frames (../../pairing/results/foam_sN_frames.jsonl.gz) carry no cell areas, and rule RM needs them. So the simulation is
regenerated from its seed with the code of ../../pairing/scripts/foam_pairing.py (copied unchanged in substance: same potts.py and
tiles.py, same parameters, same order of random draws), and every regenerated frame is compared with the saved line (string
equality). Only when all compared frames are identical are the areas used. Areas = pixel counts per cell after clean_fragments.
Rules fixed before the run (README, Rutenberg-McCurdy count): counted swaps W = P = 8 MCS (main pairing rule) and W = P = 0 (the
logger's swaps); RM rc = 1 pixel (main), also 0.5 and 2; box = L^2.
Usage: python rm_foam.py SAVED_FRAMES.jsonl.gz OUT.json seed=1 [mcs=1500]"""
import sys, os, json, gzip, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
LOGGER = os.path.join(HERE, '..', '..', 'scripts')
FOAM = os.path.join(HERE, '..', '..', '..', '2026-11-15-interstellar-bubbles', 'scripts')
sys.path.insert(0, LOGGER); sys.path.insert(0, FOAM)
import eventlog as EL, pairing as PR, rm_count as RC
import tiles, potts

src, out = sys.argv[1], sys.argv[2]
P_ = dict(a.split('=', 1) for a in sys.argv[3:])
g = lambda k, d: type(d)(P_.get(k, d))
seed = g('seed', 1); rng = np.random.default_rng(seed)
L, N, Tm, mcs, burn = g('L', 256), g('N', 2000), g('T', 0.3), g('mcs', 1500), g('burn', 20)
RULES = [(8, 8), (0, 0)]; RCS = (1.0, 0.5, 2.0); STEPS = [1, 2, 4, 8]
t0 = time.time()
saved = gzip.open(src, 'rt')
# ---- simulation copied from foam_pairing.py (frames kept in memory instead of written; areas added) ----
lab = potts.voronoi_labels((L, L), N, rng)
sim = potts.Potts(lab, T=Tm, Jbl=None, rng=rng, nmax=N + 1 + 20000)
total = burn + mcs
frames, areas, same, diff = [], [], 0, 0
for step in range(total):
    sim.sweep()
    if step >= burn:
        sim.lab, moved = tiles.clean_fragments(sim.lab)
        G = tiles.graph(sim.lab)
        T = tiles.to_tiling(EL.Tiling, sim.lab, G, step)
        d = json.loads(T.to_json())
        d['lengths'] = {f'{a}|{b}': [int(v)] for (a, b), v in G['contacts'].items()}
        d['torus_euler'] = int(tiles.torus_euler(len(T.cells), G)); d['loops'] = int(G['loops'])
        line = json.dumps(d) + '\n'
        ref = saved.readline()
        if line == ref: same += 1
        else: diff += 1
        frames.append(EL.Tiling.from_json(line))
        u, c = np.unique(sim.lab, return_counts=True)
        areas.append({str(int(a)): float(n) for a, n in zip(u, c)})
    if step % max(1, total // 50) == 0:
        print(f'PROGRESS {0.5 * step / total:.3f} sim mcs {step} cells {len(frames[-1].cells) if frames else N}; identical {same}, different {diff}', flush=True)
# ---- end of copied part ----
print(f'regenerated {len(frames)} frames in {time.time() - t0:.0f} s: identical to saved {same}, different {diff}', flush=True)
assert all(set(a) == F.cells for a, F in zip(areas, frames)), 'area labels differ from frame cells'
box = float(L * L)
res = dict(params=dict(seed=seed, L=L, N=N, T=Tm, mcs=mcs, burn=burn, rules=RULES, rcs=RCS), frames=len(frames),
           regenerated_identical=same, regenerated_different=diff, cells_first_last=[len(frames[0].cells), len(frames[-1].cells)], steps={})
k = 0
for s in STEPS:
    fr, ar = frames[::s], areas[::s]
    data = PR.collect(fr)
    res['steps'][s] = {}
    for W, P in RULES:
        res['steps'][s][f'W={W} P={P}'] = RC.rm_count(fr, data, W, P, areas=ar, box=box, rcs=RCS, units='MCS (rc: pixels)')
    k += 1; print(f'PROGRESS {0.5 + 0.5 * k / len(STEPS):.3f} step {s} done', flush=True)
res['seconds'] = round(time.time() - t0, 1)
json.dump(res, open(out, 'w'), indent=1, default=str)
for W, P in RULES:
    key = f'W={W} P={P}'; r = lambda s: res['steps'][s][key]
    print(f'{key}: vanished ' + ' / '.join(str(r(s)['vanished']) for s in STEPS) + '; swaps ' + ' / '.join(str(r(s)['swaps']) for s in STEPS))
    for lab_, f in (('total per vanished', lambda x: x['per_vanished']['total']), ('SS macroscopic per vanished', lambda x: x['per_vanished']['SS_macroscopic']),
                    ('SS side-shedding per vanished', lambda x: x['per_vanished']['SS_side_shedding']),
                    ('SS_any macroscopic per vanished', lambda x: x['per_vanished']['SS_any_macroscopic'])):
        print(f'   {lab_}: ' + ' / '.join(str(f(r(s))) for s in STEPS))
    for rc in RCS:
        print(f'   RM rc {rc} macroscopic per vanished: ' + ' / '.join(str(r(s)['RM'][str(rc)]['macroscopic_per_vanished']) for s in STEPS)
              + f'; l^2 first/last {r(1)["RM"][str(rc)]["ell2_first_last"]}; sides at l^2 (step 1) {r(1)["RM"][str(rc)]["sides_at_ell2"]}')
    print('   shed-to-vanish delay quartiles (MCS): ' + ' / '.join(str(r(s)['SS']['shed_to_vanish_delay_quartiles']) for s in STEPS))
ok = diff == 0 and same == len(frames) and all(r['SS']['identity_ok'] for st in res['steps'].values() for r in st.values())
print('RM_FOAM_OK' if ok else 'RM_FOAM_FAIL')
