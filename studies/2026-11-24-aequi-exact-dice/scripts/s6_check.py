# The two S6 dice of Part 2(a) of study 2026-11-24-aequi-certify-extend whose two orbits sit at equal depth
# (D12/6 + D12p/6, sid 5169; I12/6 + I12p/6, sid 5170): are they shadow dice, face-transitive, or face-congruent? (double precision)
import json, gzip, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from groups import DIRS
from scan_shadow import corners
from symgroup import symgroup, orbits
D = json.load(gzip.open(os.path.join(HERE, '../../2026-11-24-aequi-certify-extend/data/aequi2a.json.gz')))['new']
for d in D:
    if d['sid'] not in (5169, 5170): continue
    U = DIRS[d['idx']]; G = symgroup(U)
    V, inc = corners(d['idx'], d['sizes'], np.array([1.0, 1.0])); Vn = V / np.linalg.norm(V, axis=1)[:, None]
    print(d['sid'], ' + '.join(d['orbit_labels']), 'depths', d['depths'], '| symmetry group of the normals: order', len(G), 'orbits', [len(o) for o in orbits(U, G)])
    print('  corners off the frame axes:', sum(np.abs(DIRS - v).max(1).min() > 1e-7 for v in Vn), 'of', len(V))
    for i in (0, 6):
        c = Vn[[v for v in range(len(V)) if i in inc[v]]]
        print('  face of orbit', 1 + i // 6, 'corner-pair cosines', np.round(sorted((c @ c.T)[np.triu_indices(len(c), 1)]), 5).tolist())
