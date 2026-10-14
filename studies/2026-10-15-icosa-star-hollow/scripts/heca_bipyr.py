# The Cleo core to the Hecatodihedron with DICTO's chosen fusion (2026-10-15): each Cleo-Ico + Dharma's triangular pyramid on the same
# triangle = one triangular bipyramid (20). Confirms the hull's faces (planes merged at 1e-4) and writes the render data.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
J = json.load(open('cleo_heca.json')); FU = json.load(open('cleo_heca_fusions.json'))
P = lambda m: np.array(m['v'])
kinds = {k: [P(m) for m in L] for k, L in J.items() if k not in ('Cleo-Ico', 'tripyr (to dodecahedron)')}
kinds['bipyramid (Cleo-Ico + dodecahedron corner)'] = [P(m) for m in FU['Cleo-Ico + tripyr (to dodecahedron)']]
allp = [Q for L in kinds.values() for Q in L]
H = ConvexHull(np.vstack(allp)); planes = []
for e in H.equations:
    if not any(np.linalg.norm(e - p) < 1e-4 for p in planes): planes.append(e)
pts = H.points[H.vertices]; uniq = np.unique(np.round(pts, 4), axis=0)
sides = {}
for e in planes:
    n = sum(1 for p in uniq if abs(p @ e[:3] + e[3]) < 1e-4); sides[n] = sides.get(n, 0) + 1
vol = lambda Q: ConvexHull(Q).volume
out = [f'pieces: ' + ', '.join(f'{len(L)} {k}' for k, L in kinds.items()) + f' = {len(allp)}',
       f'hull: {len(planes)} faces (by corners per face {dict(sorted(sides.items()))}), {len(uniq)} corners; pieces {sum(map(vol, allp)):.6f} vs hull {H.volume:.6f}',
       f'bipyramid: {len(kinds["bipyramid (Cleo-Ico + dodecahedron corner)"][0])} corners, edges ' + str(sorted({round(np.linalg.norm(a - b), 4) for a, b in itertools.combinations(kinds["bipyramid (Cleo-Ico + dodecahedron corner)"][0], 2)}))]
print('\n'.join(out)); open('heca_bipyr.txt', 'w').write('\n'.join(out) + '\n')
mesh = lambda Q: {'v': np.round(Q, 6).tolist(), 'f': ConvexHull(Q).simplices.tolist(), 'c': np.round(Q.mean(0), 6).tolist()}
json.dump({k: [mesh(Q) for Q in L] for k, L in kinds.items()}, open('heca_bipyr.json', 'w'))
