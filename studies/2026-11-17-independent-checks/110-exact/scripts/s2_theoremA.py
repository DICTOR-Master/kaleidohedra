"""Item 2, exact: Theorem A (plates of A, B, C3 against the 360 walls)."""
from common import *

L = Log('logs/s2_theoremA.log')
B = load_base()
P, Q, lab = B['P'], B['Q'], B['lab']
mir, crs = wall_sets(P, Q)
R2 = (50, 50)
res = {}
for name in ['A', 'B', 'C3']:
    ids = np.nonzero(lab == name)[0]
    X = P[ids]
    F, Rg, E = face_lattice(X)
    L(f'{name}: f-vector (corners, edges, 2-faces, cells) =', (len(X), len(E), len(Rg), len(F)),
      ' cell sizes', sorted(len(f) for f in F))
    keys = plate_keys(X, Rg)
    kinds = {}
    for r, k in zip(Rg, keys):
        d2 = sorted({zkey(zdot(X[a] - X[b], X[a] - X[b])) for a, b in itertools.combinations(r, 2)
                     if True})
        w = 'mirror' if k in mir else ('cross' if k in crs else 'none')
        kinds.setdefault((len(r), tuple(d2), w), []).append(k)
    for kk, v in sorted(kinds.items()):
        L(f'  ridge with {kk[0]} corners, squared distances {kk[1]} -> {kk[2]}: {len(v)} ridges')
    res[name] = (Rg, keys, kinds)
    plates = {}
    for r, k in zip(Rg, keys):
        plates.setdefault(k, []).append(r)
    res[name] = (Rg, keys, plates)

# squared side lengths at scale 5: edge sqrt2 -> 50, radius phi sqrt2 -> 50 phi^2 = (50,50)
def count(name, nverts, side, wall):
    Rg, keys, _ = res[name]
    X = P[np.nonzero(lab == name)[0]]
    n = 0
    for r, k in zip(Rg, keys):
        if len(r) != nverts:
            continue
        ds = {zkey(zdot(X[a] - X[b], X[a] - X[b])) for a, b in itertools.combinations(r, 2)}
        w = 'mirror' if k in mir else ('cross' if k in crs else 'none')
        if (side is None or ds == side) and w == wall:
            n += 1
    return n

EDGE = {(50, 0)}
RAD = {(50, 50)}
RECT = {(50, 0), (50, 50), (100, 50)}  # sides edge and radius, diagonal^2 = edge^2+radius^2
A_pl, B_pl, C_pl = res['A'][2], res['B'][2], res['C3'][2]
L.check('A plates', len(A_pl), 30)
L.check('A: one ridge per plate (non-heart)', set(len(v) for v in A_pl.values()), {1})
L.check('A: edge-triangle plates on mirrors', count('A', 3, EDGE, 'mirror'), 20)
L.check('A: hexagon plates on mirrors', count('A', 6, None, 'mirror'), 10)
L.check('A: all plates in W(P)', all(k in mir or k in crs for k in A_pl), True)
L.check('B plates', len(B_pl), 80)
L.check('B: one ridge per plate (non-heart)', set(len(v) for v in B_pl.values()), {1})
L.check('B: edge triangles on mirrors', count('B', 3, EDGE, 'mirror'), 10)
L.check('B: golden rectangles on mirrors', count('B', 4, RECT, 'mirror'), 30)
L.check('B: radius triangles on cross walls', count('B', 3, RAD, 'cross'), 40)
L.check('B: all plates in W(P)', all(k in mir or k in crs for k in B_pl), True)
Am = {k for k in A_pl if k in mir}
Bm = {k for k in B_pl if k in mir}
s5m = {canon_dir(P[i]) for i in np.nonzero(lab == 'C3')[0]}   # roots e_i - e_j of S5
L.check('A mirrors', len(Am), 30)
L.check('B mirrors', len(Bm), 40)
L.check('A and B share exactly 10 mirrors', len(Am & Bm), 10)
L.check('the shared ones are the 10 mirrors of S5', Am & Bm == s5m, True)
L.check('A and B mirrors together: all 60', len(Am | Bm), 60)
L.check('C3 2-faces', len(res['C3'][0]), 70)
L.check('C3 plates', len(C_pl), 5)
L.check('C3 plates all cross walls', all(k in crs for k in C_pl), True)
L.check('C3 faces per plate', sorted(len(v) for v in C_pl.values()), [14] * 5)
L.final()
