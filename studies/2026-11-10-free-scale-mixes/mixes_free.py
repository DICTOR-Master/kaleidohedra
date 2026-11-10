"""#47 free scale, core (DICTO 22 Oct plan, started 10 Nov: 'yes start the free scale core'). Every mix of the five Platonic solids
fills space with the solids at their own sizes: dodecahedron edge 1, cube edge phi (Euclid's cube: same circumsphere), tetrahedron and
octahedron edge phi, icosahedron edge sqrt2/phi in Pacioli's position inside the octet's octahedra (rest = six Admiral Caps A).
Two worlds instead of four: golden-cubic (grid phi: dodecahedra + Dogstars S + boundary X/Y, and cubes C) and ONE octet of edge phi
(T, O, I+A; tetrahedra not in the mix = 4 Q, octahedra not in the mix = 2 P), turned 45 degrees about z so its square layers are the
cube faces: the seam meets FACE TO FACE. Kit: P, Q, A, S, X, Y (Q' of #47 disappears). Check as #47's mixes3.py: random points, pieces as
signed sums of convex parts, every point covered exactly once; plus the seam check (every cube top face = an octahedron's equator).
Usage: python mixes_free.py"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-10-22-platonic-mix-step1'))
from mixes3 import D_world, part, phi
a = phi; s = a / 2 ** .5                                  # octet edge phi
R45 = np.array([[2 ** -.5, -2 ** -.5, 0], [2 ** -.5, 2 ** -.5, 0], [0, 0, 1]])
def C_world(z0, layers=1, R=3):
    cube = np.array(list(itertools.product((0, 1), repeat=3)), float) * phi
    return [part(cube + np.array([i * phi, j * phi, z0 + k * phi]), 1, 'C') for i, j, k in itertools.product(range(-R, R + 1), range(-R, R + 1), range(layers))]
def octet_world(z0, mix, K=2, R=5):
    """edge-phi octet between z0 and z0 + K s (turned 45 deg), octahedra on the faces as half octahedra P; octahedron = O, or I+A
    (both alternate by layer when O and I are both in the mix), or 2 P; tetrahedron = T or 4 Q"""
    P = []; tops = []
    rot = lambda pts: [R45 @ np.asarray(p, float) + np.array([0, 0, z0]) for p in pts]
    for x, y, z in itertools.product(range(-R, R + 1), range(-R, R + 1), range(0, K + 1)):
        c = np.array([x, y, z]) * s
        if (x + y + z) % 2:
            V = [c + d * s for d in np.vstack([np.eye(3), -np.eye(3)])]; eq = [v for v in V if abs(v[2] - c[2]) < 1e-9]
            up, dn = eq + [c + np.array([0, 0, s])], eq + [c - np.array([0, 0, s])]
            if z == 0: P.append(part(rot(up), 1, 'P')); tops.append(rot(eq))
            elif z == K: P.append(part(rot(dn), 1, 'P'))
            else:
                kind = ('O' if 'O' in mix and ('I' not in mix or x % 2 == 0) else 'I+A' if 'I' in mix else None)   # O and I alternate along x when both are in the mix
                if kind: P.append(part(rot(V), 1, kind))
                else: P.append(part(rot(up), 1, 'P')); P.append(part(rot(dn), 1, 'P'))
        if z == K: continue
        cs = [np.array([x + i, y + j, z + k]) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
        ev = [q * s for q in cs if q.sum() % 2 == 0]
        if 'T' in mix: P.append(part(rot(ev), 1, 'T'))
        else:
            g = np.mean(ev, 0)
            for f in itertools.combinations(ev, 3): P.append(part(rot(list(f) + [g]), 1, 'Q'))
    return P, tops
def build(mix):
    P = []; z = 0.0; dods = []; seam = None
    if 'D' in mix: q, dods = D_world(z); P += q; z += 3 * phi
    if 'C' in mix: P += C_world(z); z += phi
    if mix & {'T', 'O', 'I'}:
        seam = z; q, tops = octet_world(z, mix); P += q; z += 2 * s
    return P, z, dods, seam, (tops if seam is not None else [])
def seam_ok(tops, seam):
    """every cube face square of the grid (edge phi) in a window equals an octahedron equator square (face to face)"""
    sq = {tuple(np.round(np.sort(np.array(t)[:, :2], axis=0).ravel(), 6)) for t in tops}
    n = 0
    for i, j in itertools.product(range(-2, 2), range(-2, 2)):
        corners = np.array([[i * phi, j * phi], [(i + 1) * phi, j * phi], [i * phi, (j + 1) * phi], [(i + 1) * phi, (j + 1) * phi]])
        n += tuple(np.round(np.sort(corners, axis=0).ravel(), 6)) in sq
    return n == 16
def check(mix, N=40000):
    P, top, dods, seam, tops = build(mix)
    rs = np.random.default_rng(3); X = np.column_stack([rs.uniform(-1.3, 1.3, N), rs.uniform(-1.3, 1.3, N), rs.uniform(0.001, top - 0.001, N)])
    tot = np.zeros(N); nd = np.zeros(N, int); kinds = set()
    for sg, n, o, k in P:
        inside = np.all(X @ n.T < o - 1e-9, axis=1); tot += sg * inside
        if k: kinds.add(k)
        if k == 'D': nd += inside
    used = {k for k in kinds}
    solids_ok = all(x in used or (x == 'I' and 'I+A' in used) for x in mix)
    face = seam_ok(tops, seam) if (seam is not None and ('C' in mix or 'D' in mix)) else None
    return sorted(kinds), int((np.abs(tot - 1) > 1e-9).sum()), int((nd > 1).sum()), round(top, 3), solids_ok, face
if __name__ == '__main__':
    allok = True; kit = set()
    for r in range(1, 6):
        for m in itertools.combinations('DICTO', r):
            k, bad, ov, top, sok, face = check(set(m)); kit |= set(k) - {'C', 'D', 'T', 'O', 'I+A'}
            allok &= bad == 0 and ov == 0 and sok and face is not False
            print(''.join(m).ljust(6), 'height', str(top).ljust(7), 'pieces', k, '| not covered once:', bad, '| D overlaps:', ov,
                  '| every solid used:', sok, '| seam face to face:', face, flush=True)
    print('connector kit used:', sorted(kit | ({'A'} if True else set())))
    print('FINAL ok' if allok else 'FINAL FAIL')
