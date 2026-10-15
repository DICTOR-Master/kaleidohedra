# Step 10 (DICTO's question): do golden rectangles fit the whole structure? The three mutually perpendicular golden rectangles have
# their 12 corners on the 5-fold axes (an icosahedron's corners). Scale k = corner radius. Where do they sit against the nest?
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
C = {n: np.array(V, float) for n, V in json.load(open('data/reversed-chain.json'))}
I = C['icosahedron']; u = I / np.linalg.norm(I, axis=1)[:, None]          # 12 five-fold directions
DO = C['dodecahedron (phi^3)']; eD = ConvexHull(DO).equations
def rad(e, d): nu = e[:, :3] @ d; m = nu > 1e-12; return np.min(-e[m, 3] / nu[m])
# the three rectangles: corner pairs at the golden distance (long edges) and at the short distance (short edges)
dist = np.linalg.norm(u[:, None] - u[None], axis=2); short = np.min(dist[dist > 1e-9])
E = [(i, j) for i in range(12) for j in range(i + 1, 12) if abs(dist[i, j] - short) < 1e-9 or abs(dist[i, j] - short * (1 + 5 ** .5) / 2) < 1e-9]
# every mirror plane through two 5-fold axes holds 4 corners: 15 golden rectangles (5 perpendicular triples), 60 edges
rect = [(i, j) for i, j in E if sum(1 for k in range(12) if abs(np.dot(np.cross(u[i], u[j]), u[k])) < 1e-9) == 4]
pts = np.vstack([u[i] + (u[j] - u[i]) * t for i, j in rect for t in np.linspace(0, 1, 201)])
r_min = max(rad(eD, p / np.linalg.norm(p)) / np.linalg.norm(p) for p in pts)  # k at which the whole frame clears D(phi^3)
lines = [f'{len(rect)} rectangle edges: 15 golden rectangles (5 perpendicular triples)',
         f'corners at the chain icosahedron (k = {np.linalg.norm(I[0]):.6f}): corners = RT tips = GSD valleys',
         f'corners at the face centres of D(phi^3): k = {min(-eD[:, 3]):.6f}; then the rectangles lie inside D(phi^3), touching its 12 faces',
         f'frames clear of the whole nest (every edge point outside D(phi^3)) from k = {r_min:.6f}']
eI = None
Ic = I / np.linalg.norm(I[0]); eIc = ConvexHull(Ic).equations; s = min(-e[3] / max(DO @ e[:3]) for e in eIc)   # smallest icosahedron around D(phi^3)
lines.append(f'smallest icosahedron around D(phi^3): corner radius {1 / s:.6f}; its golden rectangles clear the nest: {1 / s >= r_min - 1e-9}')
k3 = np.linalg.norm(I[0]) * ((1 + 5 ** .5) / 2) ** 3
lines.append(f'the next turn of the cycle, icosahedron x phi^3: corner radius {k3:.6f} = the clearing k above: {abs(k3 - r_min) < 1e-5}')
lines.append('exact: corner radius^2 = (50 - 22√5) * phi^6 = 10 + 2√5; long-edge midpoint radius^2 = (10 + 2√5) / (1 + phi^2) = 4,'
             ' the midradius^2 of D(phi^3): the 30 long edges touch its 30 edge midpoints')
print('\n'.join(lines)); open('data/polar-golden-rect.txt', 'w').write('\n'.join(lines) + '\n')

# render data: the 15 rectangles of the next turn's icosahedron (corners i, j, -i, -j for each icosahedron edge i-j, counted once),
# added to the step-5 nest (great stellated dodecahedron layers) as data/polar-rect-render.json
K = u * k3; R = []
for i, j in itertools.combinations(range(12), 2):
    if abs(dist[i, j] - short) > 1e-9: continue
    mi, mj = int(np.argmin(np.linalg.norm(u + u[i], axis=1))), int(np.argmin(np.linalg.norm(u + u[j], axis=1)))
    key = frozenset((i, j, mi, mj))
    if key not in [r[0] for r in R]: R.append((key, [K[i].tolist(), K[j].tolist(), K[mi].tolist(), K[mj].tolist()]))
assert len(R) == 15
J = json.load(open('data/polar-gsd-render.json')); J['rects'] = [r[1] for r in R]
json.dump(J, open('data/polar-rect-render.json', 'w'))
