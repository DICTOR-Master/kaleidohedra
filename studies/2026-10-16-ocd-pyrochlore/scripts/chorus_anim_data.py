# Data for the chorus renders: the five voices (inscribed cubes of the dodecahedron of hexagon directions), ordered by the
# 72-degree turn about a five-fold axis, as the 8 joined-copy offsets of each voice.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('scripts/chorus_space.py').read().split('def lattice(')[0])
voices = [[(2 * h * U[i]).tolist() for i in c] for c in cubes]
up = next(v for v in np.vstack([U, -U]) if abs(v @ a5) < 0.95)           # any direction off the axis, made perpendicular below
up = up - (up @ a5) * a5; up /= np.linalg.norm(up)
json.dump({'voices': voices, 'a5': a5.tolist(), 'up': up.tolist()}, open('data/chorus-anim.json', 'w'))
print('voices', len(voices), 'shared corners between consecutive voices', [len({tuple(np.round(v, 6)) for v in voices[k]} & {tuple(np.round(v, 6)) for v in voices[(k + 1) % 5]}) for k in range(5)])
