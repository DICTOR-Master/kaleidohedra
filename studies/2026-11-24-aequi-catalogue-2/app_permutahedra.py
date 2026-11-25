# DICTO · the three Aequi Permutahedra into the picker (25 Nov 2026). With Claude (Anthropic).
# Nos. 1233-1235: the duals of the three permutahedra, fair by symmetry (one kind of face, every face carried to every other):
#   1233 TO-24   tetrakis hexahedron        (dual of the truncated octahedron, A3)      faces normal to the permutations of (0, 1, 2)
#   1234 TCO-48  disdyakis dodecahedron     (dual of the truncated cuboctahedron, B3)   normals: permutations of (1, 1 + sqrt2, 1 + 2 sqrt2)
#   1235 TID-120 disdyakis triacontahedron  (dual of the truncated icosidodecahedron, H3) normals: the 120 corners of the truncated
#                                            icosidodecahedron (even permutations of the five standard coordinate patterns)
# Each face's normal is a corner direction of the permutahedron; all faces at distance 1. Appends the new directions (with their images
# under the picker's two transforms x -> -x and the quarter turn about z), one orbit each to Oh / Ih, and the three dice (s = 'P').
# Usage: python app_permutahedra.py <k-mix dir>
import sys, json, itertools, os
import numpy as np
KM = sys.argv[1]
data = json.load(open(os.path.join(KM, 'aequi/dice.json')))
assert not any(e.get('s') == 'P' for e in data['dice']), 'already added'
r2, ph = 2 ** 0.5, (1 + 5 ** 0.5) / 2
def signs_perms(v, even=False):
    out = set()
    for p in itertools.permutations(range(3)):
        if even and p not in ((0, 1, 2), (1, 2, 0), (2, 0, 1)): continue
        for s in itertools.product((1, -1), repeat=3):
            out.add(tuple(round(s[i] * v[p[i]], 12) for i in range(3)))
    return out
TO = signs_perms((0, 1, 2))
TCO = signs_perms((1, 1 + r2, 1 + 2 * r2))
TID = set()
for v in [(1 / ph, 1 / ph, 3 + ph), (2 / ph, ph, 1 + 2 * ph), (1 / ph, ph ** 2, 3 * ph - 1), (2 * ph - 1, 2, 2 + ph), (ph, 3, 2 * ph)]:
    TID |= signs_perms(v, even=True)
assert (len(TO), len(TCO), len(TID)) == (24, 48, 120), (len(TO), len(TCO), len(TID))
dirs = [np.array(v) for v in data['dirs']]
def index_of(u):
    u = np.array(u, float); u = u / np.linalg.norm(u)
    for k, w in enumerate(dirs):
        if np.abs(w - u).max() < 1e-9: return k
    dirs.append(u); return len(dirs) - 1
orbits = {}
for key, S in (('TO24', TO), ('TCO48', TCO), ('TID120', TID)): orbits[key] = sorted(index_of(v) for v in S)
# transforms for the new directions
def img(k, f):
    u = f(dirs[k]); j = next((i for i, w in enumerate(dirs) if np.abs(w - u).max() < 1e-9), None)
    return j if j is not None else k
n0 = len(data['PM'])
for k in range(n0, len(dirs)):
    data['PM'].append(img(k, lambda u: np.array([-u[0], u[1], u[2]])))
    data['PQ'].append(img(k, lambda u: np.array([-u[1], u[0], u[2]])))
data['dirs'] = [[round(float(x), 15) for x in w] for w in dirs]
P = [(1233, 'Oh', 'TO24', 'TO-24 · tetrakis hexahedron (dual of the truncated octahedron)', 14),
     (1234, 'Oh', 'TCO48', 'TCO-48 · disdyakis dodecahedron (dual of the truncated cuboctahedron)', 26),
     (1235, 'Ih', 'TID120', 'TID-120 · disdyakis triacontahedron (dual of the truncated icosidodecahedron)', 62)]
for no, g, key, plain, c in P:
    data['groups'][g].append({'lab': key, 'plain': plain, 'col': 'C' if g == 'Oh' else 'I', 'dirs': orbits[key]})
    N = len(orbits[key])
    data['dice'].append({'g': g, 'o': [len(data['groups'][g]) - 1], 'd': [1.0], 'm': 1, 'N': N, 'h': 0, 'c': c, 'f': ['%d×3-gon' % N],
                         's': 'P', 'no': no, 'name': 'Aequus ' + plain.split(' · ')[0] + ', ' + g})
json.dump(data, open(os.path.join(KM, 'aequi/dice.json'), 'w'), separators=(',', ':'))
ok = len(data['dirs']) == len(data['PM']) == len(data['PQ']) and sum(e.get('s') == 'P' for e in data['dice']) == 3
print('directions', len(data['dirs']), 'dice', len(data['dice']), {k: len(v) for k, v in orbits.items()})
print('FINAL ok' if ok else 'FINAL FAIL')
