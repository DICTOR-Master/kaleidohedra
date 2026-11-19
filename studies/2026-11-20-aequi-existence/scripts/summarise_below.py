# Part 2 summary of study 2026-11-20-aequi-existence: the dice below the frame groups without opposite pairs. Per group:
# sets, N, largest M/N, certified, undecided, the bound used, the smallest exclusion margin; the arithmetic margins;
# the controls rerun with the same script (must match Part 1's controls.jsonl verdict for verdict, and certify none of
# the 87 failing polar sets); the independent checks. Writes data/verdicts-below.csv.
# usage: summarise_below.py results-below.jsonl check-below.jsonl controls-rerun.jsonl controls.jsonl verdicts-below.csv
import json, sys, csv, collections
R, K, C2, C1 = [[json.loads(L) for L in open(f)] for f in sys.argv[1:5]]
K = {(k['kind'], k['name']): k for k in K}
ok = len(R) == 1300 and len(K) == 1300
print('Dice below the frame groups without opposite pairs (exact existence by Alexandrov\'s condition):')
groups = sorted(set(r['group'] for r in R), key=lambda g: -sum(r['group'] == g for r in R))
tot = collections.Counter()
for g in groups:
    rs = [r for r in R if r['group'] == g]; h = [r for r in rs if r['verdict'] == 'holds']
    b = collections.Counter(r['bound'] for r in h); mm = [r['min_margin'] for r in h if r['min_margin'] is not None]
    print('  %-4s sets %4d  holds %4d  undecided %3d  bounds %s  N %d..%d  max M/N %.4f  min margin %s  refined pairs %d'
          % (g, len(rs), len(h), len(rs) - len(h), dict(b), min(r['N'] for r in rs), max(r['N'] for r in rs),
             max(r['M'] / r['N'] for r in rs), '%.4f' % min(mm) if mm else '-', sum(r['refined'] for r in rs)))
    tot['sets'] += len(rs); tot['holds'] += len(h)
print('  all  sets %4d  holds %4d  undecided %3d' % (tot['sets'], tot['holds'], tot['sets'] - tot['holds']))
und = [r for r in R if r['verdict'] != 'holds']
print('Undecided:', len(und), [(r['group'], r['name'], r['N']) for r in und])
mm = [r for r in R if r['min_margin'] is not None]; w = min(mm, key=lambda r: r['min_margin'])
print('Smallest margin %.4f on %s (%s, N %d, M %d)' % (w['min_margin'], w['name'], w['group'], w['N'], w['M']))
hm = [r for r in R if r['min_margin'] is None]
print('Sets with no live pair (every lens holds at most N/2):', len(hm), sorted(set((r['group'], r['N'], r['M']) for r in hm)))
st = collections.defaultdict(list)
for r in R + C2:
    for k, v in r['stats'].items(): st[k].append(v)
print('Arithmetic: largest |w.x| classed zero %.2e; smallest classed nonzero %.4f; smallest |cos| in half-circle counts %.2e; smallest |x_i x x_j| kept %.4f'
      % (max(st['zero_max']), min(st['nonzero_min']), min(st['semicircle_min']), min(st['min_cross'])))
print('Controls rerun (study 2026-11-20-aequi-alexandrov, exhaustive):')
for kind, want in [('fail', 87), ('hold', 232), ('ctrl', 50)]:
    rs = [r for r in C2 if r['kind'] == kind]; c = collections.Counter(r['verdict'] for r in rs)
    print('  %-4s sets %3d  certified %3d  undecided %3d' % (kind, len(rs), c['holds'], c['undecided']))
    ok &= len(rs) == want
bad = [r for r in C2 if r['kind'] == 'fail' and r['verdict'] == 'holds']
conflict = [r for r in C2 if r['kind'] != 'fail' and r['verdict'] == 'holds' and not r['alex_verdict'].startswith('holds')]
v1 = {(r['kind'], r['name']): (r['verdict'], r['M'], r['min_margin']) for r in C1}
same = sum(v1.get((r['kind'], r['name'])) == (r['verdict'], r['M'], r['min_margin']) for r in C2)
print('  failing sets certified (must be 0): %d | certified against the exhaustive verdict (must be 0): %d | same as Part 1: %d of %d'
      % (len(bad), len(conflict), same, len(C2)))
ok &= not bad and not conflict and same == len(C2) == len(C1)
chk = list(K.values())
print('Independent checks: M sampled > exact %d, M sampled = exact %d of %d; certified sets with a cap of g >= 0: %d; largest cap g %.4f'
      % (sum(not k['M_ok'] for k in chk), sum(k['M_equal'] for k in chk), len(chk), sum(k['contradiction'] for k in chk),
         max(k['g_max_caps'] for k in chk if k['g_max_caps'] is not None)))
ok &= all(k['M_ok'] and not k['contradiction'] for k in chk)
with open(sys.argv[5], 'w', newline='') as fo:
    wr = csv.writer(fo)
    wr.writerow(['group', 'name', 'label', 'N', 'M', 'verdict', 'bound', 'pairs', 'refined_pairs', 'min_margin', 'M_sampled', 'g_max_caps'])
    for r in R:
        k = K[(r['kind'], r['name'])]
        wr.writerow([r['group'], r['name'], r['label'], r['N'], r['M'], r['verdict'], r['bound'], r['pairs'], r['refined'],
                     '' if r['min_margin'] is None else '%.6f' % r['min_margin'], k['M_sampled'],
                     '' if k['g_max_caps'] is None else '%.6f' % k['g_max_caps']])
print('FINAL ok' if ok else 'FINAL FAIL')
