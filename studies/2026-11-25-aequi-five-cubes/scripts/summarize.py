# Certification summary (copy of summarize2a.py of study 2026-11-24-aequi-certify-extend; file names changed)
import json, collections, math
R = [json.loads(L) for L in open('data/certify.jsonl')]; A = json.load(open('data/accidental.json')); S = json.load(open('data/structural.json'))
st = collections.Counter(r['status'] for r in R)
ok_acc = sum(a['split_krawczyk'].get('ok') and a['tight'].get('ok') and a.get('orthants', 0) == a.get('regions_expected', 0) for a in A)
wide = [r['wide']['r'] for r in R if r.get('wide')] + [a['split_krawczyk']['r'] for a in A]
h = collections.Counter('1e-%d' % round(-math.log10(x)) for x in wide)
print('dice', len(R), '| certified on a box of constant type:', st['certified'], '(of which orbits split by frame maps:', sum(1 for r in R if r.get('orbits_split_by_frame_maps')), ') | split box:', ok_acc, 'of', len(A))
print('tight: max |K - x~| %.1e' % max(r['tight']['dev'] for r in R if r.get('tight')))
print('uniqueness half-widths:', ', '.join('%s: %d' % kv for kv in sorted(h.items(), key=lambda kv: -float(kv[0]))))
print('structural corners: dice', S['dice_with_structural_corners'], 'checks', S['distinct_checks'], 'failures', S['failures'])
for a in A: print('split:', a['sid'], a['label'], 'walls', a.get('n_hyperplanes', 1), 'regions', a.get('orthants', 2), 'box ±%g' % a['split_krawczyk']['r'], ('h = ' + ' '.join(x[:12] for x in a['h'])) if a.get('one_hyperplane') else '')
ok = st['certified'] + ok_acc == len(R) and S['failures'] == 0
print('FINAL ok' if ok else 'FINAL FAIL')
