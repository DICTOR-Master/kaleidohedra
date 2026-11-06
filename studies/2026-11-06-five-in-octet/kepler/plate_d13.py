# Figure 2a, plate style: the nested Dodeca-13 (the 120-cell's 1 + 12) down a five-fold axis through two opposite faces of the centre.
import json, numpy as np
from davinci import Plate, look, SEPIA
d = json.load(open('/home/dicto/k-research/studies/2026-11-06-nest-supercells/nest13-aligned.json'))
Ds = [np.array(v) for v in d['dodecahedra']]; Ns = [{k: np.array(v) for k, v in n.items()} for n in d['nests']]
ci = int(np.argmin([np.linalg.norm(V.mean(0)) for V in Ds])); c = Ds[ci].mean(0)
n5 = Plate.faces(Ds[ci])[0][0]
up = np.cross(n5, [1, 0, 0]); up = up if np.linalg.norm(up) > 0.1 else np.cross(n5, [0, 1, 0])
pl = Plate(look(n5, up), scale=0.24 * 2600 / 1.9, centre=c)
order = sorted(range(13), key=lambda k: pl.z(Ds[k].mean(0)))
for k in order:
    V = Ds[k]; N = Ns[k]; centre = k == ci
    pl.glass(V, (196, 168, 220), a_back=16 if not centre else 26, a_front=14 if not centre else 24, edge=120, which='back')
    pl.glass(N['I'], (160, 186, 232), a_back=14, a_front=0, which='back')
    pl.solid(N['T'], (190, 82, 54), w=2)
    pl.glass(N['C'], (170, 210, 160), a_front=40, a_back=0, edge=110, w=2, which='front')
    pl.glass(N['I'], (160, 186, 232), a_front=10, edge=110, w=2, which='front')
    pl.skeleton(V, 5 if not centre else 6, 200, hidden=False)
pl.save('../plate-dodeca13.png', 'The nested Dodeca-13 · the 120-cell’s first shell'); print('ok')
