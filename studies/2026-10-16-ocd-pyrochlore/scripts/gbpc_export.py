# Fable, GBPC pass 4 (2026-10-16): export the exact geometry of G' (Q(sqrt5) numbers as "a|b" = a + b*sqrt5) so the search engine
# (gbpc_search.py, numpy + fractions only) can run on dicto-node. Also exports the five Bodhi pieces exactly (block coordinates p + q*phi
# from studies/2026-10-12-bodhi-pieces/data/bodhi-B*-raw.json, faces as vertex triples).
import sys, io, os, contextlib, itertools, json, re, numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
os.environ['FAST'] = '1'
lines = open(os.path.join(HERE, 'gbpc_tiling.py')).read().split('\n')
with contextlib.redirect_stdout(io.StringIO()):
    exec('\n'.join(lines[:199]))
enc = lambda x: f'{x.a}|{x.b}'; encv = lambda v: [enc(x) for x in v]
phi = Q(Fr(1, 2), Fr(1, 2))
faces = []   # ordered icosahedron faces (three mutually adjacent vertices), all 6 orderings: the 120 elements of I_h acting on a block basis
for i, j, k in itertools.combinations(range(12), 3):
    if all(p in adj for p in [(i, j), (i, k), (j, k)]):
        for o in itertools.permutations((i, j, k)): faces.append([encv(ICO[t]) for t in o])
assert len(faces) == 120
def parse(sx):
    s = re.sub(r'(\d+)', r'Q(\1)', sx)
    s = re.sub(r'\)φ', r')*P', s).replace('φ', 'P')
    return eval(s, {'P': phi, 'Q': Q})
BD = '/home/dicto/kaleidohedra/studies/2026-10-12-bodhi-pieces/data'
bodhi = {}
for b, nm in [('B1', 'Vajra (fine)'), ('B2', 'Chatra'), ('B3', 'Mudra'), ('B4', 'Crown Jewel'), ('B5', 'Diadem')]:
    d = json.load(open(f'{BD}/bodhi-{b}-raw.json'))
    st = [[parse(x) for x in c] for c in d['blockCoordinates']]
    assert all(abs(sum(x.f() for x in c) - 0) >= 0 for c in st)
    # exact volume in block units: sum over faces of det / 6 relative to the centroid-ish first corner (faces are outward triangles of a convex hull)
    bodhi[b] = {'name': nm, 'block': [encv(c) for c in st], 'faces': d['faces']}
out = {'mark': 'DICTO · dictospheres.com', 'LB': [encv(v) for v in LB], 'RT': [encv(v) for v in RT['V']], 'RT_H': [[encv(n), enc(dd)] for n, dd in RT['H']],
       'corners': [encv(p) for p in CORN], 'AX5': [encv(v) for v in AX['5']], 'AX3': [encv(v) for v in AX['3']], 'AX2': [encv(v) for v in AX['2']],
       'faces': faces, 'bodhi': bodhi, 'cellv': enc(cellv), 'GP_volume': enc(cellv - (pvol(RT) - Q(4) * Q(Fr(-704, 729), Fr(320, 729))))}
json.dump(out, open(os.path.join(STUDY, 'data', 'gbpc-geom-exact.json'), 'w'))
print('exported', len(CORN), 'corners;', len(faces), 'face frames;', list(bodhi))
