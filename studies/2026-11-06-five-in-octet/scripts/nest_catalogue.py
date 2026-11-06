"""DICTO 11-06: "if we had a few different combis of the nesting they might be easier to place together at slightly different scales".
Catalogue of the classical inscriptions between the five Platonic solids (inner corners at outer corners, edge points, face centres),
each checked (inner regular, inside outer), with edge and volume ratios; then every chain through all five solids (each once), with the
size of each solid when the outer one has edge 1. Exact forms where known in the comments; values float."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
def edge(V):
    D = np.linalg.norm(V[:, None] - V[None], axis=2); return D[D > 1e-9].min()
def faces(V):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 8)), set()).update(sp)
    return [V[list(s)].mean(0) for s in F.values()]
STD = {'O': orbit((1, 0, 0)), 'C': np.array(list(itertools.product((-1, 1), repeat=3)), float), 'I': orbit((0, 1, phi)),
       'D': np.vstack([orbit((1, 1, 1)), orbit((0, 1 / phi, phi))]), 'T': np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)}
NAME = {'D': 'dodecahedron', 'I': 'icosahedron', 'C': 'cube', 'T': 'tetrahedron', 'O': 'octahedron'}
COUNT = {'T': 4, 'O': 6, 'C': 8, 'I': 12, 'D': 20}
def regular_kind(V):
    V = np.unique(np.round(V, 9), axis=0)
    for k, n in COUNT.items():
        if len(V) == n:
            e = edge(V); s = edge(STD[k])
            # compare sorted distance multisets after scaling
            a = np.sort(np.linalg.norm(V[:, None] - V[None], axis=2).ravel()) / e
            b = np.sort(np.linalg.norm(STD[k][:, None] - STD[k][None], axis=2).ravel()) / s
            if np.allclose(a, b, atol=1e-6): return k, V
    return None, V
def inside(inner, outer):
    h = ConvexHull(outer); return ((inner @ h.equations[:, :3].T + h.equations[:, 3]) <= 1e-9).all()
INS = {}   # (outer, inner) -> (edge ratio, how)
def add(outer, cand, how):
    k, V = regular_kind(cand)
    if k and k != outer and inside(V, STD[outer]):
        r = edge(V) / edge(STD[outer]); key = (outer, k)
        if key not in INS or r > INS[key][0] + 1e-9: INS[key] = (r, how)
for o, V in STD.items():
    F = np.array(faces(V)); add(o, F, 'face centres')
    for sub in itertools.combinations(range(len(V)), 4):
        if o in ('C', 'D'): add(o, V[list(sub)], 'four corners')
    if o in ('D',):
        for sub in itertools.combinations([i for i in range(len(V)) if np.allclose(np.abs(V[i]), np.abs(V[i][0]))], 8): add(o, V[list(sub)], 'eight corners')
    for sub in itertools.combinations(range(len(F)), 4):
        if len(F) <= 8: add(o, F[list(sub)], 'four face centres')
    # edge points: midpoints and golden points
    D_ = np.linalg.norm(V[:, None] - V[None], axis=2); e = D_[D_ > 1e-9].min()
    E = [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(D_[i, j] - e) < 1e-9]
    add(o, np.array([(V[i] + V[j]) / 2 for i, j in E]), 'edge midpoints')
    mids = np.array([(V[i] + V[j]) / 2 for i, j in E])
    for sub in itertools.combinations(range(len(mids)), 6):
        if len(mids) <= 12:
            add(o, mids[list(sub)], 'six edge midpoints')
    if o == 'I':
        on_axes = np.array([m for m in mids if (np.abs(m) > 1e-9).sum() == 1]); add(o, on_axes, 'six edge midpoints (on the axes)')
    if o == 'O':   # Pacioli: one point per edge, golden, cyclically
        P = []
        for i, j in E:
            for t in (1 / phi ** 2, 1 / phi): P.append(V[i] + t * (V[j] - V[i]))
        P = np.unique(np.round(np.array(P), 9), axis=0)
        for cand in (orbit((0, 1, phi)), ):
            s = (1 / np.sqrt(1)) ; add(o, cand / (1 + phi), 'Pacioli: golden points of the edges')
    if o == 'C':
        add(o, orbit((0, 1, phi)) / phi, 'icosahedron touching all six faces (golden)')
print('Inscriptions (outer > inner): edge ratio inner/outer, volume share of outer')
vol = {k: ConvexHull(V).volume / edge(V) ** 3 for k, V in STD.items()}
for (o, i), (r, how) in sorted(INS.items()):
    print(f'  {NAME[o]:12s} > {NAME[i]:12s}  edge x{r:.6f}  volume {r**3*vol[i]/vol[o]:.4f}  ({how})')
# chains through all five
chains = []
for perm in itertools.permutations('DICTO'):
    if all((perm[k], perm[k + 1]) in INS for k in range(4)):
        sizes = [1.0]
        for k in range(4): sizes.append(sizes[-1] * INS[(perm[k], perm[k + 1])][0])
        chains.append((perm, sizes))
print(f'\nChains through all five ({len(chains)}), sizes (edge) with the outer solid of edge 1:')
for perm, sizes in chains:
    print('  ' + ' > '.join(f'{p} {s:.4f}' for p, s in zip(perm, sizes)))
print('FINAL ok')
