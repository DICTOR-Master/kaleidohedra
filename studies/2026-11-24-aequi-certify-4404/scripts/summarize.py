# Counts of the certification of the 4404 (certify.py, accidental.py, structural.py of study 2026-11-24-aequi-certify-extend).
# FINAL ok only if every die is certified: status certified (constant type on the box, tight Krawczyk ok, symmetry ok),
# or status accidental with the split-box Krawczyk test ok; and the structural corners are all proved exactly.
import json, sys, os, collections
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
dice = json.load(open(os.path.join(D, 'dice4404.json')))
import gzip; cert = [json.loads(L) for L in gzip.open(os.path.join(D, 'certify4404.jsonl.gz'), 'rt')]
acc = json.load(open(os.path.join(D, 'accidental4404.json'))) if os.path.exists(os.path.join(D, 'accidental4404.json')) else []
st = json.load(open(os.path.join(D, 'structural4404.json')))
by = {c['sid']: c for c in cert}; accok = {a['sid'] for a in acc if a['split_krawczyk'].get('ok') and a['tight'].get('ok') and a.get('orthants', 0) == a.get('regions_expected', 0)}
print('dice', len(dice), 'certify records', len(cert), 'distinct', len(by))
print('status', dict(collections.Counter(c['status'] for c in cert)))
bad = [d['sid'] for d in dice if d['sid'] not in by or not (by[d['sid']]['status'] == 'certified' or (by[d['sid']]['status'] == 'accidental' and d['sid'] in accok))]
lab = all(by[d['sid']]['label'] == d['label'] and by[d['sid']]['N'] == d['N'] for d in dice if d['sid'] in by)
ce = [c for c in cert if c['status'] == 'certified']
print('symmetry ok', sum(c['symmetry_ok'] for c in ce), '| graph ok', sum(c['graph_ok'] for c in ce), '| split by frame maps', sum('orbits_split_by_frame_maps' in c for c in cert))
print('tight max |K - x~|: %.2g' % max(c['tight']['dev'] for c in ce), '| max |F(x~)|: %.2g' % max(c['tight']['fres'] for c in ce))
print('uniqueness half-widths', dict(sorted(collections.Counter('%.0e' % c['wide']['r'] if c['wide'] else 'none' for c in ce).items(), reverse=True)))
print('split box (accidental):', len(acc), 'ok', len(accok), [(a['sid'], a.get('label')) for a in acc])
grp = collections.Counter(d['group'] for d in dice if d['sid'] not in bad)
print('certified by group', dict(sorted(grp.items())))
print('structural corners: dice', st['dice_with_structural_corners'], 'distinct checks', st['distinct_checks'], 'failures', st['failures'])
print('not certified', len(bad), bad[:20])
print('FINAL ok' if len(dice) == 4404 and len(by) == len(cert) == 4404 and lab and not bad and st['failures'] == 0 else 'NOT all certified')
