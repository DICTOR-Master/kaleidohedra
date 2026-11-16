"""merge the per-family coverage sets into one cover instance file."""
import json
from common import *
B = load_base()
out = {'note': 'pentagon k of Q is dual to edge k of the 600-cell; sets[c] = pentagons covered whole '
               'by the fins of the dual of copy c (copies given by 600-cell corner ids, see s0_base)',
       'edges_of_600cell': B['edges'].tolist(), 'pentagons_as_Q_corners': B['pent'].tolist()}
for nm in ['A', 'B', 'C3']:
    d = json.load(open(f'data/dual_sets_{nm}.json'))
    out[nm] = {'copies_600cell_corner_ids': d['copies_600cell_corner_ids'], 'sets': d['sets']}
json.dump(out, open('data/dual_cover_instance.json', 'w'))
want = {'A': 120, 'B': 120, 'C3': 60}
ok = all(len(out[nm]['sets']) == want[nm] and all(len(x) == 60 for x in out[nm]['sets']) for nm in want)
print('FINAL ok' if ok else 'FINAL FAIL instance sizes (copies per family, 60 pentagons per copy)')
