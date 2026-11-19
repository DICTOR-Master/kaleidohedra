# Summary table and checks for the Alexandrov test of the 319 polar orbit sets and the 50 controls.
# usage: summarise.py alex.jsonl confirm.jsonl verdicts.csv
import json, sys, csv, numpy as np
from collections import Counter
R = [json.loads(L) for L in open(sys.argv[1])]
C = {(o['kind'], o['cls'], o['m'], tuple(o['subset'])): o for o in map(json.loads, open(sys.argv[2]))}
key = lambda r: (r['kind'], r['cls'], r['m'], tuple(r['subset']))
with open(sys.argv[3], 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['kind', 'class', 'group', 'm', 'orbits', 'orbit_sizes', 'N', 'condition', 'verdict', 'witness_dirs', 'witness_size',
                'witness_hull_vertices', 'witness_perimeter_L', 'mu_omega', 'sigma_omega_halfpi', 'g=2pi(2|A|-N)/N-L',
                'die_depths_first_orbit_1', 'die_depth_ratio_max', 'die_80_digits', 'die_centroid_offset'])
    for r in R:
        c = C.get(key(r), {})
        die = [x[:14] for x in c['depths60']] if c.get('exact_ok') else ''
        w.writerow([r['kind'], r['cls'], r['group'], r['m'], ' + '.join('+'.join(F) for F in r['fams']), r['sizes'], r['N'],
                    r['condition'], r['verdict'], r['witness_dirs'] if r['condition'] == 'fails' else '', r['witness_size'] if r['condition'] == 'fails' else '',
                    r['witness_hull_vertices'] if r['condition'] == 'fails' else '', r['witness_perimeter'] if r['condition'] == 'fails' else '',
                    r['mu_hull'] if r['condition'] == 'fails' else '', r['sigma_hull_halfpi'] if r['condition'] == 'fails' else '', r['g'],
                    ' '.join(die), round(c['depth_ratio_max'], 6) if c.get('exact_ok') else '', bool(c.get('exact_ok')),
                    '%.3g' % c['centroid_offset'] if c.get('exact_ok') else ''])
nos = [r for r in R if r['kind'] == 'nosol']; ctl = [r for r in R if r['kind'] == 'control']
print('319 polar sets with no die in the study box:', len(nos))
print('  condition fails:', sum(r['condition'] == 'fails' for r in nos), '(of which with equality:', sum(r['equality'] for r in nos), ')')
print('  condition holds:', sum(r['condition'] == 'holds' for r in nos), '| die found and confirmed to 80 digits:',
      sum(r['condition'] == 'holds' and C.get(key(r), {}).get('exact_ok', False) for r in nos))
print('  by class (fails, holds):', sorted(Counter((r['cls'], r['group'], r['condition']) for r in nos).items()))
fl = [r for r in nos if r['condition'] == 'fails']
print('  fails: smallest g', min(float(r['g']) for r in fl), '| witness sizes', sorted(Counter((r['witness_size'], r['N']) for r in fl).items()))
print('  fails: die-finder grid minimiser runs to the bound |psi| = 25:', sum(r['die_finder']['grid_at_bound'] for r in fl), 'of', len(fl))
hl = [r for r in nos if r['condition'] == 'holds']
print('  holds: largest g (exhaustive over all subsets)', max(float(r['g']) for r in hl))
rat = [C[key(r)]['depth_ratio_max'] for r in hl if key(r) in C]
print('  holds: largest depth ratio of the die from %.3f to %.3f (study search box e^1.5 = %.3f)' % (min(rat), max(rat), np.exp(1.5)))
off = [C[key(r)]['centroid_offset'] for r in hl if key(r) in C]
print('  holds: centroid offset / volume^(1/3) from %.3g to %.3g (none at the centre: none is an Aequus)' % (min(off), max(off)))
dev = []
for r in ctl:
    d = np.array(r['die_finder']['die']['depths']) if r['die_finder']['die'] else None
    s = np.array(r['study_sols'][0])
    dev.append(np.abs(d / s - 1).max() if d is not None else np.inf)
print('50 controls: condition holds', sum(r['condition'] == 'holds' for r in ctl), '| largest g', max(float(r['g']) for r in ctl),
      '| die found', sum(r['die_finder']['die'] is not None for r in ctl), '| confirmed to 80 digits', sum(C.get(key(r), {}).get('exact_ok', False) for r in ctl),
      '| largest relative depth difference from the study die %.2g' % max(dev))
ok = (len(nos) == 319 and len(ctl) == 50 and all(r['exhaustive'] for r in R) and not any(r['verdict'] in ('CONFLICT', 'undecided') for r in R)
      and all(r['condition'] == 'holds' for r in ctl) and max(dev) < 1e-9
      and all(C.get(key(r), {}).get('exact_ok', False) for r in R if r['condition'] == 'holds')
      and all(r['hull_exact'] for r in fl))
print('FINAL ok' if ok else 'FINAL FAIL: see the lines above')
