# Figure 2b, plate style: UNITY with nests, down a five-fold axis (through a pentagon of the icosidodecahedron).
import json, numpy as np
from davinci import Plate, look, SEPIA
d = json.load(open('~/k-research/studies/2026-11-06-nest-supercells/unity-nests.json'))
ID = np.array(d['ID']); Is = [np.array(v) for v in d['icos']]; Ns = [{k: np.array(v) for k, v in n.items()} for n in d['nests']]
caps = [np.array(v) for v in d['caps']]; heart = np.array([c[-1] for c in caps])
n5 = Is[0].mean(0) / np.linalg.norm(Is[0].mean(0))
pl = Plate(look(n5, np.cross(n5, [1, 0.3, 0.1])), scale=0.24 * 2600 / 1.55)
pl.glass(ID, (230, 214, 170), a_back=28, a_front=0, which='back'); pl.skeleton(ID, 4, 150)
pl.glass(heart, (230, 190, 110), a_front=70, a_back=30, edge=170, which='both')
for k in sorted(range(12), key=lambda k: pl.z(Is[k].mean(0))):
    I = Is[k]; N = Ns[k]
    pl.glass(I, (160, 186, 232), a_back=20, a_front=0, which='back')
    pl.solid(N['T'], (190, 82, 54), w=2)
    pl.glass(N['D'], (196, 168, 220), a_front=22, edge=110, w=2, which='front')
    pl.glass(I, (160, 186, 232), a_front=16, edge=170, w=3, which='front')
pl.save('../plate-unity.png', 'UNITY with nests · the 600-cell’s middle slice'); print('ok')
