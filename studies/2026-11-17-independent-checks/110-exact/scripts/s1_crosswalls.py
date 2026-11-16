"""Item 1, exact: the 300 cross walls are the central sections of the 25
inscribed 24-cells across their cell axes.

Meaning checked: for an inscribed 24-cell T (24 corners of the 600-cell
forming a regular 24-cell), a cell axis is the line through the centre and
the centres of a pair of opposite (octahedral) cells of T; the central
section across that axis is the hyperplane through the centre perpendicular
to the axis, i.e. parallel to that pair of opposite cells."""
from common import *

L = Log('logs/s1_crosswalls.log')
B = load_base()
P, Q, refl = B['P'], B['Q'], B['refl']
mir, crs = wall_sets(P, Q)
G = gram(P)
R2 = np.array([50, 50])
HALF = np.array([25, 25])          # R^2/2  (60 deg)
M120 = -HALF                       # 120 deg
ZERO = np.array([0, 0])
# all D4 simple systems among the corners: a2 joined (120 deg) to a1,a3,a4,
# which are pairwise orthogonal.  Every 24-cell on the corners is a D4 root
# system and contains such a system, so this finds all of them.
found = set()
for a2 in range(120):
    nb = [j for j in range(120) if zeq(G[a2, j], M120)]
    for t in itertools.combinations(nb, 3):
        if all(zeq(G[x, y], ZERO) for x, y in itertools.combinations(t, 2)):
            S = set((a2,) + t)
            while True:
                new = {int(refl[r][s]) for r in S for s in S} | S
                if new == S:
                    break
                S = new
            found.add(tuple(sorted(S)))
sizes = sorted({len(s) for s in found})
L.check('sizes of the closed D4 systems', sizes, [24])
L.check('inscribed 24-cells', len(found), 25)
T24 = sorted(found)
cnt = np.zeros(120, int)
for t in T24:
    cnt[list(t)] += 1
L.check('each corner in exactly 5 of the 24-cells', set(cnt.tolist()), {5})
allowed = {(50, 50), (25, 25), (0, 0), (-25, -25), (-50, -50)}
ok = all({zkey(G[i, j]) for i in t for j in t} <= allowed for t in T24)
L.check('each 24-cell has only the 24-cell angles (0,60,90,120,180 deg)', ok, True)

keys = []
nfac, n12, nP = [], [], []
rows = []
for ti, t in enumerate(T24):
    X = P[list(t)]
    F, Rg, E = face_lattice(X)
    nfac.append((len(F), sorted({len(f) for f in F})))
    cents = [X[list(f)].sum(0) for f in F]
    axes = {}
    for f, c in zip(F, cents):
        axes.setdefault(canon_dir(c), []).append(f)
    assert len(axes) == 12 and all(len(v) == 2 for v in axes.values())
    for k, (key, pair) in enumerate(sorted(axes.items())):
        c = X[list(pair[0])].sum(0)
        # the two cells of the pair are opposite: centres c and -c
        c2 = X[list(pair[1])].sum(0)
        assert np.array_equal(c2, -c)
        onT = int((zdot(X, c[None]) == 0).all(-1).sum())
        onP = int((zdot(P, c[None]) == 0).all(-1).sum())
        n12.append(onT)
        nP.append(onP)
        keys.append(key)
        rows.append((ti, k, onT, onP, 'cross' if key in crs else ('mirror' if key in mir else 'none')))
L.check('facets of each 24-cell: 24 octahedra (6 corners)', set((a, tuple(b)) for a, b in nfac), {(24, (6,))})
L.check('corners of the 24-cell on each central section', set(n12), {12})
L.check('corners of the 600-cell on each central section', set(nP), {12})
L.check('number of sections 25 x 12', len(keys), 300)
L.check('sections distinct', len(set(keys)), 300)
L.check('sections = the 300 cross walls (normals along the dual 120-cell corners)', set(keys) == crs, True)
with open('data/crosswalls_24cells.csv', 'w') as f:
    f.write('cell24,axis,corners_of_24cell_on_section,corners_of_600cell_on_section,wall\n')
    for r in rows:
        f.write(','.join(map(str, r)) + '\n')
with open('data/24cells.txt', 'w') as f:
    for t in T24:
        f.write(' '.join(map(str, t)) + '\n')
L.final()
