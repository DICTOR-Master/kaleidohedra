"""Resolution check: the same scheme (half-axis options + centre) must give the same pieces and outcome at N = 4 and N = 6.
Usage: python compare.py a.json b.json"""
import sys, json
A, B = [json.load(open(f)) for f in sys.argv[1:3]]
key = lambda r: (r['cut'], tuple(r['half']), r['centre'])
a = {key(r): (r['outcome'], r['pieces_per_card']) for r in A['results']}; b = {key(r): (r['outcome'], r['pieces_per_card']) for r in B['results']}
diff = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
print('N=%d: %d schemes; N=%d: %d schemes; differing: %d' % (A['N'], len(a), B['N'], len(b), len(diff)))
for k in diff[:10]: print('  ', k, a.get(k), b.get(k))
print('FINAL ok' if not diff else 'FINAL FAIL')
