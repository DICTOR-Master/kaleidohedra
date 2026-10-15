# The core (DICTO's choice, 2026-10-16): the cycle repeats inward. Turn t is the whole faithful nest with the great stellated
# dodecahedron (step 5) scaled by phi^(-3t); turn t+1's outer dodecahedron is exactly turn t's inner one (closure phi^3, exact),
# so the turns fill each other with no gap. Render data for three turns, innermost dodecahedron solid.
import json, numpy as np
p = (1 + 5 ** .5) / 2
J = json.load(open('data/polar-gsd-render.json'))
def sc(S, s): return {'v': (np.array(S['v']) * s).tolist(), 'f': S['f'], 'c': (np.array(S['c']) * s).tolist()}
layers = []
TURNS = 5                                           # turns 0..4 (DICTO: render the infinite core twice more)
for t in range(TURNS):
    s = p ** (-3 * t)
    for L in J['layers']: layers.append({'name': f'turn {t}: {L["name"]}', 'pieces': [sc(S, s) for S in L['pieces']]})
D0 = np.array(J['core']['v']); Dout = np.array(J['outer']['v'])
assert abs(np.linalg.norm(Dout, axis=1).max() / p ** 3 - np.linalg.norm(D0, axis=1).max()) < 1e-9   # outer / phi^3 = inner
json.dump({'layers': layers, 'core': sc(J['core'], p ** (-3 * (TURNS - 1))), 'nlay': len(J['layers'])}, open('data/polar-turns-render.json', 'w'))
print(len(layers), 'layers,', sum(len(L['pieces']) for L in layers), 'pieces')
