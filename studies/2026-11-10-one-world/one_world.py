"""ONE WORLD, the filling (DICTO 10 Nov). Every mix of D, I, C, T, O, RD, CO fills space in world 1 alone: the alternating cubes of the
grid phi hold dodecahedral cells (D itself, or I / C / T / O / CO inside its skin: skins.py, exact) and RD cells; the other cells are the
Dogstar-type remainders; edging X / XR, and whole cubes (or Y) next to remainders. No octet, no seam. Check: random points, signed
convex parts (a skinned cell's region is the dodecahedron), covered exactly once; every solid of the mix present.
Usage: python one_world.py"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1')); sys.path.insert(0, os.path.expanduser('~/mslide/free'))
from mixes3 import part, phi, CUBE, ROOF, DOD, h
import mixes_rdco as RC
SOL = ['D', 'I', 'C', 'T', 'O', 'RD', 'CO']
def world1(mix, layers=3, R=2):
    P = []
    cell = lambda i, j, k: np.array([i * phi, j * phi, k * phi + h])
    mid = lambda k: 0 < k < layers - 1
    even = lambda i, j, k: mid(k) and (i + j + k) % 2 == 0
    avail = [x for x in SOL if x in mix]
    kind = lambda i, j, k: avail[(i + 2 * j) % len(avail)] if even(i, j, k) else None
    intr = lambda a, sg, n: (RC.PYR if kind(*n) == 'RD' else ROOF)[(a, -sg)] + cell(*n)
    cubes_edge = 'C' in mix
    for i, j, k in itertools.product(range(-R, R + 1), range(-R, R + 1), range(layers)):
        c = cell(i, j, k); kd = kind(i, j, k)
        if kd == 'RD': P.append(part(RC.RD + c, 1, 'RD')); continue
        if kd: P.append(part(DOD + c, 1, kd + ('' if kd == 'D' else '+skin'))); continue
        if mid(k):
            subs = []
            for (a, sg) in ROOF:
                d = np.zeros(3, int); d[a] = sg; n = (i + d[0], j + d[1], k + d[2])
                if kind(*n): subs.append(intr(a, sg, n))
                elif not mid(n[2]) and not cubes_edge: subs.append(ROOF[(a, -sg)] + cell(*n))
            P.append(part(CUBE + c, 1, 'S*'))
            for V in subs: P.append(part(V, -1))
        else:
            sg = 1 if k == 0 else -1; n = (i, j, k + sg); kn = kind(*n)
            if kn == 'RD': P.append(part(CUBE + c, 1, 'XR')); P.append(part(RC.PYR[(2, -sg)] + cell(*n), -1))
            elif kn: P.append(part(CUBE + c, 1, 'X')); P.append(part(ROOF[(2, -sg)] + cell(*n), -1))
            elif cubes_edge: P.append(part(CUBE + c, 1, 'C-edge'))
            else: P.append(part(CUBE + c, 1, 'Y')); P.append(part(ROOF[(2, sg)] + c, 1))
    return P, layers * phi
def check(mix, N=40000):
    P, top = world1(mix)
    rs = np.random.default_rng(3); X = np.column_stack([rs.uniform(-2.2, 2.2, N), rs.uniform(-2.2, 2.2, N), rs.uniform(0.001, top - 0.001, N)])
    tot = np.zeros(N); kinds = set()
    for sg, n, o, k in P:
        inside = np.all(X @ n.T < o - 1e-9, axis=1); tot += sg * inside
        if k and inside.any(): kinds.add(k)
    used = all(any(k == x or k == x + '+skin' for k in kinds) for x in mix)
    return sorted(kinds), int((np.abs(tot - 1) > 1e-9).sum()), used
if __name__ == '__main__':
    mixes = [set(m) for r in range(1, 8) for m in itertools.combinations(SOL, r)]
    allok = True
    for idx, m in enumerate(mixes):
        k, bad, used = check(m); ok = bad == 0 and used; allok &= ok
        if idx % 10 == 0 or not ok or len(m) == 7:
            print(f'PROGRESS {(idx + 1) / len(mixes):.3f}', '+'.join(x for x in SOL if x in m).ljust(18), 'cells', k, '| not covered once:', bad, '| all used:', used, '' if ok else '<-- FAIL', flush=True)
    print(f'{len(mixes)} mixes checked, all in ONE world (no octet, no seam)')
    print('FINAL ok' if allok else 'FINAL FAIL')
