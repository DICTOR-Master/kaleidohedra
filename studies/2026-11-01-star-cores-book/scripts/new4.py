# Star Cores book (2026-11-01): the star core treatment of #79 (star_core.treat, unchanged) for the four solids DICTO named on
# 31 October 2026 and added in DICTO Solids v7: D106 Cube Pearl, D107 Golden Clasp, D108 Hamlet, D109 Ophelia.
# Usage: python new4.py <dataset-v7 dir> <out dir> <star-cores scripts dir>
import sys, os, json
DS, OUT, SCR = sys.argv[1:4]
sys.argv = [sys.argv[0], DS, OUT]; sys.path.insert(0, SCR)
import star_core as SC
items = [('Cube Pearl', 'D106', 'solids/dicto-cube-pearl.json'), ('Golden Clasp', 'D107', 'solids/dicto-golden-clasp.json'),
         ('Hamlet', 'D108', 'solids/dicto-hamlet.json'), ('Ophelia', 'D109', 'solids/dicto-ophelia.json')]
os.makedirs(OUT, exist_ok=True); res = []
for it in items:
    r = SC.treat(it); res.append(r); print(r['D'], r['name'], '|', r['verdict'], flush=True)
json.dump(res, open(os.path.join(OUT, 'star-cores-new4.json'), 'w'), indent=1, default=float)
print('done')
