# DICTO 2026-10-17 ("it's the long drawing, the line-up"): the stations at true scale in the Cleo star figure stopped at RT and skipped
# the DICTO Metaxyhexecontahedron M. Adds M to data/cleo-build.json's stations (from data/full-cycle.json st.G; same frame: RT checked).
import json, numpy as np
C = json.load(open('data/cleo-build.json')); J = json.load(open('data/full-cycle.json'))
rt = next(s for s in C['nine'] if s['name'] == 'RT'); a, b = np.array(rt['v']), np.array(J['st']['RT']['v'])
assert len(a) == len(b) and all(np.min(np.linalg.norm(b - x, axis=1)) < 1e-5 for x in a), 'frames differ'
C['nine'] = [s for s in C['nine'] if s['name'] != 'M']
i = next(k for k, s in enumerate(C['nine']) if s['name'] == 'RT') + 1
C['nine'].insert(i, {'name': 'M', 'v': J['st']['G']['v'], 'f': J['st']['G']['f']})
json.dump(C, open('data/cleo-build.json', 'w')); print('stations:', [s['name'] for s in C['nine']])
