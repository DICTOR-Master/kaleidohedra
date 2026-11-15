"""Checks that decide FINAL ok for the validation jobs (predictions from README, written before the runs)."""
import json, sys, glob
what = sys.argv[1]; ok = True
if what == 'sweep':
    PRED = {'red': {'birth': 116, 'swap': 366, 'death': 116}, 'trunc120': {'birth': 716, 'swap': 966, 'death': 716},
            'bitruncated': {'birth': 716, 'swap': 2166, 'death': 716}}
    for st in ['red', 'trunc120', 'bitruncated', 'truncated']:
        for sd in (7, 11):
            d = json.load(open(f'sweep_{st}_{sd}.json')); s1 = d['steps']['1']
            good = s1['ok'] and d['neg_control_caught'] and (s1['counts'] == PRED[st] if st in PRED else 'swap' not in s1['counts'])
            print(st, sd, 'step1', s1['counts'], 'frames failing', s1['n_frames_failing'], 'balance failures', s1['n_balance_failures'],
                  'triple', s1['triple_formulas'], 'NEG', d['neg_control_caught'], 'OK' if good else 'MISMATCH')
            for s in ('2', '5'): print('   step', s, d['steps'][s]['counts'], 'ok', d['steps'][s]['ok'])
            ok &= good
elif what == 'sphere':
    for f in sorted(glob.glob('voronoi_*.json')):
        d = json.load(open(f)); runs = d['runs']; dts = sorted(runs, key=float)
        fine = [runs[k] for k in dts[:2]]
        same = fine[0]['logger']['counts'] == fine[1]['logger']['counts']
        good = same and all(r['logger_equals_flips'] and r['only_swap_birth_death'] and r['logger']['ok'] for r in fine) and \
            all(r['neg_control_caught'] in (True, None) for r in fine)
        if d['mode'] == 'voronoi': good &= all(set(r['logger']['counts']) <= {'swap'} for r in fine)
        for k in dts: print(f, 'dt', k, runs[k]['logger']['counts'], 'flips', runs[k]['flips'] if len(runs[k]['flips']) < 6 else f"{len(runs[k]['flips'])} kinds", 'agree', runs[k]['logger_equals_flips'])
        print(f, 'OK' if good else 'MISMATCH'); ok &= good
print('CHECKS', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
