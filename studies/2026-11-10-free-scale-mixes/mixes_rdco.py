"""Free scale, step 3 (DICTO 10 Nov: "other shapes … RD, TO and CO?" → "leave TO out … yes please"): every mix of the five Platonic
solids plus the rhombic dodecahedron RD and the cuboctahedron CO (127 mixes) fills space in the same two worlds.
World 1 (grid phi): the alternate cubes carry dodecahedra D (cube + 6 roofs) and/or RD (cube + 6 square pyramids, apex at the
neighbour cell centre); the other cells are what is left of their cube (Dogstar-type helpers; with RD only, nothing is left); edging:
next to a D an X (cube minus roof), next to an RD an XR (cube minus pyramid), next to a remainder cell a whole cube C when C is in the mix
(cubes as cubes), else Y. World 2: the octet of edge phi; CO centred at chosen corners (spacing 4 in x and y, so whole octahedra and
tetrahedra remain), each CO = its 8 tetrahedra + 6 half octahedra; a touched octahedron keeps its other half as P.
Check as before: random points, signed convex parts, covered exactly once; every solid of the mix used; seam face to face.
Usage: python mixes_rdco.py [first last]  (mix index range, for piloting)"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1'))
from mixes3 import part, phi, CUBE, ROOF, DOD, h
import mixes_free as MF
from scipy.spatial import ConvexHull
PYR = {(a, sg): np.vstack([CUBE[np.isclose(CUBE[:, a], sg * h)], (lambda e: e)(np.eye(3)[a] * sg * phi)]) for a in range(3) for sg in (1, -1)}
RD = np.vstack([CUBE] + [np.eye(3)[a] * sg * phi for a in range(3) for sg in (1, -1)])
assert abs(ConvexHull(RD).volume - 2 * phi ** 3) < 1e-9          # RD = cube + 6 pyramids = twice the cube
def world1(z0, mix, layers=3, R=2):
    P = []; dods = []
    cell = lambda i, j, k: np.array([i * phi, j * phi, z0 + k * phi + h])
    mid = lambda k: 0 < k < layers - 1
    even = lambda i, j, k: mid(k) and (i + j + k) % 2 == 0
    def kind(i, j, k):
        if not even(i, j, k): return None
        if 'D' in mix and 'RD' in mix: return 'D' if i % 2 == 0 else 'RD'
        return 'D' if 'D' in mix else 'RD'
    intr = lambda a, sg, n: (ROOF if kind(*n) == 'D' else PYR)[(a, -sg)] + cell(*n)    # what neighbour n pokes into us
    cubes = 'C' in mix
    for i, j, k in itertools.product(range(-R, R + 1), range(-R, R + 1), range(layers)):
        c = cell(i, j, k); kd = kind(i, j, k)
        if kd == 'D': P.append(part(DOD + c, 1, 'D')); dods.append(c); continue
        if kd == 'RD': P.append(part(RD + c, 1, 'RD')); continue
        if mid(k):
            subs = []
            for (a, sg) in ROOF:
                d = np.zeros(3, int); d[a] = sg; n = (i + d[0], j + d[1], k + d[2])
                if kind(*n): subs.append(intr(a, sg, n))
                elif not mid(n[2]) and not cubes: subs.append(ROOF[(a, -sg)] + cell(*n))
            P.append(part(CUBE + c, 1, 'S*'))
            for V in subs: P.append(part(V, -1))
        else:
            sg = 1 if k == 0 else -1; n = (i, j, k + sg)
            if kind(*n) == 'D': P.append(part(CUBE + c, 1, 'X')); P.append(part(ROOF[(2, -sg)] + cell(*n), -1))
            elif kind(*n) == 'RD': P.append(part(CUBE + c, 1, 'XR')); P.append(part(PYR[(2, -sg)] + cell(*n), -1))
            elif cubes: P.append(part(CUBE + c, 1, 'C'))
            else: P.append(part(CUBE + c, 1, 'Y')); P.append(part(ROOF[(2, sg)] + c, 1))
    return P, dods
def octet2(z0, mix, K=2, R=6):
    a = phi; s = MF.s; R45 = MF.R45; P = []; tops = []
    rot = lambda pts: [R45 @ (np.asarray(p, float) * s) + np.array([0, 0, z0]) for p in pts]
    CO = {(x, y, 1) for x in range(-R, R + 1) for y in range(-R, R + 1) if x % 4 == 1 and y % 4 == 0} if 'CO' in mix else set()
    E = np.vstack([np.eye(3), -np.eye(3)]).astype(int)
    for x, y, z in itertools.product(range(-R, R + 1), range(-R, R + 1), range(0, K + 1)):
        c = np.array([x, y, z])
        if (x + y + z) % 2:
            V = [c + d for d in E]; hit = [d for d in E if tuple(c + d) in CO]
            def half(axis_d):   # half octahedron with apex c + axis_d
                return [c + d for d in E if abs(d @ axis_d) == 0] + [c + axis_d]
            if z == 0 or z == K:
                up = np.array([0, 0, 1 if z == 0 else -1])
                if not any((d == up).all() for d in hit): P.append(part(rot(half(up)), 1, 'P'))
                if z == 0: tops.append(rot([c + d for d in E if d[2] == 0]))
            elif hit:
                for d in hit: pass
                if len(hit) == 1: P.append(part(rot(half(-hit[0])), 1, 'P'))
                # two opposite hits: both halves belong to COs, nothing left
            else:
                kd = ('O' if 'O' in mix and ('I' not in mix or x % 2 == 0) else 'I+A' if 'I' in mix else None)
                if kd: P.append(part(rot(V), 1, kd))
                else:
                    P.append(part(rot(half(np.array([0, 0, 1]))), 1, 'P')); P.append(part(rot(half(np.array([0, 0, -1]))), 1, 'P'))
        if z == K: continue
        cs = [np.array([x + i, y + j, z + k]) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
        ev = [q for q in cs if q.sum() % 2 == 0]
        if any(tuple(q) in CO for q in ev): continue                       # this tetrahedron is part of a CO
        if 'T' in mix: P.append(part(rot(ev), 1, 'T'))
        else:
            g = np.mean(ev, 0)
            for f in itertools.combinations(ev, 3): P.append(part(rot(list(f) + [g]), 1, 'Q'))
    for v in CO:
        v = np.array(v); cov = [v + p for p in itertools.permutations((1, 1, 0)) for p in [np.array(p)]]
        cov = [v + np.array(q) for q in {tuple(sg * np.array(p)) for p in set(itertools.permutations((1, 1, 0))) for sg in [np.array(t) for t in itertools.product((1, -1), repeat=3)]}]
        P.append(part(rot(cov), 1, 'CO'))
    return P, tops
def build(mix):
    P = []; z = 0.0; dods = []; seam = None; tops = []
    if mix & {'D', 'RD'}: q, dods = world1(z, mix); P += q; z += 3 * phi
    if 'C' in mix and not mix & {'D', 'RD'}: P += MF.C_world(z); z += phi
    if mix & {'T', 'O', 'I', 'CO'}:
        seam = z; q, tops = octet2(z, mix); P += q; z += 2 * MF.s
    return P, z, dods, seam, tops
def check(mix, N=40000):
    P, top, dods, seam, tops = build(mix)
    rs = np.random.default_rng(3); X = np.column_stack([rs.uniform(-2.2, 2.2, N), rs.uniform(-2.2, 2.2, N), rs.uniform(0.001, top - 0.001, N)])
    tot = np.zeros(N); nd = np.zeros(N, int); kinds = set()
    for sg, n, o, k in P:
        inside = np.all(X @ n.T < o - 1e-9, axis=1); tot += sg * inside
        if k and inside.any(): kinds.add(k)
        if k == 'D': nd += inside
    used = all((x in kinds) or (x == 'I' and 'I+A' in kinds) for x in mix)
    face = MF.seam_ok(tops, seam) if (seam is not None and mix & {'C', 'D', 'RD'}) else None
    return sorted(kinds), int((np.abs(tot - 1) > 1e-9).sum()), int((nd > 1).sum()), used, face
if __name__ == '__main__':
    SOL = ['D', 'I', 'C', 'T', 'O', 'RD', 'CO']
    mixes = [set(m) for r in range(1, 8) for m in itertools.combinations(SOL, r)]
    lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, len(mixes))
    allok = True; kit = set()
    for idx in range(lo, hi):
        m = mixes[idx]; k, bad, ov, used, face = check(m); kit |= set(k) - set(SOL) - {'I+A'}
        ok = bad == 0 and ov == 0 and used and face is not False; allok &= ok
        print(f'PROGRESS {(idx - lo + 1) / (hi - lo):.3f} mix {idx}', flush=True)
        print('+'.join(x for x in SOL if x in m).ljust(18), 'pieces', k, '| not covered once:', bad, '| D overlaps:', ov, '| all used:', used, '| seam f2f:', face, '' if ok else '  <-- FAIL', flush=True)
    print('helper kinds used:', sorted(kit))
    print('FINAL ok' if allok else 'FINAL FAIL')
