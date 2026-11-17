#!/usr/bin/env python3
"""Pilot / controls for mixlib: group, transforms, signed decomposition of C, exact volumes, and the lattice tilings of A, B, C
(exact: covolume = volume and no overlap with any lattice translate within 2R). Usage: pilot_lib.py <k10 dir> <inchbald json>"""
import sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from mixlib import *
t0 = time.time()
sol = load_solids(sys.argv[1], sys.argv[2])
ok = True
# transforms consistent: faces of transformed cells = transformed faces (A, B)
for nm in 'AB':
    for gi in range(120):
        F, C = place(sol, nm, gi, (1, -2, 0, 3, 0, 1))
        if from_cells(G, [c for c, _ in C]) != F: ok = False; print('transform mismatch', nm, gi)
# symmetry counts
for nm in 'ABC':
    c0 = canon_t(sol[nm]['faces']); k = sum(1 for gi in range(120) if canon_t(tfaces(sol[nm]['faces'], gi, (0,)*6)) == c0)
    sol[nm]['nsym'] = k; print(nm, 'symmetries', k, 'cells', len(sol[nm]['cells']), 'basis', sol[nm]['basis'])
ok &= [sol[x]['nsym'] for x in 'ABC'] == [4, 3, 12]
# exact volumes
for nm in 'ABC':
    v = sum((cell_volume(c)*Q(s) for c, s in sol[nm]['cells']), ZERO)
    vs = overlap_volume(sol[nm]['cells'], sol[nm]['cells'])
    print(nm, 'volume', (v.a, v.b), 'self-overlap volume', (vs.a, vs.b), 'equal:', v == vs); ok &= v == vs
    # lattice tiling: covolume and no overlap with translates
    B = sol[nm]['basis']; det = lattice_det(G, B); det = det if zsign(det) > 0 else zneg(det)
    cov_ok = Q(*det) == v; ok &= cov_ok
    E = np.array([[zfloat(c) for c in e] for e in G.E])
    pts = np.array([np.array(v, float) @ E for f in sol[nm]['faces'] for v in corners(f, 6)]); ctr = pts.mean(0); R = np.linalg.norm(pts - ctr, axis=1).max()
    Bf = np.array(B, float) @ E; tested = 0; bad = 0
    dual = np.linalg.inv(Bf).T; bound = [int(2*R*np.linalg.norm(dual[k])) + 1 for k in range(3)]   # no translate within 2R is missed
    for co in itertools.product(*[range(-b, b + 1) for b in bound]):
        if co == (0, 0, 0): continue
        l = tuple(int(x) for x in np.array(co) @ np.array(B))
        if np.linalg.norm(np.array(co, float) @ Bf) > 2*R + 1e-6: continue
        tested += 1
        Y = [(tcell(c, IDENT, l), s) for c, s in sol[nm]['cells']]
        if overlaps(sol[nm]['cells'], Y): bad += 1
    print(nm, 'lattice: covolume = volume', cov_ok, '; translates within 2R tested', tested, 'overlapping', bad, f't={time.time()-t0:.0f}s')
    ok &= bad == 0 and tested > 0
print('FINAL ok' if ok else 'FINAL FAIL: a control failed')
