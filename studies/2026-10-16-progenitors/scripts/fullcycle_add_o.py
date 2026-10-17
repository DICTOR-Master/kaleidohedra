# DICTO 2026-10-17 ("there's one missing from the full cycle, should be 12"): the full-cycle figure drew the Ogdoecontahedron only at its
# compound size 9/4 (interlocked with H), not at its own station in the cycle (3φ²/4, on the Dharma ID). Adds that station to
# data/full-cycle.json as st.O, from data/nine-render.json (same frame and scale: its ID is the same set of corners, checked here).
import json, numpy as np
N = json.load(open('data/nine-render.json')); J = json.load(open('data/full-cycle.json'))
S = {s['name']: s for s in N['stations']}
a, b = np.array(S['ID']['v']), np.array(J['st']['ID']['v'])
assert len(a) == len(b) and all(np.min(np.linalg.norm(b - x, axis=1)) < 1e-5 for x in a), 'frames differ'
J['st']['O'] = {'v': S['O']['v'], 'f': S['O']['f']}
json.dump(J, open('data/full-cycle.json', 'w')); print('O added:', len(S['O']['v']), 'corners,', len(S['O']['f']), 'faces')
