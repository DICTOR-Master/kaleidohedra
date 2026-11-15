"""Foam rung 1 (dry 2D Potts froth; the frames saved by ../../pairing/scripts/foam_pairing.py, read only) with the macroscopic count
of ../../scripts/macro.py at sampling steps 1, 2, 4, 8 MCS. Rules fixed before the run (README, Macroscopic count): W = P = 8 MCS
(the main pairing rule), tau = 16 (main, 2W), also 8 and 32.
Usage: python foam_macro.py FRAMES.jsonl.gz OUT.json [max_frames]"""
import sys, os, json, gzip, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
import eventlog as EL, pairing as PR, macro as MA
src, out = sys.argv[1], sys.argv[2]; nmax = int(sys.argv[3]) if len(sys.argv) > 3 else None
W, P, TAUS, STEPS = 8, 8, [16, 8, 32], [1, 2, 4, 8]
t0 = time.time()
frames = []
for k, l in enumerate(gzip.open(src, 'rt')):
    if not l.strip(): continue
    if nmax and len(frames) >= nmax: break
    frames.append(EL.Tiling.from_json(l))
print(f'PROGRESS 0.05 frames read {len(frames)}', flush=True)
res = dict(source=os.path.basename(src), frames=len(frames), W=W, P=P, taus=TAUS, steps={})
for k, s in enumerate(STEPS):
    fr = frames[::s]
    data = PR.collect(fr)
    _, cev = MA.cell_events(fr)
    van, app = PR.vanished_appeared(fr)
    row = dict(vanished=van, appeared=app)
    for tau in TAUS:
        m = MA.macro_from(data, cev, W, P, tau, units='MCS')
        m['free_per_vanished'] = round(m['primary']['free'] / van, 4) if van else None
        m['ring_free_per_vanished'] = round(m['ring']['free'] / van, 4) if van else None
        row[f'tau={tau}'] = m
    res['steps'][s] = row
    print(f'PROGRESS {0.05 + 0.95 * (k + 1) / len(STEPS):.3f} step {s} done', flush=True)
res['seconds'] = round(time.time() - t0, 1)
json.dump(res, open(out, 'w'), indent=1, default=str)
for tau in TAUS:
    g = lambda s, f: res['steps'][s][f'tau={tau}']
    print(f'tau {tau}: swaps ' + ' / '.join(str(g(s, 0)['swaps']) for s in STEPS) +
          '; free ' + ' / '.join(str(g(s, 0)['primary']['free']) for s in STEPS) +
          '; free per vanished ' + ' / '.join(str(g(s, 0)['free_per_vanished']) for s in STEPS) +
          '; ring free per vanished ' + ' / '.join(str(g(s, 0)['ring_free_per_vanished']) for s in STEPS))
    for s in STEPS:
        pt = g(s, 0)['primary']['per_type']
        print(f'   step {s}: vanished {res["steps"][s]["vanished"]}; ' + '; '.join(
            f'{t}: {v["events"]} events, {v["attached_swaps"]} attached, {v["sides_shed_before_vanishing"]} shed' for t, v in sorted(pt.items())))
ok = all(r[k2][v]['identity_ok'] for r in res['steps'].values() for k2 in r if k2.startswith('tau=') for v in ('primary', 'ring'))
print('FOAM_MACRO_OK' if ok else 'FOAM_MACRO_FAIL')
