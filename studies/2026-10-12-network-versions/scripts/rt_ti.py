# DICTO 2026-10-12: "the triangles of rhombi mirroring the hexagons of the fullerene cage". The rhombic triacontahedron (RT) and the
# truncated icosahedron (TI): the cage's 12 pentagons face RT's 12 five-fold corners, its 20 hexagons RT's 20 three-fold corners
# (three rhombi). Test: scale the cage so its corners touch RT's faces; is RT then exactly the cage + one cap per cage face (apex at
# the RT corner over it)? Volumes and containment checked.
import itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('network_screen.py').read().split('def sat_overlap')[0].replace('print(', '(lambda *a, **k: None)('))
def faces(V):
    E = []
    for e in ConvexHull(V).equations:
        if not any(np.linalg.norm(e - q) < 1e-7 for q in E): E.append(e)
    return np.array(E)
RT = ref['RT']; TI0 = ref['TI']; FR = faces(RT)
s = 1 / max((TI0 @ FR[:, :3].T).max(axis=1) / (-FR[:, 3]).max())   # largest TI inside RT (touching)
TI = TI0 * s
touch = np.abs((TI @ FR[:, :3].T + FR[:, 3]).max(axis=1)) < 1e-9
print(f'cage scaled to edge {s:.6f} (RT edge 1): {touch.sum()} of 60 cage corners lie on RT faces')
FT = faces(TI); caps = []
for f in FT:
    on = TI[np.abs(TI @ f[:3] + f[3]) < 1e-9]
    n = f[:3] / np.linalg.norm(f[:3]); apex = RT[np.argmax(RT @ n)]
    caps.append((len(on), np.vstack([on, apex])))
vRT, vTI = ConvexHull(RT).volume, ConvexHull(TI).volume
vc = sum(ConvexHull(c).volume for _, c in caps)
inside = all(np.all(c @ FR[:, :3].T + FR[:, 3] <= 1e-9) for _, c in caps)
print(f'RT {vRT:.6f} vs cage {vTI:.6f} + {len(caps)} caps {vc:.6f} = {vTI + vc:.6f}; caps inside RT: {inside}')
from collections import Counter
print('caps:', dict(Counter(f'{n}-gon base' for n, _ in caps)))
# the leftover: candidate wedge per hexagon-hexagon edge of the cage = hull(that edge + the RT corners over its two hexagons +
# the RT corners over the pentagons at its ends? -> use the two three-fold apexes and the two cage corners)
E = [(a, b) for a, b in itertools.combinations(range(60), 2) if abs(np.linalg.norm(TI[a] - TI[b]) - s) < 1e-9]
hexf = [f for f in FT if np.sum(np.abs(TI @ f[:3] + f[3]) < 1e-9) == 6]
apex = lambda f: RT[np.argmax(RT @ (f[:3] / np.linalg.norm(f[:3])))]
wedges = []
for a, b in E:
    hs = [f for f in hexf if abs(TI[a] @ f[:3] + f[3]) < 1e-9 and abs(TI[b] @ f[:3] + f[3]) < 1e-9]
    if len(hs) == 2: wedges.append(np.vstack([TI[a], TI[b], apex(hs[0]), apex(hs[1])]))
vw = sum(ConvexHull(w).volume for w in wedges)
print(f'{len(wedges)} hexagon-hexagon edges; tetrahedral wedge (edge + the two three-fold corners) volume each {ConvexHull(wedges[0]).volume:.6f}, '
      f'all {vw:.6f}; cage + caps + wedges = {vTI + vc + vw:.6f} vs RT {vRT:.6f}')
pentf = [f for f in FT if np.sum(np.abs(TI @ f[:3] + f[3]) < 1e-9) == 5]
w2 = []
for a, b in E:
    ps = [f for f in pentf if abs(TI[a] @ f[:3] + f[3]) < 1e-9 and abs(TI[b] @ f[:3] + f[3]) < 1e-9]
    hs = [f for f in hexf if abs(TI[a] @ f[:3] + f[3]) < 1e-9 and abs(TI[b] @ f[:3] + f[3]) < 1e-9]
    if len(ps) == 1 and len(hs) == 1: w2.append(np.vstack([TI[a], TI[b], apex(ps[0]), apex(hs[0])]))
v2 = sum(ConvexHull(w).volume for w in w2)
ins = all(np.all(w @ FR[:, :3].T + FR[:, 3] <= 1e-9) for w in w2)
ed = sorted(np.round([np.linalg.norm(w2[0][i] - w2[0][j]) for i, j in itertools.combinations(range(4), 2)], 6))
print(f'{len(w2)} pentagon-hexagon edges; wedge = edge + the five-fold and three-fold corners over its two faces: volume each '
      f'{ConvexHull(w2[0]).volume:.6f}, edges {ed}; inside RT {ins}; cage + caps + wedges = {vTI + vc + v2:.6f} vs RT {vRT:.6f}')
