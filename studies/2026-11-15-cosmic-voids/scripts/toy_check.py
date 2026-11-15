"""Check toy results. Generic runs: no simultaneous events, no clumps, all frame checks pass. A file named *lattice* is the negative
control: it must show simultaneous events (degenerate passage through the cubic lattice). Usage: toy_check.py RESULT.json ..."""
import sys, json
ok = True
for p in sys.argv[1:]:
    s = json.load(open(p))['summary']
    sim = s['stats'].get('simultaneous', 0); cl = s['counts'].get('clump', 0)
    checks = s['euler_fail'] == 0 and s['balance_fail'] == 0 and s['stats'].get('margin_fail', 0) == 0
    if 'lattice' in p: good = sim > 0 and cl > 0; role = 'NEGATIVE CONTROL (simultaneous events expected)'
    else: good = checks and sim == 0 and cl == 0 and s['robust_fail'] == 0; role = 'generic'
    print(p, role, 'counts', s['counts'], 'simultaneous', sim, 'euler/robust/balance/margin fails', s['euler_fail'], s['robust_fail'],
          s['balance_fail'], s['stats'].get('margin_fail', 0), 'mean contacts', round(s['mean_contacts_per_cell'], 3), 'lives', s['lives'],
          'coarse', s['coarse'], 'PASS' if good else 'FAIL')
    ok &= good
sys.exit(0 if ok else 1)
