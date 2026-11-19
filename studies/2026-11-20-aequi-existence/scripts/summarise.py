# Summary of study 2026-11-20-aequi-existence: per group, how many sets the reduction certifies, the bound used,
# the largest M/N, the smallest exclusion margin, the arithmetic margins, and the controls against study
# 2026-11-20-aequi-alexandrov. Writes data/verdicts.csv.
# usage: summarise.py results.jsonl controls.jsonl check-results.jsonl check-controls.jsonl verdicts.csv
import json, sys, csv, collections
R, C, KR, KC = [[json.loads(L) for L in open(f)] for f in sys.argv[1:5]]
K = {(k['kind'], k['name']): k for k in KR + KC}
ok = True
print('Main sets (exact existence by Alexandrov\'s condition):')
for kind, grp, want in [('main', 'Td', 3), ('main', 'T', 91), ('two', 'O', 31), ('two', 'Td', 91), ('two', 'T', 740)]:
    rs = [r for r in R if r['kind'] == kind and r['group'] == grp]
    h = [r for r in rs if r['verdict'] == 'holds']; b = collections.Counter(r['bound'] for r in h)
    mm = [r['min_margin'] for r in h if r['min_margin'] is not None]
    print('  %-4s %-3s sets %4d  holds %4d  undecided %3d  bounds %s  N %d..%d  max M/N %.4f  min margin %.4f  refined pairs %d'
          % (kind, grp, len(rs), len(h), len(rs) - len(h), dict(b), min(r['N'] for r in rs), max(r['N'] for r in rs),
             max(r['M'] / r['N'] for r in rs), min(mm) if mm else float('nan'), sum(r['refined'] for r in rs)))
    ok &= len(rs) == want
st = collections.defaultdict(list)
for r in R + C:
    for k, v in r['stats'].items(): st[k].append(v)
print('Arithmetic: largest |w.x| classed zero %.2e; smallest classed nonzero %.4f; smallest |cos| in half-circle counts %.2e; smallest |x_i x x_j| kept %.4f'
      % (max(st['zero_max']), min(st['nonzero_min']), min(st['semicircle_min']), min(st['min_cross'])))
print('Controls (study 2026-11-20-aequi-alexandrov, exhaustive):')
for kind, want in [('fail', 87), ('hold', 232), ('ctrl', 50)]:
    rs = [r for r in C if r['kind'] == kind]; c = collections.Counter(r['verdict'] for r in rs)
    print('  %-4s sets %3d  certified %3d  undecided %3d' % (kind, len(rs), c['holds'], c['undecided']))
    ok &= len(rs) == want
bad = [r for r in C if r['kind'] == 'fail' and r['verdict'] == 'holds']
conflict = [r for r in C if r['kind'] != 'fail' and r['verdict'] == 'holds' and not r['alex_verdict'].startswith('holds')]
print('  failing sets certified (must be 0):', len(bad), '| certified against the exhaustive verdict (must be 0):', len(conflict))
fw = [K[(r['kind'], r['name'])] for r in C if r['kind'] == 'fail']
print('  cap hunt finds a witness g >= 0 on %d of the 87 failing sets' % sum(1 for k in fw if k['g_max_caps'] is not None and k['g_max_caps'] >= -1e-12))
ok &= not bad and not conflict
chk = list(K.values())
print('Independent checks: M sampled > exact %d, M sampled = exact %d of %d; certified sets with a cap of g >= 0: %d; largest cap g on the main sets %.4f'
      % (sum(not k['M_ok'] for k in chk), sum(k['M_equal'] for k in chk), len(chk), sum(k['contradiction'] for k in chk),
         max(k['g_max_caps'] for k in KR if k['g_max_caps'] is not None)))
ok &= all(k['M_ok'] and not k['contradiction'] for k in chk)
with open(sys.argv[5], 'w', newline='') as fo:
    w = csv.writer(fo)
    w.writerow(['kind', 'group', 'name', 'label', 'N', 'M', 'verdict', 'bound', 'pairs', 'refined_pairs', 'min_margin',
                'M_sampled', 'g_max_caps', 'alexandrov_verdict'])
    for r in R + C:
        k = K[(r['kind'], r['name'])]
        w.writerow([r['kind'], r['group'], r['name'], r['label'], r['N'], r['M'], r['verdict'], r['bound'], r['pairs'],
                    r['refined'], '' if r['min_margin'] is None else '%.6f' % r['min_margin'], k['M_sampled'],
                    '' if k['g_max_caps'] is None else '%.6f' % k['g_max_caps'], r.get('alex_verdict', '')])
print('FINAL ok' if ok else 'FINAL FAIL')
