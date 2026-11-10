"""Free scale, step 2: CUBES AS CUBES (DICTO 22 Oct: "in the dodecahedron layer's edging use whole cubes (edge phi) wherever possible";
"next to a Dogstar, a plain cube if the Dogstar keeps that face's roof-space"; started 10 Nov "go on with cubes as cubes").
In mixes with D and C: every edging cell next to a Dogstar is a plain cube C (edge phi) and that Dogstar keeps the roof-space on the
edging side (a Dogstar with five roofs out, S5); Y disappears. Edging cells next to a dodecahedron stay X (the roof pokes in).
Check: as mixes_free.py, all 31 mixes (mixes without C or D unchanged), every point covered once; also the share of edging cells that
are whole cubes. Usage: python mixes_cubes.py"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1'))
import mixes3 as M3
from mixes3 import part, phi, CUBE, ROOF, DOD, h
import mixes_free as MF
def D_world_cc(z0, layers=3, R=2, cubes=True):
    P = []; dods = []; edging = {'C': 0, 'X': 0, 'Y': 0}
    cell = lambda i, j, k: np.array([i * phi, j * phi, z0 + k * phi + h])
    mid = lambda k: 0 < k < layers - 1
    isD = lambda i, j, k: mid(k) and (i + j + k) % 2 == 0
    for i, j, k in itertools.product(range(-R, R + 1), range(-R, R + 1), range(layers)):
        c = cell(i, j, k)
        if isD(i, j, k): P.append(part(DOD + c, 1, 'D')); dods.append(c); continue
        if mid(k):
            edge_side = []
            P.append(part(CUBE + c, 1, 'S5' if cubes and not (mid(k - 1) and mid(k + 1)) else 'S'))
            for (a, sg), Rf in ROOF.items():
                d = np.zeros(3, int); d[a] = sg; n = (i + d[0], j + d[1], k + d[2])
                if isD(*n): P.append(part(ROOF[(a, -sg)] + cell(*n), -1))
                elif not mid(n[2]) and not cubes: P.append(part(ROOF[(a, -sg)] + cell(*n), -1))
        else:
            sg = 1 if k == 0 else -1; n = (i, j, k + sg)
            if layers < 3 or not mid(n[2]): P.append(part(CUBE + c, 1, '?')); continue
            if isD(*n): P.append(part(CUBE + c, 1, 'X')); P.append(part(ROOF[(2, -sg)] + cell(*n), -1)); edging['X'] += 1
            elif cubes: P.append(part(CUBE + c, 1, 'C')); edging['C'] += 1
            else: P.append(part(CUBE + c, 1, 'Y')); P.append(part(ROOF[(2, sg)] + c, 1)); edging['Y'] += 1
    return P, dods, edging
EDG = {}
def build(mix):
    P = []; z = 0.0; dods = []; seam = None; tops = []
    if 'D' in mix:
        q, dods, e = D_world_cc(z, cubes='C' in mix); EDG[''.join(sorted(mix))] = e; P += q; z += 3 * phi
    if 'C' in mix: P += MF.C_world(z); z += phi
    if mix & {'T', 'O', 'I'}:
        seam = z; q, tops = MF.octet_world(z, mix); P += q; z += 2 * MF.s
    return P, z, dods, seam, tops
MF.build = build
if __name__ == '__main__':
    allok = True; kit = set()
    for r in range(1, 6):
        for m in itertools.combinations('DICTO', r):
            k, bad, ov, top, sok, face = MF.check(set(m)); kit |= set(k) - {'C', 'D', 'T', 'O', 'I+A'}
            allok &= bad == 0 and ov == 0 and sok and face is not False
            e = EDG.get(''.join(sorted(m)))
            print(''.join(m).ljust(6), 'pieces', k, '| not covered once:', bad, '| D overlaps:', ov, '| solids used:', sok, '| seam f2f:', face,
                  ('| edging: ' + ', '.join(f'{a} {b}' for a, b in e.items() if b)) if e else '', flush=True)
    print('connector kit used:', sorted(kit))
    print('FINAL ok' if allok else 'FINAL FAIL')
