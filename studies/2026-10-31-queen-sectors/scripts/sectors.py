# Queen sectors (DICTO 2026-10-31): cut each Queen from the centre along the axes of her core's pyramids.
# White Queen = 600-cell round a corner v: core = the 20 tetrahedra at v (the Cleo-Icos); 20 sectors = the cones over the
# core icosahedron's 20 faces. Red Queen = 120-cell round the cell at v: core = that dodecahedron; 12 sectors = the cones over
# its 12 pentagons (Aristotle's 12 pyramids). A cell goes to the sector its centre's direction across the seed axis falls in
# (the component of the centre orthogonal to v; the cones are the Voronoi regions of the core's face normals). Ties are reported.
import itertools, numpy as np
phi = (1 + 5 ** .5) / 2
V = set()
for i in range(4):
    for s in (1, -1):
        p = [0] * 4; p[i] = s; V.add(tuple(p))
for s in itertools.product((.5, -.5), repeat=4): V.add(s)
base = (phi / 2, .5, 1 / (2 * phi), 0)
even = [p for p in itertools.permutations(range(4)) if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 == 0]
for p in even:
    for sg in itertools.product((1, -1), repeat=3):
        q = [0.] * 4; vals = [base[0] * sg[0], base[1] * sg[1], base[2] * sg[2], 0.]
        for k in range(4): q[p[k]] = vals[k]
        V.add(tuple(round(x, 12) for x in q))
V = np.array(sorted(V)); assert len(V) == 120
e = 1 / phi; D = np.linalg.norm(V[:, None] - V[None], axis=2); A = np.abs(D - e) < 1e-9
assert (A.sum(1) == 12).all()
cells = [c for c in itertools.combinations(range(120), 4) if all(A[a, b] for a, b in itertools.combinations(c, 2))] if False else None
# faster: tetrahedra from edges
cells = set()
for a in range(120):
    nb = np.nonzero(A[a])[0]
    for b, c, d in itertools.combinations(nb, 3):
        if A[b, c] and A[b, d] and A[c, d]: cells.add(tuple(sorted((a, b, c, d))))
cells = sorted(cells); assert len(cells) == 600
v = V[0]
def sectors(centres, axes, label):
    u = centres - np.outer(centres @ v, v); n = np.linalg.norm(u, axis=1)
    on_axis = n < 1e-9
    ax = axes - np.outer(axes @ v, v); ax /= np.linalg.norm(ax, axis=1)[:, None]
    dots = (u / np.where(n, n, 1)[:, None]) @ ax.T
    best = dots.max(1); ties = (np.abs(dots - best[:, None]) < 1e-9).sum(1)
    cnt = np.zeros(len(axes), int); tie = 0
    for i in range(len(centres)):
        if on_axis[i]: continue
        if ties[i] > 1: tie += 1; continue
        cnt[dots[i].argmax()] += 1
    h = np.round(centres @ v, 9)
    print(f'{label}: {len(axes)} sectors; cells on the axis {on_axis.sum()} (split by all sectors); on a boundary {tie}; per sector {sorted(set(cnt))}')
    # boundary cells by layer height
    from collections import Counter
    bt = Counter(h[i] for i in range(len(centres)) if not on_axis[i] and ties[i] > 1)
    print('  boundary cells by height along v:', dict(sorted(bt.items(), reverse=True)), ' ties of', sorted(set(ties[~on_axis & (ties > 1)])))
    return cnt
# White Queen: cell centres; axes = the 20 core cells (at v)
C = np.array([V[list(c)].mean(0) for c in cells])
core = [i for i, c in enumerate(cells) if 0 in c]; assert len(core) == 20
sectors(C, C[core], 'White Queen (600 cells)')
# Red Queen: cells = 120-cell dodecahedra, centred on the 600-cell corners; core = the cell at v; axes = its 12 neighbours
nbr = np.nonzero(A[0])[0]
sectors(V, V[nbr], 'Red Queen (120 cells)')
