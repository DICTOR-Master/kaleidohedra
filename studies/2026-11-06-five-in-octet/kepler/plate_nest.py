# Figure 1, plate style: the nest down a three-fold axis; octahedron as skeleton, icosahedron and dodecahedron as tinted glass, cube glass,
# tetrahedron solid; construction: golden points (rings), the octahedron's face centres = the cube's corners (crosses), dotted rays.
import numpy as np
from davinci import Plate, look, SEPIA
exec(open('../scripts/nest.py').read().split("def inside")[0])
pl = Plate(look((1, 1, 1), (0, 0, 1)), scale=0.34 * 2600 * 1.55)
pl.skeleton(O, 7, 235)
pl.glass(I, (150, 176, 226), a_back=22, which='back'); pl.glass(D, (190, 160, 214), a_back=30, which='back')
c0 = np.zeros(3)
for p in O: pl.dashed(pl.P(c0), pl.P(p), SEPIA + (70,), 2, dash=10)
fc = [O[idx].mean(0) for n, idx in Plate.faces(O)]
for p in fc: pl.dashed(pl.P(c0), pl.P(p), SEPIA + (90,), 2, dash=10)
pl.glass(C, (170, 210, 160), a_front=80, a_back=35, which='both')
pl.solid(T, (190, 82, 54))
pl.glass(D, (196, 168, 220), a_front=26, edge=170, which='front'); pl.glass(I, (160, 186, 232), a_front=18, edge=200, w=4, which='front')
for p in I: pl.ring(p)
for p in fc: pl.cross(p)
pl.save('../plate-nest.png', 'Five in the Octet · the nest in one octahedron'); print('ok')
