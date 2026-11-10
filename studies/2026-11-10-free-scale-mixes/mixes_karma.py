"""Free scale, step 4A: the D-I BRIDGE by KARMA CELLS (DICTO 10 Nov: "go on with the D–I bridge" → "both, A first").
#22 (The Chain of Karma, theorem): a dodecahedron of edge 1 is exactly an icosahedron of edge 1/phi inside a shell of 12 pentagonal
pyramids, 30 AXE and 20 CLEO. So an icosahedron can stand in world 1 in a dodecahedron's place, met face to face by DICTO's shell
pieces (a 'Karma cell', region = the dodecahedron). Here every icosahedron goes into world 1: the even cells cycle through the
mix's D, I (Karma cell) and RD; the octet carries only T, O, CO. Check as mixes_rdco.py over all 127 mixes of D, I, C, T, O, RD, CO.
Usage: python mixes_karma.py [first last]"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1'))
from mixes3 import part, phi, CUBE, ROOF, DOD, h
import mixes_free as MF, mixes_rdco as RC
def world1(z0, mix, layers=3, R=2):
    P = []; dods = []
    cell = lambda i, j, k: np.array([i * phi, j * phi, z0 + k * phi + h])
    mid = lambda k: 0 < k < layers - 1
    even = lambda i, j, k: mid(k) and (i + j + k) % 2 == 0
    avail = [x for x in ('D', 'IK', 'RD') if (x if x != 'IK' else 'I') in mix]
    def kind(i, j, k):
        if not even(i, j, k): return None
        return avail[(i + 2 * j) % len(avail)]
    intr = lambda a, sg, n: (RC.PYR if kind(*n) == 'RD' else ROOF)[(a, -sg)] + cell(*n)
    cubes = 'C' in mix
    for i, j, k in itertools.product(range(-R, R + 1), range(-R, R + 1), range(layers)):
        c = cell(i, j, k); kd = kind(i, j, k)
        if kd == 'D': P.append(part(DOD + c, 1, 'D')); dods.append(c); continue
        if kd == 'IK': P.append(part(DOD + c, 1, 'I+K')); dods.append(c); continue      # icosahedron + Karma shell (#22)
        if kd == 'RD': P.append(part(RC.RD + c, 1, 'RD')); continue
        if mid(k):
            subs = []
            for (a, sg) in ROOF:
                d = np.zeros(3, int); d[a] = sg; n = (i + d[0], j + d[1], k + d[2])
                if kind(*n): subs.append(intr(a, sg, n))
                elif not mid(n[2]) and not cubes: subs.append(ROOF[(a, -sg)] + cell(*n))
            P.append(part(CUBE + c, 1, 'S*'))
            for V in subs: P.append(part(V, -1))
        else:
            sg = 1 if k == 0 else -1; n = (i, j, k + sg); kn = kind(*n)
            if kn in ('D', 'IK'): P.append(part(CUBE + c, 1, 'X')); P.append(part(ROOF[(2, -sg)] + cell(*n), -1))
            elif kn == 'RD': P.append(part(CUBE + c, 1, 'XR')); P.append(part(RC.PYR[(2, -sg)] + cell(*n), -1))
            elif cubes: P.append(part(CUBE + c, 1, 'C'))
            else: P.append(part(CUBE + c, 1, 'Y')); P.append(part(ROOF[(2, sg)] + c, 1))
    return P, dods
def build(mix):
    P = []; z = 0.0; dods = []; seam = None; tops = []
    if mix & {'D', 'RD', 'I'}: q, dods = world1(z, mix); P += q; z += 3 * phi
    if 'C' in mix and not mix & {'D', 'RD', 'I'}: P += MF.C_world(z); z += phi
    m2 = mix - {'I'}
    if m2 & {'T', 'O', 'CO'}:
        seam = z; q, tops = RC.octet2(z, m2); P += q; z += 2 * MF.s
    return P, z, dods, seam, tops
RC.build = build
_check = RC.check
def check(mix, N=40000):
    kinds, bad, ov, used, face = _check(mix, N)
    used = all((x in kinds) or (x == 'I' and 'I+K' in kinds) for x in mix)
    return kinds, bad, ov, used, face
if __name__ == '__main__':
    SOL = ['D', 'I', 'C', 'T', 'O', 'RD', 'CO']
    mixes = [set(m) for r in range(1, 8) for m in itertools.combinations(SOL, r)]
    lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, len(mixes))
    allok = True; kit = set()
    for idx in range(lo, hi):
        m = mixes[idx]; k, bad, ov, used, face = check(m); kit |= set(k) - set(SOL) - {'I+K'}
        ok = bad == 0 and ov == 0 and used and face is not False; allok &= ok
        print(f'PROGRESS {(idx - lo + 1) / (hi - lo):.3f} mix {idx}', flush=True)
        print('+'.join(x for x in SOL if x in m).ljust(18), 'pieces', k, '| not covered once:', bad, '| D/Karma overlaps:', ov, '| all used:', used, '| seam f2f:', face, '' if ok else '  <-- FAIL', flush=True)
    print('helper kinds used (Karma shells: pentagonal pyramid, AXE, CLEO inside every I+K):', sorted(kit))
    print('FINAL ok' if allok else 'FINAL FAIL')
