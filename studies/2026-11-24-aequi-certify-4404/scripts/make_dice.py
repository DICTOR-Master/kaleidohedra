# Input list for certification: the dice of study 2026-11-19-aequi-complete whose full symmetry group does not
# contain T (the 4553 minus the 149 frame-group dice, which are among the 1232 certified in Part 1 of study
# 2026-11-24-aequi-certify-extend). Same record format as load_all() in that study's certify.py.
import json, glob, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.normpath(os.path.join(HERE, '..', '..'))
WITH_T = {'Oh', 'O', 'Td', 'Th', 'T', 'Ih', 'I'}
study = '2026-11-19-aequi-complete'; recs = []; allc = 0
for f in sorted(glob.glob(os.path.join(ST, study, 'data', 'dice', '*.json'))):
    d = json.load(open(f)); allc += 1
    if d['group'] in WITH_T: continue
    recs.append(dict(study=study, sid=d['sid'], file=os.path.basename(f), label=d['label'], group=d['group'], m=d['m'], N=d['N'],
                     sizes=d['orbit_sizes'], idx=d['face_directions'], depths=d['depths_60_digits'], corners=d['corners']))
assert allc == 4553 and len(recs) == 4404 and len({r['sid'] for r in recs}) == 4404
json.dump(recs, open(os.path.join(HERE, '..', 'data', 'dice4404.json'), 'w'))
print('dice', len(recs), dict(sorted(collections.Counter(r['group'] for r in recs).items())))
