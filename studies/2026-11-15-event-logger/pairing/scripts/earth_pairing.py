"""Earth, Müller et al. 2016 (230 Ma to the present), with the pairing rules of ../../scripts/pairing.py at steps 1, 2, 5, 10 Myr.
Two readings of the same model, both made earlier and only READ here:
  vector: ../../results/plates/plates_series_muller2016_1_frames.jsonl (the event-logger Earth census; 33 of 231 frames fail a check);
  mesh:   ../../../2026-11-15-earth-plates/results/frames_muller2016_rigid_L0.jsonl (the 15 km mesh reading of the Earth-plates
          stream; every frame passes Euler; boundary lengths in km).
Coarser steps are subsamples of the 1 Myr frames (every 2nd, 5th, 10th frame; all include 230 Ma and the present).
Usage: python earth_pairing.py OUT.json        Time unit: Myr. Rule sets fixed before the run (README pairing section)."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts'))
import pairing as PR
SRC = dict(vector=os.path.join(HERE, '..', '..', 'results', 'plates', 'plates_series_muller2016_1_frames.jsonl'),
           mesh=os.path.join(HERE, '..', '..', '..', '2026-11-15-earth-plates', 'results', 'frames_muller2016_rigid_L0.jsonl'))
RULES = [(0, 0), (5, 5), (10, 10), (20, 20)]   # (W Myr, P Myr): main = (5, 5); (20, 20) added after the pilot
STEPS = [1, 2, 5, 10]
CASES = [('vector', False, 0), ('vector', True, 0), ('mesh', False, 0), ('mesh', True, 0), ('mesh', True, 150)]   # (reading, by_segment, tol km)
t0 = time.time(); out = dict(rules_fixed_in_advance=RULES, steps=STEPS, cases={})
k = 0
for src, byseg, tol in CASES:
    FL = PR.read_frames_with_lengths(SRC[src])
    frames, lens = [f for f, _ in FL], [l for _, l in FL]
    case = f'{src} by_segment={byseg} tol={tol}'; out['cases'][case] = {}
    for s in STEPS:
        fr, ln = frames[::s], lens[::s]
        span = abs(fr[-1].t - fr[0].t)
        data = PR.collect(fr, tol=tol, lengths=ln, by_segment=byseg)
        row = dict(frames=len(fr), span_myr=span)
        for Wr, Pr in RULES:
            _, sm = PR.apply_rules(data, Wr, Pr, units='Myr (tol: km)')
            sm['swaps_per_100myr'] = round(100 * sm['swaps'] / span, 2)
            row[f'W={Wr} P={Pr}'] = sm
        out['cases'][case][s] = row
        k += 1; print(f'PROGRESS {k / (len(CASES) * len(STEPS)):.3f} {case} step {s}', flush=True)
out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=str)
for case, rows in out['cases'].items():
    print(case)
    for Wr, Pr in RULES:
        key = f'W={Wr} P={Pr}'
        print(f'  {key}: swaps at steps ' + ' / '.join(str(rows[s][key]['swaps']) for s in STEPS) +
              '  per 100 Myr ' + ' / '.join(str(rows[s][key]['swaps_per_100myr']) for s in STEPS) +
              '  paired ' + ' / '.join(str(rows[s][key]['swaps_paired']) for s in STEPS) +
              '  halves left ' + ' / '.join(str(rows[s][key]['halves_left_lost'] + rows[s][key]['halves_left_gained']) for s in STEPS))
ok = all(r[k2]['balance_failures'] == 0 for rows in out['cases'].values() for r in rows.values() for k2 in r if k2.startswith('W='))
print('EARTH_OK' if ok else 'EARTH_FAIL')
