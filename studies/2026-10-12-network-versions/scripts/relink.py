# Does the network ID -> D -> cage -> RT sit inside the Lotus seed's outer icosahedron I(phi^2) (dodecahedron edge 1 = the Lotus
# seed's own D(1))? Containment and clearance of each shell, in chain units.
import numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
def F(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
I2 = ref['I'] * PHI ** 2; FI = F(I2)
shells = {'ID core (edge phi/2)': ref['ID'] * PHI / 2, 'dodecahedron (edge 1)': ref['D'], 'fullerene cage (edge 1/phi)': ref['TI'] / PHI,
          'triacontahedron (edge 1.089814)': ref['RT'] * np.sqrt(45 - 18 * np.sqrt(5)) / 2}
for k, V in shells.items():
    d = (V @ FI[:, :3].T + FI[:, 3]).max()
    print(f'{k}: {"inside" if d <= 1e-9 else "OUTSIDE"} the Lotus seed I(phi^2); deepest corner {d:+.6f} from its faces')
print(f'volumes: RT {ConvexHull(shells["triacontahedron (edge 1.089814)"]).volume:.6f}, I(phi^2) {ConvexHull(I2).volume:.6f}')
RT = shells['triacontahedron (edge 1.089814)']; FR = F(RT)
import itertools
EI = [(a, b) for a, b in itertools.combinations(range(12), 2) if abs(np.linalg.norm(I2[a] - I2[b]) - PHI ** 2) < 1e-9]
fivef = RT[np.argsort(-np.linalg.norm(RT, axis=1))]
pieces = {}
# edge pieces: each RT rhombus with the icosahedron edge it faces
for f in FR:
    n = f[:3] / np.linalg.norm(f[:3]); rh = RT[np.abs(RT @ f[:3] + f[3]) < 1e-9]
    a, b = max(EI, key=lambda e: (I2[e[0]] + I2[e[1]]) @ n)
    pieces.setdefault('edge (rhombus to icosahedron edge)', []).append(np.vstack([rh, I2[a], I2[b]]))
# face pieces: each icosahedron face with the RT corner on its normal
for f in FI:
    n = f[:3] / np.linalg.norm(f[:3]); tri = I2[np.abs(I2 @ f[:3] + f[3]) < 1e-9]; c = RT[np.argmax(RT @ n)]
    pieces.setdefault('face (icosahedron face to RT three-fold corner)', []).append(np.vstack([tri, c]))
tot = 0
for k, L in pieces.items():
    v = [ConvexHull(P).volume for P in L]; tot += sum(v)
    ins = all(np.all(P @ FI[:, :3].T + FI[:, 3] <= 1e-9) for P in L)
    print(f'  {len(L)} x {k}: volume each {v[0]:.6f}, inside I(phi^2) {ins}')
gap = ConvexHull(I2).volume - ConvexHull(RT).volume
print(f'gap {gap:.6f}; these pieces {tot:.6f}; difference {gap - tot:+.6f} (overlaps or leftovers)')
rng = np.random.default_rng(11); S = rng.uniform(-3, 3, (400000, 3))
S = S[np.all(S @ FI[:, :3].T + FI[:, 3] < -1e-9, axis=1) & ~np.all(S @ FR[:, :3].T + FR[:, 3] <= 1e-9, axis=1)][:40000]
count = np.zeros(len(S), int)
for L in pieces.values():
    for P in L:
        E = ConvexHull(P).equations; count += np.all(S @ E[:, :3].T + E[:, 3] < 1e-9, axis=1)
print(f'{len(S)} sample points in the gap: covered exactly once {np.mean(count == 1):.4%}, uncovered {np.mean(count == 0):.4%}, twice or more {np.mean(count > 1):.4%}')
