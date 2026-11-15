"""Earth, Müller et al. 2016 (230 Ma to the present), macroscopic count of ../../scripts/macro.py at steps 1, 2, 5, 10 Myr. The two
readings used by ../../pairing/scripts/earth_pairing.py, read only: vector (per pair) and mesh (15 km, per boundary).
Rules fixed before the run (README, Macroscopic count): W = P = 5 Myr (the main pairing rule), tau = 10 Myr (main, 2W), also 5 and 20.
Usage: python earth_macro.py OUT.json"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
import pairing as PR, macro as MA
SRC = dict(vector=os.path.join(HERE, '..', '..', 'results', 'plates', 'plates_series_muller2016_1_frames.jsonl'),
           mesh=os.path.join(HERE, '..', '..', '..', '2026-11-15-earth-plates', 'results', 'frames_muller2016_rigid_L0.jsonl'))
W, P, TAUS, STEPS = 5, 5, [10, 5, 20], [1, 2, 5, 10]
CASES = [('vector', False), ('mesh', True)]
t0 = time.time(); out = dict(W=W, P=P, taus=TAUS, steps=STEPS, cases={}); k = 0
for src, byseg in CASES:
    FL = PR.read_frames_with_lengths(SRC[src]); frames = [f for f, _ in FL]
    case = f'{src} by_segment={byseg}'; out['cases'][case] = {}
    for s in STEPS:
        fr = frames[::s]; span = abs(fr[-1].t - fr[0].t)
        data = PR.collect(fr, by_segment=byseg); _, cev = MA.cell_events(fr, by_segment=byseg)
        row = dict(frames=len(fr), span_myr=span)
        for tau in TAUS:
            m = MA.macro_from(data, cev, W, P, tau, units='Myr')
            m['swaps_per_100myr'] = round(100 * m['swaps'] / span, 2)
            m['free_per_100myr'] = round(100 * m['primary']['free'] / span, 2)
            m['ring_free_per_100myr'] = round(100 * m['ring']['free'] / span, 2)
            row[f'tau={tau}'] = m
        out['cases'][case][s] = row
        k += 1; print(f'PROGRESS {k / (len(CASES) * len(STEPS)):.3f} {case} step {s}', flush=True)
out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=str)
for case, rows in out['cases'].items():
    print(case)
    for tau in TAUS:
        g = lambda s: rows[s][f'tau={tau}']
        print(f'  tau {tau}: swaps ' + ' / '.join(str(g(s)['swaps']) for s in STEPS) + '; free ' +
              ' / '.join(str(g(s)['primary']['free']) for s in STEPS) + ' (per 100 Myr ' +
              ' / '.join(str(g(s)['free_per_100myr']) for s in STEPS) + '); ring free ' +
              ' / '.join(str(g(s)['ring']['free']) for s in STEPS))
        for s in STEPS:
            pt = g(s)['primary']['per_type']
            print(f'     step {s}: ' + '; '.join(f'{t}: {v["events"]} ev, {v["attached_swaps"]} att' for t, v in sorted(pt.items())))
ok = all(r[k2][v]['identity_ok'] for rows in out['cases'].values() for r in rows.values() for k2 in r if k2.startswith('tau=')
         for v in ('primary', 'ring'))
print('EARTH_MACRO_OK' if ok else 'EARTH_MACRO_FAIL')
