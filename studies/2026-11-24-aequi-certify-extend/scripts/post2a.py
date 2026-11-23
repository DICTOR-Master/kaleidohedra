# Part 2(a) after the search: classify (collect.py, as in the earlier studies), then split the Aequi into
# (i) dice whose full group contains T (their orbit sets are T orbit sets: met in study 2026-11-20-aequi-two-placements
#     or 2026-11-19-aequi-complete, so repeats), (ii) the rest: compared by congruence (scale-free plane distances and
#     corner distances, mirror images included) with the 4553 of study 2026-11-19-aequi-complete of the same N, group
#     and corner count; new ones are written to data/dice2a-new.json for certification (certify.py with DICE=...).
# usage: post2a.py collected.json [PREFIX]   (outputs data/counts<P>.md, data/dice<P>-new.json, data/aequi<P>.json; default 2a)
import json, sys, os, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from groups import DIRS
from exact import combinatorics, centroid
col = json.load(open(sys.argv[1])); dice = col['dice']; P = sys.argv[2] if len(sys.argv) > 2 else '2a'
aeq = [d for d in dice if d['centroid_at_origin'] and not d['face_transitive']]
withT = {'Oh', 'O', 'Td', 'Th', 'T', 'Ih', 'I'}
def sig(idx, sizes, dep):
    D = np.repeat(dep, sizes); Nrm = DIRS[idx]; V, inc, trip, faces = combinatorics(Nrm, D); cen, vol = centroid(V, faces, Nrm, D)
    s = vol ** (1 / 3); return np.r_[np.sort((D - Nrm @ cen) / s), np.sort(np.linalg.norm(V - cen, axis=1) / s)], len(V)
old = {}
for f in glob.glob(os.path.join(os.path.dirname(__file__), '..', '..', '2026-11-19-aequi-complete', 'data', 'dice', '*.json')):
    d = json.load(open(f)); old.setdefault((d['N'], d['group'], d['corners']), []).append(d)
new, rep_T, rep_old = [], [], []
for d in aeq:
    if d['group'] in withT: rep_T.append(d); continue
    cands = old.get((d['N'], d['group'], d['corners']), [])
    sv, _ = sig(d['idx'], d['sizes'], d['depths']); hit = None
    for o in cands:
        so, _ = sig(o['face_directions'], o['orbit_sizes'], [float(x) for x in o['depths_60_digits']])
        if len(so) == len(sv) and np.abs(so - sv).max() < 1e-6: hit = o; break
    (rep_old if hit else new).append(d)
from collections import Counter
print('Aequi found', len(aeq), '| full group contains T (repeats: met under their own group in study 2026-11-19-aequi-complete or 2026-11-20-aequi-two-placements):', len(rep_T), dict(Counter(d['group'] for d in rep_T)))
print('congruent to a die of study 2026-11-19-aequi-complete:', len(rep_old), '| NEW:', len(new))
tab = Counter((d['group'], d['m']) for d in new)
gs = sorted({g for g, m in tab}, key=lambda g: -max(d['sym_order'] for d in new if d['group'] == g)); ms = sorted({m for g, m in tab})
L = ['| group | ' + ' | '.join('m=%d' % m for m in ms) + ' | total |', '|---|' + '---|' * (len(ms) + 1)]
for g in gs: L.append('| %s | ' % g + ' | '.join(str(tab.get((g, m), '')) for m in ms) + ' | %d |' % sum(tab[(g, m)] for m in ms))
L.append('| all | ' + ' | '.join(str(sum(tab[(g, m)] for g in gs)) for m in ms) + ' | %d |' % len(new))
print('\n'.join(L)); open('data/counts%s.md' % P, 'w').write('\n'.join(L) + '\n')
recs = [dict(study='2026-11-24-part' + P, sid=i, file='', label=d['group'] + ': ' + ' + '.join(d['orbit_labels']), group=d['group'], m=d['m'], N=d['N'],
             sizes=d['sizes'], idx=d['idx'], depths=['1.0'] + ['%.17g' % x for x in d['depths'][1:]], corners=d['corners'], refine=True)
        for i, d in enumerate(new)]
json.dump(recs, open('data/dice%s-new.json' % P, 'w'))
json.dump(dict(new=new, repeats_T=len(rep_T), repeats_old=[(d['group'], d['N']) for d in rep_old]), open('data/aequi%s.json' % P, 'w'))
print('FINAL ok' if len(aeq) == len(rep_T) + len(rep_old) + len(new) else 'FINAL FAIL: dice lost in the split')
