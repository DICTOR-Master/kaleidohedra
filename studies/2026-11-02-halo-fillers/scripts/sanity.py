# Sanity checks (DICTO 2026-11-02): (1) face counts of the hulls used by the screens equal the census counts; (2) the edge test on
# classical solids (fillers must pass, the rhombic triacontahedron and other non-fillers must fail) and on the 22 known census halos.
import json, os, sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import screen as S, screen2 as S2
cen = json.load(open(os.path.join(S.HC, 'census.json'))); out = dict(face_count_mismatch=[], classical={}, known_halos={})
for r in cen:
    if 'halo' not in r['part']: continue
    s = json.load(open(os.path.join(S.HC, 'shapes', r['slug'] + '.json')))[r['part']]
    F = S2.hull_faces(s['points'])
    if len(F) != r['faces']: out['face_count_mismatch'].append([r['placeholder'], len(F), r['faces']])
    if r['status'] != 'NEW':
        A = S.classes(S.dihedrals(s['points'])); out['known_halos'][str(r['placeholder'] or r['part']) + ' of ' + r['slug'] + ' = ' + str(((r['matches'] or []) + (r['same_as'] or []) + [''])[0])] = S.test(A, [a for a, n in A])[0]
phi = (1 + 5 ** .5) / 2; perm = S.perm
cyc = lambda v: {(a, b, c) for x in [v] for (a, b, c) in [(x[0], x[1], x[2]), (x[1], x[2], x[0]), (x[2], x[0], x[1])]}
sg = lambda v: {(a * s0, b * s1, c * s2) for (a, b, c) in [v] for s0 in (1, -1) for s1 in (1, -1) for s2 in (1, -1)}
evenperm = lambda v: set().union(*[sg(w) for w in cyc(v)])
ico = evenperm((0, 1, phi)); dod = evenperm((1, 1, 1)) | evenperm((0, 1 / phi, phi))
CL = {'cube (fills)': perm((1, 1, 1)), 'rhombic dodecahedron (fills)': perm((1, 1, 1)) | perm((2, 0, 0)), 'truncated octahedron (fills)': perm((0, 1, 2)),
      'rhombic triacontahedron (does not fill)': ico | dod, 'regular dodecahedron (does not fill)': dod, 'regular icosahedron (does not fill)': ico,
      'regular octahedron (does not fill alone)': perm((1, 0, 0)), 'regular tetrahedron (does not fill alone)': {(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)}}
for k, P in CL.items():
    P = np.array(sorted(P), float); A = S.classes(S.dihedrals(P)); out['classical'][k] = S.test(A, [a for a, n in A])[0]
json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out, indent=1))
