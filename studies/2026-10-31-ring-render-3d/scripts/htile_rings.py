# Ring triangles of the HexOct h-tile at lambda = -1/8 (48 rings) -> JSON for ringmesh.py.
# Exact faces from studies/2026-10-31-hexoct-ring-build (build.py, exactfaces.py); the two orientations of ring triangles
# alternate across every tied side of a face, and the minority orientation counts as 'central' (turned over), as in
# studies/2026-10-31-ring-photo-render.  Usage (dicto-big-brother):
#   TILES_DIR=~/kres-tmp/endless RINGBUILD=~/k-research/studies/2026-10-31-hexoct-ring-build/scripts \
#   ~/geom/bin/python htile_rings.py out.json
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.expanduser(os.environ['TILES_DIR'])); sys.path.insert(0, os.path.expanduser(os.environ['RINGBUILD']))
import build as B, exactfaces as E
from tiles import tile

P = tile('AB', 0, B.LAM)[0]; faces = B.split_edges(E.union_faces([p[3] for p in P])); rings = []
allc = np.array([B.cart(p) for f in faces for p in f['loops'][0]]); cen = allc.mean(0)
for fi, f in enumerate(faces):
    n = B.cnormal(f); Ts = [[B.cart(p) for p in T] for T in B.rings_of(f)]
    fc = np.mean([B.cart(p) for p in f['loops'][0]], 0)
    c0 = np.mean(Ts[0], 0); u = Ts[0][0] - c0; u /= np.linalg.norm(u)
    cls = [any((p - np.mean(T, 0)) @ u / np.linalg.norm(p - np.mean(T, 0)) > 0.99 for p in T) for T in Ts]
    minority = sum(cls) * 2 < len(cls)
    for T, c in zip(Ts, cls):
        rings.append(dict(T=[list(map(float, p)) for p in T], n=list(map(float, n)), central=bool(c == minority), face=fi))
z0 = min(p[2] for r in rings for p in r['T'])
for r in rings: r['T'] = [[p[0] - cen[0], p[1] - cen[1], p[2] - z0] for p in r['T']]
json.dump(dict(rings=rings), open(sys.argv[1], 'w'))
print(len(faces), 'faces', len(rings), 'rings', sum(r['central'] for r in rings), 'central')
