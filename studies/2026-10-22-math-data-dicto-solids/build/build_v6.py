# DICTO · dictospheres.com — math-data dataset VERSION 6 builder (2026-10-30). Created by DICTO. Licence CC BY-SA 4.0.
# Adds the solids of paper #78, The Truncated Icosahedron Star (TI Star), in Q(sqrt5), with DICTO's D-numbers (30 October 2026):
#   D103 Golden TI Star: the truncated icosahedron TI with a pyramid on every face, tip at phi times the foot of the perpendicular from
#        the centre to the face (non-convex, 92 corners, 180 triangles); the doubling form (tip at 2 x the foot) is the same
#        construction with 2 in place of phi and is not a separate D-number;
#   D104 Star Halo (DICTO's name): the convex hull of the 32 tips (a non-Catalan pentakis dodecahedron, 32 corners, 60 triangles);
#   D105 the TI Star core: the intersection of the icosahedron of the 12 pentagon tips and the dodecahedron of the 20 hexagon tips,
#        the icosahedron truncated at 1/phi^3 of each edge (60 corners, 12 pentagons, 20 hexagons, edge ratio sqrt5).
# Frame: the twelve-station golden cycle of #54 (the icosahedron I of edge 1/phi; TI = its station 7, exact corners from
# studies/2026-10-25-gnomon-shapes/stations-exact.json, copied to sources/stations-exact-54.json). Everything exact (exactlib).
import json, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *
SRC = os.path.join(HERE, 'sources'); SOL = os.path.join(HERE, '..', 'solids')
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True); return ok
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).', 'version_added': 6}
D78 = '10.5281/zenodo.23782577'
def emit(slug, meta, V, F, published):
    V, F = canon(V, F)
    meta = dict(meta, **COMMON); meta['published_values'] = published
    r = write_solid(os.path.join(SOL, slug), meta, V, F)
    for k, v in published.items():
        if k == 'f_vector': log((r['V'], r['E'], r['F']) == tuple(v), f"{slug}: f-vector {(r['V'], r['E'], r['F'])} vs published {tuple(v)}")
        elif k == 'faces_by_sides': log({str(a): b for a, b in r['fk'].items()} == v, f"{slug}: faces {r['fk']} vs published {v}")
    log(True, f"{slug}: {r['V']}, {r['E']}, {r['F']} {dict(sorted(r['fk'].items()))}, volume {fmt(r['vol'])}, symmetry {r['cls']} ({r['order']})")
    return V, F, r

raw = json.load(open(os.path.join(SRC, 'stations-exact-54.json')))
TI = [tuple(QF(Fr(a), Fr(b), 5) for a, b in v) for v in raw['TI']]
V, F = hull(TI)
log(len(V) == 60 and len(F) == 32, f'TI from #54: {len(V)} corners, {len(F)} faces')
O = (Q(0), Q(0), Q(0))
def foot(f):
    n = cross(sub(V[f[1]], V[f[0]]), sub(V[f[2]], V[f[0]])); return mul(dot(n, V[f[0]]) / dot(n, n), n)
feet = [foot(f) for f in F]
tips = [mul(PHI, p) for p in feet]
vol = lambda VV, FF: volume(VV, FF)
volTI = volume(V, F)

# D103 the Golden TI Star: TI's corners and the 32 tips; each face of TI replaced by the side triangles of its spike
SV = list(V) + tips; SF = []
for fi, f in enumerate(F):
    t = len(V) + fi
    for i in range(len(f)):
        a, b = f[i], f[(i + 1) % len(f)]
        tri = [a, b, t]
        n = cross(sub(SV[b], SV[a]), sub(SV[t], SV[a])); m = mul(Q(Fr(1, 3)), add(add(SV[a], SV[b]), SV[t]))
        if dot(n, sub(m, feet[fi])).sign() < 0: tri = [b, a, t]   # outward: away from the centre of the face below
        SF.append(tri)
log(volume(SV, SF) == volTI * PHI, 'Golden TI Star volume = phi * TI exactly')
emit('dicto-golden-ti-star', {'name': 'Golden TI Star', 'finding': '', 'paper': '#78 The Truncated Icosahedron Star (TI Star)', 'dicto_doi': D78,
      'status': 'new (the truncated icosahedron with its own face pyramids turned outwards at height 1/phi of the inward ones; not found in the sources checked, #78)',
      'convex': False, 'symmetry_label': 'auto',
      'scale_note': 'frame of #54: the icosahedron I of edge 1/phi; TI = station 7; tips at phi x the feet of the perpendiculars to TI\'s faces',
      'source': {'app': 'study', 'path': 'research:studies/2026-10-30-spiked-ti', 'id': None}},
     SV, SF, {'f_vector': [92, 270, 180], 'faces_by_sides': {'3': 180}})

# D104 Star Halo: the hull of the 32 tips
HV, HF = hull(tips)
emit('dicto-star-halo', {'name': 'Star Halo', 'finding': '', 'paper': '#78 The Truncated Icosahedron Star (TI Star)', 'dicto_doi': D78,
      'status': 'new (the hull of the TI Star\'s tips; a pentakis dodecahedron, not the Catalan one: the five-fold corners stand out 1.0265 x the six-fold ones; DICTO\'s name; #78)',
      'convex': True, 'symmetry_label': 'auto',
      'scale_note': 'frame of #54; the hull of the Golden TI Star\'s 32 tips (the shape is the same for every spike factor)',
      'source': {'app': 'study', 'path': 'research:studies/2026-10-30-spiked-ti', 'id': None}},
     HV, HF, {'f_vector': [32, 90, 60], 'faces_by_sides': {'3': 60}})

# D105 the TI Star core: icosahedron of the pentagon tips ∩ dodecahedron of the hexagon tips
pen = [tips[i] for i, f in enumerate(F) if len(f) == 5]; hexa = [tips[i] for i, f in enumerate(F) if len(f) == 6]
IP, IPF = hull(pen); DH, DHF = hull(hexa)
CV, CF = halfspace_solid(face_planes(IP, IPF) + face_planes(DH, DHF))
el = sorted({dot(sub(CV[a], CV[b]), sub(CV[a], CV[b])) for a, b in edges_of(CF)}, key=lambda q: q.f())
log(len(el) == 2 and el[1] == el[0] * Q(5), f'core edges: two lengths, ratio^2 exactly 5 ({[fmt(x) for x in el]})')
emit('dicto-ti-star-core', {'name': 'TI Star core', 'finding': '', 'paper': '#78 The Truncated Icosahedron Star (TI Star)', 'dicto_doi': D78,
      'status': 'new as a station (the icosahedron truncated at 1/phi^3 of each edge, hexagon edges in the ratio sqrt5; the core of every turn of the TI Star cycles and the polar partner of the Star Halo; #78).',
      'convex': True, 'symmetry_label': 'auto',
      'scale_note': 'frame of #54; the intersection of the icosahedron of the Golden TI Star\'s 12 pentagon tips and the dodecahedron of its 20 hexagon tips',
      'source': {'app': 'study', 'path': 'research:studies/2026-10-30-spiked-ti', 'id': None}},
     CV, CF, {'f_vector': [60, 90, 32], 'faces_by_sides': {'5': 12, '6': 20}})
json.dump(LOG, open(os.path.join(HERE, 'build_v6.log.json'), 'w'), indent=1)
print('FAILS:', sum(1 for l in LOG if l.startswith('FAIL')))
