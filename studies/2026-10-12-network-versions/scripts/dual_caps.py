# DICTO 2026-10-12: the Lotus shell is an icosahedron separating into pentagonal elements at its 12 corners; look for the dual: a
# dodecahedron with triangular structures at its 20 corners. Check: cutting each form's corners back to the edge midpoints leaves
# the same core, the icosidodecahedron; the icosahedron's 12 corner pieces are pentagonal pyramids, the dodecahedron's 20 are
# triangular pyramids. Volumes and shapes checked.
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
def edges(V):
    d = min(np.linalg.norm(V[0] - w) for w in V[1:]); return [(a, b) for a, b in itertools.combinations(range(len(V)), 2) if abs(np.linalg.norm(V[a] - V[b]) - d) < 1e-9]
for X in ('I', 'D'):
    V = ref[X]; E = edges(V); M = np.array([(V[a] + V[b]) / 2 for a, b in E])
    core = ConvexHull(M); nb = [[(V[a] + V[b]) / 2 for a, b in E if k in (a, b)] for k in range(len(V))]
    caps = [np.vstack([V[k]] + nb[k]) for k in range(len(V))]
    vX, vcore, vcaps = ConvexHull(V).volume, core.volume, sum(ConvexHull(c).volume for c in caps)
    ecore = min(np.linalg.norm(M[0] - w) for w in M[1:])
    print(f'{X} (edge 1): corners cut to the edge midpoints leave an icosidodecahedron of edge {ecore:.6f} '
          f'({len(M)} corners); {len(V)} corner pieces, each a pyramid on a {len(nb[0])}-gon (side {ecore:.6f}, side edges {0.5:.1f}); '
          f'volumes: core {vcore:.6f} + pieces {vcaps:.6f} = {vcore + vcaps:.6f} vs {X} {vX:.6f}')
